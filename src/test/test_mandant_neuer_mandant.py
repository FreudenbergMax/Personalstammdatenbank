import unittest
import psycopg2

from src.main.Mandant import Mandant
from src.main.test_SetUp import test_set_up


class TestNeuerMandant(unittest.TestCase):

    def setUp(self):
        """
        Methode erstellt ein Testschema 'temp_test_schema' und darin die Personalstammdatenbank
        mit allen Tabellen und Stored Procedures. So können alle Tests ausgeführt werden, ohne die
        originale Datenbank zu manipulieren.
        """
        self.conn, self.cursor = test_set_up()

    def test_erster_mandant_angelegt(self):
        """
        Test prüft ab, ob ein neuer Mandant angelegt wird, sofern alle Bedingungen erfüllt sind.
        """
        testfirma = Mandant('beispielbetrieb', self.conn)

        select_query = "SELECT * FROM mandanten WHERE firma = 'beispielbetrieb'"

        cur = self.conn.cursor()
        cur.execute(select_query)

        # Ergebnisse abrufen
        ausgabe = cur.fetchall()
        mandant_id = ausgabe[0][0]
        name_neuer_mandant = ausgabe[0][1]

        self.assertEqual(mandant_id, 1)
        self.assertEqual(name_neuer_mandant, 'beispielbetrieb')

    def test_weiterer_mandant_angelegt(self):
        """
        Test prüft ab, ob ein neuer Mandant angelegt wird, sofern alle Bedingungen erfüllt sind, und ob der Zähler
        für die Erstellung der Mandanten_ID, der in der Stored Procedure 'erstelle_neue_id' implementiert ist, läuft.
        """
        testfirma = Mandant('beispielbetrieb', self.conn)
        testunternehmen = Mandant('testunternehmen', self.conn)

        select_query = "SELECT * FROM mandanten WHERE firma = 'testunternehmen'"

        cur = self.conn.cursor()
        cur.execute(select_query)

        # Ergebnisse abrufen
        ausgabe = cur.fetchall()
        mandant_id = ausgabe[0][0]
        name_neuer_mandant = ausgabe[0][1]

        self.assertEqual(mandant_id, 2)
        self.assertEqual(name_neuer_mandant, 'testunternehmen')

    def test_weiterer_mandant_mit_gleichem_Namen_Exception(self):
        """
        Test prüft ab, ob bei der Neuanlage eines Mandanten die Exception der Stored Procedure 'mandant_anlegen'
        geworfen wird, wenn der Name des Mandanten bereits existiert.
        """
        testfirma1 = Mandant('beispielbetrieb', self.conn)

        with self.assertRaises(Exception) as context:
            testfirma2 = Mandant('beispielbetrieb', self.conn)

        self.assertEqual(str(context.exception), 'FEHLER:  Dieser Mandant ist bereits angelegt!\n'
                                                 'CONTEXT:  PL/pgSQL-Funktion mandant_anlegen(character varying) Zeile 10 bei RAISE\n')

        # Folgende Code-Zeile notwendig, da eine geworfene Exception in einer postgres-Stored Procedure
        # die Transaktion beendet und deswegen in der TearDown-Methode eine fehlermeldung kommt.
        # Keine elegenatere Möglichkeit zur Fehlerbehebung gefunden
        self.conn, self.cursor = test_set_up()

    def test_name_zahl(self):
        """
        Test prüft, ob die Raise-Funktion aufgerufen wird, wenn der Name des Mandanten kein String, sondern eine Zahl
        ist.
        """

        with self.assertRaises(TypeError) as context:
            testfirma = Mandant(5, self.conn)

        self.assertEqual(str(context.exception), 'Der Name des Mandanten muss ein String sein.')

    def test_name_postgres_exception(self):
        """
        Test prüft, ob die Raise-Funktion aufgerufen wird, wenn versucht wird, im Mandantennamen den (Sub-)String
        'postgres' unterzubringen.
        """
        # Quelle: https://stackoverflow.com/questions/129507/how-do-you-test-that-a-python-function-throws-an-exception
        with self.assertRaises(ValueError) as context:
            testfirma1 = Mandant('postgres   ', self.conn)
        self.assertEqual(str(context.exception), 'Dieser Name ist nicht erlaubt: postgres   .')

        with self.assertRaises(ValueError) as context:
            testfirma2 = Mandant('   postgres   ', self.conn)
        self.assertEqual(str(context.exception), 'Dieser Name ist nicht erlaubt:    postgres   .')

        with self.assertRaises(ValueError) as context:
            testfirma2 = Mandant('postgres', self.conn)
        self.assertEqual(str(context.exception), 'Dieser Name ist nicht erlaubt: postgres.')

    def test_leerer_name_exception(self):
        """
        Test prüft, ob die Raise-Funktion aufgerufen wird, wenn bei der Anlage eines neuen Mandanten
        kein Name bzw. ein leerer String vorhanden ist
        """
        with self.assertRaises(ValueError) as context:
            testfirma = Mandant('', self.conn)

        self.assertEqual(str(context.exception), 'Der Name des Mandanten muss aus mindestens einem Zeichen bestehen.')

    def test_zu_langer_name_exception(self):
        """
        Test prüft, ob die Raise-Funktion aufgerufen wird, wenn versucht wird, einen Mandantennamen zu
        wählen, der länger als 128 Zeichen lang ist.
        """
        name_129_zeichen = "a" * 129

        with self.assertRaises(ValueError) as context:
            testfirma = Mandant(name_129_zeichen, self.conn)

        self.assertEqual(str(context.exception), "Der Name des Mandanten darf höchstens 128 Zeichen lang sein."
                                                 "'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
                                                 "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa' "
                                                 "besitzt 129 Zeichen!")

    def tearDown(self):
        """
        Methode entfernt das Test-Schema 'temp_test_schema' inkl. der darin enthaltenen Test-
        Personalstammdatenbank mit allen ihren Tabellen, Stored Procedures und Daten, die während
        der Testfälle erzeugt wurden.
        """
        self.cursor.execute(f"DROP SCHEMA temp_test_schema CASCADE")
        self.conn.commit()
