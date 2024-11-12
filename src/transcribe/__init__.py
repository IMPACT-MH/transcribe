# src/__init__.py

# Import commonly used functions and classes for easier access
from .audio_utils import convert_audio, TranscriptionError, clean_tmp_dir
from .device_utils import check_device_compatibility
from .transcription_utils import format_time, transcribe_chunk, transcribe_audio