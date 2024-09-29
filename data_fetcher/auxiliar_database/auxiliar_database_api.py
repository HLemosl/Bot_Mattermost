from flask import Flask, request, jsonify
from dotenv import load_dotenv
import os
import psycopg2
import json

app = Flask(__name__)

def get_db_connection():
    conn = psycopg2.connect(
        host="localhost",
        database=os.getenv("AUX_DB_NAME"),
        user=os.getenv("AUX_DB_USER"),
        password=os.getenv("AUX_DB_PASSWORD")
    )
    return conn

@app.route('/api/alerts', methods=['GET'])
def get_alerts():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM alerts;")
        rows = cursor.fetchall()
        
        cursor.close()
        conn.close()

        result = []
        column_names = [desc[0] for desc in cursor.description]
        for row in rows:
            result.append(dict(zip(column_names, row)))

        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/alerts', methods=['POST'])
def create_alert():
    data = request.json
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO alerts (status, data) VALUES (%s, %s) RETURNING id;", (data['status'], json.dumps(data['data'])))
        alert_id = cursor.fetchone()[0]
        conn.commit()

        cursor.close()
        conn.close()
        
        return jsonify({"id": alert_id}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/alerts/<int:alert_id>', methods=['PUT'])
def update_alert(alert_id):
    updated_data = request.json
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE alerts SET status = %s, data = %s WHERE id = %s;", (updated_data['status'], json.dumps(updated_data['data']), alert_id))
        conn.commit()
        
        cursor.close()
        conn.close()

        return jsonify({"message": f"Alert {alert_id} updated successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def run_api():
    load_dotenv()
    app.run(host='0.0.0.0', port=5001, debug=True)

if __name__ == "__main__":
    run_api()
