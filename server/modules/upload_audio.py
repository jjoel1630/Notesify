from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import os
from dotenv import load_dotenv
from bson import ObjectId
from io import BytesIO

load_dotenv()

def init_mongodb():
    user_pwd = os.getenv('MONGODB_USER_PWD')

    uri = f"mongodb+srv://jjoel1630:{user_pwd}@audiofiles.njqyy.mongodb.net/?retryWrites=true&w=majority&appName=audiofiles"

    client = MongoClient(uri, server_api=ServerApi('1'))
    try:
        client.admin.command('ping')
        print("Pinged your deployment. You successfully connected to MongoDB!")
        return client
    except Exception as e:
        print(e)
        return "Failed to connect to mongodb"

def audio_to_binary(audio_segment, format="mp3"):
    # Create an in-memory bytes buffer
    audio_io = BytesIO()
    # Export the AudioSegment to the buffer in the specified format (e.g., "mp3" or "wav")
    audio_segment.export(audio_io, format=format)
    # Reset the buffer position to the start
    audio_io.seek(0)
    # Return the binary data
    return audio_io.read()

def upload_audio(audio_content, file_name, collection):
    # if not os.path.exists(file_path):
    #     print("File not found!")
    #     return

    # with open(file_path, 'rb') as audio_file:
    #     audio_data = audio_file.read()

    audio_bytes = audio_to_binary(audio_content)

    document = {
        'filename': os.path.basename(file_name),
        'audio': audio_bytes
    }

    result = collection.insert_one(document)
    print(f"File uploaded successfully with ID: {result.inserted_id}")

    return result.inserted_id
    
def download_audio(file_id, output_path, collection):
	document = collection.find_one({'_id': file_id})

	if document is None:
		print("File not found in the database.")
		return

	audio_data = document.get('audio')

	if audio_data is None:
		print("No audio data found in the document.")
		return

	with open(output_path, 'wb') as audio_file:
		audio_file.write(audio_data)

	print(f"File downloaded successfully to {output_path}")
      

# upload_audio("outputs/test_audio.mp3")

# client = init_mongodb()
# db = client['audio']
# collection = db['files']

# file_id = ObjectId("66f84f23f2500e99053a5da3")
# download_audio(file_id, 'outputs/downloaded_audio.mp3', collection)