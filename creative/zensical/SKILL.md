---
name: zensical
description: Build professional websites using the Zensical static site generator
category: creative
---

# Zensical Website Building

Build modern, responsive websites using the Zensical static site generator from the Material for MkDocs team.
## When to Use

Use this skill when you need to:

- Build a documentation or informational website
- Create a site primarily from Markdown content
- Want a professional-looking site with minimal configuration
- Desire built-in features like search, dark/light mode, and responsive design
- Plan to host the site statically (GitHub Pages, DreamHost, etc.)
- Want to integrate AI-generated images into your site (via direct API or ComfyUI)
- Want to integrate AI-generated images into your site (via direct API or ComfyUI)

## Steps

### 1. Install Zensical

Zensical is not yet available on crates.io, so install from GitHub release:

```bash
# Create virtual environment (recommended)
python3 -m venv /tmp/zensical_env
source /tmp/zensical_env/bin/activate

# Install from GitHub release
pip install https://github.com/zensical/zensical/releases/download/v0.0.46/zensical-0.0.46-cp310-abi3-manylinux_2_17_x86_64.manylinux2014_x86_64.whl

# Alternatively, use pipx
pipx install https://github.com/zensical/zensical/releases/download/v0.0.46/zensical-0.0.46-cp310-abi3-manylinux_2_17_x86_64.manylinux2014_x86_64.whl
```

For detailed installation instructions and troubleshooting, see `references/installation.md`.

### 2. Create a New Project

```bash
zensical new /path/to/your/project
cd /path/to/your/project
```

This creates:
- `zensical.toml` - Configuration file
- `docs/` directory - For your Markdown content
- `.github/` directory - GitHub templates

### 3. Configure Your Site

Edit `zensical.toml` to set:

```toml
[project]
site_name = "Your Site Name"
site_description = "A description of your site for SEO"
site_author = "Your Name"
site_url = "https://your-domain.com/"  # Important for correct asset paths
copyright = """
Copyright &copy; 2026 Your Name
"""

[project.theme]
# Optional: Customize theme
[project.theme.font]
text = "Inter"
code = "Jetbrains Mono"

[[project.theme.palette]]
scheme = "default"
toggle.icon = "lucide/sun"
toggle.name = "Switch to dark mode"

[[project.theme.palette]]
scheme = "slate"
toggle.icon = "lucide/moon"
toggle.name = "Switch to light mode"

# Enable useful features
features = [
    "announce.dismiss",
    "content.code.annotate",
    "content.code.copy",
    "content.code.select",
    "content.footnote.tooltips",
    "content.tabs.link",
    "content.tooltips",
    "navigation.path",
    "navigation.top",
    "navigation.tracking",
    "search.highlight",
    "toc.follow",
]
```

### 4. Add Content

Create Markdown files in the `docs/` directory:
- `docs/index.md` - Home page
- `docs/about.md` - About page
- etc.

Use Zensical's extended Markdown features:
- Footnotes: `[^1]` and footnote definitions
- Code blocks with annotations: ```{ .annotate }``` 
- Tabbed content: `=== "Tab 1"` / `=== "Tab 2"`
- Mermaid diagrams: ```mermaid

### 5. Build and Preview

```bash
# Build the site
zensical build

# Or build and serve locally for preview
zensical serve
```

The built site will be in the `site/` directory.

### 6. Deploy

#### To DreamHost via rsync (Hermes-specific example):
```bash
# Using the helper script approach (recommended for Hermes)
cd /home/agent-blue/.hermes/website
source /tmp/zensical_env/bin/activate  # Adjust path to your venv
zensical build
rsync -avz -e "ssh -o StrictHostKeyChecking=no" --delete site/ agent_blue@iad1-shared-b8-40.dreamhost.com:agent-blue.gitz.us/
```

#### Direct rsync command:
```bash
rsync -avz -e "ssh -o StrictHostKeyChecking=no" --delete site/ user@host:path/to/website/
```

#### To GitHub Pages (using GitHub Actions):
Create `.github/workflows/deploy.yml`:
```yaml
name: Deploy Website

