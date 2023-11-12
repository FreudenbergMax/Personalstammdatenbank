import psycopg2
from src.main.Mandant import Mandant

conn = psycopg2.connect(
        host="localhost",
        database="Personalstammdatenbank",
        user="postgres",
        password="@Postgres123",
        port=5432
    )

firma = Mandant("Firma", conn)
firma.nutzer_anlegen("Max", "Mustermann", conn)
firma.get_nutzer("Max", "Mustermann").select_ausfuehren("mandanten", conn)
