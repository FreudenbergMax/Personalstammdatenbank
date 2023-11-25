import unittest
from src.main.Mandant import Mandant
from src.main.test_SetUp import test_set_up


class TestNeuerNutzer(unittest.TestCase):

    def setUp(self):
        """
        Methode erstellt ein Testschema 'temp_test_schema' und darin die Personalstammdatenbank
        mit allen Tabellen und Stored Procedures. So können alle Tests ausgeführt werden, ohne die
        originale Datenbank zu manipulieren.
        :return:
        """
        self.conn, self.cursor = test_set_up()

    def test_neuer_nutzer_angelegt(self):
        """
        Test prüft, ob ein neuer Nutzer angelegt und in der Datenbank gespeichert wird.
        """
        testfirma = Mandant('Testfirma', self.conn)
        testfirma.nutzer_anlegen('Max', 'Mustermann', self.conn)

        # Prüfung, ob Nutzer-Objekt angelegt und in Liste des entsprechenden Mandant-Objekts hinterlegt ist
        self.assertEqual(testfirma.get_nutzer('Max', 'Mustermann').get_vorname(), 'Max')
        self.assertEqual(testfirma.get_nutzer('Max', 'Mustermann').get_nachname(), 'Mustermann')

        # Prüfung, ob Nutzer in Datenbank angelegt ist
        select_query = "SELECT vorname, nachname FROM nutzer WHERE vorname = 'Max' AND nachname = 'Mustermann'"

        cur = self.conn.cursor()
        cur.execute(select_query)
        vorname, nachname = cur.fetchall()[0]

        self.assertEqual(vorname, 'Max')
        self.assertEqual(nachname, 'Mustermann')

    def test_vorname_zahl(self):
        """
        Test prüft, ob die Raise-Funktion aufgerufen wird, wenn der Vorname des Nutzers kein String, sondern eine Zahl
        ist.
        """
        testfirma = Mandant('testfirma', self.conn)

        with self.assertRaises(TypeError) as context:
            testfirma.nutzer_anlegen(1.2, 'Mustermann', self.conn)

        self.assertEqual(str(context.exception), 'Der Vorname des Nutzers muss ein String sein.')

    def test_vorname_postgres_exception(self):
        """
        Test prüft, ob die Raise-Funktion aufgerufen wird, wenn versucht wird, im Nachnamen des Nutzers den (Sub-)String
        'postgres' unterzubringen.
        """
        testfirma = Mandant('testfirma', self.conn)

        # Quelle: https://stackoverflow.com/questions/129507/how-do-you-test-that-a-python-function-throws-an-exception
        with self.assertRaises(ValueError) as context:
            testfirma.nutzer_anlegen('postgres   ', 'Mustermann', self.conn)
        self.assertEqual(str(context.exception), 'Dieser Vorname ist nicht erlaubt: postgres   .')

        with self.assertRaises(ValueError) as context:
            testfirma.nutzer_anlegen('   postgres   ', 'Mustermann', self.conn)
        self.assertEqual(str(context.exception), 'Dieser Vorname ist nicht erlaubt:    postgres   .')

        with self.assertRaises(ValueError) as context:
            testfirma.nutzer_anlegen('postgres', 'Mustermann', self.conn)
        self.assertEqual(str(context.exception), 'Dieser Vorname ist nicht erlaubt: postgres.')

    def test_leerer_vorname_exception(self):
        """
        Test prüft, ob die Raise-Funktion aufgerufen wird, wenn der Vorname des Nutzers ein leerer String ist.
        """
        testfirma = Mandant('testfirma', self.conn)

        with self.assertRaises(ValueError) as context:
            testfirma.nutzer_anlegen('', 'Mustermann', self.conn)

        self.assertEqual(str(context.exception), 'Der Vorname des Nutzers muss aus mindestens einem Zeichen bestehen.')

    def test_zu_langer_vorname_exception(self):
        """
        Test prüft, ob die Raise-Funktion aufgerufen wird, wenn versucht wird, einen Vornamen für einen Nutzer zu
        wählen, der länger als 64 Zeichen lang ist.
        """

        testfirma = Mandant('testfirma', self.conn)

        vorname_65_zeichen = "a" * 65

        with self.assertRaises(ValueError) as context:
            testfirma.nutzer_anlegen(vorname_65_zeichen, 'Mustermann', self.conn)

        self.assertEqual(str(context.exception), 'Der Vorname darf höchstens 64 Zeichen lang sein.')

    def test_nachname_zahl(self):
        """
        Test prüft, ob die Raise-Funktion aufgerufen wird, wenn der Nachname des Nutzers kein String, sondern eine Zahl
        ist.
        """
        testfirma = Mandant('testfirma', self.conn)

        with self.assertRaises(TypeError) as context:
            testfirma.nutzer_anlegen('Max', 3, self.conn)

        self.assertEqual(str(context.exception), 'Der Nachname des Nutzers muss ein String sein.')

    def test_nachname_postgres_exception(self):
        """
        Test prüft, ob die Raise-Funktion aufgerufen wird, wenn versucht wird, im Nachnamen des Nutzers den (Sub-)String
        'postgres' unterzubringen.
        """
        testfirma = Mandant('testfirma', self.conn)

        # Quelle: https://stackoverflow.com/questions/129507/how-do-you-test-that-a-python-function-throws-an-exception
        with self.assertRaises(ValueError) as context:
            testfirma.nutzer_anlegen('Max', 'postgres   ', self.conn)
        self.assertEqual(str(context.exception), 'Dieser Nachname ist nicht erlaubt: postgres   .')

        with self.assertRaises(ValueError) as context:
            testfirma.nutzer_anlegen('Max', '   postgres   ', self.conn)
        self.assertEqual(str(context.exception), 'Dieser Nachname ist nicht erlaubt:    postgres   .')

        with self.assertRaises(ValueError) as context:
            testfirma.nutzer_anlegen('Max', 'postgres', self.conn)
        self.assertEqual(str(context.exception), 'Dieser Nachname ist nicht erlaubt: postgres.')

    def test_leerer_nachname_exception(self):
        """
        Test prüft, ob die Raise-Funktion aufgerufen wird, wenn der Nachname des Nutzers ein leerer String ist.
        """
        testfirma = Mandant('testfirma', self.conn)

        with self.assertRaises(ValueError) as context:
            testfirma.nutzer_anlegen('Max', '', self.conn)

        self.assertEqual(str(context.exception), 'Der Nachname des Nutzers muss aus mindestens einem Zeichen bestehen.')

    def test_zu_langer_nachname_exception(self):
        """
        Test prüft, ob die Raise-Funktion aufgerufen wird, wenn versucht wird, einen Nachnamen für einen Nutzer zu
        wählen, der länger als 64 Zeichen lang ist.
        """

        testfirma = Mandant('testfirma', self.conn)

        nachname_65_zeichen = "a" * 65

        with self.assertRaises(ValueError) as context:
            testfirma.nutzer_anlegen('Max', nachname_65_zeichen, self.conn)

        self.assertEqual(str(context.exception), 'Der Nachname darf höchstens 64 Zeichen lang sein.')

    def tearDown(self):
        """
        Methode entfernt das Test-Schema 'temp_test_schema' inkl. der darin enthaltenen Test-
        Personalstammdatenbank mit allen ihren Tabellen, Stored Procedures und Daten, die während
        der Testfälle erzeugt wurden.
        """
        self.cursor.execute(f"DROP SCHEMA temp_test_schema CASCADE")
        self.conn.commit()
