from tkinter.ttk import Combobox
from tkcalendar import DateEntry
from tkinter import messagebox
from tkinter import simpledialog
from tkinter import filedialog as fd
from MainWindow import *
import webbrowser
import LogWrapper

fontVal = 'Helvetica 13 bold'
color = '#fff0f5'



class FormWindow():
    def __init__(self, window, dbController, logger,  dane=(), pliki=()):
        '''

        :param window: parent window
        :param dbController: sqlite database controller obj
        :param logger: logging obj
        :param dane: tuple of data to fill form; default = ()
        :param pliki: tuple of files related to form default = ()

        '''



        self.dbController = dbController
        self.win = window
        self.win.config(bg='#ffd3d3')
        self._logger = logger
        self._logger.debug("Building form window with data: {}".format(dane))
        lista_departamentow, lista_userow, lista_spraw, lista_sygnatur = self.get_data()
        self.win.title('Wprowadzanie danych')
        self.selectedFiles = []
        self.fileDict = {}
        self.fileIDict = {}
        self.f = tk.LabelFrame(self.win, text="Formularz", width=800, height=150, bg=color, bd=1, cursor='arrow',
                               highlightbackground='silver',
                               highlightcolor='silver', highlightthickness=0, relief=tk.RIDGE)
        self.f.grid(row=0, column=0, padx=5, pady=5, ipadx=5, ipady=5, rowspan=1, columnspan=1, sticky='NSEW')
        self.f2 = tk.LabelFrame(self.f, text="Pliki", bg=color, relief=tk.RIDGE)
        self.f2.grid(row=4, column=3,padx=5, pady=5, ipadx=5, ipady=5, rowspan=1, columnspan=1, sticky='NSEW')
        self.lbFile = tk.Listbox(self.f2, selectmode=tk.SINGLE, height=len(pliki) | 1, width=35)

        self.lbl1 = tk.Label(self.f, text='Nadawca', font=fontVal,  bg=color)
        self.lbl1.grid(row=1, column=0, sticky='w')
        self.cbb1 = (Combobox(self.f, values=list(lista_departamentow.keys()), width=50), "SENDERS", lista_departamentow)
        self.cbb1[0].grid(row=1, column=1, sticky='we')
        self.lbl2 = tk.Label(self.f, text='Data', font=fontVal,  bg=color)
        self.lbl2.grid(row=1, column=2, sticky='w', pady=5)
        self.cal =  DateEntry(self.f, date_pattern='dd.mm.yyyy', width=10, font=fontVal, background='#ffd3d3',
                                            foreground='white', borderwidth=1, selectmode='day',)
        self.cal.grid(row=1, column=3, sticky='ew')
        self.lbl2 = tk.Label(self.f, text='Sprawa IK', font=fontVal,  bg=color)
        self.lbl2.grid(row=2, column=0, sticky='w')
        self.cbb2 = (Combobox(self.f, values=list(lista_spraw.keys()), width=30), "CASES", lista_spraw)
        self.cbb2[0].grid(row=2, column=1, sticky='we')
        self.cbb2[0].bind('<<ComboboxSelected>>', self.sygn_update)
        self.signNum = tk.StringVar()
        self.lblSygn = tk.Label(self.f, textvariable=self.signNum, font=fontVal, bg=color)
        self.lblSygn.grid(row=6, column=1)
        tk.Label(self.f, text="SubID sprawy: ", font=fontVal, bg=color).grid(row=6, column=0)
        self.lbl3 = tk.Label(self.f, text='Kto otrzymał?', font=fontVal, bg=color)
        self.lbl3.grid(row=2, column=2, sticky='w', pady=5)
        self.cbb3 = (Combobox(self.f, values=list(lista_userow.keys()), width=25), "USERS", lista_userow)
        self.cbb3[0].grid(row=2, column=3,sticky='we')
        self.lbl6 = tk.Label(self.f, text='Zrobione?', font=fontVal, bg=color)
        self.lbl6.grid(row=3, column=0, sticky='w', pady=5)
        self.cbb6 = (Combobox(self.f, values=["Tak", "Nie", "Domyśl się"], width=30), "", {})
        self.cbb6[0].grid(row=3, column=1, sticky='we')
        tk.Button(self.f, text='Zatwierdź wpis', command=self.check_data).grid(row=5, column=2, sticky='news')
        tk.Button(self.f, text='Zakończ', command=self.quit_button).grid(row=5, column=3, sticky='news')
        tk.Button(self.f, text='Dodaj plik', command=(lambda: self.selectedFiles == self.select_file())).grid(row=4,
                                                                                                              column=2,
                                                                                                              sticky='news')
        tk.Button(self.f, text='Wyczyść', command=self.clear).grid(row=5, columns=1, sticky='news')
        self.cbb4 = (Combobox(self.f, values=list(lista_sygnatur.keys()), width=30), "SIGNATURES", lista_sygnatur)
        self.cbb4[0].grid(row=4, column=1, sticky='ew')
        self.lbl4 = tk.Label(self.f, text='Sygnatura', font=fontVal, bg=color)
        self.lbl4.grid(row=4, column=0, sticky='w', pady=5)
        self.lbl5 = tk.Label(self.f, text='Dotyczy', font=fontVal, bg=color)
        self.lbl5.grid(row=3, column=2, sticky='w', pady=5)
        self.cbb5 = (Combobox(self.f, width=30, values=[]), "", {})
        self.cbb5[0].grid(row=3, column=3, sticky='we')
        self.dane = dane
        print("Running with or without files added...")
        self.lbFile.bind('<Double-1>', self.save_file)
        self.lbFile.bind('<Button-3>', self.pop_up)
        self.lbFile.grid(row=0, column=0, sticky='news')
        self.m = tk.Menu(self.f2, tearoff=0)
        self.m.add_command(label="Otwórz", command=self.open_pdf_file)
        self.m.add_command(label='Usuń', command=self.del_pos)
        self.m.add_command(label='Anuluj')

        for fid, doc_id, name, blob in pliki:
            self.selectedFiles.append(name)
            self.lbFile.insert(tk.END, name)
            self.fileDict[name] = blob
            self.fileIDict[name] = fid

        if self.dane:
            j = 1
            form = [getattr(self, 'cbb' + str(i)) for i in range(1, 7)]
            for cb, table, dic in form:
                if table:
                    val = self.get_val_from_table(table, self.dane[j])
                else:
                    val = self.dane[j]
                cb.set(val)
                j += 1
            self.sygn_update(None)
            self.cal.set_date(self.dane[7])

    @LogWrapper.dec
    def pop_up(self, event):
        self.lbFile.selection_clear(0, tk.END)
        self.lbFile.selection_set(self.lbFile.nearest(event.y))
        self.lbFile.activate(self.lbFile.nearest(event.y))
        try:
            self.m.tk_popup(event.x_root, event.y_root)
        finally:
            self.m.grab_release()

    @LogWrapper.dec
    def open_pdf_file(self):
        lid = self.lbFile.curselection()
        val = self.lbFile.get(lid[0])
        f = open('temp.pdf', 'wb')

        f.write(self.fileDict[val])
        f.close()
        webbrowser.open(f.name)

    @LogWrapper.dec
    def del_pos(self):
        print("Sel files:", self.selectedFiles)
        lid = self.lbFile.curselection()
        val = self.lbFile.get(lid)
        if( val in self.fileIDict):
            querry = 'DELETE FROM FILES WHERE ID = ' + str(self.fileIDict[val]) + ';'
            self._logger.debug('SQL: {}'.format(querry))
            self.dbController.c.execute(querry)
            self.dbController.con.commit()
        if val in self.selectedFiles:
            self.selectedFiles.remove(val)
        self.lbFile.delete(lid)

    @LogWrapper.dec
    def sygn_update(self, event):
        val = self.cbb2[0].get()
        dict = self.cbb2[2]
        if val in dict:
            self.signNum.set(dict[val][1])
        else:
            self.signNum.set("Brak sygnaturku")

    @LogWrapper.dec
    def save_file(self, event):
        curs = self.lbFile.curselection()
        if curs:
            name = self.lbFile.get(curs[0])
            f = fd.asksaveasfile(mode='wb', initialfile=name)
            if f:
                f.write(self.fileDict[name])

    @LogWrapper.dec
    def get_val_from_table(self, table, i):
        c = self.dbController.c
        querry = '''SELECT NAME FROM ''' + table + ''' WHERE ID = ''' + str(i) + ''';'''
        self._logger.debug("Function {} executed SQL: {}".format('getValFromTable', querry))
        c.execute(querry)
        rows = c.fetchall()
        for row in rows:
            try:
                return row[0]
            except:
                return row

    @LogWrapper.dec
    def get_data(self):
        c = self.dbController.c
        c.execute('''SELECT * FROM SENDERS;''')
        rows = c.fetchall()
        senders = {b: a for a, b in rows}
        c.execute('''SELECT * FROM USERS;''')
        rows = c.fetchall()
        users = {b: a for a, b in rows}
        c.execute('''SELECT * FROM CASES;''')
        rows = c.fetchall()
        cases = {b: (a, c) for a, b, c in rows}
        c.execute('''SELECT * FROM SIGNATURES;''')
        rows = c.fetchall()
        signatures = {b: a for a, b in rows}
        return senders, users, cases, signatures

    def clear(self):
        self.lbFile.delete(0,tk.END)
        self.selectedFiles = []

    def select_file(self):
        try:
            files = fd.askopenfiles()
            for file in files:
                fn = file.name.split("/")[-1]
                self.selectedFiles.append(file)
                self.lbFile.insert(tk.END, fn)
            self.lbFile.configure(height=self.lbFile.size())
        except FileNotFoundError as e:
            self._logger.warning("No file selected", e)

    @staticmethod
    def convert_to_binary_data(filename):
        with open(filename, 'rb') as file:
            blobData = file.read()
        return blobData

    @LogWrapper.dec
    def insert_file(self, file, doc_id):
        c = self.dbController.c
        insert_querry = '''INSERT INTO FILES (NAME, DOC_ID, FILE) VALUES (?,?,?)'''
        self._logger.debug("Function: {} executed SQL: ".format('inserFile', insert_querry))
        bin_file = self.convert_to_binary_data(file.name)
        c.execute(insert_querry, (file.name.split('/')[-1], doc_id, bin_file))
        self.dbController.con.commit()
        return c.lastrowid

    @LogWrapper.dec
    def insert_data(self, table, values):
        c = self.dbController.c
        if (table == 'DOCUMENTS'):
            if(self.dane):
                insert_querry = '''UPDATE ''' + table + ''' SET SENDER_ID = ?, CASE_ID = ?, USER_ID = ?, SIGN_ID = ?, DESCR = ?, STATUS_VAL = ?, DATE = ? WHERE ID = ?;'''
                self._logger.debug("SQL: {} {}".format(insert_querry, values))
                c.execute(insert_querry, values)
                self.dbController.con.commit()
                return values[-1]
            else:
                insert_querry = '''INSERT INTO ''' + table + '''(SENDER_ID, CASE_ID, USER_ID, SIGN_ID, DESCR, STATUS_VAL, DATE) VALUES (?,?,?,?,?,?,?)'''
                self._logger.debug("SQL: {} {}".format(insert_querry, values))
                c.execute(insert_querry, values)
                self.dbController.con.commit()
                return c.lastrowid
        elif table == 'CASES':
            insert_querry = '''INSERT INTO ''' + table + '''  (NAME, TXT_ID) VALUES (?,?)'''
            self._logger.debug('SQL: {} {}'.format(insert_querry, values))
            c.execute(insert_querry, values)
            self.dbController.con.commit()
            return c.lastrowid
        else:
            insert_querry = '''INSERT INTO ''' + table + '''  (NAME) VALUES (?)'''
            self._logger.debug('SQL: {} {}'.format(insert_querry, values))
            c.execute(insert_querry, values)
            self.dbController.con.commit()
            return c.lastrowid

    def check_data(self):
        cbbList = [getattr(self, 'cbb' + str(i)) for i in range(1, 7)]
        lblList = [getattr(self, 'lbl' + str(i)) for i in range(1, 7)]
        if (all(el[0].get() for el in cbbList)):
            for obj in lblList:
                obj.configure(background='White', foreground='black')
            val = []
            for cb, table, dic in cbbList:
                new = cb.get()
                if new not in cb['values']:
                    values = (new,)
                    if table:
                        if table == 'CASES':
                            sygnID = simpledialog.askstring("Sygnatura", 'Podaj wartość SygnID dla sprawy: ')
                            values = (new, sygnID)
                        id = self.insert_data(table, values)
                        self._logger.debug("New element in table: {}; ID: {}".format(table, id))
                        dic[new] = id
                        cb['values'] = (*cb['values'], new)
                        print(values)
                        val.append(id)
                        print('val: ', val)
                    else:
                        val.append(new)
                else:
                    if dic:
                        if isinstance(dic[new], tuple):
                            val.append(dic[new][0])
                        else:
                            val.append(dic[new])
                    else:
                        val.append(new)
            val.append(self.cal.get())
            if self.dane:
                val.append(self.dane[0])
            print(val)
            doc_id = self.insert_data("DOCUMENTS", tuple(val))
            if self.selectedFiles:
                self._logger.debug('SELECTED FILES: {}'.format(self.selectedFiles))
                for file in self.selectedFiles:
                    if not isinstance(file, str):
                        self.insert_file(file, doc_id)
            tk.messagebox.showinfo(title="Informacja", message="Wprowadzone dane zapisane pomyśllnie w bazie")
            self.win.destroy()
            return 0
        else:
            tk.messagebox.showwarning(title="Ostrzeżenie", message="Część danych nie została wprowadzona")
            for lbl, cbo in zip(lblList, cbbList):
                if (cbo[0].get() == ''):
                    lbl.configure(background='red', foreground='white')
                else:
                    lbl.configure(background='white', foreground='black')

    def quit_button(self):
        self.win.destroy()
        return 0


def main():
    pass


if __name__ == '__main__':
    main()
