import unittest
from src.main.Mandant import Mandant
from src.main.test_SetUp_TearDown import test_set_up, test_tear_down


class TestNutzerInsertGemeldeteKrankenkasse(unittest.TestCase):

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
        Test prueft, ob gemeldete Krankenkasse mit ihrem Umlagebeitraegen eingetragen werden.
        """
        self.testfirma.get_nutzer("M100001").\
            insert_gemeldete_krankenkasse('testdaten_insert_gemeldete_krankenkasse/gemeldete Krankenkasse.xlsx',
                                          self.testschema)

        # Inhalte aus Tabellen ziehen, um zu pruefen, ob der Datensatz angelegt wurde
        ergebnis = self.testfirma.get_nutzer("M100001").abfrage_ausfuehren("SELECT * FROM gemeldete_krankenkassen",
                                                                           self.testschema)
        self.assertEqual(str(ergebnis), "[(1, 1, 'Techniker Krankenkasse', 'TK')]")

        ergebnis = self.testfirma.get_nutzer("M100001").abfrage_ausfuehren("SELECT * FROM umlagen",
                                                                           self.testschema)
        self.assertEqual(str(ergebnis), "[(1, 1, Decimal('1.600'), Decimal('0.440'), Decimal('0.060'), 'anders')]")

        ergebnis = self.testfirma.get_nutzer("M100001").abfrage_ausfuehren("SELECT * FROM hat_umlagen_anderweitig",
                                                                           self.testschema)
        self.assertEqual(str(ergebnis), "[(1, 1, 1, datetime.date(2023, 12, 15), datetime.date(9999, 12, 31))]")

    def test_kein_doppelter_eintrag(self):
        """
        Test prueft, ob bei wiederholtem Aufruf der Methode 'insert_gemeldete_krankenkasse' mit derselben Krankenkasse
        dieser nicht mehrfach eingetragen wird. Beim zweiten Eintrag muss eine Exception geworfen werden. Massgeblich
        ist hier lediglich der Wert "gemeldete_Krankenkasse" in Tabelle "gemeldete_Kkrankenkassen". Die Exception wird
        auch dann geworfen, wenn die restlichen Werte anders sind. Sollen nur die restlichen Werte geaendert werden,
        muss hierfuer eine update-Methode verwendet werden (welche im Rahmen dieser Arbeit nicht implementiert wird).
        """
        self.testfirma.get_nutzer("M100001"). \
            insert_gemeldete_krankenkasse('testdaten_insert_gemeldete_krankenkasse/gemeldete Krankenkasse.xlsx',
                                          self.testschema)

        # Versuch, dieselbe Krankenkasse einzutragen
        with self.assertRaises(Exception) as context:
            self.testfirma.get_nutzer("M100001"). \
                insert_gemeldete_krankenkasse('testdaten_insert_gemeldete_krankenkasse/gemeldete Krankenkasse.xlsx',
                                              self.testschema)

        self.assertEqual(str(context.exception), "FEHLER:  Gemeldete Krankenkasse 'Techniker Krankenkasse' ist bereits "
                                                 "vorhanden! Uebergebene Daten werden nicht eingetragen! Wenn Sie diese"
                                                 " Daten aktualisieren wollen, nutzen Sie bitte die "
                                                 "'update_gemeldete_Krankenkasse'-Funktion!\n"
                                                 "CONTEXT:  PL/pgSQL-Funktion insert_gemeldete_krankenkasse(integer,"
                                                 "character varying,character varying,numeric,numeric,numeric,character"
                                                 " varying,date) Zeile 17 bei RAISE\n")

        # Inhalte aus Tabellen ziehen, um zu pruefen, ob auch weiterhin nur ein Datensatz angelegt wurde
        ergebnis = self.testfirma.get_nutzer("M100001").abfrage_ausfuehren("SELECT * FROM gemeldete_krankenkassen",
                                                                           self.testschema)
        self.assertEqual(str(ergebnis), "[(1, 1, 'Techniker Krankenkasse', 'TK')]")

        ergebnis = self.testfirma.get_nutzer("M100001").abfrage_ausfuehren("SELECT * FROM umlagen",
                                                                           self.testschema)
        self.assertEqual(str(ergebnis), "[(1, 1, Decimal('1.600'), Decimal('0.440'), Decimal('0.060'), 'anders')]")

        ergebnis = self.testfirma.get_nutzer("M100001").abfrage_ausfuehren("SELECT * FROM hat_umlagen_anderweitig",
                                                                           self.testschema)
        self.assertEqual(str(ergebnis), "[(1, 1, 1, datetime.date(2023, 12, 15), datetime.date(9999, 12, 31))]")

    def test_kein_doppelter_eintrag_krankenkasse_case_insensitive(self):
        """
        Test prueft, ob bei wiederholtem Aufruf der Methode 'insert_gemeldete_krankenkasse' mit derselben Krankenkasse
        klein geschrieben dieser nicht mehrfach eingetragen wird. Beim zweiten Eintrag muss eine Exception geworfen
        werden. Massgeblich ist hier lediglich der Wert "gemeldete_Krankenkasse" in Tabelle "gemeldete_Krankenkassen".
        Die Exception wird auch dann geworfen, wenn die restlichen Werte anders sind. Sollen nur die restlichen Werte
        geaendert werden, muss hierfuer eine update-Methode verwendet werden (welche im Rahmen dieser Arbeit nicht
        implementiert wird).
        """
        self.testfirma.get_nutzer("M100001"). \
            insert_gemeldete_krankenkasse('testdaten_insert_gemeldete_krankenkasse/gemeldete Krankenkasse.xlsx',
                                          self.testschema)

        # Versuch, dieselbe Krankenkasse (klein geschrieben) einzutragen
        with self.assertRaises(Exception) as context:
            self.testfirma.get_nutzer("M100001"). \
                insert_gemeldete_krankenkasse('testdaten_insert_gemeldete_krankenkasse/gemeldete Krankenkasse - '
                                              'Krankenkasse klein geschrieben.xlsx', self.testschema)

        self.assertEqual(str(context.exception), "FEHLER:  Gemeldete Krankenkasse 'techniker krankenkasse' oder dessen "
                                                 "Kuerzel 'TK' bereits vorhanden!\n"
                                                 "CONTEXT:  PL/pgSQL-Funktion insert_gemeldete_krankenkasse(integer,"
                                                 "character varying,character varying,numeric,numeric,numeric,character"
                                                 " varying,date) Zeile 54 bei RAISE\n")

        # Inhalte aus Tabellen ziehen, um zu pruefen, ob auch weiterhin nur ein Datensatz angelegt wurde
        ergebnis = self.testfirma.get_nutzer("M100001").abfrage_ausfuehren("SELECT * FROM gemeldete_krankenkassen",
                                                                           self.testschema)
        self.assertEqual(str(ergebnis), "[(1, 1, 'Techniker Krankenkasse', 'TK')]")

        ergebnis = self.testfirma.get_nutzer("M100001").abfrage_ausfuehren("SELECT * FROM umlagen",
                                                                           self.testschema)
        self.assertEqual(str(ergebnis), "[(1, 1, Decimal('1.600'), Decimal('0.440'), Decimal('0.060'), 'anders')]")

        ergebnis = self.testfirma.get_nutzer("M100001").abfrage_ausfuehren("SELECT * FROM hat_umlagen_anderweitig",
                                                                           self.testschema)
        self.assertEqual(str(ergebnis), "[(1, 1, 1, datetime.date(2023, 12, 15), datetime.date(9999, 12, 31))]")

    def test_kein_doppelter_eintrag_andere_krankenkasse_gleiche_abkuerzung(self):
        """
        Test prueft, ob bei wiederholtem Aufruf der Methode 'insert_gemeldete_krankenkasse' mit anderer Krankenkasse
        (statt 'Techniker Krankenkasse' wird 'Technische Krankenkasse' eingegeben) aber gleichem Kuerzel nicht mehrfach
        eingetragen wird. Beim zweiten Eintrag muss eine Exception geworfen werden. Die Exception wird auch dann
        geworfen, wenn die restlichen Werte anders sind. Sollen nur die restlichen Werte geaendert werden, muss hierfuer
        eine update-Methode verwendet werden (welche im Rahmen dieser Arbeit nicht implementiert wird).
        """
        self.testfirma.get_nutzer("M100001"). \
            insert_gemeldete_krankenkasse('testdaten_insert_gemeldete_krankenkasse/gemeldete Krankenkasse.xlsx',
                                          self.testschema)

        # Versuch, Krankenkasse (falsch geschrieben) einzutragen
        with self.assertRaises(Exception) as context:
            self.testfirma.get_nutzer("M100001"). \
                insert_gemeldete_krankenkasse('testdaten_insert_gemeldete_krankenkasse/gemeldete Krankenkasse - '
                                              'andere Krankenkasse, gleiche Abkuerzung.xlsx',
                                              self.testschema)

        self.assertEqual(str(context.exception), "FEHLER:  Gemeldete Krankenkasse 'Technische Krankenkasse' oder dessen"
                                                 " Kuerzel 'TK' bereits vorhanden!\n"
                                                 "CONTEXT:  PL/pgSQL-Funktion insert_gemeldete_krankenkasse(integer,"
                                                 "character varying,character varying,numeric,numeric,numeric,character"
                                                 " varying,date) Zeile 54 bei RAISE\n")

        # Inhalte aus Tabellen ziehen, um zu pruefen, ob auch weiterhin nur ein Datensatz angelegt wurde
        ergebnis = self.testfirma.get_nutzer("M100001").abfrage_ausfuehren("SELECT * FROM gemeldete_krankenkassen",
                                                                           self.testschema)
        self.assertEqual(str(ergebnis), "[(1, 1, 'Techniker Krankenkasse', 'TK')]")

        ergebnis = self.testfirma.get_nutzer("M100001").abfrage_ausfuehren("SELECT * FROM umlagen",
                                                                           self.testschema)
        self.assertEqual(str(ergebnis), "[(1, 1, Decimal('1.600'), Decimal('0.440'), Decimal('0.060'), 'anders')]")

        ergebnis = self.testfirma.get_nutzer("M100001").abfrage_ausfuehren("SELECT * FROM hat_umlagen_anderweitig",
                                                                           self.testschema)
        self.assertEqual(str(ergebnis), "[(1, 1, 1, datetime.date(2023, 12, 15), datetime.date(9999, 12, 31))]")

    def test_kein_doppelter_eintrag_gleiche_krankenkasse_andere_abkuerzung(self):
        """
        Test prueft, ob bei wiederholtem Aufruf der Methode 'insert_gemeldete_krankenkasse' mit gleicher Krankenkasse
        aber anderem Kuerzel (statt richtigerweise 'TK' wurde 'T K' angegeben) nicht mehrfach eingetragen wird.
        Beim zweiten Eintrag muss eine Exception geworfen werden. Die Exception wird auch dann geworfen, wenn die
        restlichen Werte anders sind. Sollen nur die restlichen Werte geaendert werden, muss hierfuer eine
        update-Methode verwendet werden (welche im Rahmen dieser Arbeit nicht implementiert wird).
        """
        self.testfirma.get_nutzer("M100001"). \
            insert_gemeldete_krankenkasse('testdaten_insert_gemeldete_krankenkasse/gemeldete Krankenkasse.xlsx',
                                          self.testschema)

        # Versuch, die gleiche Krankenkasse mit anderer Abkuerzung einzutragen
        with self.assertRaises(Exception) as context:
            self.testfirma.get_nutzer("M100001"). \
                insert_gemeldete_krankenkasse('testdaten_insert_gemeldete_krankenkasse/gemeldete Krankenkasse - '
                                              'gleiche Krankenkasse, andere Abkuerzung.xlsx',
                                              self.testschema)

        self.assertEqual(str(context.exception), "FEHLER:  Gemeldete Krankenkasse 'Techniker Krankenkasse' ist bereits "
                                                 "vorhanden! Uebergebene Daten werden nicht eingetragen! Wenn Sie diese "
                                                 "Daten aktualisieren wollen, nutzen Sie bitte die "
                                                 "'update_gemeldete_Krankenkasse'-Funktion!\n"
                                                 "CONTEXT:  PL/pgSQL-Funktion insert_gemeldete_krankenkasse(integer,"
                                                 "character varying,character varying,numeric,numeric,numeric,character"
                                                 " varying,date) Zeile 17 bei RAISE\n")

        # Inhalte aus Tabellen ziehen, um zu pruefen, ob auch weiterhin nur ein Datensatz angelegt wurde
        ergebnis = self.testfirma.get_nutzer("M100001").abfrage_ausfuehren("SELECT * FROM gemeldete_krankenkassen",
                                                                           self.testschema)
        self.assertEqual(str(ergebnis), "[(1, 1, 'Techniker Krankenkasse', 'TK')]")

        ergebnis = self.testfirma.get_nutzer("M100001").abfrage_ausfuehren("SELECT * FROM umlagen",
                                                                           self.testschema)
        self.assertEqual(str(ergebnis), "[(1, 1, Decimal('1.600'), Decimal('0.440'), Decimal('0.060'), 'anders')]")

        ergebnis = self.testfirma.get_nutzer("M100001").abfrage_ausfuehren("SELECT * FROM hat_umlagen_anderweitig",
                                                                           self.testschema)
        self.assertEqual(str(ergebnis), "[(1, 1, 1, datetime.date(2023, 12, 15), datetime.date(9999, 12, 31))]")

    def tearDown(self):
        """
        Methode ruft Funktion 'test_tear_down' auf, welches das Datenbankschema 'temp_test_schema' mit allen Daten
        entfernt.
        """
        test_tear_down(self.conn, self.cur)
