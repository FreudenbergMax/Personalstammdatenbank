import unittest
from src.main.Mandant import Mandant
from src.main.test_SetUp_TearDown import test_set_up, test_tear_down


class TestNutzerDeleteMitarbeiterdaten(unittest.TestCase):

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

    def test_erfolgreiche_entfernung_gesetzlicher_sv_mitarbeiter(self):
        """
        Test prueft, ob gesetzlich versicherter Mitarbeiter aus Tabelle 'Mitarbeiter' und allen mitarbeiterbezogenen
        Assoziationstabellen entfernt wird
        """
        self.testfirma.get_nutzer("M100001"). \
            insert_neuer_mitarbeiter('testdaten_insert_mitarbeiter/Mitarbeiter.xlsx', self.testschema)

        # Inhalt aus Tabellen ziehen, um zu pruefen, ob der Datensatz angelegt wurde
        ergebnis = self.testfirma.get_nutzer("M100001"). \
            abfrage_ausfuehren("SELECT * FROM mitarbeiter", self.testschema)
        self.assertEqual(str(ergebnis), "[(1, 1, 'M100002', 'Max', None, 'Mustermann', datetime.date(1992, 12, 12), "
                                        "datetime.date(2024, 1, 1), '11 111 111 111', '00 121292 F 00', "
                                        "'DE00 0000 0000 0000 0000 00', '0175 1234567', 'maxmustermann@web.de', "
                                        "'030 987654321', 'Mustermann@testfirma.de', datetime.date(9999, 12, 31), "
                                        "None, None)]")

        ergebnis = self.testfirma.get_nutzer("M100001"). \
            abfrage_ausfuehren("SELECT * FROM hat_gesetzliche_rentenversicherung", self.testschema)
        self.assertEqual(str(ergebnis), "[(1, 1, 1, datetime.date(2024, 1, 1), datetime.date(9999, 12, 31))]")

        ergebnis = self.testfirma.get_nutzer("M100001"). \
            abfrage_ausfuehren("SELECT * FROM hat_gesetzliche_arbeitslosenversicherung", self.testschema)
        self.assertEqual(str(ergebnis), "[(1, 1, 1, datetime.date(2024, 1, 1), datetime.date(9999, 12, 31))]")

        ergebnis = self.testfirma.get_nutzer("M100001"). \
            abfrage_ausfuehren("SELECT * FROM arbeitet_in_sachsen", self.testschema)
        self.assertEqual(str(ergebnis), "[(1, 1, 1, datetime.date(2024, 1, 1), datetime.date(9999, 12, 31))]")

        ergebnis = self.testfirma.get_nutzer("M100001"). \
            abfrage_ausfuehren("SELECT * FROM hat_x_kinder_unter_25", self.testschema)
        self.assertEqual(str(ergebnis), "[(1, 1, 1, datetime.date(2024, 1, 1), datetime.date(9999, 12, 31))]")

        ergebnis = self.testfirma.get_nutzer("M100001"). \
            abfrage_ausfuehren("SELECT * FROM hat_gesetzliche_krankenversicherung", self.testschema)
        self.assertEqual(str(ergebnis), "[(1, 1, 1, datetime.date(2024, 1, 1), datetime.date(9999, 12, 31))]")

        ergebnis = self.testfirma.get_nutzer("M100001"). \
            abfrage_ausfuehren("SELECT * FROM ist_in_gkv", self.testschema)
        self.assertEqual(str(ergebnis), "[(1, 1, 1, datetime.date(2024, 1, 1), datetime.date(9999, 12, 31))]")

        ergebnis = self.testfirma.get_nutzer("M100001"). \
            abfrage_ausfuehren("SELECT * FROM in_gesellschaft", self.testschema)
        self.assertEqual(str(ergebnis), "[(1, 1, 1, datetime.date(2024, 1, 1), datetime.date(9999, 12, 31))]")

        ergebnis = self.testfirma.get_nutzer("M100001"). \
            abfrage_ausfuehren("SELECT * FROM ist_mitarbeitertyp", self.testschema)
        self.assertEqual(str(ergebnis), "[(1, 1, 1, datetime.date(2024, 1, 1), datetime.date(9999, 12, 31))]")

        ergebnis = self.testfirma.get_nutzer("M100001"). \
            abfrage_ausfuehren("SELECT * FROM hat_geschlecht", self.testschema)
        self.assertEqual(str(ergebnis), "[(1, 1, 1, datetime.date(2024, 1, 1), datetime.date(9999, 12, 31))]")

        ergebnis = self.testfirma.get_nutzer("M100001"). \
            abfrage_ausfuehren("SELECT * FROM wohnt_in", self.testschema)
        self.assertEqual(str(ergebnis), "[(1, 1, 1, datetime.date(2024, 1, 1), datetime.date(9999, 12, 31))]")

        ergebnis = self.testfirma.get_nutzer("M100001"). \
            abfrage_ausfuehren("SELECT * FROM hat_tarif", self.testschema)
        self.assertEqual(str(ergebnis), "[(1, 1, 1, datetime.date(2024, 1, 1), datetime.date(9999, 12, 31))]")

        ergebnis = self.testfirma.get_nutzer("M100001"). \
            abfrage_ausfuehren("SELECT * FROM hat_jobtitel", self.testschema)
        self.assertEqual(str(ergebnis), "[(1, 1, 1, 1, datetime.date(2024, 1, 1), datetime.date(9999, 12, 31))]")

        ergebnis = self.testfirma.get_nutzer("M100001"). \
            abfrage_ausfuehren("SELECT * FROM eingesetzt_in", self.testschema)
        self.assertEqual(str(ergebnis), "[(1, 1, 1, False, datetime.date(2024, 1, 1), datetime.date(9999, 12, 31))]")

        ergebnis = self.testfirma.get_nutzer("M100001"). \
            abfrage_ausfuehren("SELECT * FROM arbeitet_x_wochenstunden", self.testschema)
        self.assertEqual(str(ergebnis), "[(1, 1, 1, datetime.date(2024, 1, 1), datetime.date(9999, 12, 31))]")

        ergebnis = self.testfirma.get_nutzer("M100001"). \
            abfrage_ausfuehren("SELECT * FROM in_steuerklasse", self.testschema)
        self.assertEqual(str(ergebnis), "[(1, 1, 1, datetime.date(2024, 1, 1), datetime.date(9999, 12, 31))]")

        # Nun Entfernung des Mitarbeiters. Tabellen muessen von diesem Mitarbeiter nun wieder leer sein
        self.testfirma.get_nutzer("M100001").delete_mitarbeiterdaten("testdaten_delete_Mitarbeiterdaten/delete "
                                                                     "Personalnummer.xlsx",
                                                                     self.testschema)

        ergebnis = self.testfirma.get_nutzer("M100001").abfrage_ausfuehren("SELECT * FROM mitarbeiter", self.testschema)
        self.assertEqual(str(ergebnis), "[]")

        ergebnis = self.testfirma.get_nutzer("M100001"). \
            abfrage_ausfuehren("SELECT * FROM hat_gesetzliche_rentenversicherung", self.testschema)
        self.assertEqual(str(ergebnis), "[]")

        ergebnis = self.testfirma.get_nutzer("M100001"). \
            abfrage_ausfuehren("SELECT * FROM hat_gesetzliche_arbeitslosenversicherung", self.testschema)
        self.assertEqual(str(ergebnis), "[]")

        ergebnis = self.testfirma.get_nutzer("M100001"). \
            abfrage_ausfuehren("SELECT * FROM arbeitet_in_sachsen", self.testschema)
        self.assertEqual(str(ergebnis), "[]")

        ergebnis = self.testfirma.get_nutzer("M100001"). \
            abfrage_ausfuehren("SELECT * FROM hat_x_kinder_unter_25", self.testschema)
        self.assertEqual(str(ergebnis), "[]")

        ergebnis = self.testfirma.get_nutzer("M100001"). \
            abfrage_ausfuehren("SELECT * FROM hat_gesetzliche_krankenversicherung", self.testschema)
        self.assertEqual(str(ergebnis), "[]")

        ergebnis = self.testfirma.get_nutzer("M100001"). \
            abfrage_ausfuehren("SELECT * FROM ist_in_gkv", self.testschema)
        self.assertEqual(str(ergebnis), "[]")

        ergebnis = self.testfirma.get_nutzer("M100001"). \
            abfrage_ausfuehren("SELECT * FROM in_gesellschaft", self.testschema)
        self.assertEqual(str(ergebnis), "[]")

        ergebnis = self.testfirma.get_nutzer("M100001"). \
            abfrage_ausfuehren("SELECT * FROM ist_mitarbeitertyp", self.testschema)
        self.assertEqual(str(ergebnis), "[]")

        ergebnis = self.testfirma.get_nutzer("M100001"). \
            abfrage_ausfuehren("SELECT * FROM hat_geschlecht", self.testschema)
        self.assertEqual(str(ergebnis), "[]")

        ergebnis = self.testfirma.get_nutzer("M100001"). \
            abfrage_ausfuehren("SELECT * FROM wohnt_in", self.testschema)
        self.assertEqual(str(ergebnis), "[]")

        ergebnis = self.testfirma.get_nutzer("M100001"). \
            abfrage_ausfuehren("SELECT * FROM hat_tarif", self.testschema)
        self.assertEqual(str(ergebnis), "[]")

        ergebnis = self.testfirma.get_nutzer("M100001"). \
            abfrage_ausfuehren("SELECT * FROM hat_jobtitel", self.testschema)
        self.assertEqual(str(ergebnis), "[]")

        ergebnis = self.testfirma.get_nutzer("M100001"). \
            abfrage_ausfuehren("SELECT * FROM eingesetzt_in", self.testschema)
        self.assertEqual(str(ergebnis), "[]")

        ergebnis = self.testfirma.get_nutzer("M100001"). \
            abfrage_ausfuehren("SELECT * FROM arbeitet_x_wochenstunden", self.testschema)
        self.assertEqual(str(ergebnis), "[]")

        ergebnis = self.testfirma.get_nutzer("M100001"). \
            abfrage_ausfuehren("SELECT * FROM in_steuerklasse", self.testschema)
        self.assertEqual(str(ergebnis), "[]")

    def test_erfolgreiche_entfernung_aussertariflicher_mitarbeiter(self):
        """
        Test prueft, ob Daten eines aussertariflichen Mitarbeiters aus Tabellen 'Aussertarifliche' und
        'hat_Verguetungsbestandteil_AT' entfernt wird. Auf die restlichen Tabellen kann verzichtet werden, da bereits
        im Test 'test_erfolgreiche_entfernung_gesetzlicher_sv_mitarbeiter' erfolgreich geprueft wurde, dass die
        Methode 'delete_mitarbeiterdaten' die Daten aus den anderen Assoziationstabellen und der Tabelle 'Mitarbeiter'
        entfernt
        """
        self.testfirma.get_nutzer("M100001"). \
            insert_neuer_mitarbeiter('testdaten_insert_mitarbeiter/Mitarbeiter - aussertariflich.xlsx', self.testschema)

        self.testfirma.get_nutzer("M100001"). \
            insert_aussertarifliches_verguetungsbestandteil('testdaten_insert_aussertarifliches_verguetungsbestandteil/'
                                                            'aussertariflicher Verguetungsbestandteil.xlsx',
                                                            self.testschema)

        # Inhalt aus Tabellen ziehen, um zu pruefen, ob der Datensatz angelegt wurde
        ergebnis = self.testfirma.get_nutzer("M100001"). \
            abfrage_ausfuehren("SELECT * FROM aussertarifliche", self.testschema)
        self.assertEqual(str(ergebnis), "[(1, 1, 1, datetime.date(2024, 1, 1), datetime.date(9999, 12, 31))]")

        ergebnis = self.testfirma.get_nutzer("M100001"). \
            abfrage_ausfuehren("SELECT * FROM hat_Verguetungsbestandteil_at", self.testschema)
        self.assertEqual(str(ergebnis), "[(1, 1, 1, Decimal('7648.15'), datetime.date(2024, 1, 1), "
                                        "datetime.date(9999, 12, 31))]")

        # Nun Entfernung des Mitarbeiters. Tabellen muessen von diesem Mitarbeiter nun wieder leer sein
        self.testfirma.get_nutzer("M100001").delete_mitarbeiterdaten("testdaten_delete_Mitarbeiterdaten/delete "
                                                                     "Personalnummer.xlsx",
                                                                     self.testschema)

        ergebnis = self.testfirma.get_nutzer("M100001"). \
            abfrage_ausfuehren("SELECT * FROM aussertarifliche", self.testschema)
        self.assertEqual(str(ergebnis), "[]")

        ergebnis = self.testfirma.get_nutzer("M100001"). \
            abfrage_ausfuehren("SELECT * FROM hat_Verguetungsbestandteil_at", self.testschema)
        self.assertEqual(str(ergebnis), "[]")

    def test_erfolgreiche_entfernung_minijob_mitarbeiter(self):
        """
        Test prueft, ob Daten eines Minijob-Mitarbeiters aus Tabellen 'ist_Minijobber' entfernt wird. Auf die restlichen
        Tabellen kann verzichtet werden, da bereits im Test 'test_erfolgreiche_entfernung_gesetzlicher_sv_mitarbeiter'
        erfolgreich geprueft wurde, dass die Methode 'delete_mitarbeiterdaten' die Daten aus den anderen
        Assoziationstabellen und der Tabelle 'Mitarbeiter' entfernt
        """
        self.testfirma.get_nutzer("M100001"). \
            insert_neuer_mitarbeiter('testdaten_insert_mitarbeiter/Mitarbeiter - Minijobber.xlsx', self.testschema)

        # Inhalt aus Tabellen ziehen, um zu pruefen, ob der Datensatz angelegt wurde
        ergebnis = self.testfirma.get_nutzer("M100001"). \
            abfrage_ausfuehren("SELECT * FROM ist_minijobber", self.testschema)
        self.assertEqual(str(ergebnis), "[(1, 1, 1, datetime.date(2024, 1, 1), datetime.date(9999, 12, 31))]")

        # Nun Entfernung des Mitarbeiters. Tabelle 'hat_Minijobber muss von diesem Mitarbeiter nun wieder leer sein
        self.testfirma.get_nutzer("M100001").delete_mitarbeiterdaten("testdaten_delete_Mitarbeiterdaten/delete "
                                                                     "Personalnummer.xlsx",
                                                                     self.testschema)

        ergebnis = self.testfirma.get_nutzer("M100001"). \
            abfrage_ausfuehren("SELECT * FROM ist_minijobber", self.testschema)
        self.assertEqual(str(ergebnis), "[]")

    def test_erfolgreiche_entfernung_privatversicherter_mitarbeiter(self):
        """
        Test prueft, ob Daten eines privat versicherten Mitarbeiters aus Tabelle 'hat_Privatkrankenkasse' entfernt wird.
        Auf die restlichen Tabellen kann verzichtet werden, da bereits im Test
        'test_erfolgreiche_entfernung_gesetzlicher_sv_mitarbeiter' erfolgreich geprueft wurde, dass die Methode
        'delete_mitarbeiterdaten' die Daten aus den anderen Assoziationstabellen und der Tabelle 'Mitarbeiter' entfernt.
        """
        self.testfirma.get_nutzer("M100001"). \
            insert_neuer_mitarbeiter('testdaten_insert_mitarbeiter/Mitarbeiter - privat versichert.xlsx',
                                     self.testschema)

        # Inhalt aus Tabellen ziehen, um zu pruefen, ob der Datensatz angelegt wurde
        ergebnis = self.testfirma.get_nutzer("M100001"). \
            abfrage_ausfuehren("SELECT * FROM hat_privatkrankenkasse", self.testschema)
        self.assertEqual(str(ergebnis), "[(1, 1, 1, Decimal('300.23'), Decimal('300.23'), datetime.date(2024, 1, 1), "
                                        "datetime.date(9999, 12, 31))]")

        # Nun Entfernung des Mitarbeiters. Tabelle 'hat_Minijobber muss von diesem Mitarbeiter nun wieder leer sein
        self.testfirma.get_nutzer("M100001").delete_mitarbeiterdaten("testdaten_delete_Mitarbeiterdaten/delete "
                                                                     "Personalnummer.xlsx",
                                                                     self.testschema)

        ergebnis = self.testfirma.get_nutzer("M100001"). \
            abfrage_ausfuehren("SELECT * FROM hat_privatkrankenkasse", self.testschema)
        self.assertEqual(str(ergebnis), "[]")

    def test_erfolgreiche_entfernung_anderweitig_versicherter_mitarbeiter(self):
        """
        Test prueft, ob Daten eines Minijob-Mitarbeiters aus Tabellen 'ist_Minijobber' und entfernt wird.
        Auf die restlichen Tabellen kann verzichtet werden, da bereits im Test
        'test_erfolgreiche_entfernung_gesetzlicher_sv_mitarbeiter' erfolgreich geprueft wurde, dass die Methode
        'delete_mitarbeiterdaten' die Daten aus den anderen Assoziationstabellen und der Tabelle 'Mitarbeiter'
        entfernt
        """
        self.testfirma.get_nutzer("M100001"). \
            insert_neuer_mitarbeiter('testdaten_insert_mitarbeiter/Mitarbeiter - anderweitig versichert.xlsx',
                                     self.testschema)

        # Inhalt aus Tabellen ziehen, um zu pruefen, ob der Datensatz angelegt wurde
        ergebnis = self.testfirma.get_nutzer("M100001"). \
            abfrage_ausfuehren("SELECT * FROM ist_anderweitig_versichert", self.testschema)
        self.assertEqual(str(ergebnis), "[(1, 1, 1, datetime.date(2024, 1, 1), datetime.date(9999, 12, 31))]")

        # Nun Entfernung des Mitarbeiters. Tabelle 'hat_Minijobber muss von diesem Mitarbeiter nun wieder leer sein
        self.testfirma.get_nutzer("M100001").delete_mitarbeiterdaten("testdaten_delete_Mitarbeiterdaten/delete "
                                                                     "Personalnummer.xlsx",
                                                                     self.testschema)

        ergebnis = self.testfirma.get_nutzer("M100001"). \
            abfrage_ausfuehren("SELECT * FROM ist_anderweitig_versichert", self.testschema)
        self.assertEqual(str(ergebnis), "[]")

    def test_mitarbeiter_existiert_nicht(self):
        """
        Test prueft, ob eine Exception geworfen wird, wenn die Daten einer Personalnummer entfernt werden sollen,
        die nicht existiert.
        """
        with self.assertRaises(Exception) as context:
            self.testfirma.get_nutzer("M100001").delete_mitarbeiterdaten("testdaten_delete_Mitarbeiterdaten/delete "
                                                                         "Personalnummer - existiert nicht.xlsx",
                                                                         self.testschema)

        self.assertEqual(str(context.exception), "FEHLER:  Mitarbeiter 'M100003' existiert nicht!\n"
                                                 "CONTEXT:  PL/pgSQL-Funktion delete_mitarbeiterdaten(integer,character"
                                                 " varying) Zeile 14 bei RAISE\n")

    def tearDown(self):
        """
        Methode ruft Funktion 'test_tear_down' auf, welches das Datenbankschema 'temp_test_schema' mit allen Daten
        entfernt.
        """
        test_tear_down()
