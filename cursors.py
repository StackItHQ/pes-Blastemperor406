import mysql.connector
import gspread
from google.oauth2.service_account import Credentials


'''MySQL Connection'''
def connect_to_mysql(host, user, password, database):
    connection = mysql.connector.connect(
        host=host,
        user=user,
        password=password,
        database=database
    )
    cursor = connection.cursor()
    return cursor, connection
    

'''Google Sheets Authentication'''
def authenticate_google_sheets(credentials_file, sheet_id):
    scope = ['https://www.googleapis.com/auth/spreadsheets','https://www.googleapis.com/auth/drive']
    credentials =  Credentials.from_service_account_file(credentials_file, scopes=scope)
    client = gspread.authorize(credentials)
    sheet= client.open_by_key(sheet_id)
    return sheet