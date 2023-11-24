import psycopg2
from src.main.Mandant import Mandant

conn = psycopg2.connect(
        host="localhost",
        database="Personalstammdatenbank",
        user="postgres",
        password="@Postgres123",
        port=5432
    )

testfirma = Mandant("testfirma", conn)
testfirma.nutzer_anlegen("Max", "Mustermann", conn)
testfirma.get_nutzer("Max", "Mustermann").insert_neuer_mitarbeiter("Max Mustermann.xlsx", conn)
testfirma.get_nutzer("Max", "Mustermann").insert_neuer_mitarbeiter("Max Mustermann.xlsx", conn)
