from flask import Flask, render_template, request, redirect, url_for
import mysql.connector
import os

app = Flask(__name__)

def get_db_connection():
    return mysql.connector.connect(
        host=os.environ.get("MYSQL_HOST", "localhost"),
        user=os.environ.get("MYSQL_USER", "root"),
        password=os.environ.get("MYSQL_PASSWORD", "root"),
        database=os.environ.get("MYSQL_DB", "assetdb")
    )

@app.route("/")
def index():
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM assets ORDER BY id DESC")
        assets = cursor.fetchall()
        cursor.close()
        conn.close()
    except Exception as e:
        assets = []
    return render_template("index.html", assets=assets)

@app.route("/add", methods=["POST"])
def add_asset():
    name = request.form["name"]
    asset_type = request.form["asset_type"]
    serial = request.form["serial"]
    assigned_to = request.form["assigned_to"]
    status = request.form["status"]

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO assets (name, asset_type, serial, assigned_to, status) VALUES (%s, %s, %s, %s, %s)",
        (name, asset_type, serial, assigned_to, status)
    )
    conn.commit()
    cursor.close()
    conn.close()
    return redirect(url_for("index"))

@app.route("/delete/<int:asset_id>")
def delete_asset(asset_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM assets WHERE id = %s", (asset_id,))
    conn.commit()
    cursor.close()
    conn.close()
    return redirect(url_for("index"))

@app.route("/health")
def health():
    return "OK", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000, debug=True)