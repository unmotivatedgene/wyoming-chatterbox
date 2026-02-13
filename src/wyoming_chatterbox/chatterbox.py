"""Chatterbox TTS wrapper."""

import logging
import os
import sys
from typing import Optional

import torch

# Patch perth module BEFORE importing chatterbox
# The PyPI perth package is broken - create dummyDummyWatermarker classes
class _:
    """Dummy watermarker that does nothing."""
    def __init__(self, *args, **kwargs):
        pass
    
    def embed(self, *args, **kwargs):
        return args[0] if args else None
    
    def get_watermark(self, *args, **kwargs):
        return 0.0
    
    def apply_watermark(self, wav, sample_rate=None):
        """Apply watermark - returns audio unchanged."""
        return wav

# Install dummy perth module before chatterbox imports it
class _DummyPerthModule:
    """Dummy perth module with working classes."""
    PerthImplicitWatermarker = _
    DummyWatermarker = _
    WatermarkerBase = object
    WatermarkingException = Exception
    
    @staticmethod
    def __getattr__(name):
        return _

# Replace perth in sys.modules BEFORE any chatterbox imports
sys.modules['perth'] = _DummyPerthModule()

from chatterbox.tts_turbo import ChatterboxTurboTTS

_LOGGER = logging.getLogger(__name__)


class ChatterboxTTS:
    """Wrapper for Chatterbox-Turbo TTS model."""

    def __init__(self, model: ChatterboxTurboTTS):
        self._model = model
        self.sr = model.sr

    @classmethod
    def from_pretrained(cls, device: str = "cuda", hf_token: Optional[str] = None) -> "ChatterboxTTS":
        """Load Chatterbox-Turbo model."""
        _LOGGER.info(f"Loading Chatterbox-Turbo on {device}...")
        
        # Set token in environment if provided
        if hf_token:
            os.environ["HF_TOKEN"] = hf_token
        
        model = ChatterboxTurboTTS.from_pretrained(device=device)
        return cls(model)

    def generate(self, text: str, audio_prompt_path: Optional[str] = None):
        """Generate speech from text."""
        return self._model.generate(text=text, audio_prompt_path=audio_prompt_path)
