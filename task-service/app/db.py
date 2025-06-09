import psycopg2
from psycopg2.pool import SimpleConnectionPool
from psycopg2.extensions import connection

db_pool = SimpleConnectionPool(minconn = 1, 
                                    maxconn = 3, 
                                    database = "task-tracker-app",
                                    user = "task-tracker",
                                    host = "task-tracker-db",
                                    password = "task-tracker")

def get_connection() -> connection:
    return db_pool.getconn()

def put_connection(c: connection) -> None:
    db_pool.putconn(c)

def init_db():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id SERIAL PRIMARY KEY,
            task_name TEXT NOT NULL,
            description TEXT NOT NULL,
            status TEXT NOT NULL
        );
    """)
    conn.commit()
    cursor.close()
    conn.close()

def shutdown():
    db_pool.closeall()