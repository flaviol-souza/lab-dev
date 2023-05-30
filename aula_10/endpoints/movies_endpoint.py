import communs
from endpoints.movie_vo import MovieVO
from endpoints.rating_endpoint import rating_model
from services.movie_service import MovieService
from flask_restx import Resource, Namespace, fields
from flask import request, abort, jsonify, send_file

ns = Namespace('movies', description='The IMDb ns is an interface that enables developers to access and utilize the extensive movie and TV show database provided by IMDb (Internet Movie Database). With the IMDb ns, developers can retrieve detailed information about films, television series, actors, and other related content. This includes data such as titles, release dates, genres, ratings, cast and crew details, plot summaries, images, and more. By integrating the IMDb ns into their applications, developers can enhance their services with comprehensive movie and TV show information, enabling features like search functionality, personalized recommendations, and rich media experiences. The IMDb ns empowers developers to create engaging entertainment-related applications that leverage the wealth of data available in the IMDb database, providing users with valuable insights and an enhanced viewing experience.')

movie_model = ns.model('Movie', {
    'id': fields.Integer(required=True, description='Movie ID'),
    'title': fields.String(required=True, description='Movie title'),
    'summary': fields.String(required=True, description='Movie summary'),
    'runtime': fields.Integer(required=True, description='Movie runtime'),
    'year': fields.Integer(required=True, description='Movie Year'),
    'gender': fields.String(required=True, description='Gender of Movie'),
    'rating': fields.List(fields.Nested(rating_model), required=False)
})

@ns.route('')
class MoviesEndpoint(Resource):

    _movie_service = MovieService()

    @ns.doc(description='Get all movies')
    @ns.response(200, 'Success', movie_model)
    def get(self):
        return communs._toJsonFromMovies(self._movie_service.get_all_movies())
    
    @ns.response(200, 'Success', movie_model)
    @ns.response(400, 'Invalid values attributes')
    def post(self):
        body = request.get_json()
        try:
            movie = MovieVO()
            movie.fromJson(body)
        except ValueError as e:
            abort(400, str(e))

        self._movie_service.save_movie(movie)
        return jsonify(success="Movie Added Successfully!")

@ns.route('/<int:id>')
class MovieEndpoint(Resource):

    _movie_service = MovieService()

    @ns.doc(description='Get a movie by ID')
    @ns.response(200, 'Success', movie_model)
    @ns.response(403, 'Invalid identifier')
    @ns.response(404, 'Movie not found')
    def get(self, id):
        if id < 1:
            abort(403, "Invalid identifier")
        
        try:
            movie = self._movie_service.find_movie(id)
        except IndexError as e:
            abort(404, str(e))

        return movie.toJson()

    @ns.doc(description='Update a movie by ID')
    @ns.response(200, 'Success')
    @ns.response(400, 'Invalid values attributes')
    @ns.response(403, 'Invalid identifier')
    @ns.response(404, 'Movie not found')
    def put(self, id):
        if id < 1:
            abort(403, "Invalid identifer")
        
        body = request.get_json()
        try:
            movie = MovieVO()
            movie.fromJson(body)
            movie = self._movie_service.update_movie(id, movie)        
        except ValueError as e:
            abort(400, str(e))
        except IndexError as e:
            abort(404, str(e))
            
        return jsonify(success="Movie successfully updated!")

    @ns.doc(description='Delete a movie by ID')
    @ns.response(200, 'Success')
    @ns.response(404, 'Movie not found')
    def delete(self, id):
        if id < 1:
            abort(403, "Invalid identifer")
        
        try:
            self._movie_service.delete_movie(id)
        except IndexError as e:
            abort(404, str(e))

        return jsonify(success="Movie removed successfully!")

@ns.route('/<int:id>/cover')
class MovieCoverEndpoint(Resource):
    _movie_service = MovieService()

    @ns.doc(description='Get a cover of movie by ID')
    @ns.response(200, 'Success')
    @ns.response(403, 'Invalid identifier')
    @ns.response(404, 'Movie not found')
    def get(self, id):
        if id < 1:
            abort(403, "Invalid idenfier")
        try:
            self._movie_service.find_movie(id)
            filename = self._movie_service.find_file(str(id))
            return send_file(filename, mimetype='image/jpeg')
        except IndexError or FileNotFoundError as e:
            abort(404, str(e))

    @ns.doc(description='Save a cover of movie by ID')
    @ns.response(200, 'Success')
    @ns.response(400, 'Invalid values attributes')
    @ns.response(403, 'Invalid identifier')
    @ns.response(404, 'Movie not found')
    @ns.response(409, 'Movie has a cover')
    @ns.response(413, 'Invalid file size')
    def post(self, id):
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
            movie = self._movie_service.find_movie(id)
            current_file = self._movie_service.find_file(str(id))
            if current_file:
                abort(409, f'Movie {movie.title} has a cover.')
        except IndexError as e:
            abort(404, str(e))
        except FileNotFoundError:
            pass

        self._movie_service.save_file(file)
        return jsonify(success="Movie cover has been successfully added!")