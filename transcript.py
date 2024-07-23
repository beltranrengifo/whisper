import whisper
from pydub import AudioSegment

# Convert mp3 to wav using pydub
audio = AudioSegment.from_file("./files/source/cordoba.mp3")
audio.export("./files/wav/cordoba.wav", format="wav")

# Load the Whisper model
model = whisper.load_model("large")

# Transcribe the audio file with Whisper
result = model.transcribe("./files/wav/cordoba.wav")

# Extract segments and differentiate speakers
segments = result['segments']

# Write the transcription to a file
with open("./transcriptions/cordoba.txt", "w") as file:
    for segment in segments:
        start = segment['start']
        end = segment['end']
        text = segment['text']
        file.write(f"[{start:.2f} - {end:.2f}]: {text}\n")

print("Transcripción completada y guardada en cordoba.txt")