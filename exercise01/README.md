# distributed-systems
 
We implemented a little music application that allows to listen to youtube
while beeing offline. That is possible because music is downloaded beforehand. 
The application is structured into 4 microservises which can be used via http and gets described below. 

## download service

This service allows to download videos and playlists from youtube which are converted to 192 kb/s mp3, afterwards. An url needs to provided.
Furthermore, it allows to fetch all mp3 files that have been downloaded before. 

## music player
The music player can be used to play music. It communicates with the download service to synchronize the music library.

## youtube playlist search service
This service can be used to find playlists matching a search query. The respective url obtained by that is further used to download a playlist.

## youtube video search service
This service can be used to find videos matching a search query. The respective url obtained by that is further used to download a videa.


## Tech stack
We used Python and docker compose to create the application.


## Contributions
This application was built by Hendrik Paul Munske, Leopold Schmid and Friedrich Hartmann.
