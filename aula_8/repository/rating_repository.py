from repository.abstract_repository import AbstractRepository
from repository.rating_dto import RatingDTO

class RatingRepository(AbstractRepository):

    def __init__(self):
        super().__init__(RatingDTO)

    def find_all_by_movie(self, movie_id):
        return self._session.query(RatingDTO).where(RatingDTO.movie_id == movie_id)