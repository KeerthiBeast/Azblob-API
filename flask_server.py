import os, sys
from dotenv import load_dotenv
import subprocess
from flask import Flask, request, jsonify
import threading

load_dotenv()
app = Flask(__name__)
app.config['SECRET_KEY'] = 'Azblob_api'

#Starts subprocess for download playlists and songs
def run_subprocess_playlist():
    command = ['python3 playlist.py'] 
    print("Subprocess commences")
    subprocess.check_call(command, shell=True, stdout=sys.stdout, stderr=subprocess.STDOUT)

def run_subprocess_song():
    command = ['python3 song.py'] 
    print("Subprocess commences")
    subprocess.check_call(command, shell=True, stdout=sys.stdout, stderr=subprocess.STDOUT)

#To check the status of the api
@app.route('/api')
def response():
    return jsonify({"message": "Working"})

#To download playlist
@app.route('/playlist', methods=['POST'])
def download_upload():
    data = request.get_json() #parse the json and get the data
    if not data.get('playlist_url'):
        return ("Pass the playlist_url"), 400
    playlist_url = data.get('playlist_url')
    os.environ['PLAYLIST'] = playlist_url #the playlist value in the .env is changed with the new value
    
    thread = threading.Thread(target=run_subprocess_playlist)
    thread.start()

    return jsonify({"message": "Downloading Playlist"})

@app.route('/song', methods=['POST'])
def download_upload_song():
    data = request.get_json() #parse the json and get the data
    if not data.get('song_url'):
        return ("Pass the song_url"), 400
    song_url = data.get('song_url')
    os.environ['SONG'] = song_url #the song value in the .env is changed with the new value
    
    thread = threading.Thread(target=run_subprocess_song)
    thread.start()

    return jsonify({"message": "Downloading Song"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=6942)
