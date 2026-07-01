# NaviGator API Image Generation Workflow

This document describes the workflow for generating custom images using the NaviGator API (https://api.ai.it.ufl.edu/v1) for use in the Hermes Agent website.

## Overview
The NaviGator API provides access to Flux and Gemini image generation models. This workflow outlines how to:
1. Extract the API key from Hermes configuration
2. Generate images using Flux models (flux.1-schnell for quick tests, flux.1-dev for higher quality)
3. Use response_format: b64_json to avoid URL resolution issues with 0.0.0.0:5500 addresses
4. Scale images appropriately for web use using FFmpeg
5. Integrate generated images into the Zensical-based website

## Prerequisites
- Access to Hermes Agent configuration at `~/.hermes/config.yaml`
- The NaviGator API key configured under `api_key:` in config.yaml
- FFmpeg installed for image scaling
- curl and jq for API interaction and JSON processing

## Workflow

### 1. Extract API Key
```bash
# Extract the NaviGator API key from Hermes config
# Method 1: Using grep (simple)
NAV_KEY=$(grep "api_key:" ~/.hermes/config.yaml | head -1 | cut -d':' -f2 | tr -d ' ')
# Method 2: More precise extraction (if needed)
# NAV_KEY=$(grep -A2 "name: NaviGator" ~/.hermes/config.yaml | grep "api_key:" | cut -d':' -f2 | tr -d ' ')
echo "API Key extracted: ${NAV_KEY:0:10}... (length: ${#NAV_KEY})"
```

### 2. Test API Connectivity
```bash
# Test connection with a simple request using flux.1-schnell for quick testing
curl -s -H "Authorization: Bearer $NAV_KEY" -H "Content-Type: application/json" \
  -d '{"model": "flux.1-schnell", "prompt": "test", "n": 1, "size": "256x256", "response_format": "b64_json"}' \
  https://api.ai.it.ufl.edu/v1/images/generations | \
  jq -r '.data[0].b64_json' | base64 -d > /tmp/test.png && \
echo "Test successful: $(ls -lh /tmp/test.png | awk '{print $5}')"
```

### 3. Generate Hermes Agent Logo
```bash
# Generate the logo image using flux.1-dev for higher quality
curl -s -H "Authorization: Bearer $NAV_KEY" -H "Content-Type: application/json" \
  -d '{
    "model": "flux.1-dev",
    "prompt": "Hermes Agent AI assistant logo, futuristic AI interface with glowing blue neural networks, professional technology aesthetic, centered icon, flat vector style, white background, sleek modern design",
    "n": 1,
    "size": "1024x1024",
    "response_format": "b64_json"
  }' \
  https://api.ai.it.ufl.edu/v1/images/generations | \
  jq -r '.data[0].b64_json' | base64 -d > /home/agent-blue/.hermes/website/generated-images/herm_agent_logo.png
echo "Logo generated: $(ls -lh /home/agent-blue/.hermes/website/generated-images/herm_agent_logo.png | awk '{print $5}')"
```
```

### 4. Scale Image for Web Use
```bash
# Scale to 50% for optimal web performance (as per user preference)
ffmpeg -y -i /home/agent-blue/.hermes/website/generated-images/herm_agent_logo.png \
  -vf "scale=iw*0.5:ih*0.5" -vframes 1 \
  /home/agent-blue/.hermes/website/generated-images/herm_agent_logo_scaled.png
echo "Logo scaled: $(ls -lh /home/agent-blue/.hermes/website/generated-images/herm_agent_logo_scaled.png | awk '{print $5}')"
```

### 5. Handle API Response URLs
```bash
# After generating an image, the API may return URLs pointing to 0.0.0.0:5500
# These need to be adjusted to point to the actual API host
RESPONSE=$(curl -s -H "Authorization: Bearer *** -H "Content-Type: application/json" \
  -d '{"model":"flux.1-schnell","prompt":"A simple modern logo for an AI assistant named Hermes Agent, with wings and a stylized H","n":1,"size":"512x512"}' \
  https://api.ai.it.ufl.edu/v1/images/generations)

# Extract the image URL
IMAGE_URL=$(echo "$RESPONSE" | grep -o '"url":"[^"]*' | cut -d'"' -f4)
echo "Original URL: $IMAGE_URL"

# Adjust URL: replace 0.0.0.0:5500 with api.ai.it.ufl.edu and ensure https
if [[ "$IMAGE_URL" == *"0.0.0.0:5500"* ]]; then
  IMAGE_URL=$(echo "$IMAGE_URL" | sed 's|http://0.0.0.0:5500|https://api.ai.it.ufl.edu|')
  echo "Adjusted URL: $IMAGE_URL"
fi

# Download the image with authentication
curl -s -o /tmp/hermes_logo.png -H "Authorization: Bearer *** "$IMAGE_URL"
echo "Download completed. File info:"
file /tmp/hermes_logo.png
```

### 6. Generate Site Banner
```bash
# After generating an image, the API may return URLs pointing to 0.0.0.0:5500
# These need to be adjusted to point to the actual API host
RESPONSE=$(curl -s -H "Authorization: Bearer *** -H "Content-Type: application/json" \
  -d '{"model":"flux.1-schnell","prompt":"A simple modern logo for an AI assistant named Hermes Agent, with wings and a stylized H","n":1,"size":"512x512"}' \
  https://api.ai.it.ufl.edu/v1/images/generations)

# Extract the image URL
IMAGE_URL=$(echo "$RESPONSE" | grep -o '"url":"[^"]*' | cut -d'"' -f4)
echo "Original URL: $IMAGE_URL"

# Adjust URL: replace 0.0.0.0:5500 with api.ai.it.ufl.edu and ensure https
if [[ "$IMAGE_URL" == *"0.0.0.0:5500"* ]]; then
  IMAGE_URL=$(echo "$IMAGE_URL" | sed 's|http://0.0.0.0:5500|https://api.ai.it.ufl.edu|')
  echo "Adjusted URL: $IMAGE_URL"
fi

# Download the image with authentication
curl -s -o /tmp/hermes_logo.png -H "Authorization: Bearer *** "$IMAGE_URL"
echo "Download completed. File info:"
file /tmp/hermes_logo.png
```
```

### 5. Generate Site Banner
```bash
# Generate a wide banner image (using supported size closest to banner dimensions)
curl -s -H "Authorization: Bearer $NAV_KEY" -H "Content-Type: application/json" \
  -d '{
    "model": "flux.1-dev",
    "prompt": "Professional technology banner showing AI agent interface with flowing data lines, neural network patterns, futuristic dashboard, blue and purple color scheme, widescreen format",
    "n": 1,
    "size": "1792x1024",
    "response_format": "b64_json"
  }' \
  https://api.ai.it.ufl.edu/v1/images/generations | \
  jq -r '.data[0].b64_json' | base64 -d > /home/agent-blue/.hermes/website/generated-images/site_banner.png

echo "Banner generated: $(ls -lh /home/agent-blue/.hermes/website/generated-images/site_banner.png | awk '{print $5}')"

# Scale down for website use (maintaining aspect ratio)
ffmpeg -y -i /home/agent-blue/.hermes/website/generated-images/site_banner.png \
  -vf "scale=iw*0.3:ih*0.3" -vframes 1 \
  /home/agent-blue/.hermes/website/generated-images/site_banner_scaled.png

echo "Banner scaled: $(ls -lh /home/agent-blue/.hermes/website/generated-images/site_banner_scaled.png | awk '{print $5}')"
```

### 6. Generate Multitool Integration Graphic
```bash
# Generate graphic showing AI tools connection concept
curl -s -H "Authorization: Bearer $NAV_KEY" -H "Content-Type: application/json" \
  -d '{
    "model": "flux.1-dev",
    "prompt": "Multi-tool Integration | Skill System | Automation - three interconnected icons or symbols showing connection, professional technology illustration, flat design, white background",
    "n": 1,
    "size": "1024x1024",
    "response_format": "b64_json"
  }' \
  https://api.ai.it.ufl.edu/v1/images/generations | \
  jq -r '.data[0].b64_json' | base64 -d > /home/agent-blue/.hermes/website/generated-images/multitool_integration.png

echo "Multitool image generated: $(ls -lh /home/agent-blue/.hermes/website/generated-images/multitool_integration.png | awk '{print $5}')"

# Scale down for website use
ffmpeg -y -i /home/agent-blue/.hermes/website/generated-images/multitool_integration.png \
  -vf "scale=iw*0.6:ih*0.6" -vframes 1 \
  /home/agent-blue/.hermes/website/generated-images/multitool_integration_scaled.png

echo "Multitool image scaled: $(ls -lh /home/agent-blue/.hermes/website/generated-images/multitool_integration_scaled.png | awk '{print $5}')"
```

### 7. Integrate Images into Website
```bash
# Copy scaled images to docs/assets/images/ (Zensical source folder)
cp /home/agent-blue/.hermes/website/generated-images/herm_agent_logo_scaled.png /home/agent-blue/.hermes/website/docs/assets/images/hermes-agent-logo.png
cp /home/agent-blue/.hermes/website/generated-images/multitool_integration_scaled.png /home/agent-blue/.hermes/website/docs/assets/images/multitool-integration.png

# Update markdown to reference custom images instead of placeholders
cd /home/agent-blue/.hermes/website
sed -i 's|https://placehold.co/400x200/4A90E2/FFFFFF?text=Hermes+Agent+AI+Assistant|assets/images/hermes-agent-logo.png|g' docs/index.md
sed -i 's|https://placehold.co/600x200/50E3C2/FFFFFF?text=Multi-tool+Integration+%7C+Skill+System+%7C+Automation|assets/images/multitool-integration.png|g' docs/index.md

# Build and deploy
/zensical_env/bin/zensical build
git add docs/assets/images/hermes-agent-logo.png docs/assets/images/multitool-integration.png docs/index.md
git commit -m "Add custom generated images for website: Hermes Agent logo and multitool integration graphics"
git push origin main
```

## Important Notes

### API Size Constraints
The NaviGator API with Flux.1-dev model only accepts specific dimensions:
- Valid sizes: `256x256`, `512x512`, `1024x1024`, `1792x1024`, `1024x1536`, `1536x1024`, `256x256`, `auto`
- Requests for other sizes will return error 422 with details about valid options

### Image Optimization
- Always scale down generated images for web use to improve page load times
- Use FFmpeg with scale filter: `ffmpeg -y -i input.png -vf "scale=iw*0.5:ih*0.5" -vframes 1 output.png`
- The user prefers images scaled to 50% original size for optimal balance of quality and performance

### File Organization
- Store generated images temporarily in `generated-images/` folder
- Copy final, scaled images to `docs/assets/images/` for Zensical to process
- Never edit files directly in `/site/` folder as it is regenerated by Zensical

### Error Handling
- If API returns error 422, check the response for valid size options
- If curl commands fail with "unexpected EOF", check JSON quoting in the command
- Always verify image generation succeeded by checking file size before proceeding

## Example Commands from Session
The following commands were successfully used in a live session:

```bash
# Extract and verify API key
NAV_KEY=$(grep "api_key:" ~/.hermes/config.yaml | head -1 | cut -d':' -f2 | tr -d ' ')
echo "NAV_KEY=${NAV_KEY:0:10}..."

# Generate and scale logo
curl -s -H "Authorization: Bearer $NAV_KEY" -H "Content-Type: application/json" \
  -d '{"model":"flux.1-dev","prompt":"Hermes Agent logo","n":1,"size":"1024x1024","response_format":"b64_json"}' \
  https://api.ai.it.ufl.edu/v1/images/generations | \
  jq -r '.data[0].b64_json' | base64 -d > generated-images/herm_agent_logo.png
ffmpeg -y -i generated-images/herm_agent_logo.png -vf "scale=iw*0.5:ih*0.5" -vframes 1 generated-images/herm_agent_logo_scaled.png

# Update website
cp generated-images/herm_agent_logo_scaled.png docs/assets/images/hermes-agent-logo.png
sed -i 's|https://placehold.co/400x200/4A90E2/FFFFFF?text=Hermes+Agent+AI+Assistant|assets/images/hermes-agent-logo.png|g' docs/index.md
/zensical_env/bin/zensical build
```

## References
- NaviGator API documentation: https://api.ai.it.ufl.edu/v1
- FFmpeg scaling documentation: https://ffmpeg.org/ffmpeg-filters.html#scale
- Zensical website deployment: see references/zensical-config.md