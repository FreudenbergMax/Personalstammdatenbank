import unittest

from src.main.Login import Login
from src.main.test_SetUp_TearDown import test_set_up, test_tear_down


class TestNutzerUpdateKrankenversicherungsbeitraege(unittest.TestCase):

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

        # Krankenversicherungsbeitraege eingeben
        self.nutzer.insert_krankenversicherungsbeitraege(
            'testdaten_insert_krankenversicherungsbeitraege/Krankenversicherungsbeitraege.xlsx')

    def test_erfolgreicher_eintrag(self):
        """
        Test prueft, ob Krankenversicherungsbeitraege erfolgreich aktualisiert werden
        """
        self.nutzer.update_krankenversicherungsbeitraege(
            'testdaten_update_krankenversicherungsbeitraege/Update Krankenversicherungsbeitraege.xlsx')

        # pruefen, ob die neuen Beitraege und BEitragsbemessungsgrenzen korrekt eingetragen wurden
        ergebnis = self.nutzer.abfrage_ausfuehren("SELECT * FROM gkv_beitraege")

        self.assertEqual(str(ergebnis), "[(1, 1, Decimal('7.300'), Decimal('7.300'), Decimal('72453.56'), "
                                        "Decimal('75683.12')), "
                                        "(2, 1, Decimal('7.400'), Decimal('7.400'), Decimal('74563.82'), "
                                        "Decimal('77234.21'))]")

        ergebnis = self.nutzer.abfrage_ausfuehren("SELECT * FROM hat_gkv_beitraege")

        self.assertEqual(str(ergebnis), "[(1, 1, 1, datetime.date(2023, 12, 15), datetime.date(2024, 12, 31)), "
                                        "(1, 2, 1, datetime.date(2025, 1, 1), datetime.date(9999, 12, 31))]")

    def test_ermaessigter_beitragssatz_existiert_nicht(self):
        """
        Test prueft, ob eine Fehlermeldung erscheint, wenn noch kein Datensatz fuer ermaessigte Beitragssaetze vorhanden
        ist, dieser dann aber sofort geupdatet werden soll
        """
        with self.assertRaises(Exception) as context:
            self.nutzer.update_krankenversicherungsbeitraege(
                'testdaten_update_krankenversicherungsbeitraege/Update Krankenversicherungsbeitraege - '
                'ermaessigter Beitragssatz nicht vorhanden.xlsx')

        erwartete_fehlermeldung = "FEHLER:  Ermaessigter Beitragssatz = 't' ist nicht angelegt!"
        tatsaechliche_fehlermeldung = str(context.exception)
        self.assertTrue(tatsaechliche_fehlermeldung.startswith(erwartete_fehlermeldung))

    def test_datumbis_kleiner_datumvon(self):
        """
        Test pruft, ob eine Fehlermeldung ausgegeben wird, wenn beim alten Eintrag das "Datum_Bis" vor dem "Datum_Von"
        liegt. Da dies unlogisch ist, muss diese Eintragung verhindert werden.
        """
        with self.assertRaises(Exception) as context:
            self.nutzer.update_krankenversicherungsbeitraege(
                'testdaten_update_krankenversicherungsbeitraege/Update Krankenversicherungsbeitraege - '
                'datum_bis vor datum_von.xlsx')

        erwartete_fehlermeldung = "FEHLER:  Startdatum '2023-12-15' des alten Eintrags liegt vor " \
                                  "letztgueltiger Tag '2019-12-31'. Das ist unlogisch!"
        tatsaechliche_fehlermeldung = str(context.exception)
        self.assertTrue(tatsaechliche_fehlermeldung.startswith(erwartete_fehlermeldung))

    def tearDown(self):
        """
        Methode ruft Funktion 'test_tear_down' auf, welches das Datenbankschema 'temp_test_schema' mit allen Daten
        entfernt.
        """
        test_tear_down()
