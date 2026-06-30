# GitHub Actions Workflow Configuration for Hermes Agent Website

This document outlines the GitHub Actions workflow configuration used for building and deploying the Hermes Agent website.

## Workflow File Location
`.github/workflows/deploy.yml`

## Current Configuration (as of session updates)

```yaml
name: Deploy Website

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v4
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.11'
        cache: 'pip'
    
    - name: Install Zensical
      run: |
        python -m pip install --upgrade pip
        pip install zensical
    
    - name: Build site
      run: zensical build
    
    - name: Deploy to GitHub Pages
      uses: peaceiris/actions-gh-pages@v3
      with:
        github_token: ${{ secrets.GITHUB_TOKEN }}
        publish_dir: ./site
        force_orphan: true
```

## Key Changes Made

1. **Fixed Node.js Deprecation Error**:
   - Removed Node.js setup steps that were causing "deploy Node.js 20 is deprecated" errors
   - Switched to Python-based workflow since Zensical is a Python package

2. **Updated Actions Checkout**:
   - Changed from `actions/checkout@v3` to `actions/checkout@v4`
   - This resolves the deprecation warning and ensures compatibility

3. **Switched Deployment Target**:
   - Changed from DreamHost rsync deployment to GitHub Pages deployment
   - Uses `peaceiris/actions-gh-pages@v3` action
   - Publishes the `site/` directory to the `gh-pages` branch
   - `force_orphan: true` ensures a clean history on the gh-pages branch

## Workflow Execution Steps

1. **Checkout**: Retrieves the repository source code
2. **Setup Python**: Configures Python 3.11 environment with pip caching
3. **Install Zensical**: Installs the Zensical static site generator
4. **Build Site**: Runs `zensical build` to generate static HTML/CSS/JS in `site/` directory
5. **Deploy to GitHub Pages**: Publishes the built site to the `gh-pages` branch

## Secrets Required

The workflow requires the following GitHub repository secret:
- `GITHUB_TOKEN`: Automatically provided by GitHub Actions for repository access

## Troubleshooting

### Common Issues and Solutions

**"deploy Node.js 20 is deprecated" error**:
- Ensure you're using the updated workflow that doesn't include Node.js setup steps
- Check that you're using `actions/checkout@v4` or later

**Permission denied when deploying to GitHub Pages**:
- Verify the workflow has permission to push to the repository
- The default `GITHUB_TOKEN` should have sufficient permissions for gh-pages deployment

**Site not updating after push**:
- Check that the GitHub Actions workflow ran successfully
- Verify the `gh-pages` branch was updated with the new site content
- GitHub Pages may take a moment to reflect changes after the gh-pages branch is updated

## Alternative Configurations

### For DreamHost Deployment (when SSH is working)
If DreamHost SSH access is restored, you can switch back to rsync deployment:

```yaml
name: Deploy Website

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v4
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.11'
        cache: 'pip'
    
    - name: Install Zensical
      run: |
        python -m pip install --upgrade pip
        pip install zensical
    
    - name: Build site
      run: zensical build
    
    - name: Deploy to DreamHost
      env:
        SSH_PRIVATE_KEY: ${{ secrets.SSH_PRIVATE_KEY }}
      run: |
        mkdir -p ~/.ssh
        echo "$SSH_PRIVATE_KEY" > ~/.ssh/id_rsa
        chmod 600 ~/.ssh/id_rsa
        ssh-keyscan -H iad1-shared-b8-40.dreamhost.com >> ~/.ssh/known_hosts
        rsync -avz -e "ssh -o StrictHostKeyChecking=no" --delete site/ agent_blue@iad1-shared-b8-40.dreamhost.com:agent-blue.gitz.us/
```

This would require adding an `SSH_PRIVATE_KEY` secret to the repository.