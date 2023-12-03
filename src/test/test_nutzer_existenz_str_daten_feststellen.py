import unittest
from datetime import datetime

from src.main.test_SetUp_TearDown import test_set_up, test_tear_down
from src.main.Mandant import Mandant


class TestExistenzStrDatenFeststellen(unittest.TestCase):

    def setUp(self):
        """
        Methode ruft Funktion 'test_set_up' der Klasse 'test_SetUp_TearDown' (siehe Ordner 'main') auf, welches das
        Datenbankschema 'temp_test_schema' erstellt.
        """
        self.conn, self.cur, self.testschema = test_set_up()
        self.testfirma = Mandant('Testfirma', self.testschema)
        self.testfirma.nutzer_anlegen('M10001', 'Max', 'Mustermann', self.testschema)

    def test_optionale_zeichenkette_ist_leer(self):
        """
        Test prüft, ob die Methode 'existenz_str_daten_feststellen' ein 'None' zurückgibt, wenn die
        übergegebene Variable ein optionaler leerer String ist.
        """
        zweitname = ''
        zweitname = self.testfirma.get_nutzer('M10001'). \
            _existenz_str_daten_feststellen(zweitname, 'Zweitname', 0, False)

        self.assertEqual(zweitname, None)

    def test_pflicht_zeichenkette_ist_leer(self):
        """
        Test prüft, ob die Methode 'existenz_str_daten_feststellen' ein ValueError-Exception wirft, wenn die
        übergegebene Variable ein leerer Pflicht-String ist.
        """
        personalnummer = ''

        # Quelle: https://stackoverflow.com/questions/129507/how-do-you-test-that-a-python-function-throws-an-exception
        with self.assertRaises(ValueError) as context:
            personalnummer = self.testfirma.get_nutzer('M10001'). \
                _existenz_str_daten_feststellen(personalnummer, 'Personalnummer', 0, True)

        self.assertEqual(str(context.exception), "'Personalnummer' ist nicht vorhanden.")

    def test_ganzzahl_wird_str(self):
        """
        Test prüft, ob die Methode 'existenz_str_daten_feststellen' ein 'str' zurückgibt, wenn die
        übergegebene Variable anfangs als Ganzzahl gelesen wird, aber eigentlich als Zeichenkette in die Datenbank
        übertragen werden soll.
        """
        postleitzahl = 12345
        postleitzahl = self.testfirma.get_nutzer('M10001'). \
            _existenz_str_daten_feststellen(postleitzahl, 'Postleitzahl', 5, False)

        self.assertEqual(type(postleitzahl), str)

    def test_gleitkommazahl_wird_str(self):
        """
        Test prüft, ob die Methode 'existenz_str_daten_feststellen' ein 'str' zurückgibt, wenn die
        übergegebene Variable anfangs als Gleitkomma gelesen wird, aber eigentlich als Zeichenkette in die Datenbank
        übertragen werden soll.
        """
        double = 12.45
        double = self.testfirma.get_nutzer('M10001')._existenz_str_daten_feststellen(
            double, 'Postleitzahl', 5, False)

        self.assertEqual(type(double), str)

    def test_datum_wird_str(self):
        """
        Test prüft, ob die Methode 'existenz_str_daten_feststellen' ein 'str' zurückgibt, wenn die
        übergegebene Variable anfangs (unerwarteterweise) als Datum gelesen wird, aber eigentlich als Zeichenkette in
        die Datenbank übertragen werden soll.
        """
        date_daten = datetime.strptime('12.12.1992', '%d.%m.%Y').date()
        date_daten = self.testfirma.get_nutzer('M10001')._existenz_str_daten_feststellen(
            date_daten, 'Postleitzahl', 10, False)

        self.assertEqual(type(date_daten), str)

    def test_zu_lange_zeichenkette(self):
        """
        Test prüft, ob die Methode 'existenz_str_daten_feststellen' eine ValueError-Exception wirft, wenn die
        Zeichenekette länger ist als erlaubt.
        """
        personalnummer = '0' + ('12345678' * 4)

        with self.assertRaises(ValueError) as context:
            personalnummer = self.testfirma.get_nutzer('M10001'). \
                _existenz_str_daten_feststellen(personalnummer, 'Personalnummer', 32, True)

        self.assertEqual(str(context.exception), "'Personalnummer' darf höchstens 32 Zeichen lang sein. "
                                                 "Ihre Eingabe '012345678123456781234567812345678' besitzt 33 Zeichen!")

    def tearDown(self):
        """
        Methode ruft Funktion 'test_tear_down' auf, welches das Datenbankschema 'temp_test_schema' mit allen Daten
        entfernt.
        """
        test_tear_down(self.conn, self.cur)
