import unittest
from src.main.Mandant import Mandant
from src.main.test_SetUp_TearDown import test_set_up, test_tear_down


class TestNutzerEntfernen(unittest.TestCase):

    def setUp(self):
        """
        Methode ruft Funktion 'test_set_up' der Klasse 'test_SetUp_TearDown' (siehe Ordner 'main') auf, welches das
        Datenbankschema 'temp_test_schema' erstellt.
        """
        self.conn, self.cur, self.testschema = test_set_up()

    def test_nutzer_aus_Nutzerliste_entfernen(self):
        """
        Test prüft, ob nach Ausführung der Methode 'nutzer_entfernen' das Nutzerobjekt in der Liste des
        Mandant-Objekts entfernt wurde.
        """
        testfirma = Mandant('Testfirma', self.testschema)
        testfirma.nutzer_anlegen('M100001', 'Max', 'Mustermann', self.testschema)

        # Zwischenprüfung, ob Nutzer in Nutzerliste angelegt ist
        gesuchter_nutzer = testfirma.get_nutzer('M100001')
        self.assertEqual(gesuchter_nutzer.get_vorname(), 'Max')
        self.assertEqual(gesuchter_nutzer.get_nachname(), 'Mustermann')

        # Prüfung, ob Nutzer nun entfernt wird
        testfirma.nutzer_entfernen('M100001')

        with self.assertRaises(ValueError) as context:
            testfirma.get_nutzer('M100001')
        self.assertEqual(str(context.exception), "Nutzer mit Personalnummer M100001 nicht vorhanden!")

    def test_nutzer_aus_db_entfernen(self):
        """
        Test prüft, ob nach Ausführung der Methode 'nutzer_entfernen' das Nutzerobjekt in der Liste des
        Mandant-Objekts entfernt wurde.
        """
        testfirma = Mandant('Testfirma', self.testschema)
        testfirma.nutzer_anlegen('M100001', 'Max', 'Mustermann', self.testschema)

        # Zwischenprüfung, ob Nutzer in Datenbank angelegt ist
        select_query = "SELECT * FROM nutzer WHERE personalnummer = 'M100001'"
        self.cur.execute(select_query)
        daten = self.cur.fetchall()

        self.assertEqual(str(daten), "[(1, 1, 'M100001', 'Max', 'Mustermann')]")

        # Nutzer entfernen
        testfirma.nutzer_entfernen('M100001')

        # Prüfung, ob Nutzer aus Datenbank entfernt wurde
        select_query = "SELECT * FROM nutzer WHERE personalnummer = 'M100001'"
        self.cur = self.conn.cursor()
        self.cur.execute(select_query)
        leere_liste = self.cur.fetchall()

        self.assertEqual(str(leere_liste), "[]")

    def test_nutzer_fremder_mandanten_aus_nutzerliste_entfernen(self):
        """
        Test prüft, ob Mandant A einen Nutzer aus der Nutzerliste von Mandant B löschen kann, falls der Nutzer von
        Mandant B zufälligerweise die Personalnummer haben sollte, die Mandant A entfernen möchte.
        """
        A = Mandant('A', self.testschema)
        A.nutzer_anlegen('M100001', 'Max', 'Mustermann', self.testschema)

        B = Mandant('B', self.testschema)
        B.nutzer_anlegen('M1234', 'Erika', 'Musterfrau', self.testschema)

        A.nutzer_entfernen('M1234')
        nutzer_erika = B.get_nutzer('M1234').get_personalnummer()
        self.assertEqual(nutzer_erika, 'M1234')

        B.nutzer_entfernen('M100001')
        nutzer_max = A.get_nutzer('M100001').get_personalnummer()
        self.assertEqual(nutzer_max, 'M100001')

    def test_nutzer_fremder_mandanten_aus_datenbank_entfernen(self):
        """
        Test prüft, ob Mandant A in der Datenbank einen Nutzer von Mandant B löschen kann, falls der Nutzer von
        Mandant B zufälligerweise die Personalnummer haben sollte, die Mandant A entfernen möchte.
        """
        A = Mandant('A', self.testschema)
        A.nutzer_anlegen('M100001', 'Max', 'Mustermann', self.testschema)

        B = Mandant('B', self.testschema)
        B.nutzer_anlegen('M1234', 'Erika', 'Musterfrau', self.testschema)

        # Zwischenprüfung, ob Nutzer 'M1234' von Mandant B in Datenbank angelegt ist
        select_query = "SELECT * FROM nutzer WHERE personalnummer = 'M1234'"
        self.cur.execute(select_query)
        daten = self.cur.fetchall()

        self.assertEqual(str(daten), "[(2, 2, 'M1234', 'Erika', 'Musterfrau')]")

        # Mandant A versucht nun, Nutzer 'M1234' von Mandant B zu entfernen
        A.nutzer_entfernen('M1234')

        # Prüfung, ob Nutzer 'M1234' von Mandant B aus Datenbank entfernt wurde. Nutzer 'M1234' muss vorhanden sein
        # und die Datenbank muss die entsprechenden Daten ausgeben können
        select_query = "SELECT * FROM nutzer WHERE personalnummer = 'M1234'"
        self.cur.execute(select_query)
        daten = self.cur.fetchall()

        self.assertEqual(str(daten), "[(2, 2, 'M1234', 'Erika', 'Musterfrau')]")


    def tearDown(self):
        """
        Methode ruft Funktion 'test_tear_down' auf, welches das Datenbankschema 'temp_test_schema' mit allen Daten
        entfernt.
        """
        test_tear_down(self.conn, self.cur)
