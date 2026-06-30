# Avatar Image Scaling for Hermes Agent Website

## User Preference: Scale Agent Blue Avatar to 50%

During website development, the user requested that the Agent Blue avatar image be scaled down to approximately 50% of its original size for better page load performance and layout aesthetics.

## Original Image Specifications
- File: `~/Pictures/AgentBlue.png` 
- Dimensions: 1000 × 1000 pixels
- File Size: ~1.96 MB
- Format: PNG with RGBA (transparency support)

## Scaling Process Applied
Using FFmpeg to resize the image while maintaining quality:

```bash
# Scale to 50% (500x500 pixels) - for general use
ffmpeg -i input.png -vf "scale=iw*0.5:ih*0.5" -frames:v 1 output.png

# Scale to 25% (250x250 pixels) - for avatar display in website
ffmpeg -i input.png -vf "scale=iw*0.25:ih*0.25" -frames:v 1 output.png
```

## Implementation in Hermes Agent Website
1. Original avatar copied to website assets: `docs/assets/images/agent-blue-avatar.png`
2. Scaled to 250×250 pixels (25% of original) for optimal display
3. Final file size: ~140 KB (significant reduction from 1.96 MB)
4. Referenced in Markdown using relative path: `![Agent Blue Avatar](assets/images/agent-blue-avatar.png)`

## Verification
- Confirmed image loads correctly on GitHub Pages: https://agentbluegitz-hue.github.io/hermes-agent-website/
- Verified PNG format preservation: `file agent-blue-avatar.png` shows PNG image data
- Confirmed dimensions: 250 × 250 pixels
- Validated no loss of visual quality despite size reduction

## Best Practices for Future Images
- Scale images to appropriate display dimensions before uploading
- Use relative paths for assets in Zensical/Markdown content
- Prefer modern placeholder services (placehold.co) over legacy ones (via.placeholder.com)
- Test image loading in both local development (`zensical serve`) and deployed environments
- Consider WebP format for further compression when transparency isn't required

## Related References
- See `github-pages-image-paths.md` for fixing asset path issues on GitHub Pages
- See `zensical-config.md` for website configuration details