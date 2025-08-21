# Project Assumptions

## Technical Assumptions

1. **Browser Support**: Modern browsers only (Chrome/Edge/Firefox/Safari latest 2 versions)
2. **JavaScript Enabled**: Application requires JavaScript to function
3. **WebSocket Support**: Target browsers support WebSocket protocol
4. **Network**: Users have stable internet connection for real-time features
5. **Screen Size**: Minimum viewport of 320px width (mobile)

## Domain Assumptions  

1. **Session Size**: Teams typically have 3-16 members (as per PRD)
2. **Session Duration**: Most planning sessions complete within 2 hours
3. **Voting Patterns**: Teams use standard Fibonacci sequence for estimates
4. **Coffee Break**: "Coffee" card indicates need for break, not an estimate
5. **Scrum Master**: Every session needs one facilitator with control privileges

## User Behavior Assumptions

1. **Name Uniqueness**: Users will choose distinguishable names within a session
2. **Avatar Selection**: Default avatars sufficient (no custom upload needed)
3. **Reconnection**: Users will attempt to rejoin if disconnected
4. **Device Switching**: Users stay on same device during session
5. **Browser Storage**: Users allow localStorage for preferences

## Data & Privacy Assumptions

1. **No PII Storage**: System doesn't need to store personal information
2. **Session Privacy**: Sessions are semi-public (anyone with link can join)
3. **Data Retention**: No historical data needed after session ends
4. **GDPR**: No special GDPR compliance needed (no persistent user data)

## Performance Assumptions

1. **Concurrent Load**: Maximum 3 sessions × 16 users = 48 concurrent users
2. **Message Frequency**: Average 1-2 actions per user per minute during voting
3. **Bandwidth**: Each client uses <100KB/minute of bandwidth
4. **Server Resources**: Single server instance sufficient for load

## Security Assumptions

1. **Authentication**: No user authentication required (session-based only)
2. **Authorization**: Scrum Master role sufficient for access control
3. **Data Sensitivity**: Planning poker data is not sensitive
4. **Attack Surface**: Input validation sufficient for security

## Development Assumptions

1. **Timeline**: MVP can be completed with core features first
2. **Iterations**: UI can be refined based on user feedback
3. **Testing**: Automated tests can cover critical paths
4. **Deployment**: Standard web hosting environment available