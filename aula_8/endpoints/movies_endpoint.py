import communs
from endpoints.movie_vo import MovieVO
from flask import request, abort, jsonify, send_file
from services.movie_service import MovieService

_movie_service = MovieService()

def getMovie(id):
    if id < 1:
        abort(403, "Invalid identifer")
    
    try:
        movie = _movie_service.find_movie(id)
    except IndexError as e:
        abort(404, e)

    return movie.toJson()

def getMovies():
    return communs._toJsonFromMovies(_movie_service.get_all_movies())

def downloadCover(id):
    if id < 1:
        abort(403, "Invalid idenfier")
    try:
        _movie_service.find_movie(id)
        filename = _movie_service.find_file(str(id))
        return send_file(filename, mimetype='image/jpeg')
    except IndexError or FileNotFoundError as e:
        abort(404, e)

def uploadCover(id):
    if id < 1:
        abort(403, "Invalid idenfier")
    
    if 'file' not in request.files:
        abort(400, "The cover is required")

    file = request.files['file']
    if file.filename.strip() == '' or not communs._allowed_file(file.filename):
        abort(400, f'invalid file, extension files are allowed {communs.ALLOWED_EXTENSIONS}')
    
    blob = file.read()
    if len(blob) == 0 or len(blob) / (1024 * 1024) > 16:
        abort(413, 'invalid file size (Max. 16mb)')

    try:
        movie = _movie_service.find_movie(id)
        current_file = _movie_service.find_file(str(id))
        if current_file:
            abort(409, f'Movie {movie.title} has a cover.')
    except IndexError as e:
        abort(404, e)
    except FileNotFoundError:
        pass

    _movie_service.save_file(file)
    return jsonify(success="Capa do filme foi adicionada com Sucesso!")

def addMovie():
    body = request.get_json()
    try:
        movie = MovieVO()
        movie.fromJson(body)
    except ValueError as e:
        abort(400, e)

    _movie_service.save_movie(movie)
    return jsonify(success="Filme adicionado com Sucesso!")

def updateMovie(id):
    if id < 1:
        abort(403, "Invalid identifer")
    
    body = request.get_json()
    try:
        movie = MovieVO()
        movie.fromJson(body)
        movie = _movie_service.update_movie(id, movie)        
    except ValueError as e:
        abort(400, e)
    except IndexError as e:
        abort(404, e)
        
    return jsonify(success="Filme atualiado com sucesso!")

def deleteMovie(id):
    if id < 1:
        abort(403, "Invalid identifer")
    
    try:
        _movie_service.delete_movie(id)
    except IndexError as e:
        abort(404, e)

    return jsonify(success="Filme removido com sucesso!")
