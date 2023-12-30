import unittest
from src.main.Mandant import Mandant
from src.main.test_SetUp_TearDown import test_set_up, test_tear_down


class TestNutzerUpdateAdresse(unittest.TestCase):

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
        Test prueft, ob eine Abteilung eingetragen wird.
        """
        self.testfirma.get_nutzer("M100001").\
            update_adresse('testdaten_update_adresse/Update Adresse.xlsx', self.testschema)

        # pruefen, ob neue Adressdaten eingetragen und mit Mitarbeiter verknuepft ist
        ergebnis = self.testfirma.get_nutzer("M100001").abfrage_ausfuehren("SELECT * FROM laender", self.testschema)
        self.assertEqual(str(ergebnis), "[(1, 1, 'Deutschland')]")

        ergebnis = self.testfirma.get_nutzer("M100001").abfrage_ausfuehren("SELECT * FROM regionen", self.testschema)
        self.assertEqual(str(ergebnis), "[(2, 1, 'Berlin', 1), (1, 1, 'Brandenburg', 1)]")

        ergebnis = self.testfirma.get_nutzer("M100001").abfrage_ausfuehren("SELECT * FROM staedte", self.testschema)
        self.assertEqual(str(ergebnis), "[(2, 1, 'Berlin', 2), (1, 1, 'Bernau', 1)]")

        ergebnis = self.testfirma.get_nutzer("M100001").abfrage_ausfuehren("SELECT * FROM postleitzahlen",
                                                                           self.testschema)
        self.assertEqual(str(ergebnis), "[(1, 1, '12358', 'Ost', 1), (2, 1, '10369', 'Ost', 2)]")

        ergebnis = self.testfirma.get_nutzer("M100001").abfrage_ausfuehren("SELECT * FROM strassenbezeichnungen",
                                                                           self.testschema)
        self.assertEqual(str(ergebnis), "[(1, 1, 'Musterstraße', '1', 1), (2, 1, 'neue Straße', '42', 2)]")

        ergebnis = self.testfirma.get_nutzer("M100001").abfrage_ausfuehren("SELECT * FROM wohnt_in",
                                                                           self.testschema)
        self.assertEqual(str(ergebnis), "[(1, 1, 1, datetime.date(2024, 1, 1), datetime.date(2026, 12, 31)), "
                                        "(1, 2, 1, datetime.date(2027, 1, 1), datetime.date(9999, 12, 31))]")

    def test_kein_doppelter_eintrag(self):
        """
        Test prueft, ob bei einem wiederholtem Adress-Update mit exakt denselben Daten fuer denselben Mitarbeiter
        eine exception geworfen wird. Ausloeser ist der unique-constraint der Tabelle 'wohnt_in' der verhindern soll,
        dass ein Mitarbeiter gleichzeitig zwei Wohnsitze hat.
        """
        self.testfirma.get_nutzer("M100001").update_adresse('testdaten_update_adresse/Update Adresse.xlsx',
                                                            self.testschema)

        # Versuch, denselben Wert noch einmal einzutragen
        with self.assertRaises(Exception) as context:
            self.testfirma.get_nutzer("M100001").update_adresse('testdaten_update_adresse/Update Adresse.xlsx',
                                                                self.testschema)

        self.assertEqual(str(context.exception), "FEHLER:  Mitarbeiter 'M100002' bereits seit diesem Datum unter der "
                                                 "Adresse gemeldet!\n"
                                                 "CONTEXT:  PL/pgSQL-Funktion update_adresse(integer,character varying,"
                                                 "date,date,character varying,character varying,character varying,"
                                                 "character varying,character varying,character varying,character "
                                                 "varying) Zeile 34 bei RAISE\n")

        # Inhalt aus Tabelle ziehen, um zu pruefen, ob der Datensatz nur einmal angelegt wurde
        ergebnis = self.testfirma.get_nutzer("M100001").abfrage_ausfuehren("SELECT * FROM wohnt_in", self.testschema)
        self.assertEqual(str(ergebnis), "[(1, 1, 1, datetime.date(2024, 1, 1), datetime.date(2026, 12, 31)), "
                                        "(1, 2, 1, datetime.date(2027, 1, 1), datetime.date(9999, 12, 31))]")

    def test_kein_doppelter_eintrag_adresse_case_insensitive(self):
        """
        Test prueft, ob neue Eintraege fuer Land, Region, Stadt, Strasse, Hausnummer und Personalnummer in
        Kleinschreibung angelegt werden, wenn diese bereits in Grossschreibung vorhanden ist. In dem Fall soll kein
        neuer Eintrag durchgefuehrt werden.
        """
        self.testfirma.get_nutzer("M100001").update_adresse('testdaten_update_adresse/Update Adresse - '
                                                            'alles klein geschrieben.xlsx',
                                                            self.testschema)

        # pruefen, ob neue Adressdaten in Kleinschriebung nicht eingetragen wurden, da bereits in Grossschreibung da
        ergebnis = self.testfirma.get_nutzer("M100001").abfrage_ausfuehren("SELECT * FROM laender", self.testschema)
        self.assertEqual(str(ergebnis), "[(1, 1, 'Deutschland')]")

        ergebnis = self.testfirma.get_nutzer("M100001").abfrage_ausfuehren("SELECT * FROM regionen", self.testschema)
        self.assertEqual(str(ergebnis), "[(1, 1, 'Brandenburg', 1)]")

        ergebnis = self.testfirma.get_nutzer("M100001").abfrage_ausfuehren("SELECT * FROM staedte", self.testschema)
        self.assertEqual(str(ergebnis), "[(1, 1, 'Bernau', 1)]")

        ergebnis = self.testfirma.get_nutzer("M100001").abfrage_ausfuehren("SELECT * FROM postleitzahlen",
                                                                           self.testschema)
        self.assertEqual(str(ergebnis), "[(1, 1, '12358', 'Ost', 1)]")

        ergebnis = self.testfirma.get_nutzer("M100001").abfrage_ausfuehren("SELECT * FROM strassenbezeichnungen",
                                                                           self.testschema)
        self.assertEqual(str(ergebnis), "[(1, 1, 'Musterstraße', '1', 1)]")

        ergebnis = self.testfirma.get_nutzer("M100001").abfrage_ausfuehren("SELECT * FROM wohnt_in",
                                                                           self.testschema)
        self.assertEqual(str(ergebnis), "[(1, 1, 1, datetime.date(2024, 1, 1), datetime.date(2026, 12, 31)), "
                                        "(1, 1, 1, datetime.date(2027, 1, 1), datetime.date(9999, 12, 31))]")

    def test_mitarbeiter_existiert_nicht(self):
        """
        Test prueft, ob eine Exception geworfen wird, wenn der Adress-Update fuer eine Person vorgenommen wird,
        die in der Datenbank nicht existiert
        """
        with self.assertRaises(Exception) as context:
            self.testfirma.get_nutzer("M100001").update_adresse('testdaten_update_adresse/Update Adresse - Mitarbeiter '
                                                                'existiert nicht.xlsx', self.testschema)

        self.assertEqual(str(context.exception), "FEHLER:  Mitarbeiter 'M100003' existiert nicht!\n"
                                                 "CONTEXT:  PL/pgSQL-Funktion update_adresse(integer,character varying,"
                                                 "date,date,character varying,character varying,character varying,"
                                                 "character varying,character varying,character varying,character "
                                                 "varying) Zeile 14 bei RAISE\n")

    def tearDown(self):
        """
        Methode ruft Funktion 'test_tear_down' auf, welches das Datenbankschema 'temp_test_schema' mit allen Daten
        entfernt.
        """
        test_tear_down()
