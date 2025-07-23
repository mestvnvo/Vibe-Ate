from pydantic import BaseModel
from typing import List, Optional

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
    message: Optional[str] = None