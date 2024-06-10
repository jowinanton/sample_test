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
@app.route('/partner', methods=['GET'])
def get_partners():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute('SELECT * FROM partner')
    client = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(client)

# Route to fetch a single client by ID
@app.route('/partner/<int:partner_id>', methods=['GET'])
def get_client(partner_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute('SELECT * FROM partner WHERE partner_id = %s', (partner_id,))
    partner = cursor.fetchone()
    cursor.close()
    conn.close()
    if partner:
        return jsonify(partner)
    else:
        return jsonify({'error': 'partner not found'}), 404

# Route to create a new client
@app.route('/partner', methods=['POST'])
def create_partner():
    new_partner = request.get_json()
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO partner (partner_url, partner_name, partner_address, partner_city, partner_phone, partner_date) VALUES (%s, %s, %s, %s, %s, %s)',
                   (new_partner['partner_url'], new_partner['partner_name'], new_partner['partner_address'], new_partner['partner_city'], new_partner['partner_phone'], new_partner['partner_date']))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({'message': 'partner created successfully'}), 201

# Route to update an existing client
@app.route('/partner/<int:partner_id>', methods=['PUT'])
def update_partner(partner_id):
    updated_partner = request.get_json()
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('UPDATE partner SET partner_url = %s, partner_name = %s, partner_address = %s, partner_city = %s, partner_phone = %s, partner_date = %s WHERE partner_id = %s',
                   (updated_partner['partner_url'], updated_partner['partner_name'], updated_partner['partner_address'], updated_partner['partner_city'], updated_partner['partner_phone'], updated_partner['partner_date'], partner_id))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({'message': 'Client updated successfully'})

if __name__ == '__main__':
    app.run(debug=True)
