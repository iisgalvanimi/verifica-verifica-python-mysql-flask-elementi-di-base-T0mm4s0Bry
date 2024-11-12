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
