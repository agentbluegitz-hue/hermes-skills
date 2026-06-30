# DreamHost SSH Key Setup for Hermes Agent Website

## Overview
This guide explains how to set up SSH key authentication for deploying the Hermes Agent website to DreamHost via rsync.

## Prerequisites
- SSH access to your DreamHost account
- Local SSH key pair (id_ed25519/id_ed25519.pub) already generated
- Username for DreamHost (typically your panel username)

## Step-by-Step Setup

### 1. Verify Local SSH Key
```bash
# Check if key exists
ls -la ~/.ssh/id_ed25519*

# View public key
cat ~/.ssh/id_ed25519.pub
```

### 2. Copy Public Key to DreamHost
There are two main methods:

#### Method A: Using ssh-copy-id (if available)
```bash
ssh-copy-id -i ~/.ssh/id_ed25519.pub agent-blue@agent-blue.gitz.us
```

#### Method B: Manual Installation
```bash
# Create .ssh directory on remote host if it doesn't exist
ssh agent-blue@agent-blue.gitz.us "mkdir -p ~/.ssh && chmod 700 ~/.ssh"

# Append public key to authorized_keys
cat ~/.ssh/id_ed25519.pub | ssh agent-blue@agent-blue.gitz.us "cat >> ~/.ssh/authorized_keys && chmod 600 ~/.ssh/authorized_keys"
```

### 3. Verify Key Permissions on Remote Host
```bash
ssh agent-blue@agent-blue.gitz.us "
  echo 'Checking .ssh directory permissions:'
  ls -la ~/.ssh/
  echo ''
  echo 'Checking authorized_keys permissions:'
  ls -la ~/.ssh/authorized_keys
"
```

### 4. Test SSH Connection
```bash
# Test without password prompt
ssh -o BatchMode=yes -o PreferredAuthentications=publickey agent-blue@agent-blue.gitz.us true
echo "Exit code: $?"

# Or with verbose output to see authentication process
ssh -v -i ~/.ssh/id_ed25519 agent-blue@agent-blue.gitz.us true
```

## Troubleshooting

### Common Issues

#### "Permission denied (publickey,password,keyboard-interactive)"
- **Cause**: Public key not in authorized_keys or wrong permissions
- **Solution**: Verify key is in `~/.ssh/authorized_keys` and file is chmod 600

#### "Agent admitted failure to sign using the key"
- **Cause**: SSH agent not running or key not loaded
- **Solution**: 
  ```bash
  eval $(ssh-agent)
  ssh-add ~/.ssh/id_ed25519
  ```

#### "Connection refused" or "Connection timed out"
- **Cause**: Hostname wrong, SSH service not running, firewall blocking
- **Solution**: 
  ```bash
  ping agent-blue.gitz.us
  nc -z agent-blue.gitz.us 22
  ```

### DreamHost Specific Notes
- DreamHost typically uses your panel username as the SSH username
- The hostname is usually your domain or subdomain (e.g., agent-blue.gitz.us)
- Port 22 is standard for SSH
- Ensure your DreamHost user has SSH access enabled in the panel

## Automated Deployment Script Addition
To add this to your deployment workflow, you might add a verification step:

```bash
# In your deployment script
echo "Verifying SSH key authorization..."
ssh -o BatchMode=yes -o PreferredAuthentications=publickey agent-blue@agent-blue.gitz.us "echo 'SSH key auth successful'" || {
  echo "ERROR: SSH key authorization failed. Please check:"
  echo "1. Public key is in ~/.ssh/authorized_keys on remote host"
  echo "2. Correct username and hostname are being used"
  echo "3. SSH agent is running and key is loaded (ssh-add -l)"
  exit 1
}
```

## Related Resources
- [DreamHost SSH Keys Documentation](https://help.dreamhost.com/hc/en-us/articles/215489778-Overview-of-secure-shell-SSH)
- [OpenSSH Authorized Keys Format](https://man.openbsd.org/sshd#AUTHORIZED_KEYS_FILE_FORMAT)