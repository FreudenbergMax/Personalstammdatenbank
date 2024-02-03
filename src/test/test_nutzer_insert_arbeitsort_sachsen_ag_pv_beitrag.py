import unittest

from src.main.Login import Login
from src.main.test_SetUp_TearDown import test_set_up, test_tear_down


class TestNutzerInsertArbeitsortSachsen(unittest.TestCase):

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
        Test prueft, ob Pflegebeitragssatz der Arbeitgeber (dessen Hoehe abhaengig davon ist, ob der Arbeitgeber in
        Sachsen sitzt oder nicht) eingetragen werden.
        """
        self.nutzer.insert_arbeitsort_sachsen_ag_pv_beitrag('testdaten_insert_ag_pv_beitrag_sachsen/'
                                                            'Arbeitsort Sachsen Arbeitgeber PV-Beitrag.xlsx')

        # Inhalte aus Tabellen ziehen, um zu pruefen, ob der Datensatz angelegt wurde
        ergebnis = self.nutzer.abfrage_ausfuehren("SELECT * FROM Arbeitsort_Sachsen")
        self.assertEqual(str(ergebnis), "[(1, 1, True)]")

        ergebnis = self.nutzer.abfrage_ausfuehren("SELECT * FROM AG_Pflegeversicherungsbeitraege_gesetzlich")
        self.assertEqual(str(ergebnis), "[(1, 1, Decimal('1.200'))]")

        ergebnis = self.nutzer.abfrage_ausfuehren("SELECT * FROM hat_gesetzlichen_AG_PV_Beitragssatz")
        self.assertEqual(str(ergebnis), "[(1, 1, 1, datetime.date(2023, 12, 15), datetime.date(9999, 12, 31))]")

    def test_kein_doppelter_eintrag(self):
        """
        Test prueft, ob bei wiederholtem Aufruf der Methode 'insert_arbeitsort_sachsen_ag_pv_beitrag' mit derselben
        Angabe nicht mehrfach eingetragen wird. Beim zweiten Eintrag muss eine Fehlermeldung erscheinen. Massgeblich
        ist hier lediglich der boolesche Wert "in_Sachsen" in Tabelle "Arbeitsort_Sachsen". Die Fehlermeldung soll auch
        erscheinen, wenn der AG-Beitragssatz anders ist. Soll nur der Beitragssatz geaendert werden, muss hierfuer eine
        update-Methode verwendet werden (welche im Rahmen dieser Bachelorarbeit nicht implementiert wird).
        """
        self.nutzer.insert_arbeitsort_sachsen_ag_pv_beitrag('testdaten_insert_ag_pv_beitrag_sachsen/'
                                                            'Arbeitsort Sachsen Arbeitgeber PV-Beitrag.xlsx')

        # Versuch, nochmal den nicht ermaessigten Beitragssatz einzutragen
        with self.assertRaises(Exception) as context:
            self.nutzer.insert_arbeitsort_sachsen_ag_pv_beitrag('testdaten_insert_ag_pv_beitrag_sachsen/'
                                                                'Arbeitsort Sachsen Arbeitgeber PV-Beitrag.xlsx')

        erwartete_fehlermeldung = "FEHLER:  arbeitsort_sachsen = 't' ist bereits vorhanden! Uebergebene " \
                                  "Daten werden nicht eingetragen!"
        tatsaechliche_fehlermeldung = str(context.exception)
        self.assertTrue(tatsaechliche_fehlermeldung.startswith(erwartete_fehlermeldung))

        # Inhalte aus Tabellen ziehen, um zu pruefen, ob der Datensatz angelegt wurde
        ergebnis = self.nutzer.abfrage_ausfuehren("SELECT * FROM Arbeitsort_Sachsen")
        self.assertEqual(str(ergebnis), "[(1, 1, True)]")

        ergebnis = self.nutzer.abfrage_ausfuehren("SELECT * FROM AG_Pflegeversicherungsbeitraege_gesetzlich")
        self.assertEqual(str(ergebnis), "[(1, 1, Decimal('1.200'))]")

        ergebnis = self.nutzer.abfrage_ausfuehren("SELECT * FROM hat_gesetzlichen_AG_PV_Beitragssatz")
        self.assertEqual(str(ergebnis), "[(1, 1, 1, datetime.date(2023, 12, 15), datetime.date(9999, 12, 31))]")

    def test_kein_doppelter_eintrag_ebenfalls_true_andere_werte(self):
        """
        Test prueft, ob bei wiederholtem Aufruf der Methode 'insert_anzahl_kinder_an_pv_beitrag' mit demselben
        booleschen Wahrheitswert (= true), aber mit anderem Beitragssatz, dennoch nicht eingetragen wird. Beim zweiten
        Eintrag muss eine Fehlermeldung erscheinen. Massgeblich ist hier lediglich der boolesche Wert "in_Sachsen" in
        Tabelle "Arbeitsort_Sachsen". Die Fehlermeldung soll auch erscheinen, wenn der AG-Beitragssatz anders ist. Soll
        nur der Beitragssatz geaendert werden, muss hierfuer eine update-Methode verwendet werden (welche im Rahmen
        dieser Bachelorarbeit nicht implementiert wird).
        """
        self.nutzer.insert_arbeitsort_sachsen_ag_pv_beitrag('testdaten_insert_ag_pv_beitrag_sachsen/'
                                                            'Arbeitsort Sachsen Arbeitgeber PV-Beitrag.xlsx')

        with self.assertRaises(Exception) as context:
            self.nutzer.insert_arbeitsort_sachsen_ag_pv_beitrag('testdaten_insert_ag_pv_beitrag_sachsen/Arbeitsort '
                                                                'Sachsen Arbeitgeber PV-Beitrag - '
                                                                'anderer Beitragssatz.xlsx')

        erwartete_fehlermeldung = "FEHLER:  arbeitsort_sachsen = 't' ist bereits vorhanden! Uebergebene " \
                                  "Daten werden nicht eingetragen!"
        tatsaechliche_fehlermeldung = str(context.exception)
        self.assertTrue(tatsaechliche_fehlermeldung.startswith(erwartete_fehlermeldung))

        # Inhalte aus Tabellen ziehen, um zu pruefen, ob der Datensatz angelegt wurde
        ergebnis = self.nutzer.abfrage_ausfuehren("SELECT * FROM Arbeitsort_Sachsen")
        self.assertEqual(str(ergebnis), "[(1, 1, True)]")

        ergebnis = self.nutzer.abfrage_ausfuehren("SELECT * FROM AG_Pflegeversicherungsbeitraege_gesetzlich")
        self.assertEqual(str(ergebnis), "[(1, 1, Decimal('1.200'))]")

        ergebnis = self.nutzer.abfrage_ausfuehren("SELECT * FROM hat_gesetzlichen_AG_PV_Beitragssatz")
        self.assertEqual(str(ergebnis), "[(1, 1, 1, datetime.date(2023, 12, 15), datetime.date(9999, 12, 31))]")

    def tearDown(self):
        """
        Methode ruft Funktion 'test_tear_down' auf, welches das Datenbankschema 'temp_test_schema' mit allen Daten
        entfernt.
        """
        test_tear_down()
