from yt_dlp import YoutubeDL
from flask import Flask, request, jsonify
import os

app = Flask(__name__)

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
        'outtmpl': './downloads/%(title)s.%(ext)s',
    }
    with YoutubeDL(ydl_opts) as ydl:
        ydl.download(video_url)

    return jsonify({
        'message': 'download finished'
    })

if __name__ == '__main__':
    app.run(port=5002)
