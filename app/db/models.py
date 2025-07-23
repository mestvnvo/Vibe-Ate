from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.dialects.postgresql import TEXT
from pgvector.sqlalchemy import Vector

Base = declarative_base()

class Song(Base):
    __tablename__ = 'songs'
    spotify_id = Column(String(22), primary_key=True)
    track_name = Column(TEXT)
    track_artist = Column(TEXT)
    deezer_id = Column(Integer)

class VectorEmbedding(Base):
    __tablename__ = 'vectors'
    spotify_id = Column(TEXT, ForeignKey('songs.spotify_id'), primary_key=True)
    embedding = Column(Vector(384))