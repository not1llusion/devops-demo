from fastapi import FastAPI
import psycopg2
import os

app = FastAPI()

def get_db():
    return psycopg2.connect(
            host=os.getenv("DB_HOST", "localhost"),
            database=os.getenv("DB_NAME", "demo"),
            user=os.getenv("DB_USER", "postgres"),
            password=os.getenv("DB_PASSWORD", "password")
        )

@app.get("/api/health")
def health():
    return {"status": "ok"}

@app.get("/api/visits")
def get_visits():
    conn = get_db()
    cur = conn.cursor()
    cur.execute("UPDATE visits SET count = count + 1 RETURNING count")
    count = cur.fetchone()[0]
    conn.commit()
    cur.close()
    conn.close()
    return {"visits": count}

