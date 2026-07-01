#!/usr/bin/env python3
import requests
import json
import os
import base64
import subprocess

# Read the API key from the file we created earlier
with open('/tmp/nav_key.txt', 'r') as f:
    api_key = f.read().strip()

API_BASE = "https://api.ai.it.ufl.edu/v1"
headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {api_key}"
}

def generate_base_image(prompt, size="512x512"):
    """Generate base image at given size (must be allowed size)"""
    print(f"Generating base image: {prompt} (size: {size})")
    payload = {
        "model": "flux.1-schnell",
        "prompt": prompt,
        "n": 1,
        "size": size,
        "response_format": "b64_json"
    }
    try:
        response = requests.post(f"{API_BASE}/images/generations", headers=headers, json=payload, timeout=30)
        if response.status_code != 200:
            print(f"Error: {response.text}")
            return None
        result = response.json()
        if 'data' not in result or len(result['data']) == 0:
            print("No image data in response")
            return None
        image_data = result['data'][0]
        if not image_data.get('b64_json'):
            print("No b64_json in response")
            return None
        img_bytes = base64.b64decode(image_data['b64_json'])
        return img_bytes
    except Exception as e:
        print(f"Exception: {e}")
        return None

def scale_image(img_bytes, width, height):
    """Scale image using ffmpeg"""
    # Write input to temp file
    input_path = "/tmp/input.png"
    output_path = "/tmp/output.png"
    with open(input_path, 'wb') as f:
        f.write(img_bytes)
    # Use ffmpeg to scale
    # ffmpeg -i input.png -vf scale=width:height output.png
    cmd = [
        "ffmpeg",
        "-y",  # overwrite output
        "-i", input_path,
        "-vf", f"scale={width}:{height}",
        output_path
    ]
    try:
        result = subprocess.run(cmd, capture_output=True, timeout=30)
        if result.returncode != 0:
            print(f"ffmpeg error: {result.stderr.decode()}")
            return None
        with open(output_path, 'rb') as f:
            return f.read()
    except Exception as e:
        print(f"Exception scaling: {e}")
        return None

def generate_and_save(prompt, output_filename, target_width, target_height):
    """Generate image and save to output_filename at target dimensions"""
    # Generate base at 512x512
    base_img = generate_base_image(prompt, "512x512")
    if base_img is None:
        return False
    # Scale to target dimensions
    scaled_img = scale_image(base_img, target_width, target_height)
    if scaled_img is None:
        return False
    # Save
    with open(output_filename, 'wb') as f:
        f.write(scaled_img)
    print(f"Saved {output_filename} ({target_width}x{target_height})")
    return True

# Website directory
WEBSITE_DIR = "/home/agent-blue/.hermes/website"
IMAGES_DIR = os.path.join(WEBSITE_DIR, "docs", "assets", "images")

# Ensure images directory exists
os.makedirs(IMAGES_DIR, exist_ok=True)

# Generate the three images
success = True
success &= generate_and_save(
    "A colorful diagram showing different categories of skills for an AI assistant, with icons representing automation, coding, research, and creativity",
    os.path.join(IMAGES_DIR, "skills-diagram.png"),
    500, 300
)
success &= generate_and_save(
    "A timeline showing continuous improvement steps: daily AI briefing, automated skill updates, Zotero organization, and CI/CD workflow",
    os.path.join(IMAGES_DIR, "activity-timeline.png"),
    400, 200
)
success &= generate_and_save(
    "A simple guide showing four steps: install Hermes Agent, configure API keys, load skills, start chatting",
    os.path.join(IMAGES_DIR, "getting-started.png"),
    300, 200
)

if success:
    print("All images generated successfully!")
else:
    print("Some images failed to generate.")
    exit(1)