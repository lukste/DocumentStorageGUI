import tkinter as tk
from DataBaseControler import *
from tkinter.ttk import Combobox
from tkinter import filedialog as fd
from FormWindow import FormWindow
import LogWrapper

#TODO dodać możliwość edytowania danych źródłowych. TO DŁUGO :(


class TableWindow:
    def __init__(self, win, dbController, logger):
        self._logger = logger
        self.dbController = dbController
        fontVal = 'Helvetica 13 bold'
        self.parent = win
        self.parent.config(bg='#ffd3d3')
        self.parent.title('Pismonator C-137')
        self.f = tk.LabelFrame(self.parent, text="Dane w tabeli", width=120, height=30, bg='grey', bd=1, cursor='arrow',
                       highlightbackground='#f3d3d3',
                       highlightcolor='#ffd3d3',background='#ffd3d3', highlightthickness=5, relief=tk.RIDGE)
        self.f.grid(row=1, column=0, padx=5, pady=5, rowspan=2, columnspan=2, sticky='news')
        self.f.grid_propagate(True)
        self.f2 = tk.LabelFrame(self.parent, text='Filtr', bg='#ffd3d3', width=120, height=2, bd=1, highlightbackground='#f3d3d3',
                       highlightcolor='#ffd3d3', highlightthickness=5, relief=tk.RIDGE)
        self.f2.grid(row=0, column=0, padx=5, pady=5, rowspan=1, columnspan=1, sticky='news')
        self.f2.grid_propagate(True)
        self.tableList = Combobox(self.f2, width=20, values=['SENDERS', 'CASES', 'USERS', 'SIGNATURES', 'FILES'])
        self.tableList.set("USERS")
        self.tableList.grid(row=0, column=0)
        self.lb = tk.Listbox(self.f, height=40, width=110, bg='#fef0e6', highlightcolor='#fff0f5', highlightbackground='#fff0f5', activestyle='dotbox', selectbackground='#ffaeae')
        self.lb.bind('<Button-3>', self.pop_up)
        self.tableList.bind('<<ComboboxSelected>>', self.filter)
        self.lb.pack(side='left', fill='both')
        self.filter(None)
        self.m = tk.Menu(self.f, tearoff=0)
        self.m.add_command(label='Usuń', command=self.del_pos)
        self.m.add_command(label='Anuluj')

    def del_pos(self):
        lid = self.lb.curselection()
        val = self.lb.get(lid)
        querry = 'DELETE FROM ' + self.tableList.get() + ' WHERE ID = ' + str(val[0]) + ';'
        self.dbController.c.execute(querry)
        self.dbController.con.commit()
        self.filter()



    def pop_up(self, event):
        self.lb.selection_clear(0, tk.END)
        self.lb.selection_set(self.lb.nearest(event.y))
        self.lb.activate(self.lb.nearest(event.y))
        try:
            self.m.tk_popup(event.x_root, event.y_root)
        finally:
            self.m.grab_release()

    def filter(self, event=None):
        v = self.tableList.get()
        if v:
            if(v == 'FILES'):
                querry = '''SELECT ID, DOC_ID, NAME FROM '''
            else:
                querry = '''SELECT * FROM '''
            self.lb.delete(0,tk.END)
            self._logger.debug('SQL: '.format(querry))
            self.dbController.c.execute(querry + v)
            rows = self.dbController.c.fetchall()
            for row in rows:

                self.lb.insert(tk.END, row)

        else:
            tk.messagebox.showwarning(title="Ostrzeżenie", message="Wybierz tabele")

    @LogWrapper.dec
    def extractSelectedValues(self):
        id0  = self.lb.curselection()[0]
        doc_id = str(self.lb.get(id0)[0])
        dane = self.selectFrom("DOCUMENTS", "ID", doc_id)
        pliki = self.selectFrom("FILES", "DOC_ID", doc_id)
        return dane[0], pliki

    @LogWrapper.dec_noargs
    def selectFrom(self, table, column, id):
        c = self.dbController.c
        querry = '''SELECT * FROM '''+table+''' WHERE '''+column+''' = '''+id+''';'''
        self._logger.debug("SQL: {}".format(querry))
        c.execute(querry)
        rows = c.fetchall()
        return rows



if __name__ == '__main__':
    window = tk.Tk()
    dbController = DbController('Pisma.db')
    mywin = TableWindow(window, dbController, None)
    window.mainloop()