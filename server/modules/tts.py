from google.cloud import texttospeech
from pydub import AudioSegment
import io

client = texttospeech.TextToSpeechClient()

def chunk_text(content, limit=5000):
    chunks = []
    while content:
        chunk = content[:limit]
        if len(chunk.encode('utf-8')) > limit:
            limit_pos = chunk.rfind(' ')
            chunk = content[:limit_pos]
        chunks.append(chunk)
        content = content[len(chunk):]
    return chunks

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
    
    # wav_filename = f"outputs/output_chunk_{idx}.wav"
    # with open(wav_filename, "wb") as out:
    #     out.write(response.audio_content)
    #     print(f'Audio content written to file "{wav_filename}"')
    # print("Successfully synthesized speech")
    return response.audio_content

# def combine_audio(audios):
#     combined = AudioSegment.empty()
#     for idx in range(len(audios)): 
#         wav_filename = f"outputs/output_chunk_{idx}.wav"
#         # Convert WAV to MP3 using pydub
#         audio_segment = AudioSegment.from_wav(audios[idx])
#         # mp3_filename = f"outputs/output_chunk_{idx}.mp3"
#         # audio_segment.export(mp3_filename, format="mp3")
#         combined += AudioSegment.from_mp3(audio_segment)
#     # combined.export("outputs/combined_output.mp3", format="mp3")
#     print('Successfully combined audio')
#     return combined

# Function to combine audios
def combine_audios(audio_list, output_file):
    combined = AudioSegment.empty()

    # Loop through each audio content (in bytes)
    for audio_content in audio_list:
        audio_segment = AudioSegment.from_file(io.BytesIO(audio_content), format="wav")
        combined += audio_segment
    
    combined.export(output_file, format="mp3")
    # print(f"Combined audio saved to {output_file}")
    return combined

# Temporary instead of using script
# with open("messages/message.txt", "r") as file:
#     content = file.read()
# text_chunks = chunk_text(content)

# audios = []
# for idx, chunk in enumerate(text_chunks):
#     audio_content = synthesize_speech(chunk, idx)
#     audios.append(audio_content)

# combined = combine_audios(audios, "combined_audio.mp3")