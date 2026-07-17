# Whisper Audio Transcription

A simple tool to transcribe audio files using OpenAI's Whisper model. Generates timestamped text transcriptions from audio recordings.

## Requirements

- Python 3.8+
- FFmpeg (required by Whisper for audio processing)

## Installation

### 1. Install FFmpeg

**macOS:**
```bash
brew install ffmpeg
```

**Ubuntu/Debian:**
```bash
sudo apt update && sudo apt install ffmpeg
```

**Windows:**
Download from [ffmpeg.org](https://ffmpeg.org/download.html) and add to PATH.

### 2. Install Python dependencies

On modern macOS there is no bare `pip` command (only `pip3`), and installing
into the system Python is discouraged. Use a project-local virtual environment:

```bash
# Create and activate a virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install dependencies (inside the venv, `pip` now exists)
pip install -r requirements.txt
```

Re-activate the environment with `source .venv/bin/activate` in any new shell
before running the tool. To leave it, run `deactivate`.

> If you prefer not to use a venv, install straight into your user Python with
> `pip3 install -r requirements.txt`.

This will install:
- `openai-whisper` — OpenAI's Whisper speech recognition model
  (this pulls in PyTorch, a multi-GB download, on first install)

## Project Structure

```
whisper/
├── transcript.py        # Main transcription script
├── makefile             # Convenience commands
├── requirements.txt     # Python dependencies
├── files/
│   └── source/          # Place your audio files here
└── transcriptions/      # Output transcriptions appear here
```

## Usage

### Setup

1. Create the source directory if it doesn't exist:
   ```bash
   mkdir -p files/source
   ```

2. Place your audio file in `files/source/`

### Transcribe an audio file

**Using make (recommended):**

```bash
# Best quality transcription (large model)
make transcribe file=myaudio.mp3

# Fast transcription (small model, good for testing)
make transcribe-fast file=myaudio.mp3
```

**Using Python directly:**

```bash
python3 transcript.py <filename> [options]
```

### Command Line Options

| Option | Default | Description |
|--------|---------|-------------|
| `filename` | (required) | Audio file name in `files/source/` |
| `--model` | `large` | Whisper model size |
| `--language` | `es` | Language code for transcription |

### Model Sizes

| Model | Parameters | Speed | Quality | VRAM Required |
|-------|------------|-------|---------|---------------|
| `tiny` | 39M | Fastest | Basic | ~1 GB |
| `base` | 74M | Fast | Good | ~1 GB |
| `small` | 244M | Medium | Better | ~2 GB |
| `medium` | 769M | Slow | Great | ~5 GB |
| `large` | 1550M | Slowest | Best | ~10 GB |

### Language Codes

Common language codes:
- `es` — Spanish
- `en` — English
- `fr` — French
- `de` — German
- `pt` — Portuguese
- `it` — Italian
- `zh` — Chinese
- `ja` — Japanese

For a full list, see [Whisper's supported languages](https://github.com/openai/whisper#available-models-and-languages).

## Examples

```bash
# Transcribe Spanish interview with best quality
python3 transcript.py interview.mp3 --model large --language es

# Quick English transcription for testing
python3 transcript.py podcast.m4a --model small --language en

# Transcribe with medium model (balance of speed/quality)
python3 transcript.py recording.aac --model medium --language es
```

## Output Format

Transcriptions are saved to `transcriptions/<filename>.txt` with timestamps:

```
[0.00 - 10.22]: Hola, buenos días. Vamos a empezar con la charla.
[10.22 - 14.92]: En primer lugar, quería preguntarte si estás de acuerdo...
[14.92 - 20.72]: Sí, estoy de acuerdo. Genial.
```

## Supported Audio Formats

Whisper (via FFmpeg) supports most common audio formats:
- MP3
- M4A / AAC
- WAV
- FLAC
- OGG
- WMA
- And many more

## Tips

- **First run is slow**: Whisper downloads the model on first use (~3GB for large model)
- **Use `small` for testing**: Much faster, still good quality
- **Specify language**: Improves accuracy and speed vs auto-detection
- **Long files**: For very long recordings (>1 hour), expect processing time of 10-30+ minutes with the large model

## Troubleshooting

**"File not found" error:**
Make sure your audio file is in `files/source/` directory.

**Out of memory:**
Use a smaller model (`--model small` or `--model base`).

**Poor transcription quality:**
- Try the `large` model
- Ensure audio is clear with minimal background noise
- Verify the correct language is specified

