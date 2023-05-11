from repository.rating_dto import RatingDTO
from repository.rating_repository import RatingRepository
from repository.movie_respository import MovieRepository

class RatingService():
    
    def __init__(self):
        self.__movie_repository = MovieRepository()
        self.__rating_repository = RatingRepository()

    def getByMovie(self, id):
        votes = []
        movie = self.__movie_repository.find(id)
        
        if movie is None:
            raise IndexError("movie not found")
        
        for rating in movie.rating:
            votes.append(rating.vote)

        return votes 
    
    def vote_rating(self, id, rating):
        movie = self.__movie_repository.find(id)
        if movie is None:
            raise IndexError("movie not found")
        
        dto = RatingDTO()
        dto.movie_id = movie.id
        dto.vote = rating
        
        self.__rating_repository.add(dto)