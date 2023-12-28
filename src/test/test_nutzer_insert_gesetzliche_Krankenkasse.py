import unittest
from src.main.Mandant import Mandant
from src.main.test_SetUp_TearDown import test_set_up, test_tear_down


class TestNutzerInsertGesetzlicheKrankenkasse(unittest.TestCase):

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
        Test prueft, ob gesetzliche Krankenkasse mit ihrem Zusatzbeitrag und Umlagebeitraegen eingetragen werden.
        """
        self.testfirma.get_nutzer("M100001").\
            insert_gesetzliche_krankenkasse('testdaten_insert_gesetzliche_krankenkasse/gesetzliche Krankenkasse.xlsx',
                                            self.testschema)

        # Inhalte aus Tabellen ziehen, um zu pruefen, ob der Datensatz angelegt wurde
        ergebnis = self.testfirma.get_nutzer("M100001").abfrage_ausfuehren("SELECT * FROM gesetzliche_Krankenkassen",
                                                                           self.testschema)
        self.assertEqual(str(ergebnis), "[(1, 1, 'Kaufmaennische Krankenkasse', 'KKH')]")

        ergebnis = self.testfirma.get_nutzer("M100001").abfrage_ausfuehren("SELECT * FROM gkv_zusatzbeitraege",
                                                                           self.testschema)
        self.assertEqual(str(ergebnis), "[(1, 1, Decimal('1.500'))]")

        ergebnis = self.testfirma.get_nutzer("M100001").abfrage_ausfuehren("SELECT * FROM hat_gkv_zusatzbeitrag",
                                                                           self.testschema)
        self.assertEqual(str(ergebnis), "[(1, 1, 1, datetime.date(2023, 12, 15), datetime.date(9999, 12, 31))]")

        ergebnis = self.testfirma.get_nutzer("M100001").abfrage_ausfuehren("SELECT * FROM umlagen",
                                                                           self.testschema)
        self.assertEqual(str(ergebnis), "[(1, 1, Decimal('1.600'), Decimal('0.440'), Decimal('0.060'), "
                                        "'gesetzlich')]")
        ergebnis = self.testfirma.get_nutzer("M100001").abfrage_ausfuehren("SELECT * FROM hat_umlagen_gesetzlich",
                                                                           self.testschema)
        self.assertEqual(str(ergebnis), "[(1, 1, 1, datetime.date(2023, 12, 15), datetime.date(9999, 12, 31))]")

    def test_kein_doppelter_eintrag(self):
        """
        Test prueft, ob bei wiederholtem Aufruf der Methode 'insert_gesetzliche_krankenkasse' mit derselben Krankenkasse
        dieser nicht mehrfach eingetragen wird. Beim zweiten Eintrag muss eine Exception geworfen werden. Massgeblich
        ist hier lediglich der Wert "krankenkasse_gesetzlich" in Tabelle "gesetzliche_krankenkassen". Die Exception wird
        auch dann geworfen, wenn die restlichen Werte anders sind. Sollen nur die restlichen Werte geaendert werden,
        muss hierfuer eine update-Methode verwendet werden (welche im Rahmen dieser Arbeit nicht implementiert wird).
        """
        self.testfirma.get_nutzer("M100001"). \
            insert_gesetzliche_krankenkasse('testdaten_insert_gesetzliche_krankenkasse/gesetzliche Krankenkasse.xlsx',
                                            self.testschema)

        # Versuch, nochmal den nicht ermaessigten Beitragssatz einzutragen
        with self.assertRaises(Exception) as context:
            self.testfirma.get_nutzer("M100001"). \
                insert_gesetzliche_krankenkasse('testdaten_insert_gesetzliche_krankenkasse/'
                                                'gesetzliche Krankenkasse.xlsx', self.testschema)

        self.assertEqual(str(context.exception), "FEHLER:  Gesetzliche Krankenkasse 'Kaufmaennische Krankenkasse' ist "
                                                 "bereits vorhanden! Uebergebene Daten werden nicht eingetragen! Wenn "
                                                 "Sie diese Daten aktualisieren wollen, nutzen Sie bitte die "
                                                 "'update_gesetzliche_krankenkasse'-Funktion!\n"
                                                 "CONTEXT:  PL/pgSQL-Funktion insert_gesetzliche_krankenkasse(integer,"
                                                 "character varying,character varying,numeric,numeric,numeric,numeric,"
                                                 "character varying,date) Zeile 18 bei RAISE\n")

        # Inhalte aus Tabellen ziehen, um zu pruefen, ob auch weiterhin nur ein Datensatz angelegt wurde
        ergebnis = self.testfirma.get_nutzer("M100001").abfrage_ausfuehren("SELECT * FROM gesetzliche_Krankenkassen",
                                                                           self.testschema)
        self.assertEqual(str(ergebnis), "[(1, 1, 'Kaufmaennische Krankenkasse', 'KKH')]")

        ergebnis = self.testfirma.get_nutzer("M100001").abfrage_ausfuehren("SELECT * FROM gkv_zusatzbeitraege",
                                                                           self.testschema)
        self.assertEqual(str(ergebnis), "[(1, 1, Decimal('1.500'))]")

        ergebnis = self.testfirma.get_nutzer("M100001").abfrage_ausfuehren("SELECT * FROM hat_gkv_zusatzbeitrag",
                                                                           self.testschema)
        self.assertEqual(str(ergebnis), "[(1, 1, 1, datetime.date(2023, 12, 15), datetime.date(9999, 12, 31))]")

        ergebnis = self.testfirma.get_nutzer("M100001").abfrage_ausfuehren("SELECT * FROM umlagen",
                                                                           self.testschema)
        self.assertEqual(str(ergebnis), "[(1, 1, Decimal('1.600'), Decimal('0.440'), Decimal('0.060'), "
                                        "'gesetzlich')]")
        ergebnis = self.testfirma.get_nutzer("M100001").abfrage_ausfuehren("SELECT * FROM hat_umlagen_gesetzlich",
                                                                           self.testschema)
        self.assertEqual(str(ergebnis), "[(1, 1, 1, datetime.date(2023, 12, 15), datetime.date(9999, 12, 31))]")

    def test_kein_doppelter_eintrag_case_insensitive(self):
        """
        Test prueft, ob bei wiederholtem Aufruf der Methode 'insert_erfahrungsstufe' mit derselben Erfahrungsstufe aber
        mit Kleinschreibung dieser dennoch nicht mehrfach eingetragen wird. Beim zweiten Eintrag muss eine Exception
        geworfen werden. Ausloeser ist der unique-constraint, welcher in der Stored Procedure 'insert_erfahrungsstufe'
        implementiert ist, in Kombination mit dem unique-Index 'erfahrungsstufe_idx'.
        """
        self.testfirma.get_nutzer("M100001"). \
            insert_erfahrungsstufe('testdaten_insert_erfahrungsstufe/Erfahrungsstufe.xlsx', self.testschema)

        # Versuch, denselben Wert noch einmal einzutragen (diesmal aber in Kleinschreibung)
        with self.assertRaises(Exception) as context:
            self.testfirma.get_nutzer("M100001"). \
                insert_erfahrungsstufe('testdaten_insert_erfahrungsstufe/Erfahrungsstufe - klein geschrieben.xlsx',
                                       self.testschema)

        self.assertEqual(str(context.exception), "FEHLER:  Erfahrungsstufe 'junior' bereits vorhanden!\n"
                                                 "CONTEXT:  PL/pgSQL-Funktion insert_erfahrungsstufe(integer,character "
                                                 "varying) Zeile 16 bei RAISE\n")

        # Inhalt aus Tabelle ziehen, um zu pruefen, ob der Datensatz auch nur einmal angelegt wurde
        ergebnis = self.testfirma.get_nutzer("M100001").abfrage_ausfuehren("SELECT * FROM erfahrungsstufen",
                                                                           self.testschema)

        self.assertEqual(str(ergebnis), "[(1, 1, 'Junior')]")

    def tearDown(self):
        """
        Methode ruft Funktion 'test_tear_down' auf, welches das Datenbankschema 'temp_test_schema' mit allen Daten
        entfernt.
        """
        test_tear_down(self.conn, self.cur)
