import mysql.connector
import pandas as pd
from datetime import date

DB_CONFIG = {
    "host": "localhost",   # Or the IP address of your MySQL server
    "user": "root",
    "password": "Karan09",
    "database": "client_query_management" 
}
def get_connection():
    return mysql.connector.connect(**DB_CONFIG)

def fetchone(query, params=()):
    conn = get_connection()
    conn.autocommit = True
    cur = conn.cursor(dictionary=True,buffered=True)
    cur.execute(query, params)
    row = cur.fetchone()
    cur.close()
    conn.close()
    return row

def fetchall(query, params=()):
    conn = get_connection()
    cur = conn.cursor(dictionary=True)
    cur.execute(query, params)
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return rows

def execute(query, params=()):
    conn = get_connection()
    conn.autocommit = True
    cur = conn.cursor()
    cur.execute(query, params)
    conn.commit()
    lastid = cur.lastrowid
    cur.close()
    conn.close()
    return lastid

def create_user(username, password_hash, role='client'):
    return execute(
        "INSERT INTO users (username, hashed_password, role) VALUES (%s,%s,%s)",
        (username, password_hash, role)
    )

def get_user_by_username(username):
    return fetchone("SELECT * FROM users WHERE username=%s", (username,))

def create_query(mail_id, mobile_number, query_heading, query_description,user_id):
    sql = """
        INSERT INTO client_query (
            mail_id,
            mobile_number,
            query_heading,
            query_description,
            status,
            query_created_date,
            query_closed_date,
            user_id
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """

    params = (mail_id,mobile_number,query_heading,query_description,"Open",date.today(),None,user_id)

    return execute(sql, params)

def get_queries(status=None):
    if status:
        rows = fetchall("SELECT query_id,mail_id,mobile_number,query_heading,query_description,status,query_created_date,query_closed_date,user_id FROM client_query where status=%s ORDER BY query_id DESC",(status,))
    else:
        rows = fetchall("SELECT query_id,mail_id,mobile_number,query_heading,query_description,status,query_created_date,query_closed_date,user_id FROM client_query  ORDER BY query_id DESC")
    return pd.DataFrame(rows)

def get_query(id):
    return fetchone("SELECT query_id,status,query_heading,query_description,user_id FROM client_query where query_id=%s",(id,))

def get_queries_by_customer(customer_id):
    rows = fetchall("SELECT query_id,mail_id,mobile_number,query_heading,query_description,status,query_created_date,query_closed_date,user_id FROM client_query WHERE user_id=%s ORDER BY query_id DESC", (customer_id,))
    return pd.DataFrame(rows)

def close_query(query_id):
    sql = """
        UPDATE client_query SET status = %s, query_closed_date = %s WHERE query_id = %s
    """
    params = ("Closed", date.today(), query_id)
    return execute(sql, params)




