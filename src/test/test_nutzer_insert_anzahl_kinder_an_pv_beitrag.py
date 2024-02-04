import unittest

from src.main.Login import Login
from src.test.test_SetUp_TearDown import test_set_up, test_tear_down


class TestNutzerInsertAnzahlKinder(unittest.TestCase):

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
        Test prueft, ob die Kinderanzahl mit dessen Arbeitnehmerbeitrag und Beitragsbemessungsgrenzen eingetragen
        werden.
        """
        self.nutzer.insert_anzahl_kinder_an_pv_beitrag('testdaten_insert_anzahl_kinder/'
                                                       'Anzahl Kinder Arbeitnehmer PV-Beitrag.xlsx')

        # Inhalte aus Tabellen ziehen, um zu pruefen, ob der Datensatz angelegt wurde
        ergebnis = self.nutzer.abfrage_ausfuehren("SELECT * FROM an_pflegeversicherungsbeitraege_gesetzlich")
        self.assertEqual(str(ergebnis), "[(1, 1, Decimal('1.700'), Decimal('62100.00'), Decimal('69300.00'))]")

        ergebnis = self.nutzer.abfrage_ausfuehren("SELECT * FROM anzahl_kinder_unter_25")
        self.assertEqual(str(ergebnis), "[(1, 1, 1)]")

        ergebnis = self.nutzer.abfrage_ausfuehren("SELECT * FROM hat_gesetzlichen_an_pv_beitragssatz")
        self.assertEqual(str(ergebnis), "[(1, 1, 1, datetime.date(2024, 1, 1), datetime.date(9999, 12, 31))]")

    def test_kein_doppelter_eintrag(self):
        """
        Test prueft, ob bei wiederholtem Aufruf der Methode 'insert_anzahl_kinder_an_pv_beitrag' mit derselben Kinder-
        anzahl nicht eingetragen wird. Beim zweiten Eintrag muss eine Fehlermeldung ausgegeben werden. Massgeblich ist
        hier die Kinderanzahl. Sollen nur die Beitragsbemessungsgrenzen oder der AN-Beitragssatz geaendert werden, muss
        hierfuer die update-Methode verwendet werden (welche im Zuge der Arbeit nicht implementiert wird).
        """
        self.nutzer.insert_anzahl_kinder_an_pv_beitrag('testdaten_insert_anzahl_kinder/'
                                                       'Anzahl Kinder Arbeitnehmer PV-Beitrag.xlsx')

        # Versuch, nochmal den nicht ermaessigten Beitragssatz einzutragen
        with self.assertRaises(Exception) as context:
            self.nutzer.insert_anzahl_kinder_an_pv_beitrag('testdaten_insert_anzahl_kinder/'
                                                           'Anzahl Kinder Arbeitnehmer PV-Beitrag.xlsx')

        erwartete_fehlermeldung = "FEHLER:  Kinderanzahl '1' ist bereits vorhanden! Uebergebene Daten werden " \
                                  "nicht eingetragen!"
        tatsaechliche_fehlermeldung = str(context.exception)
        self.assertTrue(tatsaechliche_fehlermeldung.startswith(erwartete_fehlermeldung))

        # Inhalte aus Tabellen ziehen, um zu pruefen, ob der Datensatz angelegt wurde
        ergebnis = self.nutzer.abfrage_ausfuehren("SELECT * FROM an_pflegeversicherungsbeitraege_gesetzlich")
        self.assertEqual(str(ergebnis), "[(1, 1, Decimal('1.700'), Decimal('62100.00'), Decimal('69300.00'))]")

        ergebnis = self.nutzer.abfrage_ausfuehren("SELECT * FROM anzahl_kinder_unter_25")
        self.assertEqual(str(ergebnis), "[(1, 1, 1)]")

        ergebnis = self.nutzer.abfrage_ausfuehren("SELECT * FROM hat_gesetzlichen_an_pv_beitragssatz")
        self.assertEqual(str(ergebnis), "[(1, 1, 1, datetime.date(2024, 1, 1), datetime.date(9999, 12, 31))]")

    def test_kein_doppelter_eintrag_selbe_kinderanzahl_andere_werte(self):
        """
        Test prueft, ob bei wiederholtem Aufruf der Methode 'insert_anzahl_kinder_an_pv_beitrag' mit derselben Kinder-
        anzahl, aber mit anderen Werten, dennoch nicht eingetragen wird. Beim zweiten Eintrag muss eine Fehlermeldung
        ausgegeben werden. Massgeblich ist hier die Kinderanzahl. Die Exception wird auch dann geworfen, wenn die
        Beitragssaetze anders sind. Sollen nur die Beitragssaetze geaendert werden, muss hierfuer eine update-Methode
        verwendet werden (welche im Rahmen dieser Bachelorarbeit nicht implementiert wird).
        """
        self.nutzer.insert_anzahl_kinder_an_pv_beitrag('testdaten_insert_anzahl_kinder/'
                                                       'Anzahl Kinder Arbeitnehmer PV-Beitrag.xlsx')

        # Versuch, einen anderen ermaessigten Beitragssatz einzutragen
        with self.assertRaises(Exception) as context:
            self.nutzer.insert_anzahl_kinder_an_pv_beitrag('testdaten_insert_anzahl_kinder/Anzahl Kinder Arbeitnehmer '
                                                           'PV-Beitrag - selbe Kinderanzahl, andere Werte.xlsx')

        erwartete_fehlermeldung = "FEHLER:  Kinderanzahl '1' ist bereits vorhanden! Uebergebene Daten werden nicht " \
                                  "eingetragen!"
        tatsaechliche_fehlermeldung = str(context.exception)
        self.assertTrue(tatsaechliche_fehlermeldung.startswith(erwartete_fehlermeldung))

        # Inhalte aus Tabellen ziehen, um zu pruefen, ob der Datensatz angelegt wurde
        ergebnis = self.nutzer.abfrage_ausfuehren("SELECT * FROM an_pflegeversicherungsbeitraege_gesetzlich")
        self.assertEqual(str(ergebnis), "[(1, 1, Decimal('1.700'), Decimal('62100.00'), Decimal('69300.00'))]")

        ergebnis = self.nutzer.abfrage_ausfuehren("SELECT * FROM anzahl_kinder_unter_25")
        self.assertEqual(str(ergebnis), "[(1, 1, 1)]")

        ergebnis = self.nutzer.abfrage_ausfuehren("SELECT * FROM hat_gesetzlichen_an_pv_beitragssatz")
        self.assertEqual(str(ergebnis), "[(1, 1, 1, datetime.date(2024, 1, 1), datetime.date(9999, 12, 31))]")

    def tearDown(self):
        """
        Methode ruft Funktion 'test_tear_down' auf, welches das Datenbankschema 'temp_test_schema' mit allen Daten
        entfernt.
        """
        test_tear_down()
