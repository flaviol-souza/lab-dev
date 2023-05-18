from sqlalchemy.orm import relationship
from repository.base import Base
from sqlalchemy import Column, Integer, Sequence, String

class MovieDTO(Base):
    __tablename__ = 'movie'

    id = Column(Integer, Sequence('seq_movie_pk'), primary_key=True,
                 autoincrement=True)
    title = Column(String, nullable=False)
    summary = Column(String, nullable=False)
    #ACTORS TAREFA....
    gender = Column(String, nullable=False)
    runtime = Column(Integer)
    year = Column(Integer)
    rating = relationship("RatingDTO")#, lazy=True)