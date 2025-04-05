import pickle
import shelve
import json


class Song:
    def __init__(self, name="Останній день", author="MamaRika", year=2023):

        assert isinstance(name, str) and name.strip(), "Назва має бути непустим рядком"
        assert isinstance(author, str) and author.strip(), "Автор має бути непустим рядком"
        assert isinstance(year, int) and year > 0, "Рік має бути додатнім цілим числом"
        self.a = name
        self.b = author
        self.c = year

    def __str__(self):
        return f'{self.b}. "{self.a}" ({self.c})'

    def __eq__(self, other):
        if self.c == other.c:
            return f'Пісні "{self.a}" і "{other.a}" вийшли в один рік: {self.c}'
        else:
            return ""

    def length(self):
        return f'Кількість слів у назві пісні "{self.a}": {len(self.a.split())}'

    def __repr__(self):
        return f'Song("{self.a}", "{self.b}", {self.c})'


class Track(Song):
    def __init__(self, name="Останній день", author="MamaRika", year=2023, duration="2:29"):
        Song.__init__(self,name,author,year)
        self.d=duration
        
        assert isinstance(duration, str) and duration.count(":") == 1, "Тривалість має бути у форматі хв:сс"
        try:
            minutes, seconds = map(int, duration.split(":"))
        except ValueError:
            raise ValueError("Недопустимий формат тривалості.")
        self.d = duration

    def __str__(self):
        return f'{self.b}. "{self.a}" ({self.c}) {self.d}'

    def secconds(self):
        try:
            minutes, seconds = map(int, self.d.split(":"))
        except ValueError as e:
            raise ValueError(f"Помилка обчислення тривалості для пісні {self.a}: {e}")
        return f'Тривалість пісні "{self.a}" у секундах: {minutes * 60 + seconds}'

    def __add__(self, sec):
        try:
            sec = int(sec)
        except ValueError:
            raise ValueError("Додані секунди мають бути цілим числом")
        total_sec = int(self.d.split(":")[0]) * 60 + int(self.d.split(":")[1]) + sec
        new_min = total_sec // 60
        new_sec = total_sec % 60
        new_duration = f"{new_min}:{new_sec:02d}"
        return Track(self.a, self.b, self.c, new_duration)

    def __repr__(self):
        return f'Track("{self.a}", "{self.b}", {self.c}, "{self.d}")'


class Playlist:
    def __init__(self):
        self.tracks = []

    def add_track(self, name, author, year, duration, genre):
        try:
            year = int(year)
        except ValueError:
            raise ValueError("Рік має бути числом")
        try:
            track = Track(name, author, year, duration)
        except Exception as e:
            raise Exception(f"Помилка створення треку '{name}': {e}")
        self.tracks.append((track, genre))

    def load_from_file(self, filename):
        try:
            with open(filename, 'r', encoding='utf-8') as file:
                for line in file:
                    parts = line.strip().split(',')
                    if len(parts) != 5:
                        print("Невірний формат рядка:", line.strip())
                        continue
                    name, author, year, duration, genre = parts
                    try:
                        year = int(year)
                    except ValueError:
                        print("Невірний рік для пісні:", name)
                        continue
                    try:
                        self.add_track(name, author, year, duration, genre)
                    except Exception as e:
                        print(f"Помилка додавання треку {name}: {e}")
        except FileNotFoundError:
            raise FileNotFoundError(f"Файл {filename} не знайдено!")
        except Exception as e:
            raise Exception(f"Помилка при завантаженні з файлу: {e}")

    def total_duration_by_genre(self):
        genre_durations = {}
        for track, genre in self.tracks:
            try:
                minutes, seconds = map(int, track.d.split(":"))
            except ValueError:
                print("Помилка розрахунку тривалості для треку", track.a)
                continue
            total_seconds = minutes * 60 + seconds
            genre = genre.strip()
            genre_durations[genre] = genre_durations.get(genre, 0) + total_seconds
        result = ""
        for genre, duration in genre_durations.items():
            result += f"{genre}: {duration // 60}:{duration % 60:02d}, "
        return result.rstrip(", ")

    def __str__(self):
        result = "\n".join(f"{track} - {genre.strip()}" for track, genre in self.tracks)
        return f"Плейлист з {len(self.tracks)} треків:\n{result}"

    def __repr__(self):
        return f"Playlist({self.tracks})"


class SerializationError(Exception):
    def __init__(self, msg):
        Exception.__init__(msg)


def pickle_serialize(obj, filename):
    assert isinstance(filename, str) and filename.endswith(".pkl"), "Ім'я файлу має бути рядком і закінчуватися на .pkl"
    try:
        with open(filename, "wb") as f:
            pickle.dump(obj, f)
    except Exception as e:
        raise SerializationError(f"Помилка при Pickle серіалізації: {e}")
    else:
        print("Pickle серіалізація пройшла успішно.")
    finally:
        print("Завершено операцію Pickle серіалізації.")


