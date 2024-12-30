import psycopg2
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Database connection parameters
DB_HOST = os.getenv('DB_HOST', 'localhost')
DB_PORT = os.getenv('DB_PORT', '5432')
DB_NAME = os.getenv('DB_NAME', 'geescan')
DB_USER = os.getenv('DB_USER', 'postgres')
DB_PASSWORD = os.getenv('DB_PASSWORD', '')

def get_db_connection():
    """Create a database connection."""
    try:
        conn = psycopg2.connect(
            host=DB_HOST,
            port=DB_PORT,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD
        )
        return conn
    except Exception as e:
        print(f"Error connecting to database: {e}")
        return None

def run_migration():
    conn = get_db_connection()
    if conn is not None:
        try:
            with conn.cursor() as cur:
                # Add default timestamps
                cur.execute("""
                    ALTER TABLE aois 
                    ALTER COLUMN created_at SET DEFAULT CURRENT_TIMESTAMP,
                    ALTER COLUMN updated_at SET DEFAULT CURRENT_TIMESTAMP;
                """)
                conn.commit()
                print("Successfully added timestamp defaults")
        except psycopg2.Error as e:
            print(f"Error running migration: {e}")
            conn.rollback()
        finally:
            conn.close()

if __name__ == "__main__":
    run_migration()
