import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv
import os

load_dotenv()

DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_NAME")


# SQL for tables
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


def ensure_database():
    """Create database if it doesn't exist."""
    try:
        conn = mysql.connector.connect(
            host=DB_HOST,
            port=DB_PORT,
            user=DB_USER,
            password=DB_PASSWORD
        )
        cursor = conn.cursor()

        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_NAME};")
        print(f"📦 Database checked/created: {DB_NAME}")

    except Error as e:
        print("❌ Error creating database:", e)
    finally:
        cursor.close()
        conn.close()


def ensure_tables():
    """Create tables if they don't exist."""
    try:
        conn = mysql.connector.connect(
            host=DB_HOST,
            port=DB_PORT,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME
        )
        cursor = conn.cursor()

        cursor.execute(CREATE_USERS)
        cursor.execute(CREATE_ITEMS)
        conn.commit()

        print("🧱 Tables checked/created: users, items")

    except Error as e:
        print("❌ Error creating tables:", e)
    finally:
        cursor.close()
        conn.close()


if __name__ == "__main__":
    print("🔧 Starting database setup...")
    ensure_database()
    ensure_tables()
    print("✅ Database & tables ready!")
