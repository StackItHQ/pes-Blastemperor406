from datetime import datetime
def sync_google_to_mysql(sheet, cursor, conn):
    # Fetch all rows from Google Sheets
    records = sheet.get_worksheet(0).get_all_records()
    
    for record in records:
        last_modified_google = datetime.strptime(record['last_modified'], '%m/%d/%Y %H:%M:%S')

        query = """
        INSERT INTO cars (id, Name ,color, model, last_modified) 
        VALUES (%s, %s , %s, %s, %s) 
        ON DUPLICATE KEY UPDATE 
            Name=VALUES(Name),
            color = VALUES(color), 
            model = VALUES(model),
            last_modified = VALUES(last_modified)
        """
        data = (record['id'], record['Name'], record['Color'], record['Model'], last_modified_google)
        cursor.execute(query, data)
        conn.commit()

def sync_mysql_to_google(sheet, cursor):
    cursor.execute("SELECT id, Name, Color, Model, last_modified FROM cars")
    records = cursor.fetchall()

    # Convert MySQL records to Google Sheets format, including the timestamp
    for i, row in enumerate(records, start=2):  # Assuming first row is headers
        # Update Google Sheet row
        sheet.get_worksheet(0).update(f'A{i}', [[row[0], row[1], row[2], row[3], row[4].strftime('%m/%d/%Y %H:%M:%S')]])

def resolve_conflict(record_from_google, record_from_mysql):
    last_modified_google = datetime.strptime(record_from_google['last_modified'], '%m/%d/%Y %H:%M:%S')
    last_modified_mysql = record_from_mysql['last_modified']

    if last_modified_google > last_modified_mysql:
        return 'google'
    else:
        return 'mysql'
