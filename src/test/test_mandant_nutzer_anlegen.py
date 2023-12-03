import unittest
from src.main.Mandant import Mandant
from src.main.test_SetUp_TearDown import test_set_up, test_tear_down


class TestNutzerAnlegen(unittest.TestCase):

    def setUp(self):
        """
        Methode ruft Funktion 'test_set_up' der Klasse 'test_SetUp_TearDown' (siehe Ordner 'main') auf, welches das
        Datenbankschema 'temp_test_schema' erstellt.
        """
        self.conn, self.cur, self.testschema = test_set_up()

    def test_neuer_nutzer_in_datenbank_angelegt(self):
        """
        Test prüft, ob ein neuer Nutzer in der Datenbank gespeichert wird.
        """
        testfirma = Mandant('Testfirma', self.testschema)
        testfirma.nutzer_anlegen('M100001', 'Max', 'Mustermann', self.testschema)

        # Prüfung, ob Nutzer-Objekt angelegt und in Liste des entsprechenden Mandant-Objekts hinterlegt ist
        self.assertEqual(testfirma.get_nutzer('M100001').get_vorname(), 'Max')
        self.assertEqual(testfirma.get_nutzer('M100001').get_nachname(), 'Mustermann')

        # Prüfung, ob Nutzer in Datenbank angelegt ist
        select_query = "SELECT vorname, nachname FROM nutzer WHERE vorname = 'Max' AND nachname = 'Mustermann'"

        self.cur.execute(select_query)
        vorname, nachname = self.cur.fetchall()[0]

        self.assertEqual(vorname, 'Max')
        self.assertEqual(nachname, 'Mustermann')

    def test_nutzer_gleiche_personalnummer_in_datenbank(self):
        """
        Test prüft, ob eine Exception geworfen wird, wenn ein Mandant versucht, einen zweiten Nutzer mit derselben
        Personalnummer anzulegen
        """
        testfirma = Mandant('Testfirma', self.testschema)
        testfirma.nutzer_anlegen('M100001', 'Max', 'Mustermann', self.testschema)

        with self.assertRaises(Exception) as context:
            testfirma.nutzer_anlegen('M100001', 'Max', 'Mustermann', self.testschema)

        self.assertEqual(str(context.exception), "FEHLER:  Diese Personalnummer wird bereits verwendet!\n"
                                                 "CONTEXT:  PL/pgSQL-Funktion pruefe_einmaligkeit_personalnummer(integer,character varying,character varying) Zeile 14 bei RAISE\n"
                                                 "SQL-Anweisung »SELECT pruefe_einmaligkeit_personalnummer(p_mandant_id, 'nutzer', p_personalnummer)«\n"
                                                 "PL/pgSQL-Funktion nutzer_anlegen(integer,character varying,character varying,character varying) Zeile 10 bei PERFORM\n")

    def test_vorname_zahl(self):
        """
        Test prüft, ob die Raise-Funktion aufgerufen wird, wenn der Vorname des Nutzers kein String, sondern eine Zahl
        ist.
        """
        testfirma = Mandant('testfirma', self.testschema)

        with self.assertRaises(TypeError) as context:
            testfirma.nutzer_anlegen('M100001', 1.2, 'Mustermann', self.testschema)

        self.assertEqual(str(context.exception), 'Der Vorname des Nutzers muss ein String sein.')

    def test_vorname_postgres_exception(self):
        """
        Test prüft, ob die Raise-Funktion aufgerufen wird, wenn versucht wird, im Nachnamen des Nutzers den (Sub-)String
        'postgres' unterzubringen.
        """
        testfirma = Mandant('testfirma', self.testschema)

        # Quelle: https://stackoverflow.com/questions/129507/how-do-you-test-that-a-python-function-throws-an-exception
        with self.assertRaises(ValueError) as context:
            testfirma.nutzer_anlegen('M100001', 'postgres   ', 'Mustermann', self.testschema)
        self.assertEqual(str(context.exception), 'Dieser Vorname ist nicht erlaubt: postgres   .')

        with self.assertRaises(ValueError) as context:
            testfirma.nutzer_anlegen('M100001', '   postgres   ', 'Mustermann', self.testschema)
        self.assertEqual(str(context.exception), 'Dieser Vorname ist nicht erlaubt:    postgres   .')

        with self.assertRaises(ValueError) as context:
            testfirma.nutzer_anlegen('M100001', 'postgres', 'Mustermann', self.testschema)
        self.assertEqual(str(context.exception), 'Dieser Vorname ist nicht erlaubt: postgres.')

    def test_leerer_vorname_exception(self):
        """
        Test prüft, ob die Raise-Funktion aufgerufen wird, wenn der Vorname des Nutzers ein leerer String ist.
        """
        testfirma = Mandant('testfirma', self.testschema)

        with self.assertRaises(ValueError) as context:
            testfirma.nutzer_anlegen('M100001', '', 'Mustermann', self.testschema)

        self.assertEqual(str(context.exception), 'Der Vorname des Nutzers muss aus mindestens einem Zeichen bestehen.')

    def test_zu_langer_vorname_exception(self):
        """
        Test prüft, ob die Raise-Funktion aufgerufen wird, wenn versucht wird, einen Vornamen für einen Nutzer zu
        wählen, der länger als 64 Zeichen lang ist.
        """

        testfirma = Mandant('testfirma', self.testschema)

        vorname_65_zeichen = "a" * 65

        with self.assertRaises(ValueError) as context:
            testfirma.nutzer_anlegen('M100001', vorname_65_zeichen, 'Mustermann', self.testschema)

        self.assertEqual(str(context.exception), "Der Vorname darf höchstens 64 Zeichen lang sein. "
                                                 "'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa' "
                                                 "besitzt 65 Zeichen!")

    def test_nachname_zahl(self):
        """
        Test prüft, ob die Raise-Funktion aufgerufen wird, wenn der Nachname des Nutzers kein String, sondern eine Zahl
        ist.
        """
        testfirma = Mandant('testfirma', self.testschema)

        with self.assertRaises(TypeError) as context:
            testfirma.nutzer_anlegen('M100001', 'Max', 3, self.testschema)

        self.assertEqual(str(context.exception), 'Der Nachname des Nutzers muss ein String sein.')

    def test_nachname_postgres_exception(self):
        """
        Test prüft, ob die Raise-Funktion aufgerufen wird, wenn versucht wird, im Nachnamen des Nutzers den (Sub-)String
        'postgres' unterzubringen.
        """
        testfirma = Mandant('testfirma', self.testschema)

        # Quelle: https://stackoverflow.com/questions/129507/how-do-you-test-that-a-python-function-throws-an-exception
        with self.assertRaises(ValueError) as context:
            testfirma.nutzer_anlegen('M100001', 'Max', 'postgres   ', self.testschema)
        self.assertEqual(str(context.exception), 'Dieser Nachname ist nicht erlaubt: postgres   .')

        with self.assertRaises(ValueError) as context:
            testfirma.nutzer_anlegen('M100001', 'Max', '   postgres   ', self.testschema)
        self.assertEqual(str(context.exception), 'Dieser Nachname ist nicht erlaubt:    postgres   .')

        with self.assertRaises(ValueError) as context:
            testfirma.nutzer_anlegen('M100001', 'Max', 'postgres', self.testschema)
        self.assertEqual(str(context.exception), 'Dieser Nachname ist nicht erlaubt: postgres.')

    def test_leerer_nachname_exception(self):
        """
        Test prüft, ob die Raise-Funktion aufgerufen wird, wenn der Nachname des Nutzers ein leerer String ist.
        """
        testfirma = Mandant('testfirma', self.testschema)

        with self.assertRaises(ValueError) as context:
            testfirma.nutzer_anlegen('M100001', 'Max', '', self.testschema)

        self.assertEqual(str(context.exception), 'Der Nachname des Nutzers muss aus mindestens einem Zeichen bestehen.')

    def test_zu_langer_nachname_exception(self):
        """
        Test prüft, ob die Raise-Funktion aufgerufen wird, wenn versucht wird, einen Nachnamen für einen Nutzer zu
        wählen, der länger als 64 Zeichen lang ist.
        """

        testfirma = Mandant('testfirma', self.testschema)

        nachname_65_zeichen = "a" * 65

        with self.assertRaises(ValueError) as context:
            testfirma.nutzer_anlegen('M100001', 'Max', nachname_65_zeichen, self.testschema)

        self.assertEqual(str(context.exception), "Der Nachname darf höchstens 64 Zeichen lang sein. "
                                                 "'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa' "
                                                 "besitzt 65 Zeichen!")

    def test_falsches_schema_exception(self):
        """
        Test prüft, ob die ValueError-Exception geworfen wird, wenn die übergebene Schema-Bezeichnung nicht 'public'
        oder 'temp_test_schema' lautet
        """
        falsches_schema = 'hallo_welt_schema'

        testfirma = Mandant('testfirma', self.testschema)

        with self.assertRaises(ValueError) as context:
            testfirma.nutzer_anlegen('M100001', 'Max', 'Mustermann', falsches_schema)

        self.assertEqual(str(context.exception), "Diese Bezeichnung für ein Schema ist nicht erlaubt!")

    def tearDown(self):
        """
        Methode ruft Funktion 'test_tear_down' auf, welches das Datenbankschema 'temp_test_schema' mit allen Daten
        entfernt.
        """
        test_tear_down(self.conn, self.cur)
