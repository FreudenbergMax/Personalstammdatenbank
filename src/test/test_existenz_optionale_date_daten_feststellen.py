import unittest
from datetime import datetime

from src.main.test_SetUp import test_set_up
from src.main.Mandant import Mandant


class TestExistenzOptionaleDateDatenFeststellen(unittest.TestCase):

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
        Test prüft, ob die Methode 'existenz_optionale_data_daten_feststellen' ein 'None' zurückgibt, wenn die
        übergegebene Variable ein leerer String ist.
        """
        none_data = ''
        none_data = self.testfirma.get_nutzer('Max', 'Mustermann').\
            _existenz_optionale_date_daten_feststellen(none_data)

        self.assertEqual(none_data, None)

    def tearDown(self):
        """
        Methode entfernt das Test-Schema 'temp_test_schema' inkl. der darin enthaltenen Test-
        Personalstammdatenbank mit allen ihren Tabellen, Stored Procedures und Daten, die während
        der Testfälle erzeugt wurden.
        """
        self.cursor.execute(f"DROP SCHEMA temp_test_schema CASCADE")
        self.conn.commit()
