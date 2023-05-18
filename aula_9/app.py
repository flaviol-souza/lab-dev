from flask import Flask, jsonify
import endpoints.movies_endpoint as movies_endpoint
import endpoints.rating_endpoint as rating_endpoint

app = Flask(__name__)

app.add_url_rule('/movies/<int:id>', methods=['GET'], view_func=movies_endpoint.getMovie)
app.add_url_rule('/movies', methods=['GET'], view_func=movies_endpoint.getMovies)
app.add_url_rule('/movies/<int:id>/cover', methods=['GET'], view_func=movies_endpoint.downloadCover)
app.add_url_rule('/movies/<int:id>/cover', methods=['POST'], view_func=movies_endpoint.uploadCover)
app.add_url_rule('/movies/save', methods=['POST'], view_func=movies_endpoint.addMovie)
app.add_url_rule('/movies/<int:id>', methods=['PUT'], view_func=movies_endpoint.updateMovie)
app.add_url_rule('/movies/<int:id>', methods=['DELETE'], view_func=movies_endpoint.deleteMovie)

app.add_url_rule('/movies/<int:movie_id>/rating', methods=['GET'], view_func=rating_endpoint.ratingByMovie)
app.add_url_rule('/movies/<int:id>/rating/<float:rating>', methods=['PATCH'], view_func=rating_endpoint.voteMovie)


@app.errorhandler(400)
def _bad_request(e):
    return jsonify(error=str(e)), 400

@app.errorhandler(403)
def _forbidden(e):
    return jsonify(error=str(e)), 403

@app.errorhandler(404)
def _not_found(e):
    return jsonify(error=str(e)), 404

@app.errorhandler(409)
def _conflict(e):
    return jsonify(error=str(e)), 409

@app.errorhandler(413)
def _payload_too_large(e):
    return jsonify(error=str(e)), 413

if __name__ == '__main__':
    app.run(debug=True)