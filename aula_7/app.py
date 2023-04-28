from flask import Flask, request, abort, jsonify, send_file
from movie import Movie
from movie_service import MovieService

ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)
movieService = MovieService()

def _allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def _toJsonFromMovies(movies):
    jsonMovies = []
    for m in movies:
        jsonMovies.append(m.toJson())
    return jsonMovies

@app.route('/movies', methods=['GET'])
def getMovies():
    return _toJsonFromMovies(movieService.get_movies())

@app.route('/movies/<int:id>', methods=['GET'])
def getMovie(id):
    if id < 1:
        abort(403, "Invalid identifer")
    
    try:
        movie = movieService.find_movie(id)
    except IndexError as e:
        abort(404, e)

    return movie.toJson()

@app.route('/movies/<int:id>/cover', methods=['GET'])
def getMovieCover(id):
    if id < 1:
        abort(403, "Invalid identifer")

    try:
        movieService.find_movie(id)
        file = movieService.get_file(str(id))
        return send_file(file, as_attachment=True)
    except IndexError or FileNotFoundError as e:
        abort(404, e)
    
@app.route('/movies', methods=['POST'])
def addMovie():
    body = request.get_json()
    try:
        movie = Movie()
        movie.fromJson(body)
    except ValueError as e:
        abort(400, e)

    movieService.save_movie(movie)
    return jsonify(success="Movie added Successfully!")

@app.route('/movies/<int:id>/cover', methods=['POST'])
def uploadFile(id):
    if id < 1:
        abort(403, "Invalid identifer")
    
    if 'file' not in request.files:
        abort(400, 'The cover is required')
        
    file = request.files['file']    
    if file.filename.strip() == '' or (not file and not _allowed_file(file.filename)):
        abort(400, f'invalid file, extension files are allowed {ALLOWED_EXTENSIONS}')

    blob = file.read()
    if len(blob) == 0 or len(blob) / (1024 * 1024) > 16:
        abort(413, 'invalid file size (Max. 16mb)')

    try:
        movie = movieService.find_movie(id)
        current_file = movieService.get_file(str(id))
        if current_file :
            abort(409, f'Movie {movie.title} has a cover.')
    except IndexError as e:
        abort(404, e)
    except FileNotFoundError:
        pass

    movieService.save_file(movie, file)        
    return jsonify(success="Movie cover added Successfully!")

@app.route('/movies/<int:id>', methods=['PUT'])
def updateMovie(id):
    if id < 1:
        abort(403, "Invalid identifer")
    
    body = request.get_json()
    try:
        movie = Movie()
        movie.fromJson(body)
        movieService.update_movie(id, movie)
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
        movieService.vote_rating(id)
    except IndexError as e:
        abort(404, e)    

    return jsonify(success="Successfully voted movie!")

@app.route('/movies/<int:id>', methods=['DELETE'])
def deleteMovie(id):
    if id < 1:
        abort(403, "Invalid identifer")
    
    try:
         movieService.delete_movie(id)
    except IndexError as e:
        abort(404, e)

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