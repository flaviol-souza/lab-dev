from repository.base import Base
from sqlalchemy import Column, ForeignKey, Float, Integer, Sequence

class RatingDTO(Base):
    __tablename__ = "rating_movie"

    id = Column(Integer, Sequence('seq_rating_movie_pk'), primary_key=True,
                autoincrement=True)
    movie_id = Column(Integer, ForeignKey("movie.id"), nullable=False)
    vote = Column(Float, nullable=False)