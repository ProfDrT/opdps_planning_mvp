import sqlite3

class Database:
    def __init__(self, db_name='opdps.db'):
        self.db_name = db_name

    def connect(self):
        return sqlite3.connect(self.db_name)

    def create_tables(self):
        conn = self.connect()
        cursor = conn.cursor()

        # Create tables: staff, patients, equipment, schedules
        # TODO: Implement table creation SQL statements

        conn.commit()
        conn.close()

    # TODO: Add methods for CRUD operations on each table