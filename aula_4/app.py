from flask import Flask, request
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
    return None

@app.route('/movies', methods=['GET'])
def getMovies():
    return _toJsonFromMovies(_movies_db)

@app.route('/movies/save', methods=['POST'])
def addMovie():
    body = request.get_json()
    movie = Movie()
    movie.fromJson(body)
    _movies_db.append(movie)

    return "Filme adicionado com Sucesso!"

@app.route('/movies/<int:id>', methods=['PUT'])
def updateMovie(id):
    movie = _findMovie(_movies_db, id)
    body = request.get_json()
    movie.fromJson(body)
    
    return "Filme atualiado com sucesso!"

if __name__ == '__main__':
    app.run(debug=True)

