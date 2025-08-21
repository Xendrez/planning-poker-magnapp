#!/usr/bin/env python3
import os
import sys
import json
import time
from pathlib import Path
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError
from shutil import which
from datetime import datetime

# --- Minimal .env loader (optional) -----------------------------------------
# Loads KEY=VALUE pairs from a .env file if present, without external deps.
# Supports simple lines; ignores comments and blank lines.

def load_dotenv_minimal():
    # Try CWD, script dir, and project root
    candidates = [
        Path.cwd() / ".env",
        Path(__file__).resolve().parent.parent.parent / ".env",
        Path.home() / ".env",
    ]
    for p in candidates:
        if p.exists() and p.is_file():
            try:
                for line in p.read_text(encoding="utf-8").splitlines():
                    line = line.strip()
                    if not line or line.startswith('#'):
                        continue
                    if '=' in line:
                        k, v = line.split('=', 1)
                        k = k.strip()
                        v = v.strip().strip('"').strip("'")
                        # Do not overwrite if already set in the environment
                        if k and (k not in os.environ):
                            os.environ[k] = v
            except Exception as e:
                print(f"[HOOK] .env load failed from {p}: {e}", file=sys.stderr)

load_dotenv_minimal()

print("[HOOK] notification.py invoked", file=sys.stderr)

# Breadcrumb for debugging hook invocation
try:
    with open(Path.home() / ".claude_hook_probe.log", "a") as f:
        f.write(f"notification fired at {datetime.now().isoformat()}\n")
except Exception as e:
    print(f"[HOOK] breadcrumb write failed: {e}", file=sys.stderr)

# --- Read stdin payload safely ----------------------------------------------
try:
    data = json.load(sys.stdin)
except Exception as e:
    print(f"[HOOK] Failed to parse stdin JSON: {e}", file=sys.stderr)
    data = {}

# Default message can be tailored; you may also inspect `data` for tool/message
text = data.get("message") or "Heey! Claude just finished and needs you!"

api_key = os.getenv("ELEVENLABS_API_KEY")
voice_id = os.getenv("JINX_VOICE_ID") or os.getenv("LAURA_VOICE_ID") or os.getenv("ELEVEN_VOICE_ID")
# Create a unique filename based on the text and voice
import hashlib
text_hash = hashlib.md5((text + str(voice_id)).encode('utf-8')).hexdigest()
output_dir = Path.home() / ".claude" / "tts_cache"
output_dir.mkdir(parents=True, exist_ok=True)
output_path = output_dir / f"{text_hash}.mp3"

if not api_key:
    print("[EL] Missing ELEVENLABS_API_KEY", file=sys.stderr)
if not voice_id:
    print("[EL] Missing JINX_VOICE_ID/LAURA_VOICE_ID/ELEVEN_VOICE_ID", file=sys.stderr)
    
# Check if we already have this TTS cached
if output_path.exists():
    print(f"[CACHE] Using cached TTS for text: {text[:30]}...", file=sys.stderr)
    sys.exit(0) if play_audio(output_path) else sys.exit(1)

# --- Build ElevenLabs request ------------------------------------------------
print(f"[TTS] Generating new TTS for: {text}", file=sys.stderr)
body = json.dumps({
    "text": text,
    "voice_settings": {
        "stability": 0.6,
        "similarity_boost": 0.7
    }
}).encode("utf-8")

url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"
req = Request(
    url=url,
    data=body,
    headers={
        "xi-api-key": api_key or "",
        "Content-Type": "application/json",
        "accept": "audio/mpeg",
    },
    method="POST",
)

status = None
response_bytes = b""
try:
    with urlopen(req, timeout=30) as resp:
        status = resp.getcode()
        response_bytes = resp.read()
except HTTPError as e:
    status = e.code
    try:
        err_body = e.read().decode("utf-8", errors="ignore")
    except Exception:
        err_body = str(e)
    print(f"[EL] HTTPError status={status}", file=sys.stderr)
    print(f"[EL] body={err_body[:400]}", file=sys.stderr)
except URLError as e:
    print(f"[EL] URLError: {e}", file=sys.stderr)
except Exception as e:
    print(f"[EL] Unexpected error: {e}", file=sys.stderr)

if status == 200 and response_bytes:
    try:
        with open(output_path, "wb") as f:
            f.write(response_bytes)
        print(f"[EL] Wrote audio to {output_path}", file=sys.stderr)
    except Exception as e:
        print(f"[EL] Failed to write audio: {e}", file=sys.stderr)
else:
    # If the API returned JSON error content instead of audio, try to print it
    try:
        txt = response_bytes.decode("utf-8") if response_bytes else ""
        if txt:
            print(f"[EL] Non-200 or empty response body: {txt[:400]}", file=sys.stderr)
    except Exception:
        pass
    # Exit non-blocking with status 0 so hooks pipeline continues, but we log
    sys.exit(0)

# --- Playback ---------------------------------------------------------------

def play_audio(path: Path):
    if which("afplay"):
        os.system(f"afplay {path}")
        return True
    if which("ffplay"):
        os.system(f"ffplay -nodisp -autoexit {path}")
        return True
    print("[AUDIO] No player found. Install ffmpeg (for ffplay) or rely on macOS 'afplay'", file=sys.stderr)
    return False

ok = play_audio(output_path)
if not ok:
    print("[AUDIO] Playback skipped (no player found)", file=sys.stderr)
