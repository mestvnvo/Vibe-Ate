from sqlalchemy.dialects.postgresql import insert as pg_insert
from app.db.database import SessionLocal
from app.db.models import Song as SongModel, VectorEmbedding
from app.contracts.schema import SongWithEmbedding, InsertResult

async def get_songs_from_image(image):
    # TODO: implement embedding extraction and similarity search
    return ["fake_song_1", "fake_song_2"]

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