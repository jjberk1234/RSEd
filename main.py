import json

import spotipy
from spotipy import SpotifyClientCredentials
from flask import Flask, render_template, request, redirect, url_for

# Spotify setup.
SECRETS = json.load(open("secrets.json"))
client_credentials_manager = SpotifyClientCredentials(
                                client_id = SECRETS["id"],
                                client_secret = SECRETS["key"]
                            )
sp = spotipy.Spotify(client_credentials_manager = client_credentials_manager)

# Flask setup.
app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "GET":
        return render_template("index.html")
    elif request.method == "POST":
        playlist_url = request.form.get("playlist-url")
        playlist_uri = playlist_url.split("/")[-1].split("?")[0]

        return redirect(url_for("module", uri=playlist_uri))

@app.route("/module/<uri>")
def module(uri):
    tracks = sp.playlist_tracks(uri)["items"]
    return render_template("index.html", tracks=tracks)
