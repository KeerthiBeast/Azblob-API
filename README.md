# Azblob-API
A Flask endpoint for [Azblob](github.com/keerthibeast/Azblob)

Uses Spotdl library to download Songs and Playlists and upload them to an Azure Blob.

Usage: <br />
    * Rename .env_example to .env and add the require information
    * /api and /web is used to check the status of the applicatoin
    * /playlist is used to download playlists. A POST request with json body value playlist_url is expected 
    * /song is used to download songs. A POST request with json body value song_url is expected

How it works: <br />
You launch the application and send the required data to the endpoint. When the request is a success a  subprocess is started for the corresponding function. The subprocess will start in a different thread and the response will be send without waiting for the songs to download.