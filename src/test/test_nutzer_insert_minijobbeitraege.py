import unittest
from src.main.Mandant import Mandant
from src.main.test_SetUp_TearDown import test_set_up, test_tear_down


class TestNutzerInsertMinijobbeitraege(unittest.TestCase):

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
        Test prueft, ob Minijobbeitraege in Datenbank eingetragen werden.
        """
        self.testfirma.get_nutzer("M100001").\
            insert_minijobbeitraege('testdaten_insert_minijobbeitraege/Minijobbeitraege.xlsx', self.testschema)

        # Inhalte aus Tabellen ziehen, um zu pruefen, ob der Datensatz angelegt wurde
        ergebnis = self.testfirma.get_nutzer("M100001").abfrage_ausfuehren("SELECT * FROM Minijobs", self.testschema)
        self.assertEqual(str(ergebnis), "[(1, 1, False)]")

        ergebnis = self.testfirma.get_nutzer("M100001").abfrage_ausfuehren("SELECT * FROM Pauschalabgaben",
                                                                           self.testschema)
        self.assertEqual(str(ergebnis), "[(1, 1, Decimal('9.800'), Decimal('3.000'), Decimal('3.000'), "
                                        "Decimal('1.100'), Decimal('0.660'), Decimal('0.060'), Decimal('2.000'))]")

        ergebnis = self.testfirma.get_nutzer("M100001").abfrage_ausfuehren("SELECT * FROM hat_Pauschalabgaben",
                                                                           self.testschema)
        self.assertEqual(str(ergebnis), "[(1, 1, 1, datetime.date(2023, 12, 15), datetime.date(9999, 12, 31))]")

    def test_kein_doppelter_eintrag(self):
        """
        Test prueft, ob bei wiederholtem Aufruf der Methode 'insert_minijobbeitraege' mit denselben Angaben nicht erneut
        eingetragen wird. Beim zweiten Eintrag muss eine Exception geworfen werden. Massgeblich ist hier lediglich der
        boolesche Wert "kurzfristig_beschaeftigt" in Tabelle "Minijobs". Die Exception wird auch dann
        geworfen, wenn die Beitragssaetze anders sind. Sollen nur die Beitragssaetze geaendert werden, muss hierfuer
        eine update-Methode verwendet werden (welche im Rahmen dieser Bachelorarbeit nicht implementiert wird).
        """
        self.testfirma.get_nutzer("M100001"). \
            insert_minijobbeitraege('testdaten_insert_minijobbeitraege/Minijobbeitraege.xlsx', self.testschema)

        with self.assertRaises(Exception) as context:
            self.testfirma.get_nutzer("M100001"). \
                insert_minijobbeitraege('testdaten_insert_minijobbeitraege/Minijobbeitraege.xlsx', self.testschema)

        self.assertEqual(str(context.exception), "FEHLER:  Kurzfristige Beschaeftigung = 'f' ist bereits vorhanden! "
                                                 "Uebergebene Daten werden nicht eingetragen! Wenn Sie diese Daten "
                                                 "aktualisieren wollen, nutzen Sie bitte die "
                                                 "'update_Minijob'-Funktion!\n"
                                                 "CONTEXT:  PL/pgSQL-Funktion insert_minijobbeitraege(integer,boolean,"
                                                 "numeric,numeric,numeric,numeric,numeric,numeric,numeric,date) Zeile "
                                                 "15 bei RAISE\n")

        # Inhalte aus Tabellen ziehen, um zu pruefen, ob der Datensatz angelegt wurde
        ergebnis = self.testfirma.get_nutzer("M100001").abfrage_ausfuehren("SELECT * FROM Minijobs", self.testschema)
        self.assertEqual(str(ergebnis), "[(1, 1, False)]")

        ergebnis = self.testfirma.get_nutzer("M100001").abfrage_ausfuehren("SELECT * FROM Pauschalabgaben",
                                                                           self.testschema)
        self.assertEqual(str(ergebnis), "[(1, 1, Decimal('9.800'), Decimal('3.000'), Decimal('3.000'), "
                                        "Decimal('1.100'), Decimal('0.660'), Decimal('0.060'), Decimal('2.000'))]")

        ergebnis = self.testfirma.get_nutzer("M100001").abfrage_ausfuehren("SELECT * FROM hat_Pauschalabgaben",
                                                                           self.testschema)
        self.assertEqual(str(ergebnis), "[(1, 1, 1, datetime.date(2023, 12, 15), datetime.date(9999, 12, 31))]")

    def test_kein_doppelter_eintrag_andere_werte(self):
        """
        Test prueft, ob bei wiederholtem Aufruf der Methode 'insert_minijobbeitraege' mit demselben
        booleschen Wahrheitswert (= false), aber mit anderem Beitragssaetzen, dennoch nicht eingetragen wird. Beim
        zweiten Eintrag muss eine Exception geworfen werden. Massgeblich ist hier lediglich der boolesche Wert
        "kurzfristig_beschaeftigt" in Tabelle "Minijobs". Die Exception wird auch dann geworfen, wenn die Beitragssaetze
        anders sind. Sollen nur die Beitragssaetze geaendert werden, muss hierfuer eine update-Methode verwendet werden
        (welche im Rahmen dieser Bachelorarbeit nicht implementiert wird).
        """
        self.testfirma.get_nutzer("M100001"). \
            insert_minijobbeitraege('testdaten_insert_minijobbeitraege/Minijobbeitraege.xlsx', self.testschema)

        with self.assertRaises(Exception) as context:
            self.testfirma.get_nutzer("M100001"). \
                insert_minijobbeitraege('testdaten_insert_minijobbeitraege/Minijobbeitraege.xlsx', self.testschema)

        self.assertEqual(str(context.exception), "FEHLER:  Kurzfristige Beschaeftigung = 'f' ist bereits vorhanden! "
                                                 "Uebergebene Daten werden nicht eingetragen! Wenn Sie diese Daten "
                                                 "aktualisieren wollen, nutzen Sie bitte die "
                                                 "'update_Minijob'-Funktion!\n"
                                                 "CONTEXT:  PL/pgSQL-Funktion insert_minijobbeitraege(integer,boolean,"
                                                 "numeric,numeric,numeric,numeric,numeric,numeric,numeric,date) Zeile "
                                                 "15 bei RAISE\n")

        # Inhalte aus Tabellen ziehen, um zu pruefen, ob der Datensatz angelegt wurde
        ergebnis = self.testfirma.get_nutzer("M100001").abfrage_ausfuehren("SELECT * FROM Minijobs", self.testschema)
        self.assertEqual(str(ergebnis), "[(1, 1, False)]")

        ergebnis = self.testfirma.get_nutzer("M100001").abfrage_ausfuehren("SELECT * FROM Pauschalabgaben",
                                                                           self.testschema)
        self.assertEqual(str(ergebnis), "[(1, 1, Decimal('9.800'), Decimal('3.000'), Decimal('3.000'), "
                                        "Decimal('1.100'), Decimal('0.660'), Decimal('0.060'), Decimal('2.000'))]")

        ergebnis = self.testfirma.get_nutzer("M100001").abfrage_ausfuehren("SELECT * FROM hat_Pauschalabgaben",
                                                                           self.testschema)
        self.assertEqual(str(ergebnis), "[(1, 1, 1, datetime.date(2023, 12, 15), datetime.date(9999, 12, 31))]")

    def tearDown(self):
        """
        Methode ruft Funktion 'test_tear_down' auf, welches das Datenbankschema 'temp_test_schema' mit allen Daten
        entfernt.
        """
        test_tear_down()
