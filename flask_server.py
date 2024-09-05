import os, sys
from dotenv import load_dotenv
import subprocess
from flask import Flask, request, jsonify, render_template
import threading

load_dotenv()
app = Flask(__name__)
app.config['SECRET_KEY'] = 'this is life'

def get_mp3_files():
    all_files = os.listdir('.')
    mp3_files = [file for file in all_files if file.endswith('.mp3')]
    return mp3_files

def run_subprocess_playlist():
    command = ['python3 playlist.py'] 
    print("Subprocess commences")
    subprocess.check_call(command, shell=True, stdout=sys.stdout, stderr=subprocess.STDOUT)

def run_subprocess_song():
    command = ['python3 song.py'] 
    print("Subprocess commences")
    subprocess.check_call(command, shell=True, stdout=sys.stdout, stderr=subprocess.STDOUT)

@app.route('/api')
def response():
    return jsonify({"message": "Working"})

@app.route('/web')
def index():
    return render_template('index.html')

@app.route('/playlist', methods=['POST'])
def download_upload():
    data = request.get_json()
    if not data.get('playlist_url'):
        return ("Pass the playlist_url"), 400
    playlist_url = data.get('playlist_url')
    os.environ['PLAYLIST'] = playlist_url
    
    thread = threading.Thread(target=run_subprocess_playlist)
    thread.start()

    return jsonify({"message": "Downloading Playlist"})

@app.route('/song', methods=['POST'])
def download_upload_song():
    data = request.get_json()
    if not data.get('song_url'):
        return ("Pass the song_url"), 400
    song_url = data.get('song_url')
    os.environ['SONG'] = song_url
    
    thread = threading.Thread(target=run_subprocess_song)
    thread.start()

    return jsonify({"message": "Downloading Song"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=6942)
