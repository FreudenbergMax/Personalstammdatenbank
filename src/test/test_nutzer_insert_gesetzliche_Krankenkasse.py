import unittest

from src.main.Login import Login
from src.test.test_SetUp_TearDown import test_set_up, test_tear_down


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

    def test_erfolgreicher_eintrag_mit_abkuerzung(self):
        """
        Test prueft, ob gesetzliche Krankenkasse mit dessen Abkuerzung und mit ihrem Zusatzbeitrag und Umlagebeitraegen
        eingetragen werden.
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

    def test_erfolgreicher_eintrag_ohne_abkuerzung(self):
        """
        Test prueft, ob gesetzliche Krankenkasse ohne dessen Abkuerzung und mit ihrem Zusatzbeitrag und Umlagebeitraegen
        eingetragen werden.
        """
        self.nutzer.insert_gesetzliche_krankenkasse(
            'testdaten_insert_gesetzliche_krankenkasse/gesetzliche Krankenkasse - ohne Abkuerzung.xlsx')

        # Inhalte aus Tabellen ziehen, um zu pruefen, ob der Datensatz angelegt wurde
        ergebnis = self.nutzer.abfrage_ausfuehren("SELECT * FROM gesetzliche_Krankenkassen")
        self.assertEqual(str(ergebnis), "[(1, 1, 'Kaufmaennische Krankenkasse', None)]")

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
        dieser nicht mehrfach eingetragen wird. Beim zweiten Eintrag muss eine Fehlermeldung erscheinen. Massgeblich
        ist hier lediglich der Wert "krankenkasse_gesetzlich" in Tabelle "gesetzliche_krankenkassen". Die Fehlermeldung
        erscheint auch, wenn die restlichen Werte anders sind. Sollen nur die restlichen Werte geaendert werden,
        muss hierfuer eine update-Methode verwendet werden (welche im Rahmen dieser Arbeit nicht implementiert wird).
        """
        self.nutzer.insert_gesetzliche_krankenkasse('testdaten_insert_gesetzliche_krankenkasse/'
                                                    'gesetzliche Krankenkasse.xlsx')

        # Versuch, dieselbe Krankenkasse einzutragen
        with self.assertRaises(Exception) as context:
            self.nutzer.insert_gesetzliche_krankenkasse(
                'testdaten_insert_gesetzliche_krankenkasse/gesetzliche Krankenkasse.xlsx')

        erwartete_fehlermeldung = "FEHLER:  Gesetzliche Krankenkasse 'Kaufmaennische Krankenkasse' ist bereits " \
                                  "vorhanden! Uebergebene Daten werden nicht eingetragen!"
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
        klein geschrieben dieser nicht mehrfach eingetragen wird. Beim zweiten Eintrag muss eine Fehlermeldung
        erscheinen. Massgeblich ist hier lediglich der Wert "krankenkasse_gesetzlich" in Tabelle
        "gesetzliche_krankenkassen". Die Fehlermeldung soll auch erscheinen, wenn die restlichen Werte anders sind.
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

        erwartete_fehlermeldung = "FEHLER:  Gesetzliche Krankenkasse 'kaufmaennische krankenkasse' bereits vorhanden!"
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

    def tearDown(self):
        """
        Methode ruft Funktion 'test_tear_down' auf, welches das Datenbankschema 'temp_test_schema' mit allen Daten
        entfernt.
        """
        test_tear_down()
