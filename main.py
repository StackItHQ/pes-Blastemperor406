import cursors
import os
import dotenv
import sync
import time
dotenv.load_dotenv(dotenv_path='variables.env')


def bi_directional_sync(sheet, cursor, conn, interval=10):
    while True:
        print("Syncing from Google Sheets to MySQL...")
        sync.sync_google_to_mysql(sheet, cursor, conn)
        
        print("Syncing from MySQL to Google Sheets...")
        sync.sync_mysql_to_google(sheet, cursor)
        
        print(f"Sync completed. Waiting for {interval} seconds before next sync.")
        time.sleep(interval)  # Wait for the next sync cycle

# 7. Main Execution

if __name__ == "__main__":
    # Initialize Google Sheets and MySQL connections
    print("Initializing Google Sheets API...")
    cursor,connection=cursors.connect_to_mysql(os.getenv('HOST'), os.getenv('USER'), os.getenv('PASSWORD'), os.getenv('DATABASE'))
    sheet=cursors.authenticate_google_sheets('Credentials.json', os.getenv('SHEET_ID'))

    try:
        # Start bi-directional sync
        bi_directional_sync(sheet, cursor, connection, interval=10)
    except KeyboardInterrupt:
        print("Sync process interrupted by user.")
    finally:
        cursor.close()
        connection.close()
        print("MySQL connection closed.")


