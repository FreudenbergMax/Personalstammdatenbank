import unittest
from src.main.Mandant import Mandant
from src.main.test_SetUp_TearDown import test_set_up, test_tear_down


class TestNutzerInsertAbteilung(unittest.TestCase):

    def setUp(self):
        """
        Methode ruft Funktion 'test_set_up' der Klasse 'test_SetUp_TearDown' (siehe Ordner 'main') auf, welches das
        Datenbankschema 'temp_test_schema' erstellt.
        """
        self.testschema = test_set_up()
        self.testfirma = Mandant('Testfirma', self.testschema)
        self.testfirma.nutzer_anlegen('M100001', 'Max', 'Mustermann', self.testschema)

    def test_erfolgreicher_eintrag(self):
        """
        Test prueft, ob eine Abteilung eingetragen wird.
        """
        self.testfirma.get_nutzer("M100001").\
            insert_abteilung('testdaten_insert_abteilung/Abteilung.xlsx', self.testschema)

        # Inhalt aus Tabelle ziehen, um zu pruefen, ob der Datensatz angelegt wurde
        ergebnis = self.testfirma.get_nutzer("M100001").\
            abfrage_ausfuehren("SELECT * FROM abteilungen", self.testschema)

        self.assertEqual(str(ergebnis), "[(1, 1, 'Human Resources Personalcontrolling', 'HR PC', None)]")

    def test_kein_doppelter_eintrag_Abteilung_und_abkuerzung_identisch(self):
        """
        Test prueft, ob bei wiederholtem Aufruf der Methode 'insert_abteilung' mit derselben Abteilung und Abkuerzung
        dieser nicht mehrfach eingetragen wird. Beim zweiten Eintrag muss eine Exception geworfen werden. Ausloeser ist
        der unique-constraint, welcher in der Stored Procedure 'insert_abteilung' implementiert ist.
        """
        self.testfirma.get_nutzer("M100001"). \
            insert_abteilung('testdaten_insert_abteilung/Abteilung.xlsx', self.testschema)

        # Versuch, denselben Wert noch einmal einzutragen
        with self.assertRaises(Exception) as context:
            self.testfirma.get_nutzer("M100001"). \
                insert_abteilung('testdaten_insert_abteilung/Abteilung.xlsx', self.testschema)

        self.assertEqual(str(context.exception), "FEHLER:  Abteilung 'Human Resources Personalcontrolling' oder "
                                                 "Abteilungskuerzel 'HR PC' bereits vorhanden!\n"
                                                 "CONTEXT:  PL/pgSQL-Funktion insert_abteilung(integer,character "
                                                 "varying,character varying) Zeile 17 bei RAISE\n")

        # Inhalt aus Tabelle ziehen, um zu pruefen, ob der Datensatz auch nur einmal angelegt wurde
        ergebnis = self.testfirma.get_nutzer("M100001").abfrage_ausfuehren("SELECT * FROM abteilungen",
                                                                           self.testschema)

        self.assertEqual(str(ergebnis), "[(1, 1, 'Human Resources Personalcontrolling', 'HR PC', None)]")

    def test_kein_doppelter_eintrag_Abteilung_identisch(self):
        """
        Test prueft, ob bei wiederholtem Aufruf der Methode 'insert_abteilung' mit derselben Abteilung aber anderer
        Abkuerzung dieser nicht eingetragen wird. Beim zweiten Eintrag muss eine Exception geworfen werden.
        Ausloeser ist  der unique-constraint, welcher in der Stored Procedure 'insert_abteilung' implementiert ist.
        """
        self.testfirma.get_nutzer("M100001"). \
            insert_abteilung('testdaten_insert_abteilung/Abteilung.xlsx', self.testschema)

        # Versuch, denselben Wert noch einmal einzutragen
        with self.assertRaises(Exception) as context:
            self.testfirma.get_nutzer("M100001"). \
                insert_abteilung('testdaten_insert_abteilung/Abteilung - Abteilung identisch.xlsx', self.testschema)

        self.assertEqual(str(context.exception), "FEHLER:  Abteilung 'Human Resources Personalcontrolling' oder "
                                                 "Abteilungskuerzel 'HRPC' bereits vorhanden!\n"
                                                 "CONTEXT:  PL/pgSQL-Funktion insert_abteilung(integer,character "
                                                 "varying,character varying) Zeile 17 bei RAISE\n")

        # Inhalt aus Tabelle ziehen, um zu pruefen, ob der Datensatz auch nur einmal angelegt wurde
        ergebnis = self.testfirma.get_nutzer("M100001").abfrage_ausfuehren("SELECT * FROM abteilungen",
                                                                           self.testschema)

        self.assertEqual(str(ergebnis), "[(1, 1, 'Human Resources Personalcontrolling', 'HR PC', None)]")

    def test_kein_doppelter_eintrag_Abkuerzung_identisch(self):
        """
        Test prueft, ob bei wiederholtem Aufruf der Methode 'insert_abteilung' mit anderer Abteilung aber identischer
        Abkuerzung dieser nicht eingetragen wird. Beim zweiten Eintrag muss eine Exception geworfen werden.
        Ausloeser ist  der unique-constraint, welcher in der Stored Procedure 'insert_abteilung' implementiert ist.
        """
        self.testfirma.get_nutzer("M100001"). \
            insert_abteilung('testdaten_insert_abteilung/Abteilung.xlsx', self.testschema)

        # Versuch, denselben Wert noch einmal einzutragen
        with self.assertRaises(Exception) as context:
            self.testfirma.get_nutzer("M100001"). \
                insert_abteilung('testdaten_insert_abteilung/Abteilung - Abkuerzung identisch.xlsx', self.testschema)

        self.assertEqual(str(context.exception), "FEHLER:  Abteilung 'HumanResources Personalcontrolling' oder "
                                                 "Abteilungskuerzel 'HR PC' bereits vorhanden!\n"
                                                 "CONTEXT:  PL/pgSQL-Funktion insert_abteilung(integer,character "
                                                 "varying,character varying) Zeile 17 bei RAISE\n")

        # Inhalt aus Tabelle ziehen, um zu pruefen, ob der Datensatz auch nur einmal angelegt wurde
        ergebnis = self.testfirma.get_nutzer("M100001").abfrage_ausfuehren("SELECT * FROM abteilungen",
                                                                           self.testschema)

        self.assertEqual(str(ergebnis), "[(1, 1, 'Human Resources Personalcontrolling', 'HR PC', None)]")

    def test_kein_doppelter_eintrag_abteilung_case_insensitive(self):
        """
        Test prueft, ob bei wiederholtem Aufruf der Methode 'insert_abteilung' mit derselben Abteilung aber mit Klein-
        schreibung dieser dennoch nicht mehrfach eingetragen wird. Beim zweiten Eintrag muss eine Exception geworfen
        werden. Ausloeser ist der unique-constraint, welcher in der Stored Procedure 'insert_abteilung'
        implementiert ist, in Kombination mit dem unique-Index 'abteilung_idx'.
        """
        self.testfirma.get_nutzer("M100001"). \
            insert_abteilung('testdaten_insert_abteilung/Abteilung.xlsx', self.testschema)

        # Versuch, denselben Wert noch einmal einzutragen (diesmal aber in Kleinschreibung)
        with self.assertRaises(Exception) as context:
            self.testfirma.get_nutzer("M100001"). \
                insert_abteilung('testdaten_insert_abteilung/Abteilung - Abteilung klein geschrieben.xlsx',
                                 self.testschema)

        self.assertEqual(str(context.exception), "FEHLER:  Abteilung 'human resources personalcontrolling' oder "
                                                 "Abteilungskuerzel 'HR PC' bereits vorhanden!\n"
                                                 "CONTEXT:  PL/pgSQL-Funktion insert_abteilung(integer,character "
                                                 "varying,character varying) Zeile 17 bei RAISE\n")

        # Inhalt aus Tabelle ziehen, um zu pruefen, ob der Datensatz auch nur einmal angelegt wurde
        ergebnis = self.testfirma.get_nutzer("M100001").abfrage_ausfuehren("SELECT * FROM abteilungen",
                                                                           self.testschema)

        self.assertEqual(str(ergebnis), "[(1, 1, 'Human Resources Personalcontrolling', 'HR PC', None)]")

    def test_kein_doppelter_eintrag_abkuerzung_case_insensitive(self):
        """
        Test prueft, ob bei wiederholtem Aufruf der Methode 'insert_abteilung' mit derselben Abkuerzung aber mit Klein-
        schreibung dieser dennoch nicht mehrfach eingetragen wird. Beim zweiten Eintrag muss eine Exception geworfen
        werden. Ausloeser ist der unique-constraint, welcher in der Stored Procedure 'insert_abteilung'
        implementiert ist, in Kombination mit dem unique-Index 'abk_abteilung_idx'.
        """
        self.testfirma.get_nutzer("M100001"). \
            insert_abteilung('testdaten_insert_abteilung/Abteilung.xlsx', self.testschema)

        # Versuch, denselben Wert noch einmal einzutragen (diesmal aber in Kleinschreibung)
        with self.assertRaises(Exception) as context:
            self.testfirma.get_nutzer("M100001"). \
                insert_abteilung('testdaten_insert_abteilung/Abteilung - Abkuerzung klein geschrieben.xlsx',
                                 self.testschema)

        self.assertEqual(str(context.exception), "FEHLER:  Abteilung 'Human Resources Personalcontrolling' oder "
                                                 "Abteilungskuerzel 'hr pc' bereits vorhanden!\n"
                                                 "CONTEXT:  PL/pgSQL-Funktion insert_abteilung(integer,character "
                                                 "varying,character varying) Zeile 17 bei RAISE\n")

        # Inhalt aus Tabelle ziehen, um zu pruefen, ob der Datensatz auch nur einmal angelegt wurde
        ergebnis = self.testfirma.get_nutzer("M100001").abfrage_ausfuehren("SELECT * FROM abteilungen",
                                                                           self.testschema)

        self.assertEqual(str(ergebnis), "[(1, 1, 'Human Resources Personalcontrolling', 'HR PC', None)]")

    def tearDown(self):
        """
        Methode ruft Funktion 'test_tear_down' auf, welches das Datenbankschema 'temp_test_schema' mit allen Daten
        entfernt.
        """
        test_tear_down()
