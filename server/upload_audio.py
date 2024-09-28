from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import os
from dotenv import load_dotenv
from bson import ObjectId

load_dotenv()

user_pwd = os.getenv('MONGODB_USER_PWD')

uri = f"mongodb+srv://jjoel1630:{user_pwd}@audiofiles.njqyy.mongodb.net/?retryWrites=true&w=majority&appName=audiofiles"

# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))
# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)
    

db = client['audio']
collection = db['files']

def upload_audio(file_path):
    # Check if the file exists
    if not os.path.exists(file_path):
        print("File not found!")
        return

    # Read the audio file as binary
    with open(file_path, 'rb') as audio_file:
        audio_data = audio_file.read()

    # Create a document to store in MongoDB
    document = {
        'filename': os.path.basename(file_path),
        'audio': audio_data  # Store audio data as binary
    }

    # Insert the document into the collection
    result = collection.insert_one(document)
    print(f"File uploaded successfully with ID: {result.inserted_id}")
    
def download_audio(file_id, output_path):
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
      
file_id = ObjectId("66f7a64557cf9f7d1441162a")  # Convert string ID to ObjectId
download_audio(file_id, 'outputs/downloaded_audio.mp3')

# upload_audio("outputs/test_audio.mp3")