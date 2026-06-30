# SSH Troubleshooting Reference

Common issues and solutions for SSH connections to agent-blue.gitz.us

## Connection Refused Errors

### Symptom
```
ssh: connect to host agent-blue.gitz.us port 22: Connection refused
```

### Possible Causes
1. SSH service not running on remote host
2. Firewall blocking port 22
3. Incorrect hostname or IP address
4. Remote host not accessible

### Solutions
1. Verify the host is reachable:
   ```bash
   ping agent-blue.gitz.us
   ```
2. Check if SSH port is open:
   ```bash
   nc -z agent-blue.gitz.us 22
   ```
   or
   ```bash
   timeout 5 bash -c '</dev/tcp/agent-blue.gitz.us/22' 2>/dev/null && echo "Port 22 open" || echo "Port 22 closed"
   ```
3. Contact system administrator to ensure SSH service is running
4. Verify DNS resolution:
   ```bash
   host agent-blue.gitz.us
   ```

## Permission Denied Errors

### Symptom
```
Permission denied (publickey,password,keyboard-interactive).
```
or
```
Received disconnect from 173.236.255.19 port 22:2: Too many authentication failures
```

### Possible Causes
1. SSH key not properly installed
2. Public key not in authorized_keys on remote host
3. Key file permissions too open
4. SSH agent not running or key not loaded

### Solutions
1. Verify key file permissions:
   ```bash
   chmod 600 ~/.ssh/id_ed25519
   chmod 644 ~/.ssh/id_ed25519.pub
   ```
2. Ensure SSH agent is running and key is loaded:
   ```bash
   eval $(ssh-agent)
   ssh-add ~/.ssh/id_ed25519
   ```
3. Test connection with verbose output:
   ```bash
   ssh -v -i ~/.ssh/id_ed25519 agent-blue.gitz.us
   ```
4. Check that the public key is in `~/.ssh/authorized_keys` on the remote host
5. Ensure you're using the correct key file (check for multiple identities)

## Rsync Specific Issues

### Symptom
```
rsync: connection unexpectedly closed (0 bytes received so far) [sender]
rsync error: unexplained error (code 255) at io.c(232)
```

### Possible Causes
1. SSH connection dropped during transfer
2. Remote command not found (rsync not installed on remote host)
3. Incompatible rsync versions
4. Shell issues on remote host

### Solutions
1. Verify rsync is installed on remote host:
   ```bash
   ssh agent-blue.gitz.us "which rsync"
   ```
2. Try a simple SSH command first to verify connectivity
3. Check remote shell environment:
   ```bash
   ssh agent-blue.gitz.us "echo $SHELL"
   ```
4. Use rsync with SSH options to debug:
   ```bash
   rsync -avz -e "ssh -v" site/ agent-blue.gitz.us:~/public_html/
   ```

## Post-Quantum Warning

### Symptom
```
** WARNING: connection is not using a post-quantum key exchange algorithm.
** This session may be vulnerable to "store now, decrypt later" attacks.
```

### Explanation
This is a warning from newer OpenSSH versions about using non-post-quantum key exchange algorithms. It does not prevent the connection from working but indicates the cryptography used may be vulnerable to future quantum attacks.

### Solutions
1. This warning is informational and does not affect connection functionality
2. To suppress, update OpenSSH to a version that supports post-quantum algorithms
3. The connection will work normally despite this warning

## General Debugging Steps

1. Test basic connectivity:
   ```bash
   ping -c 3 agent-blue.gitz.us
   ```
2. Test SSH port:
   ```bash
   nc -zv agent-blue.gitz.us 22
   ```
3. Test SSH login with verbose mode:
   ```bash
   ssh -v -i ~/.ssh/id_ed25519 agent-blue.gitz.us true
   ```
4. Check local SSH configuration:
   ```bash
   cat ~/.ssh/config
   ```
5. Verify known hosts:
   ```bash
   ssh-keygen -R agent-blue.gitz.us
   ssh-keyscan agent-blue.gitz.us >> ~/.ssh/known_hosts
   ```

## When All Else Fails

1. Contact the system administrator for agent-blue.gitz.us
2. Verify the hosting service is active and not suspended
3. Check if there are any network restrictions or firewall rules blocking access
4. Consider using an alternative deployment method if SSH is consistently problematic