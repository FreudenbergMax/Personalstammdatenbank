import unittest
from src.main.Mandant import Mandant
from src.main.test_SetUp_TearDown import test_set_up, test_tear_down


class TestNutzerInsertTariflicherVerguetungsbestandteil(unittest.TestCase):

    def setUp(self):
        """
        Methode ruft Funktion 'test_set_up' der Klasse 'test_SetUp_TearDown' (siehe Ordner 'main') auf, welches das
        Datenbankschema 'temp_test_schema' erstellt.
        """
        self.testschema = test_set_up()
        self.testfirma = Mandant('Testfirma', self.testschema)
        self.testfirma.nutzer_anlegen('M100001', 'Max', 'Mustermann', self.testschema)

        # Gewerkschaft, Tarif und Verguetungsbestandteil muessen angelegt sein, damit Verguetungsbestandteile mit Tarife
        # verknuepft werden koennen
        self.testfirma.get_nutzer("M100001").insert_gewerkschaft('testdaten_insert_gewerkschaft/Gewerkschaft.xlsx',
                                                                 self.testschema)
        self.testfirma.get_nutzer("M100001").insert_tarif('testdaten_insert_tarif/Tarif.xlsx', self.testschema)
        self.testfirma.get_nutzer("M100001").insert_verguetungsbestandteil(
            'testdaten_insert_verguetungsbestandteil/Verguetungsbestandteil.xlsx', self.testschema)

    def test_erfolgreicher_eintrag(self):
        """
        Test prueft, ob ein Verguetungsbestandteil eingetragen wird.
        """
        self.testfirma.get_nutzer("M100001").\
            insert_tarifliches_verguetungsbestandteil('testdaten_insert_tariflicher_verguetungsbestandteil/'
                                                      'tariflicher Verguetungsbestandteil.xlsx',
                                                      self.testschema)

        # Inhalte aus Tabellen ziehen, um zu pruefen, ob der Datensatz angelegt wurde
        ergebnis = self.testfirma.get_nutzer("M100001").abfrage_ausfuehren("SELECT * FROM verguetungsbestandteile",
                                                                           self.testschema)
        self.assertEqual(str(ergebnis), "[(1, 1, 'Grundgehalt', 'jeden Monat')]")

        ergebnis = self.testfirma.get_nutzer("M100001").abfrage_ausfuehren("SELECT * FROM "
                                                                           "hat_Verguetungsbestandteil_Tarif",
                                                                           self.testschema)
        self.assertEqual(str(ergebnis), "[(1, 1, 1, Decimal('3330.18'), datetime.date(2023, 5, 1), "
                                        "datetime.date(9999, 12, 31))]")

    def test_kein_doppelter_eintrag(self):
        """
        Test prueft, ob bei wiederholtem Aufruf der Methode 'insert_tariflicher_verguetungsbestandteil' mit demselben
        Verguetungsbestandteil fuer einen Tarif dieser nicht erneut eingetragen wird. Beim zweiten Eintrag muss eine
        Exception geworfen werden. Ausloeser ist der unique-constraint der Tabelle "hat_Verguetungsbestandteil_Tarif"
        der fuer jeden Mandanten die mehrmalige identische Eintragung desselben Verguetungsbestandteils fuer einen Tarif
        verbietet. Falls der Verguetungsbestandteil fuer einen Tarif aktualisiert werden soll, so muss eine
        update-Funktion ausgefuehrt werden (welche im Rahmen dieser Bachelorarbeit nicht implementiert wurde).
        """
        self.testfirma.get_nutzer("M100001"). \
            insert_tarifliches_verguetungsbestandteil('testdaten_insert_tariflicher_verguetungsbestandteil/'
                                                      'tariflicher Verguetungsbestandteil.xlsx',
                                                      self.testschema)

        # Versuch, denselben Wert noch einmal einzutragen
        with self.assertRaises(Exception) as context:
            self.testfirma.get_nutzer("M100001"). \
                insert_tarifliches_verguetungsbestandteil('testdaten_insert_tariflicher_verguetungsbestandteil/'
                                                          'tariflicher Verguetungsbestandteil.xlsx',
                                                          self.testschema)

        self.assertEqual(str(context.exception), "FEHLER:  Verguetungsbestandteil 'Grundgehalt' fuer Tarif 'A5-1' "
                                                 "bereits verknuepft!\n"
                                                 "CONTEXT:  PL/pgSQL-Funktion insert_tarifliches_verguetungsbestandteil"
                                                 "(integer,character varying,character varying,numeric,date) Zeile 35 "
                                                 "bei RAISE\n")

        # Inhalt aus Tabelle ziehen, um zu pruefen, ob der Datensatz nur einmal angelegt wurde
        ergebnis = self.testfirma.get_nutzer("M100001").abfrage_ausfuehren("SELECT * FROM "
                                                                           "hat_Verguetungsbestandteil_Tarif",
                                                                           self.testschema)
        self.assertEqual(str(ergebnis), "[(1, 1, 1, Decimal('3330.18'), datetime.date(2023, 5, 1), "
                                        "datetime.date(9999, 12, 31))]")

    def test_erfolgreicher_eintraege_klein_geschrieben(self):
        """
        Test prueft, ob bei Aufruf der Methode 'insert_tariflicher_verguetungsbestandteil' eine Verknuepfung zwischen
        Verguetungsbestandteil und Tarif eingetragen wird, wenn der Tarif eine andere Grossschreibung hat, als in
        Tabelle 'Tarife' hinterlegt, aber ansonsten gleich geschrieben ist (in diesem Beispiel: "a5-1" statt wie in
        Tabelle 'Tarife' "A5-1") und der Verguetungsbestandteil eine andere Grossschriebung hat, als in Tabelle
        'Verguetungsbestandteile' hinterlegt, aber ansonsten gleich geschrieben ist (in diesem Beispiel: "grundgehalt"
        statt wie in Tabelle 'Verguetungsbestandteile' "Grundgehalt")
        """
        self.testfirma.get_nutzer("M100001"). \
            insert_tarifliches_verguetungsbestandteil('testdaten_insert_tariflicher_verguetungsbestandteil/tariflicher '
                                                      'Verguetungsbestandteil - Eintraege klein geschrieben.xlsx',
                                                      self.testschema)

        # Inhalte aus Tabellen ziehen, um zu pruefen, ob der Datensatz nur einmal angelegt wurde
        ergebnis = self.testfirma.get_nutzer("M100001").abfrage_ausfuehren("SELECT * FROM "
                                                                           "hat_Verguetungsbestandteil_Tarif",
                                                                           self.testschema)
        self.assertEqual(str(ergebnis), "[(1, 1, 1, Decimal('3330.18'), datetime.date(2023, 5, 1), "
                                        "datetime.date(9999, 12, 31))]")

    def test_kein_eintrag_nicht_existenter_tarif(self):
        """
        Test prueft, ob eine Exception geworfen wird, wenn der Verguetungsbestandteil zu einem Tarif zugeordnet wird,
        die bisher nicht in der Datenbank eingetragen wurde.
        """
        with self.assertRaises(Exception) as context:
            self.testfirma.get_nutzer("M100001").\
                insert_tarifliches_verguetungsbestandteil('testdaten_insert_tariflicher_verguetungsbestandteil/'
                                                          'tariflicher Verguetungsbestandteil - nicht existenter '
                                                          'Tarif.xlsx', self.testschema)

        self.assertEqual(str(context.exception), "FEHLER:  Bitte erst Tarif 'E8' anlegen!\n"
                                                 "CONTEXT:  PL/pgSQL-Funktion insert_tarifliches_verguetungsbestandteil"
                                                 "(integer,character varying,character varying,numeric,date) Zeile 25 "
                                                 "bei RAISE\n")

        # Pruefen, ob auch tatsaechlich aufgrund fehlenden Tarifs kein Datensatz angelegt wurde
        ergebnis = self.testfirma.get_nutzer("M100001").abfrage_ausfuehren("SELECT * FROM "
                                                                           "hat_Verguetungsbestandteil_Tarif",
                                                                           self.testschema)
        self.assertEqual(str(ergebnis), "[]")

    def test_kein_eintrag_nicht_existenter_verguetungsbestandteil(self):
        """
        Test prueft, ob eine Exception geworfen wird, wenn ein Tarif zu einem Verguetungsbestandteil zugeordnet wird,
        die bisher nicht in der Datenbank eingetragen wurde.
        """
        with self.assertRaises(Exception) as context:
            self.testfirma.get_nutzer("M100001").\
                insert_tarifliches_verguetungsbestandteil('testdaten_insert_tariflicher_verguetungsbestandteil/'
                                                          'tariflicher Verguetungsbestandteil - nicht existenter '
                                                          'Verguetungsbestandteil.xlsx', self.testschema)

        self.assertEqual(str(context.exception), "FEHLER:  Bitte erst Verguetungsbestandteil 'Sonderzahlung' anlegen!\n"
                                                 "CONTEXT:  PL/pgSQL-Funktion insert_tarifliches_verguetungsbestandteil"
                                                 "(integer,character varying,character varying,numeric,date) Zeile 16 "
                                                 "bei RAISE\n")

        # Pruefen, ob auch tatsaechlich aufgrund fehlenden Tarifs kein Datensatz angelegt wurde
        ergebnis = self.testfirma.get_nutzer("M100001").abfrage_ausfuehren("SELECT * FROM "
                                                                           "hat_Verguetungsbestandteil_Tarif",
                                                                           self.testschema)
        self.assertEqual(str(ergebnis), "[]")

    def tearDown(self):
        """
        Methode ruft Funktion 'test_tear_down' auf, welches das Datenbankschema 'temp_test_schema' mit allen Daten
        entfernt.
        """
        test_tear_down()
