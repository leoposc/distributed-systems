from flask import Flask, render_template, send_file, abort
import os

app = Flask(__name__)
music_folder = os.path.join(os.getcwd(), 'music')  # Ensure this points to the correct directory

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

if __name__ == '__main__':
    app.run(port=5000, host='0.0.0.0', debug=True)
