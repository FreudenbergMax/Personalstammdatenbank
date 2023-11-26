import unittest
from src.main.Mandant import Mandant
from src.main.test_SetUp import test_set_up


class TestGetNutzer(unittest.TestCase):

    def setUp(self):
        """
        Methode erstellt ein Testschema 'temp_test_schema' und darin die Personalstammdatenbank
        mit allen Tabellen und Stored Procedures. So können alle Tests ausgeführt werden, ohne die
        originale Datenbank zu manipulieren.
        :return:
        """
        self.conn, self.cursor = test_set_up()

    def test_nutzer_objekt_vorhanden(self):
        """
        Test prüft, ob ein tatsächlich angelegter Nutzer mithilfe der Methode 'get_nutzer' gefunden und übergeben wird
        """
        testfirma = Mandant('Testfirma', self.conn)
        testfirma.nutzer_anlegen('Max', 'Mustermann', self.conn)

        gesuchter_nutzer = testfirma.get_nutzer('Max', 'Mustermann')

        self.assertEqual(gesuchter_nutzer.get_vorname(), 'Max')
        self.assertEqual(gesuchter_nutzer.get_nachname(), 'Mustermann')

    def test_nutzer_objekt_nicht_vorhanden(self):
        """
        Test prüft, ob bei der Eingabe eines nicht vorhandenen Nutzers eine Fehlermeldung kommt.
        """
        testfirma = Mandant('Testfirma', self.conn)

        with self.assertRaises(ValueError) as context:
            gesuchter_nutzer = testfirma.get_nutzer('Max', 'Mustermann')
        self.assertEqual(str(context.exception), 'Nutzer Max Mustermann nicht vorhanden!')

    def test_kein_zugriff_auf_nutzer_anderer_mandanten(self):
        """
        Test prüft, ob Mandant A keinen Zugriff auf Nutzer des Mandanten B hat und umgekehrt.
        """
        A = Mandant('A', self.conn)
        A.nutzer_anlegen('Max', 'Mustermann', self.conn)

        B = Mandant('B', self.conn)
        B.nutzer_anlegen('Erika', 'Musterfrau', self.conn)

        with self.assertRaises(ValueError) as context:
            gesuchter_nutzer = A.get_nutzer('Erika', 'Musterfrau')
        self.assertEqual(str(context.exception), 'Nutzer Erika Musterfrau nicht vorhanden!')

        with self.assertRaises(ValueError) as context:
            gesuchter_nutzer = B.get_nutzer('Max', 'Mustermann')
        self.assertEqual(str(context.exception), 'Nutzer Max Mustermann nicht vorhanden!')

    def tearDown(self):
        """
        Methode entfernt das Test-Schema 'temp_test_schema' inkl. der darin enthaltenen Test-
        Personalstammdatenbank mit allen ihren Tabellen, Stored Procedures und Daten, die während
        der Testfälle erzeugt wurden.
        """
        self.cursor.execute(f"DROP SCHEMA temp_test_schema CASCADE")
        self.conn.commit()
