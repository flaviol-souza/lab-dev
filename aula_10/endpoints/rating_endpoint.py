from flask import abort, jsonify
from flask_restx import Resource, Namespace, fields
from services.rating_service import RatingService

ns = Namespace('movies', description='The IMDb ns is an interface that enables developers to access and utilize the extensive movie and TV show database provided by IMDb (Internet Movie Database). With the IMDb ns, developers can retrieve detailed information about films, television series, actors, and other related content. This includes data such as titles, release dates, genres, ratings, cast and crew details, plot summaries, images, and more. By integrating the IMDb ns into their applications, developers can enhance their services with comprehensive movie and TV show information, enabling features like search functionality, personalized recommendations, and rich media experiences. The IMDb ns empowers developers to create engaging entertainment-related applications that leverage the wealth of data available in the IMDb database, providing users with valuable insights and an enhanced viewing experience.')

rating_model = ns.model('Rating', {
    'id': fields.Integer(required=True, description='User ID'),
    'movie_id': fields.Integer(required=True, description='User name'),
    'vote': fields.Float(required=True, description='User name')
})

@ns.route('<int:movie_id>/rating')
class RatingEndpoint(Resource):

    __rating_service = RatingService()

    @ns.doc(description='Get ratings of movie by ID')
    @ns.response(200, 'Success')
    @ns.response(403, 'Invalid identifier')
    def get(self, movie_id):
        if movie_id < 1:
            abort(403, "Invalid identifer")

        return self.__rating_service.get_all_by_movie(movie_id)

@ns.route('<int:movie_id>/rating/<float:rating>')
class RatingEndpoint(Resource):

    __rating_service = RatingService()

    @ns.doc(description='Save a vote in movie')
    @ns.response(200, 'Success')
    @ns.response(400, 'Invalid values attributes')
    @ns.response(403, 'Invalid identifier')
    @ns.response(404, 'Movie not found')
    def patch(self, movie_id, rating):
        if movie_id < 1:
            abort(403, "Invalid identifer")
        
        if rating < 0 or rating > 10:
            abort(400, "Invalid rating!")
        
        try:
            self.__rating_service.vote_rating(movie_id, rating)
        except IndexError as e:
            abort(404, e)    

        return jsonify(success="Movie voted successfully!")