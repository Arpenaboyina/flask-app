from flask import Flask, jsonify
import os
import time
import mysql.connector

app = Flask(__name__)

DB_HOST = os.environ.get("MYSQL_HOST", "db")
DB_USER = os.environ.get("MYSQL_USER", "user")
DB_PASS = os.environ.get("MYSQL_PASSWORD", "Rakesh04@")
DB_NAME = os.environ.get("MYSQL_DATABASE", "testdb")

def get_db_connection():
    # retry loop until MySQL is ready
    for _ in range(10):
        try:
            conn = mysql.connector.connect(
                host=DB_HOST,
                user=DB_USER,
                password=DB_PASS,
                database=DB_NAME
            )
            return conn
        except Exception as e:
            print("DB not ready, retrying...", e)
            time.sleep(2)
    raise Exception("Could not connect to database")

@app.route("/")
def index():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS hits (id INT AUTO_INCREMENT PRIMARY KEY, ts TIMESTAMP DEFAULT CURRENT_TIMESTAMP)")
        cursor.execute("INSERT INTO hits () VALUES ()")
        conn.commit()
        cursor.execute("SELECT COUNT(*) FROM hits")
        count = cursor.fetchone()[0]
        cursor.close()
        conn.close()
        return jsonify({"message":"Hello from Flask","hits": count})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
