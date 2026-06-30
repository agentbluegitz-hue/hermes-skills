# Active Interaction Workflow Preferences

When actively interacting with the user in a live session, follow these workflow preferences to ensure immediate responsiveness and avoid confusion:

## Immediate Updates vs Cron Jobs

**User Preference**: During active conversation sessions, make direct updates to systems (like GitHub repositories) immediately rather than waiting for scheduled cron jobs to run.

### Why This Matters
- Prevents confusion when the user expects to see immediate results from their requests
- Eliminates uncertainty about whether changes have been applied
- Provides real-time feedback during collaborative work sessions
- Respects the user's time and desire for prompt completion of requested tasks

### Implementation
When the user requests updates to:
- GitHub repositories
- Website content
- Skill configurations
- Or any other system that has both direct update mechanisms and cron-based automation

**Do**: Perform the update directly using appropriate CLI/git commands during the session
**Do Not**: Wait for or rely solely on cron jobs to propagate changes during active interaction

### Verification
After making direct changes during a session:
1. Verify the changes are present in the target system
2. Confirm the user can see/access the updates immediately
3. Only then consider the task complete

### Background Operations
Cron jobs remain valuable for:
- Background maintenance when no active session is occurring
- Routine periodic tasks that don't require immediate user feedback
- Backup and synchronization processes
- Non-time-sensitive automation

But during active user interaction, prioritize direct, immediate updates to maintain trust and clarity in the collaboration.

## Related Practices
- Always provide clear commit messages that describe what was changed and why
- Verify connectivity and access permissions before attempting updates
- Use appropriate tools for the task (git, rsync, API calls, etc.)
- Handle errors gracefully and inform the user of any issues immediately