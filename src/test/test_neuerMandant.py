import unittest
import psycopg2

from src.main.Mandant import Mandant
from src.main.neuerMandant import neuer_mandant


class TestNeuerMandant(unittest.TestCase):

    def test_neuer_mandant(self):
        conn = psycopg2.connect(
            host="localhost",
            database="postgres",
            user="postgres",
            password="@Postgres123"
        )

        neuer_mandant(conn, 'Testfirma', 'Teststraße 1, 00000 Teststadt')

        # Ein Cursor-Objekt erstellen
        cursor = conn.cursor()
        setPostgres_query = "set role postgres;"
        select_query = "SELECT Mandant_ID, Mandant, Adresse FROM Mandanten"

        # SQL-Abfragen ausführen
        cursor.execute(setPostgres_query)
        cursor.execute(select_query)

        # Ergebnisse abrufen
        result = cursor.fetchall()

        for row in result:
            mandant_id, mandant, adresse = row

        self.assertEqual(mandant_id, 1)
        self.assertEqual(mandant, 'Testfirma')
        self.assertEqual(adresse, 'Teststraße 1, 00000 Teststadt')

    def test_neuer_mandant_angelegt(self):

        # Verbindung zur PostgreSQL-Datenbank herstellen
        conn = psycopg2.connect(
            host="localhost",
            database="postgres",
            user="postgres",
            password="@Postgres123"
        )

        # neuen Mandanten erstellen und als User in Datenbank speichern
        testfirma = Mandant('testfirma', conn)

        # Verbindung zur Datenbank schließen
        conn.close()