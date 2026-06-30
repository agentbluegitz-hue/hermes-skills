# GitHub Actions Workflow Fixes for Hermes Agent Website

## Common Issues Encountered

### Issue 1: Incorrect GitHub Token Syntax
**Problem**: Using `*** secrets.GITHUB_TOKEN }}` instead of `${{ secrets.GITHUB_TOKEN }}`
**Error**: Workflow fails with authentication errors
**Fix**: Use proper GitHub Actions syntax for accessing secrets:
```yaml
github_token: ${{ secrets.GITHUB_TOKEN }}
```

### Issue 2: Workflow Validation Failures
**Problem**: YAML syntax errors or incorrect action usage
**Solutions**:
- Use `yamllint` to validate workflow files before committing
- GitHub provides workflow validation in the Actions tab
- Common validation issues:
  - Incorrect indentation (YAML is space-sensitive)
  - Missing required fields
  - Using deprecated action versions

### Issue 3: Action Version Deprecation
**Problem**: Using outdated action versions (e.g., `actions/checkout@v2` instead of `@v3`)
**Fix**: Always check for and use the latest stable versions of actions:
- `actions/checkout@v4`
- `actions/setup-python@v4`
- `peaceiris/actions-gh-pages@v3`

## Verification Steps

1. **Syntax Check**: Use `yamllint .github/workflows/deploy.yml`
2. **GitHub Validation**: Push changes and check the "Actions" tab for workflow validation
3. **Test Run**: Manually trigger the workflow to verify it completes successfully

## Example Corrected Workflow

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

## Prevention Tips

1. **Use IDE with YAML linting** (VS Code with YAML extension, etc.)
2. **Validate before committing** - run syntax checks locally
3. **Keep actions updated** - periodically check for newer versions of used actions
4. **Document changes** - when fixing workflow issues, note what was wrong and how it was fixed