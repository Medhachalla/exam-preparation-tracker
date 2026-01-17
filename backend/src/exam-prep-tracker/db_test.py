from db import get_connection

print("CONNECTING TO DATABASE")

conn = get_connection()
print("CONNECTED")

cur = conn.cursor()
cur.execute("SELECT COUNT(*) FROM subjects;")
count = cur.fetchone()[0]

print("SUBJECT COUNT:", count)

cur.close()
conn.close()
