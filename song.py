#Download songs

"""Works almost the same as playlist.py but does not see if the file is already present in 
the blob storage. If the file exists an exception will be thrown and the process end."""

import os
from azure.identity import ClientSecretCredential
from azure.storage.blob import BlobServiceClient
from spotdl import Spotdl
from dotenv import load_dotenv

load_dotenv() #Load .env

#Get mp3 files in the local folder
def get_mp3_files():
    all_files = os.listdir('.')
    mp3_files = [file for file in all_files if file.endswith('.mp3')]
    return mp3_files

#Initialize the spotdl library
spotdl = Spotdl(
    client_id=os.getenv('SP_CLIENT_ID'),
    client_secret=os.getenv('SP_CLIENT_SECRET')
)

#Main function
def download_upload():
    print("Downloading songs")
    accountUrl = os.getenv('AZURE_CONTAINER')
    #Initialize Azure storage library
    Account = ClientSecretCredential(
        tenant_id = os.getenv('AZURE_TENANT_ID'),
        client_id = os.getenv('AZURE_CLIENT_ID'),
        client_secret = os.getenv('AZURE_CLIENT_SECRET')
    )

    blobServiceClient = BlobServiceClient(accountUrl, credential=Account)
    containerName = "songs"
    songs = spotdl.search([os.getenv('SONG')])

    spotdl.download(songs[0])
    mp3files = get_mp3_files()
    
    for name in mp3files: 
        with open('log.txt', mode='w', encoding='utf-8') as file:
            blobClient = blobServiceClient.get_blob_client(
                container = containerName,
                blob = name
            )
            try:
                file.write(f"Uploading {name}\n")
                print(f"Now uploading {name}")
                with open(file=name, mode='rb') as data:
                    blobClient.upload_blob(data)
                os.remove(name)
            except Exception as e:
                file.write(f"Error in uploading {name}\n")
                print(f"Error in uploading {name}")

        file.close()

    print("Complete")

download_upload()

mp3_files = get_mp3_files()
for files in mp3_files:
    os.remove(files)
