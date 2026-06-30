# Avatar Scaling Technique for Hermes Agent Website

## Problem
The Agent Blue avatar image was originally 1000x1000px (~1.9MB) causing unnecessary bandwidth usage and potentially affecting page layout.

## Solution
Use FFmpeg to scale images down to 50% while maintaining aspect ratio and quality.

## FFmpeg Command
```bash
# Scale image to 50% width and height
ffmpeg -y -i input.png -vf "scale=iw*0.5:ih*0.5" -vframes 1 output.png
```

## Parameters Explained
- `-y`: Overwrite output file without asking
- `-i input.png`: Input file path
- `-vf "scale=iw*0.5:ih*0.5"`: Video filter to scale width and height to 50%
- `-vframes 1`: Process only 1 frame (for images)
- `output.png`: Output file path

## Alternative Syntax
```bash
# Using explicit dimensions (calculated)
ffmpeg -y -i input.png -vf "scale=500:500" -vframes 1 output.png

# Using percentage notation
ffmpeg -y -i input.png -vf "scale=0.5*iw:0.5*ih" -vframes 1 output.png
```

## Verification
After scaling, verify:
1. File size reduction (should be ~75% smaller for PNG)
2. Dimensions: `identify output.png` or `file output.png`
3. Visual quality: Check that important details remain visible

## Example from Session
```bash
# Original: 1000x1000px, 1.9MB
ls -lh /home/agent-blue/.hermes/website/docs/assets/images/agent-blue-avatar.png
# Output: -rw-rw-r-- 1 agent-blue agent-blue 1.9M Jun 30 13:44 agent-blue-avatar.png

# Scale to 50%
cd /home/agent-blue/.hermes/website/docs/assets/images
ffmpeg -y -i agent-blue-avatar.png -vf "scale=iw*0.5:ih*0.5" -vframes 1 agent-blue-avatar.png

# Result: 500x500px, ~503KB
ls -lh agent-blue-avatar.png
# Output: -rw-rw-r-- 1 agent-blue agent-blue 503K Jun 30 14:16 agent-blue-avatar.png
```

## Best Practices
1. Always keep original images backed up
2. Test scaled images on actual web pages before deploying
3. Consider different scaling percentages based on container size (25%, 33%, 50%, 75%)
4. For web use, consider also optimizing with tools like `optipng` or `pngquant` after scaling
5. Document the scaling factor used in case you need to reproduce or adjust later

## Troubleshooting
- "File already exists" error: Use `-y` flag to auto-overwrite
- Invalid dimensions: Ensure width/height are even numbers for some codecs
- Quality loss: Adjust with `-q:v` parameter (2-31 for PNG, lower is better)