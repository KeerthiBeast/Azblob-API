import os
from azure.identity import ClientSecretCredential
from azure.storage.blob import BlobServiceClient
from spotdl import Spotdl
from spotdl.utils.formatter import create_file_name
from dotenv import load_dotenv

load_dotenv()

def get_mp3_files():
    all_files = os.listdir('.')
    mp3_files = [file for file in all_files if file.endswith('.mp3')]
    return mp3_files

"""def get_name_only(mp3_files):
    names = [line.split('-',1)[1].lstrip() for line in mp3_files if '-' in line]
    return names"""

spotdl = Spotdl(
    client_id=os.getenv('SP_CLIENT_ID'),
    client_secret=os.getenv('SP_CLIENT_SECRET')
)

def download_upload():
    print("Downloading songs")
    accountUrl = os.getenv('AZURE_CONTAINER')
    Account = ClientSecretCredential(
        tenant_id = os.getenv('AZURE_TENANT_ID'),
        client_id = os.getenv('AZURE_CLIENT_ID'),
        client_secret = os.getenv('AZURE_CLIENT_SECRET')
    )

    blobServiceClient = BlobServiceClient(accountUrl, credential=Account)
    containerName = "songs"
    songsBlob = blobServiceClient.get_container_client(container=containerName)
    songs = spotdl.search([os.getenv('PLAYLIST')])
    blobList = songsBlob.list_blobs()
    blobl = []
    songsl = []

    for blob in blobList:
        blobl.append(blob.name)

    for song in songs:
        currSong = create_file_name(song, "", "mp3")
        if blobl and currSong.name not in blobl:
            songsl.append(song)
        elif not blobl:
            songsl.append(song) 

    if songsl:
        spotdl.download_songs(songsl)
    mp3files = get_mp3_files()

    with open('log.txt', mode='w', encoding='utf-8') as file:
        for name in mp3files:
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
