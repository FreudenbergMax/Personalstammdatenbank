import psycopg2
from src.main.Mandant import Mandant

conn = psycopg2.connect(
        host="localhost",
        database="Personalstammdatenbank",
        user="postgres",
        password="@Postgres123",
        port=5432
    )

testfirma = Mandant("testu", conn)
testfirma.nutzer_anlegen("M100001", "Max", "Mustermann", conn)

testfirma.get_nutzer("M100001").insert_neuer_mitarbeiter('Max Mustermann.xlsx', conn)
#datum = testfirma.get_nutzer("Max", "Mustermann")._existenz_date_daten_feststellen('32.12.2023', 'Eintrittsdatum', True)
#print(datum)
#testfirma.nutzer_entfernen('Max', 'Mustermann', conn)
#testfirma.get_nutzer("Max", "Mustermann")

