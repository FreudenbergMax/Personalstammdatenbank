import unittest

from src.main.Login import Login
from src.test.test_SetUp_TearDown import test_set_up, test_tear_down


class TestNutzerInsertMinijobbeitraege(unittest.TestCase):

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
        Test prueft, ob Minijobbeitraege in Datenbank eingetragen werden.
        """
        self.nutzer.insert_minijobbeitraege('testdaten_insert_minijobbeitraege/Minijobbeitraege.xlsx')

        # Inhalte aus Tabellen ziehen, um zu pruefen, ob der Datensatz angelegt wurde
        ergebnis = self.nutzer.abfrage_ausfuehren("SELECT * FROM Minijobs")
        self.assertEqual(str(ergebnis), "[(1, 1, False, True)]")

        ergebnis = self.nutzer.abfrage_ausfuehren("SELECT * FROM Pauschalabgaben")
        self.assertEqual(str(ergebnis), "[(1, 1, Decimal('13.000'), Decimal('15.000'), Decimal('3.600'), "
                                        "Decimal('1.100'), Decimal('0.240'), Decimal('0.060'), Decimal('2.000'))]")

        ergebnis = self.nutzer.abfrage_ausfuehren("SELECT * FROM hat_Pauschalabgaben")
        self.assertEqual(str(ergebnis), "[(1, 1, 1, datetime.date(2024, 1, 1), datetime.date(9999, 12, 31))]")

    def test_kein_doppelter_eintrag(self):
        """
        Test prueft, ob bei wiederholtem Aufruf der Methode 'insert_minijobbeitraege' mit denselben Angaben nicht erneut
        eingetragen wird. Beim zweiten Eintrag muss eine Fehlermeldung erscheinen. Massgeblich ist hier lediglich der
        boolesche Wert "kurzfristig_beschaeftigt" in Tabelle "Minijobs". Die Fehlermeldung soll auch dann erscheinen,
        wenn die Beitragssaetze anders sind.
        """
        self.nutzer.insert_minijobbeitraege('testdaten_insert_minijobbeitraege/Minijobbeitraege.xlsx')

        with self.assertRaises(Exception) as context:
            self.nutzer.insert_minijobbeitraege('testdaten_insert_minijobbeitraege/Minijobbeitraege.xlsx')

        erwartete_fehlermeldung = "FEHLER:  Kurzfristige Beschaeftigung = 'f' mit AN-Rentenpauschale = 't' ist " \
                                  "bereits vorhanden! Uebergebene Daten werden nicht eingetragen!"
        tatsaechliche_fehlermeldung = str(context.exception)
        self.assertTrue(tatsaechliche_fehlermeldung.startswith(erwartete_fehlermeldung))

        # Inhalte aus Tabellen ziehen, um zu pruefen, ob der Datensatz angelegt wurde
        ergebnis = self.nutzer.abfrage_ausfuehren("SELECT * FROM Minijobs")
        self.assertEqual(str(ergebnis), "[(1, 1, False, True)]")

        ergebnis = self.nutzer.abfrage_ausfuehren("SELECT * FROM Pauschalabgaben")
        self.assertEqual(str(ergebnis), "[(1, 1, Decimal('13.000'), Decimal('15.000'), Decimal('3.600'), "
                                        "Decimal('1.100'), Decimal('0.240'), Decimal('0.060'), Decimal('2.000'))]")

        ergebnis = self.nutzer.abfrage_ausfuehren("SELECT * FROM hat_Pauschalabgaben")
        self.assertEqual(str(ergebnis), "[(1, 1, 1, datetime.date(2024, 1, 1), datetime.date(9999, 12, 31))]")

    def test_kein_doppelter_eintrag_andere_werte(self):
        """
        Test prueft, ob bei wiederholtem Aufruf der Methode 'insert_minijobbeitraege' mit demselben
        booleschen Wahrheitswert (= false), aber mit anderem Beitragssaetzen, dennoch nicht eingetragen wird. Beim
        zweiten Eintrag muss eine Fehlermeldung erscheinen. Massgeblich ist hier lediglich der boolesche Wert
        "kurzfristig_beschaeftigt" in Tabelle "Minijobs". Die Fehlermeldung soll auch erscheinen, wenn die
        Beitragssaetze anders sind. Sollen nur die Beitragssaetze geaendert werden, muss hierfuer eine update-Methode
        verwendet werden (welche im Rahmen dieser Bachelorarbeit nicht implementiert wird).
        """
        self.nutzer.insert_minijobbeitraege('testdaten_insert_minijobbeitraege/Minijobbeitraege.xlsx')

        with self.assertRaises(Exception) as context:
            self.nutzer.insert_minijobbeitraege('testdaten_insert_minijobbeitraege/Minijobbeitraege.xlsx')

        erwartete_fehlermeldung = "FEHLER:  Kurzfristige Beschaeftigung = 'f' mit AN-Rentenpauschale = 't' ist " \
                                  "bereits vorhanden! Uebergebene Daten werden nicht eingetragen!"
        tatsaechliche_fehlermeldung = str(context.exception)
        self.assertTrue(tatsaechliche_fehlermeldung.startswith(erwartete_fehlermeldung))

        # Inhalte aus Tabellen ziehen, um zu pruefen, ob der Datensatz angelegt wurde
        ergebnis = self.nutzer.abfrage_ausfuehren("SELECT * FROM Minijobs")
        self.assertEqual(str(ergebnis), "[(1, 1, False, True)]")

        ergebnis = self.nutzer.abfrage_ausfuehren("SELECT * FROM Pauschalabgaben")
        self.assertEqual(str(ergebnis), "[(1, 1, Decimal('13.000'), Decimal('15.000'), Decimal('3.600'), "
                                        "Decimal('1.100'), Decimal('0.240'), Decimal('0.060'), Decimal('2.000'))]")

        ergebnis = self.nutzer.abfrage_ausfuehren("SELECT * FROM hat_Pauschalabgaben")
        self.assertEqual(str(ergebnis), "[(1, 1, 1, datetime.date(2024, 1, 1), datetime.date(9999, 12, 31))]")

    def test_kurzfristig_beschaeftigt_mit_an_rentenpauschale(self):
        """
        Test prueft, ob eine Fehlermeldung ausgegeben wird, wenn fehlerhafterweise angegeben wird, dass ein kurzfristig
        beschaeftigter Minijobber AN-Rentenpauschale zahlt. Dies ist rechtlich nicht moeglich
        """
        with self.assertRaises(ValueError) as context:
            self.nutzer.insert_minijobbeitraege('testdaten_insert_minijobbeitraege/'
                                                'Minijobbeitraege - kurzfristig beschaeftigt und zahlt '
                                                'AN-Rentenpauschale.xlsx')

        erwartete_fehlermeldung = "Ein kurzfristig beschaeftiger Minijobber zahlt keine AN-Rentenpauschale!"
        tatsaechliche_fehlermeldung = str(context.exception)
        self.assertTrue(tatsaechliche_fehlermeldung.startswith(erwartete_fehlermeldung))

    def tearDown(self):
        """
        Methode ruft Funktion 'test_tear_down' auf, welches das Datenbankschema 'temp_test_schema' mit allen Daten
        entfernt.
        """
        test_tear_down()
