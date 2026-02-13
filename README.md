# Wyoming Chatterbox

Wyoming protocol server for Chatterbox-Turbo TTS with web interface.

## Features

- **Wyoming Protocol**: Compatible with Home Assistant and Rhasspy
- **Voice Cloning**: Upload audio clips to create custom voices
- **Web Interface**: Test TTS, manage voices, and configure settings
- **Streaming**: Full audio streaming support

## Quick Start

```bash
# Build
docker build -t wyoming-chatterbox .

# Run (CPU)
docker run -d -p 10200:10200 -p 5000:5000 \
  -v ./prompts:/data/prompts \
  wyoming-chatterbox --device cpu

# Run (GPU)
docker run -d --gpus all -p 10200:10200 -p 5000:5000 \
  -v ./prompts:/data/prompts \
  wyoming-chatterbox --device cuda
```

## Ports

- **10200/TCP**: Wyoming protocol (for Home Assistant)
- **5000/TCP**: Web interface and HTTP API

## Web Interface

Open http://localhost:5000 to:
- Test text-to-speech synthesis
- Upload audio clips for voice cloning
- Manage and delete custom voices

## Wyoming Protocol Usage

```python
from wyoming.client import AsyncTcpClient
from wyoming.tts import Synthesize

async with AsyncTcpClient("localhost", 10200) as client:
    await client.write_event(Synthesize(text="Hello!").event())
    # Read audio events...
```

## Voice Cloning

1. Open the web interface at http://localhost:5000
2. Upload an audio file (WAV, MP3, FLAC, OGG, M4A)
3. Enter a name for the voice
4. Use the voice in synthesis

## API

### POST /api/tts
```bash
curl -X POST http://localhost:5000/api/tts \
  -H "Content-Type: application/json" \
  -d '{"text": "Hello world", "voice": "my-voice"}' \
  --output speech.wav
```

### GET /api/info
Returns server status and available voices.

### GET /api/voices
List all available voice prompts.
