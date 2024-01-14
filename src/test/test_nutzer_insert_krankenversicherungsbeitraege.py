import unittest
from src.main.Mandant import Mandant
from src.main.test_SetUp_TearDown import test_set_up, test_tear_down


class TestNutzerInsertKrankenversicherungsbeitraege(unittest.TestCase):

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
        Test prueft, ob Krankenversicherungsbeitraege eingetragen werden.
        """
        self.testfirma.get_nutzer("M100001").\
            insert_krankenversicherungsbeitraege('testdaten_insert_krankenversicherungsbeitraege/'
                                                 'Krankenversicherungsbeitraege.xlsx', self.testschema)

        # Inhalte aus Tabellen ziehen, um zu pruefen, ob der Datensatz angelegt wurde
        ergebnis = self.testfirma.get_nutzer("M100001").abfrage_ausfuehren("SELECT * FROM gkv_beitraege",
                                                                           self.testschema)
        self.assertEqual(str(ergebnis), "[(1, 1, Decimal('7.300'), Decimal('7.300'), Decimal('72453.56'), "
                                        "Decimal('75683.12'))]")

        ergebnis = self.testfirma.get_nutzer("M100001").abfrage_ausfuehren("SELECT * FROM krankenversicherungen",
                                                                           self.testschema)
        self.assertEqual(str(ergebnis), "[(1, 1, False)]")

        ergebnis = self.testfirma.get_nutzer("M100001").abfrage_ausfuehren("SELECT * FROM hat_GKV_Beitraege",
                                                                           self.testschema)
        self.assertEqual(str(ergebnis), "[(1, 1, 1, datetime.date(2023, 12, 15), datetime.date(9999, 12, 31))]")

    def test_kein_doppelter_eintrag(self):
        """
        Test prueft, ob bei wiederholtem Aufruf der Methode 'insert_krankenversicherungsbeitraege' mit derselben Angabe,
        ob es der ermaessigte Beitrag ist, und denselben Beitragssaetzen dieser nicht erneut eingetragen wird. Beim
        zweiten Eintrag muss eine Exception geworfen werden. Massgeblich sit hier lediglich der boolesche Wert
        "ermaessigter_beitragssatz" in Tabelle "Krankenversicherungen". Die Exception wird auch dann geworfen, wenn die
        Beitragssaetze anders sind. Sollen nur die Beitragssaetze geaendert werden, muss hierfuer die update-Methode
        'update_krankenversicherungsbeitraege' verwendet werden.
        """
        self.testfirma.get_nutzer("M100001"). \
            insert_krankenversicherungsbeitraege('testdaten_insert_krankenversicherungsbeitraege/'
                                                 'Krankenversicherungsbeitraege.xlsx', self.testschema)

        # Versuch, nochmal den nicht ermaessigten Beitragssatz einzutragen
        with self.assertRaises(Exception) as context:
            self.testfirma.get_nutzer("M100001"). \
                insert_krankenversicherungsbeitraege('testdaten_insert_krankenversicherungsbeitraege/'
                                                     'Krankenversicherungsbeitraege.xlsx',
                                                     self.testschema)

        self.assertEqual(str(context.exception), "FEHLER:  Ermaessigung = 'f' ist bereits vorhanden! Uebergebene Daten "
                                                 "werden nicht eingetragen! Wenn Sie diese Daten aktualisieren wollen, "
                                                 "nutzen Sie bitte die 'update_krankenversicherungsbeitraege'-"
                                                 "Funktion!\n"
                                                 "CONTEXT:  PL/pgSQL-Funktion insert_krankenversicherungsbeitraege("
                                                 "integer,boolean,numeric,numeric,numeric,numeric,date) Zeile 16 bei "
                                                 "RAISE\n")

        # Inhalte aus Tabellen ziehen, um zu pruefen, ob auch weiterhin nur ein Datensatz angelegt wurde
        ergebnis = self.testfirma.get_nutzer("M100001").abfrage_ausfuehren("SELECT * FROM gkv_beitraege",
                                                                           self.testschema)
        self.assertEqual(str(ergebnis), "[(1, 1, Decimal('7.300'), Decimal('7.300'), Decimal('72453.56'), "
                                        "Decimal('75683.12'))]")

        ergebnis = self.testfirma.get_nutzer("M100001").abfrage_ausfuehren("SELECT * FROM krankenversicherungen",
                                                                           self.testschema)
        self.assertEqual(str(ergebnis), "[(1, 1, False)]")

        ergebnis = self.testfirma.get_nutzer("M100001").abfrage_ausfuehren("SELECT * FROM hat_GKV_Beitraege",
                                                                           self.testschema)
        self.assertEqual(str(ergebnis), "[(1, 1, 1, datetime.date(2023, 12, 15), datetime.date(9999, 12, 31))]")

    def test_kein_doppelter_eintrag_andere_werte(self):
        """
        Test prueft, ob bei wiederholtem Aufruf der Methode 'insert_krankenversicherungsbeitraege' mit derselben Angabe,
        ob es der ermaessigte Beitrag ist, aber anderen Beitragssaetzen dieser nicht erneut eingetragen wird. Beim
        zweiten Eintrag muss eine Exception geworfen werden. Massgeblich sit hier lediglich der boolesche Wert
        "ermaessigter_beitragssatz" in Tabelle "Krankenversicherungen". Die Exception wird auch dann geworfen, wenn die
        Beitragssaetze anders sind. Sollen nur die Beitragssaetze geaendert werden, muss hierfuer die update-Methode
        'update_krankenversicherungsbeitraege' verwendet werden.
        """
        self.testfirma.get_nutzer("M100001"). \
            insert_krankenversicherungsbeitraege('testdaten_insert_krankenversicherungsbeitraege/'
                                                 'Krankenversicherungsbeitraege.xlsx', self.testschema)

        # Versuch, nochmal den nicht ermaessigten Beitragssatz (aber mit anderen Werten) einzutragen
        with self.assertRaises(Exception) as context:
            self.testfirma.get_nutzer("M100001"). \
                insert_krankenversicherungsbeitraege('testdaten_insert_krankenversicherungsbeitraege/'
                                                     'Krankenversicherungsbeitraege - selbe Ermaessigung.xlsx',
                                                     self.testschema)

        self.assertEqual(str(context.exception), "FEHLER:  Ermaessigung = 'f' ist bereits vorhanden! Uebergebene Daten "
                                                 "werden nicht eingetragen! Wenn Sie diese Daten aktualisieren wollen, "
                                                 "nutzen Sie bitte die 'update_krankenversicherungsbeitraege'-"
                                                 "Funktion!\n"
                                                 "CONTEXT:  PL/pgSQL-Funktion insert_krankenversicherungsbeitraege("
                                                 "integer,boolean,numeric,numeric,numeric,numeric,date) Zeile 16 bei "
                                                 "RAISE\n")

        # Inhalte aus Tabellen ziehen, um zu pruefen, ob auch weiterhin nur ein Datensatz angelegt wurde
        ergebnis = self.testfirma.get_nutzer("M100001").abfrage_ausfuehren("SELECT * FROM gkv_beitraege",
                                                                           self.testschema)
        self.assertEqual(str(ergebnis), "[(1, 1, Decimal('7.300'), Decimal('7.300'), Decimal('72453.56'), "
                                        "Decimal('75683.12'))]")

        ergebnis = self.testfirma.get_nutzer("M100001").abfrage_ausfuehren("SELECT * FROM krankenversicherungen",
                                                                           self.testschema)
        self.assertEqual(str(ergebnis), "[(1, 1, False)]")

        ergebnis = self.testfirma.get_nutzer("M100001").abfrage_ausfuehren("SELECT * FROM hat_GKV_Beitraege",
                                                                           self.testschema)
        self.assertEqual(str(ergebnis), "[(1, 1, 1, datetime.date(2023, 12, 15), datetime.date(9999, 12, 31))]")

    def tearDown(self):
        """
        Methode ruft Funktion 'test_tear_down' auf, welches das Datenbankschema 'temp_test_schema' mit allen Daten
        entfernt.
        """
        test_tear_down()
