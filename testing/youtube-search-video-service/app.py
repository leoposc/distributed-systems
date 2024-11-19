# create a flask app that can search for youtube videos
# and return the best video based on the search query 
# as link to the video

from flask import Flask, request
from dotenv import load_dotenv
import requests
import os 

load_dotenv()
app = Flask(__name__)
API_KEY = os.getenv('API_KEY')

@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('keyword')
    api = f'https://www.googleapis.com/youtube/v3/search?part=snippet&maxResults=1&q={query}&type=video&key={API_KEY}'

    # fetch response from the api
    response = requests.get(api)
    # get the first video from the response
    data = response.json()
    video = data['items'][0]
    video_id = video['id']['videoId']
    video_link = f'https://www.youtube.com/watch?v={video_id}'

    print("video link", video_link)
    # send a request to the convert-video-service running on port 5002
    # to convert the video to mp3
    convert_api = 'http://localhost:5002/convert'
    data = {
        'url': video_link
    }
    # jsonify the data
    response = requests.post(convert_api, json=data)
    print(response.json())
    return response.json()


if __name__ == '__main__':
    app.run(port=5000)

