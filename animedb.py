import sqlite3
from texttable import Texttable


class AnimeDatabase:
    def __init__(self, db):
        self._db = db
        self._con = None
        self._cur = None

    def connect(self):
        self._con = sqlite3.connect(self._db)
        self._cur = self._con.cursor()

    def create_table(self):
        self._cur.execute("""
        CREATE TABLE IF NOT EXISTS AnimeDatabase
        (id integer primary key autoincrement,
        name TEXT,
        sport TEXT,
        finished_airing INTEGER, 
        rating REAL,
        seen INTEGER);
        """)

    def insert_row(self, name, sport, finished_airing, rating, seen=False):
        self._cur.execute(" INSERT INTO AnimeDatabase(name,sport,finished_airing,rating,seen) Values (?,?,?,?,?)",
                          (name, sport, finished_airing, rating, seen))
        self._con.commit()

    def delete_row(self, row_id):
        self._cur.execute("""
        delete from AnimeDatabase
        where id=?
        """, (row_id,))
        self._con.commit()

    def mark_as_seen(self, row_id):
        self._cur.execute("""
        update AnimeDatabase set seen=1
        where id=?""", (row_id,))
        self._con.commit()

    def select_all(self):
        self._cur.execute("select * from AnimeDatabase")
        rows = self._cur.fetchall()
        table = Texttable()
        table.add_row(["ID", "Name", "Sport", "Finished Airing", "Rating", "Seen"])
        for row in rows:
            table.add_row(row)
        print(table.draw())

    def select_by_sport(self, sport):
        self._cur.execute("""
        select * from AnimeDatabase
        where sport=?""", (sport,))
        res = self._cur.fetchall()
        if res:
            table = Texttable()
            table.add_row(["ID", "Name", "Sport", "Finished Airing", "Rating", "Seen"])
            for row in res:
                table.add_row(row)
            print(table.draw())

    def select_random(self):
        self._cur.execute("""select * from AnimeDatabase
        Where seen=0 AND finished_airing="1"
        ORDER BY random() LIMIT 1;""")
        rand = self._cur.fetchone()
        if rand:
            table = Texttable()
            table.add_row(["ID", "Name", "Sport", "Finished Airing", "Rating", "Seen"])
            table.add_row(rand)
            print(table.draw())
        else:
            print("An anime that has finished airing and is not seen by you could not be found.")

    def disconnect(self):
        self._cur.close()
        self._con.close()


def main():
    obj = AnimeDatabase("anime_database.sqlite")
    obj.connect()
    obj.create_table()
    while True:
        choice = int(input("--------Anime Database--------\nChoose an option:\n1. Add anime\n2. View all animes"
                           "\n3. Filter animes by sport\n4. Choose random anime to watch"
                           "\n5. Mark anime as seen\n6. Delete anime\n7. Quit\n------------------------------"
                           "\n>>> Enter your choice: "))

        if choice == 1:
            anime_name = input(">>> Enter name: ")
            sport_type = input(">>> Enter type of sport: ")
            
            while True:
                 finished = input(">>> Is the anime finished? [y/n]: ")
                    if finished == "y":
                        finished = 1
                        break
                    elif finished == "n":
                        finished = 0
                        break
                    else:
                        print("Please enter only 'y' or 'n'")
  
            rate = float(input(">>> Enter rating: "))

            obj.insert_row(anime_name, sport_type, finished, rate, False)

        elif choice == 2:
            obj.select_all()
        elif choice == 3:
            sport_name = input(">>> Enter type of sport: ")
            obj.select_by_sport(sport=sport_name)
        elif choice == 4:
            obj.select_random()
        elif choice == 5:
            enter_id = int(input(">>> Enter ID: "))
            obj.mark_as_seen(enter_id)
        elif choice == 6:
            enter_id = int(input(">>> Enter ID: "))
            obj.delete_row(enter_id)

        elif choice == 7:
            obj.disconnect()
            break
        else:
            print("Error!")


if __name__ == '__main__':
    main()
