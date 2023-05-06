from repository.abstract_repository import AbstractRepository
from repository.rating_dto import RatingDTO

class RatingRepository(AbstractRepository):

    def __init__(self):
        super().__init__(RatingDTO)