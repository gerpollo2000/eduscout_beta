import psycopg2
import os

def main(args):
    school_id = args.get("school_id")
    school_name = args.get("school_name", "")

    conn = psycopg2.connect(
        host=os.environ["DB_HOST"],
        port=os.environ["DB_PORT"],
        dbname=os.environ["DB_NAME"],
        user=os.environ["DB_USER"],
        password=os.environ["DB_PASSWORD"],
        sslmode=os.environ.get("DB_SSLMODE", "require")
    )
    cur = conn.cursor()

    if school_id:
        cur.execute(
            "SELECT id, name, email, phone, address, website FROM schools WHERE id = %s",
            (school_id,)
        )
    else:
        cur.execute(
            "SELECT id, name, email, phone, address, website FROM schools WHERE name ILIKE %s LIMIT 5",
            (f"%{school_name}%",)
        )

    rows = cur.fetchall()
    cur.close()
    conn.close()

    if not rows:
        return {"body": {"error": "School not found", "results": []}}

    results = [
        {"id": r[0], "name": r[1], "email": r[2], "phone": r[3], "address": r[4], "website": r[5]}
        for r in rows
    ]
    return {"body": {"results": results}}
