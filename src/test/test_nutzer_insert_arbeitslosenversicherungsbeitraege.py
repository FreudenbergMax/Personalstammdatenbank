import unittest
from src.main.Mandant import Mandant
from src.main.test_SetUp_TearDown import test_set_up, test_tear_down


class TestNutzerInsertRentenversicherungsbeitraege(unittest.TestCase):

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
        Test prueft, ob Rentenversicherungsbeitraege eingetragen werden.
        """
        self.testfirma.get_nutzer("M100001").\
            insert_arbeitslosenversicherungsbeitraege('testdaten_insert_arbeitslosenversicherungsbeitraege/'
                                                      'Arbeitslosenversicherungsbeitraege.xlsx', self.testschema)

        # Inhalte aus Tabellen ziehen, um zu pruefen, ob der Datensatz angelegt wurde
        ergebnis = self.testfirma.get_nutzer("M100001").abfrage_ausfuehren("SELECT * FROM Arbeitslosenversicherungen",
                                                                           self.testschema)
        self.assertEqual(str(ergebnis), "[(1, 1)]")

        ergebnis = self.testfirma.get_nutzer("M100001").abfrage_ausfuehren("SELECT * FROM "
                                                                           "Arbeitslosenversicherungsbeitraege",
                                                                           self.testschema)
        self.assertEqual(str(ergebnis), "[(1, 1, Decimal('3.000'), Decimal('3.000'), Decimal('57846.12'), "
                                        "Decimal('60000.00'))]")

        ergebnis = self.testfirma.get_nutzer("M100001").abfrage_ausfuehren("SELECT * FROM hat_AV_Beitraege",
                                                                           self.testschema)
        self.assertEqual(str(ergebnis), "[(1, 1, 1, datetime.date(2023, 12, 15), datetime.date(9999, 12, 31))]")

    def test_kein_doppelter_eintrag(self):
        """
        Test prueft, ob bei wiederholtem Aufruf der Methode 'insert_arbeitslosenversicherungsbeitraege' mit denselben
        Angaben nicht mehrfach eingetragen wird. Beim zweiten Eintrag muss eine Exception geworfen werden. Massgeblich
        ist hier lediglich die Mandant_ID in Tabelle "Krankenversicherungen" (denn jeder Arbeitgeber bezahlt fuer alle
        Mitarbeiter dieselben Saetze). Die Exception wird auch dann geworfen, wenn die Beitragssaetze anders sind.
        Sollen nur die Beitragssaetze geaendert werden, muss hierfuer eine update-Methode verwendet werden (welche im
        Rahmen dieser Bachelorarbeit nicht implementiert wird).
        """
        self.testfirma.get_nutzer("M100001"). \
            insert_arbeitslosenversicherungsbeitraege('testdaten_insert_arbeitslosenversicherungsbeitraege/'
                                                      'Arbeitslosenversicherungsbeitraege.xlsx', self.testschema)

        # Versuch, dieselben Beitragssaetze einzutragen
        with self.assertRaises(Exception) as context:
            self.testfirma.get_nutzer("M100001"). \
                insert_arbeitslosenversicherungsbeitraege('testdaten_insert_arbeitslosenversicherungsbeitraege/'
                                                          'Arbeitslosenversicherungsbeitraege.xlsx', self.testschema)

        self.assertEqual(str(context.exception), "FEHLER:  Arbeitslosenversicherung ist bereits vorhanden! Uebergebene "
                                                 "Daten werden nicht eingetragen! Wenn Sie diese Daten aktualisieren "
                                                 "wollen, nutzen Sie bitte die "
                                                 "'update_arbeitslosenversicherung'-Funktion!\n"
                                                 "CONTEXT:  PL/pgSQL-Funktion insert_arbeitslosenversicherungsbeitraege"
                                                 "(integer,numeric,numeric,numeric,numeric,date) Zeile 17 bei RAISE\n")

        # Inhalte aus Tabellen ziehen, um zu pruefen, ob der Datensatz angelegt wurde
        ergebnis = self.testfirma.get_nutzer("M100001").abfrage_ausfuehren("SELECT * FROM Arbeitslosenversicherungen",
                                                                           self.testschema)
        self.assertEqual(str(ergebnis), "[(1, 1)]")

        ergebnis = self.testfirma.get_nutzer("M100001").abfrage_ausfuehren("SELECT * FROM "
                                                                           "Arbeitslosenversicherungsbeitraege",
                                                                           self.testschema)
        self.assertEqual(str(ergebnis), "[(1, 1, Decimal('3.000'), Decimal('3.000'), Decimal('57846.12'), "
                                        "Decimal('60000.00'))]")

        ergebnis = self.testfirma.get_nutzer("M100001").abfrage_ausfuehren("SELECT * FROM hat_AV_Beitraege",
                                                                           self.testschema)
        self.assertEqual(str(ergebnis), "[(1, 1, 1, datetime.date(2023, 12, 15), datetime.date(9999, 12, 31))]")

    def test_kein_doppelter_eintrag_andere_werte(self):
        """
        Test prueft, ob bei wiederholtem Aufruf der Methode 'insert_arbeitslosenversicherungsbeitraege' mit anderen
        Beitragssaetzen dennoch nicht mehrfach eingetragen wird. Beim zweiten Eintrag muss eine Exception geworfen
        werden. Massgeblich ist hier lediglich die Mandant_ID in Tabelle "Krankenversicherungen" (denn jeder Arbeitgeber
        bezahlt fuer alle Mitarbeiter dieselben Saetze). Die Exception wird auch dann geworfen, wenn die Beitragssaetze
        anders sind. Sollen nur die Beitragssaetze geaendert werden, muss hierfuer eine update-Methode verwendet werden
        (welche im Rahmen dieser Bachelorarbeit nicht implementiert wird).
        """
        self.testfirma.get_nutzer("M100001"). \
            insert_arbeitslosenversicherungsbeitraege('testdaten_insert_arbeitslosenversicherungsbeitraege/'
                                                      'Arbeitslosenversicherungsbeitraege.xlsx', self.testschema)

        with self.assertRaises(Exception) as context:
            self.testfirma.get_nutzer("M100001"). \
                insert_arbeitslosenversicherungsbeitraege('testdaten_insert_arbeitslosenversicherungsbeitraege/'
                                                          'Arbeitslosenversicherungsbeitraege - '
                                                          'andere Beitragssaetze.xlsx', self.testschema)

        self.assertEqual(str(context.exception), "FEHLER:  Arbeitslosenversicherung ist bereits vorhanden! Uebergebene "
                                                 "Daten werden nicht eingetragen! Wenn Sie diese Daten aktualisieren "
                                                 "wollen, nutzen Sie bitte die "
                                                 "'update_arbeitslosenversicherung'-Funktion!\n"
                                                 "CONTEXT:  PL/pgSQL-Funktion insert_arbeitslosenversicherungsbeitraege"
                                                 "(integer,numeric,numeric,numeric,numeric,date) Zeile 17 bei RAISE\n")

        # Inhalte aus Tabellen ziehen, um zu pruefen, ob der Datensatz angelegt wurde
        ergebnis = self.testfirma.get_nutzer("M100001").abfrage_ausfuehren("SELECT * FROM Arbeitslosenversicherungen",
                                                                           self.testschema)
        self.assertEqual(str(ergebnis), "[(1, 1)]")

        ergebnis = self.testfirma.get_nutzer("M100001").abfrage_ausfuehren("SELECT * FROM "
                                                                           "Arbeitslosenversicherungsbeitraege",
                                                                           self.testschema)
        self.assertEqual(str(ergebnis), "[(1, 1, Decimal('3.000'), Decimal('3.000'), Decimal('57846.12'), "
                                        "Decimal('60000.00'))]")

        ergebnis = self.testfirma.get_nutzer("M100001").abfrage_ausfuehren("SELECT * FROM hat_AV_Beitraege",
                                                                           self.testschema)
        self.assertEqual(str(ergebnis), "[(1, 1, 1, datetime.date(2023, 12, 15), datetime.date(9999, 12, 31))]")

    def tearDown(self):
        """
        Methode ruft Funktion 'test_tear_down' auf, welches das Datenbankschema 'temp_test_schema' mit allen Daten
        entfernt.
        """
        test_tear_down(self.conn, self.cur)
