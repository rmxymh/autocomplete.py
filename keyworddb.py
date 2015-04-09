#!/usr/bin/env python3
import sqlite3
import traceback
import os

class KeywordBase:
    def __init__(self, dbfile):
        self.dbfile = dbfile
        self.conn = None
        self.reopen()

    def reopen(self):
        newdb = not os.path.exists(self.dbfile)
        if self.conn == None:
            self.conn = sqlite3.connect(self.dbfile)
            if newdb:
                c = self.conn.cursor()
                c.execute('''
                    CREATE TABLE KeywordBase (
                        word TEXT PRIMARY KEY,
                        access_count INT DEFAULT 0
                    );
                ''')
                self.conn.commit()
            
    def get_word_list(self, word, limit = 20):
        self.reopen()
        try:
            c = self.conn.cursor()
            c.execute("SELECT * FROM KeywordBase WHERE word LIKE ? ORDER BY access_count DESC LIMIT ?", ('%%%s%%' %(word), limit,))
            print(c.fetchall())
        except:
            self.conn.rollback()
            print("NONE")
    
    def close(self):
        if self.conn != None:
            self.conn.close()
            self.conn = None
            
    def inc_query(self, word):
        self.reopen()
        try:
            c = self.conn.cursor()
            
            # check whether the word exists first
            c.execute("SELECT * FROM KeywordBase WHERE word LIKE ?", (word, ))
            data = c.fetchall()
            
            if len(data) == 0:
                # no data here, insert one
                c = self.conn.cursor()
                c.execute("INSERT INTO KeywordBase VALUES (?, 1)", (word, ))
                self.conn.commit()
            else:
                count = data[0][1]
                c = self.conn.cursor()
                c.execute("UPDATE KeywordBase SET access_count = ? WHERE word LIKE ?", (count+1, word, ))
                self.conn.commit()
        except:
            print(traceback.format_exc())
            print("NONE")
            self.conn.rollback()

    def moc_data_init(self):
        data = [('test', 400),
                ('testcase', 20),
                ('execute', 10),
                ('C++', 10),
                ('share', 20),
                ('linux', 20),
               ]
        self.reopen()
        try:
            c = self.conn.cursor()
            c.executemany("INSERT INTO KeywordBase VALUES(?, ?)", data)
            self.conn.commit()
        except:
            self.conn.rollback()


if __name__ == "__main__":
    db = KeywordBase("keyword.db")
    db.mock_data_init()
    db.get_word_list("test")
    db.inc_query("abc")
    db.inc_query("test")
    db.get_word_list("")
    db.close()