import tkinter as tk
from tkinter import ttk
from DataBaseControler import *
from FormWindow import FormWindow
import logging
import LogWrapper

fontVal = 'Helvetica 10 bold'
columns= (('ID', 30),('Nadawca', 100), ('Sprawa',300), ('Sygnatura',150), ('Kto dostał',80), ('Czego dotyczy', 100), ('Zrobione?',80), ('Data pisma',80))


class RecordsWindow:
    @LogWrapper.dec_noargs
    def __init__(self, win, dbController, logger):
        self.dbController = dbController
        self._logger = logger
        self._logger.debug("Building Records Window")
        self.parent = win
        self.parent.config(bg='#ffd3d3')
        self.parent.title('Pismonator C-137')
        self.f = tk.LabelFrame(self.parent, text="Wprowadzone dokumenty", width=250, height=30, bg='grey', bd=1, cursor='arrow',
                       highlightbackground='#f3d3d3',
                       highlightcolor='#ffd3d3',background='#ffd3d3', highlightthickness=5, relief=tk.RIDGE)
        self.f.grid(row=1, column=0, padx=5, pady=5, rowspan=2, columnspan=2, sticky='news')
        self.f.grid_propagate(True)
        self.f2 = tk.LabelFrame(self.parent, text='Filtr', bg='#ffd3d3', width=120, height=2, bd=1, highlightbackground='#f3d3d3',
                       highlightcolor='#ffd3d3', highlightthickness=5, relief=tk.RIDGE)
        self.f2.grid(row=0, column=0, padx=5, pady=5, rowspan=1, columnspan=1, sticky='news')
        self.f2.grid_propagate(True)
        tk.Button(self.f2, text=" Odśwież ", width=20, command=self.refresh).pack(side = 'right', fill='both')
        self.ent = tk.Entry(self.f2, width=120)
        self.ent.bind('<Return>', self.refresh)
        #self.ent.grid(row=0, column=0, sticky='news')
        self.ent.pack(side = 'left', fill='both')
        self.dbController.c.execute('''SELECT DOCUMENTS.ID, SENDERS.NAME, CASES.NAME, SIGNATURES.NAME, USERS.NAME, DOCUMENTS.DESCR, DOCUMENTS.STATUS_VAL, DOCUMENTS.DATE  FROM Documents, Cases, Users, Senders, SIGNATURES 
        WHERE DOCUMENTS.SENDER_ID = SENDERS.ID and DOCUMENTS.CASE_ID = CASES.ID and DOCUMENTS.USER_ID = USERS.ID and DOCUMENTS.SIGN_ID = SIGNATURES.ID''')
        self.rows = self.dbController.c.fetchall()
        self.lb = ttk.Treeview(self.f, height=40, show='headings', columns=columns, selectmode='browse')
        self.tree_setup()
        self.tree_scroll = ttk.Scrollbar(self.f)
        self.tree_scroll.configure(command=self.lb.yview)
        self.lb.configure(yscrollcommand=self.tree_scroll.set)
        self.lb.bind('<Double-1>', self.edit_window)
        self.lb.bind('<Button-3>', self.pop_up)
        self.lb.pack(side='left', fill='both')
        self.tree_scroll.pack(side='right', fill='both')
        self.filter(None)
        self.m = tk.Menu(self.f, tearoff=0)
        self.m.add_command(label="Edytuj", command=self.edit_window)
        self.m.add_command(label='Usuń', command=self.del_pos)
        self.m.add_command(label='Anuluj')

    @LogWrapper.dec
    def find_in_rows(self, doc_id):
        for el in self.rows:
            did = el[0]
            if (did == doc_id):
                return self.rows.index(el)

    @LogWrapper.dec
    def del_pos(self):
        if(tk.messagebox.askquestion("Usuwanie danych", "Czy na pewno chcesz usunąć dokument?") == 'yes'):
            id = self.lb.item(self.lb.selection()[0])['values'][0]
            querry = 'DELETE FROM DOCUMENTS WHERE ID = ' + str(id) + ';'
            self.rows.pop(self.find_in_rows(id))
            self._logger.debug('SQL: {}'.format(querry))
            self.dbController.c.execute(querry)
            self.dbController.con.commit()
            self.filter(None)

    @LogWrapper.dec_noargs
    def pop_up(self, event):
        iid = self.lb.identify_row(event.y)
        if iid:
            self.lb.selection_set(iid)
            try:
                self.m.tk_popup(event.x_root, event.y_root)
            finally:
                self.m.grab_release()
        else:
            pass


    def tree_setup(self):
        i = 0
        for col, width in columns:
            self.lb.heading(i, text=col)
            self.lb.column(i, width=width, anchor='w')
            i += 1
        for row in self.rows:
            self.lb.insert('', 'end', value=row)


    def refresh(self, *args):
        self.dbController.c.execute('''SELECT DOCUMENTS.ID, SENDERS.NAME, CASES.NAME, SIGNATURES.NAME, USERS.NAME, DOCUMENTS.DESCR, DOCUMENTS.STATUS_VAL, DOCUMENTS.DATE  FROM Documents, Cases, Users, Senders, SIGNATURES 
                WHERE DOCUMENTS.SENDER_ID = SENDERS.ID and DOCUMENTS.CASE_ID = CASES.ID and DOCUMENTS.USER_ID = USERS.ID and DOCUMENTS.SIGN_ID = SIGNATURES.ID''')
        self.rows = self.dbController.c.fetchall()
        self.filter(None)


    def filter(self, event):
        val = (self.ent.get()).upper()
        for line in self.lb.get_children():
            self.lb.delete(line)
        for row in self.rows:
            for el in row:
                el = str(el).upper()
                if(val in el or not val):
                    self.lb.insert('', 'end', value=row)
                    break


    def extract_selected_values(self):
        doc_id = str(self.lb.item(self.lb.focus())['values'][0])
        dane = self.select_from("DOCUMENTS", "ID", doc_id)
        pliki = self.select_from("FILES", "DOC_ID", doc_id)
        return dane[0], pliki

    def select_from(self, table, column, id):
        c = self.dbController.c
        querry = '''SELECT * FROM '''+table+''' WHERE '''+column+''' = '''+id+''';'''
        self._logger.debug('SQL: {}'.format(querry))
        c.execute(querry)
        rows = c.fetchall()
        return rows


    def edit_window(self, event):
        d, f = self.extract_selected_values()
        win = tk.Toplevel()
        FormWindow(win, self.dbController, self._logger, dane=d, pliki=f)


if __name__ == '__main__':
    window = tk.Tk()
    dbController = DbController('Pisma.db')
    mywin = RecordsWindow(window, dbController)
    window.mainloop()