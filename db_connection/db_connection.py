
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


class DbClient:

    def __init__(self):
        self.connection = self.get_connection()

    def get_connection(self):
        connection = mysql.connector.connect(**CONFIG)
        return connection

    def get_user(self, username: str):
        cursor = self.connection.cursor()
        cursor.execute(f'SELECT * FROM users WHERE name="{username}";')
        user = cursor.fetchone()
        if not user:
            cursor.close()
            return None

        # if time:
        #     time = user[6].strftime('%Y-%d-%m %H:%M:%S')
        data = {
                "id": user[0],
                "name": user[1],
                "password": user[3],
                "email": user[2],
                "token": user[4],
                }
        print(user)
        cursor.close()
        return data

    def update_user(self, data):
        cursor = self.connection.cursor()
        cursor.execute(f"UPDATE `users` SET {data['field_name']}={data['new_data']} WHERE name='{data['name']}';")
        self.connection.commit()
        cursor.close()
        return 'Successful'

    def insert_user(self, data):
        cursor = self.connection.cursor()
        insert = f"""
                       INSERT INTO users (
                        `name`,
                        `password`,
                        `email`,
                        `token`
                       )
                        VALUES (
                        '{data["name"]}',
                        '{data["password"]}',
                        '{data["email"]}',
                        NULL
                        );
                   """
        cursor.execute(insert)
        self.connection.commit()
        cursor.close()
        return 'Successful'

    def delete_user(self, username):
        cursor = self.connection.cursor()
        cursor.execute(f" DELETE FROM `users` WHERE name='{username}';")
        self.connection.commit()
        cursor.close()
        return 'Successful'


