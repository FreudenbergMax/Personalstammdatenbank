import unittest
from src.main.Mandant import Mandant
from src.main.test_SetUp_TearDown import test_set_up, test_tear_down


class TestNutzerInsertMitarbeiter(unittest.TestCase):

    def setUp(self):
        """
        Methode ruft Funktion 'test_set_up' der Klasse 'test_SetUp_TearDown' (siehe Ordner 'main') auf, welches das
        Datenbankschema 'temp_test_schema' erstellt.
        """
        self.testschema = test_set_up()
        self.testfirma = Mandant('Testfirma', self.testschema)
        self.testfirma.nutzer_anlegen('M100001', 'Max', 'Mustermann', self.testschema)

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
        self.testfirma.get_nutzer("M100001").insert_tarifliches_verguetungsbestandteil(
            'testdaten_insert_verguetungsbestandteil/Verguetungsbestandteil.xlsx', self.testschema)

    def test_erfolgreicher_eintrag(self):
        """
        Test prueft, ob eine Abteilung eingetragen wird.
        """
        self.testfirma.get_nutzer("M100001").\
            insert_neuer_mitarbeiter('testdaten_insert_mitarbeiter/Mitarbeiter.xlsx', self.testschema)

        # Inhalt aus Tabellen ziehen, um zu pruefen, ob der Datensatz angelegt wurde
        ergebnis = self.testfirma.get_nutzer("M100001").\
            abfrage_ausfuehren("SELECT * FROM mitarbeiter", self.testschema)
        self.assertEqual(str(ergebnis), "[(1, 1, 'M100001', 'Max', None, 'Mustermann', datetime.date(1992, 12, 12), "
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

        # muss leer sein, da tariflich angestellt. Kann also nicht aussertariflich sein
        ergebnis = self.testfirma.get_nutzer("M100001"). \
            abfrage_ausfuehren("SELECT * FROM aussertarifliche", self.testschema)
        self.assertEqual(str(ergebnis), "[]")

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

    def test_Mitarbeiter_aussertariflich_erfolgreich_angelegt(self):
        """
        Test prueft, ob Mitarbeiter auch keinem Tarif zugeordnet wird, wenn er als Aussertariflicher angegeben wird
        """
        self.testfirma.get_nutzer("M100001"). \
            insert_neuer_mitarbeiter('testdaten_insert_mitarbeiter/Mitarbeiter - aussertariflich.xlsx', self.testschema)

        # muss leer sein, da aussertariflich angestellt. Kann also nicht tariflich beschaeftigt sein
        ergebnis = self.testfirma.get_nutzer("M100001"). \
            abfrage_ausfuehren("SELECT * FROM hat_tarif", self.testschema)
        self.assertEqual(str(ergebnis), "[]")

        ergebnis = self.testfirma.get_nutzer("M100001"). \
            abfrage_ausfuehren("SELECT * FROM aussertarifliche", self.testschema)
        self.assertEqual(str(ergebnis), "[(1, 1, 1, datetime.date(2024, 1, 1), datetime.date(9999, 12, 31))]")

    def test_Mitarbeiter_Minijobber_erfolgreich_angelegt(self):
        """
        Test prueft, ob Mitarbeiter nicht als gesetzlich oder privat oder anderweitig versichert eingetragen ist,
        wenn er als Minijobber angegeben wird
        """
        self.testfirma.get_nutzer("M100001"). \
            insert_neuer_mitarbeiter('testdaten_insert_mitarbeiter/Mitarbeiter - Minijobber.xlsx', self.testschema)

        ergebnis = self.testfirma.get_nutzer("M100001"). \
            abfrage_ausfuehren("SELECT * FROM ist_Minijobber", self.testschema)
        self.assertEqual(str(ergebnis), "[(1, 1, 1, datetime.date(2024, 1, 1), datetime.date(9999, 12, 31))]")

        # muss leer sein, da als Minijobber angestellt. Kann also nicht ueber den Arbeitgeber gesetzlich versichert sein
        ergebnis = self.testfirma.get_nutzer("M100001"). \
            abfrage_ausfuehren("SELECT * FROM ist_in_gkv", self.testschema)
        self.assertEqual(str(ergebnis), "[]")

        # muss leer sein, da als Minijobber angestellt. Kann also nicht ueber den Arbeitgeber privat versichert sein
        ergebnis = self.testfirma.get_nutzer("M100001"). \
            abfrage_ausfuehren("SELECT * FROM hat_privatkrankenkasse", self.testschema)
        self.assertEqual(str(ergebnis), "[]")

        # muss leer sein, da Minijobber. Kann also nicht ueber den Arbeitgeber anderweitig versichert sein
        ergebnis = self.testfirma.get_nutzer("M100001"). \
            abfrage_ausfuehren("SELECT * FROM ist_anderweitig_versichert", self.testschema)
        self.assertEqual(str(ergebnis), "[]")

        # muss leer sein, da Minijobber. Kann also nicht ueber den Arbeitgeber arbeitslosenversichert sein
        ergebnis = self.testfirma.get_nutzer("M100001"). \
            abfrage_ausfuehren("SELECT * FROM hat_gesetzliche_arbeitslosenversicherung", self.testschema)
        self.assertEqual(str(ergebnis), "[]")

        # muss leer sein, da Minijobber. Kann also nicht ueber den Arbeitgeber rentenversichert sein
        ergebnis = self.testfirma.get_nutzer("M100001"). \
            abfrage_ausfuehren("SELECT * FROM hat_gesetzliche_rentenversicherung", self.testschema)
        self.assertEqual(str(ergebnis), "[]")

    def test_mitarbeiter_zweifach_versichert(self):
        """
        Test prueft, ob eine Exception geworfen wird, wenn fehlerhafterweise angegeben wird, dass ein neuer Mitarbeiter
        gleichzeitig gesetzlich als auch privat versichert ist. Mitarbeiter kann nur gesetzlich ODER privat oder
        anderweitig versichert oder Minijobber sein.
        """
        with self.assertRaises(Exception) as context:
            self.testfirma.get_nutzer("M100001").\
                insert_neuer_mitarbeiter('testdaten_insert_mitarbeiter/'
                                         'Mitarbeiter - unzulaessig gesetzlich und privat versichert.xlsx',
                                         self.testschema)

        self.assertEqual(str(context.exception), "Ein Mitarbeiter kann nur gesetzlich oder privat krankenversichert "
                                                 "oder Minijobber oder anderweitig versichert sein. Sie haben 2 Angaben"
                                                 " bejaht. Das ist falsch!")

    def test_minijobber_und_arbeitslosenversichert(self):
        """
        Test prueft, ob eine Exception geworfen wird, wenn fehlerhafterweise angegeben wird, dass ein neuer Mitarbeiter
        Minijobber und gleichzeitig ueber den Arbeitgeber arbeitslosenversichert ist. Das ist rechtlich nicht moeglich.
        """
        with self.assertRaises(Exception) as context:
            self.testfirma.get_nutzer("M100001").\
                insert_neuer_mitarbeiter('testdaten_insert_mitarbeiter/'
                                         'Mitarbeiter - Minijobber und arbeitslosenversichert.xlsx',
                                         self.testschema)

        self.assertEqual(str(context.exception), "Ein Minijobber ist niemals ueber den Arbeitgeber arbeitslosen- und "
                                                 "rentenversichert!")

    def test_minijobber_und_rentenversichert(self):
        """
        Test prueft, ob eine Exception geworfen wird, wenn fehlerhafterweise angegeben wird, dass ein neuer Mitarbeiter
        Minijobber und gleichzeitig ueber den Arbeitgeber rentenversichert ist. Das ist rechtlich nicht moeglich.
        """
        with self.assertRaises(Exception) as context:
            self.testfirma.get_nutzer("M100001").\
                insert_neuer_mitarbeiter('testdaten_insert_mitarbeiter/'
                                         'Mitarbeiter - Minijobber und rentenversichert.xlsx',
                                         self.testschema)

        self.assertEqual(str(context.exception), "Ein Minijobber ist niemals ueber den Arbeitgeber arbeitslosen- und "
                                                 "rentenversichert!")

    def test_kurzfristig_beschaeftigter_und_arbeitslosenversichert(self):
        """
        Test prueft, ob eine Exception geworfen wird, wenn fehlerhafterweise angegeben wird, dass ein neuer Mitarbeiter
        Minijobber und gleichzeitig ueber den Arbeitgeber arbeitslosenversichert ist. Das ist rechtlich nicht moeglich.
        """
        with self.assertRaises(Exception) as context:
            self.testfirma.get_nutzer("M100001").\
                insert_neuer_mitarbeiter('testdaten_insert_mitarbeiter/'
                                         'Mitarbeiter - Kurzfristig Beschaeftigter und arbeitslosenversichert.xlsx',
                                         self.testschema)

        self.assertEqual(str(context.exception), "Ein kurzfristig Beschaeftigter ist niemals ueber den Arbeitgeber "
                                                 "arbeitslosen- und rentenversichert!")

    def test_kurzfristig_beschaeftigter_und_rentenversichert(self):
        """
        Test prueft, ob eine Exception geworfen wird, wenn fehlerhafterweise angegeben wird, dass ein neuer Mitarbeiter
        kurzfristig Beschaeftigter und gleichzeitig ueber den Arbeitgeber rentenversichert ist. Das ist rechtlich nicht
        moeglich.
        """
        with self.assertRaises(Exception) as context:
            self.testfirma.get_nutzer("M100001").\
                insert_neuer_mitarbeiter('testdaten_insert_mitarbeiter/'
                                         'Mitarbeiter - Kurzfristig Beschaeftigter und rentenversichert.xlsx',
                                         self.testschema)

        self.assertEqual(str(context.exception), "Ein kurzfristig Beschaeftigter ist niemals ueber den Arbeitgeber "
                                                 "arbeitslosen- und rentenversichert!")

    def test_kurzfristig_beschaeftigter_gesetzlich_versichert(self):
        """
        Test prueft, ob eine Exception geworfen wird, wenn fehlerhafterweise angegeben wird, dass ein neuer Mitarbeiter
        kurzfristig beschaeftigt und gleichzeitig ueber den Arbeitgeber gesetzlich versichert ist. Das ist rechtlich
        nicht moeglich.
        """
        with self.assertRaises(Exception) as context:
            self.testfirma.get_nutzer("M100001").\
                insert_neuer_mitarbeiter('testdaten_insert_mitarbeiter/Mitarbeiter - '
                                         'kurzfristig Beschaeftigter gesetzlich krankenversichert.xlsx',
                                         self.testschema)

        self.assertEqual(str(context.exception), "Sie haben angegeben, dass dieser Mitarbeiter kurzfristig beschaeftigt"
                                                 " und gleichzeitig bei Ihnen gesetzlich versichert ist. Das ist "
                                                 "rechtlich nicht moeglich!")

    def test_kurzfristig_beschaeftigter_privat_versichert(self):
        """
        Test prueft, ob eine Exception geworfen wird, wenn fehlerhafterweise angegeben wird, dass ein neuer Mitarbeiter
        kurzfristig beschaeftigt und gleichzeitig ueber den Arbeitgeber gesetzlich versichert ist. Das ist rechtlich
        nicht moeglich.
        """
        with self.assertRaises(Exception) as context:
            self.testfirma.get_nutzer("M100001").\
                insert_neuer_mitarbeiter('testdaten_insert_mitarbeiter/Mitarbeiter - '
                                         'kurzfristig Beschaeftigter privat krankenversichert.xlsx',
                                         self.testschema)

        self.assertEqual(str(context.exception), "Sie haben angegeben, dass dieser Mitarbeiter kurzfristig beschaeftigt"
                                                 " und gleichzeitig bei Ihnen privat versichert ist und somit Anspruch "
                                                 "auf Arbeitgeberzuschuss hat. Das ist rechtlich nicht moeglich!")

    def tearDown(self):
        """
        Methode ruft Funktion 'test_tear_down' auf, welches das Datenbankschema 'temp_test_schema' mit allen Daten
        entfernt.
        """
        test_tear_down()
