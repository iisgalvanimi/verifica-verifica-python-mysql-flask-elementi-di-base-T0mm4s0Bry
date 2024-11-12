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

