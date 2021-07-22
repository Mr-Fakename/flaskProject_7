from flask import Flask, render_template, request, redirect, jsonify, make_response
from .parser import parse

from grandpy import app


app.config.from_object('grandpy.config')


@app.route('/')
def index():
    return render_template("index.html")


@app.route("/search", methods=["POST"])
def search():
    return jsonify(parse(request.get_json()))
