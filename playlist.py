#Downloads Playlists

import os
from azure.identity import ClientSecretCredential
from azure.storage.blob import BlobServiceClient
from spotdl import Spotdl
from spotdl.utils.formatter import create_file_name
from dotenv import load_dotenv

load_dotenv() #loads the .env file

#Get files with .mp3 extension
def get_mp3_files():
    all_files = os.listdir('.')
    mp3_files = [file for file in all_files if file.endswith('.mp3')]
    return mp3_files

#Initializes spotdl library with client_id and client_secret
spotdl = Spotdl(
    client_id=os.getenv('SP_CLIENT_ID'),
    client_secret=os.getenv('SP_CLIENT_SECRET')
)

"""Searches songs in the playlist url and get the list of songs already present in the
Blob storage. Compares them and remove existing songs from the download list and downloads
songs. The songs are then uploaded to the Blob and deleted from the local folder"""

def download_upload():
    print("Downloading songs")
    accountUrl = os.getenv('AZURE_CONTAINER')
    #Initializes Azure storage library
    Account = ClientSecretCredential(
        tenant_id = os.getenv('AZURE_TENANT_ID'),
        client_id = os.getenv('AZURE_CLIENT_ID'),
        client_secret = os.getenv('AZURE_CLIENT_SECRET')
    )

    blobServiceClient = BlobServiceClient(accountUrl, credential=Account)
    containerName = "songs" #Name of the container. Change to your container name
    songsBlob = blobServiceClient.get_container_client(container=containerName)
    songs = spotdl.search([os.getenv('PLAYLIST')]) #Search for songs in the playlist. Returns a list
    blobList = songsBlob.list_blobs() #Songs present in the container
    blobl = [] #List to save the names of the blobs
    songsl = [] #List to save the songs to download

    for blob in blobList:
        blobl.append(blob.name)

    for song in songs:
        """create_file_name function present in the spotdl function is used to find the name
        which will be given to a song when downloaded by the spotdl library. This is then used to
        compare with the name of the songs present in the container"""
        
        currSong = create_file_name(song, "", "mp3") 
        if blobl and currSong.name not in blobl:
            songsl.append(song)
        elif not blobl:
            songsl.append(song) 

    if songsl:
        spotdl.download_songs(songsl) #files are downloaded using the spotdl library
    mp3files = get_mp3_files() #Files present in the local folder are compiled in a list to be uploaded

    #A log.txt is create just to see which files are uploaded
    with open('log.txt', mode='w', encoding='utf-8') as file:
        for name in mp3files:
            #Create a blob with the name of the file to be uploaded
            blobClient = blobServiceClient.get_blob_client(
                container = containerName,
                blob = name
            )
            try:
                file.write(f"Uploading {name}\n")
                print(f"Now uploading {name}")
                with open(file=name, mode='rb') as data:
                    blobClient.upload_blob(data) #upload the file
                os.remove(name)
            except Exception as e:
                file.write(f"Error in uploading {name}\n")
                print(f"Error in uploading {name}")

    file.close()
    print("Complete")

download_upload()

#Cleanup if any mp3 file is present after the upload
mp3_files = get_mp3_files()
for files in mp3_files:
    os.remove(files)
