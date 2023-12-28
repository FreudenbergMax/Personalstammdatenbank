import unittest
from src.main.Mandant import Mandant
from src.main.test_SetUp_TearDown import test_set_up, test_tear_down


class TestNutzerInsertMitarbeitertyp(unittest.TestCase):

    def setUp(self):
        """
        Methode ruft Funktion 'test_set_up' der Klasse 'test_SetUp_TearDown' (siehe Ordner 'main') auf, welches das
        Datenbankschema 'temp_test_schema' erstellt.
        """
        self.conn, self.cur, self.testschema = test_set_up()
        self.testfirma = Mandant('Testfirma', self.testschema)
        self.testfirma.nutzer_anlegen('M100001', 'Max', 'Mustermann', self.testschema)

    def test_erfolgreicher_eintrag(self):
        """
        Test prueft, ob ein Mitarbeitertyp eingetragen wird.
        """
        self.testfirma.get_nutzer("M100001").\
            insert_mitarbeitertyp('testdaten_insert_mitarbeitertyp/Mitarbeitertyp.xlsx', self.testschema)

        # Inhalt aus Tabelle ziehen, um zu pruefen, ob der Datensatz angelegt wurde
        ergebnis = self.testfirma.get_nutzer("M100001").\
            abfrage_ausfuehren("SELECT * FROM mitarbeitertypen", self.testschema)

        self.assertEqual(str(ergebnis), "[(1, 1, 'Angestellter')]")

    def test_kein_doppelter_eintrag(self):
        """
        Test prueft, ob bei wiederholtem Aufruf der Methode 'insert_mitarbeitertyp' mit demselben Mitarbeitertypen
        dieser nicht mehrfach eingetragen wird. Beim zweiten Eintrag muss eine Exception geworfen werden. Ausloeser ist
        der unique-constraint, welcher in der Stored Procedure 'insert_mitarbeitertyp' implementiert ist.
        """
        self.testfirma.get_nutzer("M100001").\
            insert_mitarbeitertyp('testdaten_insert_mitarbeitertyp/Mitarbeitertyp.xlsx', self.testschema)

        # Versuch, denselben Wert noch einmal einzutragen
        with self.assertRaises(Exception) as context:
            self.testfirma.get_nutzer("M100001"). \
                insert_mitarbeitertyp('testdaten_insert_mitarbeitertyp/Mitarbeitertyp.xlsx', self.testschema)

        self.assertEqual(str(context.exception), "FEHLER:  Mitarbeitertyp 'Angestellter' bereits vorhanden!\n"
                                                 "CONTEXT:  PL/pgSQL-Funktion insert_mitarbeitertyp(integer,character "
                                                 "varying) Zeile 16 bei RAISE\n")

        # Inhalt aus Tabelle ziehen, um zu pruefen, ob der Datensatz auch nur einmal angelegt wurde
        ergebnis = self.testfirma.get_nutzer("M100001").abfrage_ausfuehren("SELECT * FROM mitarbeitertypen",
                                                                           self.testschema)

        self.assertEqual(str(ergebnis), "[(1, 1, 'Angestellter')]")

    def test_kein_doppelter_eintrag_case_insensitive(self):
        """
        Test prueft, ob bei wiederholtem Aufruf der Methode 'insert_mitarbeitertyp' mit demselben Mitarbeitertypen aber
        mit Kleinschreibung dieser dennoch nicht mehrfach eingetragen wird. Beim zweiten Eintrag muss eine Exception
        geworfen werden. Ausloeser ist der unique-constraint, welcher in der Stored Procedure 'insert_mitarbeitertyp'
        implementiert ist, in Kombination mit dem unique-Index 'mitarbeitertyp_idx'.
        """
        self.testfirma.get_nutzer("M100001"). \
            insert_mitarbeitertyp('testdaten_insert_mitarbeitertyp/Mitarbeitertyp.xlsx', self.testschema)

        # Versuch, denselben Wert noch einmal einzutragen (diesmal aber in Kleinschreibung)
        with self.assertRaises(Exception) as context:
            self.testfirma.get_nutzer("M100001"). \
                insert_mitarbeitertyp('testdaten_insert_mitarbeitertyp/Mitarbeitertyp - klein geschrieben.xlsx',
                                      self.testschema)

        self.assertEqual(str(context.exception), "FEHLER:  Mitarbeitertyp 'angestellter' bereits vorhanden!\n"
                                                 "CONTEXT:  PL/pgSQL-Funktion insert_mitarbeitertyp(integer,character "
                                                 "varying) Zeile 16 bei RAISE\n")

        # Inhalt aus Tabelle ziehen, um zu pruefen, ob der Datensatz auch nur einmal angelegt wurde
        ergebnis = self.testfirma.get_nutzer("M100001").abfrage_ausfuehren("SELECT * FROM mitarbeitertypen",
                                                                           self.testschema)

        self.assertEqual(str(ergebnis), "[(1, 1, 'Angestellter')]")

    def tearDown(self):
        """
        Methode ruft Funktion 'test_tear_down' auf, welches das Datenbankschema 'temp_test_schema' mit allen Daten
        entfernt.
        """
        test_tear_down(self.conn, self.cur)