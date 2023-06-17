
from werkzeug.exceptions import HTTPException
from flask import Flask, jsonify
from flask_restx import Api
from endpoints.rating_endpoint import ns as ns_rating
from endpoints.movies_endpoint import ns as ns_movie

app = Flask(__name__)
api = Api(
    app=app,
    doc='/_docs',
    version='1.0.0',
    title='IMDb APP API',
    description='TEST APP API'
)

api.add_namespace(ns_rating)
api.add_namespace(ns_movie)

@app.errorhandler(HTTPException)
def handle_exception(e):
    return jsonify(error=str(e)), e.code

if __name__ == '__main__':
    app.run(debug=True)