import psycopg2

# Verbindung zur PostgreSQL-Datenbank herstellen
conn = psycopg2.connect(
    host="localhost",
    database="postgres",
    user="postgres",
    password="@Postgres123"
)

# Ein Cursor-Objekt erstellen
cursor = conn.cursor()

# SQL-Abfrage definieren
sql_query = "SELECT mitarbeiter_id, vorname, Nachname FROM Mitarbeiter"

# SQL-Abfrage ausführen
cursor.execute(sql_query)

# Ergebnisse abrufen
results = cursor.fetchall()

# Ergebnisse verarbeiten (hier einfach ausgeben)
for row in results:
    mitarbeiter_id, vorname, nachname = row
    print(f"Mitarbeiter_ID: {mitarbeiter_id}, Vorname: {vorname}, Nachname: {nachname}")

# Verbindung schließen
conn.close()
