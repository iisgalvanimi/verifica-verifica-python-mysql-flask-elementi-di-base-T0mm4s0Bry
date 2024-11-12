@app.route('/piante/<filtro>/<valore>', methods=['GET'])
def get_filtered_plants(filtro=None, valore=None):
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor(dictionary=True)

        query = "SELECT * FROM Piante WHERE " + filtro + " = %s"
        cursor.execute(query, (valore,))
        result = cursor.fetchall()

        return jsonify(result)
    
    except Error as e:
        print("Errore nella connessione al database:", e)
        return jsonify({"errore": "Impossibile connettersi al database"}), 500
    
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()
