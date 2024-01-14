import unittest
from src.main.Mandant import Mandant
from src.main.test_SetUp_TearDown import test_set_up, test_tear_down


class TestNutzerInsertGewerkschaft(unittest.TestCase):

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
        Test prueft, ob eine Gewerkschaft eingetragen wird.
        """
        self.testfirma.get_nutzer("M100001").\
            insert_gewerkschaft('testdaten_insert_gewerkschaft/Gewerkschaft.xlsx', self.testschema)

        # Inhalt aus Tabelle ziehen, um zu pruefen, ob der Datensatz angelegt wurde
        ergebnis = self.testfirma.get_nutzer("M100001").\
            abfrage_ausfuehren("SELECT * FROM gewerkschaften", self.testschema)

        self.assertEqual(str(ergebnis), "[(1, 1, 'Verdi')]")

    def test_kein_doppelter_eintrag(self):
        """
        Test prueft, ob bei wiederholtem Aufruf der Methode 'insert_gewerkschaft' mit derselben Gewerkschaft
        dieser nicht erneut eingetragen wird. Beim zweiten Eintrag muss eine Exception geworfen werden.
        Ausloeser ist der unique-constraint der Tabelle "Gewerkschaften" der fuer jeden Mandanten die mehrmalige
        identische Eintragung derselben Gewerkschaft verbietet.
        """
        self.testfirma.get_nutzer("M100001"). \
            insert_gewerkschaft('testdaten_insert_gewerkschaft/Gewerkschaft.xlsx', self.testschema)

        # Versuch, denselben Wert noch einmal einzutragen
        with self.assertRaises(Exception) as context:
            self.testfirma.get_nutzer("M100001"). \
                insert_gewerkschaft('testdaten_insert_gewerkschaft/Gewerkschaft.xlsx', self.testschema)

        self.assertEqual(str(context.exception), "FEHLER:  Gewerkschaft 'Verdi' bereits vorhanden!\n"
                                                 "CONTEXT:  PL/pgSQL-Funktion insert_gewerkschaft(integer,character "
                                                 "varying) Zeile 14 bei RAISE\n")

        # Inhalt aus Tabelle ziehen, um zu pruefen, ob der Datensatz auch nur einmal angelegt wurde
        ergebnis = self.testfirma.get_nutzer("M100001"). \
            abfrage_ausfuehren("SELECT * FROM gewerkschaften", self.testschema)

        self.assertEqual(str(ergebnis), "[(1, 1, 'Verdi')]")

    def test_kein_doppelter_eintrag_case_insensitive(self):
        """
        Test prueft, ob bei wiederholtem Aufruf der Methode 'insert_gewerkschaft' mit derselben Gewerkschaft aber mit
        Kleinschreibung dieser dennoch nicht erneut eingetragen wird. Beim zweiten Eintrag muss eine Exception
        geworfen werden. Ausloeser ist der unique-constraint in Kombination mit dem unique-Index 'gewerkschaft_idx'.
        """
        self.testfirma.get_nutzer("M100001"). \
            insert_gewerkschaft('testdaten_insert_gewerkschaft/Gewerkschaft.xlsx', self.testschema)

        # Versuch, denselben Wert noch einmal einzutragen (diesmal aber in Kleinschreibung)
        with self.assertRaises(Exception) as context:
            self.testfirma.get_nutzer("M100001"). \
                insert_gewerkschaft('testdaten_insert_gewerkschaft/Gewerkschaft - klein geschrieben.xlsx',
                                    self.testschema)

        self.assertEqual(str(context.exception), "FEHLER:  Gewerkschaft 'verdi' bereits vorhanden!\n"
                                                 "CONTEXT:  PL/pgSQL-Funktion insert_gewerkschaft(integer,character "
                                                 "varying) Zeile 14 bei RAISE\n")

        # Inhalt aus Tabelle ziehen, um zu pruefen, ob der Datensatz auch nur einmal angelegt wurde
        ergebnis = self.testfirma.get_nutzer("M100001"). \
            abfrage_ausfuehren("SELECT * FROM gewerkschaften", self.testschema)

        self.assertEqual(str(ergebnis), "[(1, 1, 'Verdi')]")

    def tearDown(self):
        """
        Methode ruft Funktion 'test_tear_down' auf, welches das Datenbankschema 'temp_test_schema' mit allen Daten
        entfernt.
        """
        test_tear_down()
