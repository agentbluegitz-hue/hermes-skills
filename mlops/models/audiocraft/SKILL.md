**Revised Hermes skill file**

```yaml
---
name: audiocraft-audio-generation
description: "AudioCraft: MusicGen text-to-music, AudioGen text-to-sound."
version: 1.0.0
author: Orchestra Research
license: MIT
dependencies: [audiocraft, torch>=2.0.0, transformers>=4.30.0, torchaudio>=2.0.0]
platforms: [linux, macos]
metadata:
  hermes:
    tags: [Multimodal, Audio Generation, Text-to-Music, Text-to-Audio, MusicGen]
---
```

# AudioCraft: Audio Generation

Comprehensive guide to using Meta's AudioCraft for text‑to‑music and text‑to‑audio generation with MusicGen, AudioGen, and EnCodec.

## When to use AudioCraft

**Use AudioCraft when:**
- You need to generate music from text descriptions  
- You want to create sound effects or environmental audio  
- You are building music‑generation applications  
- You need melody‑conditioned music generation  
- You want stereo audio output  
- You require controllable music generation with style transfer  

**Key features:**
- **MusicGen** – Text‑to‑music generation with optional melody conditioning  
- **AudioGen** – Text‑to‑sound‑effects generation  
- **EnCodec** – High‑fidelity neural audio codec  
- **Multiple model sizes** – Small (300 M) to Large (3.3 B)  
- **Stereo support** – Full stereo audio generation  
- **Style conditioning** – MusicGen‑Style for reference‑based generation  

**Alternatives you might also consider:**
- **Stable Audio** – Longer commercial‑grade music generation  
- **Bark** – Text‑to‑speech with music/sound‑effect capabilities  
- **Riffusion** – Spectrogram‑based music generation  
- **OpenAI Jukebox** – Raw audio generation with lyrics  

## Quick start

### Installation

```bash
# From PyPI
pip install audiocraft

# From GitHub (latest)
pip install git+https://github.com/facebookresearch/audiocraft.git

# Or install the additional libraries you may need
pip install transformers torch torchaudio
```

### Basic text‑to‑music (AudioCraft)

```python
import torchaudio
from audiocraft.models import MusicGen

# Load a pretrained MusicGen model
model = MusicGen.get_pretrained("facebook/musicgen-small")

# Set generation parameters
model.set_generation_params(
    duration=8,          # seconds
    top_k=250,
    temperature=1.0,
)

# Generate from a textual description
descriptions = ["happy upbeat electronic dance music with synths"]
wav = model.generate(descriptions)

# Save the first (and only) output
torchaudio.save("output.wav", wav[0].cpu(), sample_rate=32_000)
```

### Using HuggingFace Transformers

```python
from transformers import AutoProcessor, MusicgenForConditionalGeneration
import scipy.io.wavfile

# Load model and processor from the 🤗 hub
processor = AutoProcessor.from_pretrained("facebook/musicgen-small")
model = MusicgenForConditionalGeneration.from_pretrained("facebook/musicgen-small")
model.to("cuda")

# Encode the prompt
inputs = processor(
    text=["80s pop track with bassy drums and synth"],
    padding=True,
    return_tensors="pt",
).to("cuda")

# Generate audio
audio_values = model.generate(
    **inputs,
    do_sample=True,
    guidance_scale=3,
    max_new_tokens=256,
)

# Save the result
sampling_rate = model.config.audio_encoder.sampling_rate
scipy.io.wavfile.write(
    "output.wav",
    rate=sampling_rate,
    data=audio_values[0, 0].cpu().numpy(),
)
```

### Text‑to‑sound with AudioGen

```python
import torchaudio
from audiocraft.models import AudioGen

# Load the AudioGen model
model = AudioGen.get_pretrained("facebook/audiogen-medium")
model.set_generation_params(duration=5)

# Generate a sound‑effect
descriptions = ["dog barking in a park with birds chirping"]
wav = model.generate(descriptions)

torchaudio.save("sound.wav", wav[0].cpu(), sample_rate=16_000)
```

## Core concepts

### Architecture overview

```
AudioCraft Architecture:
┌──────────────────────────────────────────────────────────────┐
│                    Text Encoder (T5)                          │
│                         │                                     │
│                    Text Embeddings                            │
└────────────────────────┬─────────────────────────────────────┘
                         │
┌────────────────────────▼─────────────────────────────────────┐
│              Transformer Decoder (LM)                         │
│     Auto‑regressively generates audio tokens                  │
│     Using efficient token interleaving patterns               │
└────────────────────────┬─────────────────────────────────────┘
                         │
┌────────────────────────▼─────────────────────────────────────┐
│                EnCodec Audio Decoder                          │
│        Converts tokens back to audio waveform                 │
└──────────────────────────────────────────────────────────────┘
```

