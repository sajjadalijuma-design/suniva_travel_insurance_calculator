import bcrypt
from database_functions import connect_database

db_path = r"\DATA\users.db"

def get_user_by_username(username):
    """Retrieve user by username."""
    conn = connect_database(db_path)
    cursor = conn.cursor()
    cursor.execute(
        "SELECT * FROM users WHERE username = ?",
        (username,)
    )
    user = cursor.fetchone()
    conn.close()
    return user

def login_user(username, password):
    """Authenticate user."""
    user = get_user_by_username(username)
    if not user:
        return False, "User not found."
    
    # Verify password
    stored_hash = user[2]  # password_hash column
    if bcrypt.checkpw(password.encode('utf-8'), stored_hash):
        return True, f"Login successful!"
    
    return False, "Incorrect password."