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
    def __init__(self, rootEdit, xx, yy):
        f = Frame(rootEdit)
        f.place(x=xx, y=yy)
        scroll = Scrollbar(f)
        self.textEdit = Text(f, height=20, width=53, borderwidth=3, state='disabled', yscrollcommand=scroll.set)
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

        ORIGINAL_DPI = 96.04726735598227
        self.SCALE = self.winfo_fpixels('1i') / ORIGINAL_DPI
        self.geometry(f'{self.scaled(500)}x{self.scaled(580)}')

        self.dictwork = DictWork("DicEngUkr.sl3")
        self.createWindow()

    def scaled(self, original_width):
        return int(original_width * self.SCALE)

    def enter_only_digits(self, entry, action_type) -> bool:
        if action_type == '1' and not entry.isdigit():
            return False

        return True

    def createWindow(self):
        labelText1 = Label(self, text="Додати слово в словник або знайти слово у словнику")
        labelText1.place(x=self.scaled(30), y=self.scaled(10))

        Label1 = Label(self, text="Слово 1")
        Label2 = Label(self, text="Слово 2")
        Label1.place(x=self.scaled(30), y=self.scaled(50))
        Label2.place(x=self.scaled(30), y=self.scaled(90))

        Label1Del = Label(self, text="Введіть айді слова")
        Label1Del.place(x=self.scaled(30), y=self.scaled(160))

        self.addWordTo1 = Entry(self, width=50)
        self.addWordTo2 = Entry(self, width=50)

        self.addWordTo1.place(x=self.scaled(110), y=self.scaled(50))
        self.addWordTo2.place(x=self.scaled(110), y=self.scaled(90))

        vcmd = (self.register(self.enter_only_digits), '%P', '%d')
        self.delword1 = Entry(self, width=50, validate='key', validatecommand=vcmd)
        self.delword1.place(x=self.scaled(140), y=self.scaled(160))

        self.textedit = TextEdit(self, self.scaled(30), self.scaled(225))

        # buttons
        Button(self, text="Add", width=10, command=self.addWord).place(x=self.scaled(30), y=self.scaled(120))

        Button(self, text="Find", width=10, command=self.getWord).place(x=self.scaled(120), y=self.scaled(120))

        Button(self, text="Delete", width=10, command=self.deleteWord).place(x=self.scaled(30), y=self.scaled(190))

        Button(self, text="Show All", width=10, command=self.showAllWord).place(x=self.scaled(120), y=self.scaled(190))

        Button(self, text="Delete All", width=10, command=self.deleteAll).place(x=self.scaled(380), y=self.scaled(190))

    def showAllWord(self, bAll=True):
        self.textedit.clear()
        res = self.dictwork.get_word("", 'All')
        if self.dictwork.get_word("", 'All'):
            for id, l1Word, l2Word in res[::-1]:
                self.textedit.writeln(f"{id}:{l1Word}:{l2Word}")
        else:
            self.textedit.writeln("Словник пустий!")

    def getWord(self, bAll=True):
        self.addWordTo2.delete(0, END)
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

        try:
            textid = int(self.delword1.get())
        except:
            self.textedit.writeln(f"Помилка! Введіть числом номер слова!")
            return

        if not self.dictwork.get_wordById(textid) or self.dictwork.del_word(textid) < 0:
            self.textedit.writeln(f"Помилка! Не вдалося витерти слово з номером: '{textid}'!")
        else:
            self.textedit.writeln(f"Cлово з номером: '{textid}' видалено!")
            self.delword1.delete(0, END)

    def deleteAll(self):
        self.textedit.clear()
        msg_box = messagebox.askquestion("Delete all data", "Ви справді хочете видалити всі дані?")
        if msg_box == 'yes':
            self.dictwork.droop_all()
            self.textedit.writeln("Cловик видалений!")


app = App()
app.mainloop()
