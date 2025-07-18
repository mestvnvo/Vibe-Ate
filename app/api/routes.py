from fastapi import APIRouter, UploadFile, File
from app.services.vibe_service import get_songs_from_image, insert_songs
from app.contracts.schema import SongWithEmbedding
from typing import List

router = APIRouter()

@router.get("/vibe")
async def get_songs(image: UploadFile = File(...)):
    return await get_songs_from_image(image)

@router.post("/songs")
async def add_songs(songs: List[SongWithEmbedding]):
    return await insert_songs(songs)