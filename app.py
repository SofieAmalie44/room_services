"""
Room Service:
Styrer listen over værelser, inklusive detaljer såsom type, kontak info og loyalitets point.
Tilbyder funktionalitet til at søge, filtrere, updatere og slette gæster.
"""
from flask import Flask, jsonify, request
from services.rooms import fetch_rooms
from services.rooms import create_room
from services.rooms import update_room
from services.rooms import delete_room

app = Flask(__name__)


########### CRUD method GET ############

@app.route('/rooms', methods=['GET'])
def get_all_rooms():
    rooms = fetch_rooms()
    return jsonify(rooms)

@app.route('/rooms/<int:id>', methods=['GET'])
def get_room(id):
    rooms = fetch_rooms()
    
    return jsonify([room for room in rooms if room['roomID'] == id])

# Søg efter gæster på efternavn
@app.route('/rooms/search', methods=['GET'])
def search_room():
    query = request.args.get('room_type', '').lower()
    rooms = fetch_rooms()
    
    filtered_rooms = [room for room in rooms if query in room['room_type'].lower()]
    return jsonify(filtered_rooms)

@app.route('/room/price/<type>', methods=['GET'])
def get_price_by_room(type):
    rooms = fetch_rooms()
    
    filtered_rooms = [room for room in rooms if room['room_type'] == type]
    return jsonify(filtered_rooms)


########### CRUD method POST ############

@app.route('/rooms', methods=['POST'])
def add_rooms():
    data = request.get_json()
    if not data:
        return jsonify({"error": "Invalid json data"}), 400
    
    result, status_code = create_room(data)
    return jsonify(result), status_code


########### CRUD method POST ############

@app.route('/rooms/<int:room_id>', methods=['PUT'])
def modify_room(room_id):
    data = request.get_json()
    if not data:
        return jsonify({"error": "Invalid json data"}), 400
    
    result, status_code = update_room(room_id, data)
    return jsonify(result), status_code


########### CRUD method DELETE ############

@app.route('/rooms/<int:room_id>', methods=['DELETE'])
def remove_room(room_id):
    result, status_code = delete_room(room_id)
    return jsonify(result), status_code


if __name__ == '__main__':
    app.run(debug=True)

app.run(host='0.0.0.0', port=5004)