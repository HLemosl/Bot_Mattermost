import sys
import os
import psycopg2

from auxiliar_database_api import run_api

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from dotenv import load_dotenv
from tools.utils import Logger

class AuxiliarDatabase:
    def __init__(self):
        load_dotenv()
        self.logger = Logger(log_file="auxiliar_database.log")
        run_api()

    def get_db_connection(self):
        try:
            conn = psycopg2.connect(
                host="localhost",
                database=os.getenv("AUX_DB_NAME"),
                user=os.getenv("AUX_DB_USER"),
                password=os.getenv("AUX_DB_PASSWORD")
            )
            return conn
        except Exception as e:
            self.logger.error(f"Error connecting to the database: {e}")
            return None

    def create_database(self):
        try:
            self.logger.info("Creating auxiliar database and table...")
            conn = self.get_db_connection()
            if conn is not None:
                conn.autocommit = True
                cursor = conn.cursor()
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS alerts (
                        id SERIAL PRIMARY KEY,
                        status VARCHAR(50),
                        data JSONB
                    );
                ''')
                self.logger.info("Table 'alerts' created successfully.")
                cursor.close()
                conn.close()
        except Exception as e:
            self.logger.error(f"Error creating auxiliar database: {e}")

if __name__ == "__main__":
    auxiliar_db = AuxiliarDatabase()
    auxiliar_db.create_database()
