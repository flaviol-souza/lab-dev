from flask import Flask, request, abort, jsonify
from movie import Movie

app = Flask(__name__)
_movies_db = []

def _toJsonFromMovies(movies):
    jsonMovies = []
    for m in movies:
        jsonMovies.append(m.toJson())
    return jsonMovies

def _findMovie(movies, id):
    for m in movies:
        if id == m.id:
            return m
    raise IndexError("Movie not found")

@app.route('/movies/<int:id>', methods=['GET'])
def getMovie(id):
    if id < 1:
        abort(403, "Invalid identifer")
    
    try:
        movie = _findMovie(_movies_db, id)
    except IndexError as e:
        abort(404, e)

    return movie.toJson()

@app.route('/movies', methods=['GET'])
def getMovies():
    return _toJsonFromMovies(_movies_db)

@app.route('/movies/save', methods=['POST'])
def addMovie():
    body = request.get_json()
    try:
        movie = Movie()
        movie.fromJson(body)
    except ValueError as e:
        abort(400, e)

    _movies_db.append(movie)

    return jsonify(success="Movie added Successfully!")

@app.route('/movies/<int:id>', methods=['PUT'])
def updateMovie(id):
    if id < 1:
        abort(403, "Invalid identifer")
    
    body = request.get_json()
    try:
        movie = _findMovie(_movies_db, id)
        movie.fromJson(body)
    except ValueError as e:
        abort(400, e)
    except IndexError as e:
        abort(404, e)
        
    return jsonify(success="Movie successfully updated!")

@app.route('/movies/<int:id>/rating/<float:rating>', methods=['PATCH'])
def voteMovie(id, rating):
    if id < 1:
        abort(403, "Invalid identifer")
    
    if rating < 0 or rating > 10:
        abort(403, "Invalid rating!")
    
    try:
        movie = _findMovie(_movies_db, id)
    except IndexError as e:
        abort(404, e)    

    movie.rating.append(rating)

    return jsonify(success="Successfully voted movie!")

@app.route('/movies/<int:id>', methods=['DELETE'])
def deleteMovie(id):
    if id < 1:
        abort(403, "Invalid identifer")
    
    try:
        movie = _findMovie(_movies_db, id)
    except IndexError as e:
        abort(404, e)

    _movies_db.remove(movie)

    return jsonify(success="Filme removido com sucesso!")

@app.errorhandler(400)
def _bad_request(e):
    return jsonify(error=str(e)), 400

@app.errorhandler(403)
def _forbidden(e):
    return jsonify(error=str(e)), 403

@app.errorhandler(404)
def _not_found(e):
    return jsonify(error=str(e)), 404

if __name__ == '__main__':
    app.run(debug=True)