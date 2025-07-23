from fastapi import APIRouter, UploadFile, File, Depends
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession

from app.services.vibe_services import get_songs_from_image, insert_songs
from app.services.debug_services import get_latest_song, get_table_count
from app.contracts.schema import SongWithEmbedding, InsertResult
from app.db.database import get_db

router = APIRouter()

@router.get("/vibe")
async def get_songs(image: UploadFile = File(...)):
    return await get_songs_from_image(image)

@router.post("/songs", response_model=InsertResult)
async def add_songs(songs: List[SongWithEmbedding]):
    return await insert_songs(songs)

@router.get("/debug/latest")
async def debug_db_latest_song(session: AsyncSession = Depends(get_db)):
    song, vector_row = await get_latest_song(session)

    if not song:
        return {"message": "No songs in database."}

    return {
        "song": {
            "spotify_id": song.spotify_id,
            "track_name": song.track_name,
            "track_artist": song.track_artist,
            "deezer_id": song.deezer_id
        },
        "embedding_preview": [float(x) for x in vector_row.embedding[:5]] if vector_row else None
    }

@router.get("/debug/count")
async def debug_db_count(session: AsyncSession = Depends(get_db)):
    counts = await get_table_count(session)
    return {"table_counts": counts}