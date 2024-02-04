import unittest

from src.main.Login import Login
from src.test.test_SetUp_TearDown import test_set_up, test_tear_down


class TestRLS(unittest.TestCase):

    def setUp(self):
        """
        Methode ruft Funktion 'test_set_up' der Klasse 'test_SetUp_TearDown' (siehe Ordner 'main') auf, welches das
        Datenbankschema 'temp_test_schema' erstellt.
        """
        self.testschema = test_set_up()

        # ersten Mandanten + deren Admin und einen Nutzer erstellen
        login = Login(self.testschema)
        login.registriere_mandant_und_admin('Testfirma', 'mandantenpw', 'mandantenpw', 'M100000', 'Otto',
                                            'Normalverbraucher', 'adminpw', 'adminpw')
        self.admin = login.login_admin('Testfirma', 'mandantenpw', 'M100000', 'adminpw')
        self.admin.nutzer_anlegen('M100001', 'Erika', 'Musterfrau', 'nutzerpw', 'nutzerpw')

        self.nutzer = login.login_nutzer('Testfirma', 'mandantenpw', 'M100001', 'nutzerpw')
        self.nutzer.passwort_aendern('neues passwort', 'neues passwort')

        # zweiten Mandanten + deren Admin und einen Nutzer erstellen
        login = Login(self.testschema)
        login.registriere_mandant_und_admin('Testbetrieb', 'mpw', 'mpw', 'M1', 'Max', 'Mustermann',
                                            'apw', 'apw')
        self.admin2 = login.login_admin('Testbetrieb', 'mpw', 'M1', 'apw')
        self.admin2.nutzer_anlegen('M2', 'Max', 'Mustermann', 'npw', 'npw')

        self.nutzer2 = login.login_nutzer('Testbetrieb', 'mpw', 'M2', 'npw')
        self.nutzer2.passwort_aendern('neues_pw', 'neues_pw')

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

        # verschiedene Mitarbeiter anlegen, um alle SV-Formen abzudecken (der Privaat Versicherte Mitarbeiter ist
        # zusaetzlich noch aussertariflich angestellt, um auch das abzudecken)
        self.nutzer.insert_neuer_mitarbeiter('testdaten_delete_Mandantendaten/Mitarbeiter - gesetzlich versichert.xlsx')

        self.nutzer.insert_neuer_mitarbeiter('testdaten_delete_Mandantendaten/Mitarbeiter - privat versichert.xlsx')

        self.nutzer.insert_aussertarifliches_verguetungsbestandteil(
            'testdaten_delete_Mandantendaten/aussertariflicher Verguetungsbestandteil.xlsx')

        self.nutzer.insert_neuer_mitarbeiter(
            'testdaten_delete_Mandantendaten/Mitarbeiter - anderweitig versichert.xlsx')

        self.nutzer.insert_neuer_mitarbeiter('testdaten_delete_Mandantendaten/Mitarbeiter - Minijobber.xlsx')

    def test_fremder_mandant_kann_nicht_auf_daten_zugreifen(self):
        """
        Test prueft, ob Mandant 'prueffirma' keinen Zugang zu den Daten des Mandanten 'testfirma' hat. Keinesfalls
        darf 'prueffirma' diese Daten einsehen koennen.
        """

        # Alle Tabellen abfragen und pruefen, ob Datensaetze in allen Tabellen vorhanden sind
        ergebnis = self.nutzer.abfrage_ausfuehren("SELECT * FROM mandanten")
        self.assertEqual(str(ergebnis), "[(1, 'Testfirma', 'mandantenpw')]")

        ergebnis = self.nutzer.abfrage_ausfuehren("SELECT * FROM nutzer")
        self.assertEqual(str(ergebnis), "[(1, 1, 'M100001', 'Erika', 'Musterfrau', 'neues passwort', 0)]")

        ergebnis = self.nutzer.abfrage_ausfuehren("SELECT * FROM administratoren")
        self.assertEqual(str(ergebnis), "[(1, 1, 'M100000', 'Otto', 'Normalverbraucher', 'adminpw', 0)]")

        ergebnis = self.nutzer.abfrage_ausfuehren("SELECT count(*) FROM mitarbeiter")
        self.assertEqual(str(ergebnis), "[(4,)]")

        ergebnis = self.nutzer.abfrage_ausfuehren("SELECT count(*) FROM hat_gesetzliche_Rentenversicherung")
        self.assertEqual(str(ergebnis), "[(2,)]")

        ergebnis = self.nutzer.abfrage_ausfuehren("SELECT count(*) FROM rentenversicherungen")
        self.assertEqual(str(ergebnis), "[(1,)]")

        ergebnis = self.nutzer.abfrage_ausfuehren("SELECT count(*) FROM hat_rv_beitraege")
        self.assertEqual(str(ergebnis), "[(1,)]")

        ergebnis = self.nutzer.abfrage_ausfuehren("SELECT count(*) FROM rentenversicherungsbeitraege")
        self.assertEqual(str(ergebnis), "[(1,)]")

        ergebnis = self.nutzer.abfrage_ausfuehren("SELECT count(*) FROM hat_gesetzliche_arbeitslosenversicherung")
        self.assertEqual(str(ergebnis), "[(2,)]")

        ergebnis = self.nutzer.abfrage_ausfuehren("SELECT count(*) FROM arbeitslosenversicherungen")
        self.assertEqual(str(ergebnis), "[(1,)]")

        ergebnis = self.nutzer.abfrage_ausfuehren("SELECT count(*) FROM hat_av_beitraege")
        self.assertEqual(str(ergebnis), "[(1,)]")

        ergebnis = self.nutzer.abfrage_ausfuehren("SELECT count(*) FROM arbeitslosenversicherungsbeitraege")
        self.assertEqual(str(ergebnis), "[(1,)]")

        ergebnis = self.nutzer.abfrage_ausfuehren("SELECT count(*) FROM arbeitet_in_sachsen")
        self.assertEqual(str(ergebnis), "[(1,)]")

        ergebnis = self.nutzer.abfrage_ausfuehren("SELECT count(*) FROM arbeitsort_sachsen")
        self.assertEqual(str(ergebnis), "[(1,)]")

        ergebnis = self.nutzer.abfrage_ausfuehren("SELECT count(*) FROM hat_gesetzlichen_ag_pv_beitragssatz")
        self.assertEqual(str(ergebnis), "[(1,)]")

        ergebnis = self.nutzer.abfrage_ausfuehren("SELECT count(*) FROM ag_pflegeversicherungsbeitraege_gesetzlich")
        self.assertEqual(str(ergebnis), "[(1,)]")

        ergebnis = self.nutzer.abfrage_ausfuehren("SELECT count(*) FROM hat_x_kinder_unter_25")
        self.assertEqual(str(ergebnis), "[(1,)]")

        ergebnis = self.nutzer.abfrage_ausfuehren("SELECT count(*) FROM anzahl_kinder_unter_25")
        self.assertEqual(str(ergebnis), "[(1,)]")

        ergebnis = self.nutzer.abfrage_ausfuehren("SELECT count(*) FROM hat_gesetzlichen_an_pv_beitragssatz")
        self.assertEqual(str(ergebnis), "[(1,)]")

        ergebnis = self.nutzer.abfrage_ausfuehren("SELECT count(*) FROM an_pflegeversicherungsbeitraege_gesetzlich")
        self.assertEqual(str(ergebnis), "[(1,)]")

        ergebnis = self.nutzer.abfrage_ausfuehren("SELECT count(*) FROM hat_gesetzliche_krankenversicherung")
        self.assertEqual(str(ergebnis), "[(1,)]")

        ergebnis = self.nutzer.abfrage_ausfuehren("SELECT count(*) FROM krankenversicherungen")
        self.assertEqual(str(ergebnis), "[(1,)]")

        ergebnis = self.nutzer.abfrage_ausfuehren("SELECT count(*) FROM hat_gkv_beitraege")
        self.assertEqual(str(ergebnis), "[(1,)]")

        ergebnis = self.nutzer.abfrage_ausfuehren("SELECT count(*) FROM gkv_beitraege")
        self.assertEqual(str(ergebnis), "[(1,)]")

        ergebnis = self.nutzer.abfrage_ausfuehren("SELECT count(*) FROM ist_in_gkv")
        self.assertEqual(str(ergebnis), "[(1,)]")

        ergebnis = self.nutzer.abfrage_ausfuehren("SELECT count(*) FROM gesetzliche_krankenkassen")
        self.assertEqual(str(ergebnis), "[(1,)]")

        ergebnis = self.nutzer.abfrage_ausfuehren("SELECT count(*) FROM hat_gkv_zusatzbeitrag")
        self.assertEqual(str(ergebnis), "[(1,)]")

        ergebnis = self.nutzer.abfrage_ausfuehren("SELECT count(*) FROM gkv_zusatzbeitraege")
        self.assertEqual(str(ergebnis), "[(1,)]")

        ergebnis = self.nutzer.abfrage_ausfuehren("SELECT count(*) FROM hat_privatkrankenkasse")
        self.assertEqual(str(ergebnis), "[(1,)]")

        ergebnis = self.nutzer.abfrage_ausfuehren("SELECT count(*) FROM privatkrankenkassen")
        self.assertEqual(str(ergebnis), "[(1,)]")

        ergebnis = self.nutzer.abfrage_ausfuehren("SELECT count(*) FROM ist_anderweitig_versichert")
        self.assertEqual(str(ergebnis), "[(1,)]")

        ergebnis = self.nutzer.abfrage_ausfuehren("SELECT count(*) FROM gemeldete_krankenkassen")
        self.assertEqual(str(ergebnis), "[(1,)]")

        ergebnis = self.nutzer.abfrage_ausfuehren("SELECT count(*) FROM hat_umlagen_gesetzlich")
        self.assertEqual(str(ergebnis), "[(1,)]")

        ergebnis = self.nutzer.abfrage_ausfuehren("SELECT count(*) FROM hat_umlagen_privat")
        self.assertEqual(str(ergebnis), "[(1,)]")

        ergebnis = self.nutzer.abfrage_ausfuehren("SELECT count(*) FROM hat_umlagen_anderweitig")
        self.assertEqual(str(ergebnis), "[(1,)]")

        ergebnis = self.nutzer.abfrage_ausfuehren("SELECT count(*) FROM umlagen")
        self.assertEqual(str(ergebnis), "[(3,)]")

        ergebnis = self.nutzer.abfrage_ausfuehren("SELECT count(*) FROM ist_minijobber")
        self.assertEqual(str(ergebnis), "[(1,)]")

        ergebnis = self.nutzer.abfrage_ausfuehren("SELECT count(*) FROM minijobs")
        self.assertEqual(str(ergebnis), "[(1,)]")

        ergebnis = self.nutzer.abfrage_ausfuehren("SELECT count(*) FROM hat_pauschalabgaben")
        self.assertEqual(str(ergebnis), "[(1,)]")

        ergebnis = self.nutzer.abfrage_ausfuehren("SELECT count(*) FROM pauschalabgaben")
        self.assertEqual(str(ergebnis), "[(1,)]")

        ergebnis = self.nutzer.abfrage_ausfuehren("SELECT count(*) FROM in_unternehmen")
        self.assertEqual(str(ergebnis), "[(4,)]")

        ergebnis = self.nutzer.abfrage_ausfuehren("SELECT count(*) FROM unternehmen")
        self.assertEqual(str(ergebnis), "[(1,)]")

        ergebnis = self.nutzer.abfrage_ausfuehren("SELECT count(*) FROM unfallversicherungsbeitraege")
        self.assertEqual(str(ergebnis), "[(1,)]")

        ergebnis = self.nutzer.abfrage_ausfuehren("SELECT count(*) FROM berufsgenossenschaften")
        self.assertEqual(str(ergebnis), "[(1,)]")

        ergebnis = self.nutzer.abfrage_ausfuehren("SELECT count(*) FROM ist_mitarbeitertyp")
        self.assertEqual(str(ergebnis), "[(4,)]")

        ergebnis = self.nutzer.abfrage_ausfuehren("SELECT count(*) FROM mitarbeitertypen")
        self.assertEqual(str(ergebnis), "[(1,)]")

        ergebnis = self.nutzer.abfrage_ausfuehren("SELECT count(*) FROM hat_geschlecht")
        self.assertEqual(str(ergebnis), "[(4,)]")

        ergebnis = self.nutzer.abfrage_ausfuehren("SELECT count(*) FROM geschlechter")
        self.assertEqual(str(ergebnis), "[(1,)]")

        ergebnis = self.nutzer.abfrage_ausfuehren("SELECT count(*) FROM wohnt_in")
        self.assertEqual(str(ergebnis), "[(4,)]")

        ergebnis = self.nutzer.abfrage_ausfuehren("SELECT count(*) FROM strassenbezeichnungen")
        self.assertEqual(str(ergebnis), "[(1,)]")

        ergebnis = self.nutzer.abfrage_ausfuehren("SELECT count(*) FROM postleitzahlen")
        self.assertEqual(str(ergebnis), "[(1,)]")

        ergebnis = self.nutzer.abfrage_ausfuehren("SELECT count(*) FROM staedte")
        self.assertEqual(str(ergebnis), "[(1,)]")

        ergebnis = self.nutzer.abfrage_ausfuehren("SELECT count(*) FROM regionen")
        self.assertEqual(str(ergebnis), "[(1,)]")

        ergebnis = self.nutzer.abfrage_ausfuehren("SELECT count(*) FROM laender")
        self.assertEqual(str(ergebnis), "[(1,)]")

        ergebnis = self.nutzer.abfrage_ausfuehren("SELECT count(*) FROM hat_tarif")
        self.assertEqual(str(ergebnis), "[(3,)]")

        ergebnis = self.nutzer.abfrage_ausfuehren("SELECT count(*) FROM tarife")
        self.assertEqual(str(ergebnis), "[(1,)]")

        ergebnis = self.nutzer.abfrage_ausfuehren("SELECT count(*) FROM gewerkschaften")
        self.assertEqual(str(ergebnis), "[(1,)]")

        ergebnis = self.nutzer.abfrage_ausfuehren("SELECT count(*) FROM hat_verguetungsbestandteil_tarif")
        self.assertEqual(str(ergebnis), "[(1,)]")

        ergebnis = self.nutzer.abfrage_ausfuehren("SELECT count(*) FROM aussertarifliche")
        self.assertEqual(str(ergebnis), "[(1,)]")

        ergebnis = self.nutzer.abfrage_ausfuehren("SELECT count(*) FROM hat_verguetungsbestandteil_at")
        self.assertEqual(str(ergebnis), "[(1,)]")

        ergebnis = self.nutzer.abfrage_ausfuehren("SELECT count(*) FROM verguetungsbestandteile")
        self.assertEqual(str(ergebnis), "[(1,)]")

        ergebnis = self.nutzer.abfrage_ausfuehren("SELECT count(*) FROM austrittsgruende")
        self.assertEqual(str(ergebnis), "[(1,)]")

        ergebnis = self.nutzer.abfrage_ausfuehren("SELECT count(*) FROM kategorien_austrittsgruende")
        self.assertEqual(str(ergebnis), "[(1,)]")

        ergebnis = self.nutzer.abfrage_ausfuehren("SELECT count(*) FROM hat_jobtitel")
        self.assertEqual(str(ergebnis), "[(4,)]")

        ergebnis = self.nutzer.abfrage_ausfuehren("SELECT count(*) FROM jobtitel")
        self.assertEqual(str(ergebnis), "[(1,)]")

        ergebnis = self.nutzer.abfrage_ausfuehren("SELECT count(*) FROM erfahrungsstufen")
        self.assertEqual(str(ergebnis), "[(1,)]")

        ergebnis = self.nutzer.abfrage_ausfuehren("SELECT count(*) FROM eingesetzt_in")
        self.assertEqual(str(ergebnis), "[(4,)]")

        ergebnis = self.nutzer.abfrage_ausfuehren("SELECT count(*) FROM abteilungen")
        self.assertEqual(str(ergebnis), "[(1,)]")

        ergebnis = self.nutzer.abfrage_ausfuehren("SELECT count(*) FROM arbeitet_x_wochenstunden")
        self.assertEqual(str(ergebnis), "[(4,)]")

        ergebnis = self.nutzer.abfrage_ausfuehren("SELECT count(*) FROM wochenarbeitsstunden")
        self.assertEqual(str(ergebnis), "[(1,)]")

        ergebnis = self.nutzer.abfrage_ausfuehren("SELECT count(*) FROM in_steuerklasse")
        self.assertEqual(str(ergebnis), "[(4,)]")

        ergebnis = self.nutzer.abfrage_ausfuehren("SELECT count(*) FROM steuerklassen")
        self.assertEqual(str(ergebnis), "[(1,)]")

        # Nutzer eines anderen Mandanten ruft nun die Tabellen ab. Es darf nichts zu sehen sein.
        ergebnis = self.nutzer2.abfrage_ausfuehren("SELECT count(*) FROM mitarbeiter")
        self.assertEqual(str(ergebnis), "[(0,)]")

        ergebnis = self.nutzer2.abfrage_ausfuehren("SELECT count(*) FROM hat_gesetzliche_Rentenversicherung")
        self.assertEqual(str(ergebnis), "[(0,)]")

        ergebnis = self.nutzer2.abfrage_ausfuehren("SELECT count(*) FROM rentenversicherungen")
        self.assertEqual(str(ergebnis), "[(0,)]")

        ergebnis = self.nutzer2.abfrage_ausfuehren("SELECT count(*) FROM hat_rv_beitraege")
        self.assertEqual(str(ergebnis), "[(0,)]")

        ergebnis = self.nutzer2.abfrage_ausfuehren("SELECT count(*) FROM rentenversicherungsbeitraege")
        self.assertEqual(str(ergebnis), "[(0,)]")

        ergebnis = self.nutzer2.abfrage_ausfuehren("SELECT count(*) FROM hat_gesetzliche_arbeitslosenversicherung")
        self.assertEqual(str(ergebnis), "[(0,)]")

        ergebnis = self.nutzer2.abfrage_ausfuehren("SELECT count(*) FROM arbeitslosenversicherungen")
        self.assertEqual(str(ergebnis), "[(0,)]")

        ergebnis = self.nutzer2.abfrage_ausfuehren("SELECT count(*) FROM hat_av_beitraege")
        self.assertEqual(str(ergebnis), "[(0,)]")

        ergebnis = self.nutzer2.abfrage_ausfuehren("SELECT count(*) FROM arbeitslosenversicherungsbeitraege")
        self.assertEqual(str(ergebnis), "[(0,)]")

        ergebnis = self.nutzer2.abfrage_ausfuehren("SELECT count(*) FROM arbeitet_in_sachsen")
        self.assertEqual(str(ergebnis), "[(0,)]")

        ergebnis = self.nutzer2.abfrage_ausfuehren("SELECT count(*) FROM arbeitsort_sachsen")
        self.assertEqual(str(ergebnis), "[(0,)]")

        ergebnis = self.nutzer2.abfrage_ausfuehren("SELECT count(*) FROM hat_gesetzlichen_ag_pv_beitragssatz")
        self.assertEqual(str(ergebnis), "[(0,)]")

        ergebnis = self.nutzer2.abfrage_ausfuehren("SELECT count(*) FROM ag_pflegeversicherungsbeitraege_gesetzlich")
        self.assertEqual(str(ergebnis), "[(0,)]")

        ergebnis = self.nutzer2.abfrage_ausfuehren("SELECT count(*) FROM hat_x_kinder_unter_25")
        self.assertEqual(str(ergebnis), "[(0,)]")

        ergebnis = self.nutzer2.abfrage_ausfuehren("SELECT count(*) FROM anzahl_kinder_unter_25")
        self.assertEqual(str(ergebnis), "[(0,)]")

        ergebnis = self.nutzer2.abfrage_ausfuehren("SELECT count(*) FROM hat_gesetzlichen_an_pv_beitragssatz")
        self.assertEqual(str(ergebnis), "[(0,)]")

        ergebnis = self.nutzer2.abfrage_ausfuehren("SELECT count(*) FROM an_pflegeversicherungsbeitraege_gesetzlich")
        self.assertEqual(str(ergebnis), "[(0,)]")

        ergebnis = self.nutzer2.abfrage_ausfuehren("SELECT count(*) FROM hat_gesetzliche_krankenversicherung")
        self.assertEqual(str(ergebnis), "[(0,)]")

        ergebnis = self.nutzer2.abfrage_ausfuehren("SELECT count(*) FROM krankenversicherungen")
        self.assertEqual(str(ergebnis), "[(0,)]")

        ergebnis = self.nutzer2.abfrage_ausfuehren("SELECT count(*) FROM hat_gkv_beitraege")
        self.assertEqual(str(ergebnis), "[(0,)]")

        ergebnis = self.nutzer2.abfrage_ausfuehren("SELECT count(*) FROM gkv_beitraege")
        self.assertEqual(str(ergebnis), "[(0,)]")

        ergebnis = self.nutzer2.abfrage_ausfuehren("SELECT count(*) FROM ist_in_gkv")
        self.assertEqual(str(ergebnis), "[(0,)]")

        ergebnis = self.nutzer2.abfrage_ausfuehren("SELECT count(*) FROM gesetzliche_krankenkassen")
        self.assertEqual(str(ergebnis), "[(0,)]")

        ergebnis = self.nutzer2.abfrage_ausfuehren("SELECT count(*) FROM hat_gkv_zusatzbeitrag")
        self.assertEqual(str(ergebnis), "[(0,)]")

        ergebnis = self.nutzer2.abfrage_ausfuehren("SELECT count(*) FROM gkv_zusatzbeitraege")
        self.assertEqual(str(ergebnis), "[(0,)]")

        ergebnis = self.nutzer2.abfrage_ausfuehren("SELECT count(*) FROM hat_privatkrankenkasse")
        self.assertEqual(str(ergebnis), "[(0,)]")

        ergebnis = self.nutzer2.abfrage_ausfuehren("SELECT count(*) FROM privatkrankenkassen")
        self.assertEqual(str(ergebnis), "[(0,)]")

        ergebnis = self.nutzer2.abfrage_ausfuehren("SELECT count(*) FROM ist_anderweitig_versichert")
        self.assertEqual(str(ergebnis), "[(0,)]")

        ergebnis = self.nutzer2.abfrage_ausfuehren("SELECT count(*) FROM gemeldete_krankenkassen")
        self.assertEqual(str(ergebnis), "[(0,)]")

        ergebnis = self.nutzer2.abfrage_ausfuehren("SELECT count(*) FROM hat_umlagen_gesetzlich")
        self.assertEqual(str(ergebnis), "[(0,)]")

        ergebnis = self.nutzer2.abfrage_ausfuehren("SELECT count(*) FROM hat_umlagen_privat")
        self.assertEqual(str(ergebnis), "[(0,)]")

        ergebnis = self.nutzer2.abfrage_ausfuehren("SELECT count(*) FROM hat_umlagen_anderweitig")
        self.assertEqual(str(ergebnis), "[(0,)]")

        ergebnis = self.nutzer2.abfrage_ausfuehren("SELECT count(*) FROM umlagen")
        self.assertEqual(str(ergebnis), "[(0,)]")

        ergebnis = self.nutzer2.abfrage_ausfuehren("SELECT count(*) FROM ist_minijobber")
        self.assertEqual(str(ergebnis), "[(0,)]")

        ergebnis = self.nutzer2.abfrage_ausfuehren("SELECT count(*) FROM minijobs")
        self.assertEqual(str(ergebnis), "[(0,)]")

        ergebnis = self.nutzer2.abfrage_ausfuehren("SELECT count(*) FROM hat_pauschalabgaben")
        self.assertEqual(str(ergebnis), "[(0,)]")

        ergebnis = self.nutzer2.abfrage_ausfuehren("SELECT count(*) FROM pauschalabgaben")
        self.assertEqual(str(ergebnis), "[(0,)]")

        ergebnis = self.nutzer2.abfrage_ausfuehren("SELECT count(*) FROM in_unternehmen")
        self.assertEqual(str(ergebnis), "[(0,)]")

        ergebnis = self.nutzer2.abfrage_ausfuehren("SELECT count(*) FROM unternehmen")
        self.assertEqual(str(ergebnis), "[(0,)]")

        ergebnis = self.nutzer2.abfrage_ausfuehren("SELECT count(*) FROM unfallversicherungsbeitraege")
        self.assertEqual(str(ergebnis), "[(0,)]")

        ergebnis = self.nutzer2.abfrage_ausfuehren("SELECT count(*) FROM berufsgenossenschaften")
        self.assertEqual(str(ergebnis), "[(0,)]")

        ergebnis = self.nutzer2.abfrage_ausfuehren("SELECT count(*) FROM ist_mitarbeitertyp")
        self.assertEqual(str(ergebnis), "[(0,)]")

        ergebnis = self.nutzer2.abfrage_ausfuehren("SELECT count(*) FROM mitarbeitertypen")
        self.assertEqual(str(ergebnis), "[(0,)]")

        ergebnis = self.nutzer2.abfrage_ausfuehren("SELECT count(*) FROM hat_geschlecht")
        self.assertEqual(str(ergebnis), "[(0,)]")

        ergebnis = self.nutzer2.abfrage_ausfuehren("SELECT count(*) FROM geschlechter")
        self.assertEqual(str(ergebnis), "[(0,)]")

        ergebnis = self.nutzer2.abfrage_ausfuehren("SELECT count(*) FROM wohnt_in")
        self.assertEqual(str(ergebnis), "[(0,)]")

        ergebnis = self.nutzer2.abfrage_ausfuehren("SELECT count(*) FROM strassenbezeichnungen")
        self.assertEqual(str(ergebnis), "[(0,)]")

        ergebnis = self.nutzer2.abfrage_ausfuehren("SELECT count(*) FROM postleitzahlen")
        self.assertEqual(str(ergebnis), "[(0,)]")

        ergebnis = self.nutzer2.abfrage_ausfuehren("SELECT count(*) FROM staedte")
        self.assertEqual(str(ergebnis), "[(0,)]")

        ergebnis = self.nutzer2.abfrage_ausfuehren("SELECT count(*) FROM regionen")
        self.assertEqual(str(ergebnis), "[(0,)]")

        ergebnis = self.nutzer2.abfrage_ausfuehren("SELECT count(*) FROM laender")
        self.assertEqual(str(ergebnis), "[(0,)]")

        ergebnis = self.nutzer2.abfrage_ausfuehren("SELECT count(*) FROM hat_tarif")
        self.assertEqual(str(ergebnis), "[(0,)]")

        ergebnis = self.nutzer2.abfrage_ausfuehren("SELECT count(*) FROM tarife")
        self.assertEqual(str(ergebnis), "[(0,)]")

        ergebnis = self.nutzer2.abfrage_ausfuehren("SELECT count(*) FROM gewerkschaften")
        self.assertEqual(str(ergebnis), "[(0,)]")

        ergebnis = self.nutzer2.abfrage_ausfuehren("SELECT count(*) FROM hat_verguetungsbestandteil_tarif")
        self.assertEqual(str(ergebnis), "[(0,)]")

        ergebnis = self.nutzer2.abfrage_ausfuehren("SELECT count(*) FROM aussertarifliche")
        self.assertEqual(str(ergebnis), "[(0,)]")

        ergebnis = self.nutzer2.abfrage_ausfuehren("SELECT count(*) FROM hat_verguetungsbestandteil_at")
        self.assertEqual(str(ergebnis), "[(0,)]")

        ergebnis = self.nutzer2.abfrage_ausfuehren("SELECT count(*) FROM verguetungsbestandteile")
        self.assertEqual(str(ergebnis), "[(0,)]")

        ergebnis = self.nutzer2.abfrage_ausfuehren("SELECT count(*) FROM austrittsgruende")
        self.assertEqual(str(ergebnis), "[(0,)]")

        ergebnis = self.nutzer2.abfrage_ausfuehren("SELECT count(*) FROM kategorien_austrittsgruende")
        self.assertEqual(str(ergebnis), "[(0,)]")

        # In Tabelle Mandanten kann er sich selbst sehen, ...
        ergebnis = self.nutzer2.abfrage_ausfuehren("SELECT * FROM mandanten")
        self.assertEqual(str(ergebnis), "[(2, 'Testbetrieb', 'mpw')]")

        # ... seinen Nutzer ...
        ergebnis = self.nutzer2.abfrage_ausfuehren("SELECT * FROM nutzer")
        self.assertEqual(str(ergebnis), "[(2, 2, 'M2', 'Max', 'Mustermann', 'neues_pw', 0)]")

        # ... und seinen Administrator
        ergebnis = self.nutzer2.abfrage_ausfuehren("SELECT * FROM administratoren")
        self.assertEqual(str(ergebnis), "[(2, 2, 'M1', 'Max', 'Mustermann', 'apw', 0)]")

        ergebnis = self.nutzer2.abfrage_ausfuehren("SELECT count(*) FROM hat_jobtitel")
        self.assertEqual(str(ergebnis), "[(0,)]")

        ergebnis = self.nutzer2.abfrage_ausfuehren("SELECT count(*) FROM jobtitel")
        self.assertEqual(str(ergebnis), "[(0,)]")

        ergebnis = self.nutzer2.abfrage_ausfuehren("SELECT count(*) FROM erfahrungsstufen")
        self.assertEqual(str(ergebnis), "[(0,)]")

        ergebnis = self.nutzer2.abfrage_ausfuehren("SELECT count(*) FROM eingesetzt_in")
        self.assertEqual(str(ergebnis), "[(0,)]")

        ergebnis = self.nutzer2.abfrage_ausfuehren("SELECT count(*) FROM abteilungen")
        self.assertEqual(str(ergebnis), "[(0,)]")

        ergebnis = self.nutzer2.abfrage_ausfuehren("SELECT count(*) FROM arbeitet_x_wochenstunden")
        self.assertEqual(str(ergebnis), "[(0,)]")

        ergebnis = self.nutzer2.abfrage_ausfuehren("SELECT count(*) FROM wochenarbeitsstunden")
        self.assertEqual(str(ergebnis), "[(0,)]")

        ergebnis = self.nutzer2.abfrage_ausfuehren("SELECT count(*) FROM in_steuerklasse")
        self.assertEqual(str(ergebnis), "[(0,)]")

        ergebnis = self.nutzer2.abfrage_ausfuehren("SELECT count(*) FROM steuerklassen")
        self.assertEqual(str(ergebnis), "[(0,)]")

    def tearDown(self):
        """
        Methode ruft Funktion 'test_tear_down' auf, welches das Datenbankschema 'temp_test_schema' mit allen Daten
        entfernt.
        """
        test_tear_down()
