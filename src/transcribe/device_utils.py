# src/device_utils.py

import os
import torch
import logging
import platform

logger = logging.getLogger(__name__)

def check_device_compatibility() -> tuple[str, int]:
    """
    Check and return the best available device for processing.
    Supports CUDA (NVIDIA), MPS (Apple Silicon), and CPU.
    """
    try:
        # Check for CUDA (NVIDIA GPUs)
        if torch.cuda.is_available():
            logger.info("CUDA (NVIDIA GPU) detected")
            return "float16", os.cpu_count() or 4

        # Check for MPS (Apple Silicon)
        if platform.system() == "Darwin" and hasattr(torch.backends, "mps") and torch.backends.mps.is_available():
            logger.info("MPS (Apple Silicon) detected")
            return "float32", os.cpu_count() or 4

        # Fallback to CPU
        logger.info("No GPU detected, using CPU")
        return "int8", os.cpu_count() or 4

    except Exception as e:
        logger.warning(f"Error checking device compatibility: {e}, falling back to CPU")
        return "int8", os.cpu_count() or 4