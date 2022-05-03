import tkinter as tk
from tkinter import *
from tkinter import messagebox
import sqlite3


class DictWork:
    def __init__(self, name):
        self.dictname = name
        conn = None
        curs = None
        try:
            conn = sqlite3.connect(self.dictname, 5)
            curs = conn.cursor()
            curs.execute('CREATE TABLE IF NOT EXISTS dictionary (l1 TEXT, l2 TEXT)')
            conn.commit()
        except:
            raise

        finally:
            if curs is not None:
                curs.close()
            if conn is not None:
                conn.close()

    def get_word(self, findText, iTbale='1'):
        conn = None
        curs = None

        try:
            conn = sqlite3.connect(self.dictname, 5)
            curs = conn.cursor()

            if iTbale == '1':
                curs.execute(f"SELECT rowid, l2 FROM dictionary WHERE l1 ='{findText}'")
            elif iTbale == '2':
                curs.execute(f"SELECT rowid, l1 FROM dictionary WHERE l2 ='{findText}'")
            else:
                curs.execute("SELECT rowid, l1, l2 FROM dictionary")

            res = curs.fetchall()
            return res

        except:
            return []

        finally:
            if curs is not None:
                curs.close()
            if conn is not None:
                conn.close()

    def get_wordById(self, wordId):
        conn = None
        curs = None
        if not isinstance(wordId, int):
            return []
        try:
            conn = sqlite3.connect(self.dictname, 5)
            curs = conn.cursor()
            curs.execute(f"SELECT l1, l2 FROM dictionary WHERE rowid ='{wordId}'")
            res = curs.fetchall()
            return res

        except:
            return []

        finally:
            if curs is not None:
                curs.close()
            if conn is not None:
                conn.close()

    def set_word(self, text1, text2):
        conn = None
        curs = None

        if text1 == '' or text2 == '':
            return -1

        try:
            conn = sqlite3.connect(self.dictname, 5)
            curs = conn.cursor()
            curs.execute("INSERT INTO dictionary (l1, l2) VALUES(?, ?)", (text1, text2))
            conn.commit()
            return 0
        except:
            return -2

        finally:
            if curs is not None:
                curs.close()
            if conn is not None:
                conn.close()

    def del_word(self, dellId):
        conn = None
        curs = None
        if not isinstance(dellId, int):
            return -1

        try:
            conn = sqlite3.connect(self.dictname, 5)
            curs = conn.cursor()
            curs.execute(f"DELETE FROM dictionary WHERE rowid = {dellId}")
            conn.commit()
            return 0
        except:
            return -2

        finally:
            if curs is not None:
                curs.close()
            if conn is not None:
                conn.close()

    def droop_all(self):
        conn = None
        curs = None

        try:
            conn = sqlite3.connect(self.dictname, 5)
            curs = conn.cursor()
            curs.execute("DROP TABLE IF EXISTS dictionary")
            conn.commit()
            curs.execute('CREATE TABLE IF NOT EXISTS dictionary (l1 TEXT, l2 TEXT)')
            conn.commit()
            return 0
        except:
            return -1

        finally:
            if curs is not None:
                curs.close()
            if conn is not None:
                conn.close()


class TextEdit:
    def __init__(self, rootEdit):
        f = LabelFrame(rootEdit)
        f.pack(fill=tk.X)

        scroll = Scrollbar(f)
        self.textEdit = Text(f, height=20, bd=0, width=53, state='disabled', yscrollcommand=scroll.set)
        scroll.config(command=self.textEdit.yview)
        scroll.pack(side=RIGHT, fill=Y)
        self.textEdit.pack()

    def writeln(self, text):
        self.textEdit.configure(state='normal')
        self.textEdit.insert(1.0, f'{text}\n')
        self.textEdit.configure(state='disabled')

    def clear(self):
        self.textEdit.configure(state='normal')
        self.textEdit.delete('1.0', END)
        self.textEdit.configure(state='disabled')


