# Wyoming Chatterbox - Specification

## Project Overview

**Project Name:** wyoming-chatterbox
**Type:** TTS Server (Wyoming Protocol)
**Core Functionality:** Wyoming protocol server using Chatterbox-Turbo for text-to-speech, compatible with Home Assistant and Rhasspy voice assistants.
**Target Users:** Home Assistant users, voice assistant enthusiasts replacing Piper with Chatterbox-Turbo

## Architecture

### Components
1. **Chatterbox-Turbo TTS Engine** - Core TTS model from Resemble AI
2. **Wyoming Protocol Server** - TCP/UDP server implementing Wyoming protocol
3. **HTTP API** - Optional HTTP endpoint for direct TTS requests

### Ports
- **10200/TCP** - Wyoming protocol (binary JSONL + PCM audio)
- **5000/TCP** - HTTP API (for direct TTS requests)

## Wyoming Protocol Implementation

### Event Types (TTS)

#### synthesize (request)
```json
{
  "type": "synthesize",
  "data": {
    "text": "Hello world",
    "voice": {"name": "default"},
    "language": "en"
  }
}
```

#### synthesize-start (response)
```json
{
  "type": "synthesize-start",
  "data": {
    "voice": {"name": "default"},
    "language": "en"
  }
}
```

#### audio-chunk (response)
```json
{
  "type": "audio-chunk",
  "data": {
    "rate": 24000,
    "width": 2,
    "channels": 1
  }
}
```
Payload: Raw PCM audio bytes

#### synthesize-stop (request)
```json
{"type": "synthesize-stop"}
```

#### synthesize-stopped (response)
```json
{"type": "synthesize-stopped"}
```

#### info (response)
```json
{
  "type": "info",
  "data": {
    "tts": {
      "models": [
        {
          "name": "default",
          "languages": ["en"],
          "attribution": {"name": "Resemble AI", "url": "https://resemble.ai"},
          "installed": true,
          "description": "Chatterbox-Turbo - State-of-the-art open-source TTS"
        }
      ],
      "supports_synthesize_streaming": true
    },
    "name": "wyoming-chatterbox",
    "version": "1.0.0"
  }
}
```

## Docker Configuration

### Base Image
- `nvidia/cuda:12.4.0-runtime-ubuntu22.04` (for GPU support)
- `ubuntu:22.04` (fallback for CPU-only)

### Dependencies
- Python 3.11+
- PyTorch (with CUDA support)
- torchaudio
- chatterbox-tts
- numpy

### Runtime
- Model cached in `/data/models`
- Sample audio prompts stored in `/data/prompts`

## API Usage

### Wyoming Protocol (TCP port 10200)
Standard Wyoming protocol communication (same as Piper)

### HTTP API (port 5000)

#### POST /api/tts
```bash
curl -X POST http://localhost:5000/api/tts \
  -H "Content-Type: application/json" \
  -d '{"text": "Hello world", "voice": "default"}' \
  --output audio.wav
```

Query parameters:
- `text` (required): Text to synthesize
- `voice` (optional): Voice name (default: "default")
- `language` (optional): Language code (default: "en")

#### GET /api/info
Returns server info and available voices

## Voice Configuration

### Default Voice
- Name: `default`
- Language: English
- Requires: Audio prompt reference for voice cloning

### Custom Voices
Place `.wav` reference audio files in `/data/prompts/` directory
- Filename format: `{voice_name}.wav`
- Recommended: 10-30 seconds of clean speech

## Streaming Support

Full streaming support via Wyoming protocol:
1. Client sends `synthesize` with text
2. Server responds with `synthesize-start`
3. Server streams audio via `audio-chunk` events
4. Server sends `synthesize-stopped` when complete

## Configuration Options

### Environment Variables
- `MODEL_DEVICE` - Device to use (cuda/cpu, default: cuda if available)
- `DEFAULT_VOICE` - Default voice name
- `WYOMING_PORT` - Wyoming protocol port (default: 10200)
- `HTTP_PORT` - HTTP API port (default: 5000)

### Command Line Arguments
```
--voice NAME       Default voice name (default: default)
--device DEVICE    Device to use: cuda or cpu (default: cuda)
--uri URI          Wyoming URI (default: tcp://0.0.0.0:10200)
--http-port PORT   HTTP server port (default: 5000)
--data-dir DIR     Data directory (default: /data)
--download-dir DIR  Download directory (default: /data)
```

## Compatibility

### With Piper
- Same Wyoming protocol implementation
- Drop-in replacement for wyoming-piper
- Compatible with Home Assistant Wyoming integration

### Tested With
- Home Assistant OS / Supervised
- Rhasspy voice assistant
- wyoming-openai proxy

## Build & Run

### Build
```bash
docker build -t wyoming-chatterbox .
```

### Run (CPU)
```bash
docker run -d -p 10200:10200 -p 5000:5000 \
  -v /path/to/prompts:/data/prompts \
  wyoming-chatterbox --voice default
```

### Run (GPU)
```bash
docker run -d --gpus all -p 10200:10200 -p 5000:5000 \
  -v /path/to/prompts:/data/prompts \
  wyoming-chatterbox --voice default --device cuda
```

## File Structure
```
wyoming-chatterbox/
├── Dockerfile
├── README.md
├── pyproject.toml
├── requirements.txt
├── src/
│   └── wyoming_chatterbox/
│       ├── __init__.py
│       ├── server.py          # Main Wyoming server
│       ├── handler.py         # TTS request handler
│       ├── chatterbox_tts.py  # Chatterbox wrapper
│       └── http_server.py     # Optional HTTP API
├── script/
│   ├── setup
│   └── run
└── tests/
```
