import os
from flask import Flask, request, abort, jsonify, send_file
from movie import Movie

STORAGE_PATH = 'C:\\workspace\\ifsp\\lab-dev\\aula_6\\tmp\\uploads'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

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

def _allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def _find_file(name):
    for root, dirs, files in os.walk(STORAGE_PATH):
        #files = [filename for filename in os.listdir(STORAGE_PATH) if x.endswith('.py')]
        for filename in files:
            if name in filename:
                return os.path.join(root, filename)
    raise FileNotFoundError('File Not Found')

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

@app.route('/movies/<int:id>/cover', methods=['GET'])
def downloadCover(id):
    if id < 1:
        abort(403, "Invalid identifer")

    try:
        _findMovie(_movies_db, id)
        filename = _find_file(str(id))
        return send_file(filename, mimetype='image/jpeg')
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

    _movies_db.append(movie)

    return jsonify(success="Movie added Successfully!")

@app.route('/movies/<int:id>/cover', methods=['POST'])
def uploadFile(id):
    if id < 1:
        abort(403, "Invalid identifer")
    
    if 'file' not in request.files:
        abort(400, '')
        
    cover = request.files['file']    
    if cover.filename == '' or (not _allowed_file(cover.filename)):
        abort(400, 'invalid file, extension files are allowed {ALLOWED_EXTENSIONS}')

    blob = cover.read()
    if len(blob) == 0 or len(blob) / (1024 * 1024) > 16:
        abort(413, 'invalid file size (Max. 16mb)')

    try:
        movie = _findMovie(_movies_db, id)
        current_file = _find_file(str(id))
        if current_file :
            abort(409, f'Movie {movie.title} has a cover.')
    except IndexError as e:
        abort(404, e)
    except FileNotFoundError:
        pass

    filename = str(id) + '.' + cover.filename.split('.')[-1]
    file = open(os.path.join(STORAGE_PATH, filename), 'wb')
    file.write(blob)
    file.close()
    
    return jsonify(success="Movie cover added Successfully!")

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

@app.errorhandler(409)
def _conflict(e):
    return jsonify(error=str(e)), 409

@app.errorhandler(413)
def _payload_too_large(e):
    return jsonify(error=str(e)), 413

if __name__ == '__main__':
    app.run(debug=True)
    app.config['STORAGE_PATH'] = STORAGE_PATH