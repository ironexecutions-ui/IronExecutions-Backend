import mysql.connector

def conectar():
    return mysql.connector.connect(
        host="sql5.freesqldatabase.com",
        user="sql5807683",
        password="RKCTBqiFvy",
        database="sql5807683",
        port=3306
    )

def executar_select(query, params=None):
    conn = conectar()
    cursor = conn.cursor(dictionary=True)

    if params:
        cursor.execute(query, params)
    else:
        cursor.execute(query)

    dados = cursor.fetchall()
    cursor.close()
    conn.close()

    return dados

def executar_comando(query, params=None):
    conn = conectar()
    cursor = conn.cursor()

    if params:
        cursor.execute(query, params)
    else:
        cursor.execute(query)

    conn.commit()
    cursor.close()
    conn.close()
