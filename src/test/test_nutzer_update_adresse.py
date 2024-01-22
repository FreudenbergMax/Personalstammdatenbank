import unittest

from src.main.Login import Login
from src.main.Mandant import Mandant
from src.main.test_SetUp_TearDown import test_set_up, test_tear_down


class TestNutzerUpdateAdresse(unittest.TestCase):

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

        # Eintragen personenbezogener Daten
        self.nutzer.insert_geschlecht('testdaten_insert_geschlecht/Geschlecht.xlsx')
        self.nutzer.insert_mitarbeitertyp('testdaten_insert_mitarbeitertyp/Mitarbeitertyp.xlsx')
        self.nutzer.insert_steuerklasse('testdaten_insert_steuerklasse/Steuerklasse.xlsx')
        self.nutzer.insert_abteilung('testdaten_insert_abteilung/Abteilung.xlsx')
        self.nutzer.insert_jobtitel('testdaten_insert_jobtitel/Jobtitel.xlsx')
        self.nutzer.insert_erfahrungsstufe('testdaten_insert_erfahrungsstufe/Erfahrungsstufe.xlsx')
        self.nutzer.insert_gesellschaft('testdaten_insert_gesellschaft/Gesellschaft.xlsx')
        self.nutzer.insert_austrittsgrundkategorie(
            'testdaten_insert_austrittsgrundkategorie/Austrittsgrundkategorie.xlsx')
        self.nutzer.insert_austrittsgrund('testdaten_insert_austrittsgrund/Austrittsgrund.xlsx')

        # Krankenversicherungsdaten eingeben
        self.nutzer.insert_krankenversicherungsbeitraege(
            'testdaten_insert_krankenversicherungsbeitraege/Krankenversicherungsbeitraege.xlsx')
        self.nutzer.insert_gesetzliche_krankenkasse(
            'testdaten_insert_gesetzliche_krankenkasse/gesetzliche Krankenkasse.xlsx')
        self.nutzer.insert_private_krankenkasse(
            'testdaten_insert_privatkrankenkasse/private Krankenkasse.xlsx')
        self.nutzer.insert_gemeldete_krankenkasse('testdaten_insert_gemeldete_krankenkasse/gemeldete Krankenkasse.xlsx')
        self.nutzer.insert_anzahl_kinder_an_pv_beitrag(
            'testdaten_insert_anzahl_kinder/Anzahl Kinder Arbeitnehmer PV-Beitrag.xlsx')
        self.nutzer.insert_arbeitsort_sachsen_ag_pv_beitrag(
            'testdaten_insert_ag_pv_beitrag_sachsen/Arbeitsort Sachsen Arbeitgeber PV-Beitrag.xlsx')
        self.nutzer.insert_arbeitslosenversicherungsbeitraege(
            'testdaten_insert_arbeitslosenversicherungsbeitraege/Arbeitslosenversicherungsbeitraege.xlsx')
        self.nutzer.insert_rentenversicherungsbeitraege(
            'testdaten_insert_rentenversicherungsbeitraege/Rentenversicherungsbeitraege.xlsx')
        self.nutzer.insert_minijobbeitraege('testdaten_insert_minijobbeitraege/Minijobbeitraege.xlsx')
        self.nutzer.insert_berufsgenossenschaft('testdaten_insert_berufsgenossenschaft/Berufsgenossenschaft.xlsx')
        self.nutzer.insert_unfallversicherungsbeitrag('testdaten_insert_unfallversicherungsbeitrag/'
                                              'Unfallversicherungsbeitrag.xlsx')

        # Entgeltdaten eingeben
        self.nutzer.insert_gewerkschaft('testdaten_insert_gewerkschaft/Gewerkschaft.xlsx')
        self.nutzer.insert_tarif('testdaten_insert_tarif/Tarif.xlsx')
        self.nutzer.insert_verguetungsbestandteil(
            'testdaten_insert_verguetungsbestandteil/Verguetungsbestandteil.xlsx')
        self.nutzer.insert_tarifliches_verguetungsbestandteil(
            'testdaten_insert_tariflicher_verguetungsbestandteil/tariflicher Verguetungsbestandteil.xlsx')

        # Mitarbeiter einfuegen
        self.nutzer.insert_neuer_mitarbeiter('testdaten_insert_mitarbeiter/Mitarbeiter.xlsx')

    def test_erfolgreicher_eintrag(self):
        """
        Test prueft, ob die Adresse eines Mitarbeiters geupdated wird.
        """
        self.nutzer.update_adresse('testdaten_update_adresse/Update Adresse.xlsx')

        # pruefen, ob neue Adressdaten eingetragen und mit Mitarbeiter verknuepft ist
        ergebnis = self.nutzer.abfrage_ausfuehren("SELECT * FROM laender")
        self.assertEqual(str(ergebnis), "[(1, 1, 'Deutschland')]")

        ergebnis = self.nutzer.abfrage_ausfuehren("SELECT * FROM regionen")
        self.assertEqual(str(ergebnis), "[(2, 1, 'Berlin', 1), (1, 1, 'Brandenburg', 1)]")

        ergebnis = self.nutzer.abfrage_ausfuehren("SELECT * FROM staedte")
        self.assertEqual(str(ergebnis), "[(2, 1, 'Berlin', 2), (1, 1, 'Bernau', 1)]")

        ergebnis = self.nutzer.abfrage_ausfuehren("SELECT * FROM postleitzahlen")
        self.assertEqual(str(ergebnis), "[(1, 1, '12358', 'Ost', 1), (2, 1, '10369', 'Ost', 2)]")

        ergebnis = self.nutzer.abfrage_ausfuehren("SELECT * FROM strassenbezeichnungen")
        self.assertEqual(str(ergebnis), "[(1, 1, 'Musterstraße', '1', 1), (2, 1, 'neue Straße', '42', 2)]")

        ergebnis = self.nutzer.abfrage_ausfuehren("SELECT * FROM wohnt_in")
        self.assertEqual(str(ergebnis), "[(1, 1, 1, datetime.date(2024, 1, 1), datetime.date(2026, 12, 31)), "
                                        "(1, 2, 1, datetime.date(2027, 1, 1), datetime.date(9999, 12, 31))]")

    def test_kein_doppelter_eintrag(self):
        """
        Test prueft, ob bei einem wiederholtem Adress-Update mit exakt denselben Daten fuer denselben Mitarbeiter
        eine exception geworfen wird. Ausloeser ist der unique-constraint der Tabelle 'wohnt_in' der verhindern soll,
        dass ein Mitarbeiter gleichzeitig zwei Wohnsitze hat.
        """
        self.nutzer.update_adresse('testdaten_update_adresse/Update Adresse.xlsx')

        # Versuch, denselben Wert noch einmal einzutragen
        with self.assertRaises(Exception) as context:
            self.nutzer.update_adresse('testdaten_update_adresse/Update Adresse.xlsx')

        erwartete_fehlermeldung = "FEHLER:  Mitarbeiter 'M100002' bereits seit diesem Datum unter der Adresse gemeldet!"
        tatsaechliche_fehlermeldung = str(context.exception)
        self.assertTrue(tatsaechliche_fehlermeldung.startswith(erwartete_fehlermeldung))

        # Inhalt aus Tabelle ziehen, um zu pruefen, ob der Datensatz nur einmal angelegt wurde
        ergebnis = self.nutzer.abfrage_ausfuehren("SELECT * FROM wohnt_in")
        self.assertEqual(str(ergebnis), "[(1, 1, 1, datetime.date(2024, 1, 1), datetime.date(2026, 12, 31)), "
                                        "(1, 2, 1, datetime.date(2027, 1, 1), datetime.date(9999, 12, 31))]")

    def test_kein_doppelter_eintrag_adresse_case_insensitive(self):
        """
        Test prueft, ob neue Eintraege fuer Land, Region, Stadt, Strasse, Hausnummer und Personalnummer in
        Kleinschreibung angelegt werden, wenn diese bereits in Grossschreibung vorhanden ist. In dem Fall soll kein
        neuer Eintrag durchgefuehrt werden.
        """
        self.nutzer.update_adresse('testdaten_update_adresse/Update Adresse - alles klein geschrieben.xlsx')

        # pruefen, ob neue Adressdaten in Kleinschriebung nicht eingetragen wurden, da bereits in Grossschreibung da
        ergebnis = self.nutzer.abfrage_ausfuehren("SELECT * FROM laender")
        self.assertEqual(str(ergebnis), "[(1, 1, 'Deutschland')]")

        ergebnis = self.nutzer.abfrage_ausfuehren("SELECT * FROM regionen")
        self.assertEqual(str(ergebnis), "[(1, 1, 'Brandenburg', 1)]")

        ergebnis = self.nutzer.abfrage_ausfuehren("SELECT * FROM staedte")
        self.assertEqual(str(ergebnis), "[(1, 1, 'Bernau', 1)]")

        ergebnis = self.nutzer.abfrage_ausfuehren("SELECT * FROM postleitzahlen")
        self.assertEqual(str(ergebnis), "[(1, 1, '12358', 'Ost', 1)]")

        ergebnis = self.nutzer.abfrage_ausfuehren("SELECT * FROM strassenbezeichnungen")
        self.assertEqual(str(ergebnis), "[(1, 1, 'Musterstraße', '1', 1)]")

        ergebnis = self.nutzer.abfrage_ausfuehren("SELECT * FROM wohnt_in")
        self.assertEqual(str(ergebnis), "[(1, 1, 1, datetime.date(2024, 1, 1), datetime.date(2026, 12, 31)), "
                                        "(1, 1, 1, datetime.date(2027, 1, 1), datetime.date(9999, 12, 31))]")

    def test_mitarbeiter_existiert_nicht(self):
        """
        Test prueft, ob eine Exception geworfen wird, wenn der Adress-Update fuer eine Person vorgenommen wird,
        die in der Datenbank nicht existiert
        """
        with self.assertRaises(Exception) as context:
            self.nutzer.update_adresse('testdaten_update_adresse/Update Adresse - Mitarbeiter existiert nicht.xlsx')

        erwartete_fehlermeldung = "FEHLER:  Mitarbeiter 'M100003' existiert nicht!"
        tatsaechliche_fehlermeldung = str(context.exception)
        self.assertTrue(tatsaechliche_fehlermeldung.startswith(erwartete_fehlermeldung))

    def tearDown(self):
        """
        Methode ruft Funktion 'test_tear_down' auf, welches das Datenbankschema 'temp_test_schema' mit allen Daten
        entfernt.
        """
        test_tear_down()
