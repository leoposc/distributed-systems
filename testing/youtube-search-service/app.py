from flask import Flask, request
from youtubesearchpython import PlaylistsSearch

app = Flask(__name__)

@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('query')

    playlist_search = PlaylistsSearch(query, limit = 10)

    result = playlist_search.result()

    return result 


if __name__ == '__main__':
    app.run(port=5000)

