# GitHub Pages Image Path Fix for Zensical Sites

## Issue: Images Not Loading on GitHub Pages

During deployment of a Hermes Agent website built with Zensical to GitHub Pages (https://agentbluegitz-hue.github.io/hermes-agent-website/), images were not displaying despite being present in the built site directory.

## Root Cause

The issue was caused by using **absolute paths** for images in Markdown content:

```markdown
![Agent Blue Avatar](/assets/images/agent-blue-avatar.png)
```

When GitHub Pages serves the site from a subdirectory (e.g., `username.github.io/repository/`), absolute paths starting with `/` resolve to the domain root rather than the repository subdirectory, causing 404 errors for assets.

## Solution

Changed to **relative paths** in Markdown content:

```markdown
![Agent Blue Avatar](assets/images/agent-blue-avatar.png)
```

## Verification Steps

1. Check built HTML in `site/` directory for correct path usage
2. Verify image accessibility via direct URL:
   - `https://username.github.io/repository/assets/images/photo.png`
3. Use browser developer tools to confirm images load without 404 errors

## Prevention\n\nWhen creating content for Zensical sites intended for GitHub Pages deployment:\n- Always use relative paths for images and assets in Markdown\n- Avoid leading slashes in asset paths unless you intend to serve from domain root\n- Test locally with `zensical serve` before deployment\n- Verify built site structure before pushing to GitHub\n- **Important**: Use reliable placeholder services like `placehold.co` instead of `via.placeholder.com` for consistent image loading, as the former service was experiencing connectivity issues (TLS connect errors).

## Hermes-Specific Context

This fix was applied to the Hermes Agent website repository:
- Repository: https://github.com/agentbluegitz-hue/hermes-agent-website
- GitHub Pages: https://agentbluegitz-hue.github.io/hermes-agent-website/
- Affected file: `docs/index.md` (and similar content files)
- Fix committed: `586121c` - "Fix image paths: use relative paths for local assets instead of absolute paths"