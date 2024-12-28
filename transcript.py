import whisper
from pydub import AudioSegment
import argparse
import os

# Set up argument parsing
parser = argparse.ArgumentParser(description="Transcribe an audio file using Whisper.")
parser.add_argument("filename", type=str, help="The audio file name with extension (e.g., 'audio.mp3', 'recording.aac')")
args = parser.parse_args()

# Extract filename without extension for output files
filename_without_ext = os.path.splitext(args.filename)[0]

# Paths for source and output
input_path = os.path.join("./files/source", args.filename)
output_wav_path = os.path.join("./files/wav", f"{filename_without_ext}.wav")
output_txt_path = os.path.join("./transcriptions", f"{filename_without_ext}.txt")

# Convert audio to wav using pydub
audio = AudioSegment.from_file(input_path)
audio.export(output_wav_path, format="wav")

# Load the Whisper model
model = whisper.load_model("large")

# Transcribe the audio file with Whisper
result = model.transcribe(output_wav_path)

# Extract segments and differentiate speakers
segments = result['segments']

# Write the transcription to a file
os.makedirs(os.path.dirname(output_txt_path), exist_ok=True)
with open(output_txt_path, "w") as file:
    for segment in segments:
        start = segment['start']
        end = segment['end']
        text = segment['text']
        file.write(f"[{start:.2f} - {end:.2f}]: {text}\n")

print(f"Transcription completed and saved in {output_txt_path}")