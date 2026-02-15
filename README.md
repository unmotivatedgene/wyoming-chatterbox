# Wyoming Chatterbox

> **Created in conjunction with AI** 🤖

AI Rewrite of a personal project based on [wyoming-piper](https://github.com/rhasspy/wyoming-piper) where I swapped Piper for Maya1, now making it Chatterbox.

## License

MIT License - See LICENSE file for details.

**No Warranty**: This software is provided "as is", without warranty of any kind, express or implied.

## Features

- **Wyoming Protocol**: Compatible with Home Assistant and Rhasspy
- **Chatterbox-Turbo**: Fast, low-latency TTS model (350M parameters)
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

## Paralinguistic Tags

Chatterbox supports embedded audio tags for natural speech effects:

| Tag | Description | Example Usage |
|-----|-------------|---------------|
| `[clear throat]` | Throat clearing sound | Start of speech |
| `[sigh]` | Sighing | Expressing frustration |
| `[shush]` | Shushing sound | Quieting someone |
| `[cough]` | Coughing | Natural interruption |
| `[groan]` | Groaning | Expressing discomfort |
| `[sniff]` | Sniffing | Emotional or physical response |
| `[gasp]` | Gasping | Surprise or shock |
| `[chuckle]` | Light laughter | Mild amusement |
| `[laugh]` | Full laughter | Strong amusement |

Example: "Well, [sigh] I guess that's it. [laugh] Thanks for listening!"

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

## License

MIT License

Copyright (c) 2026

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
