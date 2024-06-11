from flask import Flask, request, jsonify
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)

def get_db_connection():
    connection =  mysql.connector.connect(
        host = "localost",
        user = "root",
        password = "NISHAN@999@11",
        database = "project_2"
    )
    return connection

@app.route('/client/<int:client_id>', methods=['GET'])
def get_clients(client_id):
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM client WHERE client_id = %s", (client_id,))
    client = cursor.fetchone()
    cursor.close
    connection.close()
    if client:
        return jsonify(client)
    else:
        return jsonify({"error": "client not found"}), 404


@app.route('/client', methods=['GET'])
def get_client():
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * from client")
    client = cursor.fetchone()
    cursor.close
    connection.close()
    return jsonify(client)

@app.route('/client/date', methods=['GET'])
def get_client_by_date():
    client_name = request.args.get('name')
    client_address = request.args.get('address')
    client_city = request.args.get('city')
    client_phone = request.args.get('phone')
    client_url = request.args.get('url')
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')

    query = "SELECT * FROM client WHERE 1=1"
    params = []

    if client_name:
        query += "AND name = %s"
        params.append(client_name)
    if client_address:
        query += "AND address = %s"
        params.append(client_address)
    if client_city:
        query += "AND city = %s"
        params.append(client_city)
    if client_url:
        query += "AND url = %s"
        params.append(client_url)
    if client_phone:
        query += "AND phone = %s"
        params.append(client_phone)
    if start_date:
        query += "AND client_date >= %s"
        params.append(start_date)
    if end_date:
        query += "AND client_date <= %s"
        params.append(end_date)

        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)
        cursor.execute(query, params)
        result = cursor.fetchall()
        cursor.close()
        connection.close()
        return jsonify(result)


@app.route('/client', method=['GET'])
def get_client_from_params():
    client_name = request.args.get('client_name')
    client_city = request.args.get('client_city')
    client_address = request.args.get('client_address')
    client_id = request.args.get('client_id')
    client_phone = request.args.get('client_phone')
    client_date = request.args.get('client_date')
    client_url = request.args.get('client_url')

    query = "SELECT client_name, client_city, client_address, client_id, client_phone, client_date, client_url FROM client WHERE 1=1"
    params = []

    if client_name:
        query += "AND client_name = %s"
        params.append(client_name)
    if client_city:
        query += "AND client_city = %s"
        params.append(client_city)
    if client_address:
        query += "AND client_address = %s"
        params.append(client_address)
    if client_id:
        query += "And client_id = %s"
        params.append(client_id)
    if client_phone:
        query += "AND client_phone = %s"
        params.append(client_phone)
    if client_date:
        query += "AND client_date = %s"
        params.append(client_date)
    if client_url:
        query += "AND client_url = %s"
        params.append(client_url)

        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)
        cursor.execute(query, params)
        results =cursor.fetchall()
        cursor.close()
        return jsonify(results)
    
@app.route('/client', method=['POST'])
def add_client():
    new_client = request.json
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("""
    INSERT INTO client (client_name, client_url, client_address, client_city, client_phone, client_date) VALUES (%s, %s, %s, %s, %s, %s)""",
    (
        new_client['client_name'],
        new_client['client_url'],
        new_client['client_address'],
        new_client['client_city'],
        new_client['client_phone'],
        new_client['client_date'] 
    ))
    connection.commit()
    cursor.close()
    connection.close()
    return jsonify({"MESSAGE": "NEW CLIENT ADDED SUCESSFULLY", "ID": cursor.lastrowid}), 201

@app.route('/client/<int:client_id>', methods=['PUT'])
def update_client(client_id):
    update_data = request.json
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("""
        UPDATE client SET  client_url = %s, client_name = %s, client_address = %s, client_city = %s, client_phone = %s, client_date = %s WHERE client_id = %s""",
        (
            update_client['client_url'],
            update_client['client_name'],
            update_client['client_address'],
            update_client['client_city'],
            update_client['client_phone'],
            update_client['client_date'],
            client_id
        ))
    
    connection.commit()
    cursor.close()
    connection.close()
    return jsonify(update_data)

if __name__ == '__main__':
    app.run(debug = True)

    