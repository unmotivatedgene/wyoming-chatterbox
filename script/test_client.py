#!/usr/bin/env python3
"""Test client for Wyoming Chatterbox server."""

import asyncio
import json
import sys
import wave

from wyoming.client import AsyncTcpClient
from wyoming.tts import Synthesize
from wyoming.info import Describe


async def test_server(
    host: str = "localhost",
    port: int = 10200,
    text: str = "Hello! This is a test of the Chatterbox TTS system.",
    output_file: str = "test_output.wav",
):
    """Connect to Wyoming server and synthesize speech."""
    print(f"Connecting to {host}:{port}...")
    
    try:
        async with AsyncTcpClient(host, port) as client:
            # Request info
            await client.write_event(Describe().event())
            
            # Read info response
            info_event = await client.read_event()
            if info_event:
                print(f"Received event type: {info_event.type}")
                if info_event.data:
                    info = info_event.data
                    print(f"Server info: {info.get('tts', [{}])[0].get('name', 'unknown')}")
            
            # Send synthesize request
            print(f"Synthesizing: {text}")
            synthesize = Synthesize(text=text)
            await client.write_event(synthesize.event())
            
            # Collect audio
            audio_data = bytearray()
            sample_rate = 24000
            width = 2
            channels = 1
            
            while True:
                event = await client.read_event()
                if not event:
                    break
                    
                event_type = event.type
                print(f"Received: {event_type}")
                
                if event_type == "audio-start":
                    if event.data:
                        sample_rate = event.data.get("rate", 24000)
                        width = event.data.get("width", 2)
                        channels = event.data.get("channels", 1)
                
                elif event_type == "audio-stop":
                    break
                    
                elif event_type == "audio-chunk":
                    if event.audio:
                        audio_data.extend(event.audio)
            
            # Write WAV file
            if audio_data:
                with wave.open(output_file, "wb") as wav:
                    wav.setnchannels(channels)
                    wav.setsampwidth(width)
                    wav.setframerate(sample_rate)
                    wav.writeframes(bytes(audio_data))
                print(f"Audio saved to: {output_file}")
            else:
                print("No audio received")
                
    except ConnectionRefusedError:
        print(f"Error: Could not connect to {host}:{port}")
        print("Make sure the server is running: docker run -p 10200:10200 wyoming-chatterbox")
        sys.exit(1)
    except Exception as e:
        import traceback
        print(f"Error: {e}")
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Test Wyoming Chatterbox TTS")
    parser.add_argument("--host", default="localhost", help="Server host")
    parser.add_argument("--port", type=int, default=10200, help="Server port")
    parser.add_argument("--text", default="Hello! This is a test.", help="Text to synthesize")
    parser.add_argument("--output", default="test_output.wav", help="Output WAV file")
    
    args = parser.parse_args()
    asyncio.run(test_server(args.host, args.port, args.text, args.output))
