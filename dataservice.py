import sqlite3
import csv

# Connect to SQLite database (or create it if it doesn't exist)
conn = sqlite3.connect('database.db')
cursor = conn.cursor()

cursor.execute('DROP TABLE IF EXISTS Rooms')

# Create table with extra fields for roomID and price_pr_night, roomNR and status
cursor.execute('''
    CREATE TABLE IF NOT EXISTS Rooms (
        roomID INTEGER PRIMARY KEY AUTOINCREMENT,
        "Room Type" TEXT,
        "RoomNR" INTEGER,
        "Price pr night" REAL,
        "Status" TEXT
    );
''')

# Read the CSV file and insert data into the table
with open('room_info.csv', 'r', encoding='utf-8') as file:
    csv_reader = csv.DictReader(file, delimiter=',')
    print("CSV Headers:", csv_reader.fieldnames)

    for row in csv_reader:
        print(row)
        
        roomNR = int(row.get('RoomNR', 0)) 
        status = row.get('Status', 'available') if row.get('Status') in ["available", "taken"] else "unknown"
        price_pr_night = float(row.get('Price per Night', 0.0)) 

        # Insert data into the database
        cursor.execute('''
            INSERT INTO Rooms ("Room Type", "RoomNR", "Price pr night", "Status") 
            VALUES (?, ?, ?, ?)
        ''', (
            row['Room Type'].strip(),
            roomNR,
            price_pr_night,
            status
        ))

conn.commit()
conn.close()

print("Data inserted successfully into the Rooms table.")