class App(tk.Tk):

    def __init__(self):
        super().__init__()
        self.title("Dictionary")
        self.dictwork = DictWork("DicEngUkr.sl3")
        self.resizable(0, 0)
        self.createWindow()

    def createWindow(self):
        group_0 = Frame(self)
        group_0.pack(padx=4, pady=3)

        group_1 = LabelFrame(group_0, text=" Додати слово в словник або знайти слово у словнику ")
        group_1.pack(ipadx=3, ipady=2, pady=2, fill=tk.X)

        group_1_1 = Frame(group_1)
        group_1_1.pack(fill=tk.X, pady=2)

        Label(group_1_1, text="Слово 1", width=7).pack(side=tk.LEFT)
        self.addWordTo1 = Entry(group_1_1)
        self.addWordTo1.pack(padx=5, fill=tk.X)

        group_1_2 = Frame(group_1)
        group_1_2.pack(fill=tk.X, pady=2)

        Label(group_1_2, text="Слово 2", width=7).pack(side=tk.LEFT)
        self.addWordTo2 = Entry(group_1_2)
        self.addWordTo2.pack(padx=5, fill=tk.X)

        group_1_3 = Frame(group_1)
        group_1_3.pack(fill=tk.X, pady=2)
        Label(group_1_3, text="", width=7).pack(side=tk.LEFT)

        Button(group_1_3, text="Add", width=10, command=self.addWord).pack(padx=5, side=tk.LEFT)
        Label(group_1_3, text="", width=2).pack(side=tk.LEFT)

        Button(group_1_3, text="Find", width=10, command=self.getWord).pack(padx=5, side=tk.LEFT)
        Label(group_1_3, text="", width=2).pack(side=tk.LEFT)

        Button(group_1_3, text="Show All", width=10, command=self.showAllWord).pack(padx=5, side=tk.LEFT)

        group_2 = LabelFrame(group_0, text=" Видалити слово ")
        group_2.pack(ipadx=3, ipady=2, pady=2, fill=tk.X)

        group_2_1 = Frame(group_2)
        group_2_1.pack(fill=tk.X)

        Label(group_2_1, text="Введіть ID", width=9).pack(side=tk.LEFT)

        vcmd = (self.register(self.enter_only_digits), '%P', '%d')
        self.delword1 = Entry(group_2_1, validate='key', validatecommand=vcmd)
        self.delword1.pack(padx=5, fill=tk.X)

        group_2_2 = Frame(group_2)
        group_2_2.pack(fill=tk.X)

        Label(group_2_2, text="", width=9).pack(side=tk.LEFT)
        Button(group_2_2, text="Delete", width=10, command=self.deleteWord).pack(padx=5, pady=3, side=tk.LEFT)
        Button(group_2_2, text="Delete All", width=10, command=self.deleteAll).pack(padx=5, pady=3, side=tk.RIGHT)

        self.textedit = TextEdit(group_0)

    def showAllWord(self):
        self.textedit.clear()
        res = self.dictwork.get_word("", 'All')
        if self.dictwork.get_word("", 'All'):
            for id, l1Word, l2Word in res[::-1]:
                self.textedit.writeln(f"{id}:{l1Word}:{l2Word}")
        else:
            self.textedit.writeln("Словник пустий!")

    def getWord(self, bAll=True):
        self.textedit.clear()
        text = self.addWordTo1.get()
        if text != '':
            res = self.dictwork.get_word(text)
            if not res:
                res = self.dictwork.get_word(text, '2')

            if not res:
                self.textedit.writeln(f"Помилка! Слова '{text}' не знайдено у словнику!")
            else:
                for id, l1Word in res[::-1]:
                    self.textedit.writeln(f"{id}:{l1Word}")
                self.addWordTo1.delete(0, END)
        else:
            self.textedit.writeln("Введіть слово 1")

    def addWord(self):
        self.textedit.clear()
        text1 = self.addWordTo1.get()
        text2 = self.addWordTo2.get()
        if text1 == '' or text2 == '':
            self.textedit.writeln(f"Помилка! Введіть обидва слова!")
            return

        if self.dictwork.set_word(text1, text2) < 0:
            self.textedit.writeln(f"Помилка! Слова '{text1}':'{text2}' не додалися у словник!")
        else:
            self.textedit.writeln(f"Слова '{text1}':'{text2}' додані у словник!")
            self.addWordTo1.delete(0, END)
            self.addWordTo2.delete(0, END)

    def deleteWord(self):
        self.textedit.clear()

        textID = None
        try:
            textID = int(self.delword1.get())
        except:
            self.textedit.writeln(f"Помилка! Введіть числом номер слова!")
            return

        if not self.dictwork.get_wordById(textID) or self.dictwork.del_word(textID) < 0:
            self.textedit.writeln(f"Помилка! Не вдалося видалити слово з номером: '{textID}'!")
        else:
            self.textedit.writeln(f"Cлово з номером: '{textID}' видалено!")
            self.delword1.delete(0, END)

    def deleteAll(self):
        self.textedit.clear()
        MsgBox = messagebox.askquestion("Delete all data", "Ви справді хочете видалити всі дані?")
        if MsgBox == 'yes':
            self.dictwork.droop_all()
            self.textedit.writeln("Cловик видалений!")

    def enter_only_digits(self, entry, action_type):
        if action_type == '1' and not entry.isdigit():
            return False

        return True


app = App()
app.mainloop()






