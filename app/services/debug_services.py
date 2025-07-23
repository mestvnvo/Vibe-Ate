from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc, func

from app.db.models import Song, VectorEmbedding

async def get_latest_song(session: AsyncSession):
    stmt = select(Song).order_by(desc(Song.spotify_id)).limit(1)
    result = await session.execute(stmt)
    song = result.scalar_one_or_none()

    if not song:
        return None, None

    vec_stmt = select(VectorEmbedding).where(VectorEmbedding.spotify_id == song.spotify_id)
    vec_result = await session.execute(vec_stmt)
    vector = vec_result.scalar_one_or_none()

    return song, vector

async def get_table_count(session):
    song_count = await session.scalar(select(func.count()).select_from(Song))
    vector_count = await session.scalar(select(func.count()).select_from(VectorEmbedding))
    return {
        "songs": song_count,
        "vectors": vector_count
    }