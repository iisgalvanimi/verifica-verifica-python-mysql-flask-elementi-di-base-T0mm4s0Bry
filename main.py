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


@app.route('/piante', methods=['GET'])
@app.route('/piante/<filtro>/<valore>', methods=['GET'])
@app.route('/piante/<filtro>/<valore_min>/<valore_max>', methods=['GET'])
def get_plants(filtro=None, valore=None, valore_min=None, valore_max=None):
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor(dictionary=True)
        
        query = "SELECT * FROM Piante"
        params = ()

        if filtro and valore and not valore_min and not valore_max:
            if filtro in ['scientific_name', 'common_name', 'type', 'flower_color', 'height']:
                query += f" WHERE {filtro} = %s"
                params = (valore,)

        elif filtro and valore_min and valore_max:
            if filtro in ['height']:  
                query += f" WHERE {filtro} BETWEEN %s AND %s"
                params = (valore_min, valore_max)
        
        cursor.execute(query, params)
        result = cursor.fetchall()
        return jsonify(result)
    
    except Error as e:
        print("Errore nella connessione al database:", e)
        return jsonify({"errore": "Impossibile connettersi al database"}), 500
    
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()

@app.route('/piante/crea', methods=['POST'])
def create_plant():
    data = request.get_json()

    scientific_name = data.get('scientific_name')
    common_name = data.get('common_name')
    type_ = data.get('type')
    flower_color = data.get('flower_color')
    height = data.get('height')

    if not scientific_name or not common_name or not type_ or not flower_color or not height:
        return jsonify({"errore": "Tutti i campi sono obbligatori"}), 400

    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()

        query = "INSERT INTO Piante (scientific_name, common_name, type, flower_color, height) VALUES (%s, %s, %s, %s, %s)"
        cursor.execute(query, (scientific_name, common_name, type_, flower_color, height))
        conn.commit()

        return jsonify({"successo": "Nuova pianta aggiunta", "id": cursor.lastrowid}), 201
    
    except Error as e:
        print("Errore nella connessione al database:", e)
        return jsonify({"errore": "Impossibile inserire la pianta nel database"}), 500
    
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()

@app.route('/piante/aggiorna/<int:id>', methods=['PUT'])
def update_plant(id):
    data = request.get_json()

    scientific_name = data.get('scientific_name')
    common_name = data.get('common_name')
    type_ = data.get('type')
    flower_color = data.get('flower_color')
    height = data.get('height')

    if not scientific_name or not common_name or not type_ or not flower_color or not height:
        return jsonify({"errore": "Tutti i campi sono obbligatori"}), 400

    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()

        query = "UPDATE Piante SET scientific_name = %s, common_name = %s, type = %s, flower_color = %s, height = %s WHERE id = %s"
        cursor.execute(query, (scientific_name, common_name, type_, flower_color, height, id))
        conn.commit()

        if cursor.rowcount == 0:
            return jsonify({"errore": "Pianta non trovata"}), 404

        return jsonify({"successo": "Pianta aggiornata"}), 200
    
    except Error as e:
        print("Errore nella connessione al database:", e)
        return jsonify({"errore": "Impossibile aggiornare la pianta nel database"}), 500
    
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()

@app.route('/piante/elimina/<int:id>', methods=['DELETE'])
def delete_plant(id):
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()

        query = "DELETE FROM Piante WHERE id = %s"
        cursor.execute(query, (id,))
        conn.commit()

        if cursor.rowcount == 0:
            return jsonify({"errore": "Pianta non trovata"}), 404

        return jsonify({"successo": "Pianta eliminata"}), 200
    
    except Error as e:
        print("Errore nella connessione al database:", e)
        return jsonify({"errore": "Impossibile eliminare la pianta nel database"}), 500
    
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()
if __name__ == "__main__":
    app.run() 