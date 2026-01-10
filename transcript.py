import whisper
import argparse
import os

# Set up argument parsing
parser = argparse.ArgumentParser(description="Transcribe an audio file using Whisper.")
parser.add_argument("filename", type=str, help="The audio file name with extension (e.g., 'audio.mp3', 'recording.aac')")
parser.add_argument("--model", type=str, default="large",
                    choices=["tiny", "base", "small", "medium", "large"],
                    help="Whisper model size (default: large)")
parser.add_argument("--language", type=str, default="es",
                    help="Language code for transcription (default: es)")
args = parser.parse_args()

# Extract filename without extension for output files
filename_without_ext = os.path.splitext(args.filename)[0]

# Paths for source and output
input_path = os.path.join("./files/source", args.filename)
output_txt_path = os.path.join("./transcriptions", f"{filename_without_ext}.txt")

# Validate input file exists
if not os.path.exists(input_path):
    print(f"Error: File not found: {input_path}")
    exit(1)

# Load the Whisper model
print(f"Loading Whisper model '{args.model}'...")
model = whisper.load_model(args.model)

# Transcribe the audio file with Whisper (reads audio directly, no WAV conversion needed)
print(f"Transcribing {args.filename}...")
result = model.transcribe(
    input_path,
    language=args.language,
    condition_on_previous_text=False,  # Reduces hallucinations and repetitions
)

# Write the transcription to a file
os.makedirs(os.path.dirname(output_txt_path), exist_ok=True)
with open(output_txt_path, "w") as file:
    for segment in result['segments']:
        start = segment['start']
        end = segment['end']
        text = segment['text']
        file.write(f"[{start:.2f} - {end:.2f}]: {text}\n")

print(f"✓ Transcription saved to {output_txt_path}")