def pickle_deserialize(filename):
    assert isinstance(filename, str) and filename.endswith(".pkl"), "Ім'я файлу має бути рядком і закінчуватися на .pkl"
    try:
        with open(filename, "rb") as f:
            obj = pickle.load(f)
    except Exception as e:
        raise SerializationError(f"Помилка при Pickle десеріалізації: {e}")
    else:
        print("Pickle десеріалізація пройшла успішно.")
        return obj
    finally:
        print("Завершено операцію Pickle десеріалізації.")


def shelve_serialize(obj, filename):
    assert isinstance(filename, str) and filename.strip(), "Ім'я файлу не може бути пустим"
    try:
        with shelve.open(filename) as db:
            db["collection"] = obj
    except Exception as e:
        raise SerializationError(f"Помилка при Shelve серіалізації: {e}")
    else:
        print("Shelve серіалізація пройшла успішно.")
    finally:
        print("Завершено операцію Shelve серіалізації.")


def shelve_deserialize(filename):
    try:
        with shelve.open(filename) as db:
            obj = db["collection"]
    except Exception as e:
        raise SerializationError(f"Помилка при Shelve десеріалізації: {e}")
    else:
        print("Shelve десеріалізація пройшла успішно.")
        return obj
    finally:
        print("Завершено операцію Shelve десеріалізації.")


def json_serialize(obj, filename, to_json_func):
    assert callable(to_json_func), "to_json_func має бути функцією"
    try:
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(to_json_func(obj), f, ensure_ascii=False, indent=4)
    except Exception as e:
        raise SerializationError(f"Помилка при JSON серіалізації: {e}")
    else:
        print("JSON серіалізація пройшла успішно.")
    finally:
        print("Завершено операцію JSON серіалізації.")


def json_deserialize(filename, from_json_func):
    assert callable(from_json_func), "from_json_func має бути функцією"
    try:
        with open(filename, "r", encoding="utf-8") as f:
            data = json.load(f)
            obj = from_json_func(data)
    except Exception as e:
        raise SerializationError(f"Помилка при JSON десеріалізації: {e}")
    else:
        print("JSON десеріалізація пройшла успішно.")
        return obj
    finally:
        print("Завершено операцію JSON десеріалізації.")


# Функції для перетворення об'єктів у JSON-формат і навпаки
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


def from_json(data):
    pl = Playlist()
    for item in data:
        t = item["track"]
        pl.add_track(t["name"], t["author"], t["year"], t["duration"], item["genre"])
    return pl

if __name__ == "__main__":
    try:

        s = Song("Любов", "Скрябін", 2005)
        b = Song("Бета-каротин", "Boombox", 2005)
        m = Song()
        print(s)
        print(b)
        print(m)
        print(s.length())
        print(b.length())
        print(m.length())
        print(s == m)
        print(s == b)
        print(b == m)

        M = Track()
        print(M)
        S = Track("Любов", "Скрябін", 2005, "3:14")
        print(S)
        print(M.secconds())
        print(S.secconds())
        print(S + 87)
        print(M + 18)

        p = Playlist()
        try:
            print("\nСпроба завантаження треків з файлу 'tracks.txt':")
            p.load_from_file("tracks.txt")
        except Exception as e:
            print(e)
        p.add_track("Любов", "Скрябін", 2005, "3:14", "Поп")
        p.add_track("Бери своє", "Антитіла", 2008, "3:40", "Рок")
        print(p)
        print(p.total_duration_by_genre())

        # Pickle серіалізація/десеріалізація
        try:
            pickle_serialize(p, "playlist.pkl")
            loaded_playlist = pickle_deserialize("playlist.pkl")
            print("\nPickle десеріалізований плейлист:")
            print(loaded_playlist)
        except Exception as e:
            print(e)

        # Shelve серіалізація/десеріалізація
        try:
            shelve_serialize(p, "playlist_slv")
            shelved_playlist = shelve_deserialize("playlist_slv")
            print("\nShelve десеріалізований плейлист:")
            print(shelved_playlist)
        except Exception as e:
            print(e)

        # JSON серіалізація/десеріалізація
        try:
            json_serialize(p, "playlist.json", to_json)
            json_playlist = json_deserialize("playlist.json", from_json)
            print("\nJSON десеріалізований плейлист:")
            print(json_playlist)
        except Exception as e:
            print(e)
        
    except Exception as e:
        print(f"Виникла помилка: {e}")
    else:
        print("\nПрограма виконана успішно без аварійного завершення.")
    finally:
        print("Виконання програми завершено.")
