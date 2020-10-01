from songfinder import db
from songfinder.spotify_client import get_genre
from songfinder.models import Aid

import time

def load_genres_task(artist, aidid):
    print(f"Loading the genre from spotify api of Aid {aidid}")
    time.sleep(2)
    genre = get_genre(artist)
    aid = Aid.query.filter_by(id=aidid).first()
    aid.genre = genre
    db.session.commit()
    print("Done")

def load_all_aids_genre():
    for aid in Aid.query.all():
        if not aid.genre:
            load_genres_task(aid.artist, aid.id)