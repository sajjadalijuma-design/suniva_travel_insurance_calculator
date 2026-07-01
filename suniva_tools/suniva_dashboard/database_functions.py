import sqlite3
import bcrypt
import os

db_folder = "DATA"
db_file = "users.db"
db_path = os.path.join(db_folder, db_file)

# Make sure the folder exists
os.makedirs(db_folder, exist_ok=True)

print(f"Database path: {os.path.abspath(db_path)}")

def connect_database(db_path):
    """
    Connect to the SQLite database.
    """
    sqlite3.connect(str(db_path))
    return sqlite3.connect(str(db_path))

def create_users_table(db_path):
    """
    Create the users table if it doesn't exist.
    """
    conn = connect_database(db_path)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

    print(f"Users table created in {db_path}.")

def add_user(db_path, username, password):
    """
    Add a new user with a bcrypt-hashed password.
    """
    password_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
    conn = connect_database(db_path)
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO users (username, password_hash) VALUES (?, ?)",
            (username, password_hash)
        )
        conn.commit()
    except sqlite3.IntegrityError:
        print(f"Username '{username}' already exists.")
    finally:
        conn.close()

add_user(db_path, "admin", "admin1234")