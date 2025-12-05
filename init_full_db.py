# init_full_db.py
# Creates database + tables automatically (safe to run anytime)

import mysql.connector
from mysql.connector import errorcode
import os
from dotenv import load_dotenv

load_dotenv()

DB_HOST = os.getenv("DB_HOST")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_NAME")

# SQL Table Definitions
CREATE_USERS_TABLE = """
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100),
    email VARCHAR(150) UNIQUE,
    password_hash VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
"""

CREATE_ITEMS_TABLE = """
CREATE TABLE IF NOT EXISTS items (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    title VARCHAR(150),
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);
"""

def create_database(cursor):
    try:
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_NAME}")
        print(f"✅ Database '{DB_NAME}' verified/created.")
    except mysql.connector.Error as err:
        print(f"❌ Failed creating database: {err}")

def main():
    try:
        # Connect without selecting database first
        conn = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD
        )
        cursor = conn.cursor()

        # Step 1: Create DB if missing
        create_database(cursor)

        # Step 2: Select the database
        cursor.execute(f"USE {DB_NAME}")
        print(f"📂 Using database: {DB_NAME}")

        # Step 3: Create tables
        cursor.execute(CREATE_USERS_TABLE)
        cursor.execute(CREATE_ITEMS_TABLE)
        conn.commit()

        print("✅ Tables 'users' and 'items' verified/created successfully.")

    except mysql.connector.Error as err:
        print(f"❌ MySQL Error: {err}")

    finally:
        try:
            cursor.close()
            conn.close()
            print("🔒 Connection closed.")
        except:
            pass

if __name__ == "__main__":
    main()
