from repository.abstract_repository import AbstractRepository
from repository.movie_dto import MovieDTO

class MovieRepository(AbstractRepository):

    def __init__(self):
        super().__init__(MovieDTO)

    def update(self, id, movie:MovieDTO):
        movie_current = self.find(id)

        movie_current.title = movie.title
        movie_current.summary = movie.summary
        movie_current.runtime = movie.runtime
        movie_current.year = movie.year
        movie_current.gender = movie.gender

        self._session.commit()
