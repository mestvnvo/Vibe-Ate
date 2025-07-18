from sqlalchemy.dialects.postgresql import insert as pg_insert
from app.db.database import SessionLocal
from app.db.models import Song as SongModel, VectorEmbedding
from app.contracts.schema import SongWithEmbedding, InsertResult

from fastapi import UploadFile
from app.services.utils import call_gradio_client_api
from app.db.database import SessionLocal
from sqlalchemy import text

async def get_songs_from_image(image: UploadFile):
    image_bytes = await image.read()

    # kosmos captions image
    caption = call_gradio_client_api(
        space_name="mestvnvo/Kosmos2-API",
        input_data=image_bytes,
        input_type="image"
    )

    # SmolLM2 turns caption to 'vibe'
    vibe_string = call_gradio_client_api(
        space_name="mestvnvo/SmolLM2-API",
        input_data=caption,
        input_type="text"
    )

    # MiniLM embeds 'vibe'
    embedding = call_gradio_client_api(
        space_name="mestvnvo/SentenceTransformer-API",
        input_data=vibe_string,
        input_type="text"
    )

    # pgvector similarity searches w/ embedding
    async with SessionLocal() as session:
        query = text('''
            SELECT s.spotify_id, s.track_name, s.track_artist, s.deezer_id
            FROM vectors v
            JOIN songs s ON s.spotify_id = v.spotify_id
            ORDER BY v.embedding <#> :embedding
            LIMIT 8
        ''')
        result = await session.execute(query, {"embedding": embedding})
        rows = result.fetchall()

    return [
        {
            "spotify_id": row.spotify_id,
            "track_name": row.track_name,
            "track_artist": row.track_artist,
            "deezer_id": row.deezer_id
        }
        for row in rows
    ]

async def insert_songs(songs):
    if not songs:
        return InsertResult(inserted=0, skipped=0, status="success", detail="No songs submitted.")

    song_values = []
    vector_values = []

    for s in songs:
        song_values.append({
            "spotify_id": s.spotify_id,
            "track_name": s.track_name,
            "track_artist": s.track_artist,
            "deezer_id": s.deezer_id
        })
        vector_values.append({
            "spotify_id": s.spotify_id,
            "embedding": s.embedding
        })

    async with SessionLocal() as session:
        async with session.begin():
            try:
                song_stmt = pg_insert(SongModel).values(song_values).on_conflict_do_nothing(index_elements=["spotify_id"])
                song_result = await session.execute(song_stmt)

                vector_stmt = pg_insert(VectorEmbedding).values(vector_values).on_conflict_do_nothing(index_elements=["spotify_id"])
                vector_result = await session.execute(vector_stmt)

                await session.commit()

                inserted = song_result.rowcount or 0
                skipped = len(songs) - inserted
                status = "success" if skipped == 0 else "partial"

                return InsertResult(
                    inserted=inserted,
                    skipped=skipped,
                    status=status,
                    message=None
                )

            except Exception as e:
                await session.rollback()
                return InsertResult(
                    inserted=0,
                    skipped=0,
                    status="error",
                    message=str(e)
                )