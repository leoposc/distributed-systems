from yt_dlp import YoutubeDL
from flask import Flask, request, jsonify, send_from_directory
import os

app = Flask(__name__)
MUSIC_FOLDER = MUSIC_FOLDER = os.path.join(app.root_path, 'downloads')

@app.route('/convert', methods=['POST'])
def convert():
    data = request.json
    video_url = data['url']

    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'outtmpl': '{MUSIC_FOLDER}/%(title)s.%(ext)s',
    }
    with YoutubeDL(ydl_opts) as ydl:
        ydl.download(video_url)

    return jsonify({
        'message': 'download finished'
    })

@app.route('/music/<filename>', methods=['GET'])
def music(filename):
    return send_from_directory(MUSIC_FOLDER, filename)

@app.route('/all_music', methods=['GET'])
def all_music():
    files = os.listdir(MUSIC_FOLDER)
    mp3_files = [f for f in files if f.endswith('.mp3')]
    return {'files': mp3_files}


if __name__ == '__main__':
    app.run(port=5002)
