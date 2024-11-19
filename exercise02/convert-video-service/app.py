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
        'outtmpl': '~/Downloads/%(title)s.%(ext)s'  # Save the file in /app/downloads
        # 'outtmpl': '/app/downloads/%(title)s.%(ext)s'  # Save the file in /app/downloads

    }
    with YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(video_url)
        audio_file = ydl.prepare_filename(info_dict).replace('.webm', '.mp3').replace('.mp4', '.mp3')

    return jsonify({
        'message': 'Video converted to mp3',
        'file_path': audio_file
    })

if __name__ == '__main__':
    app.run(port=5002)
