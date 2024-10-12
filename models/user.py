import mysql.connector
from config import db_config

class User:
    @staticmethod
    def authenticate(username, password):
        try:
            conn = mysql.connector.connect(**db_config)
            cursor = conn.cursor()
            query = "SELECT * FROM users WHERE username = %s AND password = %s"
            cursor.execute(query, (username, password))
            user = cursor.fetchone()
            cursor.close()
            conn.close()
            return user
        except mysql.connector.Error as err:
            print("Error:", err)
            return None
