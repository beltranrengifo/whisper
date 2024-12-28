import whisper
from pydub import AudioSegment
import argparse
import os

# Set up argument parsing
parser = argparse.ArgumentParser(description="Transcribe an audio file using Whisper.")
parser.add_argument("filename", type=str, help="The name of the audio file (without extension) located in './files/source/'")
args = parser.parse_args()

# Paths for source and output
input_path = f"./files/source/{args.filename}.mp3"
output_wav_path = f"./files/wav/{args.filename}.wav"
output_txt_path = f"./transcriptions/{args.filename}.txt"

# Convert mp3 to wav using pydub
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