from flask import Flask, jsonify
import psycopg2

app = Flask(__name__)

# Database connection
conn_dw = psycopg2.connect(
    host="localhost",
    port=5433,  # Port for dw-db
    database="dw",
    user="user",
    password="password"
)
cursor_dw = conn_dw.cursor()

@app.route('/starship_sales', methods=['GET'])
def get_starship_sales():
    cursor_dw.execute("SELECT * FROM starship_sales;")
    rows = cursor_dw.fetchall()
    return jsonify(rows)

if __name__ == "__main__":
    app.run(debug=True)
