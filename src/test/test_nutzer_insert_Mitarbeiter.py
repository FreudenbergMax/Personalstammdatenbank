import unittest

from src.main.Login import Login
from src.main.Mandant import Mandant
from src.main.test_SetUp_TearDown import test_set_up, test_tear_down


class TestNutzerInsertMitarbeiter(unittest.TestCase):

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

    def test_erfolgreicher_eintrag(self):
        """
        Test prueft, ob ein neuer Mitarbeiter angelegt wird.
        """
        self.nutzer.insert_neuer_mitarbeiter('testdaten_insert_mitarbeiter/Mitarbeiter.xlsx')

        # Inhalt aus Tabellen ziehen, um zu pruefen, ob der Datensatz angelegt wurde
        ergebnis = self.nutzer.abfrage_ausfuehren("SELECT * FROM mitarbeiter")
        self.assertEqual(str(ergebnis), "[(1, 1, 'M100002', 'Max', None, 'Mustermann', datetime.date(1992, 12, 12), "
                                        "datetime.date(2024, 1, 1), '11 111 111 111', '00 121292 F 00', "
                                        "'DE00 0000 0000 0000 0000 00', '0175 1234567', 'maxmustermann@web.de', "
                                        "'030 987654321', 'Mustermann@testfirma.de', datetime.date(9999, 12, 31), "
                                        "None, None)]")

        ergebnis = self.nutzer.abfrage_ausfuehren("SELECT * FROM hat_gesetzliche_rentenversicherung")
        self.assertEqual(str(ergebnis), "[(1, 1, 1, datetime.date(2024, 1, 1), datetime.date(9999, 12, 31))]")

        ergebnis = self.nutzer.abfrage_ausfuehren("SELECT * FROM hat_gesetzliche_arbeitslosenversicherung")
        self.assertEqual(str(ergebnis), "[(1, 1, 1, datetime.date(2024, 1, 1), datetime.date(9999, 12, 31))]")

        ergebnis = self.nutzer.abfrage_ausfuehren("SELECT * FROM arbeitet_in_sachsen")
        self.assertEqual(str(ergebnis), "[(1, 1, 1, datetime.date(2024, 1, 1), datetime.date(9999, 12, 31))]")

        ergebnis = self.nutzer.abfrage_ausfuehren("SELECT * FROM hat_x_kinder_unter_25")
        self.assertEqual(str(ergebnis), "[(1, 1, 1, datetime.date(2024, 1, 1), datetime.date(9999, 12, 31))]")

        ergebnis = self.nutzer.abfrage_ausfuehren("SELECT * FROM hat_gesetzliche_krankenversicherung")
        self.assertEqual(str(ergebnis), "[(1, 1, 1, datetime.date(2024, 1, 1), datetime.date(9999, 12, 31))]")

        ergebnis = self.nutzer.abfrage_ausfuehren("SELECT * FROM ist_in_gkv")
        self.assertEqual(str(ergebnis), "[(1, 1, 1, datetime.date(2024, 1, 1), datetime.date(9999, 12, 31))]")

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

        ergebnis = self.nutzer.abfrage_ausfuehren("SELECT * FROM in_gesellschaft")
        self.assertEqual(str(ergebnis), "[(1, 1, 1, datetime.date(2024, 1, 1), datetime.date(9999, 12, 31))]")

        ergebnis = self.nutzer.abfrage_ausfuehren("SELECT * FROM ist_mitarbeitertyp")
        self.assertEqual(str(ergebnis), "[(1, 1, 1, datetime.date(2024, 1, 1), datetime.date(9999, 12, 31))]")

        ergebnis = self.nutzer.abfrage_ausfuehren("SELECT * FROM hat_geschlecht")
        self.assertEqual(str(ergebnis), "[(1, 1, 1, datetime.date(2024, 1, 1), datetime.date(9999, 12, 31))]")

        ergebnis = self.nutzer.abfrage_ausfuehren("SELECT * FROM wohnt_in")
        self.assertEqual(str(ergebnis), "[(1, 1, 1, datetime.date(2024, 1, 1), datetime.date(9999, 12, 31))]")

        ergebnis = self.nutzer.abfrage_ausfuehren("SELECT * FROM hat_tarif")
        self.assertEqual(str(ergebnis), "[(1, 1, 1, datetime.date(2024, 1, 1), datetime.date(9999, 12, 31))]")

        # muss leer sein, da tariflich angestellt. Kann also nicht aussertariflich sein
        ergebnis = self.nutzer.abfrage_ausfuehren("SELECT * FROM aussertarifliche")
        self.assertEqual(str(ergebnis), "[]")

        ergebnis = self.nutzer.abfrage_ausfuehren("SELECT * FROM hat_jobtitel")
        self.assertEqual(str(ergebnis), "[(1, 1, 1, 1, datetime.date(2024, 1, 1), datetime.date(9999, 12, 31))]")

        ergebnis = self.nutzer.abfrage_ausfuehren("SELECT * FROM eingesetzt_in")
        self.assertEqual(str(ergebnis), "[(1, 1, 1, False, datetime.date(2024, 1, 1), datetime.date(9999, 12, 31))]")

        ergebnis = self.nutzer.abfrage_ausfuehren("SELECT * FROM arbeitet_x_wochenstunden")
        self.assertEqual(str(ergebnis), "[(1, 1, 1, datetime.date(2024, 1, 1), datetime.date(9999, 12, 31))]")

        ergebnis = self.nutzer.abfrage_ausfuehren("SELECT * FROM in_steuerklasse")
        self.assertEqual(str(ergebnis), "[(1, 1, 1, datetime.date(2024, 1, 1), datetime.date(9999, 12, 31))]")

    def test_kein_eintrag_gleicher_mitarbeiter(self):
        """
        Test prueft, ob eine Exception geworfen wird, wenn versucht wird, denselben Mitarbeiter mit derselben
        Personalnummer, zweimal einzutragen
        """
        self.nutzer.insert_neuer_mitarbeiter('testdaten_insert_mitarbeiter/Mitarbeiter.xlsx')

        with self.assertRaises(Exception) as context:
            self.nutzer.insert_neuer_mitarbeiter('testdaten_insert_mitarbeiter/Mitarbeiter.xlsx')

        expected_error_prefix = "FEHLER:  Personalnummer 'M100002' bereits vorhanden!"
        actual_error_message = str(context.exception)
        self.assertTrue(actual_error_message.startswith(expected_error_prefix))

        # Pruefen, ob es wirklich nur einen Datensatz mit der Personalnummer 'M100002' gibt
        ergebnis = self.nutzer.abfrage_ausfuehren("SELECT * FROM mitarbeiter")
        self.assertEqual(str(ergebnis), "[(1, 1, 'M100002', 'Max', None, 'Mustermann', datetime.date(1992, 12, 12), "
                                        "datetime.date(2024, 1, 1), '11 111 111 111', '00 121292 F 00', "
                                        "'DE00 0000 0000 0000 0000 00', '0175 1234567', 'maxmustermann@web.de', "
                                        "'030 987654321', 'Mustermann@testfirma.de', datetime.date(9999, 12, 31), "
                                        "None, None)]")

    def test_kein_eintrag_gleicher_mitarbeiter_personalnummer_klein_geschrieben(self):
        """
        Test prueft, ob eine Exception geworfen wird, wenn versucht wird, einen anderen Mitarbeiter mit einer bereits
        vorhandenen Personalnummer (aber klein geschrieben) anzulegen
        """
        self.nutzer.insert_neuer_mitarbeiter('testdaten_insert_mitarbeiter/Mitarbeiter.xlsx')

        with self.assertRaises(Exception) as context:
            self.nutzer.insert_neuer_mitarbeiter('testdaten_insert_mitarbeiter/'
                                                 'Mitarbeiter - Personalnummer klein geschrieben.xlsx')

        expected_error_prefix = "FEHLER:  Personalnummer 'm100002' bereits vorhanden!"
        actual_error_message = str(context.exception)

        self.assertTrue(actual_error_message.startswith(expected_error_prefix))

        # Pruefen, ob es wirklich nur einen Datensatz mit der Personalnummer 'M100002' gibt
        ergebnis = self.nutzer.abfrage_ausfuehren("SELECT * FROM mitarbeiter")
        self.assertEqual(str(ergebnis), "[(1, 1, 'M100002', 'Max', None, 'Mustermann', datetime.date(1992, 12, 12), "
                                        "datetime.date(2024, 1, 1), '11 111 111 111', '00 121292 F 00', "
                                        "'DE00 0000 0000 0000 0000 00', '0175 1234567', 'maxmustermann@web.de', "
                                        "'030 987654321', 'Mustermann@testfirma.de', datetime.date(9999, 12, 31), "
                                        "None, None)]")

    def test_Mitarbeiter_aussertariflich_erfolgreich_angelegt(self):
        """
        Test prueft, ob Mitarbeiter auch keinem Tarif zugeordnet wird, wenn er als Aussertariflicher angegeben wird
        """
        self.nutzer.insert_neuer_mitarbeiter('testdaten_insert_mitarbeiter/Mitarbeiter - aussertariflich.xlsx')

        # muss leer sein, da aussertariflich angestellt. Kann also nicht tariflich beschaeftigt sein
        ergebnis = self.nutzer.abfrage_ausfuehren("SELECT * FROM hat_tarif")
        self.assertEqual(str(ergebnis), "[]")

        ergebnis = self.nutzer.abfrage_ausfuehren("SELECT * FROM aussertarifliche")
        self.assertEqual(str(ergebnis), "[(1, 1, 1, datetime.date(2024, 1, 1), datetime.date(9999, 12, 31))]")

    def test_Mitarbeiter_Minijobber_erfolgreich_angelegt(self):
        """
        Test prueft, ob Mitarbeiter nicht als gesetzlich oder privat oder anderweitig versichert eingetragen ist,
        wenn er als Minijobber angegeben wird
        """
        self.nutzer.insert_neuer_mitarbeiter('testdaten_insert_mitarbeiter/Mitarbeiter - Minijobber.xlsx')

        ergebnis = self.nutzer.abfrage_ausfuehren("SELECT * FROM ist_Minijobber")
        self.assertEqual(str(ergebnis), "[(1, 1, 1, datetime.date(2024, 1, 1), datetime.date(9999, 12, 31))]")

        # muss leer sein, da als Minijobber angestellt. Kann also nicht ueber den Arbeitgeber gesetzlich versichert sein
        ergebnis = self.nutzer.abfrage_ausfuehren("SELECT * FROM ist_in_gkv")
        self.assertEqual(str(ergebnis), "[]")

        # muss leer sein, da als Minijobber angestellt. Kann also nicht ueber den Arbeitgeber privat versichert sein
        ergebnis = self.nutzer.abfrage_ausfuehren("SELECT * FROM hat_privatkrankenkasse")
        self.assertEqual(str(ergebnis), "[]")

        # muss leer sein, da Minijobber. Kann also nicht ueber den Arbeitgeber anderweitig versichert sein
        ergebnis = self.nutzer.abfrage_ausfuehren("SELECT * FROM ist_anderweitig_versichert")
        self.assertEqual(str(ergebnis), "[]")

        # muss leer sein, da Minijobber. Kann also nicht ueber den Arbeitgeber arbeitslosenversichert sein
        ergebnis = self.nutzer.abfrage_ausfuehren("SELECT * FROM hat_gesetzliche_arbeitslosenversicherung")
        self.assertEqual(str(ergebnis), "[]")

        # muss leer sein, da Minijobber. Kann also nicht ueber den Arbeitgeber rentenversichert sein
        ergebnis = self.nutzer.abfrage_ausfuehren("SELECT * FROM hat_gesetzliche_rentenversicherung")
        self.assertEqual(str(ergebnis), "[]")

    def test_mitarbeiter_zweifach_versichert(self):
        """
        Test prueft, ob eine Exception geworfen wird, wenn fehlerhafterweise angegeben wird, dass ein neuer Mitarbeiter
        gleichzeitig gesetzlich als auch privat versichert ist. Mitarbeiter kann nur gesetzlich ODER privat oder
        anderweitig versichert oder Minijobber sein.
        """
        with self.assertRaises(Exception) as context:
            self.nutzer.insert_neuer_mitarbeiter('testdaten_insert_mitarbeiter/'
                                                 'Mitarbeiter - unzulaessig gesetzlich und privat versichert.xlsx')

        self.assertEqual(str(context.exception), "Ein Mitarbeiter kann nur gesetzlich oder privat krankenversichert "
                                                 "oder Minijobber oder anderweitig versichert sein. Sie haben 2 Angaben"
                                                 " bejaht. Das ist falsch!")

    def test_minijobber_und_arbeitslosenversichert(self):
        """
        Test prueft, ob eine Exception geworfen wird, wenn fehlerhafterweise angegeben wird, dass ein neuer Mitarbeiter
        Minijobber und gleichzeitig ueber den Arbeitgeber arbeitslosenversichert ist. Das ist rechtlich nicht moeglich.
        """
        with self.assertRaises(Exception) as context:
            self.nutzer.insert_neuer_mitarbeiter('testdaten_insert_mitarbeiter/'
                                                 'Mitarbeiter - Minijobber und arbeitslosenversichert.xlsx')

        self.assertEqual(str(context.exception), "Ein Minijobber ist niemals ueber den Arbeitgeber arbeitslosen- und "
                                                 "rentenversichert!")

    def test_minijobber_und_rentenversichert(self):
        """
        Test prueft, ob eine Exception geworfen wird, wenn fehlerhafterweise angegeben wird, dass ein neuer Mitarbeiter
        Minijobber und gleichzeitig ueber den Arbeitgeber rentenversichert ist. Das ist rechtlich nicht moeglich.
        """
        with self.assertRaises(Exception) as context:
            self.nutzer.insert_neuer_mitarbeiter(
                'testdaten_insert_mitarbeiter/Mitarbeiter - Minijobber und rentenversichert.xlsx')

        self.assertEqual(str(context.exception), "Ein Minijobber ist niemals ueber den Arbeitgeber arbeitslosen- und "
                                                 "rentenversichert!")

    def test_kurzfristig_beschaeftigter_und_arbeitslosenversichert(self):
        """
        Test prueft, ob eine Exception geworfen wird, wenn fehlerhafterweise angegeben wird, dass ein neuer Mitarbeiter
        Minijobber und gleichzeitig ueber den Arbeitgeber arbeitslosenversichert ist. Das ist rechtlich nicht moeglich.
        """
        with self.assertRaises(Exception) as context:
            self.nutzer.insert_neuer_mitarbeiter(
                'testdaten_insert_mitarbeiter/Mitarbeiter - Kurzfristig Beschaeftigter und arbeitslosenversichert.xlsx')

        self.assertEqual(str(context.exception), "Ein kurzfristig Beschaeftigter ist niemals ueber den Arbeitgeber "
                                                 "arbeitslosen- und rentenversichert!")

    def test_kurzfristig_beschaeftigter_und_rentenversichert(self):
        """
        Test prueft, ob eine Exception geworfen wird, wenn fehlerhafterweise angegeben wird, dass ein neuer Mitarbeiter
        kurzfristig Beschaeftigter und gleichzeitig ueber den Arbeitgeber rentenversichert ist. Das ist rechtlich nicht
        moeglich.
        """
        with self.assertRaises(Exception) as context:
            self.nutzer.insert_neuer_mitarbeiter(
                'testdaten_insert_mitarbeiter/Mitarbeiter - Kurzfristig Beschaeftigter und rentenversichert.xlsx')

        self.assertEqual(str(context.exception), "Ein kurzfristig Beschaeftigter ist niemals ueber den Arbeitgeber "
                                                 "arbeitslosen- und rentenversichert!")

    def test_kurzfristig_beschaeftigter_gesetzlich_versichert(self):
        """
        Test prueft, ob eine Exception geworfen wird, wenn fehlerhafterweise angegeben wird, dass ein neuer Mitarbeiter
        kurzfristig beschaeftigt und gleichzeitig ueber den Arbeitgeber gesetzlich versichert ist. Das ist rechtlich
        nicht moeglich.
        """
        with self.assertRaises(Exception) as context:
            self.nutzer.insert_neuer_mitarbeiter('testdaten_insert_mitarbeiter/Mitarbeiter - '
                                                 'kurzfristig Beschaeftigter gesetzlich krankenversichert.xlsx')

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
            self.nutzer.insert_neuer_mitarbeiter('testdaten_insert_mitarbeiter/Mitarbeiter - '
                                                 'kurzfristig Beschaeftigter privat krankenversichert.xlsx')

        self.assertEqual(str(context.exception), "Sie haben angegeben, dass dieser Mitarbeiter kurzfristig beschaeftigt"
                                                 " und gleichzeitig bei Ihnen privat versichert ist und somit Anspruch "
                                                 "auf Arbeitgeberzuschuss hat. Das ist rechtlich nicht moeglich!")

    def test_Eintrag_trotz_fehlender_Daten(self):
        """
        Test prueft, ob es moeglich ist, einen neuen Mitarbeiter anzulegen, auch wenn noch nicht alle Daten vorliegen.
        In der Praxis liegen nach einer Jobzusage haeufig nur einige Daten des neuen Mitarbeiters vor (da sie
        fuer gewoehnlich bei der Bewerbung bereits angegeben werden) wie Personalnummer (da vom Arbeitgeber vergeben),
        Vorname, evtl. Zweitname, Nachname, Geburtsdatum, Eintrittsdatum, private E-Mail und Telefonnummer, Adresse
        und Geschlecht.

        Zudem sind fuer gewoehnlich bereits Mitarbeitertyp, Wochenarbeitsstunden, Abteilung, ob Mitarbeiter
        Fuehrungskraft ist, Jobtitel, Erfahrungsstufe, die Gesellschaft die Frage und ob Mitarbeiter tarifbeschaeftigt
        ist, da dies bereits in der Stellenausschreibung bzw. im Laufe der Vertragsverhandlungen bekannt ist.

        Speziell Sozialversicherungs- und Steuerdaten aber auch die IBAN werden fuer gewoehnlich erst nachgereicht. Es
        soll dennoch moeglich sein, die oben beschriebenen bereits vorhandenen Daten einzutragen.

        Fuer den Nachtrag sind update-Funktionen notwendig, die im Rahmen dieser Bachelorarbeit aber nicht implementiert
        werden.
        """
        self.nutzer.insert_neuer_mitarbeiter('testdaten_insert_mitarbeiter/Mitarbeiter - '
                                             'Daten nur teilweise bekannt.xlsx')

        # Optionale Daten in Tabelle 'Mitarbeiter' sind null
        ergebnis = self.nutzer.abfrage_ausfuehren("SELECT "
                                                  "    zweitname, "
                                                  "    steuernummer, "
                                                  "    sozialversicherungsnummer, "
                                                  "    iban, dienstliche_telefonnummer, "
                                                  "    dienstliche_emailadresse, "
                                                  "    befristet_bis, "
                                                  "    austrittsdatum, "
                                                  "    austrittsgrund_id "
                                                  "FROM "
                                                  "    mitarbeiter")
        self.assertEqual(str(ergebnis), "[(None, None, None, None, None, None, None, None, None)]")

        # Die nicht eingetragenen optionalen Daten in den Assoziationstabellen muessen dazu fuehren, dass diese
        # Assoziationen leer sind
        ergebnis = self.nutzer.abfrage_ausfuehren("SELECT * FROM in_steuerklasse")
        self.assertEqual(str(ergebnis), "[]")

        # Sozialversicherungen: damit ein Eintrag in die Datenbank erfolgt, muss genau eines der vier Werte true sein:
        # gesetzlich krankenversichert, privat krankenversichert, anderweitig versichert oder Minijob. In diesem
        # liegt eine gesetzliche Krankenversicheurng vor, allerdings liegt in keiner der SV eine Verknuepfung vor,
        # weil die Daten hierfuer noch nciht vorliegen
        ergebnis = self.nutzer.abfrage_ausfuehren("SELECT * FROM ist_in_gkv")
        self.assertEqual(str(ergebnis), "[]")

        ergebnis = self.nutzer.abfrage_ausfuehren("SELECT * FROM hat_gesetzliche_Krankenversicherung")
        self.assertEqual(str(ergebnis), "[]")

        ergebnis = self.nutzer.abfrage_ausfuehren("SELECT * FROM hat_x_kinder_unter_25")
        self.assertEqual(str(ergebnis), "[]")

        ergebnis = self.nutzer.abfrage_ausfuehren("SELECT * FROM arbeitet_in_sachsen")
        self.assertEqual(str(ergebnis), "[]")

        ergebnis = self.nutzer.abfrage_ausfuehren("SELECT * FROM hat_gesetzliche_arbeitslosenversicherung")
        self.assertEqual(str(ergebnis), "[]")

        ergebnis = self.nutzer.abfrage_ausfuehren("SELECT * FROM hat_gesetzliche_rentenversicherung")
        self.assertEqual(str(ergebnis), "[]")

        # Pruefung des Vorhandenseins der Pflichtdaten:
        ergebnis = self.nutzer.abfrage_ausfuehren("SELECT * FROM mitarbeiter")
        self.assertEqual(str(ergebnis), "[(1, 1, 'M100002', 'Max', None, 'Mustermann', datetime.date(1992, 12, 12), "
                                        "datetime.date(2024, 1, 1), None, None, None, '0175 1234567', "
                                        "'maxmustermann@web.de', None, None, None, None, None)]")

        ergebnis = self.nutzer.abfrage_ausfuehren("SELECT * FROM in_gesellschaft")
        self.assertEqual(str(ergebnis), "[(1, 1, 1, datetime.date(2024, 1, 1), datetime.date(9999, 12, 31))]")

        ergebnis = self.nutzer.abfrage_ausfuehren("SELECT * FROM ist_mitarbeitertyp")
        self.assertEqual(str(ergebnis), "[(1, 1, 1, datetime.date(2024, 1, 1), datetime.date(9999, 12, 31))]")

        ergebnis = self.nutzer.abfrage_ausfuehren("SELECT * FROM hat_geschlecht")
        self.assertEqual(str(ergebnis), "[(1, 1, 1, datetime.date(2024, 1, 1), datetime.date(9999, 12, 31))]")

        ergebnis = self.nutzer.abfrage_ausfuehren("SELECT * FROM wohnt_in")
        self.assertEqual(str(ergebnis), "[(1, 1, 1, datetime.date(2024, 1, 1), datetime.date(9999, 12, 31))]")

        ergebnis = self.nutzer.abfrage_ausfuehren("SELECT * FROM hat_tarif")
        self.assertEqual(str(ergebnis), "[(1, 1, 1, datetime.date(2024, 1, 1), datetime.date(9999, 12, 31))]")

        ergebnis = self.nutzer.abfrage_ausfuehren("SELECT * FROM hat_jobtitel")
        self.assertEqual(str(ergebnis), "[(1, 1, 1, 1, datetime.date(2024, 1, 1), datetime.date(9999, 12, 31))]")

        ergebnis = self.nutzer.abfrage_ausfuehren("SELECT * FROM eingesetzt_in")
        self.assertEqual(str(ergebnis), "[(1, 1, 1, False, datetime.date(2024, 1, 1), datetime.date(9999, 12, 31))]")

        ergebnis = self.nutzer.abfrage_ausfuehren("SELECT * FROM arbeitet_x_wochenstunden")
        self.assertEqual(str(ergebnis), "[(1, 1, 1, datetime.date(2024, 1, 1), datetime.date(9999, 12, 31))]")

    def tearDown(self):
        """
        Methode ruft Funktion 'test_tear_down' auf, welches das Datenbankschema 'temp_test_schema' mit allen Daten
        entfernt.
        """
        test_tear_down()
