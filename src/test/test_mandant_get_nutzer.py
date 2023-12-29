import unittest
from src.main.Mandant import Mandant
from src.main.test_SetUp_TearDown import test_set_up, test_tear_down


class TestGetNutzer(unittest.TestCase):

    def setUp(self):
        """
        Methode ruft Funktion 'test_set_up' der Klasse 'test_SetUp_TearDown' (siehe Ordner 'main') auf, welches das
        Datenbankschema 'temp_test_schema' erstellt.
        """
        self.testschema = test_set_up()

    def test_nutzer_objekt_vorhanden(self):
        """
        Test prüft, ob ein tatsächlich angelegter Nutzer mithilfe der Methode 'get_nutzer' gefunden und übergeben wird
        """
        testfirma = Mandant('Testfirma', self.testschema)
        testfirma.nutzer_anlegen('M10001', 'Max', 'Mustermann', self.testschema)

        gesuchter_nutzer = testfirma.get_nutzer('M10001')

        self.assertEqual(gesuchter_nutzer.get_vorname(), 'Max')
        self.assertEqual(gesuchter_nutzer.get_nachname(), 'Mustermann')

    def test_nutzer_objekt_nicht_vorhanden(self):
        """
        Test prüft, ob bei der Eingabe eines nicht vorhandenen Nutzers eine Fehlermeldung kommt.
        """
        testfirma = Mandant('Testfirma', self.testschema)

        with self.assertRaises(ValueError) as context:
            testfirma.get_nutzer('M10001')
        self.assertEqual(str(context.exception), "Nutzer mit Personalnummer M10001 nicht vorhanden!")

    def test_kein_zugriff_auf_nutzer_anderer_mandanten(self):
        """
        Test prüft, ob Mandant A keinen Zugriff auf Nutzer des Mandanten B hat und umgekehrt.
        """
        A = Mandant('A', self.testschema)
        A.nutzer_anlegen('M10001', 'Max', 'Mustermann', self.testschema)

        B = Mandant('B', self.testschema)
        B.nutzer_anlegen('111111', 'Erika', 'Musterfrau', self.testschema)

        with self.assertRaises(ValueError) as context:
            gesuchter_nutzer = A.get_nutzer('111111')
        self.assertEqual(str(context.exception), 'Nutzer mit Personalnummer 111111 nicht vorhanden!')

        with self.assertRaises(ValueError) as context:
            gesuchter_nutzer = B.get_nutzer('M10001')
        self.assertEqual(str(context.exception), 'Nutzer mit Personalnummer M10001 nicht vorhanden!')

    def tearDown(self):
        """
        Methode ruft Funktion 'test_tear_down' auf, welches das Datenbankschema 'temp_test_schema' mit allen Daten
        entfernt.
        """
        test_tear_down()
