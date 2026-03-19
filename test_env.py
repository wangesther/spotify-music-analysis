from dotenv import load_dotenv
import os

load_dotenv()

client_id = os.getenv('SPOTIPY_CLIENT_ID')
client_secret = os.getenv('SPOTIPY_CLIENT_SECRET')

print("Client ID:", client_id)
print("Client Secret:", client_secret)

if client_id and client_secret:
    print("\nCredentials loaded successfully!")
else:
    print("\nCredentials NOT loaded - check your .env file")