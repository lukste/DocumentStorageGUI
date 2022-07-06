from FormWindow import *
from DataBaseControler import *
from FormWindow import FormWindow
from RecordsWindow import *

from TableWindow import *


'''TO DO: 
DODAĆ CONFIG FILE ABY MÓC ZAPISAĆ USTAWIENIA (DB PATH)'''

class MainWindow():
    def __init__(self, win, dbController, logger):
        self._logger = logger
        self._logger.debug("Main window creation started")
        fontVal = 'Helvetica 13 bold'
        self.dbController = dbController
        self.parent = win
        self.parent.title('Pismonator C-137')
        self.parent.resizable(False, False)
        self.parent.config(bg='#ffd3d3')
        self.frame = tk.Frame(win, background='#ffdfdf')
        self.frame.grid(row=0, column=0, sticky='news')
        tk.Button(self.frame, command=self.newRecord, text="Wprowadź nowe pismo", width=50, height=4,
                            borderwidth=10, activebackground='#ffd3d3', font=fontVal, background='#f3d3d3').pack()
        tk.Button(self.frame, text="Edytuj wpis", width=50, height=4, borderwidth=10,
                            activebackground='#ffd3d3', font=fontVal, command=self.viewRecords, background='#f3d3d3').pack()
        tk.Button(self.frame, text="Edytuj dane źródłowe", width=50, height=4, borderwidth=10,
                  activebackground='#ffd3d3', font=fontVal, command=self.tableWindow, background='#f3d3d3').pack()
        tk.Button(self.frame, command=self.quitWindow, text="Wyjdź", width=50, height=4, borderwidth=10,
                            activebackground='#ffd3d3', font=fontVal, background='#f3d3d3').pack()
        self.frame.tkraise()
        self._logger.debug('Main window created!')

    def tableWindow(self):
        win = tk.Toplevel()
        self._logger.debug("Creating Window with tables")
        TableWindow(win, self.dbController, self._logger)

    def quitWindow(self):
        self._logger.debug("Quiting MainWindow...")
        self.parent.destroy()
        return 0

    def viewRecords(self):
        self._logger.debug("Creating Document Table Window")
        win = tk.Toplevel()
        RecordsWindow(win, self.dbController, self._logger)

    def newRecord(self):
        self._logger.debug("Creating Form Window")
        win = tk.Toplevel()
        FormWindow(win, self.dbController, self._logger)

def main():
    window = tk.Tk()
    mywin = MainWindow(window)
    window.mainloop()

if __name__ == '__main__':
    main()