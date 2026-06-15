import sqlite3 as sql

conn_obj = sql.connect("python_web.db")

cursor = conn_obj.cursor()

create_users_table = """
CREATE TABLE users (
    user_id INTEGER PRIMARY KEY NOT NULL,
    username TEXT,
    password TEXT
);
"""

create_tasks_table = """
CREATE TABLE tasks (
    task_id INTEGER PRIMARY KEY NOT NULL,
    title TEXT,
    created_at DATETIME,
    is_completed BOOLEAN,
    user_id INTEGER,
    FOREIGN KEY(user_id) REFERENCES users(user_id)
);
"""

try:
    cursor.execute(create_users_table)
    cursor.execute(create_tasks_table)
    conn_obj.commit()
    
    print("Table have been created successfuly!")
    
except sql.Error as error:
    print("Error occured while creating tables: ", error)
    
finally:
    cursor.close()
    conn_obj.close()