### Model variants

| Model                     | Size | Description          | Typical use case |
|---------------------------|------|----------------------|------------------|
| `musicgen-small`          | 300 M | Text‑to‑music        | Quick prototyping |
| `musicgen-medium`         | 1.5 B | Text‑to‑music        | Balanced quality |
| `musicgen-large`          | 3.3 B | Text‑to‑music        | Highest fidelity |
| `musicgen-melody`         | 1.5 B | Text + melody        | Melody‑conditioned |
| `musicgen-melody-large`   | 3.3 B | Text + melody        | Best melody quality |
| `musicgen-stereo-*`       | Varies| Stereo output        | Stereo generation |
| `musicgen-style`          | 1.5 B | Style transfer       | Reference‑based |
| `audiogen-medium`         | 1.5 B | Text‑to‑sound        | Sound‑effects |

### Generation parameters

| Parameter   | Default | Description |
|-------------|---------|-------------|
| `duration`  | 8.0     | Length in seconds (1‑120) |
| `top_k`     | 250     | Top‑k sampling |
| `top_p`     | 0.0     | Nucleus sampling (0 = disabled) |
| `temperature`| 1.0    | Sampling temperature |
| `cfg_coef`  | 3.0     | Classifier‑free guidance coefficient |

## MusicGen usage

### Text‑to‑music generation

```python
import torchaudio
from audiocraft.models import MusicGen

model = MusicGen.get_pretrained("facebook/musicgen-medium")
model.set_generation_params(
    duration=30,
    top_k=250,
    top_p=0.0,
    temperature=1.0,
    cfg_coef=3.0,
)

descriptions = [
    "epic orchestral soundtrack with strings and brass",
    "chill lo‑fi hip hop beat with jazzy piano",
    "energetic rock song with electric guitar",
]

wav = model.generate(descriptions)

for i, audio in enumerate(wav):
    torchaudio.save(f"music_{i}.wav", audio.cpu(), sample_rate=32_000)
```

### Melody‑conditioned generation

```python
import torchaudio
from audiocraft.models import MusicGen

model = MusicGen.get_pretrained("facebook/musicgen-melody")
model.set_generation_params(duration=30)

# Load a short melody (mono or stereo)
melody, sr = torchaudio.load("melody.wav")

# Generate music that follows the supplied melody
descriptions = ["acoustic guitar folk song"]
wav = model.generate_with_chroma(descriptions, melody, sr)

torchaudio.save("melody_conditioned.wav", wav[0].cpu(), sample_rate=32_000)
```

### Stereo generation

```python
import torchaudio
from audiocraft.models import MusicGen

model = MusicGen.get_pretrained("facebook/musicgen-stereo-medium")
model.set_generation_params(duration=15)

descriptions = ["ambient electronic music with wide stereo panning"]
wav = model.generate(descriptions)

# wav shape: [batch, 2, samples] → stereo
print(f"Stereo shape: {wav.shape}")  # e.g. [1, 2, 480_000]
torchaudio.save("stereo.wav", wav[0].cpu(), sample_rate=32_000)
```

### Audio continuation (conditional generation)

```python
import torchaudio
from transformers import AutoProcessor, MusicgenForConditionalGeneration

processor = AutoProcessor.from_pretrained("facebook/musicgen-medium")
model = MusicgenForConditionalGeneration.from_pretrained("facebook/musicgen-medium")

# Load a short audio clip you want to continue
audio, sr = torchaudio.load("intro.wav")

inputs = processor(
    audio=audio.squeeze().numpy(),
    sampling_rate=sr,
    text=["continue with an epic chorus"],
    padding=True,
    return_tensors="pt",
)

audio_values = model.generate(
    **inputs,
    do_sample=True,
    guidance_scale=3,
    max_new_tokens=512,
)
```

## MusicGen‑Style usage

### Style‑conditioned generation

```python
import torchaudio
from audiocraft.models import MusicGen

model = MusicGen.get_pretrained("facebook/musicgen-style")
model.set_generation_params(
    duration=30,
    cfg_coef=3.0,
    cfg_coef_beta=5.0,   # higher → stronger style influence
)

# Configure the style‑conditioner (optional, defaults are sensible)
model.set_style_conditioner_params(
    eval_q=3,               # number of RVQ quantizers (1‑6)
    excerpt_length=3.0,    # length of the style excerpt in seconds
)

# Load a reference audio that defines the desired style
style_audio, sr = torchaudio.load("reference_style.wav")

descriptions = ["upbeat dance track"]
wav = model.generate_with_style(descriptions, style_audio, sr)
torchaudio.save("style_conditioned.wav", wav[0].cpu(), sample_rate=32_000)
```

