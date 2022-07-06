import sqlite3
from sqlite3 import Error

class DbController:
    def __init__(self, address):
        try:
            self.con = sqlite3.connect(address)
            self.c = self.con.cursor()
            self.con.commit()
        except Error as e:
            print("Błąd tworzenia bazy danych!", e)



    def __del__(self):
        try:
            self.con.close()
        except Error as e:
            print("Błąd zamykania bazy danych!", e)
