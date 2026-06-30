# AI Image Generation with Zensical

This guide explains how to integrate AI-generated images into your Zensical-built website, using either direct API calls or ComfyUI for more advanced workflows.

## Direct API Approach

When you have API access to image generation services (like NaviGator, Replicate, Hugging Face, etc.), you can generate images directly via HTTP API calls.

### NaviGator API Example

The NaviGator API at `https://api.ai.it.ufl.edu/v1` provides access to Flux and Gemini image generation models using the same API key used for the Nemotron LLM.

#### Endpoint
```
POST https://api.ai.it.ufl.edu/v1/images/generations
```

#### Headers
```
Authorization: Bearer <YOUR_API_KEY>
Content-Type: application/json
```

#### Request Body
```json
{
  "model": "flux.1-dev",  // or other available model (check API for options)
  "prompt": "Your image description here",
  "n": 1,                 // number of images
  "size": "1024x1024",    // check API for supported sizes
  "response_format": "b64_json"  // or "url"
}
```

#### Supported Sizes (NaviGator/Flux)
Based on API responses:
- 256x256
- 512x512  
- 1024x1024
- 1792x1024
- 1024x1792

#### Example: Generating a Hermes Agent Logo
```bash
# Extract API key from Hermes config
API_KEY=$(grep "api_key:" /home/agent-blue/.hermes/config.yaml | head -1 | cut -d':' -f2 | tr -d ' ')

# Generate image
curl -s -H "Authorization: Bearer *** -H "Content-Type: application/json" \
  -d '{
    "model": "flux.1-dev",
    "prompt": "Hermes Agent AI assistant logo, futuristic AI interface with glowing blue neural networks, professional technology aesthetic, centered icon, flat vector style, white background, sleek modern design",
    "n": 1,
    "size": "1024x1024",
    "response_format": "b64_json"
  }' https://api.ai.it.ufl.edu/v1/images/generations | \
  jq -r '.data[0].b64_json' | base64 -d > herm_agent_logo.png

# Scale for web use (as per Hermes preference)
ffmpeg -y -i herm_agent_logo.png -vf "scale=iw*0.5:ih*0.5" -vframes 1 herm_agent_logo_scaled.png

# Deploy to Zensical site
cp herm_agent_logo_scaled.png /path/to/your/zensical/site/assets/images/
```

#### Python Example
```python
import requests
import base64
import os
import subprocess

API_KEY = "your..."  # Or extract from Hermes config
BASE_URL = "https://api.ai.it.ufl.edu/v1"

headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

# Generate Hermes Agent logo
payload = {
    "model": "flux.1-dev",
    "prompt": "Hermes Agent AI assistant logo, futuristic interface with neural networks",
    "n": 1,
    "size": "1024x1024",
    "response_format": "b64_json"
}

response = requests.post(f"{BASE_URL}/images/generations", headers=headers, json=payload)
if response.status_code == 200:
    result = response.json()
    image_data = base64.b64decode(result['data'][0]['b64_json'])
    
    # Save original
    with open("herm_agent_logo.png", "wb") as f:
        f.write(image_data)
    
    # Scale for web use
    subprocess.run([
        "ffmpeg", "-y", "-i", "herm_agent_logo.png", 
        "-vf", "scale=iw*0.5:ih*0.5", 
        "-vframes", "1", 
        "herm_agent_logo_scaled.png"
    ], check=True)
    
    # Copy to Zensical site
    shutil.copy("herm_agent_logo_scaled.png", "/path/to/your/zensical/site/assets/images/")
else:
    print(f"Error: {response.status_code}")
    print(response.text)
```

## ComfyUI Approach

For more complex image generation workflows (ControlNet, img2img, etc.), use ComfyUI:

1. Set up ComfyUI using the `comfyui` skill
2. Generate images with your desired workflow
3. Scale and deploy as shown above

## Best Practices for Zensical Integration

1. **Always scale images for web use**: Large images slow down your site. Use the Hermes-preferred scaling:
   ```bash
   ffmpeg -y -i input.png -vf "scale=iw*0.5:ih*0.5" -vframes 1 output.png
   ```

2. **Use relative paths in Markdown**: Reference images as `/assets/images/your-image.png` rather than absolute paths.

3. **Optimize file formats**: PNG for graphics with transparency, JPEG for photographs.

4. **Cache generated images**: Store generated images in your repository rather than regenerating on every build.

5. **Check API limits**: Be aware of rate limits and costs for your chosen image generation service.

## Verification

After adding AI-generated images to your Zensical site:
- Verify images load correctly on both desktop and mobile
- Check that scaled images maintain visual quality
- Confirm the site builds and deploys successfully
- Test dark/light mode compatibility with your images

## References

- NaviGator API: https://api.ai.it.ufl.edu/v1
- Hermes config location: /home/agent-blue/.hermes/config.yaml
- Zensical documentation: https://zensical.github.io/
- FFmpeg documentation: https://ffmpeg.org/