on:
  push:
    branches: [ main ]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.x'
    
    - name: Install Zensical
      run: |
        python -m venv venv
        source venv/bin/activate
        pip install https://github.com/zensical/zensical/releases/download/v0.0.46/zensical-0.0.46-cp310-abi3-manylinux_2_17_x86_64.manylinux2014_x86_64.whl
    
    - name: Build
      run: |
        source venv/bin/activate
        zensical build
    
    - name: Deploy
      uses: peaceiris/actions-gh-pages@v3
      with:
        github_token: ${{ secrets.GITHUB_TOKEN }}
        publish_dir: ./site
```

### 7. Automate Updates (Hermes-specific example)

Set up a cron job to keep your Hermes Agent website updated:

```bash
# Create deployment script: /home/agent-blue/.hermes/scripts/auto-deploy-website.sh
#!/bin/bash
# Change to website directory
WEBSITE_DIR="/home/agent-blue/.hermes/website"
mkdir -p "$WEBSITE_DIR"
cd "$WEBSITE_DIR" || { echo "Failed to change to website directory"; exit 1; }

# Pull latest changes
git fetch origin
git reset --hard origin/main

# Add and commit changes if any
if ! git diff-index --quiet HEAD --; then
  git add .
  git commit -m "Auto-update: $(date '+%Y-%m-%d %H:%M:%S')"
  git push origin main
  echo "Website updated and pushed to GitHub"
else
  echo "No changes in website repository"
fi

# Build the site with Zensical
echo "Building site with Zensical..."
source /tmp/zensical_env/bin/activate
zensical build

# Deploy to DreamHost via rsync (deploy the built site)
echo "Deploying to DreamHost..."
rsync -avz -e "ssh -o StrictHostKeyChecking=no" --delete ./site/ agent_blue@iad1-shared-b8-40.dreamhost.com:agent-blue.gitz.us/
echo "Deployment complete"
```

# Make executable and set up cron job
chmod +x /home/agent-blue/.hermes/scripts/auto-deploy-website.sh
# Then configure via hermes cron create or manually in crontab
```

### 7. Automate Updates (Optional)

Set up a cron job to keep your site updated:
```bash
# Example cron job (runs hourly)
0 * * * * cd /path/to/your/project && git pull && source /path/to/venv/bin/activate && zensical build && rsync -avz -e "ssh -o StrictHostKeyChecking=no" --delete site/ user@host:path/to/website/
```

#### Hermes-specific automation example:
See `templates/deploy-script.sh` for a complete deployment script designed for use with Hermes Agent's automation system.

## Pitfalls

- **Installation**: Zensical is not on crates.io yet - you must install from GitHub release wheels
- **Site URL**: The `site_url` in zensical.toml must match your actual deployment URL for proper asset loading
- **Deployment Target**: Always deploy the contents of the `site/` directory, not your source files
- **Git Metadata**: When deploying via rsync, consider excluding `.git/` if you don't want to deploy your Git history
- **Theme Customization**: Some theme overrides require creating a `custom_dir` directory and understanding Zensical's templating system
- **Path Resolution for GitHub Pages**: When deploying to GitHub Pages, use relative paths for assets (e.g., `assets/images/photo.png`) rather than absolute paths (`/assets/images/photo.png`). Absolute paths can break when the site is served from a subdirectory (like `username.github.io/repository/`). Zensical builds relative links correctly when configured properly, but manual HTML/Markdown overrides may need adjustment.

## Verification

After building, verify:
- All links work correctly
- Search functionality operates as expected
- Dark/light mode toggle functions properly
- Site displays correctly on mobile and desktop browsers
- Markdown renders correctly (especially footnotes, code blocks, etc.)
- Performance is acceptable (static sites should be fast)

## Related Skills

- `github`: For repository management and GitHub Actions setup
- `hermes-file-operations`: For safe file manipulation during site updates
- `cronjob`: For scheduling automated updates
- `terminal`: For running build and deployment commands

## Support Files

This skill includes the following support files:
- `references/installation.md` - Detailed installation instructions and troubleshooting
- `templates/deploy-script.sh` - Ready-to-use deployment script for Hermes Agent automation
- `references/github-pages-image-paths.md` - Guide to fixing image path issues when deploying to GitHub Pages
- `references/ai-image-generation.md` - Guide to integrating AI-generated images with Zensical sites