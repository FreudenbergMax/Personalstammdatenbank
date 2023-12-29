import unittest
from src.main.Mandant import Mandant
from src.main.test_SetUp_TearDown import test_set_up, test_tear_down


class TestNutzerInsertBerufsgenossenschaft(unittest.TestCase):

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
        Test prueft, ob eine Berufsgenossenschaft eingetragen wird.
        """
        self.testfirma.get_nutzer("M100001").\
            insert_berufsgenossenschaft('testdaten_insert_berufsgenossenschaft/Berufsgenossenschaft.xlsx',
                                        self.testschema)

        # Inhalt aus Tabelle ziehen, um zu pruefen, ob der Datensatz angelegt wurde
        ergebnis = self.testfirma.get_nutzer("M100001").\
            abfrage_ausfuehren("SELECT * FROM berufsgenossenschaften", self.testschema)

        self.assertEqual(str(ergebnis), "[(1, 1, 'Berufsgenossenschaft Nahrungsmittel', 'BGN')]")

    def test_kein_doppelter_eintrag_Abteilung_und_abkuerzung_identisch(self):
        """
        Test prueft, ob bei wiederholtem Aufruf der Methode 'insert_berufsgenossenschaft' mit derselben
        Berufsgenossenschaft und Abkuerzung dieser nicht erneut eingetragen wird. Beim zweiten Eintrag muss eine
        Exception geworfen werden. Ausloeser ist der unique-constraint, welcher in der Stored Procedure
        'insert_berufsgenossenschaft' implementiert ist.
        """
        self.testfirma.get_nutzer("M100001"). \
            insert_berufsgenossenschaft('testdaten_insert_berufsgenossenschaft/Berufsgenossenschaft.xlsx',
                                        self.testschema)

        # Versuch, denselben Wert noch einmal einzutragen
        with self.assertRaises(Exception) as context:
            self.testfirma.get_nutzer("M100001"). \
                insert_berufsgenossenschaft('testdaten_insert_berufsgenossenschaft/Berufsgenossenschaft.xlsx',
                                            self.testschema)

        self.assertEqual(str(context.exception), "FEHLER:  Berufsgenossenschaft 'Berufsgenossenschaft Nahrungsmittel' "
                                                 "oder Abkuerzung 'BGN' bereits vorhanden!\n"
                                                 "CONTEXT:  PL/pgSQL-Funktion insert_berufsgenossenschaft(integer,"
                                                 "character varying,character varying) Zeile 16 bei RAISE\n")

        # Inhalt aus Tabelle ziehen, um zu pruefen, ob der Datensatz auch nur einmal angelegt wurde
        ergebnis = self.testfirma.get_nutzer("M100001"). \
            abfrage_ausfuehren("SELECT * FROM berufsgenossenschaften", self.testschema)

        self.assertEqual(str(ergebnis), "[(1, 1, 'Berufsgenossenschaft Nahrungsmittel', 'BGN')]")

    def test_kein_doppelter_eintrag_berufsgenossenschaft_identisch(self):
        """
        Test prueft, ob bei wiederholtem Aufruf der Methode 'insert_berufsgenossenschaft' mit derselben Gesellschaft
        aber anderer Abkuerzung ("BG N" statt "BGN") dieser nicht eingetragen wird. Beim zweiten Eintrag muss eine
        Exception geworfen werden. Ausloeser ist  der unique-constraint, welcher in der Stored Procedure
        'insert_berufsgenossenschaft' implementiert ist.
        """
        self.testfirma.get_nutzer("M100001"). \
            insert_berufsgenossenschaft('testdaten_insert_berufsgenossenschaft/Berufsgenossenschaft.xlsx',
                                        self.testschema)

        # Versuch, denselben Wert noch einmal einzutragen
        with self.assertRaises(Exception) as context:
            self.testfirma.get_nutzer("M100001"). \
                insert_berufsgenossenschaft('testdaten_insert_berufsgenossenschaft/'
                                            'Berufsgenossenschaft - Berufsgenossenschaft identisch.xlsx',
                                            self.testschema)

        self.assertEqual(str(context.exception), "FEHLER:  Berufsgenossenschaft 'Berufsgenossenschaft Nahrungsmittel' "
                                                 "oder Abkuerzung 'BG N' bereits vorhanden!\n"
                                                 "CONTEXT:  PL/pgSQL-Funktion insert_berufsgenossenschaft(integer,"
                                                 "character varying,character varying) Zeile 16 bei RAISE\n")

        # Inhalt aus Tabelle ziehen, um zu pruefen, ob der Datensatz auch nur einmal angelegt wurde
        ergebnis = self.testfirma.get_nutzer("M100001"). \
            abfrage_ausfuehren("SELECT * FROM berufsgenossenschaften", self.testschema)

        self.assertEqual(str(ergebnis), "[(1, 1, 'Berufsgenossenschaft Nahrungsmittel', 'BGN')]")

    def test_kein_doppelter_eintrag_Abkuerzung_identisch(self):
        """
        Test prueft, ob bei wiederholtem Aufruf der Methode 'insert_berufsgenossenschaft' mit anderer Berufsgenossen-
        schaft ('Berufsgenossenschaft Nahrung' statt 'Berufsgenossenschaft Nahrungsmittel') aber identischer Abkuerzung
        dieser nicht eingetragen wird. Beim zweiten Eintrag muss eine Exception geworfen werden. Ausloeser ist
        der unique-constraint, welcher in der Stored Procedure 'insert_berufsgenossenschaft' implementiert ist.
        """
        self.testfirma.get_nutzer("M100001"). \
            insert_berufsgenossenschaft('testdaten_insert_berufsgenossenschaft/Berufsgenossenschaft.xlsx',
                                        self.testschema)

        with self.assertRaises(Exception) as context:
            self.testfirma.get_nutzer("M100001"). \
                insert_berufsgenossenschaft('testdaten_insert_berufsgenossenschaft/'
                                            'Berufsgenossenschaft - Abkuerzung identisch.xlsx',
                                            self.testschema)

        self.assertEqual(str(context.exception), "FEHLER:  Berufsgenossenschaft 'Berufsgenossenschaft Nahrung' oder "
                                                 "Abkuerzung 'BGN' bereits vorhanden!\n"
                                                 "CONTEXT:  PL/pgSQL-Funktion insert_berufsgenossenschaft(integer,"
                                                 "character varying,character varying) Zeile 16 bei RAISE\n")

        # Inhalt aus Tabelle ziehen, um zu pruefen, ob der Datensatz auch nur einmal angelegt wurde
        ergebnis = self.testfirma.get_nutzer("M100001"). \
            abfrage_ausfuehren("SELECT * FROM berufsgenossenschaften", self.testschema)

        self.assertEqual(str(ergebnis), "[(1, 1, 'Berufsgenossenschaft Nahrungsmittel', 'BGN')]")

    def test_kein_doppelter_eintrag_berufsgenossenschaft_case_insensitive(self):
        """
        Test prueft, ob bei wiederholtem Aufruf der Methode 'insert_berufsgenossenschaft' mit derselben Berufs-
        genossenschaft aber mit Kleinschreibung dieser dennoch nicht erneut eingetragen wird. Beim zweiten Eintrag muss
        eine Exception geworfen werden. Ausloeser ist der unique-constraint, welcher in der Stored Procedure
        'insert_berufsgenossenschaft' implementiert ist, in Kombination mit dem unique-Index 'berufsgenossenschaft_idx.
        """
        self.testfirma.get_nutzer("M100001"). \
            insert_berufsgenossenschaft('testdaten_insert_berufsgenossenschaft/Berufsgenossenschaft.xlsx',
                                        self.testschema)

        # Versuch, denselben Wert noch einmal einzutragen (diesmal aber in Kleinschreibung)
        with self.assertRaises(Exception) as context:
            self.testfirma.get_nutzer("M100001"). \
                insert_berufsgenossenschaft('testdaten_insert_berufsgenossenschaft/'
                                            'Berufsgenossenschaft - Berufsgenossenschaft klein geschrieben.xlsx',
                                            self.testschema)

        self.assertEqual(str(context.exception), "FEHLER:  Berufsgenossenschaft 'berufsgenossenschaft nahrungsmittel' "
                                                 "oder Abkuerzung 'BGN' bereits vorhanden!\n"
                                                 "CONTEXT:  PL/pgSQL-Funktion insert_berufsgenossenschaft(integer,"
                                                 "character varying,character varying) Zeile 16 bei RAISE\n")

        # Inhalt aus Tabelle ziehen, um zu pruefen, ob der Datensatz auch nur einmal angelegt wurde
        ergebnis = self.testfirma.get_nutzer("M100001"). \
            abfrage_ausfuehren("SELECT * FROM berufsgenossenschaften", self.testschema)

        self.assertEqual(str(ergebnis), "[(1, 1, 'Berufsgenossenschaft Nahrungsmittel', 'BGN')]")

    def test_kein_doppelter_eintrag_abkuerzung_case_insensitive(self):
        """
        Test prueft, ob bei wiederholtem Aufruf der Methode 'insert_berufsgenossenschaft' mit derselben Abkuerzung aber
        mit Kleinschreibung dieser dennoch nicht erneut eingetragen wird. Beim zweiten Eintrag muss eine Exception
        geworfen werden. Ausloeser ist der unique-constraint, welcher in der Stored Procedure
        'insert_berufsgenossenschaft' implementiert ist, in Kombination mit dem unique-Index
        'Berufsgenossenschaft_abk_idx'.
        """
        self.testfirma.get_nutzer("M100001"). \
            insert_berufsgenossenschaft('testdaten_insert_berufsgenossenschaft/Berufsgenossenschaft.xlsx',
                                        self.testschema)

        # Versuch, denselben Wert noch einmal einzutragen (diesmal aber in Kleinschreibung)
        with self.assertRaises(Exception) as context:
            self.testfirma.get_nutzer("M100001"). \
                insert_berufsgenossenschaft('testdaten_insert_berufsgenossenschaft/'
                                            'Berufsgenossenschaft - Abkuerzung klein geschrieben.xlsx',
                                            self.testschema)

        self.assertEqual(str(context.exception), "FEHLER:  Berufsgenossenschaft 'Berufsgenossenschaft Nahrungsmittel' "
                                                 "oder Abkuerzung 'bgn' bereits vorhanden!\n"
                                                 "CONTEXT:  PL/pgSQL-Funktion insert_berufsgenossenschaft(integer,"
                                                 "character varying,character varying) Zeile 16 bei RAISE\n")

        # Inhalt aus Tabelle ziehen, um zu pruefen, ob der Datensatz auch nur einmal angelegt wurde
        ergebnis = self.testfirma.get_nutzer("M100001"). \
            abfrage_ausfuehren("SELECT * FROM berufsgenossenschaften", self.testschema)

        self.assertEqual(str(ergebnis), "[(1, 1, 'Berufsgenossenschaft Nahrungsmittel', 'BGN')]")

    def tearDown(self):
        """
        Methode ruft Funktion 'test_tear_down' auf, welches das Datenbankschema 'temp_test_schema' mit allen Daten
        entfernt.
        """
        test_tear_down()
