import unittest
from src.main.Mandant import Mandant
from src.main.test_SetUp import test_set_up


class TestNutzerEntfernen(unittest.TestCase):

    def setUp(self):
        """
        Methode erstellt ein Testschema 'temp_test_schema' und darin die Personalstammdatenbank
        mit allen Tabellen und Stored Procedures. So können alle Tests ausgeführt werden, ohne die
        originale Datenbank zu manipulieren.
        """
        self.conn, self.cursor = test_set_up()

    def test_nutzer_aus_Nutzerliste_entfernen(self):
        """
        Test prüft, ob nach Ausführung der Methode 'nutzer_entfernen' das Nutzerobjekt in der Liste des
        Mandant-Objekts entfernt wurde.
        """
        testfirma = Mandant('Testfirma', self.conn)
        testfirma.nutzer_anlegen('M100001', 'Max', 'Mustermann', self.conn)

        # Zwischenprüfung, ob Nutzer in Nutzerliste angelegt ist
        gesuchter_nutzer = testfirma.get_nutzer('M100001')
        self.assertEqual(gesuchter_nutzer.get_vorname(), 'Max')
        self.assertEqual(gesuchter_nutzer.get_nachname(), 'Mustermann')

        # Prüfung, ob Nutzer nun entfernt wird
        testfirma.nutzer_entfernen('M100001', self.conn)

        with self.assertRaises(ValueError) as context:
            testfirma.get_nutzer('M100001')
        self.assertEqual(str(context.exception), "Nutzer mit Personalnummer M100001 nicht vorhanden!")

    def test_kein_entfernen_von_nutzer_anderer_mandanten(self):
        pass

    def tearDown(self):
        """
        Methode entfernt das Test-Schema 'temp_test_schema' inkl. der darin enthaltenen Test-
        Personalstammdatenbank mit allen ihren Tabellen, Stored Procedures und Daten, die während
        der Testfälle erzeugt wurden.
        """
        self.cursor.execute(f"DROP SCHEMA temp_test_schema CASCADE")
        self.conn.commit()
