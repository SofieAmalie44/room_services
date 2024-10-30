import sqlite3
import json

############   Database connection function   ##########

def get_db_connection():
    # Connect to the SQLite database
    conn = sqlite3.connect('database.db')
    return conn

############   Fetch room data   ##########

def fetch_rooms():
    conn = get_db_connection()
    cursor = conn.cursor()

    # Execute a query to fetch all records from the Rooms table
    cursor.execute("SELECT * FROM Rooms")
    rows = cursor.fetchall()

    # Fetch column names to use as keys
    column_names = [description[0] for description in cursor.description]

    # Convert the data into a list of dictionaries
    rooms = [dict(zip(column_names, row)) for row in rows]

    # Close the database connection
    conn.close()

    return rooms

# Fetch and print the filtered room data
rooms_data = fetch_rooms()
# print(json.dumps(rooms_data, indent=4))


############   Create new room data   ##########

def create_room(data):
    room_type = data.get("Room Type")
    roomNR = data.get("RoomNR")
    price_pr_night = data.get("Price pr night", 0.0) 
    status = data.get("Status")

    # Verify the required fields
    if not room_type or price_pr_night == 0.0:
        return {"error": "Room type and price per night are required fields"}, 400

    # Insert data into database
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO Rooms ([Room Type], RoomNR, [Price pr night], Status) VALUES (?, ?, ?, ?)",
        (room_type, roomNR, price_pr_night, status)
    )
    conn.commit()
    room_id = cursor.lastrowid
    conn.close()

    # Return the newly created room ID as confirmation
    return {"message": "Room created successfully", "roomID": room_id}, 201


############   Update room data   ##########

def update_room(room_id, data):
    room_type = data.get("Room Type")
    roonNR = data.get("RoomNR")
    price_pr_night = data.get("Price pr night", 0.0)
    status = data.get("Status")

    if not room_type or price_pr_night == 0.0:
        return {"error": "Room type and price per night are required fields"}, 400

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE Rooms 
        SET [Room Type] = ?, RoomNR = ?, [Price pr night] = ?, Status = ?
        WHERE roomID = ?
        ''', 
        (room_type, roonNR, price_pr_night, room_id, status)
    )
    conn.commit()
    updated_rows = cursor.rowcount
    conn.close()

    if updated_rows == 0:
        return {"error": "Room not found"}, 404

    return {"message": "Room updated successfully"}, 200


############   Delete room data   ##########

def delete_room(room_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        'DELETE FROM Rooms WHERE roomID = ?',
        (room_id,)
    )
    conn.commit()
    deleted_rows = cursor.rowcount
    conn.close()

    if deleted_rows == 0:
        return {"error": "Room not found"}, 404

    return {"message": "Room deleted successfully"}, 200
