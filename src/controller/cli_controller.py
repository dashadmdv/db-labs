import sys

from src.storage.database import Database


class CLIController:
    def __init__(self):
        try:
            db = Database()
        except Exception as e:
            print(f'Unable to connect!\n{e}')
            sys.exit()
        else:
            self.db = db

    def close_database(self):
        self.db.close()
