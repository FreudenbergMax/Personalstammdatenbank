import unittest

from src.main.Mandant import Mandant
from src.main.test_SetUp_TearDown import test_set_up, test_tear_down


class TestNeuerMandant(unittest.TestCase):

    def setUp(self):
        """
        Methode ruft Funktion 'test_set_up' der Klasse 'test_SetUp_TearDown' (siehe Ordner 'main') auf, welches das
        Datenbankschema 'temp_test_schema' erstellt.
        """
        self.testschema = test_set_up()

    def test_erster_mandant_angelegt(self):
        """
        Test prüft ab, ob ein neuer Mandant angelegt wird, sofern alle Bedingungen erfüllt sind.
        """

        testfirma = Mandant('beispielbetrieb', self.testschema)
        testfirma.nutzer_anlegen('M100001', 'Max', 'Mustermann', self.testschema)

        ausgabe = testfirma.get_nutzer("M100001").abfrage_ausfuehren("SELECT * FROM mandanten WHERE firma = "
                                                                     "'beispielbetrieb'", self.testschema)

        self.assertEqual(str(ausgabe), "[(1, 'beispielbetrieb')]")

    def test_weiterer_mandant_mit_gleichem_Namen_Exception(self):
        """
        Test prüft ab, ob bei der Neuanlage eines Mandanten die Exception der Stored Procedure 'mandant_anlegen'
        geworfen wird, wenn der Name des Mandanten bereits existiert.
        """
        testfirma1 = Mandant('beispielbetrieb', self.testschema)

        with self.assertRaises(Exception) as context:
            testfirma2 = Mandant('beispielbetrieb', self.testschema)

        self.assertEqual(str(context.exception), 'FEHLER:  Dieser Mandant ist bereits angelegt!\n'
                                                 'CONTEXT:  PL/pgSQL-Funktion mandant_anlegen(character varying) Zeile 13 bei RAISE\n')

    def test_name_zahl(self):
        """
        Test prüft, ob die Raise-Funktion aufgerufen wird, wenn der Name des Mandanten kein String, sondern eine Zahl
        ist.
        """

        with self.assertRaises(TypeError) as context:
            testfirma = Mandant(5, self.testschema)

        self.assertEqual(str(context.exception), 'Der Name des Mandanten muss ein String sein.')

    def test_name_postgres_exception(self):
        """
        Test prüft, ob die Raise-Funktion aufgerufen wird, wenn versucht wird, im Mandantennamen den (Sub-)String
        'postgres' unterzubringen.
        """
        # Quelle: https://stackoverflow.com/questions/129507/how-do-you-test-that-a-python-function-throws-an-exception
        with self.assertRaises(ValueError) as context:
            testfirma1 = Mandant('postgres   ', self.testschema)
        self.assertEqual(str(context.exception), 'Dieser Name ist nicht erlaubt: postgres   .')

        with self.assertRaises(ValueError) as context:
            testfirma2 = Mandant('   postgres   ', self.testschema)
        self.assertEqual(str(context.exception), 'Dieser Name ist nicht erlaubt:    postgres   .')

        with self.assertRaises(ValueError) as context:
            testfirma2 = Mandant('postgres', self.testschema)
        self.assertEqual(str(context.exception), 'Dieser Name ist nicht erlaubt: postgres.')

    def test_leerer_name_exception(self):
        """
        Test prüft, ob die Raise-Funktion aufgerufen wird, wenn bei der Anlage eines neuen Mandanten
        kein Name bzw. ein leerer String vorhanden ist
        """
        with self.assertRaises(ValueError) as context:
            testfirma = Mandant('', self.testschema)

        self.assertEqual(str(context.exception), 'Der Name des Mandanten muss aus mindestens einem Zeichen bestehen.')

    def test_zu_langer_name_exception(self):
        """
        Test prüft, ob die Raise-Funktion aufgerufen wird, wenn versucht wird, einen Mandantennamen zu
        wählen, der länger als 128 Zeichen lang ist.
        """
        name_129_zeichen = "a" * 129

        with self.assertRaises(ValueError) as context:
            testfirma = Mandant(name_129_zeichen, self.testschema)

        self.assertEqual(str(context.exception), "Der Name des Mandanten darf höchstens 128 Zeichen lang sein."
                                                 "'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
                                                 "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa' "
                                                 "besitzt 129 Zeichen!")

    def test_falsches_schema_exception(self):
        """
        Test prüft, ob die ValueError-Exception geworfen wird, wenn die übergebene Schema-Bezeichnung nicht 'public'
        oder 'temp_test_schema' lautet
        """
        falsches_schema = 'hallo_welt_schema'

        with self.assertRaises(ValueError) as context:
            testfirma = Mandant("Beispielfirma", falsches_schema)

        self.assertEqual(str(context.exception), "Diese Bezeichnung für ein Schema ist nicht erlaubt!")

    def tearDown(self):
        """
        Methode ruft Funktion 'test_tear_down' der Klasse 'test_SetUp_TearDown' (siehe Ordner 'main') auf, welches das
        Datenbankschema 'temp_test_schema' mit allen Daten entfernt.
        """
        test_tear_down()
