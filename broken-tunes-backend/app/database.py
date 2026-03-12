import os
import mysql.connector
from mysql.connector.connection import MySQLConnection

from dotenv import load_dotenv
load_dotenv()


def get_db() -> MySQLConnection:
    try:
      return mysql.connector.connect(
            host=os.getenv('DB_HOST', '127.0.0.1'),
            user=os.getenv('DB_USER', 'root'),
            password=os.getenv('DB_PASS', '12345'),
            database=os.getenv('DB_NAME', 'broken_tunes2')
        )
    except mysql.connector.Error as e:
        print(f"Error connecting to MySQL: {e}")
        raise
