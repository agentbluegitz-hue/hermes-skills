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

## Trigger Conditions\n- The Hermes Agent website source code has been updated\n- Scheduled cron job for website updates\n- Manual request to update the website\n- User feedback indicating image sizing or loading issues (e.g., requests to scale images down or fix broken links)

## Preparation\\\\\\\\n1. Ensure you are in the Hermes Agent website directory:\\\\\\\\\\\\\\\\n   ```bash\\\\\\\\\\\\\\\\n   cd /home/agent-blue/.hermes/website\\\\\\\\\\\\\\\\n   ```\\\\\\\\\\\\\\\\n2. Verify you have the necessary permissions and SSH access to the deployment target (`agent_blue@iad1-shared-b8-40.dreamhost.com`).\\\\\\\\\\\\\\\\n3. For personalization, prepare any custom images (like avatars) to be placed in `docs/assets/images/`. **User preference**: Scale avatar images to 50% size (e.g., 250x250px from 1000x1000px) for better page load and layout. Use FFmpeg with the command: `ffmpeg -y -i input.png -vf \\\"scale=iw*0.5:ih*0.5\\\" -vframes 1 output.png`\\\\\\\\\\\\\\\\n4. Ensure website content includes appropriate disclaimers stating that the site reflects personal experience and is not an official Hermes Agent site.\\\\\\\\\\\\\\\\n5. **Important**: When using Markdown for Zensical sites, use relative paths for assets (e.g., `![Alt text](assets/images/photo.png)`) rather than absolute paths (`![Alt text](/assets/images/photo.png)`) to ensure proper loading when deployed to GitHub Pages or subdirectory paths.\\\\\\\\\\\\\\\\n6. **Important**: Use reliable placeholder services like `placehold.co` instead of `via.placeholder.com` for consistent image loading, as the former service was experiencing connectivity issues. Verify placeholder images load with `curl -s -o /dev/null -w \\\"%{http_code}\\\" URL`.\\\\\\\\\\\\\\\\n7. **Note**: Before building, check if a virtual environment already exists (e.g., `/tmp/zensical_env/`). If so, activate it with `source /tmp/zensical_env/bin/activate`. Otherwise, create a new virtual environment using your preferred method (uv, venv, etc.).\\\\\\\\\\\\\\\\n8. **Important**: For GitHub Actions workflows, ensure proper syntax for accessing secrets: use `${{ secrets.GITHUB_TOKEN }}` (not `*** secrets.GITHUB_TOKEN }}`). Validate workflow files before committing to avoid deployment failures.

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

## Pitfalls and Troubleshooting\\\\\\\\n- **SSH Connection Refused**: Ensure the remote host is reachable and SSH service is running. Verify firewall settings and SSH port. If connection is refused, check:\\\\\\\\n  - The SSH daemon is running on the remote host\\\\\\\\n  - The correct hostname/IP address is being used\\\\\\\\n  - Port 22 is open and accessible (not blocked by firewall)\\\\\\\\n  - SSH keys are properly configured and authorized\\\\\\\\n- **Zensical Not Found**: Install Zensical in a virtual environment to avoid system Python restrictions.\\\\\\\\n- **Local Changes Not Committed**: Always commit and push local changes before building to ensure the built site reflects the latest source.\\\\\\\\n- **Build Artifacts Not Generated**: Ensure the `zensical build` command completes without errors and the `site/` directory is populated with HTML, CSS, JS, and other assets.\\\\\\\\n- **Image Loading Issues on GitHub Pages**: Use relative paths for assets (e.g., `![Alt text](assets/images/photo.png)`) rather than absolute paths (`![Alt text](/assets/images/photo.png)`) and use reliable placeholder services like `placehold.co` instead of `via.placeholder.com` to avoid connectivity issues.\\\\\\\\n- **Avatar Image Too Large**: Large avatar images (e.g., 1000x1000px) can slow page loading. Scale images to appropriate size (e.g., 50% for 250x250px) using FFmpeg: `ffmpeg -y -i input.png -vf \\\"scale=iw*0.5:ih*0.5\\\" -vframes 1 output.png`\\\\\\\\n- **GitHub Actions Workflow Syntax Errors**: Ensure proper syntax for GitHub Actions workflow files, particularly for the `github_token` which must be specified as `${{ secrets.GITHUB_TOKEN }}` (not `*** secrets.GITHUB_TOKEN }}`). Validate workflow files using `yamllint` or by checking GitHub's workflow validation. Common issues include:\\\\\\\\n  - Incorrect token syntax (using asterisks instead of proper variable substitution)\\\\\\\\n  - Missing or incorrect `uses:` declarations for actions\\\\\\\\n  - Improper indentation (YAML is sensitive to spacing)\\\\\\\\n  - Using deprecated action versions (always check for latest versions of actions like `actions/checkout@v4`)\n\n## References\\\\\\\\n- For details on the Zensical configuration, see `references/zensical-config.md`\\\\\\\\n- For troubleshooting SSH issues, see `references/ssh-troubleshooting.md`\\\\\\\\n- For personalization and disclaimer guidelines, see `references/personalization-and-disclaimers.md`\\\\\\\\n- For fixing image path issues when deploying to GitHub Pages, see `references/github-pages-image-paths.md`\\\\\\\\n- For scaling avatar images to 50% size for better page load and layout, see `references/avatar-scaling.md`\\\\\\\\n- For fixing GitHub Actions workflow syntax issues, see `references/github-actions-workflow-fixes.md`\\\\\\\\n- For fixing GitHub Actions workflow syntax issues, see `references/github-actions-workflow-fixes.md`

## References\\\\n- For details on the Zensical configuration, see `references/zensical-config.md`\\\\n- For troubleshooting SSH issues, see `references/ssh-troubleshooting.md`\\\\n- For personalization and disclaimer guidelines, see `references/personalization-and-disclaimers.md`\\\\n- For fixing image path issues when deploying to GitHub Pages, see `references/github-pages-image-paths.md`\\\\n- For scaling avatar images to 50% size for better page load and layout, see `references/avatar-scaling.md`

## Related Skills
- `hermes-agent` (for general Hermes Agent configuration)