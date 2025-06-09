import pyodbc

def get_db_connection():
    conn = pyodbc.connect(
        'Driver={SQL Server};'
        'Server=#put your credentials here
        'Database=model;'
        'Trusted_Connection=yes;'
    )
    return conn

def execute_query(query, params=None):
    conn = get_db_connection()
    cursor = conn.cursor()
    if params:
        cursor.execute(query, params)
    else:
        cursor.execute(query)
    conn.commit()
    cursor.close()
    conn.close()
