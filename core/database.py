import sqlite3

class Database:
    def __init__(self):
        self.path = '.tmp/test_db.db'

    def get_db(self):
        self.con = sqlite3.connect(self.path)
        return self.con  # FIXME error processing!

    def query(self, query, one=False):
        con = self.get_db()
        cur = con.cursor().execute(query)
        rv = cur.fetchall()
        cur.close()
        return (rv[0] if rv else None) if one else rv

    def close(self):
        con = self.con
        con.close()
