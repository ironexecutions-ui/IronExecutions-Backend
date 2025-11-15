import mysql.connector

def conectar():
    return mysql.connector.connect(
        host="sql5.freesqldatabase.com",
        user="sql5807683",
        password="RKCTBqiFvy",
        database="sql5807683",
        port=3306
    )
