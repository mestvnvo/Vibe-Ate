from pydantic import BaseModel
from typing import List

class Song(BaseModel):
    spotify_id: str
    track_name: str
    track_artist: str
    deezer_id: int

class SongWithEmbedding(Song):
    embedding: List[float]

class InsertResult(BaseModel):
    inserted: int
    skipped: int
    status: str
    message: str