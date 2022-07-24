import sqlite3

import LogWrapper
from LogWrapper import *
from sqlite3 import Error

class DbController:
    @LogWrapper.dec_noargs
    def __init__(self, address):
        try:
            self.con = sqlite3.connect(address)
            self.c = self.con.cursor()
            self.con.commit()
        except Error as e:
            print("Błąd tworzenia bazy danych!", e)

    @LogWrapper.dec_noargs
    def __del__(self):
        try:
            self.con.close()
        except Error as e:
            print("Błąd zamykania bazy danych!", e)
