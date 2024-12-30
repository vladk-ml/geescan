import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()

def get_db_connection():
    """Establishes a connection to the PostgreSQL database."""
    conn = None
    try:
        conn = psycopg2.connect(
            host=os.environ.get("DB_HOST"),
            port=os.environ.get("DB_PORT"),
            database=os.environ.get("DB_NAME"),
            user=os.environ.get("DB_USER"),
            password=os.environ.get("DB_PASSWORD")
        )
        print("Database connection successful") # Debugging
    except psycopg2.Error as e:
        print(f"Error connecting to database: {e}")
    finally:
        if conn is not None:
            print("Connection is not none, testing fetch")
            try:
                with conn.cursor() as cur:
                    cur.execute("SELECT * FROM aois")
                    result = cur.fetchall()
                    print(result)
                    print("Connection test: OK")
            except:
                print("Failed test fetch")
    return conn

def create_aoi(name, geometry, description=None):
    """Inserts a new AOI into the database."""
    print(f"create_aoi called with name: {name}, geometry: {geometry}") # Debugging
    conn = get_db_connection()
    if conn is not None:
        try:
            with conn.cursor() as cur:
                print("Executing query") # Debugging
                cur.execute(
                    """
                    INSERT INTO aois (name, geometry, description) 
                    VALUES (%s, ST_GeomFromGeoJSON(%s)::geography, %s) 
                    RETURNING id
                    """,
                    (name, geometry, description)
                )
                print("Query executed") # Debugging
                aoi_id = cur.fetchone()[0]
                conn.commit()
                print(f"Successfully created AOI with ID: {aoi_id}")
                return aoi_id
        except psycopg2.Error as e:
            print(f"Error creating AOI: {e}")
            conn.rollback()
            return None
        finally:
            conn.close()
    else:
        print("Failed to establish database connection.")
        return None

def get_aois():
    """Retrieves all AOIs from the database."""
    conn = get_db_connection()
    aois = []
    if conn is not None:
        try:
            with conn.cursor() as cur:
                cur.execute("""
                    SELECT id, name, description, ST_AsGeoJSON(geometry) as geometry,
                           created_at, updated_at
                    FROM aois
                    ORDER BY created_at DESC
                """)
                rows = cur.fetchall()
                for row in rows:
                    aois.append({
                        'id': row[0],
                        'name': row[1],
                        'description': row[2],
                        'geometry': row[3],
                        'created_at': row[4].isoformat() if row[4] else None,
                        'updated_at': row[5].isoformat() if row[5] else None
                    })
        except psycopg2.Error as e:
            print(f"Error getting AOIs: {e}")
            return None
        finally:
            conn.close()
    return aois

def get_aoi(aoi_id):
    """Retrieves a specific AOI by its ID."""
    conn = get_db_connection()
    if conn is not None:
        try:
            with conn.cursor() as cur:
                cur.execute("""
                    SELECT id, name, description, ST_AsGeoJSON(geometry) as geometry,
                           created_at, updated_at
                    FROM aois 
                    WHERE id = %s
                """, (aoi_id,))
                row = cur.fetchone()
                if row:
                    return {
                        'id': row[0],
                        'name': row[1],
                        'description': row[2],
                        'geometry': row[3],
                        'created_at': row[4].isoformat() if row[4] else None,
                        'updated_at': row[5].isoformat() if row[5] else None
                    }
                else:
                    return None
        except psycopg2.Error as e:
            print(f"Error getting AOI: {e}")
            return None
        finally:
            conn.close()
    return None

def update_aoi(aoi_id, name, geometry, description=None):
    """Updates an existing AOI in the database."""
    conn = get_db_connection()
    if conn is not None:
        try:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    UPDATE aois 
                    SET name = %s, geometry = ST_GeomFromGeoJSON(%s)::geography, 
                        description = %s, updated_at = CURRENT_TIMESTAMP
                    WHERE id = %s
                    """,
                    (name, geometry, description, aoi_id)
                )
                conn.commit()
                return True
        except psycopg2.Error as e:
            print(f"Error updating AOI: {e}")
            return False
        finally:
            conn.close()

def delete_aoi(aoi_id):
    """Deletes an AOI from the database."""
    conn = get_db_connection()
    if conn is not None:
        try:
            with conn.cursor() as cur:
                cur.execute("DELETE FROM aois WHERE id = %s", (aoi_id,))
                conn.commit()
                return True
        except psycopg2.Error as e:
            print(f"Error deleting AOI: {e}")
            return False
        finally:
            conn.close()