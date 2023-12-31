import unittest
from src.main.Mandant import Mandant
from src.main.test_SetUp_TearDown import test_set_up, test_tear_down


class TestNutzerInsertAussertariflicherVerguetungsbestandteil(unittest.TestCase):

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

        self.testfirma.get_nutzer("M100001").insert_verguetungsbestandteil(
            'testdaten_insert_verguetungsbestandteil/Verguetungsbestandteil.xlsx', self.testschema)

        # Mitarbeiter einfuegen
        self.testfirma.get_nutzer("M100001"). \
            insert_neuer_mitarbeiter('testdaten_insert_mitarbeiter/Mitarbeiter - aussertariflich.xlsx', self.testschema)

    def test_erfolgreicher_eintrag(self):
        """
        Test prueft, ob ein Verguetungsbestandteil eingetragen wird.
        """
        self.testfirma.get_nutzer("M100001").\
            insert_aussertarifliches_verguetungsbestandteil('testdaten_insert_aussertarifliches_verguetungsbestandteil/'
                                                            'aussertariflicher Verguetungsbestandteil.xlsx',
                                                            self.testschema)

        # Inhalte aus Tabellen ziehen, um zu pruefen, ob der Datensatz angelegt wurde
        ergebnis = self.testfirma.get_nutzer("M100001").abfrage_ausfuehren("SELECT * FROM verguetungsbestandteile",
                                                                           self.testschema)
        self.assertEqual(str(ergebnis), "[(1, 1, 'Grundgehalt', 'jeden Monat')]")

        # Pruefen, ob Daten eingetragen wurden
        ergebnis = self.testfirma.get_nutzer("M100001").abfrage_ausfuehren("SELECT * FROM "
                                                                           "hat_verguetungsbestandteil_at",
                                                                           self.testschema)
        self.assertEqual(str(ergebnis), "[(1, 1, 1, Decimal('7648.15'), datetime.date(2024, 1, 1), "
                                        "datetime.date(9999, 12, 31))]")

    def test_kein_doppelter_eintrag(self):
        """
        Test prueft, ob bei wiederholtem Aufruf der Methode 'insert_aussertarifliches_verguetungsbestandteil' mit
        demselben Verguetungsbestandteil fuer einen aussertariflichen Mitarbeiter dieser nicht erneut eingetragen wird.
        Beim zweiten Eintrag muss eine Exception geworfen werden. Ausloeser ist der unique-constraint der Tabelle
        "hat_Verguetungsbestandteil_AT" der fuer jeden Mandanten die mehrmalige identische Eintragung desselben
        Verguetungsbestandteils fuer einen aussertariflichen Mitarbeiter verbietet. Falls der Verguetungsbestandteil
        fuer einen aussertariflichen Mitarbeiter aktualisiert werden soll, so muss eine update-Funktion ausgefuehrt
        werden (welche im Rahmen dieser Bachelorarbeit nicht implementiert wurde).
        """
        self.testfirma.get_nutzer("M100001"). \
            insert_aussertarifliches_verguetungsbestandteil('testdaten_insert_aussertarifliches_verguetungsbestandteil/'
                                                            'aussertariflicher Verguetungsbestandteil.xlsx',
                                                            self.testschema)

        # Versuch, denselben Wert noch einmal einzutragen
        with self.assertRaises(Exception) as context:
            self.testfirma.get_nutzer("M100001").insert_aussertarifliches_verguetungsbestandteil(
                'testdaten_insert_aussertarifliches_verguetungsbestandteil/aussertariflicher '
                'Verguetungsbestandteil.xlsx', self.testschema)

        self.assertEqual(str(context.exception), "FEHLER:  Aussertariflicher Mitarbeiter 'M100002' hat bereits "
                                                 "aktuellen Verguetungsbestandteil 'Grundgehalt'!\n"
                                                 "CONTEXT:  PL/pgSQL-Funktion "
                                                 "insert_aussertarifliches_verguetungsbestandteil(integer,character "
                                                 "varying,character varying,numeric,date) Zeile 45 bei RAISE\n")

        # Pruefen, ob Daten nur einmal eingetragen wurden
        ergebnis = self.testfirma.get_nutzer("M100001").abfrage_ausfuehren("SELECT * FROM "
                                                                           "hat_verguetungsbestandteil_at",
                                                                           self.testschema)
        self.assertEqual(str(ergebnis), "[(1, 1, 1, Decimal('7648.15'), datetime.date(2024, 1, 1), "
                                        "datetime.date(9999, 12, 31))]")

    def test_erfolgreiche_eintraege_klein_geschrieben(self):
        """
        Test prueft, ob bei Aufruf der Methode 'insert_aussertarifliches_verguetungsbestandteil' eine Verknuepfung
        zwischen Verguetungsbestandteil und aussertariflichen Mitarbeiter eingetragen wird, wenn die Personalnummer eine
        andere Grossschreibung hat, als in Tabelle 'Mitarbeiter' hinterlegt, aber ansonsten gleich geschrieben ist
        (in diesem Beispiel: "m100002" statt wie in Tabelle 'Mitarbeiter' "M100002") und der Verguetungsbestandteil eine
        andere Grossschriebung hat, als in Tabelle 'Verguetungsbestandteile' hinterlegt, aber ansonsten gleich
        geschrieben ist (in diesem Beispiel: "grundgehalt" statt wie in Tabelle 'Verguetungsbestandteile' "Grundgehalt")
        """
        self.testfirma.get_nutzer("M100001"). \
            insert_aussertarifliches_verguetungsbestandteil('testdaten_insert_aussertarifliches_verguetungsbestandteil/'
                                                            'aussertariflicher Verguetungsbestandteil.xlsx',
                                                            self.testschema)

        # Pruefen, ob Daten eingetragen wurden
        ergebnis = self.testfirma.get_nutzer("M100001").abfrage_ausfuehren("SELECT * FROM "
                                                                           "hat_verguetungsbestandteil_at",
                                                                           self.testschema)
        self.assertEqual(str(ergebnis), "[(1, 1, 1, Decimal('7648.15'), datetime.date(2024, 1, 1), "
                                        "datetime.date(9999, 12, 31))]")

    def test_kein_eintrag_nicht_existenter_aussertariflicher_Mitarbeiter(self):
        """
        Test prueft, ob eine Exception geworfen wird, wenn der Verguetungsbestandteil zu einem Mitarbeiter zugeordnet
        wird, der zwar existiert, aber nicht aussertariflich ist, sondern tariflich eingruppiert ist.
        """
        # tariflichen Mitarbeiter einfuegen
        self.testfirma.get_nutzer("M100001").insert_gewerkschaft('testdaten_insert_gewerkschaft/Gewerkschaft.xlsx',
                                                                 self.testschema)
        self.testfirma.get_nutzer("M100001").insert_tarif('testdaten_insert_tarif/Tarif.xlsx', self.testschema)
        self.testfirma.get_nutzer("M100001").insert_tarifliches_verguetungsbestandteil(
            'testdaten_insert_tariflicher_verguetungsbestandteil/tariflicher Verguetungsbestandteil.xlsx',
            self.testschema)
        self.testfirma.get_nutzer("M100001"). \
            insert_neuer_mitarbeiter('testdaten_insert_mitarbeiter/Mitarbeiter 2.xlsx', self.testschema)

        with self.assertRaises(Exception) as context:
            self.testfirma.get_nutzer("M100001").insert_aussertarifliches_verguetungsbestandteil(
                'testdaten_insert_aussertarifliches_verguetungsbestandteil/aussertariflicher Verguetungsbestandteil - '
                'nicht existenter aussertariflicher Mitarbeiter.xlsx', self.testschema)

        self.assertEqual(str(context.exception), "FEHLER:  Mitarbeiter 'M100003' ist nicht als aussertariflicher "
                                                 "Beschaeftigter hinterlegt!\n"
                                                 "CONTEXT:  PL/pgSQL-Funktion "
                                                 "insert_aussertarifliches_verguetungsbestandteil(integer,character "
                                                 "varying,character varying,numeric,date) Zeile 35 bei RAISE\n")

        # Pruefen, ob auch tatsaechlich aufgrund fehlenden aussertariflichen Mitarbeiter kein Datensatz angelegt wurde
        ergebnis = self.testfirma.get_nutzer("M100001").abfrage_ausfuehren("SELECT * FROM "
                                                                           "hat_verguetungsbestandteil_at",
                                                                           self.testschema)
        self.assertEqual(str(ergebnis), "[]")

    def test_kein_eintrag_nicht_existenter_Mitarbeiter(self):
        """
        Test prueft, ob eine Exception geworfen wird, wenn der Verguetungsbestandteil zu einem aussertariflichen
        Mitarbeiter zugeordnet wird, die bisher nicht in der Datenbank eingetragen wurde.
        """
        with self.assertRaises(Exception) as context:
            self.testfirma.get_nutzer("M100001").insert_aussertarifliches_verguetungsbestandteil(
                'testdaten_insert_aussertarifliches_verguetungsbestandteil/aussertariflicher Verguetungsbestandteil - '
                'nicht existenter Mitarbeiter.xlsx', self.testschema)

        self.assertEqual(str(context.exception), "FEHLER:  Bitte erst Mitarbeiter 'M100004' anlegen!\n"
                                                 "CONTEXT:  PL/pgSQL-Funktion "
                                                 "insert_aussertarifliches_verguetungsbestandteil(integer,character "
                                                 "varying,character varying,numeric,date) Zeile 26 bei RAISE\n")

        # Pruefen, ob auch tatsaechlich aufgrund fehlenden Mitarbeiters kein Datensatz angelegt wurde
        ergebnis = self.testfirma.get_nutzer("M100001").abfrage_ausfuehren("SELECT * FROM "
                                                                           "hat_verguetungsbestandteil_at",
                                                                           self.testschema)
        self.assertEqual(str(ergebnis), "[]")

    def test_kein_eintrag_nicht_existenter_verguetungsbestandteil(self):
        """
        Test prueft, ob eine Exception geworfen wird, wenn ein aussertariflicher Mitarbeiter zu einem
        Verguetungsbestandteil zugeordnet wird, die bisher nicht in der Datenbank eingetragen wurde.
        """
        with self.assertRaises(Exception) as context:
            self.testfirma.get_nutzer("M100001").insert_aussertarifliches_verguetungsbestandteil(
                'testdaten_insert_aussertarifliches_verguetungsbestandteil/aussertariflicher Verguetungsbestandteil - '
                'nicht existenter Verguetungsbestandteil.xlsx', self.testschema)

        self.assertEqual(str(context.exception), "FEHLER:  Bitte erst Verguetungsbestandteil 'Bonus' anlegen!\n"
                                                 "CONTEXT:  PL/pgSQL-Funktion "
                                                 "insert_aussertarifliches_verguetungsbestandteil(integer,character "
                                                 "varying,character varying,numeric,date) Zeile 17 bei RAISE\n")

        # Pruefen, ob auch tatsaechlich aufgrund fehlenden Verguetungsbestandteils kein Datensatz angelegt wurde
        ergebnis = self.testfirma.get_nutzer("M100001").abfrage_ausfuehren("SELECT * FROM "
                                                                           "hat_verguetungsbestandteil_at",
                                                                           self.testschema)
        self.assertEqual(str(ergebnis), "[]")

    def tearDown(self):
        """
        Methode ruft Funktion 'test_tear_down' auf, welches das Datenbankschema 'temp_test_schema' mit allen Daten
        entfernt.
        """
        test_tear_down()
