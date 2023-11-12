import psycopg2

conn = psycopg2.connect(
    host="localhost",
    database="Personalstammdatenbank",
    user="postgres",
    password="@Postgres123",
    port=5432
)

# Erstelle einen Cursor
cursor = conn.cursor()

# SQL-code in Python einlesen und anschließend ausführen
with open("../test/Datenbank und Stored Procedures.sql") as f:
    setup_sql = f.read()

cursor.execute(setup_sql)
conn.commit()
