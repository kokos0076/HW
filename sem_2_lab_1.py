class Song:
    def __init__(self,name="Останній день",author="MamaRika", year=2023):
        self.a=name
        self.b=author
        self.c=year

    def __str__(self):
        return f'{self.b}. "{self.a}" ({self.c})'

    def __eq__(self, other):
        if self.c == other.c:
            return f'Пісні "{self.a}" і "{other.a}" вийшли в один рік: {self.c}'
        else:
            return f''

    def length(self):
        return f'Кількість слів у назві пісні "{self.a}":{len(self.a.split())}'


class Track(Song):
    def __init__(self,name="Останній день",author="MamaRika", year=2023,duration="2:29"):
        Song.__init__(self,name,author,year)
        self.d=duration

    def __str__(self):
        return f'{self.b}. "{self.a}" ( {self.c})  {self.d}'

    def secconds(self):
        return f'Тривалість пісні "{self.a}" у секундах: {int(self.d.split(":")[0]) * 60 + int(self.d.split(":")[1])}'

    def __add__(self,sec):
        all_sec = int(self.d.split(":")[0]) * 60 + int(self.d.split(":")[1]) + int(sec)
        new_min = all_sec // 60
        new_sec = all_sec%60
        new_duration = f'Тривалість пісні після доданих {int(sec)} секунд: {new_min}:{new_sec}'
        return Track(self.a, self.b, self.c, new_duration)

class Playlist:
    def __init__(self):
        self.tracks = []

    def add_track(self, name, author, year, duration, genre):
        track = Track(name, author, year, duration)
        self.tracks.append((track, genre))

    def load_from_file(self, filename):
        with open(filename, 'r', encoding='utf-8') as file:
            for line in file:
                parts = line.split(',')
                name, author, year, duration, genre = parts
                track = Track(name, author, year, duration)
                self.tracks.append((track, genre))

    def total_duration_by_genre(self):
        genre_durations = {}
        for track, genre in self.tracks:
            genre = genre.strip()  
            minutes, seconds = map(int, track.d.split(":"))
            total_seconds = minutes * 60 + seconds
            if genre in genre_durations:
                genre_durations[genre] += total_seconds
            else:
                genre_durations[genre] = total_seconds
        result = ""
        for genre in genre_durations:
            duration = genre_durations[genre]
            result += f"{genre}: {duration // 60}:{duration % 60:02d}, "
        return f'Тривалість всіх пісень за цими жанрами: {result.rstrip(", ")}' 

    def __str__(self):
       result = ""
       for track, genre in self.tracks:
           result += f'{track} - {genre}'
       return f'Плейлист з {len(self.tracks)} треків: \n{result}'


s = Song("Любов","Скрябін",2005)
b = Song("Бета-каротин","Boombox",2005)
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
S = Track("Любов","Скрябін",2005,"3:14")
print(S)
print(M.secconds())
print(S.secconds())
print(S + 87)
print(M + 18)
p = Playlist()
p.load_from_file("tracks.txt")
p.add_track("Любов",'\n'" Скрябін",2005,"3:14", "Поп")
p.add_track("Бери своє",'\n'" Антитіла", 2008, "3:40", "Рок") 
print(p)
print(p.total_duration_by_genre())
