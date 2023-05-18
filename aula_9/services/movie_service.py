from endpoints.movie_vo import MovieVO
from repository.movie_dto import MovieDTO
from repository.movie_respository import MovieRepository
import os

class MovieService():
    STORAGE_PATH = 'C:\\Users\\svcj238521\\workspace\\lab-dev\\aula_3\\tmp\\cover'

    __movie_repository = MovieRepository()
    _movies_db = []

    def delete_movie(self, id):
        movie = self.__movie_repository.find(id)
        if movie is None:
            raise IndexError("Movie not found") 
        self.__movie_repository.delete(movie)

    def get_all_movies(self):
        vos = []
        dtos = self.__movie_repository.find_all()
        for dto in dtos:
            vos.append(MovieVO.fromDto(dto))
        
        return vos
    
    def find_movie(self, id):
        dto:MovieDTO = self.__movie_repository.find(id)
        if dto is None:
            raise IndexError("Movie not found")
        
        return MovieVO.fromDto(dto)

    def find_file(self, name):
        for path, _, files in os.walk(self.STORAGE_PATH): 
            for filename in files:
                if name in filename:
                    return os.path.join(path, filename)
        raise FileNotFoundError('File not found')
    
    def save_file(self, file):
        blob = file.read()
        filename = str(id) + '.' + file.filename.split('.')[-1]
        file_image = open(os.path.join(self.STORAGE_PATH, filename), 'wb')
        file_image.write(blob)
        file_image.close()

    def save_movie(self, movie:MovieVO):
        self.__movie_repository.add(movie.toDto())

    def update_movie(self, id, movie:MovieVO):
        self.__movie_repository.update(id, movie.toDto())