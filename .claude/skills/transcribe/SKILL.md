---
name: transcribe
description: Transcribe an audio file to timestamped text using this repo's Whisper setup. Use when the user wants to transcribe, caption, or get a text version of an audio recording (mp3, m4a, opus, wav, aac, flac, etc.). Handles venv, file placement, model/language selection, and reading back the result.
---

# Transcribe audio with Whisper

This skill drives `transcript.py` (OpenAI Whisper) in this repository. The script
is rigid about paths and args, so this skill wraps it: place the input correctly,
run it through the project venv, and read the result back.

## Hard facts about the script

- Input **must** live at `files/source/<filename>` — the script builds
  `./files/source/<filename>` and exits with an error if it's missing.
- Output is written to `transcriptions/<name>.txt` (name without extension).
  `transcriptions/` is committed to git; `files/` is gitignored.
- Args: `transcript.py <filename> [--model tiny|base|small|medium|large] [--language <code>]`.
  Defaults: `--model large`, `--language es`.
- Output format is one line per segment: `[start - end]: text`.

## Steps

1. **Ensure deps are installed.** Check the venv exists and has whisper:
   ```bash
   .venv/bin/python3 -c "import whisper" 2>/dev/null && echo OK || echo MISSING
   ```
   If `MISSING` (or `.venv` absent), tell the user to install first (this pulls
   in multi-GB PyTorch, so do NOT run it silently — let them run the commands):
   ```bash
   python3 -m venv .venv
   .venv/bin/pip install -r requirements.txt
   ```

2. **Place the audio file.** The script only reads from `files/source/`.
   - If the user's file is already in `files/source/`, use its filename as-is.
   - Otherwise copy it in: `cp "<their/path/audio.mp3>" files/source/`
   - `mkdir -p files/source` first if the directory doesn't exist.

3. **Pick model and language.**
   - Model: default `large` (best quality). Use `small` when the user wants speed
     or is testing, or when they mention limited memory. Honor any explicit request.
   - Language: default `es`. Set `--language en` (etc.) when the audio isn't Spanish
     or the user specifies. Common codes: `es`, `en`, `fr`, `de`, `pt`, `it`, `zh`, `ja`.

4. **Run the transcription** through the venv python (no activation needed):
   ```bash
   .venv/bin/python3 transcript.py <filename> --model <model> --language <code>
   ```
   First run of a given model downloads it (large is ~3GB) — this can be slow.
   Long recordings can take 10–30+ min on `large`; warn the user for long files.

5. **Read back the result** from `transcriptions/<name>.txt` and summarize or show
   it as the user asked (full text, summary, specific timestamps, etc.).

## Notes

- Prefer running the script directly with `.venv/bin/python3` over `make`, since the
  makefile assumes an activated venv and only exposes `large`/`small` presets.
- If transcription quality is poor: confirm the correct `--language`, try `large`,
  or note that noisy audio degrades results.
- If it errors with "File not found", the audio isn't in `files/source/` — recheck step 2.
