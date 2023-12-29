import unittest
from src.main.Mandant import Mandant
from src.main.test_SetUp_TearDown import test_set_up, test_tear_down


class TestNutzerInsertArbeitslosenversicherungsbeitraege(unittest.TestCase):

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
        Test prueft, ob Rentenversicherungsbeitraege eingetragen werden.
        """
        self.testfirma.get_nutzer("M100001").\
            insert_rentenversicherungsbeitraege('testdaten_insert_rentenversicherungsbeitraege/'
                                                'Rentenversicherungsbeitraege.xlsx', self.testschema)

        # Inhalte aus Tabellen ziehen, um zu pruefen, ob der Datensatz angelegt wurde
        ergebnis = self.testfirma.get_nutzer("M100001").abfrage_ausfuehren("SELECT * FROM rentenversicherungen",
                                                                           self.testschema)
        self.assertEqual(str(ergebnis), "[(1, 1)]")

        ergebnis = self.testfirma.get_nutzer("M100001").abfrage_ausfuehren("SELECT * FROM "
                                                                           "Rentenversicherungsbeitraege",
                                                                           self.testschema)
        self.assertEqual(str(ergebnis), "[(1, 1, Decimal('9.800'), Decimal('9.800'), Decimal('75000.00'), "
                                        "Decimal('80125.46'))]")

        ergebnis = self.testfirma.get_nutzer("M100001").abfrage_ausfuehren("SELECT * FROM hat_RV_Beitraege",
                                                                           self.testschema)
        self.assertEqual(str(ergebnis), "[(1, 1, 1, datetime.date(2023, 12, 15), datetime.date(9999, 12, 31))]")

    def test_kein_doppelter_eintrag(self):
        """
        Test prueft, ob bei wiederholtem Aufruf der Methode 'insert_rentenversicherungsbeitraege' mit denselben
        Angaben nicht mehrfach eingetragen wird. Beim zweiten Eintrag muss eine Exception geworfen werden. Massgeblich
        ist hier lediglich die Mandant_ID in Tabelle "Rentenversicherungen" (denn jeder Arbeitgeber bezahlt fuer alle
        Mitarbeiter dieselben Saetze). Die Exception wird auch dann geworfen, wenn die Beitragssaetze anders sind.
        Sollen nur die Beitragssaetze geaendert werden, muss hierfuer eine update-Methode verwendet werden (welche im
        Rahmen dieser Bachelorarbeit nicht implementiert wird).
        """
        self.testfirma.get_nutzer("M100001"). \
            insert_rentenversicherungsbeitraege('testdaten_insert_rentenversicherungsbeitraege/'
                                                'Rentenversicherungsbeitraege.xlsx', self.testschema)

        # Versuch, dieselben Beitragssaetze einzutragen
        with self.assertRaises(Exception) as context:
            self.testfirma.get_nutzer("M100001"). \
                insert_rentenversicherungsbeitraege('testdaten_insert_rentenversicherungsbeitraege/'
                                                    'Rentenversicherungsbeitraege.xlsx', self.testschema)

        self.assertEqual(str(context.exception), "FEHLER:  Rentenversicherung ist bereits vorhanden! Uebergebene Daten "
                                                 "werden nicht eingetragen! Wenn Sie diese Daten aktualisieren wollen, "
                                                 "nutzen Sie bitte die 'update_rentenversicherung'-Funktion!\n"
                                                 "CONTEXT:  PL/pgSQL-Funktion insert_rentenversicherungsbeitraege"
                                                 "(integer,numeric,numeric,numeric,numeric,date) Zeile 19 bei RAISE\n")

        # Inhalte aus Tabellen ziehen, um zu pruefen, ob der Datensatz angelegt wurde
        ergebnis = self.testfirma.get_nutzer("M100001").abfrage_ausfuehren("SELECT * FROM rentenversicherungen",
                                                                           self.testschema)
        self.assertEqual(str(ergebnis), "[(1, 1)]")

        ergebnis = self.testfirma.get_nutzer("M100001").abfrage_ausfuehren("SELECT * FROM "
                                                                           "Rentenversicherungsbeitraege",
                                                                           self.testschema)
        self.assertEqual(str(ergebnis), "[(1, 1, Decimal('9.800'), Decimal('9.800'), Decimal('75000.00'), "
                                        "Decimal('80125.46'))]")

        ergebnis = self.testfirma.get_nutzer("M100001").abfrage_ausfuehren("SELECT * FROM hat_RV_Beitraege",
                                                                           self.testschema)
        self.assertEqual(str(ergebnis), "[(1, 1, 1, datetime.date(2023, 12, 15), datetime.date(9999, 12, 31))]")

    def test_kein_doppelter_eintrag_andere_werte(self):
        """
        Test prueft, ob bei wiederholtem Aufruf der Methode 'insert_rentenversicherungsbeitraege' mit anderen
        Beitragssaetzen dennoch nicht mehrfach eingetragen wird. Beim zweiten Eintrag muss eine Exception geworfen
        werden. Massgeblich ist hier lediglich die Mandant_ID in Tabelle "Rentenversicherungen" (denn jeder Arbeitgeber
        bezahlt fuer alle Mitarbeiter dieselben Saetze). Die Exception wird auch dann geworfen, wenn die Beitragssaetze
        anders sind. Sollen nur die Beitragssaetze geaendert werden, muss hierfuer eine update-Methode verwendet werden
        (welche im Rahmen dieser Bachelorarbeit nicht implementiert wird).
        """
        self.testfirma.get_nutzer("M100001"). \
            insert_rentenversicherungsbeitraege('testdaten_insert_rentenversicherungsbeitraege/'
                                                'Rentenversicherungsbeitraege.xlsx', self.testschema)

        # Versuch, nochmal den nicht ermaessigten Beitragssatz einzutragen
        with self.assertRaises(Exception) as context:
            self.testfirma.get_nutzer("M100001"). \
                insert_rentenversicherungsbeitraege('testdaten_insert_rentenversicherungsbeitraege/'
                                                    'Rentenversicherungsbeitraege - andere Beitragssaetze.xlsx',
                                                    self.testschema)

        self.assertEqual(str(context.exception), "FEHLER:  Rentenversicherung ist bereits vorhanden! Uebergebene Daten "
                                                 "werden nicht eingetragen! Wenn Sie diese Daten aktualisieren wollen, "
                                                 "nutzen Sie bitte die 'update_rentenversicherung'-Funktion!\n"
                                                 "CONTEXT:  PL/pgSQL-Funktion insert_rentenversicherungsbeitraege"
                                                 "(integer,numeric,numeric,numeric,numeric,date) Zeile 19 bei RAISE\n")

        # Versuch, andere Beitragssaetze einzutragen
        ergebnis = self.testfirma.get_nutzer("M100001").abfrage_ausfuehren("SELECT * FROM rentenversicherungen",
                                                                           self.testschema)
        self.assertEqual(str(ergebnis), "[(1, 1)]")

        ergebnis = self.testfirma.get_nutzer("M100001").abfrage_ausfuehren("SELECT * FROM "
                                                                           "Rentenversicherungsbeitraege",
                                                                           self.testschema)
        self.assertEqual(str(ergebnis), "[(1, 1, Decimal('9.800'), Decimal('9.800'), Decimal('75000.00'), "
                                        "Decimal('80125.46'))]")

        ergebnis = self.testfirma.get_nutzer("M100001").abfrage_ausfuehren("SELECT * FROM hat_RV_Beitraege",
                                                                           self.testschema)
        self.assertEqual(str(ergebnis), "[(1, 1, 1, datetime.date(2023, 12, 15), datetime.date(9999, 12, 31))]")

    def tearDown(self):
        """
        Methode ruft Funktion 'test_tear_down' auf, welches das Datenbankschema 'temp_test_schema' mit allen Daten
        entfernt.
        """
        test_tear_down()