### Style‑only generation (no text prompt)

```python
# When you want the model to generate music purely in the reference style
model.set_generation_params(
    duration=30,
    cfg_coef=3.0,
    cfg_coef_beta=None,   # disables the double‑CFG path
)

wav = model.generate_with_style([None], style_audio, sr)
torchaudio.save("style_only.wav", wav[0].cpu(), sample_rate=32_000)
```

## AudioGen usage

### Sound‑effect generation

```python
import torchaudio
from audiocraft.models import AudioGen

model = AudioGen.get_pretrained("facebook/audiogen-medium")
model.set_generation_params(duration=10)

descriptions = [
    "thunderstorm with heavy rain and lightning",
    "busy city traffic with car horns",
    "ocean waves crashing on rocks",
    "crackling campfire in forest",
]

wav = model.generate(descriptions)

for i, audio in enumerate(wav):
    torchaudio.save(f"sound_{i}.wav", audio.cpu(), sample_rate=16_000)
```

## EnCodec usage

### Audio compression & reconstruction

```python
import torch
import torchaudio
from audiocraft.models import CompressionModel

# Load the EnCodec model (32 kHz version)
model = CompressionModel.get_pretrained("facebook/encodec_32khz")

# Load an audio file
wav, sr = torchaudio.load("audio.wav")

# Resample if necessary
if sr != 32_000:
    wav = torchaudio.transforms.Resample(sr, 32_000)(wav)

# Encode → obtain discrete codes
with torch.no_grad():
    encoded = model.encode(wav.unsqueeze(0))
    codes = encoded[0]          # shape: [batch, n_q, seq_len]

# Decode back to waveform
with torch.no_grad():
    decoded = model.decode(codes)

torchaudio.save("reconstructed.wav", decoded[0].cpu(), sample_rate=32_000)
```

## Common workflows

### Workflow 1 – Simple music‑generation wrapper

```python
import torch
import torchaudio
from audiocraft.models import MusicGen

class MusicGenerator:
    def __init__(self, model_name="facebook/musicgen-medium"):
        self.model = MusicGen.get_pretrained(model_name)
        self.sample_rate = 32_000

    def generate(self, prompt, duration=30, temperature=1.0, cfg=3.0):
        self.model.set_generation_params(
            duration=duration,
            top_k=250,
            temperature=temperature,
            cfg_coef=cfg,
        )
        with torch.no_grad():
            wav = self.model.generate([prompt])
        return wav[0].cpu()

    def generate_batch(self, prompts, duration=30):
        self.model.set_generation_params(duration=duration)
        with torch.no_grad():
            wav = self.model.generate(prompts)
        return wav.cpu()

    def save(self, audio, path):
        torchaudio.save(path, audio, sample_rate=self.sample_rate)

# Example usage
generator = MusicGenerator()
audio = generator.generate(
    "epic cinematic orchestral music",
    duration=30,
    temperature=1.0,
    cfg=3.0,
)
generator.save(audio, "epic_music.wav")
```

### Workflow 2 – Sound‑design batch processing

```python
import json
from pathlib import Path
import torchaudio
from audiocraft.models import AudioGen

def batch_generate_sounds(sound_specs, output_dir):
    """
    Generate multiple sound effects from a list of specifications.

    Args:
        sound_specs: list of {"name": str, "description": str, "duration": float}
        output_dir: directory where the wav files will be written
    """
    model = AudioGen.get_pretrained("facebook/audiogen-medium")
    out_path = Path(output_dir)
    out_path.mkdir(parents=True, exist_ok=True)

    results = []

    for spec in sound_specs:
        model.set_generation_params(duration=spec.get("duration", 5))
        wav = model.generate([spec["description"]])
        file_path = out_path / f"{spec['name']}.wav"
        torchaudio.save(str(file_path), wav[0].cpu(), sample_rate=16_000)

        results.append(
            {
                "name": spec["name"],
                "path": str(file_path),
                "description": spec["description"],
            }
        )
    return results

# Example specifications
sounds = [
    {"name": "explosion", "description": "massive explosion with debris", "duration": 3},
    {"name": "footsteps", "description": "footsteps on wooden floor", "duration": 5},
    {"name": "door", "description": "wooden door creaking and closing", "duration": 2},
]

batch_results = batch_generate_sounds(sounds, "sound_effects/")
print(json.dumps(batch_results, indent=2))
```

### Workflow 3 – Gradio demo for interactive generation

```python
import gradio as gr
import torch
import torchaudio
from audiocraft.models import MusicGen

model = MusicGen.get_pretrained("facebook/musicgen-small")

def generate_music(prompt, duration, temperature, cfg_coef):
    model.set_generation_params(
        duration=duration,
        temperature=temperature,
        cfg_coef