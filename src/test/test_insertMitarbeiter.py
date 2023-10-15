import unittest
import psycopg2
from datetime import date
from src.main.Mandant import Mandant


class TestInsertMitarbeiter(unittest.TestCase):

    def test_neuer_mitarbeiter_angelegt(self):

        # Verbindung zur PostgreSQL-Datenbank herstellen
        conn = psycopg2.connect(
            host="localhost",
            database="postgres",
            user="postgres",
            password="@Postgres123"
        )

        # neuen Mandanten erstellen und als User in Datenbank speichern
        testfirma = Mandant('testfirma', conn)

        # neuen Mitarbeiter für Mandanten "testfirma" in die Datenbank eintragen
        testfirma.insert_neuer_mitarbeiter("Max Mustermann.xlsx", conn)

        select_query = "SELECT * FROM mitarbeiter"

        cur = conn.cursor()
        cur.execute(select_query)

        # Ergebnisse abrufen
        result = cur.fetchall()
        print(result)
        print(type(result[0][5]))

        self.assertEqual(result[0][0], 1)
        self.assertEqual(result[0][1], 'testfirma')
        self.assertEqual(result[0][2], 'Max')
        self.assertEqual(result[0][3], 'Mustermann')
        self.assertEqual(result[0][4], 'maennlich')
        self.assertEqual(result[0][5], date(1992, 12, 12))
        self.assertEqual(result[0][6], date(2023, 12, 1))
        self.assertEqual(result[0][7], '11 111 111 111')
        self.assertEqual(result[0][8], '00 121292 F 00')
        self.assertEqual(result[0][9], 'DE00 0000 0000 0000 0000 00')
        self.assertEqual(result[0][10], '0175 2572025')
        self.assertEqual(result[0][11], 'maxmustermann@web.de')
        self.assertEqual(result[0][12], None)

        # Verbindung zur Datenbank schließen
        conn.close()
