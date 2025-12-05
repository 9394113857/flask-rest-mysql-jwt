# init_db.py - one-time initialization script to create tables (no migrations)
# Usage: python init_db.py  (ensure .env is filled)
import sys
from db import get_connection

CREATE_USERS = '''
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100),
    email VARCHAR(150) UNIQUE,
    password_hash VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
'''

CREATE_ITEMS = '''
CREATE TABLE IF NOT EXISTS items (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    title VARCHAR(150),
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);
'''

def main():
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(CREATE_USERS)
        cursor.execute(CREATE_ITEMS)
        conn.commit()
        print('âœ… Tables created (or already exist).')
    except Exception as e:
        conn.rollback()
        print('âŒ Error creating tables:', e)
    finally:
        cursor.close()
        conn.close()

if __name__ == '__main__':
    main()
