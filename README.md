# 🎙️ Whisper Transcription CLI

Fast, accurate audio transcription powered by OpenAI's Whisper model, optimized for Apple Silicon and NVIDIA GPUs.

## ✨ Features
- 🚀 Hardware-accelerated transcription using Metal (Apple Silicon) or CUDA (NVIDIA)
- 🎯 Multiple accuracy levels from ultra-fast to production-quality
- 🌍 Supports 100+ languages with auto-detection
- ⚡ Processes 10-minute audio in 1-7 minutes (model dependent)
- 📝 Flexible output formats (TXT/JSON) with timestamps

## 🚀 Quick Start (macOS)
```bash
# Install prerequisites
brew install ffmpeg python@3.11

# Setup environment
python3.11 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip

# Install package
pip install --pre torch torchvision torchaudio --index-url https://download.pytorch.org/whl/nightly/cpu
pip install faster-whisper pydub tqdm
pip install -e .

# Run transcription
transcribe audio_file.m4a
```

## 🛠️ Installation 

### macOS (Apple Silicon)

1. **Install required tools**:
```bash
# Install ffmpeg if you don't have it
brew install ffmpeg

# Install Python 3.11
brew install python@3.11
```

2. **Create and activate virtual environment**:
```bash
# Create a new virtual environment with Python 3.11 specifically
python3.11 -m venv .venv

# Activate the environment
source .venv/bin/activate
```

3. **Update pip**:
```bash
pip install --upgrade pip
```

4. **Install PyTorch with Apple Silicon support**:
```bash
pip install --pre torch torchvision torchaudio --index-url https://download.pytorch.org/whl/nightly/cpu
```

5. **Install faster-whisper and dependencies**:
```bash
pip install faster-whisper pydub tqdm
```

6. **Install the package in editable mode**:
```bash
pip install -e .
```

### Windows/Linux (NVIDIA GPU)
```bash
# Ubuntu/Debian
sudo apt update && sudo apt install ffmpeg python3.11 python3.11-venv
# OR Windows (using chocolatey)
choco install ffmpeg python311

# Create and activate environment
python3.11 -m venv .venv
# Linux:
source .venv/bin/activate
# Windows:
.\.venv\Scripts\activate

# Install packages with CUDA support
pip install --upgrade pip
pip install torch torchaudio --index-url https://download.pytorch.org/whl/cu118
pip install faster-whisper pydub tqdm
pip install -e .
```

## 📚 Usage Guide

### Command Structure
```bash
transcribe <audio_file> [options]
```

### Model Selection
Choose the model that best fits your needs:

| Model    | Speed      | Accuracy   | Use Case                    |
|----------|------------|------------|----------------------------|
| `tiny`   | ⚡⚡⚡⚡⚡ | ⭐        | Quick testing/prototyping   |
| `base`   | ⚡⚡⚡⚡  | ⭐⭐      | Development/general use     |
| `small`  | ⚡⚡⚡    | ⭐⭐⭐    | Better accuracy needed      |
| `medium` | ⚡⚡      | ⭐⭐⭐⭐  | High accuracy required      |
| `large-v2`| ⚡        | ⭐⭐⭐⭐⭐| Production/Critical content |

### Available Options
| Option | Description | Values | Default |
|--------|-------------|---------|---------|
| `-m, --model` | Whisper model size | `tiny`, `base`, `small`, `medium`, `large-v2` | `base` |
| `-f, --format` | Output format | `txt`, `json` | `txt` |
| `-l, --language` | Language code | `en`, `fr`, `de`, etc. | auto-detect |
| `--list-models` | Show available models | - | - |
| `-h, --help` | Show help message | - | - |

### Example Commands
```bash
# Basic usage (fastest)
transcribe podcast.mp3 -m tiny

# High accuracy with timestamps
transcribe interview.wav -m large-v2 -f json

# Specific language with medium model
transcribe speech.m4a -m medium -l fr
```

## 📝 Output Formats

### Text Output (Default)
```
[00:00:00.000] First segment of transcription
[00:00:05.230] Next segment of transcription
```

### JSON Output
```json
{
  "segments": [
    {
      "start": 0.0,
      "end": 5.0,
      "text": "First segment of transcription"
    },
    {
      "start": 5.23,
      "end": 8.95,
      "text": "Next segment of transcription"
    }
  ]
}
```

## ⚡ Performance

### Hardware Acceleration
- **Apple Silicon**: Uses Metal Performance Shaders (MPS) for optimal speed
- **NVIDIA GPUs**: CUDA acceleration with float16 computation
- **CPU**: Optimized fallback with int8 quantization

### Processing Speed (10min audio)
| Model     | Time  | Speed vs Real-time |
|-----------|-------|-------------------|
| tiny      | 1-2m  | 5-10x            |
| base      | 2-3m  | 3-5x             |
| large-v2  | 5-7m  | 1.5-2x           |

## 💻 System Requirements

### Hardware (One of)
- Apple Silicon Mac (M1/M2/M3)
- NVIDIA GPU with CUDA support
- Modern CPU (fallback)

### Software
- Python 3.11
- ffmpeg
- PyTorch 2.0+
- faster-whisper
- pydub, tqdm
