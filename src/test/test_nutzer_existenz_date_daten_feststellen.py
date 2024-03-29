import unittest
from datetime import datetime

from src.main.Login import Login
from src.test.test_SetUp_TearDown import test_set_up, test_tear_down


class TestExistenzDateDatenFeststellen(unittest.TestCase):

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

    def test_optionales_datum_ist_leer(self):
        """
        Test prueft, ob die Methode 'existenz_data_daten_feststellen' ein 'None' zurueckgibt, wenn die
        uebergegebene Variable ein optionaler leerer String ist.
        """
        austrittsdatum = ''
        austrittsdatum = self.nutzer._existenz_date_daten_feststellen(austrittsdatum, 'Austrittsdatum', False)

        self.assertEqual(austrittsdatum, None)

    def test_pflicht_datum_ist_leer(self):
        """
        Test prueft, ob eine Fehlermeldung ausgegeben wird, wenn die uebergegebene Variable, welche nicht leer sein
        darf, denoch leer ist.
        """
        eintrittsdatum = ''

        # Quelle: https://stackoverflow.com/questions/129507/how-do-you-test-that-a-python-function-throws-an-exception
        with self.assertRaises(ValueError) as context:
            eintrittsdatum = self.nutzer._existenz_date_daten_feststellen(eintrittsdatum, 'Eintrittsdatum', True)

        self.assertEqual(str(context.exception), "'Eintrittsdatum' ist nicht vorhanden.")

    def test_falsches_datumsformat(self):
        """
        Test prueft, ob eine Fehlemeldung ausgegeben wird, wenn die uebergegebene Variable ein Datum im falschen Format
        (z.B. englisches statt deutsches Format) ist.
        """
        eintrittsdatum = '01-01-2024'

        # Quelle: https://stackoverflow.com/questions/129507/how-do-you-test-that-a-python-function-throws-an-exception
        with self.assertRaises(ValueError) as context:
            eintrittsdatum = self.nutzer._existenz_date_daten_feststellen(eintrittsdatum, 'Eintrittsdatum', True)

        self.assertEqual(str(context.exception), "'01-01-2024' hat nicht das Muster 'TT.MM.JJJJ'!")

    def test_datum_unmoeglicher_tag(self):
        """
        Test prueft, ob eine Fehlemeldung ausgegeben wird, wenn die uebergegebene Variable ein Datum im richtigen format
        (deutsch), aber der Tag unmoeglich hoch ist (z.B. 32.12.2023).
        """
        eintrittsdatum = '32.12.2023'

        # Quelle: https://stackoverflow.com/questions/129507/how-do-you-test-that-a-python-function-throws-an-exception
        with self.assertRaises(ValueError) as context:
            eintrittsdatum = self.nutzer._existenz_date_daten_feststellen(eintrittsdatum, 'Eintrittsdatum', True)

        self.assertEqual(str(context.exception), "'32.12.2023' ist nicht moeglich!")

    def test_datum_unmoeglicher_hoher_monat(self):
        """
        Test prueft, ob eine Fehlemeldung ausgegeben wird, wenn die uebergegebene Variable ein Datum im richtigen format
        (deutsch), aber der Monat unmoeglich ist (z.B. 31.13.2023).
        """
        eintrittsdatum = '31.13.2023'

        # Quelle: https://stackoverflow.com/questions/129507/how-do-you-test-that-a-python-function-throws-an-exception
        with self.assertRaises(ValueError) as context:
            eintrittsdatum = self.nutzer._existenz_date_daten_feststellen(eintrittsdatum, 'Eintrittsdatum', True)

        self.assertEqual(str(context.exception), "'31.13.2023' ist nicht moeglich!")

    def test_datum_tag_0(self):
        """
        Test prueft, ob eine Fehlemeldung ausgegeben wird, wenn die uebergegebene Variable ein Datum im richtigen format
        (deutsch), aber der Tag 0 ist (z.B. 00.01.2024).
        """
        eintrittsdatum = '00.01.2024'

        # Quelle: https://stackoverflow.com/questions/129507/how-do-you-test-that-a-python-function-throws-an-exception
        with self.assertRaises(ValueError) as context:
            eintrittsdatum = self.nutzer._existenz_date_daten_feststellen(eintrittsdatum, 'Eintrittsdatum', True)

        self.assertEqual(str(context.exception), "'00.01.2024' ist nicht moeglich!")

    def test_datum_monat_0(self):
        """
        Test prueft, ob eine Fehlemeldung ausgegeben wird, wenn die uebergegebene Variable ein Datum im richtigen format
        (deutsch), aber der Monat 0 ist (z.B. 01.00.2024).
        """
        eintrittsdatum = '01.00.2024'

        # Quelle: https://stackoverflow.com/questions/129507/how-do-you-test-that-a-python-function-throws-an-exception
        with self.assertRaises(ValueError) as context:
            eintrittsdatum = self.nutzer._existenz_date_daten_feststellen(eintrittsdatum, 'Eintrittsdatum', True)

        self.assertEqual(str(context.exception), "'01.00.2024' ist nicht moeglich!")

    def test_datum_falsches_schaltjahr(self):
        """
        Test prueft, ob eine Fehlemeldung ausgegeben wird, wenn die uebergegebene Variable ein Datum im richtigen Format
        (deutsch), aber es sich um einen 29. Februar in Jahr handelt, welches kein Schaltjahr ist.
        """
        eintrittsdatum = '29.02.2023'

        # Quelle: https://stackoverflow.com/questions/129507/how-do-you-test-that-a-python-function-throws-an-exception
        with self.assertRaises(ValueError) as context:
            eintrittsdatum = self.nutzer._existenz_date_daten_feststellen(eintrittsdatum, 'Eintrittsdatum', True)

        self.assertEqual(str(context.exception), "'29.02.2023' ist nicht moeglich!")

    def test_datum_richtiges_schaltjahr(self):
        """
        Test prueft, ob die Methode 'existenz_date_daten_feststellen' mit der Angabe 29. Februar zurecht kommt,
        sofern es sich tatsaechlich um ein Schaltjahr handelt.
        """
        eintrittsdatum = '29.02.2024'

        eintrittsdatum = self.nutzer._existenz_date_daten_feststellen(eintrittsdatum, 'Eintrittsdatum', True)

        self.assertEqual(eintrittsdatum, datetime.strptime('29.02.2024', '%d.%m.%Y').date())

    def tearDown(self):
        """
        Methode ruft Funktion 'test_tear_down' auf, welches das Datenbankschema 'temp_test_schema' mit allen Daten
        entfernt.
        """
        test_tear_down()
