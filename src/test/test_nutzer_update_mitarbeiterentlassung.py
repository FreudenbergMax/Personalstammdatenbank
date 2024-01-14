import unittest
from src.main.Mandant import Mandant
from src.main.test_SetUp_TearDown import test_set_up, test_tear_down


class TestNutzerUpdateMitarbeiterentlassung(unittest.TestCase):

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

        # Mitarbeiter einfuegen
        self.testfirma.get_nutzer("M100001"). \
            insert_neuer_mitarbeiter('testdaten_insert_mitarbeiter/Mitarbeiter.xlsx', self.testschema)

    def test_erfolgreicher_eintrag(self):
        """
        Test prueft, ob Entlassungsdatum und -grund eingetragen werden
        """
        self.testfirma.get_nutzer("M100001").\
            update_mitarbeiterentlassung('testdaten_update_mitarbeiterentlassung/'
                                         'Update Mitarbeiterentlassung.xlsx', self.testschema)

        # pruefen, ob fuer Mitarbeiter Austrittsdatum und Fremdschluessel-ID des Austrittsgrundes eingetragen sind
        ergebnis = self.testfirma.get_nutzer("M100001").abfrage_ausfuehren("SELECT austrittsdatum, austrittsgrund_id "
                                                                           "FROM mitarbeiter", self.testschema)
        self.assertEqual(str(ergebnis), "[(datetime.date(2030, 12, 31), 1)]")

        # pruefen, ob in den mitarbeiterbezogenen Assoziationstabellen die 'Bis-Datum'-Angaben auf Austrittsdatum
        # umgestellt sind
        ergebnis = self.testfirma.get_nutzer("M100001"). \
            abfrage_ausfuehren("SELECT * FROM hat_gesetzliche_rentenversicherung", self.testschema)
        self.assertEqual(str(ergebnis), "[(1, 1, 1, datetime.date(2024, 1, 1), datetime.date(2030, 12, 31))]")

        ergebnis = self.testfirma.get_nutzer("M100001"). \
            abfrage_ausfuehren("SELECT * FROM hat_gesetzliche_arbeitslosenversicherung", self.testschema)
        self.assertEqual(str(ergebnis), "[(1, 1, 1, datetime.date(2024, 1, 1), datetime.date(2030, 12, 31))]")

        ergebnis = self.testfirma.get_nutzer("M100001"). \
            abfrage_ausfuehren("SELECT * FROM arbeitet_in_sachsen", self.testschema)
        self.assertEqual(str(ergebnis), "[(1, 1, 1, datetime.date(2024, 1, 1), datetime.date(2030, 12, 31))]")

        ergebnis = self.testfirma.get_nutzer("M100001"). \
            abfrage_ausfuehren("SELECT * FROM hat_x_kinder_unter_25", self.testschema)
        self.assertEqual(str(ergebnis), "[(1, 1, 1, datetime.date(2024, 1, 1), datetime.date(2030, 12, 31))]")

        ergebnis = self.testfirma.get_nutzer("M100001"). \
            abfrage_ausfuehren("SELECT * FROM hat_gesetzliche_krankenversicherung", self.testschema)
        self.assertEqual(str(ergebnis), "[(1, 1, 1, datetime.date(2024, 1, 1), datetime.date(2030, 12, 31))]")

        ergebnis = self.testfirma.get_nutzer("M100001"). \
            abfrage_ausfuehren("SELECT * FROM ist_in_gkv", self.testschema)
        self.assertEqual(str(ergebnis), "[(1, 1, 1, datetime.date(2024, 1, 1), datetime.date(2030, 12, 31))]")

        # muss leer sein, da gesetzlich krankenversichert. Kann also nicht privatversichert sein.
        ergebnis = self.testfirma.get_nutzer("M100001"). \
            abfrage_ausfuehren("SELECT * FROM hat_privatkrankenkasse", self.testschema)
        self.assertEqual(str(ergebnis), "[]")

        # muss leer sein, da gesetzlich krankenversichert, kann also nicht ueber einen anderen Arbeitgeber oder
        # freiwillig versichert sein
        ergebnis = self.testfirma.get_nutzer("M100001"). \
            abfrage_ausfuehren("SELECT * FROM ist_anderweitig_versichert", self.testschema)
        self.assertEqual(str(ergebnis), "[]")

        # muss leer sein, da gesetzlich krankenversichert, kann also kein Minijobber sein
        ergebnis = self.testfirma.get_nutzer("M100001"). \
            abfrage_ausfuehren("SELECT * FROM ist_minijobber", self.testschema)
        self.assertEqual(str(ergebnis), "[]")

        ergebnis = self.testfirma.get_nutzer("M100001"). \
            abfrage_ausfuehren("SELECT * FROM in_gesellschaft", self.testschema)
        self.assertEqual(str(ergebnis), "[(1, 1, 1, datetime.date(2024, 1, 1), datetime.date(2030, 12, 31))]")

        ergebnis = self.testfirma.get_nutzer("M100001"). \
            abfrage_ausfuehren("SELECT * FROM ist_mitarbeitertyp", self.testschema)
        self.assertEqual(str(ergebnis), "[(1, 1, 1, datetime.date(2024, 1, 1), datetime.date(2030, 12, 31))]")

        ergebnis = self.testfirma.get_nutzer("M100001"). \
            abfrage_ausfuehren("SELECT * FROM hat_geschlecht", self.testschema)
        self.assertEqual(str(ergebnis), "[(1, 1, 1, datetime.date(2024, 1, 1), datetime.date(2030, 12, 31))]")

        ergebnis = self.testfirma.get_nutzer("M100001"). \
            abfrage_ausfuehren("SELECT * FROM wohnt_in", self.testschema)
        self.assertEqual(str(ergebnis), "[(1, 1, 1, datetime.date(2024, 1, 1), datetime.date(2030, 12, 31))]")

        ergebnis = self.testfirma.get_nutzer("M100001"). \
            abfrage_ausfuehren("SELECT * FROM hat_tarif", self.testschema)
        self.assertEqual(str(ergebnis), "[(1, 1, 1, datetime.date(2024, 1, 1), datetime.date(2030, 12, 31))]")

        # muss leer sein, da tariflich angestellt. Kann also nicht aussertariflich sein
        ergebnis = self.testfirma.get_nutzer("M100001"). \
            abfrage_ausfuehren("SELECT * FROM aussertarifliche", self.testschema)
        self.assertEqual(str(ergebnis), "[]")

        ergebnis = self.testfirma.get_nutzer("M100001"). \
            abfrage_ausfuehren("SELECT * FROM hat_jobtitel", self.testschema)
        self.assertEqual(str(ergebnis), "[(1, 1, 1, 1, datetime.date(2024, 1, 1), datetime.date(2030, 12, 31))]")

        ergebnis = self.testfirma.get_nutzer("M100001"). \
            abfrage_ausfuehren("SELECT * FROM eingesetzt_in", self.testschema)
        self.assertEqual(str(ergebnis), "[(1, 1, 1, False, datetime.date(2024, 1, 1), datetime.date(2030, 12, 31))]")

        ergebnis = self.testfirma.get_nutzer("M100001"). \
            abfrage_ausfuehren("SELECT * FROM arbeitet_x_wochenstunden", self.testschema)
        self.assertEqual(str(ergebnis), "[(1, 1, 1, datetime.date(2024, 1, 1), datetime.date(2030, 12, 31))]")

        ergebnis = self.testfirma.get_nutzer("M100001"). \
            abfrage_ausfuehren("SELECT * FROM in_steuerklasse", self.testschema)
        self.assertEqual(str(ergebnis), "[(1, 1, 1, datetime.date(2024, 1, 1), datetime.date(2030, 12, 31))]")

    def test_mitarbeiter_existiert_nicht(self):
        """
        Test prueft, ob eine Exception geworfen wird, wenn der Mitarbeiter-Update fuer eine Personalnummer vorgenommen
        wird, die in der Datenbank nicht existiert
        """
        with self.assertRaises(Exception) as context:
            self.testfirma.get_nutzer("M100001"). \
                update_mitarbeiterentlassung('testdaten_update_mitarbeiterentlassung/'
                                             'Update Mitarbeiterentlassung - Mitarbeiter existiert nicht.xlsx',
                                             self.testschema)

        self.assertEqual(str(context.exception), "FEHLER:  Mitarbeiter 'M100003' existiert nicht!\n"
                                                 "CONTEXT:  PL/pgSQL-Funktion update_mitarbeiterentlassung(integer,"
                                                 "character varying,date,character varying) Zeile 16 bei RAISE\n")

    def test_austrittsdatum_vor_eintrittsdatum(self):
        """
        Test pruft, ob eine Fehlermeldung ausgegeben wird, wenn durch einen fehlerhaften Eintrag das Austrittsdatum vor
        dem Eintrittsdatum liegt
        """
        with self.assertRaises(Exception) as context:
            self.testfirma.get_nutzer("M100001"). \
                update_mitarbeiterentlassung('testdaten_update_mitarbeiterentlassung/'
                                             'Update Mitarbeiterentlassung - Austrittsdatum vor Eintrittsdatum.xlsx',
                                             self.testschema)

        self.assertEqual(str(context.exception), "FEHLER:  Austrittsdatum '2010-12-31' liegt vor Eintrittsdatum "
                                                 "'2024-01-01'. Das ist unlogisch!\n"
                                                 "CONTEXT:  PL/pgSQL-Funktion update_mitarbeiterentlassung(integer,"
                                                 "character varying,date,character varying) Zeile 21 bei RAISE\n")

    def test_austrittsgrund_existiert_nicht(self):
        """
        Test pruft, ob eine Fehlermeldung ausgegeben wird, wenn ein Austrittsgrund angegeben wird, der in der
        Datenbank nicht hinterlegt ist.
        """
        with self.assertRaises(Exception) as context:
            self.testfirma.get_nutzer("M100001"). \
                update_mitarbeiterentlassung('testdaten_update_mitarbeiterentlassung/'
                                             'Update Mitarbeiterentlassung - Austrittsgrund existiert nicht.xlsx',
                                             self.testschema)

        self.assertEqual(str(context.exception), "FEHLER:  Austrittsgrund 'Insolvenz' ist nicht in Datenbank vorhanden."
                                                 " Bitte erst anlegen!\n"
                                                 "CONTEXT:  PL/pgSQL-Funktion update_mitarbeiterentlassung(integer,"
                                                 "character varying,date,character varying) Zeile 29 bei RAISE\n")

    def test_austrittsgrund_klein_geschrieben(self):
        """
        Test pruft, ob Eintrag durchgefuehrt wird, wenn Austrittsgrund und Personalnummer klein aber ansonsten korrekt
        geschrieben ist. Beispiel: "umsatzrueckgang" statt wie in Tabelle "Austrittsgruende" geschrieben
        "Umsatzrueckgang" oder "m100002" statt "M100002" als Personalnummer.
        """
        self.testfirma.get_nutzer("M100001"). \
            update_mitarbeiterentlassung('testdaten_update_mitarbeiterentlassung/'
                                         'Update Mitarbeiterentlassung - Austrittsgrund und Personalnummer '
                                         'klein geschrieben.xlsx',
                                         self.testschema)

        # pruefen, ob fuer Mitarbeiter Austrittsdatum und Fremdschluessel-ID des Austrittsgrundes eingetragen sind
        ergebnis = self.testfirma.get_nutzer("M100001").abfrage_ausfuehren("SELECT austrittsdatum, austrittsgrund_id "
                                                                           "FROM mitarbeiter", self.testschema)
        self.assertEqual(str(ergebnis), "[(datetime.date(2030, 12, 31), 1)]")

        # pruefen, ob in den mitarbeiterbezogenen Assoziationstabellen die 'Bis-Datum'-Angaben auf Austrittsdatum
        # umgestellt sind
        ergebnis = self.testfirma.get_nutzer("M100001"). \
            abfrage_ausfuehren("SELECT * FROM hat_gesetzliche_rentenversicherung", self.testschema)
        self.assertEqual(str(ergebnis), "[(1, 1, 1, datetime.date(2024, 1, 1), datetime.date(2030, 12, 31))]")

        ergebnis = self.testfirma.get_nutzer("M100001"). \
            abfrage_ausfuehren("SELECT * FROM hat_gesetzliche_arbeitslosenversicherung", self.testschema)
        self.assertEqual(str(ergebnis), "[(1, 1, 1, datetime.date(2024, 1, 1), datetime.date(2030, 12, 31))]")

        ergebnis = self.testfirma.get_nutzer("M100001"). \
            abfrage_ausfuehren("SELECT * FROM arbeitet_in_sachsen", self.testschema)
        self.assertEqual(str(ergebnis), "[(1, 1, 1, datetime.date(2024, 1, 1), datetime.date(2030, 12, 31))]")

        ergebnis = self.testfirma.get_nutzer("M100001"). \
            abfrage_ausfuehren("SELECT * FROM hat_x_kinder_unter_25", self.testschema)
        self.assertEqual(str(ergebnis), "[(1, 1, 1, datetime.date(2024, 1, 1), datetime.date(2030, 12, 31))]")

        ergebnis = self.testfirma.get_nutzer("M100001"). \
            abfrage_ausfuehren("SELECT * FROM hat_gesetzliche_krankenversicherung", self.testschema)
        self.assertEqual(str(ergebnis), "[(1, 1, 1, datetime.date(2024, 1, 1), datetime.date(2030, 12, 31))]")

        ergebnis = self.testfirma.get_nutzer("M100001"). \
            abfrage_ausfuehren("SELECT * FROM ist_in_gkv", self.testschema)
        self.assertEqual(str(ergebnis), "[(1, 1, 1, datetime.date(2024, 1, 1), datetime.date(2030, 12, 31))]")

        # muss leer sein, da gesetzlich krankenversichert. Kann also nicht privatversichert sein.
        ergebnis = self.testfirma.get_nutzer("M100001"). \
            abfrage_ausfuehren("SELECT * FROM hat_privatkrankenkasse", self.testschema)
        self.assertEqual(str(ergebnis), "[]")

        # muss leer sein, da gesetzlich krankenversichert, kann also nicht ueber einen anderen Arbeitgeber oder
        # freiwillig versichert sein
        ergebnis = self.testfirma.get_nutzer("M100001"). \
            abfrage_ausfuehren("SELECT * FROM ist_anderweitig_versichert", self.testschema)
        self.assertEqual(str(ergebnis), "[]")

        # muss leer sein, da gesetzlich krankenversichert, kann also kein Minijobber sein
        ergebnis = self.testfirma.get_nutzer("M100001"). \
            abfrage_ausfuehren("SELECT * FROM ist_minijobber", self.testschema)
        self.assertEqual(str(ergebnis), "[]")

        ergebnis = self.testfirma.get_nutzer("M100001"). \
            abfrage_ausfuehren("SELECT * FROM in_gesellschaft", self.testschema)
        self.assertEqual(str(ergebnis), "[(1, 1, 1, datetime.date(2024, 1, 1), datetime.date(2030, 12, 31))]")

        ergebnis = self.testfirma.get_nutzer("M100001"). \
            abfrage_ausfuehren("SELECT * FROM ist_mitarbeitertyp", self.testschema)
        self.assertEqual(str(ergebnis), "[(1, 1, 1, datetime.date(2024, 1, 1), datetime.date(2030, 12, 31))]")

        ergebnis = self.testfirma.get_nutzer("M100001"). \
            abfrage_ausfuehren("SELECT * FROM hat_geschlecht", self.testschema)
        self.assertEqual(str(ergebnis), "[(1, 1, 1, datetime.date(2024, 1, 1), datetime.date(2030, 12, 31))]")

        ergebnis = self.testfirma.get_nutzer("M100001"). \
            abfrage_ausfuehren("SELECT * FROM wohnt_in", self.testschema)
        self.assertEqual(str(ergebnis), "[(1, 1, 1, datetime.date(2024, 1, 1), datetime.date(2030, 12, 31))]")

        ergebnis = self.testfirma.get_nutzer("M100001"). \
            abfrage_ausfuehren("SELECT * FROM hat_tarif", self.testschema)
        self.assertEqual(str(ergebnis), "[(1, 1, 1, datetime.date(2024, 1, 1), datetime.date(2030, 12, 31))]")

        # muss leer sein, da tariflich angestellt. Kann also nicht aussertariflich sein
        ergebnis = self.testfirma.get_nutzer("M100001"). \
            abfrage_ausfuehren("SELECT * FROM aussertarifliche", self.testschema)
        self.assertEqual(str(ergebnis), "[]")

        ergebnis = self.testfirma.get_nutzer("M100001"). \
            abfrage_ausfuehren("SELECT * FROM hat_jobtitel", self.testschema)
        self.assertEqual(str(ergebnis), "[(1, 1, 1, 1, datetime.date(2024, 1, 1), datetime.date(2030, 12, 31))]")

        ergebnis = self.testfirma.get_nutzer("M100001"). \
            abfrage_ausfuehren("SELECT * FROM eingesetzt_in", self.testschema)
        self.assertEqual(str(ergebnis), "[(1, 1, 1, False, datetime.date(2024, 1, 1), datetime.date(2030, 12, 31))]")

        ergebnis = self.testfirma.get_nutzer("M100001"). \
            abfrage_ausfuehren("SELECT * FROM arbeitet_x_wochenstunden", self.testschema)
        self.assertEqual(str(ergebnis), "[(1, 1, 1, datetime.date(2024, 1, 1), datetime.date(2030, 12, 31))]")

        ergebnis = self.testfirma.get_nutzer("M100001"). \
            abfrage_ausfuehren("SELECT * FROM in_steuerklasse", self.testschema)
        self.assertEqual(str(ergebnis), "[(1, 1, 1, datetime.date(2024, 1, 1), datetime.date(2030, 12, 31))]")

    def tearDown(self):
        """
        Methode ruft Funktion 'test_tear_down' auf, welches das Datenbankschema 'temp_test_schema' mit allen Daten
        entfernt.
        """
        test_tear_down()
