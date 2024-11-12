# src/audio_utils.py

from pydub import AudioSegment
from typing import List
import logging
import os
import tempfile
from pathlib import Path
import shutil

logger = logging.getLogger(__name__)

class TranscriptionError(Exception):
    """Custom exception for transcription-related errors."""
    pass

def format_duration(milliseconds: int) -> str:
    """Format milliseconds into human readable time."""
    seconds = milliseconds / 1000
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    seconds = int(seconds % 60)
    return f"{hours:02d}:{minutes:02d}:{seconds:02d}"

def get_transcribe_temp_dir() -> str:
    """
    Get system's temp directory path with a transcribe subdirectory.
    This will be:
        - /tmp/transcribe on Linux/Mac
        - C:\\Users\\<user>\\AppData\\Local\\Temp\\transcribe on Windows
    """
    temp_dir = os.path.join(tempfile.gettempdir(), 'transcribe')
    os.makedirs(temp_dir, exist_ok=True)
    return temp_dir

def get_temp_filepath(prefix: str, suffix: str) -> str:
    """Get a file path in the system's temp directory."""
    temp_dir = get_transcribe_temp_dir()
    return os.path.join(temp_dir, f"{prefix}{suffix}")

def clean_tmp_dir() -> None:
    """Remove the transcribe directory from system temp."""
    temp_dir = get_transcribe_temp_dir()
    try:
        shutil.rmtree(temp_dir)
        logger.debug(f"Cleaned up temporary directory: {temp_dir}")
    except Exception as e:
        logger.warning(f"Failed to clean temporary directory {temp_dir}: {e}")

def convert_audio(audio_path: str, output_format: str = "wav") -> List[str]:
    """Convert audio file to specified format and split into chunks."""
    try:
        # Clean any existing temp files
        clean_tmp_dir()
        
        logger.info(f"Loading audio file: {audio_path}")
        audio = AudioSegment.from_file(audio_path)
        
        # Log original audio properties
        duration = len(audio)
        logger.info(f"Audio duration: {format_duration(duration)}")
        logger.info(f"Original: {audio.channels} channels, {audio.frame_rate}Hz")
        
        # Convert audio properties
        logger.info("Converting to mono 16kHz...")
        audio = audio.set_channels(1).set_frame_rate(16000)
        
        chunk_duration = 10 * 60 * 1000  # 10 minutes in milliseconds
        chunks = []
        for i in range(0, len(audio), chunk_duration):
            chunks.append(audio[i:i + chunk_duration])
        
        chunk_paths = []
        logger.info(f"Splitting into {len(chunks)} chunks...")
        
        for i, chunk in enumerate(chunks):
            # Create temporary file in system temp directory
            temp_path = get_temp_filepath(f"chunk_{i}", f".{output_format}")
            chunk.export(temp_path, format=output_format)
            chunk_paths.append(temp_path)
        
        return chunk_paths
    except Exception as e:
        # Clean up on error
        clean_tmp_dir()
        raise TranscriptionError(f"Audio conversion failed: {str(e)}")