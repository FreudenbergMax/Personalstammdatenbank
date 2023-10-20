import unittest
import psycopg2
from src.main.Mandant import Mandant


class TestNeuerMandant(unittest.TestCase):

    def test_neuer_mandant_angelegt(self):

        # Verbindung zur PostgreSQL-Datenbank herstellen
        conn = psycopg2.connect(
            host="localhost",
            database="Personalstammdatenbank",
            user="postgres",
            password="@Postgres123"
        )

        # neuen Mandanten erstellen und als User in Datenbank speichern
        testfirma = Mandant('firma', conn)

        role_query = "SET ROLE postgres"
        select_query = "SELECT usename FROM pg_catalog.pg_user WHERE usename = 'firma'"

        cur = conn.cursor()
        cur.execute(role_query)
        cur.execute(select_query)

        # Ergebnisse abrufen
        result = cur.fetchall()
        name_neuer_mandant = result[0][0]

        self.assertEqual(name_neuer_mandant, 'firma')

        # Verbindung zur Datenbank schließen
        conn.close()

    def test_verbotenerName(self):
        # Verbindung zur PostgreSQL-Datenbank herstellen
        conn = psycopg2.connect(
            host="localhost",
            database="postgres",
            user="postgres",
            password="@Postgres123"
        )

        # neuen Mandanten erstellen und als User in Datenbank speichern
        testfirma = Mandant('postgres', conn)
