import unittest

from src.main.Login import Login
from src.main.test_SetUp_TearDown import test_set_up, test_tear_down


class TestNutzerInsertGesetzlicheKrankenkasse(unittest.TestCase):

    def setUp(self):
        """
        Methode ruft Funktion 'test_set_up' der Klasse 'test_SetUp_TearDown' (siehe Ordner 'main') auf, welches das
        Datenbankschema 'temp_test_schema' erstellt.
        """
        self.testschema = test_set_up()

        login = Login(self.testschema)
        login.registriere_mandant_und_admin('Testfirma', 'mandantenpw', 'mandantenpw', 'M100000', 'Otto',
                                            'Normalverbraucher', 'adminpw', 'adminpw')
        self.admin = login.login_admin('Testfirma', 'mandantenpw', 'M100000', 'adminpw')
        self.admin.nutzer_anlegen('M100001', 'Erika', 'Musterfrau', 'nutzerpw', 'nutzerpw')

        self.nutzer = login.login_nutzer('Testfirma', 'mandantenpw', 'M100001', 'nutzerpw')
        self.nutzer.passwort_aendern('neues passwort', 'neues passwort')

    def test_erfolgreicher_eintrag(self):
        """
        Test prueft, ob gesetzliche Krankenkasse mit ihrem Zusatzbeitrag und Umlagebeitraegen eingetragen werden.
        """
        self.nutzer.insert_gesetzliche_krankenkasse('testdaten_insert_gesetzliche_krankenkasse/'
                                                    'gesetzliche Krankenkasse.xlsx')

        # Inhalte aus Tabellen ziehen, um zu pruefen, ob der Datensatz angelegt wurde
        ergebnis = self.nutzer.abfrage_ausfuehren("SELECT * FROM gesetzliche_Krankenkassen")
        self.assertEqual(str(ergebnis), "[(1, 1, 'Kaufmaennische Krankenkasse', 'KKH')]")

        ergebnis = self.nutzer.abfrage_ausfuehren("SELECT * FROM gkv_zusatzbeitraege")
        self.assertEqual(str(ergebnis), "[(1, 1, Decimal('1.500'))]")

        ergebnis = self.nutzer.abfrage_ausfuehren("SELECT * FROM hat_gkv_zusatzbeitrag")
        self.assertEqual(str(ergebnis), "[(1, 1, 1, datetime.date(2023, 12, 15), datetime.date(9999, 12, 31))]")

        ergebnis = self.nutzer.abfrage_ausfuehren("SELECT * FROM umlagen")
        self.assertEqual(str(ergebnis), "[(1, 1, Decimal('1.600'), Decimal('0.440'), Decimal('0.060'), 'gesetzlich')]")

        ergebnis = self.nutzer.abfrage_ausfuehren("SELECT * FROM hat_umlagen_gesetzlich")
        self.assertEqual(str(ergebnis), "[(1, 1, 1, datetime.date(2023, 12, 15), datetime.date(9999, 12, 31))]")

    def test_kein_doppelter_eintrag(self):
        """
        Test prueft, ob bei wiederholtem Aufruf der Methode 'insert_gesetzliche_krankenkasse' mit derselben Krankenkasse
        dieser nicht mehrfach eingetragen wird. Beim zweiten Eintrag muss eine Exception geworfen werden. Massgeblich
        ist hier lediglich der Wert "krankenkasse_gesetzlich" in Tabelle "gesetzliche_krankenkassen". Die Exception wird
        auch dann geworfen, wenn die restlichen Werte anders sind. Sollen nur die restlichen Werte geaendert werden,
        muss hierfuer eine update-Methode verwendet werden (welche im Rahmen dieser Arbeit nicht implementiert wird).
        """
        self.nutzer.insert_gesetzliche_krankenkasse('testdaten_insert_gesetzliche_krankenkasse/'
                                                    'gesetzliche Krankenkasse.xlsx')

        # Versuch, dieselbe Krankenkasse einzutragen
        with self.assertRaises(Exception) as context:
            self.nutzer.insert_gesetzliche_krankenkasse(
                'testdaten_insert_gesetzliche_krankenkasse/gesetzliche Krankenkasse.xlsx')

        erwartete_fehlermeldung = "FEHLER:  Gesetzliche Krankenkasse 'Kaufmaennische Krankenkasse' ist bereits " \
                                  "vorhanden! Uebergebene Daten werden nicht eingetragen! Wenn Sie diese Daten " \
                                  "aktualisieren wollen, nutzen Sie bitte die 'update_gesetzliche_krankenkasse'" \
                                  "-Funktion!"
        tatsaechliche_fehlermeldung = str(context.exception)
        self.assertTrue(tatsaechliche_fehlermeldung.startswith(erwartete_fehlermeldung))

        # Inhalte aus Tabellen ziehen, um zu pruefen, ob auch weiterhin nur ein Datensatz angelegt wurde
        ergebnis = self.nutzer.abfrage_ausfuehren("SELECT * FROM gesetzliche_Krankenkassen")
        self.assertEqual(str(ergebnis), "[(1, 1, 'Kaufmaennische Krankenkasse', 'KKH')]")

        ergebnis = self.nutzer.abfrage_ausfuehren("SELECT * FROM gkv_zusatzbeitraege")
        self.assertEqual(str(ergebnis), "[(1, 1, Decimal('1.500'))]")

        ergebnis = self.nutzer.abfrage_ausfuehren("SELECT * FROM hat_gkv_zusatzbeitrag")
        self.assertEqual(str(ergebnis), "[(1, 1, 1, datetime.date(2023, 12, 15), datetime.date(9999, 12, 31))]")

        ergebnis = self.nutzer.abfrage_ausfuehren("SELECT * FROM umlagen")
        self.assertEqual(str(ergebnis), "[(1, 1, Decimal('1.600'), Decimal('0.440'), Decimal('0.060'), 'gesetzlich')]")
        ergebnis = self.nutzer.abfrage_ausfuehren("SELECT * FROM hat_umlagen_gesetzlich")
        self.assertEqual(str(ergebnis), "[(1, 1, 1, datetime.date(2023, 12, 15), datetime.date(9999, 12, 31))]")

    def test_kein_doppelter_eintrag_krankenkasse_case_insensitive(self):
        """
        Test prueft, ob bei wiederholtem Aufruf der Methode 'insert_gesetzliche_krankenkasse' mit derselben Krankenkasse
        klein geschrieben dieser nicht mehrfach eingetragen wird. Beim zweiten Eintrag muss eine Exception geworfen
        werden. Massgeblich ist hier lediglich der Wert "krankenkasse_gesetzlich" in Tabelle
        "gesetzliche_krankenkassen". Die Exception wird auch dann geworfen, wenn die restlichen Werte anders sind.
        Sollen nur die restlichen Werte geaendert werden, muss hierfuer eine update-Methode verwendet werden (welche im
        Rahmen dieser Arbeit nicht implementiert wird).
        """
        self.nutzer.insert_gesetzliche_krankenkasse(
            'testdaten_insert_gesetzliche_krankenkasse/gesetzliche Krankenkasse.xlsx')

        # Versuch, dieselbe Krankenkasse (klein geschrieben) einzutragen
        with self.assertRaises(Exception) as context:
            self.nutzer.insert_gesetzliche_krankenkasse(
                'testdaten_insert_gesetzliche_krankenkasse/gesetzliche Krankenkasse - '
                'Krankenkasse klein geschrieben.xlsx')

        erwartete_fehlermeldung = "FEHLER:  Gesetzliche Krankenkasse 'kaufmaennische krankenkasse' oder dessen " \
                                  "Kuerzel 'KKH' bereits vorhanden!"
        tatsaechliche_fehlermeldung = str(context.exception)
        self.assertTrue(tatsaechliche_fehlermeldung.startswith(erwartete_fehlermeldung))

        # Inhalte aus Tabellen ziehen, um zu pruefen, ob auch weiterhin nur ein Datensatz angelegt wurde
        ergebnis = self.nutzer.abfrage_ausfuehren("SELECT * FROM gesetzliche_Krankenkassen")
        self.assertEqual(str(ergebnis), "[(1, 1, 'Kaufmaennische Krankenkasse', 'KKH')]")

        ergebnis = self.nutzer.abfrage_ausfuehren("SELECT * FROM gkv_zusatzbeitraege")
        self.assertEqual(str(ergebnis), "[(1, 1, Decimal('1.500'))]")

        ergebnis = self.nutzer.abfrage_ausfuehren("SELECT * FROM hat_gkv_zusatzbeitrag")
        self.assertEqual(str(ergebnis), "[(1, 1, 1, datetime.date(2023, 12, 15), datetime.date(9999, 12, 31))]")

        ergebnis = self.nutzer.abfrage_ausfuehren("SELECT * FROM umlagen")
        self.assertEqual(str(ergebnis), "[(1, 1, Decimal('1.600'), Decimal('0.440'), Decimal('0.060'), "
                                        "'gesetzlich')]")
        ergebnis = self.nutzer.abfrage_ausfuehren("SELECT * FROM hat_umlagen_gesetzlich")
        self.assertEqual(str(ergebnis), "[(1, 1, 1, datetime.date(2023, 12, 15), datetime.date(9999, 12, 31))]")

    def test_kein_doppelter_eintrag_andere_krankenkasse_gleiche_abkuerzung(self):
        """
        Test prueft, ob bei wiederholtem Aufruf der Methode 'insert_gesetzliche_krankenkasse' mit anderer Krankenkasse
        (fuer diesen Zweck wurde zwar wieder die 'kaufmaennische Krankenkasse' verwendet, aber ohne Leerzeichen)
        aber gleichem Kuerzel nicht mehrfach eingetragen wird. Beim zweiten Eintrag muss eine
        Exception geworfen werden. Die Exception wird auch dann geworfen, wenn die restlichen Werte anders sind.
        Sollen nur die restlichen Werte geaendert werden, muss hierfuer eine update-Methode verwendet werden (welche im
        Rahmen dieser Arbeit nicht implementiert wird).
        """
        self.nutzer.insert_gesetzliche_krankenkasse(
            'testdaten_insert_gesetzliche_krankenkasse/gesetzliche Krankenkasse.xlsx')

        # Versuch, Krankenkasse (falsch geschrieben) einzutragen
        with self.assertRaises(Exception) as context:
            self.nutzer.insert_gesetzliche_krankenkasse(
                'testdaten_insert_gesetzliche_krankenkasse/gesetzliche Krankenkasse - '
                'andere Krankenkasse, gleiche Abkuerzung.xlsx')

        erwartete_fehlermeldung = "FEHLER:  Gesetzliche Krankenkasse 'KaufmaennischeKrankenkasse' oder dessen " \
                                  "Kuerzel 'KKH' bereits vorhanden!"
        tatsaechliche_fehlermeldung = str(context.exception)
        self.assertTrue(tatsaechliche_fehlermeldung.startswith(erwartete_fehlermeldung))

        # Inhalte aus Tabellen ziehen, um zu pruefen, ob auch weiterhin nur ein Datensatz angelegt wurde
        ergebnis = self.nutzer.abfrage_ausfuehren("SELECT * FROM gesetzliche_Krankenkassen")
        self.assertEqual(str(ergebnis), "[(1, 1, 'Kaufmaennische Krankenkasse', 'KKH')]")

        ergebnis = self.nutzer.abfrage_ausfuehren("SELECT * FROM gkv_zusatzbeitraege")
        self.assertEqual(str(ergebnis), "[(1, 1, Decimal('1.500'))]")

        ergebnis = self.nutzer.abfrage_ausfuehren("SELECT * FROM hat_gkv_zusatzbeitrag")
        self.assertEqual(str(ergebnis), "[(1, 1, 1, datetime.date(2023, 12, 15), datetime.date(9999, 12, 31))]")

        ergebnis = self.nutzer.abfrage_ausfuehren("SELECT * FROM umlagen")
        self.assertEqual(str(ergebnis), "[(1, 1, Decimal('1.600'), Decimal('0.440'), Decimal('0.060'), "
                                        "'gesetzlich')]")
        ergebnis = self.nutzer.abfrage_ausfuehren("SELECT * FROM hat_umlagen_gesetzlich")
        self.assertEqual(str(ergebnis), "[(1, 1, 1, datetime.date(2023, 12, 15), datetime.date(9999, 12, 31))]")

    def test_kein_doppelter_eintrag_gleiche_krankenkasse_andere_abkuerzung(self):
        """
        Test prueft, ob bei wiederholtem Aufruf der Methode 'insert_gesetzliche_krankenkasse' mit gleicher Krankenkasse
        aber anderem Kuerzel (statt richtigerweise 'KKH' wurde 'KK' angegeben) nicht mehrfach eingetragen wird.
        Beim zweiten Eintrag muss eine Exception geworfen werden. Die Exception wird auch dann geworfen, wenn die
        restlichen Werte anders sind. Sollen nur die restlichen Werte geaendert werden, muss hierfuer eine
        update-Methode verwendet werden (welche im Rahmen dieser Arbeit nicht implementiert wird).
        """
        self.nutzer.insert_gesetzliche_krankenkasse(
            'testdaten_insert_gesetzliche_krankenkasse/gesetzliche Krankenkasse.xlsx')

        # Versuch, die gleiche Krankenkasse mit anderer Abkuerzung einzutragen
        with self.assertRaises(Exception) as context:
            self.nutzer.insert_gesetzliche_krankenkasse(
                'testdaten_insert_gesetzliche_krankenkasse/gesetzliche Krankenkasse - '
                'gleiche Krankenkasse, andere Abkuerzung.xlsx')

        erwartete_fehlermeldung = "FEHLER:  Gesetzliche Krankenkasse 'Kaufmaennische Krankenkasse' ist bereits " \
                                  "vorhanden! Uebergebene Daten werden nicht eingetragen! Wenn Sie diese Daten " \
                                  "aktualisieren wollen, nutzen Sie bitte die 'update_gesetzliche_krankenkasse'-" \
                                  "Funktion!"
        tatsaechliche_fehlermeldung = str(context.exception)
        self.assertTrue(tatsaechliche_fehlermeldung.startswith(erwartete_fehlermeldung))

        # Inhalte aus Tabellen ziehen, um zu pruefen, ob auch weiterhin nur ein Datensatz angelegt wurde
        ergebnis = self.nutzer.abfrage_ausfuehren("SELECT * FROM gesetzliche_Krankenkassen")
        self.assertEqual(str(ergebnis), "[(1, 1, 'Kaufmaennische Krankenkasse', 'KKH')]")

        ergebnis = self.nutzer.abfrage_ausfuehren("SELECT * FROM gkv_zusatzbeitraege")
        self.assertEqual(str(ergebnis), "[(1, 1, Decimal('1.500'))]")

        ergebnis = self.nutzer.abfrage_ausfuehren("SELECT * FROM hat_gkv_zusatzbeitrag")
        self.assertEqual(str(ergebnis), "[(1, 1, 1, datetime.date(2023, 12, 15), datetime.date(9999, 12, 31))]")

        ergebnis = self.nutzer.abfrage_ausfuehren("SELECT * FROM umlagen")
        self.assertEqual(str(ergebnis), "[(1, 1, Decimal('1.600'), Decimal('0.440'), Decimal('0.060'), 'gesetzlich')]")

        ergebnis = self.nutzer.abfrage_ausfuehren("SELECT * FROM hat_umlagen_gesetzlich")
        self.assertEqual(str(ergebnis), "[(1, 1, 1, datetime.date(2023, 12, 15), datetime.date(9999, 12, 31))]")

    def tearDown(self):
        """
        Methode ruft Funktion 'test_tear_down' auf, welches das Datenbankschema 'temp_test_schema' mit allen Daten
        entfernt.
        """
        test_tear_down()
