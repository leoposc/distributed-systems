from flask import Flask, render_template, send_file, abort, send_from_directory, jsonify
import os, requests

app = Flask(__name__)
music_folder = os.path.join(os.getcwd(), 'music')  # Ensure this points to the correct directory
download_service_url = 'http://127.0.0.1:5002'

@app.route('/', methods=['GET'])
def home():
    audio_files = [f for f in os.listdir(music_folder) if f.endswith('.mp3')]
    return render_template('index.html', audio_files=audio_files)

@app.route('/play/<filename>', methods=['GET'])
def play(filename):
    print(filename)
    try:
        return send_file(os.path.join(music_folder, filename), mimetype='audio/mpeg')
    except FileNotFoundError:
        abort(404)  # Return a 404 if the file is not found

@app.route('/sync', methods=['GET'])
def sync():
    # Get list of MP3 files from the server
    response = requests.get(f"{download_service_url}/all_music")
    mp3_files = response.json().get('files', [])

    # Download each MP3 file and save it in the 'music' folder
    for filename in mp3_files:
        file_url = f"{download_service_url}/music/{filename}"
        file_response = requests.get(file_url)

        if file_response.status_code == 200:
            with open(os.path.join(music_folder, filename), 'wb') as file:
                file.write(file_response.content)
            print(f"Downloaded: {filename}")
        else:
            print(f"Failed to download: {filename}")

    return {'message': 'sync finished' }

if __name__ == '__main__':
    app.run(port=5000, host='0.0.0.0', debug=True)
