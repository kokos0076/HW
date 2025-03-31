from sem_2_lab_1 import *
import pickle
import shelve
import json


playlist = Playlist()
playlist.add_track("Любов", "Скрябін", 2005, "3:14", "Поп ")
playlist.add_track("Бета-каротин", "Boombox", 2005, "4:05", "Рок ")
playlist.add_track("Останній день", "MamaRika", 2023, "2:29", "Поп ")

print("\nСЕРІАЛІЗАЦІЯ")

# Pickle Серіалізація
with open("playlist.pkl", "wb") as f:
    pickle.dump(playlist, f)

# Pickle Десеріалізаціяn
with open("playlist.pkl", "rb") as f:
    loaded_playlist = pickle.load(f)
print("\nPickle:")
print(loaded_playlist)

# Shelve Серіалізація 
with shelve.open("playlist.slv") as db:
    db["collection"] = playlist

# Shelve Десеріалізація
with shelve.open("playlist.slv") as db:
    shelve_playlist = db["collection"]
print("\nShelve:")
print(shelve_playlist)

# Repr Серіалізація 
text_repr = repr(playlist.tracks)
with open("playlist.txt", "w", encoding="utf-8") as f:
    f.write(text_repr)

# Eval Десеріалізація
with open("playlist.txt", "r", encoding="utf-8") as f:
    eval_tracks = eval(f.read())
print("\nRepr:")
for track, genre in eval_tracks:
    print(f"{track} - {genre}")

# JSON Серіалізація
def to_json(obj):
    if isinstance(obj, Track):
        return {
            "name": obj.a,
            "author": obj.b,
            "year": obj.c,
            "duration": obj.d
        }
    elif isinstance(obj, Playlist):
        return [{"track": to_json(t), "genre": g} for t, g in obj.tracks]
    return obj

with open("playlist.json", "w", encoding="utf-8") as f:
    json.dump(to_json(playlist), f, ensure_ascii=False, indent=4)

# JSON Десеріалізація
def from_json(data):
    pl = Playlist()
    for item in data:
        t = item["track"]
        pl.add_track(t["name"], t["author"], t["year"], t["duration"], item["genre"])
    return pl

with open("playlist.json", "r", encoding="utf-8") as f:
    json_playlist = from_json(json.load(f))
print("\nJSON:")
print(json_playlist)
