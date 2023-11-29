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

    def test_nutzer_aus_db_entfernen(self):
        """
        Test prüft, ob nach Ausführung der Methode 'nutzer_entfernen' das Nutzerobjekt in der Liste des
        Mandant-Objekts entfernt wurde.
        """
        testfirma = Mandant('Testfirma', self.conn)
        testfirma.nutzer_anlegen('M100001', 'Max', 'Mustermann', self.conn)

        # Zwischenprüfung, ob Nutzer in Datenbank angelegt ist
        select_query = "SELECT * FROM nutzer WHERE personalnummer = 'M100001'"

        cur1 = self.conn.cursor()
        cur1.execute(select_query)
        nutzer_id, mandant_id, personalnummer, vorname, nachname = cur1.fetchall()[0]

        self.assertEqual(nutzer_id, 1)
        self.assertEqual(mandant_id, 1)
        self.assertEqual(personalnummer, 'M100001')
        self.assertEqual(vorname, 'Max')
        self.assertEqual(nachname, 'Mustermann')

        # Nutzer entfernen
        testfirma.nutzer_entfernen('M100001', self.conn)

        # Prüfung, ob Nutzer aus Datenbank entfernt wurde
        select_query = "SELECT * FROM nutzer WHERE personalnummer = 'M100001'"

        cur2 = self.conn.cursor()
        cur2.execute(select_query)
        leere_liste = cur2.fetchall()

        self.assertEqual(leere_liste, list())

    def test_nutzer_fremder_mandanten_aus_nutzerliste_entfernen(self):
        """
        Test prüft, ob Mandant A einen Nutzer aus der Nutzerliste von Mandant B löschen kann, falls der Nutzer von
        Mandant B zufälligerweise die Personalnummer haben sollte, die Mandant A entfernen möchte.
        """
        A = Mandant('A', self.conn)
        A.nutzer_anlegen('M100001', 'Max', 'Mustermann', self.conn)

        B = Mandant('B', self.conn)
        B.nutzer_anlegen('M1234', 'Erika', 'Musterfrau', self.conn)

        A.nutzer_entfernen('M1234', self.conn)
        nutzer_erika = B.get_nutzer('M1234').get_personalnummer()
        self.assertEqual(nutzer_erika, 'M1234')

        B.nutzer_entfernen('M100001', self.conn)
        nutzer_max = A.get_nutzer('M100001').get_personalnummer()
        self.assertEqual(nutzer_max, 'M100001')

    def test_nutzer_fremder_mandanten_aus_datenbank_entfernen(self):
        """
        Test prüft, ob Mandant A in der Datenbank einen Nutzer von Mandant B löschen kann, falls der Nutzer von
        Mandant B zufälligerweise die Personalnummer haben sollte, die Mandant A entfernen möchte.
        """
        A = Mandant('A', self.conn)
        A.nutzer_anlegen('M100001', 'Max', 'Mustermann', self.conn)

        B = Mandant('B', self.conn)
        B.nutzer_anlegen('M1234', 'Erika', 'Musterfrau', self.conn)

        # Zwischenprüfung, ob Nutzer 'M1234' von Mandant B in Datenbank angelegt ist
        select_query = "SELECT * FROM nutzer WHERE personalnummer = 'M1234'"

        cur1 = self.conn.cursor()
        cur1.execute(select_query)
        nutzer_id, mandant_id, personalnummer, vorname, nachname = cur1.fetchall()[0]

        self.assertEqual(nutzer_id, 2)
        self.assertEqual(mandant_id, 2)
        self.assertEqual(personalnummer, 'M1234')
        self.assertEqual(vorname, 'Erika')
        self.assertEqual(nachname, 'Musterfrau')

        # Mandant A versucht nun, Nutzer 'M1234' von Mandant B zu entfernen
        A.nutzer_entfernen('M1234', self.conn)

        # Prüfung, ob Nutzer 'M1234' von Mandant B aus Datenbank entfernt wurde
        select_query = "SELECT * FROM nutzer WHERE personalnummer = 'M1234'"

        cur2 = self.conn.cursor()
        cur2.execute(select_query)
        nutzer_id, mandant_id, personalnummer, vorname, nachname = cur2.fetchall()[0]

        self.assertEqual(nutzer_id, 2)
        self.assertEqual(mandant_id, 2)
        self.assertEqual(personalnummer, 'M1234')
        self.assertEqual(vorname, 'Erika')
        self.assertEqual(nachname, 'Musterfrau')

    def tearDown(self):
        """
        Methode entfernt das Test-Schema 'temp_test_schema' inkl. der darin enthaltenen Test-
        Personalstammdatenbank mit allen ihren Tabellen, Stored Procedures und Daten, die während
        der Testfälle erzeugt wurden.
        """
        self.cursor.execute(f"DROP SCHEMA temp_test_schema CASCADE")
        self.conn.commit()
