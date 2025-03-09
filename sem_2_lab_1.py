class Song():
    def __init__(self,name="Останній день",author="MamaRika", year=2023):
        self.a=name
        self.b=author
        self.c=year
    def __str__(self):
        return f'{self.b}. "{self.a}" ({self.c})'
    def __eq__(self, other):
        if self.c == other.c:
            return f'Пісні "{self.a}" і "{other.a}" вийшли в один рік'
        else:
            return f''
    def length(self):
        return f'Кількість слів у назві пісні "{self.a}":{len(self.a.split())}'

class Track(Song):
    def __init__(self,name="Останній день",author="MamaRika", year=2023,duration="2:29"):
        Song.__init__(self,name,author,year)
        self.d=duration
    def __str__(self):
        return f'{self.b}. "{self.a}" ({self.c}): {self.d}'
    def secconds(self):
        return f'Тривалість пісні "{self.a}" у секундах: {int(self.d.split(":")[0]) * 60 + int(self.d.split(":")[1])}'

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
