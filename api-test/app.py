from flask import Flask, request, jsonify
import mysql.connector

app = Flask(__name__)

def get_db_connection():
    conn = mysql.connector.connect(
        host="localhost", 
        user="admin",
        password="db4dev",
        database="db4dev"
    )
    return conn

@app.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO USERS (name, age) VALUES (%s, %s)", (data['name'], data['age']))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({"message": "User created!"}), 201

@app.route('/users', methods=['GET'])
def get_users():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM USERS")
    users = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(users)

@app.route('/users/<int:uid>', methods=['PUT'])
def update_user(uid):
    data = request.get_json()
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE USERS SET name = %s, age = %s WHERE uid = %s", (data['name'], data['age'], uid))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({"message": "User updated!"})

@app.route('/users/<int:uid>', methods=['DELETE'])
def delete_user(uid):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM USERS WHERE uid = %s", (uid,))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({"message": "User deleted!"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8081)
