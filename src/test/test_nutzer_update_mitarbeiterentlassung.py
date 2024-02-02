import unittest

from src.main.Login import Login
from src.main.test_SetUp_TearDown import test_set_up, test_tear_down


class TestNutzerUpdateMitarbeiterentlassung(unittest.TestCase):

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
        self.nutzer.insert_unternehmen('testdaten_insert_unternehmen/Unternehmen.xlsx')
        self.nutzer.insert_austrittsgrundkategorie(
            'testdaten_insert_austrittsgrundkategorie/Austrittsgrundkategorie.xlsx')
        self.nutzer.insert_austrittsgrund('testdaten_insert_austrittsgrund/Austrittsgrund.xlsx')

        # Krankenversicherungsdaten eingeben
        self.nutzer.insert_krankenversicherungsbeitraege(
            'testdaten_insert_krankenversicherungsbeitraege/Krankenversicherungsbeitraege.xlsx')
        self.nutzer.insert_gesetzliche_krankenkasse(
            'testdaten_insert_gesetzliche_krankenkasse/gesetzliche Krankenkasse.xlsx')
        self.nutzer.insert_private_krankenkasse('testdaten_insert_privatkrankenkasse/private Krankenkasse.xlsx')
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
        self.nutzer.insert_unfallversicherungsbeitrag(
            'testdaten_insert_unfallversicherungsbeitrag/Unfallversicherungsbeitrag.xlsx')

        # Entgeltdaten eingeben
        self.nutzer.insert_gewerkschaft('testdaten_insert_gewerkschaft/Gewerkschaft.xlsx')
        self.nutzer.insert_tarif('testdaten_insert_tarif/Tarif.xlsx')
        self.nutzer.insert_verguetungsbestandteil('testdaten_insert_verguetungsbestandteil/Verguetungsbestandteil.xlsx')
        self.nutzer.insert_tarifliches_verguetungsbestandteil(
            'testdaten_insert_tariflicher_verguetungsbestandteil/tariflicher Verguetungsbestandteil.xlsx')

        # Mitarbeiter einfuegen
        self.nutzer.insert_neuer_mitarbeiter('testdaten_insert_mitarbeiter/Mitarbeiter.xlsx')

    def test_erfolgreicher_eintrag(self):
        """
        Test prueft, ob Entlassungsdatum und -grund eingetragen werden
        """
        self.nutzer.update_mitarbeiterentlassung(
            'testdaten_update_mitarbeiterentlassung/Update Mitarbeiterentlassung.xlsx')

        # pruefen, ob fuer Mitarbeiter Austrittsdatum und Fremdschluessel-ID des Austrittsgrundes eingetragen sind
        ergebnis = self.nutzer.abfrage_ausfuehren("SELECT austrittsdatum, austrittsgrund_id FROM mitarbeiter")
        self.assertEqual(str(ergebnis), "[(datetime.date(2030, 12, 31), 1)]")

        # pruefen, ob in den mitarbeiterbezogenen Assoziationstabellen die 'Bis-Datum'-Angaben auf Austrittsdatum
        # umgestellt sind
        ergebnis = self.nutzer.abfrage_ausfuehren("SELECT * FROM hat_gesetzliche_rentenversicherung")
        self.assertEqual(str(ergebnis), "[(1, 1, 1, datetime.date(2024, 1, 1), datetime.date(2030, 12, 31))]")

        ergebnis = self.nutzer.abfrage_ausfuehren("SELECT * FROM hat_gesetzliche_arbeitslosenversicherung")
        self.assertEqual(str(ergebnis), "[(1, 1, 1, datetime.date(2024, 1, 1), datetime.date(2030, 12, 31))]")

        ergebnis = self.nutzer.abfrage_ausfuehren("SELECT * FROM arbeitet_in_sachsen")
        self.assertEqual(str(ergebnis), "[(1, 1, 1, datetime.date(2024, 1, 1), datetime.date(2030, 12, 31))]")

        ergebnis = self.nutzer.abfrage_ausfuehren("SELECT * FROM hat_x_kinder_unter_25")
        self.assertEqual(str(ergebnis), "[(1, 1, 1, datetime.date(2024, 1, 1), datetime.date(2030, 12, 31))]")

        ergebnis = self.nutzer.abfrage_ausfuehren("SELECT * FROM hat_gesetzliche_krankenversicherung")
        self.assertEqual(str(ergebnis), "[(1, 1, 1, datetime.date(2024, 1, 1), datetime.date(2030, 12, 31))]")

        ergebnis = self.nutzer.abfrage_ausfuehren("SELECT * FROM ist_in_gkv")
        self.assertEqual(str(ergebnis), "[(1, 1, 1, datetime.date(2024, 1, 1), datetime.date(2030, 12, 31))]")

        # muss leer sein, da gesetzlich krankenversichert. Kann also nicht privatversichert sein.
        ergebnis = self.nutzer.abfrage_ausfuehren("SELECT * FROM hat_privatkrankenkasse")
        self.assertEqual(str(ergebnis), "[]")

        # muss leer sein, da gesetzlich krankenversichert, kann also nicht ueber einen anderen Arbeitgeber oder
        # freiwillig versichert sein
        ergebnis = self.nutzer.abfrage_ausfuehren("SELECT * FROM ist_anderweitig_versichert")
        self.assertEqual(str(ergebnis), "[]")

        # muss leer sein, da gesetzlich krankenversichert, kann also kein Minijobber sein
        ergebnis = self.nutzer.abfrage_ausfuehren("SELECT * FROM ist_minijobber")
        self.assertEqual(str(ergebnis), "[]")

        ergebnis = self.nutzer.abfrage_ausfuehren("SELECT * FROM in_unternehmen")
        self.assertEqual(str(ergebnis), "[(1, 1, 1, datetime.date(2024, 1, 1), datetime.date(2030, 12, 31))]")

        ergebnis = self.nutzer.abfrage_ausfuehren("SELECT * FROM ist_mitarbeitertyp")
        self.assertEqual(str(ergebnis), "[(1, 1, 1, datetime.date(2024, 1, 1), datetime.date(2030, 12, 31))]")

        ergebnis = self.nutzer.abfrage_ausfuehren("SELECT * FROM hat_geschlecht")
        self.assertEqual(str(ergebnis), "[(1, 1, 1, datetime.date(2024, 1, 1), datetime.date(2030, 12, 31))]")

        ergebnis = self.nutzer.abfrage_ausfuehren("SELECT * FROM wohnt_in")
        self.assertEqual(str(ergebnis), "[(1, 1, 1, datetime.date(2024, 1, 1), datetime.date(2030, 12, 31))]")

        ergebnis = self.nutzer.abfrage_ausfuehren("SELECT * FROM hat_tarif")
        self.assertEqual(str(ergebnis), "[(1, 1, 1, datetime.date(2024, 1, 1), datetime.date(2030, 12, 31))]")

        # muss leer sein, da tariflich angestellt. Kann also nicht aussertariflich sein
        ergebnis = self.nutzer.abfrage_ausfuehren("SELECT * FROM aussertarifliche")
        self.assertEqual(str(ergebnis), "[]")

        ergebnis = self.nutzer.abfrage_ausfuehren("SELECT * FROM hat_jobtitel")
        self.assertEqual(str(ergebnis), "[(1, 1, 1, 1, datetime.date(2024, 1, 1), datetime.date(2030, 12, 31))]")

        ergebnis = self.nutzer.abfrage_ausfuehren("SELECT * FROM eingesetzt_in")
        self.assertEqual(str(ergebnis), "[(1, 1, 1, False, datetime.date(2024, 1, 1), datetime.date(2030, 12, 31))]")

        ergebnis = self.nutzer.abfrage_ausfuehren("SELECT * FROM arbeitet_x_wochenstunden")
        self.assertEqual(str(ergebnis), "[(1, 1, 1, datetime.date(2024, 1, 1), datetime.date(2030, 12, 31))]")

        ergebnis = self.nutzer.abfrage_ausfuehren("SELECT * FROM in_steuerklasse")
        self.assertEqual(str(ergebnis), "[(1, 1, 1, datetime.date(2024, 1, 1), datetime.date(2030, 12, 31))]")

    def test_mitarbeiter_existiert_nicht(self):
        """
        Test prueft, ob eine Exception geworfen wird, wenn der Mitarbeiter-Update fuer eine Personalnummer vorgenommen
        wird, die in der Datenbank nicht existiert
        """
        with self.assertRaises(Exception) as context:
            self.nutzer.update_mitarbeiterentlassung(
                'testdaten_update_mitarbeiterentlassung/Update Mitarbeiterentlassung - Mitarbeiter existiert nicht.xlsx')

        erwartete_fehlermeldung = "FEHLER:  Mitarbeiter 'M100003' existiert nicht!"
        tatsaechliche_fehlermeldung = str(context.exception)
        self.assertTrue(tatsaechliche_fehlermeldung.startswith(erwartete_fehlermeldung))

    def test_austrittsdatum_vor_eintrittsdatum(self):
        """
        Test pruft, ob eine Fehlermeldung ausgegeben wird, wenn durch einen fehlerhaften Eintrag das Austrittsdatum vor
        dem Eintrittsdatum liegt
        """
        with self.assertRaises(Exception) as context:
            self.nutzer.update_mitarbeiterentlassung(
                'testdaten_update_mitarbeiterentlassung/'
                'Update Mitarbeiterentlassung - Austrittsdatum vor Eintrittsdatum.xlsx')

        erwartete_fehlermeldung = "FEHLER:  Austrittsdatum '2010-12-31' liegt vor Eintrittsdatum '2024-01-01'. " \
                                  "Das ist unlogisch!\n"
        tatsaechliche_fehlermeldung = str(context.exception)
        self.assertTrue(tatsaechliche_fehlermeldung.startswith(erwartete_fehlermeldung))

    def test_austrittsgrund_existiert_nicht(self):
        """
        Test pruft, ob eine Fehlermeldung ausgegeben wird, wenn ein Austrittsgrund angegeben wird, der in der
        Datenbank nicht hinterlegt ist.
        """
        with self.assertRaises(Exception) as context:
            self.nutzer.update_mitarbeiterentlassung(
                'testdaten_update_mitarbeiterentlassung/'
                'Update Mitarbeiterentlassung - Austrittsgrund existiert nicht.xlsx')

        erwartete_fehlermeldung = "FEHLER:  Austrittsgrund 'Insolvenz' ist nicht in Datenbank vorhanden. " \
                                  "Bitte erst anlegen!"
        tatsaechliche_fehlermeldung = str(context.exception)
        self.assertTrue(tatsaechliche_fehlermeldung.startswith(erwartete_fehlermeldung))

    def test_austrittsgrund_klein_geschrieben(self):
        """
        Test pruft, ob Eintrag durchgefuehrt wird, wenn Austrittsgrund und Personalnummer klein aber ansonsten korrekt
        geschrieben ist. Beispiel: "umsatzrueckgang" statt wie in Tabelle "Austrittsgruende" geschrieben
        "Umsatzrueckgang" oder "m100002" statt "M100002" als Personalnummer.
        """
        self.nutzer.update_mitarbeiterentlassung(
            'testdaten_update_mitarbeiterentlassung/Update Mitarbeiterentlassung - Austrittsgrund und Personalnummer '
            'klein geschrieben.xlsx')

        # pruefen, ob fuer Mitarbeiter Austrittsdatum und Fremdschluessel-ID des Austrittsgrundes eingetragen sind
        ergebnis = self.nutzer.abfrage_ausfuehren("SELECT austrittsdatum, austrittsgrund_id FROM mitarbeiter")
        self.assertEqual(str(ergebnis), "[(datetime.date(2030, 12, 31), 1)]")

        # pruefen, ob in den mitarbeiterbezogenen Assoziationstabellen die 'Bis-Datum'-Angaben auf Austrittsdatum
        # umgestellt sind
        ergebnis = self.nutzer.abfrage_ausfuehren("SELECT * FROM hat_gesetzliche_rentenversicherung")
        self.assertEqual(str(ergebnis), "[(1, 1, 1, datetime.date(2024, 1, 1), datetime.date(2030, 12, 31))]")

        ergebnis = self.nutzer.abfrage_ausfuehren("SELECT * FROM hat_gesetzliche_arbeitslosenversicherung")
        self.assertEqual(str(ergebnis), "[(1, 1, 1, datetime.date(2024, 1, 1), datetime.date(2030, 12, 31))]")

        ergebnis = self.nutzer.abfrage_ausfuehren("SELECT * FROM arbeitet_in_sachsen")
        self.assertEqual(str(ergebnis), "[(1, 1, 1, datetime.date(2024, 1, 1), datetime.date(2030, 12, 31))]")

        ergebnis = self.nutzer.abfrage_ausfuehren("SELECT * FROM hat_x_kinder_unter_25")
        self.assertEqual(str(ergebnis), "[(1, 1, 1, datetime.date(2024, 1, 1), datetime.date(2030, 12, 31))]")

        ergebnis = self.nutzer.abfrage_ausfuehren("SELECT * FROM hat_gesetzliche_krankenversicherung")
        self.assertEqual(str(ergebnis), "[(1, 1, 1, datetime.date(2024, 1, 1), datetime.date(2030, 12, 31))]")

        ergebnis = self.nutzer.abfrage_ausfuehren("SELECT * FROM ist_in_gkv")
        self.assertEqual(str(ergebnis), "[(1, 1, 1, datetime.date(2024, 1, 1), datetime.date(2030, 12, 31))]")

        # muss leer sein, da gesetzlich krankenversichert. Kann also nicht privatversichert sein.
        ergebnis = self.nutzer.abfrage_ausfuehren("SELECT * FROM hat_privatkrankenkasse")
        self.assertEqual(str(ergebnis), "[]")

        # muss leer sein, da gesetzlich krankenversichert, kann also nicht ueber einen anderen Arbeitgeber oder
        # freiwillig versichert sein
        ergebnis = self.nutzer.abfrage_ausfuehren("SELECT * FROM ist_anderweitig_versichert")
        self.assertEqual(str(ergebnis), "[]")

        # muss leer sein, da gesetzlich krankenversichert, kann also kein Minijobber sein
        ergebnis = self.nutzer.abfrage_ausfuehren("SELECT * FROM ist_minijobber")
        self.assertEqual(str(ergebnis), "[]")

        ergebnis = self.nutzer.abfrage_ausfuehren("SELECT * FROM in_unternehmen")
        self.assertEqual(str(ergebnis), "[(1, 1, 1, datetime.date(2024, 1, 1), datetime.date(2030, 12, 31))]")

        ergebnis = self.nutzer.abfrage_ausfuehren("SELECT * FROM ist_mitarbeitertyp")
        self.assertEqual(str(ergebnis), "[(1, 1, 1, datetime.date(2024, 1, 1), datetime.date(2030, 12, 31))]")

        ergebnis = self.nutzer.abfrage_ausfuehren("SELECT * FROM hat_geschlecht")
        self.assertEqual(str(ergebnis), "[(1, 1, 1, datetime.date(2024, 1, 1), datetime.date(2030, 12, 31))]")

        ergebnis = self.nutzer.abfrage_ausfuehren("SELECT * FROM wohnt_in")
        self.assertEqual(str(ergebnis), "[(1, 1, 1, datetime.date(2024, 1, 1), datetime.date(2030, 12, 31))]")

        ergebnis = self.nutzer.abfrage_ausfuehren("SELECT * FROM hat_tarif")
        self.assertEqual(str(ergebnis), "[(1, 1, 1, datetime.date(2024, 1, 1), datetime.date(2030, 12, 31))]")

        # muss leer sein, da tariflich angestellt. Kann also nicht aussertariflich sein
        ergebnis = self.nutzer.abfrage_ausfuehren("SELECT * FROM aussertarifliche")
        self.assertEqual(str(ergebnis), "[]")

        ergebnis = self.nutzer.abfrage_ausfuehren("SELECT * FROM hat_jobtitel")
        self.assertEqual(str(ergebnis), "[(1, 1, 1, 1, datetime.date(2024, 1, 1), datetime.date(2030, 12, 31))]")

        ergebnis = self.nutzer.abfrage_ausfuehren("SELECT * FROM eingesetzt_in")
        self.assertEqual(str(ergebnis), "[(1, 1, 1, False, datetime.date(2024, 1, 1), datetime.date(2030, 12, 31))]")

        ergebnis = self.nutzer.abfrage_ausfuehren("SELECT * FROM arbeitet_x_wochenstunden")
        self.assertEqual(str(ergebnis), "[(1, 1, 1, datetime.date(2024, 1, 1), datetime.date(2030, 12, 31))]")

        ergebnis = self.nutzer.abfrage_ausfuehren("SELECT * FROM in_steuerklasse")
        self.assertEqual(str(ergebnis), "[(1, 1, 1, datetime.date(2024, 1, 1), datetime.date(2030, 12, 31))]")

    def tearDown(self):
        """
        Methode ruft Funktion 'test_tear_down' auf, welches das Datenbankschema 'temp_test_schema' mit allen Daten
        entfernt.
        """
        test_tear_down()
