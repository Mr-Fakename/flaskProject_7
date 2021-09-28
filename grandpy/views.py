from flask import render_template, request, jsonify

from grandpy import app
from .API_classes import GoogleMaps, Wiki
from .parser import parse

app.config.from_object('grandpy.config')


@app.route('/')
def index():
    return render_template("index.html")


@app.route("/search", methods=["POST"])
def search():
    cleaned_query = " ".join(parse(request.get_json()))
    maps_client = GoogleMaps()
    locations, coordinates = maps_client.geocode(cleaned_query)
    wiki_hits = []
    for location in locations:
        wiki_search = Wiki(location, coordinates)
        wiki_request = wiki_search.wiki_query()
        wiki_hits.append(wiki_request['query']['pages'][next(iter(wiki_request['query']['pages']))])
    return jsonify(wiki_hits, coordinates)
