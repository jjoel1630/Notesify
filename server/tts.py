import os
from google.cloud import texttospeech
from pydub import AudioSegment

# Instantiates a client for Google Text-to-Speech
client = texttospeech.TextToSpeechClient()

# Function to split the content into smaller chunks, respecting the 5000 byte limit
def chunk_text(content, limit=5000):
    chunks = []
    while content:
        chunk = content[:limit]
        if len(chunk.encode('utf-8')) > limit:
            # Make sure we split by words to avoid cutting a word in half
            limit_pos = chunk.rfind(' ')
            chunk = content[:limit_pos]
        chunks.append(chunk)
        content = content[len(chunk):]
    return chunks

# Read the file and split content into chunks
with open("messages/message.txt", "r") as file:
    content = file.read()

text_chunks = chunk_text(content)

# Function to synthesize speech from text
def synthesize_speech(text, idx):
    synthesis_input = texttospeech.SynthesisInput(text=text)
    voice = texttospeech.VoiceSelectionParams(
        language_code="en-US", name="en-US-Journey-F", ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL
    )
    audio_config = texttospeech.AudioConfig(
        # Use LINEAR16 (WAV format)
        audio_encoding=texttospeech.AudioEncoding.LINEAR16
    )
    
    response = client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )
    
    # Save each chunk as a WAV file (since LINEAR16 corresponds to WAV)
    wav_filename = f"outputs/output_chunk_{idx}.wav"
    with open(wav_filename, "wb") as out:
        out.write(response.audio_content)
        print(f'Audio content written to file "{wav_filename}"')

# Create the "outputs" directory if it doesn't exist
os.makedirs("outputs", exist_ok=True)

# Synthesize speech for each chunk
for idx, chunk in enumerate(text_chunks):
    synthesize_speech(chunk, idx)

# Convert WAV files to MP3 and combine them using pydub
combined = AudioSegment.empty()

for idx in range(len(text_chunks)):  # Use the length of text_chunks to ensure all chunks are processed
    wav_filename = f"outputs/output_chunk_{idx}.wav"
    # Convert WAV to MP3 using pydub
    audio_segment = AudioSegment.from_wav(wav_filename)
    mp3_filename = f"outputs/output_chunk_{idx}.mp3"
    audio_segment.export(mp3_filename, format="mp3")  # Save as MP3 file
    combined += AudioSegment.from_mp3(mp3_filename)

# Export the combined audio as a single MP3 file
combined.export("outputs/combined_output.mp3", format="mp3")
print('Combined audio content written to "outputs/combined_output.mp3"')
