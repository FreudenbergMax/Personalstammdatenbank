import unittest
import psycopg2
from src.main.Mandant import Mandant
import psycopg2.extras


class TestNeuerMandant(unittest.TestCase):

    # Erstelle ein temporäres Schema für die Tests
    def setUp(self):
        """
        Methode erstellt ein Testschema 'temp_test_schema' und darin die Personalstammdatenbank
        mit allen Tabellen und Stored Procedures. So können alle Tests ausgeführt werden, ohne die
        originale Datenbank zu manipulieren.
        :return:
        """
        self.conn = psycopg2.connect(
            host="localhost",
            database="Personalstammdatenbank",
            user="postgres",
            password="@Postgres123",
            port=5432
        )

        # Erstelle einen Cursor
        self.cursor = self.conn.cursor()

        # SQL-code in Python einlesen und anschließend ausführen
        with open("Datenbank und Stored Procedures.sql") as f:
            setup_sql = f.read()

        self.cursor.execute(setup_sql)
        self.conn.commit()

    def test_neuer_mandant_angelegt(self):
        """
        Test prüft ab, ob ein neuer Mandant angelegt wird, sofern alle Bedingungen erfüllt sind
        """
        testfirma = Mandant('firma', self.conn)

        role_query = "SET ROLE postgres"
        select_query = "SELECT usename FROM pg_catalog.pg_user WHERE usename = 'firma'"

        cur = self.conn.cursor()
        cur.execute(role_query)
        cur.execute(select_query)

        # Ergebnisse abrufen
        result = cur.fetchall()
        name_neuer_mandant = result

        self.assertEqual(name_neuer_mandant, 'firma')

    def test_name_postgres_exception(self):
        """
        Test prüft, ob eine Exception geworfen wird, wenn versucht wird, als Mandantenname "postgres"
        zu wählen. ("postgres" ist der Adminname der Personalstammdatenbank und darf für Mandanten
        nicht zugänglich sein)
        :return:
        """
        pass

    def test_kein_name_exception(self):
        """
        Test prüft, ob eine Exception geworfen wird, wenn bei der Anlage eines neuen Mandanten
        kein Name vorhanden ist
        :return:
        """
        pass

    def test_zu_langer_name_exception(self):
        """
        Test prüft, ob eine Exception geworfen wird, wenn versucht wird, einen Mandantennamen zu
        wählen, der länger als 128 Zeichen lang ist.
        :return:
        """
        pass

    def test_name_mehrfach_exception(self):
        """
        Test prüft, ob eine Exception geworfen wird, wenn ein Mandantenname gewählt wird, der
        bereits existiert.
        :return:
        """
        pass
'''
    # Lösche das temporäre Schema
    def tearDown(self):
        """
        Methode entfernt das Test-Schema 'temp_test_schema' inkl. der darin enthaltenen Test-
        Personalstammdatenbank mit allen ihren Tabellen, Stored Procedures und Daten, die während
        der Testfälle erzeugt wurden.
        :return:
        """
        self.cursor.execute(f"DROP SCHEMA temp_test_schema CASCADE")
        self.conn.commit()
'''