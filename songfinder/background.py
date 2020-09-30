from songfinder import db
from songfinder.spotify_client import get_genre
from songfinder.models import Aid

def load_genres_task(artist, aidid):
    print(f"Loading the genre from spotify api of Aid {aidid}")
    genre = get_genre(artist)
    aid = Aid.query.get_or_404(id=aidid)
    aid.genre = genre
    db.session.commit()

def load_all_aids_genre():
    for aid in Aid.query.all():
        if not aid.genre:
            load_genres_task(aid.artist, aid.id)