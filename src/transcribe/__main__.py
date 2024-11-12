# transcribe/__main__.py

import os
import argparse
import sys
import logging
from . import check_device_compatibility, transcribe_audio
from faster_whisper import WhisperModel

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

MODELS = {
    'tiny': 'Fastest, least accurate (good for testing)',
    'base': 'Good balance of speed and accuracy',
    'small': 'Better accuracy, slower than base',
    'medium': 'High accuracy, significantly slower',
    'large-v2': 'Highest accuracy, slowest (best for production)'
}

def print_model_info():
    """Print information about available models."""
    logger.info("\nAvailable Models:")
    logger.info("=" * 60)
    for model, description in MODELS.items():
        logger.info(f"{model:8} - {description}")
    logger.info("=" * 60)

def parse_arguments():
    parser = argparse.ArgumentParser(
        description='Transcribe audio using Whisper with MPS acceleration',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    
    parser.add_argument(
        'audio_path',
        type=str,
        help='Path to the audio file to transcribe'
    )
    
    parser.add_argument(
        '-m', '--model',
        type=str,
        choices=list(MODELS.keys()),
        default='base',
        help='Whisper model size to use (see model descriptions below)'
    )
    
    parser.add_argument(
        '-f', '--format',
        type=str,
        choices=['txt', 'json'],
        default='txt',
        help='Output format for transcription'
    )
    
    parser.add_argument(
        '-l', '--language',
        type=str,
        help='Language code (optional, e.g., "en" for English)'
    )
    
    # Add --list-models flag
    parser.add_argument(
        '--list-models',
        action='store_true',
        help='List available models and their descriptions'
    )
    
    args = parser.parse_args()
    
    # If --list-models is specified, print model info and exit
    if args.list_models:
        print_model_info()
        sys.exit(0)
    
    return args

def main():
    args = parse_arguments()
    try:
        # Print selected model info
        logger.info("\nTranscription Configuration:")
        logger.info("=" * 60)
        logger.info(f"Model selected: {args.model}")
        logger.info(f"Model description: {MODELS[args.model]}")
        if args.language:
            logger.info(f"Language: {args.language}")
        logger.info(f"Output format: {args.format}")
        logger.info("=" * 60 + "\n")
        
        # Configure compute settings
        compute_type, num_threads = check_device_compatibility()
        
        # Initialize model
        logger.info(f"Initializing {args.model} model...")
        model = WhisperModel(
            model_size_or_path=args.model,
            device="cpu",
            compute_type=compute_type,
            num_workers=1,
            cpu_threads=num_threads,
            download_root=os.path.expanduser("~/.cache/whisper")
        )
        
        # Run transcription
        output_file = transcribe_audio(
            audio_path=args.audio_path,
            model=model,
            language=args.language,
            output_format=args.format
        )
        
        print(f"\nTranscription saved to: {output_file}")
        sys.exit(0)
    except Exception as e:
        logger.error(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()