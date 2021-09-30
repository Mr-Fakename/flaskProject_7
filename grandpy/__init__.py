from flask import Flask


"""Create and configure an instance of the Flask application."""
app = Flask(__name__, instance_relative_config=True)
app.config.from_mapping(
    # a default secret that should be overridden by instance config
    SECRET_KEY="dev",
)

from .views import *
