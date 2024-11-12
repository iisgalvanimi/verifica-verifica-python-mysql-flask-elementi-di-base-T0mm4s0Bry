import mysql.connector
from mysql.connector import Error

try:
    conn = mysql.connector.connect(
        host="localhost",
        user="root", 
        password="",  
    )

    if conn.is_connected():
        cursor = conn.cursor()
  
        cursor.execute("CREATE DATABASE PianteGiardino")
        print("Database creato o già esistente.")

       
        conn.database = "PianteGiardino"

       
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS Piante (
            id INT AUTO_INCREMENT PRIMARY KEY,
            scientific_name VARCHAR(100) NOT NULL,
            common_name VARCHAR(100) NOT NULL,
            type VARCHAR(50) NOT NULL,
            flower_color VARCHAR(50) NOT NULL,
            height VARCHAR(20) NOT NULL
        )
        """)
        print("Tabella 'Piante' creata o già esistente.")

    conn.commit()

except Error as e:
    print(f"Errore: {e}")

finally:
    if conn.is_connected():
        cursor.close()
        conn.close()
