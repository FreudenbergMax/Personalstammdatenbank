import unittest
from datetime import datetime

from src.main.Login import Login
from src.test.test_SetUp_TearDown import test_set_up, test_tear_down


class TestExistenzStrDatenFeststellen(unittest.TestCase):

    def setUp(self):
        """
        Methode ruft Funktion 'test_set_up' der Klasse 'test_SetUp_TearDown' (siehe Ordner 'main') auf, welches das
        Datenbankschema 'temp_test_schema' erstellt.
        """
        self.testschema = test_set_up()

        login = Login(self.testschema)
        login.registriere_mandant_und_admin('Testfirma', 'mandantenpw', 'mandantenpw', 'M100000', 'Otto',
                                            'Normalverbraucher', 'adminpw', 'adminpw')
        self.admin = login.login_admin('Testfirma', 'mandantenpw', 'M100000', 'adminpw')
        self.admin.nutzer_anlegen('M100001', 'Erika', 'Musterfrau', 'nutzerpw', 'nutzerpw')

        self.nutzer = login.login_nutzer('Testfirma', 'mandantenpw', 'M100001', 'nutzerpw')
        self.nutzer.passwort_aendern('neues passwort', 'neues passwort')

    def test_optionale_zeichenkette_ist_leer(self):
        """
        Test prueft, ob die Methode 'existenz_str_daten_feststellen' ein 'None' zurueckgibt, wenn die
        uebergegebene Variable ein optionaler leerer String ist.
        """
        zweitname = ''
        zweitname = self.nutzer._existenz_str_daten_feststellen(zweitname, 'Zweitname', 0, False)

        self.assertEqual(zweitname, None)

    def test_pflicht_zeichenkette_ist_leer(self):
        """
        Test prueft, ob eine Fehlemeldung ausgegeben wird, wenn die uebergegebene Variable ein leerer Pflicht-String
        ist.
        """
        personalnummer = ''

        # Quelle: https://stackoverflow.com/questions/129507/how-do-you-test-that-a-python-function-throws-an-exception
        with self.assertRaises(ValueError) as context:
            personalnummer = self.nutzer._existenz_str_daten_feststellen(personalnummer, 'Personalnummer', 0, True)

        self.assertEqual(str(context.exception), "'Personalnummer' ist nicht vorhanden.")

    def test_ganzzahl_wird_str(self):
        """
        Test prueft, ob eine Fehlemeldung ausgegeben wird, wenn die uebergegebene Variable anfangs als Ganzzahl gelesen
        wird, aber eigentlich als Zeichenkette in die Datenbank uebertragen werden soll.
        """
        postleitzahl = 12345
        postleitzahl = self.nutzer._existenz_str_daten_feststellen(postleitzahl, 'Postleitzahl', 5, False)

        self.assertEqual(type(postleitzahl), str)

    def test_gleitkommazahl_wird_str(self):
        """
        Test prueft, ob die Methode 'existenz_str_daten_feststellen' ein 'str' zurueckgibt, wenn die
        uebergegebene Variable anfangs als Gleitkomma gelesen wird, aber eigentlich als Zeichenkette in die Datenbank
        uebertragen werden soll.
        """
        double = 12.45
        double = self.nutzer._existenz_str_daten_feststellen(double, 'Zahl_zu_String', 5, False)

        self.assertEqual(type(double), str)

    def test_datum_wird_str(self):
        """
        Test prueft, ob die Methode 'existenz_str_daten_feststellen' ein 'str' zurueckgibt, wenn die
        uebergegebene Variable anfangs (unerwarteterweise) als Datum gelesen wird, aber eigentlich als Zeichenkette in
        die Datenbank uebertragen werden soll.
        """
        date_daten = datetime.strptime('12.12.1992', '%d.%m.%Y').date()
        date_daten = self.nutzer._existenz_str_daten_feststellen(date_daten, 'Datum_zu_String', 10, False)

        self.assertEqual(type(date_daten), str)

    def test_zu_lange_zeichenkette(self):
        """
        Test prueft, ob eine Fehlemeldung ausgegeben wird, wenn die eichenkette laenger ist als erlaubt.
        """
        personalnummer = '0' + ('12345678' * 4)

        with self.assertRaises(ValueError) as context:
            personalnummer = self.nutzer._existenz_str_daten_feststellen(personalnummer, 'Personalnummer', 32, True)

        self.assertEqual(str(context.exception), "'Personalnummer' darf hoechstens 32 Zeichen lang sein. "
                                                 "Ihre Eingabe '012345678123456781234567812345678' besitzt 33 Zeichen!")

    def tearDown(self):
        """
        Methode ruft Funktion 'test_tear_down' auf, welches das Datenbankschema 'temp_test_schema' mit allen Daten
        entfernt.
        """
        test_tear_down()
