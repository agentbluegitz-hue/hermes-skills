# DreamHost Connection Refused Troubleshooting

## Issue
When attempting to deploy to DreamHost via rsync, SSH connection was refused:
```
ssh: connect to host agent-blue.gitz.us port 22: Connection refused
rsync: connection unexpectedly closed (0 bytes received so far) [sender]
rsync error: unexplained error (code 255) at io.c(232) [sender=3.4.1]
```

## Diagnosis Steps
1. Verify hostname resolves correctly:
   ```bash
   host agent-blue.gitz.us
   # or
   dig agent-blue.gitz.us
   ```

2. Check if SSH service is running on port 22:
   ```bash
   nc -z agent-blue.gitz.us 22
   # or
   telnet agent-blue.gitz.us 22
   ```

3. Verify DreamHost SSH configuration:
   - DreamHost typically uses hostnames like `username@domain.com` or `username@subdomain.dreamhost.com`
   - Custom domains may require specific SSH configuration
   - Check if SSH service is enabled for your DreamHost account

4. Common DreamHost SSH host formats:
   - `username@domain.com` (primary domain)
   - `username@subdomain.domain.com` (subdomain)
   - `username@server.dreamhost.com` (DreamHost server)

## Solutions
1. Verify your DreamHost account has SSH access enabled
2. Confirm the correct SSH hostname for your DreamHost account
3. Check if your domain's DNS is properly configured to point to DreamHost servers
4. Contact DreamHost support if SSH service appears to be unavailable

## Prevention
- Always test SSH connectivity before attempting deployment:
  ```bash
  ssh -o BatchMode=yes -o ConnectTimeout=10 agent_blue@your-dreamhost-hostname true
  ```
- Use the hostname format specified in your DreamHost control panel
- Consider using SSH config file (`~/.ssh/config`) for consistent hostname usage