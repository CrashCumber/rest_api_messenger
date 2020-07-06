
import json
import threading

import mysql.connector
import datetime

CONFIG = {
        'user': 'root',
        'password': '',
        'host': 'localhost',
        'port': '3306',
        'database': 'messenger'
}

class Api():

    def __init__(self, config):
        self.url = config
        # self.connection = self.get_connection()

    # def get_connection(self):
    #     connection = mysql.connector.connect(**CONFIG)
    #     return connection
    #
    # def get_user_from_db(self, username: str):
    #     cursor = self.connection.cursor()
    #     cursor.execute(f'SELECT * FROM test_users WHERE username="{username}";')
    #     user = cursor.fetchone()
    #     if not user:
    #         cursor.close()
    #         return None
    #     cursor.close()
    #     time = user[6]
    #     if time:
    #         time = user[6].strftime('%Y-%d-%m %H:%M:%S')
    #     data = {
    #             "id": user[0],
    #             "username": user[1],
    #             "password": user[2],
    #             "email": user[3],
    #             "access": user[4],
    #             "active": user[5],
    #             "start_active_time": time
    #             }
    #     return data
    #
    # def insert_user_in_db(self, data):
    #     cursor = self.connection.cursor()
    #     insert = f"""
    #                    INSERT INTO `test_users` (
    #                     `username`,
    #                     `password`,
    #                     `email`,
    #                     `access`
    #                     )
    #                     VALUES (
    #                     '{data["username"]}',
    #                     '{data["password"]}',
    #                     '{data["email"]}',
    #                      {data["access"]}
    #                     );
    #                """
    #     cursor.execute(insert)
    #     self.connection.commit()
    #     cursor.close()
    #     return 'Successful'
    #
    # def delete_user_from_db(self, username):
    #     cursor = self.connection.cursor()
    #     cursor.execute(f" DELETE FROM `test_users` WHERE username='{username}';")
    #     self.connection.commit()
    #     cursor.close()
    #     return 'Successful'
    #
    # def delete_users(self):
    #     cursor = self.connection.cursor()
    #     cursor.execute(" DELETE FROM `test_users` WHERE id>1;")
    #     self.connection.commit()
    #     cursor.close()
    #     return 'Successful'
    #
    # def active_user(self, username):
    #     connection = mysql.connector.connect(**CONFIG)
    #     cursor = connection.cursor()
    #     cursor.execute(f"UPDATE `test_users` SET active=1, start_active_time=CURRENT_TIMESTAMP WHERE username='{username}';")
    #     connection.commit()
    #     cursor.close()
    #     return 'Successful'
    #
    # def __del__(self):
    #     self.delete_users()
    #     self.connection.close()
