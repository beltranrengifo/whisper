.PHONY: transcribe transcribe-fast

# Full transcription with large model (best quality, slower)
transcribe:
	python3 transcript.py $(file) --model large --language es

# Quick transcription with small model (faster, good for testing)
transcribe-fast:
	python3 transcript.py $(file) --model small --language es