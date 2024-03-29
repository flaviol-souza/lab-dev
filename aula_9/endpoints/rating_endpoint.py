from flask import abort, jsonify
from services.rating_service import RatingService

__rating_service = RatingService()

def ratingByMovie(movie_id):
    if movie_id < 1:
        abort(403, "Invalid identifer")

    return __rating_service.get_all_by_movie(movie_id)

def voteMovie(id, rating):
    if id < 1:
        abort(403, "Invalid identifer")
    
    if rating < 0 or rating > 10:
        abort(403, "Invalid rating!")
    
    try:
        __rating_service.vote_rating(id, rating)
    except IndexError as e:
        abort(404, e)    

    return jsonify(success="Filme votado com sucesso!")