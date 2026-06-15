import psycopg2 as psql
from psycopg2 import sql

dbname = "postgres"
user = "postgres"
password = "123456"
host = "localhost"
port = "5432"

create_users_table = """
CREATE TABLE users (
    user_id SERIAL PRIMARY KEY,
    username TEXT,
    password TEXT
);
"""

create_tasks_table = """
CREATE TABLE tasks (
    task_is SERIAL PRIMARY KEY,
    title TEXT,
    created_at TIMESTAMP,
    is_completed BOOLEAN,
    user_id INTEGER,
    FOREIGN KEY(user_id) REFERENCES users(user_id)
);
"""

conn = psql.connect(dbname=dbname, user=user, password=password, host=host, port=port)
cursor = conn.cursor()

try:
    cursor.execute(create_users_table)
    cursor.execute(create_tasks_table)
    conn.commit()
    
    print("Table have been created successfuly!")
    
except Exception as e:
    print("Error occured while creating tables: ", e)
    conn.rollback()
    
finally:
    cursor.close()
    conn.close()