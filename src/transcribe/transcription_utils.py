# src/transcription_utils.py

from faster_whisper import WhisperModel
from typing import Optional, List
import os
os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"
import json
import logging
from time import time
from tqdm import tqdm
from datetime import timedelta

from .audio_utils import TranscriptionError, convert_audio, clean_tmp_dir

logger = logging.getLogger(__name__)


def format_time(seconds: float) -> str:
    """Format seconds into human readable time."""
    return str(timedelta(seconds=round(seconds)))


def transcribe_chunk(
    model: 'WhisperModel',
    audio_path: str,
    language: Optional[str] = None,
    initial_prompt: Optional[str] = None
) -> List[dict]:
    """Transcribe a single audio chunk."""
    segments, _ = model.transcribe(
        audio_path,
        language=language,
        initial_prompt=initial_prompt,
        beam_size=5,
        vad_filter=True,
        vad_parameters=dict(
            min_silence_duration_ms=500,
            speech_pad_ms=400
        )
    )
    
    return [
        {
            "start": segment.start,
            "end": segment.end,
            "text": segment.text.strip()
        }
        for segment in segments
    ]


def transcribe_audio(
    audio_path: str,
    model: WhisperModel,
    language: Optional[str] = None,
    output_format: str = "txt"
) -> str:
    """
    Transcribe an audio file sequentially by chunks with progress tracking.
    """
    try:
        start_time = time()
        
        # Get just the filename without path
        base_name = os.path.basename(audio_path)
        # Remove extension
        base_name = os.path.splitext(base_name)[0]
        # Create output path in current directory
        output_path = f"{base_name}.{output_format}"
        
        # Convert and split audio
        chunk_paths = convert_audio(audio_path)
        total_chunks = len(chunk_paths)  # Define total_chunks here
        
        # Process chunks sequentially with progress tracking
        all_segments = []
        chunk_times = []
        initial_prompt = None
        
        logger.info(f"\nProcessing {total_chunks} chunks sequentially:")
        for i, chunk_path in enumerate(chunk_paths, 1):
            chunk_start = time()
            
            # Log chunk start
            logger.info(f"\nChunk {i}/{total_chunks}:")
            segments = transcribe_chunk(model, chunk_path, language, initial_prompt)
            
            # Calculate and log chunk timing
            chunk_duration = time() - chunk_start
            chunk_times.append(chunk_duration)
            logger.info(f"✓ Processed in {format_time(chunk_duration)}")
            
            # Update initial prompt for next chunk
            if segments:
                initial_prompt = segments[-1]["text"]
            
            # Adjust timestamps
            if i > 1:  # First chunk starts at 0
                time_offset = (i - 1) * 10 * 60  # 10 minutes per chunk
                for segment in segments:
                    segment["start"] += time_offset
                    segment["end"] += time_offset
            
            # Add segments and clean up
            all_segments.extend(segments)
            
            # Show progress percentage
            progress = (i / total_chunks) * 100
            logger.info(f"Overall progress: {progress:.1f}%")
        
        # Save results
        logger.info("\nSaving transcript...")
        if output_format == "txt":
            with open(output_path, "w", encoding="utf-8") as f:
                for segment in all_segments:
                    minutes, seconds = divmod(segment["start"], 60)
                    hours, minutes = divmod(minutes, 60)
                    timestamp = f"[{int(hours):02d}:{int(minutes):02d}:{seconds:05.2f}]"
                    f.write(f"{timestamp} {segment['text']}\n")
        else:  # json format
            with open(output_path, "w", encoding="utf-8") as f:
                json.dump({"segments": all_segments}, f, ensure_ascii=False, indent=2)

        # Calculate and display timing statistics
        total_time = time() - start_time
        avg_time = sum(chunk_times) / len(chunk_times) if chunk_times else 0
        
        logger.info("\nTranscription Statistics:")
        logger.info("=" * 50)
        logger.info(f"Total chunks processed: {total_chunks}")
        logger.info(f"Total processing time: {format_time(total_time)}")
        logger.info(f"Average chunk time:    {format_time(avg_time)}")
        if chunk_times:
            logger.info(f"Fastest chunk:        {format_time(min(chunk_times))}")
            logger.info(f"Slowest chunk:        {format_time(max(chunk_times))}")
        logger.info("=" * 50)
        
        logger.info(f"\nTranscription saved to: {output_path}")
        return output_path

    except Exception as e:
        logger.error(f"Transcription failed: {str(e)}")
        raise TranscriptionError(f"Transcription failed: {str(e)}")
    finally:
        # Clean up temporary files
        clean_tmp_dir()