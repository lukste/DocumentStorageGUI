from MainWindow import *
import configparser as cf
import logging


class Main:
    def __init__(self):
        config = cf.ConfigParser()
        try:
            config.read('config.ini')
            cdef = config['DEF']
        except KeyError as e:
            print("No config file detected! Add config file to .exe directory.")
        if cdef['debug']:
            logging.basicConfig(filename=cdef['logfile'], level=logging.DEBUG, format="%(asctime)s %(message)s")
        else:
            logging.basicConfig(filename=cdef['logfile'], level=logging.WARNING, format="%(asctime)s %(message)s")
        self.dbAddr = cdef['db']
        self.dbController = DbController(self.dbAddr)
        self.window = tk.Tk()
        self.winMain = MainWindow(self.window, self.dbController, logging.getLogger())
        self.window.mainloop()

if __name__ == '__main__':
    c = Main()