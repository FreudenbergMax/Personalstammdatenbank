import unittest
from src.main.Mandant import Mandant
from src.main.test_SetUp_TearDown import test_set_up, test_tear_down


class TestNutzerInsertAnzahlKinder(unittest.TestCase):

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
        Test prueft, ob die Kindernazahl mit dessen Arbeitnehmerbeitrag und Beitragsbemessungsgrenzen eingetragen
        werden.
        """
        self.testfirma.get_nutzer("M100001").\
            insert_anzahl_kinder_an_pv_beitrag('testdaten_insert_anzahl_kinder/'
                                                 'Anzahl Kinder Arbeitnehmer PV-Beitrag.xlsx', self.testschema)

        # Inhalte aus Tabellen ziehen, um zu pruefen, ob der Datensatz angelegt wurde
        ergebnis = self.testfirma.get_nutzer("M100001").abfrage_ausfuehren("SELECT * FROM "
                                                                           "an_pflegeversicherungsbeitraege_gesetzlich",
                                                                           self.testschema)
        self.assertEqual(str(ergebnis), "[(1, 1, Decimal('1.700'), Decimal('75000.00'), Decimal('80125.46'))]")

        ergebnis = self.testfirma.get_nutzer("M100001").abfrage_ausfuehren("SELECT * FROM anzahl_kinder_unter_25",
                                                                           self.testschema)
        self.assertEqual(str(ergebnis), "[(1, 1, 1)]")

        ergebnis = self.testfirma.get_nutzer("M100001").abfrage_ausfuehren("SELECT * FROM "
                                                                           "hat_gesetzlichen_an_pv_beitragssatz",
                                                                           self.testschema)
        self.assertEqual(str(ergebnis), "[(1, 1, 1, datetime.date(2023, 12, 15), datetime.date(9999, 12, 31))]")

    def test_kein_doppelter_eintrag(self):
        """
        Test prueft, ob bei wiederholtem Aufruf der Methode 'insert_anzahl_kinder_an_pv_beitrag' mit derselben Kinder-
        anzahl nicht eingetragen wird. Beim zweiten Eintrag muss eine Exception geworfen werden. Massgeblich ist hier
        die Kinderanzahl. Sollen nur die Beitragsbemessungsgrenzen oder der AN-Beitragssatz geaendert werden, muss
        hierfuer die update-Methode verwendet werden (welche im Zuge der Arbeit nicht implementiert wird).
        """
        self.testfirma.get_nutzer("M100001"). \
            insert_anzahl_kinder_an_pv_beitrag('testdaten_insert_anzahl_kinder/'
                                               'Anzahl Kinder Arbeitnehmer PV-Beitrag.xlsx', self.testschema)

        # Versuch, nochmal den nicht ermaessigten Beitragssatz einzutragen
        with self.assertRaises(Exception) as context:
            self.testfirma.get_nutzer("M100001"). \
                insert_anzahl_kinder_an_pv_beitrag('testdaten_insert_anzahl_kinder/'
                                                   'Anzahl Kinder Arbeitnehmer PV-Beitrag.xlsx', self.testschema)

        self.assertEqual(str(context.exception), "FEHLER:  Kinderanzahl '1' ist bereits vorhanden! Uebergebene Daten "
                                                 "werden nicht eingetragen! Wenn Sie diese Daten aktualisieren wollen, "
                                                 "nutzen Sie bitte die 'update_anzahl_kinder'-Funktion!\n"
                                                 "CONTEXT:  PL/pgSQL-Funktion insert_anzahl_kinder_an_pv_beitrag("
                                                 "integer,integer,numeric,numeric,numeric,date) Zeile 16 bei RAISE\n")

        # Inhalte aus Tabellen ziehen, um zu pruefen, ob der Datensatz angelegt wurde
        ergebnis = self.testfirma.get_nutzer("M100001").abfrage_ausfuehren("SELECT * FROM "
                                                                           "an_pflegeversicherungsbeitraege_gesetzlich",
                                                                           self.testschema)
        self.assertEqual(str(ergebnis), "[(1, 1, Decimal('1.700'), Decimal('75000.00'), Decimal('80125.46'))]")

        ergebnis = self.testfirma.get_nutzer("M100001").abfrage_ausfuehren("SELECT * FROM anzahl_kinder_unter_25",
                                                                           self.testschema)
        self.assertEqual(str(ergebnis), "[(1, 1, 1)]")

        ergebnis = self.testfirma.get_nutzer("M100001").abfrage_ausfuehren("SELECT * FROM "
                                                                           "hat_gesetzlichen_an_pv_beitragssatz",
                                                                           self.testschema)
        self.assertEqual(str(ergebnis), "[(1, 1, 1, datetime.date(2023, 12, 15), datetime.date(9999, 12, 31))]")

    def test_kein_doppelter_eintrag_selbe_kinderanzahl_andere_werte(self):
        """
        Test prueft, ob bei wiederholtem Aufruf der Methode 'insert_anzahl_kinder_an_pv_beitrag' mit derselben Kinder-
        anzahl, aber mit anderen Werten, dennoch nicht eingetragen wird. Beim zweiten Eintrag muss eine Exception
        geworfen werden. Massgeblich ist hier die Kinderanzahl. Die Exception wird auch dann geworfen, wenn die
        Beitragssaetze anders sind. Sollen nur die Beitragsbemessungsgrenzen oder der AN-Beitragssatz geaendert werden,
        muss hierfuer die update-Methode verwendet werden (welche im Zuge der Arbeit nicht implementiert wird).
        """
        self.testfirma.get_nutzer("M100001"). \
            insert_anzahl_kinder_an_pv_beitrag('testdaten_insert_anzahl_kinder/'
                                               'Anzahl Kinder Arbeitnehmer PV-Beitrag.xlsx', self.testschema)

        # Versuch, einen anderen ermaessigten Beitragssatz einzutragen
        with self.assertRaises(Exception) as context:
            self.testfirma.get_nutzer("M100001"). \
                insert_anzahl_kinder_an_pv_beitrag('testdaten_insert_anzahl_kinder/'
                                                   'Anzahl Kinder Arbeitnehmer PV-Beitrag - selbe Kinderanzahl, '
                                                   'andere Werte.xlsx', self.testschema)

        self.assertEqual(str(context.exception), "FEHLER:  Kinderanzahl '1' ist bereits vorhanden! Uebergebene Daten "
                                                 "werden nicht eingetragen! Wenn Sie diese Daten aktualisieren wollen, "
                                                 "nutzen Sie bitte die 'update_anzahl_kinder'-Funktion!\n"
                                                 "CONTEXT:  PL/pgSQL-Funktion insert_anzahl_kinder_an_pv_beitrag("
                                                 "integer,integer,numeric,numeric,numeric,date) Zeile 16 bei RAISE\n")

        # Inhalte aus Tabellen ziehen, um zu pruefen, ob der Datensatz angelegt wurde
        ergebnis = self.testfirma.get_nutzer("M100001").abfrage_ausfuehren("SELECT * FROM "
                                                                           "an_pflegeversicherungsbeitraege_gesetzlich",
                                                                           self.testschema)
        self.assertEqual(str(ergebnis), "[(1, 1, Decimal('1.700'), Decimal('75000.00'), Decimal('80125.46'))]")

        ergebnis = self.testfirma.get_nutzer("M100001").abfrage_ausfuehren("SELECT * FROM anzahl_kinder_unter_25",
                                                                           self.testschema)
        self.assertEqual(str(ergebnis), "[(1, 1, 1)]")

        ergebnis = self.testfirma.get_nutzer("M100001").abfrage_ausfuehren("SELECT * FROM "
                                                                           "hat_gesetzlichen_an_pv_beitragssatz",
                                                                           self.testschema)
        self.assertEqual(str(ergebnis), "[(1, 1, 1, datetime.date(2023, 12, 15), datetime.date(9999, 12, 31))]")

    def tearDown(self):
        """
        Methode ruft Funktion 'test_tear_down' auf, welches das Datenbankschema 'temp_test_schema' mit allen Daten
        entfernt.
        """
        test_tear_down()
