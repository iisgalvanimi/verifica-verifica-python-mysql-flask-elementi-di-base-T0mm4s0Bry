from flask import Flask, jsonify, request
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)

db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': 'PianteGiardino'
}

def initialize_database():
    try:

        conn = mysql.connector.connect(host='localhost', user='root', password='')
        cursor = conn.cursor()

        cursor.execute("CREATE DATABASE IF NOT EXISTS PianteGiardino")
        conn.commit()

        conn.close()
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()

        create_table_query = """
        CREATE TABLE IF NOT EXISTS Piante (
            id INT AUTO_INCREMENT PRIMARY KEY,
            scientific_name VARCHAR(255),
            common_name VARCHAR(255),
            type VARCHAR(255),
            flower_color VARCHAR(255),
            height FLOAT
        )
        """
        cursor.execute(create_table_query)
        conn.commit()

        insert_data_query = """
        INSERT INTO Piante (scientific_name, common_name, type, flower_color, height)
        VALUES
        ('Rosa indica', 'Rosa', 'Fiore', 'Rosso', 1.5),
        ('Tulipa gesneriana', 'Tulipano', 'Fiore', 'Giallo', 0.6)
        """
        cursor.execute(insert_data_query)
        conn.commit()

        print("Tabella e dati caricati con successo!")

    except Error as e:
        print(f"Errore nella connessione al database: {e}")

    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()


initialize_database()

