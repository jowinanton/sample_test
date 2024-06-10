from flask import Flask, request, jsonify
import mysql.connector

app = Flask(__name__)

# Database connection
def get_db_connection():
    return mysql.connector.connect(
        host='localhost',
        user='root',
        password='JO03@in!w',
        database='test'
    )

# Route to fetch all clients
@app.route('/client', methods=['GET'])
def get_clients():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute('SELECT * FROM client')
    client = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(client)

# Route to fetch a single client by ID
@app.route('/client/<int:client_id>', methods=['GET'])
def get_client(client_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute('SELECT * FROM client WHERE client_id = %s', (client_id,))
    client = cursor.fetchone()
    cursor.close()
    conn.close()
    if client:
        return jsonify(client)
    else:
        return jsonify({'error': 'Client not found'}), 404

# Route to create a new client
@app.route('/client', methods=['POST'])
def create_client():
    new_client = request.get_json()
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO client (client_url, client_name, client_address, client_city, client_phone, client_date) VALUES (%s, %s, %s, %s, %s, %s)',
                   (new_client['client_url'], new_client['client_name'], new_client['client_address'], new_client['client_city'], new_client['client_phone'], new_client['client_date']))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({'message': 'Client created successfully'}), 201

# Route to update an existing client
@app.route('/client/<int:client_id>', methods=['PUT'])
def update_client(client_id):
    updated_client = request.get_json()
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('UPDATE client SET client_url = %s, client_name = %s, client_address = %s, client_city = %s, client_phone = %s, client_date = %s WHERE client_id = %s',
                   (updated_client['client_url'], updated_client['client_name'], updated_client['client_address'], updated_client['client_city'], updated_client['client_phone'], updated_client['client_date'], client_id))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({'message': 'Client updated successfully'})

if __name__ == '__main__':
    app.run(debug=True)
