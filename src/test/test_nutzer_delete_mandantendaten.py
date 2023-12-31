import unittest
from src.main.Mandant import Mandant
from src.main.test_SetUp_TearDown import test_set_up, test_tear_down


class TestNutzerDeleteMandantendaten(unittest.TestCase):

    def setUp(self):
        """
        Methode ruft Funktion 'test_set_up' der Klasse 'test_SetUp_TearDown' (siehe Ordner 'main') auf, welches das
        Datenbankschema 'temp_test_schema' erstellt.
        """
        self.testschema = test_set_up()
        self.testfirma = Mandant('Testfirma', self.testschema)
        self.testfirma.nutzer_anlegen('M100001', 'Erika', 'Musterfrau', self.testschema)

        # Eintragen personenbezogener Daten
        self.testfirma.get_nutzer("M100001").insert_geschlecht('testdaten_insert_geschlecht/Geschlecht.xlsx',
                                                               self.testschema)
        self.testfirma.get_nutzer("M100001").insert_mitarbeitertyp('testdaten_insert_mitarbeitertyp/'
                                                                   'Mitarbeitertyp.xlsx', self.testschema)
        self.testfirma.get_nutzer("M100001").insert_steuerklasse('testdaten_insert_steuerklasse/Steuerklasse.xlsx',
                                                                 self.testschema)
        self.testfirma.get_nutzer("M100001").insert_abteilung('testdaten_insert_abteilung/Abteilung.xlsx',
                                                              self.testschema)
        self.testfirma.get_nutzer("M100001").insert_jobtitel('testdaten_insert_jobtitel/Jobtitel.xlsx', self.testschema)
        self.testfirma.get_nutzer("M100001").insert_erfahrungsstufe('testdaten_insert_erfahrungsstufe/'
                                                                    'Erfahrungsstufe.xlsx', self.testschema)
        self.testfirma.get_nutzer("M100001").insert_gesellschaft('testdaten_insert_gesellschaft/Gesellschaft.xlsx',
                                                                 self.testschema)
        self.testfirma.get_nutzer("M100001").insert_austrittsgrundkategorie(
            'testdaten_insert_austrittsgrundkategorie/Austrittsgrundkategorie.xlsx', self.testschema)
        self.testfirma.get_nutzer("M100001").insert_austrittsgrund(
            'testdaten_insert_austrittsgrund/Austrittsgrund.xlsx', self.testschema)

        # Krankenversicherungsdaten eingeben
        self.testfirma.get_nutzer("M100001").insert_krankenversicherungsbeitraege(
            'testdaten_insert_krankenversicherungsbeitraege/Krankenversicherungsbeitraege.xlsx', self.testschema)
        self.testfirma.get_nutzer("M100001").insert_gesetzliche_krankenkasse(
            'testdaten_insert_gesetzliche_krankenkasse/gesetzliche Krankenkasse.xlsx', self.testschema)
        self.testfirma.get_nutzer("M100001"). \
            insert_private_krankenkasse('testdaten_insert_privatkrankenkasse/private Krankenkasse.xlsx',
                                        self.testschema)
        self.testfirma.get_nutzer("M100001"). \
            insert_gemeldete_krankenkasse('testdaten_insert_gemeldete_krankenkasse/gemeldete Krankenkasse.xlsx',
                                          self.testschema)
        self.testfirma.get_nutzer("M100001").insert_anzahl_kinder_an_pv_beitrag(
            'testdaten_insert_anzahl_kinder/Anzahl Kinder Arbeitnehmer PV-Beitrag.xlsx', self.testschema)
        self.testfirma.get_nutzer("M100001"). \
            insert_arbeitsort_sachsen_ag_pv_beitrag(
            'testdaten_insert_ag_pv_beitrag_sachsen/Arbeitsort Sachsen Arbeitgeber PV-Beitrag.xlsx', self.testschema)
        self.testfirma.get_nutzer("M100001"). \
            insert_arbeitslosenversicherungsbeitraege(
            'testdaten_insert_arbeitslosenversicherungsbeitraege/Arbeitslosenversicherungsbeitraege.xlsx',
            self.testschema)
        self.testfirma.get_nutzer("M100001"). \
            insert_rentenversicherungsbeitraege('testdaten_insert_rentenversicherungsbeitraege/'
                                                'Rentenversicherungsbeitraege.xlsx', self.testschema)
        self.testfirma.get_nutzer("M100001"). \
            insert_minijobbeitraege('testdaten_insert_minijobbeitraege/Minijobbeitraege.xlsx', self.testschema)
        self.testfirma.get_nutzer("M100001"). \
            insert_berufsgenossenschaft('testdaten_insert_berufsgenossenschaft/Berufsgenossenschaft.xlsx',
                                        self.testschema)
        self.testfirma.get_nutzer("M100001"). \
            insert_unfallversicherungsbeitrag('testdaten_insert_unfallversicherungsbeitrag/'
                                              'Unfallversicherungsbeitrag.xlsx', self.testschema)

        # Entgeltdaten eingeben
        self.testfirma.get_nutzer("M100001").insert_gewerkschaft('testdaten_insert_gewerkschaft/Gewerkschaft.xlsx',
                                                                 self.testschema)
        self.testfirma.get_nutzer("M100001").insert_tarif('testdaten_insert_tarif/Tarif.xlsx', self.testschema)
        self.testfirma.get_nutzer("M100001").insert_verguetungsbestandteil(
            'testdaten_insert_verguetungsbestandteil/Verguetungsbestandteil.xlsx', self.testschema)
        self.testfirma.get_nutzer("M100001").insert_tarifliches_verguetungsbestandteil(
            'testdaten_insert_tariflicher_verguetungsbestandteil/tariflicher Verguetungsbestandteil.xlsx',
            self.testschema)

        # verschiedene Mitarbeiter anlegen, um alle SV-Formen abzudecken (der Privaat Versicherte Mitarbeiter ist
        # zusaetzlich noch aussertariflich angestellt, um auch das abzudecken)
        self.testfirma.get_nutzer("M100001"). \
            insert_neuer_mitarbeiter('testdaten_delete_Mandantendaten/Mitarbeiter - gesetzlich versichert.xlsx',
                                     self.testschema)

        self.testfirma.get_nutzer("M100001"). \
            insert_neuer_mitarbeiter('testdaten_delete_Mandantendaten/Mitarbeiter - privat versichert.xlsx',
                                     self.testschema)

        self.testfirma.get_nutzer("M100001"). \
            insert_aussertarifliches_verguetungsbestandteil('testdaten_delete_Mandantendaten/'
                                                            'aussertariflicher Verguetungsbestandteil.xlsx',
                                                            self.testschema)

        self.testfirma.get_nutzer("M100001"). \
            insert_neuer_mitarbeiter('testdaten_delete_Mandantendaten/Mitarbeiter - anderweitig versichert.xlsx',
                                     self.testschema)

        self.testfirma.get_nutzer("M100001"). \
            insert_neuer_mitarbeiter('testdaten_delete_Mandantendaten/Mitarbeiter - Minijobber.xlsx',
                                     self.testschema)

    def test_erfolgreiche_entfernung_aller_mandantendaten(self):
        """
        Test prueft, ob aller Mndantendaten nach Nutzung der Methode "delete_mandantendaten" entfernt sind
        """

        # Alle Tabellen abfragen und pruefen, ob Datensaetze in allen Tabellen vorhanden sind
        ergebnis = self.testfirma.get_nutzer("M100001"). \
            abfrage_ausfuehren("SELECT count(*) FROM mitarbeiter", self.testschema)
        self.assertEqual(str(ergebnis), "[(4,)]")

        ergebnis = self.testfirma.get_nutzer("M100001"). \
            abfrage_ausfuehren("SELECT count(*) FROM hat_gesetzliche_Rentenversicherung", self.testschema)
        self.assertEqual(str(ergebnis), "[(2,)]")

        ergebnis = self.testfirma.get_nutzer("M100001"). \
            abfrage_ausfuehren("SELECT count(*) FROM rentenversicherungen", self.testschema)
        self.assertEqual(str(ergebnis), "[(1,)]")

        ergebnis = self.testfirma.get_nutzer("M100001"). \
            abfrage_ausfuehren("SELECT count(*) FROM hat_rv_beitraege", self.testschema)
        self.assertEqual(str(ergebnis), "[(1,)]")

        ergebnis = self.testfirma.get_nutzer("M100001"). \
            abfrage_ausfuehren("SELECT count(*) FROM rentenversicherungsbeitraege", self.testschema)
        self.assertEqual(str(ergebnis), "[(1,)]")

        ergebnis = self.testfirma.get_nutzer("M100001"). \
            abfrage_ausfuehren("SELECT count(*) FROM hat_gesetzliche_arbeitslosenversicherung", self.testschema)
        self.assertEqual(str(ergebnis), "[(2,)]")

        ergebnis = self.testfirma.get_nutzer("M100001"). \
            abfrage_ausfuehren("SELECT count(*) FROM arbeitslosenversicherungen", self.testschema)
        self.assertEqual(str(ergebnis), "[(1,)]")

        ergebnis = self.testfirma.get_nutzer("M100001"). \
            abfrage_ausfuehren("SELECT count(*) FROM hat_av_beitraege", self.testschema)
        self.assertEqual(str(ergebnis), "[(1,)]")

        ergebnis = self.testfirma.get_nutzer("M100001"). \
            abfrage_ausfuehren("SELECT count(*) FROM arbeitslosenversicherungsbeitraege", self.testschema)
        self.assertEqual(str(ergebnis), "[(1,)]")

        ergebnis = self.testfirma.get_nutzer("M100001"). \
            abfrage_ausfuehren("SELECT count(*) FROM arbeitet_in_sachsen", self.testschema)
        self.assertEqual(str(ergebnis), "[(1,)]")

        ergebnis = self.testfirma.get_nutzer("M100001"). \
            abfrage_ausfuehren("SELECT count(*) FROM arbeitsort_sachsen", self.testschema)
        self.assertEqual(str(ergebnis), "[(1,)]")

        ergebnis = self.testfirma.get_nutzer("M100001"). \
            abfrage_ausfuehren("SELECT count(*) FROM hat_gesetzlichen_ag_pv_beitragssatz", self.testschema)
        self.assertEqual(str(ergebnis), "[(1,)]")

        ergebnis = self.testfirma.get_nutzer("M100001"). \
            abfrage_ausfuehren("SELECT count(*) FROM ag_pflegeversicherungsbeitraege_gesetzlich", self.testschema)
        self.assertEqual(str(ergebnis), "[(1,)]")

        ergebnis = self.testfirma.get_nutzer("M100001"). \
            abfrage_ausfuehren("SELECT count(*) FROM hat_x_kinder_unter_25", self.testschema)
        self.assertEqual(str(ergebnis), "[(1,)]")

        ergebnis = self.testfirma.get_nutzer("M100001"). \
            abfrage_ausfuehren("SELECT count(*) FROM anzahl_kinder_unter_25", self.testschema)
        self.assertEqual(str(ergebnis), "[(1,)]")

        ergebnis = self.testfirma.get_nutzer("M100001"). \
            abfrage_ausfuehren("SELECT count(*) FROM hat_gesetzlichen_an_pv_beitragssatz", self.testschema)
        self.assertEqual(str(ergebnis), "[(1,)]")

        ergebnis = self.testfirma.get_nutzer("M100001"). \
            abfrage_ausfuehren("SELECT count(*) FROM an_pflegeversicherungsbeitraege_gesetzlich", self.testschema)
        self.assertEqual(str(ergebnis), "[(1,)]")

        ergebnis = self.testfirma.get_nutzer("M100001"). \
            abfrage_ausfuehren("SELECT count(*) FROM hat_gesetzliche_krankenversicherung", self.testschema)
        self.assertEqual(str(ergebnis), "[(1,)]")

        ergebnis = self.testfirma.get_nutzer("M100001"). \
            abfrage_ausfuehren("SELECT count(*) FROM krankenversicherungen", self.testschema)
        self.assertEqual(str(ergebnis), "[(1,)]")

        ergebnis = self.testfirma.get_nutzer("M100001"). \
            abfrage_ausfuehren("SELECT count(*) FROM hat_gkv_beitraege", self.testschema)
        self.assertEqual(str(ergebnis), "[(1,)]")

        ergebnis = self.testfirma.get_nutzer("M100001"). \
            abfrage_ausfuehren("SELECT count(*) FROM gkv_beitraege", self.testschema)
        self.assertEqual(str(ergebnis), "[(1,)]")

        ergebnis = self.testfirma.get_nutzer("M100001"). \
            abfrage_ausfuehren("SELECT count(*) FROM ist_in_gkv", self.testschema)
        self.assertEqual(str(ergebnis), "[(1,)]")

        ergebnis = self.testfirma.get_nutzer("M100001"). \
            abfrage_ausfuehren("SELECT count(*) FROM gesetzliche_krankenkassen", self.testschema)
        self.assertEqual(str(ergebnis), "[(1,)]")

        ergebnis = self.testfirma.get_nutzer("M100001"). \
            abfrage_ausfuehren("SELECT count(*) FROM hat_gkv_zusatzbeitrag", self.testschema)
        self.assertEqual(str(ergebnis), "[(1,)]")

        ergebnis = self.testfirma.get_nutzer("M100001"). \
            abfrage_ausfuehren("SELECT count(*) FROM gkv_zusatzbeitraege", self.testschema)
        self.assertEqual(str(ergebnis), "[(1,)]")

        ergebnis = self.testfirma.get_nutzer("M100001"). \
            abfrage_ausfuehren("SELECT count(*) FROM hat_privatkrankenkasse", self.testschema)
        self.assertEqual(str(ergebnis), "[(1,)]")

        ergebnis = self.testfirma.get_nutzer("M100001"). \
            abfrage_ausfuehren("SELECT count(*) FROM privatkrankenkassen", self.testschema)
        self.assertEqual(str(ergebnis), "[(1,)]")

        ergebnis = self.testfirma.get_nutzer("M100001"). \
            abfrage_ausfuehren("SELECT count(*) FROM ist_anderweitig_versichert", self.testschema)
        self.assertEqual(str(ergebnis), "[(1,)]")

        ergebnis = self.testfirma.get_nutzer("M100001"). \
            abfrage_ausfuehren("SELECT count(*) FROM gemeldete_krankenkassen", self.testschema)
        self.assertEqual(str(ergebnis), "[(1,)]")

        ergebnis = self.testfirma.get_nutzer("M100001"). \
            abfrage_ausfuehren("SELECT count(*) FROM hat_umlagen_gesetzlich", self.testschema)
        self.assertEqual(str(ergebnis), "[(1,)]")

        ergebnis = self.testfirma.get_nutzer("M100001"). \
            abfrage_ausfuehren("SELECT count(*) FROM hat_umlagen_privat", self.testschema)
        self.assertEqual(str(ergebnis), "[(1,)]")

        ergebnis = self.testfirma.get_nutzer("M100001"). \
            abfrage_ausfuehren("SELECT count(*) FROM hat_umlagen_anderweitig", self.testschema)
        self.assertEqual(str(ergebnis), "[(1,)]")

        ergebnis = self.testfirma.get_nutzer("M100001"). \
            abfrage_ausfuehren("SELECT count(*) FROM umlagen", self.testschema)
        self.assertEqual(str(ergebnis), "[(3,)]")

        ergebnis = self.testfirma.get_nutzer("M100001"). \
            abfrage_ausfuehren("SELECT count(*) FROM ist_minijobber", self.testschema)
        self.assertEqual(str(ergebnis), "[(1,)]")

        ergebnis = self.testfirma.get_nutzer("M100001"). \
            abfrage_ausfuehren("SELECT count(*) FROM minijobs", self.testschema)
        self.assertEqual(str(ergebnis), "[(1,)]")

        ergebnis = self.testfirma.get_nutzer("M100001"). \
            abfrage_ausfuehren("SELECT count(*) FROM hat_pauschalabgaben", self.testschema)
        self.assertEqual(str(ergebnis), "[(1,)]")

        ergebnis = self.testfirma.get_nutzer("M100001"). \
            abfrage_ausfuehren("SELECT count(*) FROM pauschalabgaben", self.testschema)
        self.assertEqual(str(ergebnis), "[(1,)]")

        ergebnis = self.testfirma.get_nutzer("M100001"). \
            abfrage_ausfuehren("SELECT count(*) FROM in_gesellschaft", self.testschema)
        self.assertEqual(str(ergebnis), "[(4,)]")

        ergebnis = self.testfirma.get_nutzer("M100001"). \
            abfrage_ausfuehren("SELECT count(*) FROM gesellschaften", self.testschema)
        self.assertEqual(str(ergebnis), "[(1,)]")

        ergebnis = self.testfirma.get_nutzer("M100001"). \
            abfrage_ausfuehren("SELECT count(*) FROM unfallversicherungsbeitraege", self.testschema)
        self.assertEqual(str(ergebnis), "[(1,)]")

        ergebnis = self.testfirma.get_nutzer("M100001"). \
            abfrage_ausfuehren("SELECT count(*) FROM berufsgenossenschaften", self.testschema)
        self.assertEqual(str(ergebnis), "[(1,)]")

        ergebnis = self.testfirma.get_nutzer("M100001"). \
            abfrage_ausfuehren("SELECT count(*) FROM ist_mitarbeitertyp", self.testschema)
        self.assertEqual(str(ergebnis), "[(4,)]")

        ergebnis = self.testfirma.get_nutzer("M100001"). \
            abfrage_ausfuehren("SELECT count(*) FROM mitarbeitertypen", self.testschema)
        self.assertEqual(str(ergebnis), "[(1,)]")

        ergebnis = self.testfirma.get_nutzer("M100001"). \
            abfrage_ausfuehren("SELECT count(*) FROM hat_geschlecht", self.testschema)
        self.assertEqual(str(ergebnis), "[(4,)]")

        ergebnis = self.testfirma.get_nutzer("M100001"). \
            abfrage_ausfuehren("SELECT count(*) FROM geschlechter", self.testschema)
        self.assertEqual(str(ergebnis), "[(1,)]")

        ergebnis = self.testfirma.get_nutzer("M100001"). \
            abfrage_ausfuehren("SELECT count(*) FROM wohnt_in", self.testschema)
        self.assertEqual(str(ergebnis), "[(4,)]")

        ergebnis = self.testfirma.get_nutzer("M100001"). \
            abfrage_ausfuehren("SELECT count(*) FROM strassenbezeichnungen", self.testschema)
        self.assertEqual(str(ergebnis), "[(1,)]")

        ergebnis = self.testfirma.get_nutzer("M100001"). \
            abfrage_ausfuehren("SELECT count(*) FROM postleitzahlen", self.testschema)
        self.assertEqual(str(ergebnis), "[(1,)]")

        ergebnis = self.testfirma.get_nutzer("M100001"). \
            abfrage_ausfuehren("SELECT count(*) FROM staedte", self.testschema)
        self.assertEqual(str(ergebnis), "[(1,)]")

        ergebnis = self.testfirma.get_nutzer("M100001"). \
            abfrage_ausfuehren("SELECT count(*) FROM regionen", self.testschema)
        self.assertEqual(str(ergebnis), "[(1,)]")

        ergebnis = self.testfirma.get_nutzer("M100001"). \
            abfrage_ausfuehren("SELECT count(*) FROM laender", self.testschema)
        self.assertEqual(str(ergebnis), "[(1,)]")

        ergebnis = self.testfirma.get_nutzer("M100001"). \
            abfrage_ausfuehren("SELECT count(*) FROM hat_tarif", self.testschema)
        self.assertEqual(str(ergebnis), "[(3,)]")

        ergebnis = self.testfirma.get_nutzer("M100001"). \
            abfrage_ausfuehren("SELECT count(*) FROM tarife", self.testschema)
        self.assertEqual(str(ergebnis), "[(1,)]")

        ergebnis = self.testfirma.get_nutzer("M100001"). \
            abfrage_ausfuehren("SELECT count(*) FROM gewerkschaften", self.testschema)
        self.assertEqual(str(ergebnis), "[(1,)]")

        ergebnis = self.testfirma.get_nutzer("M100001"). \
            abfrage_ausfuehren("SELECT count(*) FROM hat_verguetungsbestandteil_tarif", self.testschema)
        self.assertEqual(str(ergebnis), "[(1,)]")

        ergebnis = self.testfirma.get_nutzer("M100001"). \
            abfrage_ausfuehren("SELECT count(*) FROM aussertarifliche", self.testschema)
        self.assertEqual(str(ergebnis), "[(1,)]")

        ergebnis = self.testfirma.get_nutzer("M100001"). \
            abfrage_ausfuehren("SELECT count(*) FROM hat_verguetungsbestandteil_at", self.testschema)
        self.assertEqual(str(ergebnis), "[(1,)]")

        ergebnis = self.testfirma.get_nutzer("M100001"). \
            abfrage_ausfuehren("SELECT count(*) FROM verguetungsbestandteile", self.testschema)
        self.assertEqual(str(ergebnis), "[(1,)]")

        ergebnis = self.testfirma.get_nutzer("M100001"). \
            abfrage_ausfuehren("SELECT count(*) FROM austrittsgruende", self.testschema)
        self.assertEqual(str(ergebnis), "[(1,)]")

        ergebnis = self.testfirma.get_nutzer("M100001"). \
            abfrage_ausfuehren("SELECT count(*) FROM kategorien_austrittsgruende", self.testschema)
        self.assertEqual(str(ergebnis), "[(1,)]")

        ergebnis = self.testfirma.get_nutzer("M100001"). \
            abfrage_ausfuehren("SELECT count(*) FROM mandanten", self.testschema)
        self.assertEqual(str(ergebnis), "[(1,)]")

        ergebnis = self.testfirma.get_nutzer("M100001"). \
            abfrage_ausfuehren("SELECT count(*) FROM nutzer", self.testschema)
        self.assertEqual(str(ergebnis), "[(1,)]")

        ergebnis = self.testfirma.get_nutzer("M100001"). \
            abfrage_ausfuehren("SELECT count(*) FROM hat_jobtitel", self.testschema)
        self.assertEqual(str(ergebnis), "[(4,)]")

        ergebnis = self.testfirma.get_nutzer("M100001"). \
            abfrage_ausfuehren("SELECT count(*) FROM jobtitel", self.testschema)
        self.assertEqual(str(ergebnis), "[(1,)]")

        ergebnis = self.testfirma.get_nutzer("M100001"). \
            abfrage_ausfuehren("SELECT count(*) FROM erfahrungsstufen", self.testschema)
        self.assertEqual(str(ergebnis), "[(1,)]")

        ergebnis = self.testfirma.get_nutzer("M100001"). \
            abfrage_ausfuehren("SELECT count(*) FROM eingesetzt_in", self.testschema)
        self.assertEqual(str(ergebnis), "[(4,)]")

        ergebnis = self.testfirma.get_nutzer("M100001"). \
            abfrage_ausfuehren("SELECT count(*) FROM abteilungen", self.testschema)
        self.assertEqual(str(ergebnis), "[(1,)]")

        ergebnis = self.testfirma.get_nutzer("M100001"). \
            abfrage_ausfuehren("SELECT count(*) FROM arbeitet_x_wochenstunden", self.testschema)
        self.assertEqual(str(ergebnis), "[(4,)]")

        ergebnis = self.testfirma.get_nutzer("M100001"). \
            abfrage_ausfuehren("SELECT count(*) FROM wochenarbeitsstunden", self.testschema)
        self.assertEqual(str(ergebnis), "[(1,)]")

        ergebnis = self.testfirma.get_nutzer("M100001"). \
            abfrage_ausfuehren("SELECT count(*) FROM in_steuerklasse", self.testschema)
        self.assertEqual(str(ergebnis), "[(4,)]")

        ergebnis = self.testfirma.get_nutzer("M100001"). \
            abfrage_ausfuehren("SELECT count(*) FROM steuerklassen", self.testschema)
        self.assertEqual(str(ergebnis), "[(1,)]")

        # Mandantendaten loeschen. In allen Tabellen duerfen nun keine Datensaetze des Mandanten vorhanden sein
        self.testfirma.get_nutzer("M100001").delete_mandantendaten(self.testschema)

        ergebnis = self.testfirma.get_nutzer("M100001"). \
            abfrage_ausfuehren("SELECT count(*) FROM mitarbeiter", self.testschema)
        self.assertEqual(str(ergebnis), "[(0,)]")

        ergebnis = self.testfirma.get_nutzer("M100001"). \
            abfrage_ausfuehren("SELECT count(*) FROM hat_gesetzliche_Rentenversicherung", self.testschema)
        self.assertEqual(str(ergebnis), "[(0,)]")

        ergebnis = self.testfirma.get_nutzer("M100001"). \
            abfrage_ausfuehren("SELECT count(*) FROM rentenversicherungen", self.testschema)
        self.assertEqual(str(ergebnis), "[(0,)]")

        ergebnis = self.testfirma.get_nutzer("M100001"). \
            abfrage_ausfuehren("SELECT count(*) FROM hat_rv_beitraege", self.testschema)
        self.assertEqual(str(ergebnis), "[(0,)]")

        ergebnis = self.testfirma.get_nutzer("M100001"). \
            abfrage_ausfuehren("SELECT count(*) FROM rentenversicherungsbeitraege", self.testschema)
        self.assertEqual(str(ergebnis), "[(0,)]")

        ergebnis = self.testfirma.get_nutzer("M100001"). \
            abfrage_ausfuehren("SELECT count(*) FROM hat_gesetzliche_arbeitslosenversicherung", self.testschema)
        self.assertEqual(str(ergebnis), "[(0,)]")

        ergebnis = self.testfirma.get_nutzer("M100001"). \
            abfrage_ausfuehren("SELECT count(*) FROM arbeitslosenversicherungen", self.testschema)
        self.assertEqual(str(ergebnis), "[(0,)]")

        ergebnis = self.testfirma.get_nutzer("M100001"). \
            abfrage_ausfuehren("SELECT count(*) FROM hat_av_beitraege", self.testschema)
        self.assertEqual(str(ergebnis), "[(0,)]")

        ergebnis = self.testfirma.get_nutzer("M100001"). \
            abfrage_ausfuehren("SELECT count(*) FROM arbeitslosenversicherungsbeitraege", self.testschema)
        self.assertEqual(str(ergebnis), "[(0,)]")

        ergebnis = self.testfirma.get_nutzer("M100001"). \
            abfrage_ausfuehren("SELECT count(*) FROM arbeitet_in_sachsen", self.testschema)
        self.assertEqual(str(ergebnis), "[(0,)]")

        ergebnis = self.testfirma.get_nutzer("M100001"). \
            abfrage_ausfuehren("SELECT count(*) FROM arbeitsort_sachsen", self.testschema)
        self.assertEqual(str(ergebnis), "[(0,)]")

        ergebnis = self.testfirma.get_nutzer("M100001"). \
            abfrage_ausfuehren("SELECT count(*) FROM hat_gesetzlichen_ag_pv_beitragssatz", self.testschema)
        self.assertEqual(str(ergebnis), "[(0,)]")

        ergebnis = self.testfirma.get_nutzer("M100001"). \
            abfrage_ausfuehren("SELECT count(*) FROM ag_pflegeversicherungsbeitraege_gesetzlich", self.testschema)
        self.assertEqual(str(ergebnis), "[(0,)]")

        ergebnis = self.testfirma.get_nutzer("M100001"). \
            abfrage_ausfuehren("SELECT count(*) FROM hat_x_kinder_unter_25", self.testschema)
        self.assertEqual(str(ergebnis), "[(0,)]")

        ergebnis = self.testfirma.get_nutzer("M100001"). \
            abfrage_ausfuehren("SELECT count(*) FROM anzahl_kinder_unter_25", self.testschema)
        self.assertEqual(str(ergebnis), "[(0,)]")

        ergebnis = self.testfirma.get_nutzer("M100001"). \
            abfrage_ausfuehren("SELECT count(*) FROM hat_gesetzlichen_an_pv_beitragssatz", self.testschema)
        self.assertEqual(str(ergebnis), "[(0,)]")

        ergebnis = self.testfirma.get_nutzer("M100001"). \
            abfrage_ausfuehren("SELECT count(*) FROM an_pflegeversicherungsbeitraege_gesetzlich", self.testschema)
        self.assertEqual(str(ergebnis), "[(0,)]")

        ergebnis = self.testfirma.get_nutzer("M100001"). \
            abfrage_ausfuehren("SELECT count(*) FROM hat_gesetzliche_krankenversicherung", self.testschema)
        self.assertEqual(str(ergebnis), "[(0,)]")

        ergebnis = self.testfirma.get_nutzer("M100001"). \
            abfrage_ausfuehren("SELECT count(*) FROM krankenversicherungen", self.testschema)
        self.assertEqual(str(ergebnis), "[(0,)]")

        ergebnis = self.testfirma.get_nutzer("M100001"). \
            abfrage_ausfuehren("SELECT count(*) FROM hat_gkv_beitraege", self.testschema)
        self.assertEqual(str(ergebnis), "[(0,)]")

        ergebnis = self.testfirma.get_nutzer("M100001"). \
            abfrage_ausfuehren("SELECT count(*) FROM gkv_beitraege", self.testschema)
        self.assertEqual(str(ergebnis), "[(0,)]")

        ergebnis = self.testfirma.get_nutzer("M100001"). \
            abfrage_ausfuehren("SELECT count(*) FROM ist_in_gkv", self.testschema)
        self.assertEqual(str(ergebnis), "[(0,)]")

        ergebnis = self.testfirma.get_nutzer("M100001"). \
            abfrage_ausfuehren("SELECT count(*) FROM gesetzliche_krankenkassen", self.testschema)
        self.assertEqual(str(ergebnis), "[(0,)]")

        ergebnis = self.testfirma.get_nutzer("M100001"). \
            abfrage_ausfuehren("SELECT count(*) FROM hat_gkv_zusatzbeitrag", self.testschema)
        self.assertEqual(str(ergebnis), "[(0,)]")

        ergebnis = self.testfirma.get_nutzer("M100001"). \
            abfrage_ausfuehren("SELECT count(*) FROM gkv_zusatzbeitraege", self.testschema)
        self.assertEqual(str(ergebnis), "[(0,)]")

        ergebnis = self.testfirma.get_nutzer("M100001"). \
            abfrage_ausfuehren("SELECT count(*) FROM hat_privatkrankenkasse", self.testschema)
        self.assertEqual(str(ergebnis), "[(0,)]")

        ergebnis = self.testfirma.get_nutzer("M100001"). \
            abfrage_ausfuehren("SELECT count(*) FROM privatkrankenkassen", self.testschema)
        self.assertEqual(str(ergebnis), "[(0,)]")

        ergebnis = self.testfirma.get_nutzer("M100001"). \
            abfrage_ausfuehren("SELECT count(*) FROM ist_anderweitig_versichert", self.testschema)
        self.assertEqual(str(ergebnis), "[(0,)]")

        ergebnis = self.testfirma.get_nutzer("M100001"). \
            abfrage_ausfuehren("SELECT count(*) FROM gemeldete_krankenkassen", self.testschema)
        self.assertEqual(str(ergebnis), "[(0,)]")

        ergebnis = self.testfirma.get_nutzer("M100001"). \
            abfrage_ausfuehren("SELECT count(*) FROM hat_umlagen_gesetzlich", self.testschema)
        self.assertEqual(str(ergebnis), "[(0,)]")

        ergebnis = self.testfirma.get_nutzer("M100001"). \
            abfrage_ausfuehren("SELECT count(*) FROM hat_umlagen_privat", self.testschema)
        self.assertEqual(str(ergebnis), "[(0,)]")

        ergebnis = self.testfirma.get_nutzer("M100001"). \
            abfrage_ausfuehren("SELECT count(*) FROM hat_umlagen_anderweitig", self.testschema)
        self.assertEqual(str(ergebnis), "[(0,)]")

        ergebnis = self.testfirma.get_nutzer("M100001"). \
            abfrage_ausfuehren("SELECT count(*) FROM umlagen", self.testschema)
        self.assertEqual(str(ergebnis), "[(0,)]")

        ergebnis = self.testfirma.get_nutzer("M100001"). \
            abfrage_ausfuehren("SELECT count(*) FROM ist_minijobber", self.testschema)
        self.assertEqual(str(ergebnis), "[(0,)]")

        ergebnis = self.testfirma.get_nutzer("M100001"). \
            abfrage_ausfuehren("SELECT count(*) FROM minijobs", self.testschema)
        self.assertEqual(str(ergebnis), "[(0,)]")

        ergebnis = self.testfirma.get_nutzer("M100001"). \
            abfrage_ausfuehren("SELECT count(*) FROM hat_pauschalabgaben", self.testschema)
        self.assertEqual(str(ergebnis), "[(0,)]")

        ergebnis = self.testfirma.get_nutzer("M100001"). \
            abfrage_ausfuehren("SELECT count(*) FROM pauschalabgaben", self.testschema)
        self.assertEqual(str(ergebnis), "[(0,)]")

        ergebnis = self.testfirma.get_nutzer("M100001"). \
            abfrage_ausfuehren("SELECT count(*) FROM in_gesellschaft", self.testschema)
        self.assertEqual(str(ergebnis), "[(0,)]")

        ergebnis = self.testfirma.get_nutzer("M100001"). \
            abfrage_ausfuehren("SELECT count(*) FROM gesellschaften", self.testschema)
        self.assertEqual(str(ergebnis), "[(0,)]")

        ergebnis = self.testfirma.get_nutzer("M100001"). \
            abfrage_ausfuehren("SELECT count(*) FROM unfallversicherungsbeitraege", self.testschema)
        self.assertEqual(str(ergebnis), "[(0,)]")

        ergebnis = self.testfirma.get_nutzer("M100001"). \
            abfrage_ausfuehren("SELECT count(*) FROM berufsgenossenschaften", self.testschema)
        self.assertEqual(str(ergebnis), "[(0,)]")

        ergebnis = self.testfirma.get_nutzer("M100001"). \
            abfrage_ausfuehren("SELECT count(*) FROM ist_mitarbeitertyp", self.testschema)
        self.assertEqual(str(ergebnis), "[(0,)]")

        ergebnis = self.testfirma.get_nutzer("M100001"). \
            abfrage_ausfuehren("SELECT count(*) FROM mitarbeitertypen", self.testschema)
        self.assertEqual(str(ergebnis), "[(0,)]")

        ergebnis = self.testfirma.get_nutzer("M100001"). \
            abfrage_ausfuehren("SELECT count(*) FROM hat_geschlecht", self.testschema)
        self.assertEqual(str(ergebnis), "[(0,)]")

        ergebnis = self.testfirma.get_nutzer("M100001"). \
            abfrage_ausfuehren("SELECT count(*) FROM geschlechter", self.testschema)
        self.assertEqual(str(ergebnis), "[(0,)]")

        ergebnis = self.testfirma.get_nutzer("M100001"). \
            abfrage_ausfuehren("SELECT count(*) FROM wohnt_in", self.testschema)
        self.assertEqual(str(ergebnis), "[(0,)]")

        ergebnis = self.testfirma.get_nutzer("M100001"). \
            abfrage_ausfuehren("SELECT count(*) FROM strassenbezeichnungen", self.testschema)
        self.assertEqual(str(ergebnis), "[(0,)]")

        ergebnis = self.testfirma.get_nutzer("M100001"). \
            abfrage_ausfuehren("SELECT count(*) FROM postleitzahlen", self.testschema)
        self.assertEqual(str(ergebnis), "[(0,)]")

        ergebnis = self.testfirma.get_nutzer("M100001"). \
            abfrage_ausfuehren("SELECT count(*) FROM staedte", self.testschema)
        self.assertEqual(str(ergebnis), "[(0,)]")

        ergebnis = self.testfirma.get_nutzer("M100001"). \
            abfrage_ausfuehren("SELECT count(*) FROM regionen", self.testschema)
        self.assertEqual(str(ergebnis), "[(0,)]")

        ergebnis = self.testfirma.get_nutzer("M100001"). \
            abfrage_ausfuehren("SELECT count(*) FROM laender", self.testschema)
        self.assertEqual(str(ergebnis), "[(0,)]")

        ergebnis = self.testfirma.get_nutzer("M100001"). \
            abfrage_ausfuehren("SELECT count(*) FROM hat_tarif", self.testschema)
        self.assertEqual(str(ergebnis), "[(0,)]")

        ergebnis = self.testfirma.get_nutzer("M100001"). \
            abfrage_ausfuehren("SELECT count(*) FROM tarife", self.testschema)
        self.assertEqual(str(ergebnis), "[(0,)]")

        ergebnis = self.testfirma.get_nutzer("M100001"). \
            abfrage_ausfuehren("SELECT count(*) FROM gewerkschaften", self.testschema)
        self.assertEqual(str(ergebnis), "[(0,)]")

        ergebnis = self.testfirma.get_nutzer("M100001"). \
            abfrage_ausfuehren("SELECT count(*) FROM hat_verguetungsbestandteil_tarif", self.testschema)
        self.assertEqual(str(ergebnis), "[(0,)]")

        ergebnis = self.testfirma.get_nutzer("M100001"). \
            abfrage_ausfuehren("SELECT count(*) FROM aussertarifliche", self.testschema)
        self.assertEqual(str(ergebnis), "[(0,)]")

        ergebnis = self.testfirma.get_nutzer("M100001"). \
            abfrage_ausfuehren("SELECT count(*) FROM hat_verguetungsbestandteil_at", self.testschema)
        self.assertEqual(str(ergebnis), "[(0,)]")

        ergebnis = self.testfirma.get_nutzer("M100001"). \
            abfrage_ausfuehren("SELECT count(*) FROM verguetungsbestandteile", self.testschema)
        self.assertEqual(str(ergebnis), "[(0,)]")

        ergebnis = self.testfirma.get_nutzer("M100001"). \
            abfrage_ausfuehren("SELECT count(*) FROM austrittsgruende", self.testschema)
        self.assertEqual(str(ergebnis), "[(0,)]")

        ergebnis = self.testfirma.get_nutzer("M100001"). \
            abfrage_ausfuehren("SELECT count(*) FROM kategorien_austrittsgruende", self.testschema)
        self.assertEqual(str(ergebnis), "[(0,)]")

        ergebnis = self.testfirma.get_nutzer("M100001"). \
            abfrage_ausfuehren("SELECT count(*) FROM mandanten", self.testschema)
        self.assertEqual(str(ergebnis), "[(0,)]")

        ergebnis = self.testfirma.get_nutzer("M100001"). \
            abfrage_ausfuehren("SELECT count(*) FROM nutzer", self.testschema)
        self.assertEqual(str(ergebnis), "[(0,)]")

        ergebnis = self.testfirma.get_nutzer("M100001"). \
            abfrage_ausfuehren("SELECT count(*) FROM hat_jobtitel", self.testschema)
        self.assertEqual(str(ergebnis), "[(0,)]")

        ergebnis = self.testfirma.get_nutzer("M100001"). \
            abfrage_ausfuehren("SELECT count(*) FROM jobtitel", self.testschema)
        self.assertEqual(str(ergebnis), "[(0,)]")

        ergebnis = self.testfirma.get_nutzer("M100001"). \
            abfrage_ausfuehren("SELECT count(*) FROM erfahrungsstufen", self.testschema)
        self.assertEqual(str(ergebnis), "[(0,)]")

        ergebnis = self.testfirma.get_nutzer("M100001"). \
            abfrage_ausfuehren("SELECT count(*) FROM eingesetzt_in", self.testschema)
        self.assertEqual(str(ergebnis), "[(0,)]")

        ergebnis = self.testfirma.get_nutzer("M100001"). \
            abfrage_ausfuehren("SELECT count(*) FROM abteilungen", self.testschema)
        self.assertEqual(str(ergebnis), "[(0,)]")

        ergebnis = self.testfirma.get_nutzer("M100001"). \
            abfrage_ausfuehren("SELECT count(*) FROM arbeitet_x_wochenstunden", self.testschema)
        self.assertEqual(str(ergebnis), "[(0,)]")

        ergebnis = self.testfirma.get_nutzer("M100001"). \
            abfrage_ausfuehren("SELECT count(*) FROM wochenarbeitsstunden", self.testschema)
        self.assertEqual(str(ergebnis), "[(0,)]")

        ergebnis = self.testfirma.get_nutzer("M100001"). \
            abfrage_ausfuehren("SELECT count(*) FROM in_steuerklasse", self.testschema)
        self.assertEqual(str(ergebnis), "[(0,)]")

        ergebnis = self.testfirma.get_nutzer("M100001"). \
            abfrage_ausfuehren("SELECT count(*) FROM steuerklassen", self.testschema)
        self.assertEqual(str(ergebnis), "[(0,)]")

    def tearDown(self):
        """
        Methode ruft Funktion 'test_tear_down' auf, welches das Datenbankschema 'temp_test_schema' mit allen Daten
        entfernt.
        """
        test_tear_down()
