ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

def _toJsonFromMovies(movies):
    jsonMovies = []
    for m in movies:
        jsonMovies.append(m.toJson())
    return jsonMovies

def _allowed_file(filename):
    return '.' in filename and \
        filename.split('.')[-1].lower() in ALLOWED_EXTENSIONS
