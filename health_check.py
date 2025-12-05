from db import get_connection
from mysql.connector import Error

def check_database():
    try:
        conn = get_connection()
        cursor = conn.cursor()

        print("🔗 Connected to MySQL successfully.")

        # Check database
        cursor.execute("SELECT DATABASE();")
        current_db = cursor.fetchone()[0]
        print(f"📂 Current database: {current_db}")

        # Check users table
        cursor.execute("""
            SELECT COUNT(*) 
            FROM information_schema.tables 
            WHERE table_schema=%s AND table_name='users'
        """, (current_db,))
        users_exists = cursor.fetchone()[0] == 1

        print("🧾 users table:", "FOUND" if users_exists else "NOT FOUND")

        # Check items table
        cursor.execute("""
            SELECT COUNT(*) 
            FROM information_schema.tables 
            WHERE table_schema=%s AND table_name='items'
        """, (current_db,))
        items_exists = cursor.fetchone()[0] == 1

        print("📦 items table:", "FOUND" if items_exists else "NOT FOUND")

        # If both exist:
        if users_exists and items_exists:
            print("\n✅ Everything looks good. Safe to start the Flask API.")
        else:
            print("\n⚠️ Missing tables — please check your SQL setup.")

    except Error as e:
        print("❌ MySQL Error:", e)

    except Exception as ex:
        print("⚠️ Unexpected Error:", ex)

    finally:
        try:
            cursor.close()
            conn.close()
        except:
            pass

if __name__ == "__main__":
    check_database()
