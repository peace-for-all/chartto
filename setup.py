# TODO install requirements in virtualenv and roll out the app
from core.database import Database
import os


class Setup:
    def __init__(self):
        self.structure_dir = "db_structure"

    def create_tables(self):
        self.db = Database()
        for f in self.structure_dir:  # TODO check
            sql_path = os.path.join(self.structure_dir, f)
            sql = open(sql_path, 'r').read()
            result = self.db.query(sql)
            if not result:
                return False
        return True

if __name__ == '__main__':
    s = Setup()
    s.create_tables()