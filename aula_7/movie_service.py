import os
from movie import Movie

class MovieService():
    
    _movies_db = None
    STORAGE_FOLDER_PATH = 'C:\\workspace\\ifsp\\lab-dev\\aula_6\\tmp\\uploads'

    def __init__(self):
        self._movies_db = []
   
    def delete_movie(self, id):
        movie = self.find_movie(id)
        self._movies_db.remove(movie)
        
    def find_movie(self, id):
        for m in self._movies_db:
            if id == m.id:
                return m
        raise IndexError("Movie not found")

    def get_file(self, name):
        for root, _, files in os.walk(self.STORAGE_FOLDER_PATH):
            for filename in files:
                if name in filename:
                    return os.path.join(root, filename)
        raise FileNotFoundError('File Not Found')

    def get_movies(self):
        return self._movies_db
    
    def update_movie(self, id, movie:Movie):        
        movie_old = self.find_movie(id)
        movie_old.fromModel(movie)
    
    def save_file(self, movie:Movie, file):        
        filename = str(id) + '.' + file.filename.split('.')[1]
        file.save(os.path.join(self.STORAGE_FOLDER_PATH, filename))

    def save_movie(self, movie:Movie):
         self._movies_db.append(movie)
    
    def vote_rating(self, id, rating):
        movie = self.find_movie(id)
        movie.rating.append(rating)
    