import sqlite3

CONN = sqlite3.connect('music.db')
CURSOR = CONN.cursor()

class Song:

    all = []

    def __init__(self, name, album, id= None):
        self.id = id
        self.name = name
        self.album = album

    @classmethod
    def create_table(cls):
        sql = """
            CREATE TABLE IF NOT EXISTS songs (
                id INTEGER PRIMARY KEY,
                name TEXT,
                album TEXT
            )
        """

        CURSOR.execute(sql)

    @classmethod
    def drop_table(cls):
        sql = """
            DROP TABLE IF EXISTS songs
        """

        CURSOR.execute(sql)

    def save(self):
        sql = """
            INSERT INTO songs (name, album)
            VALUES (?, ?)
        """

        CURSOR.execute(sql, (self.name, self.album))
        CONN.commit()
        #self.id = CURSOR.execute("SELECT last_insert_rowid() FROM songs").fetchone()[0]

    @classmethod
    def create(cls, name, album):
        #song = Song(name, album)
        song = cls(name,album)
        song.save()
        return song

    # new code goes here!
    @classmethod
    def new_from_db(cls,row):
        CURSOR.execute("SELECT last_insert_rowid() FROM songs").fetchone()[0]
        song = cls(
            name = row[1],
            album = row[2], 
            id = row[0]   
        )
        #song = cls(row[1],row[2])
        return song
        
    @classmethod
    def get_all(cls):
        sql = """
            SELECT * 
            FROM songs
        """
        all = CURSOR.execute(sql).fetchall()
        cls.all = [cls.new_from_db(row) for row in all]
        return cls.all
    @classmethod
    def find_by_name(cls,name):
        sql = """
            SELECT *
            FROM songs
            WHERE name = ?
            LIMIT 1
        """
        song = CURSOR.execute(sql,(name,)).fetchone()
        if not song:
            return None
        #print(song)
        return cls(
            name = song[1],
            album = song[2],
            id = song[0] 
        )
        #return cls.new_from_db(song)
#song = Song.create("Dheera","maha")
#song = Song.find_by_name("Hello")
#print(song)
    #find by id
    @classmethod
    def find_by_id(cls,id):
        sql = """
            SELECT * FROM songs
            WHERE id = ?
            LIMIT 1
        """
        song = CURSOR.execute(sql,(id,)).fetchone()
        if not song:
            return None
        print(song)
        return cls(
            name = song[1],
            album = song[2],
            id = song[0] 
        )
#song = Song.find_by_id(3)
#print(song)
    @classmethod
    def find_or_create(cls,name,album):
        sql = """
            SELECT * FROM songs
            WHERE name = ? and album = ?
            LIMIT 1
        """
        song = CURSOR.execute(sql,(name,album,)).fetchone()
        if not song:
            new_song = cls.create(name,album)
            print(new_song)
            return new_song
        print(song)
        return cls(
            name = song[1],
            album = song[2],
            id = song[0], 
        )
#song = Song.find_or_create("Hello",None)
#print(song)
    def update(self, name, album):
        #print(self, self.name, self.album)
        self.name = name or self.name
        self.album = album or self.album
        sql = """
            UPDATE songs SET name = ?, album = ? WHERE id = ?
    """
        song = CURSOR.execute(sql,(self.name,self.album,self.id))
        CONN.commit()

    @classmethod
    def update_cls(cls,id,name,album):
        song = cls.find_by_id(id)
        song.update(name,album)
        return song


#happy = Song.find_by_id(2)
happy = Song.update_cls(2,"99 Problems","Srii")   
print(happy)