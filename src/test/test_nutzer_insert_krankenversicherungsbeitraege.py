import unittest

from src.main.Login import Login
from src.test.test_SetUp_TearDown import test_set_up, test_tear_down


class TestNutzerInsertKrankenversicherungsbeitraege(unittest.TestCase):

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
        Test prueft, ob Krankenversicherungsbeitraege eingetragen werden.
        """
        self.nutzer.insert_krankenversicherungsbeitraege(
            'testdaten_insert_krankenversicherungsbeitraege/Krankenversicherungsbeitraege.xlsx')

        # Inhalte aus Tabellen ziehen, um zu pruefen, ob der Datensatz angelegt wurde
        ergebnis = self.nutzer.abfrage_ausfuehren("SELECT * FROM gkv_beitraege")
        self.assertEqual(str(ergebnis), "[(1, 1, Decimal('7.300'), Decimal('7.300'), Decimal('72453.56'), "
                                        "Decimal('75683.12'))]")

        ergebnis = self.nutzer.abfrage_ausfuehren("SELECT * FROM krankenversicherungen")
        self.assertEqual(str(ergebnis), "[(1, 1, False)]")

        ergebnis = self.nutzer.abfrage_ausfuehren("SELECT * FROM hat_GKV_Beitraege")
        self.assertEqual(str(ergebnis), "[(1, 1, 1, datetime.date(2023, 12, 15), datetime.date(9999, 12, 31))]")

    def test_kein_doppelter_eintrag(self):
        """
        Test prueft, ob bei wiederholtem Aufruf der Methode 'insert_krankenversicherungsbeitraege' mit derselben Angabe,
        ob es der ermaessigte Beitrag ist, und denselben Beitragssaetzen dieser nicht erneut eingetragen wird. Beim
        zweiten Eintrag muss eine Fehlermeldung erscheinen. Massgeblich sit hier lediglich der boolesche Wert
        "ermaessigter_beitragssatz" in Tabelle "Krankenversicherungen". Die Fehlermeldung soll auch erscheinen, wenn die
        Beitragssaetze anders sind. Sollen nur die Beitragssaetze geaendert werden, muss hierfuer die update-Methode
        'update_krankenversicherungsbeitraege' verwendet werden.
        """
        self.nutzer.insert_krankenversicherungsbeitraege(
            'testdaten_insert_krankenversicherungsbeitraege/Krankenversicherungsbeitraege.xlsx')

        # Versuch, nochmal den nicht ermaessigten Beitragssatz einzutragen
        with self.assertRaises(Exception) as context:
            self.nutzer.insert_krankenversicherungsbeitraege(
                'testdaten_insert_krankenversicherungsbeitraege/Krankenversicherungsbeitraege.xlsx')

        erwartete_fehlermeldung = "FEHLER:  Ermaessigung = 'f' ist bereits vorhanden! Uebergebene Daten werden nicht " \
                                  "eingetragen! Wenn Sie diese Daten aktualisieren wollen, nutzen Sie bitte die " \
                                  "'update_krankenversicherungsbeitraege'-Funktion!"
        tatsaechliche_fehlermeldung = str(context.exception)
        self.assertTrue(tatsaechliche_fehlermeldung.startswith(erwartete_fehlermeldung))

        # Inhalte aus Tabellen ziehen, um zu pruefen, ob auch weiterhin nur ein Datensatz angelegt wurde
        ergebnis = self.nutzer.abfrage_ausfuehren("SELECT * FROM gkv_beitraege")
        self.assertEqual(str(ergebnis), "[(1, 1, Decimal('7.300'), Decimal('7.300'), Decimal('72453.56'), "
                                        "Decimal('75683.12'))]")

        ergebnis = self.nutzer.abfrage_ausfuehren("SELECT * FROM krankenversicherungen")
        self.assertEqual(str(ergebnis), "[(1, 1, False)]")

        ergebnis = self.nutzer.abfrage_ausfuehren("SELECT * FROM hat_GKV_Beitraege")
        self.assertEqual(str(ergebnis), "[(1, 1, 1, datetime.date(2023, 12, 15), datetime.date(9999, 12, 31))]")

    def test_kein_doppelter_eintrag_andere_werte(self):
        """
        Test prueft, ob bei wiederholtem Aufruf der Methode 'insert_krankenversicherungsbeitraege' mit derselben Angabe,
        ob es der ermaessigte Beitrag ist, aber anderen Beitragssaetzen dieser nicht erneut eingetragen wird. Beim
        zweiten Eintrag muss eine Fehlermeldung erscheinen. Massgeblich ist hier lediglich der boolesche Wert
        "ermaessigter_beitragssatz" in Tabelle "Krankenversicherungen". Die Fehlermeldung soll auch erscheinen, wenn die
        Beitragssaetze anders sind. Sollen nur die Beitragssaetze geaendert werden, muss hierfuer die update-Methode
        'update_krankenversicherungsbeitraege' verwendet werden.
        """
        self.nutzer.insert_krankenversicherungsbeitraege(
            'testdaten_insert_krankenversicherungsbeitraege/Krankenversicherungsbeitraege.xlsx')

        # Versuch, nochmal den nicht ermaessigten Beitragssatz (aber mit anderen Werten) einzutragen
        with self.assertRaises(Exception) as context:
            self.nutzer.insert_krankenversicherungsbeitraege(
                'testdaten_insert_krankenversicherungsbeitraege/Krankenversicherungsbeitraege - '
                'selbe Ermaessigung.xlsx')

        erwartete_fehlermeldung = "FEHLER:  Ermaessigung = 'f' ist bereits vorhanden! Uebergebene Daten werden " \
                                  "nicht eingetragen! Wenn Sie diese Daten aktualisieren wollen, nutzen Sie bitte " \
                                  "die 'update_krankenversicherungsbeitraege'-Funktion!"
        tatsaechliche_fehlermeldung = str(context.exception)
        self.assertTrue(tatsaechliche_fehlermeldung.startswith(erwartete_fehlermeldung))

        # Inhalte aus Tabellen ziehen, um zu pruefen, ob auch weiterhin nur ein Datensatz angelegt wurde
        ergebnis = self.nutzer.abfrage_ausfuehren("SELECT * FROM gkv_beitraege")
        self.assertEqual(str(ergebnis), "[(1, 1, Decimal('7.300'), Decimal('7.300'), Decimal('72453.56'), "
                                        "Decimal('75683.12'))]")

        ergebnis = self.nutzer.abfrage_ausfuehren("SELECT * FROM krankenversicherungen")
        self.assertEqual(str(ergebnis), "[(1, 1, False)]")

        ergebnis = self.nutzer.abfrage_ausfuehren("SELECT * FROM hat_GKV_Beitraege")
        self.assertEqual(str(ergebnis), "[(1, 1, 1, datetime.date(2023, 12, 15), datetime.date(9999, 12, 31))]")

    def tearDown(self):
        """
        Methode ruft Funktion 'test_tear_down' auf, welches das Datenbankschema 'temp_test_schema' mit allen Daten
        entfernt.
        """
        test_tear_down()
