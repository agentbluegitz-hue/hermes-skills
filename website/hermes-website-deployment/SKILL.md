---
name: hermes-website-deployment
description: "Update and deploy the Hermes Agent website built with Zensical to either DreamHost via rsync or GitHub Pages."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux]
---

# Hermes Agent Website Deployment

This skill outlines the process for updating and deploying the Hermes Agent website, which is built with Zensical and can be deployed to either DreamHost via rsync or GitHub Pages.

## Trigger Conditions\\n- The Hermes Agent website source code has been updated\\n- Scheduled cron job for website updates\\n- Manual request to update the website\\n- User feedback indicating image sizing or loading issues (e.g., requests to scale images down or fix broken links)\\n- Need to diagnose and resolve SSH authentication issues for DreamHost deployment

## Preparation\\\\\\\\\\\\\\\\n1. Ensure you are in the Hermes Agent website directory:\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\n   ```bash\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\n   cd /home/agent-blue/.hermes/website\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\n   ```\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\n2. Verify you have the necessary permissions and SSH access to the deployment target (`agent_blue@iad1-shared-b8-40.dreamhost.com`).\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\n3. **CRITICAL**: For Zensical-based sites, ALL content updates MUST go in the `/docs` folder, NEVER in the `/site` folder. The `/site` folder is generated automatically by Zensical from the `/docs` content. Editing `/site` directly will result in lost changes when the site is rebuilt.\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\n4. For personalization, prepare any custom images (like avatars) to be placed in `docs/assets/images/`. **User preference**: Scale avatar images to 50% size (e.g., 250x250px from 1000x1000px) for better page load and layout. Use FFmpeg with the command: `ffmpeg -y -i input.png -vf \\\\\\\"scale=iw*0.5:ih*0.5\\\\\\\" -vframes 1 output.png`\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\n5. Ensure website content includes appropriate disclaimers stating that the site reflects personal experience and is not an official Hermes Agent site.\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\n6. **Important**: When using Markdown for Zensical sites, use relative paths for assets (e.g., `![Alt text](assets/images/photo.png)`) rather than absolute paths (`![Alt text](/assets/images/photo.png)`) to ensure proper loading when deployed to GitHub Pages or subdirectory paths.\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\n7. **Important**: Use reliable placeholder services like `placehold.co` instead of `via.placeholder.com` for consistent image loading, as the former service was experiencing connectivity issues. Verify placeholder images load with `curl -s -o /dev/null -w \\\\\\\"%{http_code}\\\\\\\" URL`.\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\n8. **Note**: Before building, check if a virtual environment already exists (e.g., `/tmp/zensical_env/`). If so, activate it with `source /tmp/zensical_env/bin/activate`. Otherwise, create a new virtual environment using your preferred method (uv, venv, etc.).\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\n9. **Important**: For GitHub Actions workflows, ensure proper syntax for accessing secrets: use `${{ secrets.GITHUB_TOKEN }}` (not `*** secrets.GITHUB_TOKEN }}`). Validate workflow files before committing to avoid deployment failures.

## Steps

### 1. Update Source Code
```bash
# Pull latest changes from GitHub
git pull

# Check for local changes
if ! git diff-index --quiet HEAD --; then
  echo "Local changes detected. Committing..."
  git add .
  git commit -m "Automated update: $(date -Iseconds)"
  git push
  echo "Changes pushed to GitHub."
else
  echo "No local changes to commit."
fi
```

### 2. Build the Site\nThe website is built using Zensical. Ensure Zensical is installed in a virtual environment or via pipx.\n\n#### Install Zensical (if needed)\n```bash\n# Check if a virtual environment already exists (e.g., from automated scripts)\nif [ -d \"/tmp/zensical_env\" ]; then\n  echo \"Using existing virtual environment at /tmp/zensical_env\"\n  source /tmp/zensical_env/bin/activate\nelse\n  # Create a virtual environment if not present\n  uv venv\n  source .venv/bin/activate\n  uv pip install zensical\nfi\n\n# If not already installed in the active environment, install Zensical\nif ! pip list | grep -q zensical; then\n  pip install zensical\nfi\n```\n\n#### Build the site\n```bash\nzensical build\n```\nThis generates the static site in the `site/` directory.

### 3. Deploy to DreamHost
Deploy the built site to DreamHost using rsync over SSH.

#### Verify SSH connectivity
```bash
ssh -i ~/.ssh/id_ed25519 -o BatchMode=yes -o PreferredAuthentications=publickey agent-blue.gitz.us true
```
If this fails, check:
- SSH key is correctly installed in `~/.ssh/id_ed25519`
- The public key is in `~agent-blue/.ssh/authorized_keys` on the remote host
- The SSH daemon is running on the remote host and accessible on port 22

#### Deploy with rsync
```bash
rsync -avz --delete site/ agent-blue.gitz.us:~/public_html/
```
Note: The `--delete` flag ensures the destination mirrors the source, removing files not present in the source.

### 4. Verification
After deployment, verify the site is accessible:
- Visit `https://agent-blue.gitz.us/` in a browser
- Check for any error messages in the browser console

- **SSH Key Rejected**: If SSH connection fails with "Permission denied (publickey,password,keyboard-interactive)" despite the key being offered in verbose output, the remote host rejected the public key. Solutions:
  1. Verify the public key being offered (`cat ~/.ssh/id_ed25519.pub`) matches what's in the remote host's `~/.ssh/authorized_keys`
  2. Add the public key to `~/.ssh/authorized_keys` on the remote host
  3. Ensure no extra characters or whitespace in the authorized_keys entry
  4. Check that the remote SSH user matches the expected username (in this case, 'agent-blue')
  5. Verify the remote host's SSH configuration allows publickey authentication
  - **Post-Quantum Warning Informational**: Newer OpenSSH versions show a warning about non-post-quantum key exchange algorithms. This warning is informational and does not prevent connection functionality. The connection will work normally despite this warning.
  - **Avatar Image Too Large**: Large avatar images (e.g., 1000x1000px) can slow page loading. Scale images to appropriate size (e.g., 50% for 250x250px) using FFmpeg: `ffmpeg -y -i input.png -vf \\\\\\\\\\\\\\\"scale=iw*0.5:ih*0.5\\\\\\\\\\\\\\\" -vframes 1 output.png`\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\

## References\\\\\\\\n- For details on the Zensical configuration, see `references/zensical-config.md`\\\\\\\\n- For troubleshooting SSH issues, see `references/ssh-troubleshooting.md`\\\\\\\\n- For DreamHost SSH key setup procedures, see `references/dreamhost-ssh-key-setup.md`\\\\\\\\n- For personalization and disclaimer guidelines, see `references/personalization-and-disclaimers.md`\\\\\\\\n- For fixing image path issues when deploying to GitHub Pages, see `references/github-pages-image-paths.md`\\\\\\\\n- For scaling avatar images to 50% size for better page load and layout, see `references/avatar-scaling.md`

## Related Skills\n- `hermes-agent` (for general Hermes Agent configuration)\n- Active interaction workflow preferences: see `references/active-interaction-workflow.md`