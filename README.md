# 🎙️ AI Transcription Tool Documentation

## 🛠️ Building the Environment

### Prerequisites
- Python 3.9 or higher
- pip package manager

### Installation Steps

1. **Create and activate a virtual environment**:
```bash
python3 -m venv env
source env/bin/activate  # On Unix/macOS
.\env\Scripts\activate   # On Windows
```

2. **Install all required packages**:
```bash
pip install torch torchaudio faster-whisper pydub tqdm
```

## 🎮 Command Options

### Basic Command Structure
```bash
transcribe <audio_file> [options]
```

### Available Options
| Option | Description | Values | Default |
|--------|-------------|---------|---------|
| `-m, --model` | Whisper model size | `tiny`, `base`, `small`, `medium`, `large-v2` | `base` |
| `-f, --format` | Output format | `txt`, `json` | `txt` |
| `-l, --language` | Language code (optional) | e.g., `en`, `fr`, `de`, etc. | auto-detect |
| `--list-models` | Show available models | - | - |
| `-h, --help` | Show help message | - | - |

### Model Descriptions
- `tiny`: Fastest, least accurate (good for testing)
- `base`: Good balance of speed and accuracy
- `small`: Better accuracy, slower than base
- `medium`: High accuracy, significantly slower
- `large-v2`: Highest accuracy, slowest (best for production)

### Examples
1. **Basic transcription** (uses base model):
```bash
transcribe audio_file.m4a
```

2. **Fast transcription** (for testing):
```bash
transcribe audio_file.m4a -m tiny
```

3. **High accuracy** (slower):
```bash
transcribe audio_file.m4a -m large-v2
```

4. **JSON output with timestamps**:
```bash
transcribe audio_file.m4a -f json
```

5. **Specific language**:
```bash
transcribe audio_file.m4a -l en
```

6. **Combined options**:
```bash
transcribe audio_file.m4a -m medium -f json -l fr
```

## 📝 Output Formats

### TXT Format (default)
```
[00:00:00.000] First segment of transcription
[00:00:05.230] Next segment of transcription
```

### JSON Format
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

## ⚡ Hardware Acceleration

### NVIDIA GPUs (Windows/Linux)
- Uses CUDA for GPU acceleration
- Supports float16 computation
- Best performance on NVIDIA graphics cards

### Apple Silicon (macOS)
- Uses MPS (Metal Performance Shaders)
- Optimized for M1/M2/M3 chips
- Uses float32 computation

### CPU (All Platforms)
- Falls back to CPU if no GPU is available
- Uses int8 quantization for efficiency
- Works on any system

## ⏱️ Performance Notes
- Model speed (fastest to slowest): tiny → base → small → medium → large-v2
- Each 10-minute chunk is processed sequentially
- Time estimates per chunk:
  - `tiny`: ~1-2 minutes
  - `base`: ~2-3 minutes
  - `large-v2`: ~5-7 minutes
- Metal acceleration is used when available on Apple Silicon

## 💻 System Requirements

### Hardware Requirements (any of the following):
- NVIDIA GPU with CUDA support (Windows/Linux)
- Apple Silicon Mac (M1/M2/M3)
- Any modern CPU (fallback option)

### Software Requirements
- Python 3.9+
- PyTorch 2.0+
- faster-whisper
- pydub (for audio processing)
- tqdm (for progress bars)
