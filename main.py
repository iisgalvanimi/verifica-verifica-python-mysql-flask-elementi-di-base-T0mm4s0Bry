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
