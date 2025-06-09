import psycopg2

def get_connection():
    return psycopg2.connect(database = "task-tracker-app",
                            user = "task-tracker",
                            host = "task-tracker-db",
                            password = "task-tracker",
                            port = 5432)

def init_db():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id SERIAL PRIMARY KEY,
            task_name TEXT NOT NULL,
            description TEXT NOT NULL
        );
    """)
    conn.commit()
    cursor.close()
    conn.close()