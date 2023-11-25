import unittest
from datetime import datetime

from src.main.test_SetUp import test_set_up
from src.main.Mandant import Mandant


class TestExistenzOptionaleStrDatenFeststellen(unittest.TestCase):

    def setUp(self):
        """
        Methode erstellt ein Testschema 'temp_test_schema' und darin die Personalstammdatenbank
        mit allen Tabellen und Stored Procedures. So können alle Tests ausgeführt werden, ohne die
        originale Datenbank zu manipulieren.
        """
        self.conn, self.cursor = test_set_up()
        self.testfirma = Mandant('Testfirma', self.conn)
        self.testfirma.nutzer_anlegen('Max', 'Mustermann', self.conn)

    def test_zeichenkette_ist_leer(self):
        """
        Test prüft, ob die Methode 'existenz_optionale_str_daten_feststellen' ein 'None' zurückgibt, wenn die
        übergegebene Variable ein leerer String ist.
        """
        none_data = ''
        none_data = self.testfirma.get_nutzer('Max', 'Mustermann').\
            _existenz_optionale_str_daten_feststellen(none_data, 'none_data', 0)

        self.assertEqual(none_data, None)

    def test_ganzzahl_wird_str(self):
        """
        Test prüft, ob die Methode 'existenz_optionale_str_daten_feststellen' ein 'str' zurückgibt, wenn die
        übergegebene Variable anfangs als Ganzzahl gelesen wird, aber eigentlich als Zeichenkette in die Datenbank
        übertragen werden soll.
        """
        postleitzahl = 12345
        postleitzahl = self.testfirma.get_nutzer('Max', 'Mustermann').\
            _existenz_optionale_str_daten_feststellen(postleitzahl, 'Postleitzahl', 5)

        self.assertEqual(type(postleitzahl), str)

    def test_gleitkommazahl_wird_str(self):
        """
        Test prüft, ob die Methode 'existenz_optionale_str_daten_feststellen' ein 'str' zurückgibt, wenn die
        übergegebene Variable anfangs als Gleitkomma gelesen wird, aber eigentlich als Zeichenkette in die Datenbank
        übertragen werden soll.
        """
        double = 12.45
        double = self.testfirma.get_nutzer('Max', 'Mustermann')._existenz_optionale_str_daten_feststellen(
            double, 'Postleitzahl', 5)

        self.assertEqual(type(double), str)

    def test_datum_wird_str(self):
        """
        Test prüft, ob die Methode 'existenz_optionale_str_daten_feststellen' ein 'str' zurückgibt, wenn die
        übergegebene Variable anfangs (unerwarteterweise) als Datum gelesen wird, aber eigentlich als Zeichenkette in
        die Datenbank übertragen werden soll.
        """
        date_daten = datetime.strptime('12.12.1992', '%d.%m.%Y').date()
        date_daten = self.testfirma.get_nutzer('Max', 'Mustermann')._existenz_optionale_str_daten_feststellen(
            date_daten, 'Postleitzahl', 10)

        self.assertEqual(type(date_daten), str)

    def tearDown(self):
        """
        Methode entfernt das Test-Schema 'temp_test_schema' inkl. der darin enthaltenen Test-
        Personalstammdatenbank mit allen ihren Tabellen, Stored Procedures und Daten, die während
        der Testfälle erzeugt wurden.
        """
        self.cursor.execute(f"DROP SCHEMA temp_test_schema CASCADE")
        self.conn.commit()
