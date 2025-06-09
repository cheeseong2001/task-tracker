import psycopg2
from psycopg2.pool import SimpleConnectionPool
from psycopg2.extensions import connection
from contextlib import contextmanager

db_pool = SimpleConnectionPool(minconn = 1, 
                                    maxconn = 3, 
                                    database = "task-tracker-app",
                                    user = "task-tracker",
                                    host = "task-tracker-db",
                                    password = "task-tracker")

@contextmanager
def get_db_cursor():
    conn: connection | None = None
    try:
        conn = db_pool.getconn()
        if conn:
            cursor = conn.cursor()
            yield cursor
            conn.commit()
            cursor.close()
    finally:
        if conn:
            db_pool.putconn(conn)

def init_db():
    with get_db_cursor() as cursor:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS tasks (
                id SERIAL PRIMARY KEY,
                task_name TEXT NOT NULL,
                description TEXT NOT NULL,
                status TEXT NOT NULL
            );
        """)

def shutdown():
    db_pool.closeall()