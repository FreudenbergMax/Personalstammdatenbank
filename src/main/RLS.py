import psycopg2

# Verbindung zur PostgreSQL-Datenbank herstellen
conn = psycopg2.connect(
    host="localhost",
    database="postgres",
    user="postgres",
    password="@Postgres123"
)

cur = conn.cursor()

# SELECT-Abfrage ausführen
cur.execute("SELECT * FROM customer_orders;")
results = cur.fetchall()

# Ergebnisse ausgeben (Mandant 2 sollte keine Daten erhalten)
print("Ergebnisse:", results)

# Verbindung schließen
conn.close()
