import unittest
from src.main.Mandant import Mandant
from src.main.test_SetUp_TearDown import test_set_up, test_tear_down


class TestNutzerInsertAustrittsgrund(unittest.TestCase):

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
        Test prueft, ob ein Austrittsgrund eingetragen wird.
        """
        # Zuerst muss die Austrittsgrundkategorie eingetragen werden, damit dann eine Verknupfung ueber Fremdschluessel
        # zwischen Austrittsgrund und dessen Kategorie vorgenommen werden kann
        self.testfirma.get_nutzer("M100001"). \
            insert_austrittsgrundkategorie('testdaten_insert_austrittsgrundkategorie/Austrittsgrundkategorie.xlsx',
                                           self.testschema)

        self.testfirma.get_nutzer("M100001").\
            insert_austrittsgrund('testdaten_insert_austrittsgrund/Austrittsgrund.xlsx', self.testschema)

        # Inhalt aus Tabelle ziehen, um zu pruefen, ob der Datensatz angelegt wurde
        ergebnis = self.testfirma.get_nutzer("M100001").abfrage_ausfuehren("SELECT * FROM austrittsgruende",
                                                                           self.testschema)

        self.assertEqual(str(ergebnis), "[(1, 1, 'Umsatzrueckgang', 1)]")

    def test_erfolgreicher_eintrag_kategorie_gross(self):
        """
        Test prueft, ob ein Austrittsgrund eingetragen wird, auch wenn die Austrittsgrundkategorie in der Excel-Tabelle
        gross geschrieben wurde.
        Hinweis: die Excel-Datei ist fuer gewoehnlich so praepariert, dass man nur die richtige Rechtschreibung
        fuer die Austrittsgrundkategorie eintragen kann. Dennoch soll getestet werden, ob im Ernstfall die Datenbank die
        Fremdschluesselverknuepfung erstellen kann. Hierfuer wurde die Excel-Datei so umgestaltet, dass man auch gross
        geschriebene Austrittsgrundkategorien eintragen kann.
        """
        # Zuerst muss die Austrittsgrundkategorie eingetragen werden, damit dann eine Verknupfung ueber Fremdschluessel
        # zwischen Austrittsgrund und dessen Kategorie vorgenommen werden kann
        self.testfirma.get_nutzer("M100001"). \
            insert_austrittsgrundkategorie('testdaten_insert_austrittsgrundkategorie/Austrittsgrundkategorie.xlsx',
                                           self.testschema)

        self.testfirma.get_nutzer("M100001").\
            insert_austrittsgrund('testdaten_insert_austrittsgrund/Austrittsgrund - Kategorie gross geschrieben.xlsx',
                                  self.testschema)

        # Inhalt aus Tabelle ziehen, um zu pruefen, ob der Datensatz angelegt wurde
        ergebnis = self.testfirma.get_nutzer("M100001").abfrage_ausfuehren("SELECT * FROM austrittsgruende",
                                                                           self.testschema)

        self.assertEqual(str(ergebnis), "[(1, 1, 'Umsatzrueckgang', 1)]")

    def test_kein_doppelter_eintrag(self):
        """
        Test prueft, ob bei wiederholtem Aufruf der Methode 'insert_austrittsgrund' mit demselben Austrittsgrund
        dieser nicht mehrfach eingetragen wird. Beim zweiten Eintrag muss eine Exception geworfen werden. Ausloeser ist
        der unique-constraint, welcher in der Stored Procedure 'insert_austrittsgruende' implementiert ist.
        """
        # Zuerst muss die Austrittsgrundkategorie eingetragen werden, damit dann eine Verknupfung ueber Fremdschluessel
        # zwischen Austrittsgrund und dessen Kategorie vorgenommen werden kann
        self.testfirma.get_nutzer("M100001"). \
            insert_austrittsgrundkategorie('testdaten_insert_austrittsgrundkategorie/Austrittsgrundkategorie.xlsx',
                                           self.testschema)

        self.testfirma.get_nutzer("M100001"). \
            insert_austrittsgrund('testdaten_insert_austrittsgrund/Austrittsgrund.xlsx', self.testschema)

        # Versuch, denselben Wert noch einmal einzutragen
        with self.assertRaises(Exception) as context:
            self.testfirma.get_nutzer("M100001"). \
                insert_austrittsgrund('testdaten_insert_austrittsgrund/Austrittsgrund.xlsx', self.testschema)

        self.assertEqual(str(context.exception), "FEHLER:  Austrittsgrund 'Umsatzrueckgang' bereits vorhanden!\n"
                                                 "CONTEXT:  PL/pgSQL-Funktion insert_austrittsgrund(integer,character"
                                                 " varying,character varying) Zeile 21 bei RAISE\n")

        # Inhalt aus Tabelle ziehen, um zu pruefen, ob der Datensatz angelegt wurde
        ergebnis = self.testfirma.get_nutzer("M100001").abfrage_ausfuehren("SELECT * FROM austrittsgruende",
                                                                           self.testschema)

        self.assertEqual(str(ergebnis), "[(1, 1, 'Umsatzrueckgang', 1)]")

    def test_kein_doppelter_eintrag_case_insensitive(self):
        """
        Test prueft, ob bei wiederholtem Aufruf der Methode 'insert_austrittsgrund' mit demselben Austrittsgrund aber
        mit Kleinschreibung dieser dennoch nicht mehrfach eingetragen wird. Beim zweiten Eintrag muss eine Exception
        geworfen werden. Ausloeser ist der unique-constraint, welcher in der Stored Procedure 'insert_austrittsgruende'
        implementiert ist, in Kombination mit dem unique-Index 'austrittsgrund_idx'.
        """
        # Zuerst muss die Austrittsgrundkategorie eingetragen werden, damit dann eine Verknupfung ueber Fremdschluessel
        # zwischen Austrittsgrund und dessen Kategorie vorgenommen werden kann
        self.testfirma.get_nutzer("M100001"). \
            insert_austrittsgrundkategorie('testdaten_insert_austrittsgrundkategorie/Austrittsgrundkategorie.xlsx',
                                           self.testschema)

        self.testfirma.get_nutzer("M100001"). \
            insert_austrittsgrund('testdaten_insert_austrittsgrund/Austrittsgrund.xlsx', self.testschema)

        # Versuch, denselben Wert noch einmal einzutragen (diesmal aber in Kleinschreibung)
        with self.assertRaises(Exception) as context:
            self.testfirma.get_nutzer("M100001"). \
                insert_austrittsgrund('testdaten_insert_austrittsgrund/Austrittsgrund - klein geschrieben.xlsx',
                                      self.testschema)

        self.assertEqual(str(context.exception), "FEHLER:  Austrittsgrund 'umsatzrueckgang' bereits vorhanden!\n"
                                                 "CONTEXT:  PL/pgSQL-Funktion insert_austrittsgrund(integer,character"
                                                 " varying,character varying) Zeile 21 bei RAISE\n")

        # Inhalt aus Tabelle ziehen, um zu pruefen, ob der Datensatz angelegt wurde
        ergebnis = self.testfirma.get_nutzer("M100001").abfrage_ausfuehren("SELECT * FROM austrittsgruende",
                                                                           self.testschema)

        self.assertEqual(str(ergebnis), "[(1, 1, 'Umsatzrueckgang', 1)]")

    def tearDown(self):
        """
        Methode ruft Funktion 'test_tear_down' auf, welches das Datenbankschema 'temp_test_schema' mit allen Daten
        entfernt.
        """
        test_tear_down()
