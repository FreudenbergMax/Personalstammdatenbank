import unittest
import psycopg2
from src.main.Mandant import Mandant
import psycopg2.extras


class TestNeuerMandant(unittest.TestCase):

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
        setup_sql = "create schema if not exists temp_test_schema;\n\nset search_path to temp_test_schema;\n\n"

        with open("Datenbank und Stored Procedures.sql") as f:
            setup_sql = setup_sql + f.read()

        self.cursor.execute(setup_sql)
        self.conn.commit()

    def test_neuer_mandant_angelegt(self):
        """
        Test prüft ab, ob ein neuer Mandant angelegt wird, sofern alle Bedingungen erfüllt sind.
        """
        testfirma = Mandant('beispielbetrieb', self.conn)

        select_query = "SELECT firma FROM mandanten WHERE firma = 'beispielbetrieb'"

        cur = self.conn.cursor()
        cur.execute(select_query)

        # Ergebnisse abrufen
        name_neuer_mandant = cur.fetchall()[0][0]

        self.assertEqual(name_neuer_mandant, 'beispielbetrieb')

    def test_name_postgres_exception(self):
        """
        Test prüft, ob eine Exception geworfen wird, wenn versucht wird, als Mandantenname "postgres"
        zu wählen. ("postgres" ist der Adminname der Personalstammdatenbank und darf für Mandanten
        nicht zugänglich sein)
        """
        # Quelle: https://stackoverflow.com/questions/129507/how-do-you-test-that-a-python-function-throws-an-exception
        with self.assertRaises(ValueError) as context:
            testfirma = Mandant('postgres', self.conn)

        self.assertEqual(str(context.exception), "Dieser Name ist nicht erlaubt: postgres.")

    def test_kein_name_exception(self):
        """
        Test prüft, ob eine Exception geworfen wird, wenn bei der Anlage eines neuen Mandanten
        kein Name vorhanden ist
        """
        with self.assertRaises(ValueError) as context:
            testfirma = Mandant('', self.conn)

        self.assertEqual(str(context.exception), "Der Name des Mandanten muss aus mindestens einem Zeichen bestehen.")

    def test_zu_langer_name_exception(self):
        """
        Test prüft, ob eine Exception geworfen wird, wenn versucht wird, einen Mandantennamen zu
        wählen, der länger als 128 Zeichen lang ist.
        """
        name_129_zeichen = "a" * 129

        with self.assertRaises(ValueError) as context:
            testfirma = Mandant(name_129_zeichen, self.conn)

        self.assertEqual(str(context.exception), "Der Name des Mandanten darf höchstens 128 Zeichen lang sein.")

    def tearDown(self):
        """
        Methode entfernt das Test-Schema 'temp_test_schema' inkl. der darin enthaltenen Test-
        Personalstammdatenbank mit allen ihren Tabellen, Stored Procedures und Daten, die während
        der Testfälle erzeugt wurden.
        """
        self.cursor.execute(f"DROP SCHEMA temp_test_schema CASCADE")
        self.conn.commit()
