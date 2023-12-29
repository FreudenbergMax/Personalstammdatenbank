import unittest
from src.main.Mandant import Mandant
from src.main.test_SetUp_TearDown import test_set_up, test_tear_down


class TestNutzerInsertVerguetungsbestandteil(unittest.TestCase):

    def setUp(self):
        """
        Methode ruft Funktion 'test_set_up' der Klasse 'test_SetUp_TearDown' (siehe Ordner 'main') auf, welches das
        Datenbankschema 'temp_test_schema' erstellt.
        """
        self.testschema = test_set_up()
        self.testfirma = Mandant('Testfirma', self.testschema)
        self.testfirma.nutzer_anlegen('M100001', 'Max', 'Mustermann', self.testschema)

        # Gewerkschaft und Tarif muessen anlegen, damit Verguetungsbestandteile mit Tarife verknuepft werden koennen
        self.testfirma.get_nutzer("M100001").insert_gewerkschaft('testdaten_insert_gewerkschaft/Gewerkschaft.xlsx',
                                                                 self.testschema)
        self.testfirma.get_nutzer("M100001").insert_tarif('testdaten_insert_tarif/Tarif.xlsx', self.testschema)

    def test_erfolgreicher_eintrag(self):
        """
        Test prueft, ob ein Verguetungsbestandteil eingetragen wird.
        """
        self.testfirma.get_nutzer("M100001").\
            insert_tarifliches_verguetungsbestandteil('testdaten_insert_verguetungsbestandteil/'
                                                      'Verguetungsbestandteil.xlsx',
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
        Test prueft, ob bei wiederholtem Aufruf der Methode 'insert_verguetungsbestandteil' mit demselben Verguetungs-
        bestandteil dieser nicht erneut eingetragen wird. Beim zweiten Eintrag muss eine Exception geworfen werden.
        Ausloeser ist der unique-constraint der Tabelle "Verguetungsbestandteile" der fuer jeden Mandanten die
        mehrmalige identische Eintragung desselben Verguetungsbestandteile und Auszahlungsmonats verbietet. Falls ein
        Verguetungsbestandteil aktualisiert werden soll, so muss eine update-Funktion ausgefuehrt werden (welche im
        Rahmen dieser Bachelorarbeit nicht implementiert wurde).
        """
        self.testfirma.get_nutzer("M100001"). \
            insert_tarifliches_verguetungsbestandteil('testdaten_insert_verguetungsbestandteil/'
                                                      'Verguetungsbestandteil.xlsx',
                                                      self.testschema)

        # Versuch, denselben Wert noch einmal einzutragen
        with self.assertRaises(Exception) as context:
            self.testfirma.get_nutzer("M100001"). \
                insert_tarifliches_verguetungsbestandteil('testdaten_insert_verguetungsbestandteil/'
                                                          'Verguetungsbestandteil.xlsx',
                                                          self.testschema)

        self.assertEqual(str(context.exception), "FEHLER:  Verguetungsbestandteil 'Grundgehalt' bereits vorhanden!\n"
                                                 "CONTEXT:  PL/pgSQL-Funktion insert_tarifliches_verguetungsbestandteil"
                                                 "(integer,character varying,character varying,character varying,"
                                                 "numeric,date) Zeile 32 bei RAISE\n")

        # Inhalte aus Tabellen ziehen, um zu pruefen, ob der Datensatz nur einmal angelegt wurde
        ergebnis = self.testfirma.get_nutzer("M100001").abfrage_ausfuehren("SELECT * FROM verguetungsbestandteile",
                                                                           self.testschema)
        self.assertEqual(str(ergebnis), "[(1, 1, 'Grundgehalt', 'jeden Monat')]")

        ergebnis = self.testfirma.get_nutzer("M100001").abfrage_ausfuehren("SELECT * FROM "
                                                                           "hat_Verguetungsbestandteil_Tarif",
                                                                           self.testschema)
        self.assertEqual(str(ergebnis), "[(1, 1, 1, Decimal('3330.18'), datetime.date(2023, 5, 1), "
                                        "datetime.date(9999, 12, 31))]")

    def test_kein_doppelter_eintrag_case_insensitive(self):
        """
        Test prueft, ob bei wiederholtem Aufruf der Methode 'insert_verguetungsbestandteil' mit demselben Verguetungs-
        bestandteil aber mit Kleinschreibung dieser dennoch nicht erneut eingetragen wird. Beim zweiten Eintrag muss
        eine Exception geworfen werden. Ausloeser ist der unique-constraint in Kombination mit dem unique-Index
        'verguetungsbestandteil_idx'. Falls ein Verguetungsbestandteil aktualisiert werden soll, so muss eine
        update-Funktion ausgefuehrt werden (welche im Rahmen dieser Bachelorarbeit nicht implementiert wurde).
        """
        self.testfirma.get_nutzer("M100001"). \
            insert_tarifliches_verguetungsbestandteil('testdaten_insert_verguetungsbestandteil/'
                                                      'Verguetungsbestandteil.xlsx',
                                                      self.testschema)

        # Versuch, denselben Wert noch einmal einzutragen
        with self.assertRaises(Exception) as context:
            self.testfirma.get_nutzer("M100001"). \
                insert_tarifliches_verguetungsbestandteil('testdaten_insert_verguetungsbestandteil/'
                                                          'Verguetungsbestandteil - Verguetungsbestandteil klein '
                                                          'geschrieben.xlsx',
                                                          self.testschema)

        self.assertEqual(str(context.exception), "FEHLER:  Verguetungsbestandteil 'grundgehalt' bereits vorhanden!\n"
                                                 "CONTEXT:  PL/pgSQL-Funktion insert_tarifliches_verguetungsbestandteil"
                                                 "(integer,character varying,character varying,character varying,"
                                                 "numeric,date) Zeile 32 bei RAISE\n")

        # Inhalte aus Tabellen ziehen, um zu pruefen, ob der Datensatz nur einmal angelegt wurde
        ergebnis = self.testfirma.get_nutzer("M100001").abfrage_ausfuehren("SELECT * FROM verguetungsbestandteile",
                                                                           self.testschema)
        self.assertEqual(str(ergebnis), "[(1, 1, 'Grundgehalt', 'jeden Monat')]")

        ergebnis = self.testfirma.get_nutzer("M100001").abfrage_ausfuehren("SELECT * FROM "
                                                                           "hat_Verguetungsbestandteil_Tarif",
                                                                           self.testschema)
        self.assertEqual(str(ergebnis), "[(1, 1, 1, Decimal('3330.18'), datetime.date(2023, 5, 1), "
                                        "datetime.date(9999, 12, 31))]")

    def test_erfolgreicher_eintrag_tarif_klein_geschrieben(self):
        """
        Test prueft, ob bei Aufruf der Methode 'insert_verguetungsbestandteil' ein Verguetungsbestandteil eingetragen
        wird, wenn der Tarif eine andere Grossschreibung hat, als in Tabelle 'Tarife' hinterlegt, aber ansonsten gleich
        geschrieben ist (in diesem Beispiel: "a5-1" statt wie in Tabelle 'Tarife' "A5-1").
        """
        self.testfirma.get_nutzer("M100001"). \
            insert_tarifliches_verguetungsbestandteil('testdaten_insert_verguetungsbestandteil/'
                                                      'Verguetungsbestandteil - Tarif klein geschrieben.xlsx',
                                                      self.testschema)

        # Inhalte aus Tabellen ziehen, um zu pruefen, ob der Datensatz nur einmal angelegt wurde
        ergebnis = self.testfirma.get_nutzer("M100001").abfrage_ausfuehren("SELECT * FROM verguetungsbestandteile",
                                                                           self.testschema)
        self.assertEqual(str(ergebnis), "[(1, 1, 'Grundgehalt', 'jeden Monat')]")

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
                insert_tarifliches_verguetungsbestandteil('testdaten_insert_verguetungsbestandteil/'
                                                          'Verguetungsbestandteil - nicht existenter Tarif.xlsx',
                                                          self.testschema)

        self.assertEqual(str(context.exception), "FEHLER:  Bitte erst Tarif 'E8' anlegen!\n"
                                                 "CONTEXT:  PL/pgSQL-Funktion insert_tarifliches_verguetungsbestandteil"
                                                 "(integer,character varying,character varying,character varying,"
                                                 "numeric,date) Zeile 22 bei RAISE\n")

        # Inhalt aus Tabelle ziehen, um zu pruefen, ob kein Datensatz angelegt wurde
        ergebnis = self.testfirma.get_nutzer("M100001").abfrage_ausfuehren("SELECT * FROM verguetungsbestandteile",
                                                                           self.testschema)
        self.assertEqual(str(ergebnis), "[]")

        ergebnis = self.testfirma.get_nutzer("M100001").abfrage_ausfuehren("SELECT * FROM "
                                                                           "hat_Verguetungsbestandteil_Tarif",
                                                                           self.testschema)
        self.assertEqual(str(ergebnis), "[]")

    def test_falscher_eintrag(self):
        """
        Test prueft, ob eine Exception geworfen wird, wenn die geforderte Rechtschreibung fuer den Auszahlungsmonat
        nicht eingehalten wird. Ausloeser der Exception ist der check-constraint, welcher in der Stored Procedure
        'insert_geschlecht' implementiert ist bzw. in der Tabelle 'Verguetungsbestandteile'.
        Hinweis: die Excel-Datei ist fuer gewoehnlich so praepariert, dass man nur die richtige Rechtschreibung
        eintragen kann. Dennoch soll getestet werden, ob im Ernstfall der constraint greift. Hierfuer wurde die Excel-
        Datei so umgestaltet, dass man auch falsch geschriebene Auszahlungamonate eintragen kann.
        """
        # Versuch, falsch geschriebenes Auszahlungsmonat 'in jedem Monat' einzutragen
        with self.assertRaises(Exception) as context:
            self.testfirma.get_nutzer("M100001"). \
                insert_tarifliches_verguetungsbestandteil('testdaten_insert_verguetungsbestandteil/'
                                                          'Verguetungsbestandteil - Auszahlungsmonat falsch.xlsx',
                                                          self.testschema)

        self.assertEqual(str(context.exception), "FEHLER:  Auszahlungsmonat 'in jedem Monat' nicht vorhanden! Bitte "
                                                 "waehlen Sie zwischen folgenden Moeglichkeiten: 'jeden Monat', "
                                                 "'Januar', 'Februar', 'Maerz', 'April', 'Mai', 'Juni', 'Juli', "
                                                 "'August', 'September', 'Oktober', 'November', 'Dezember'!\n"
                                                 "CONTEXT:  PL/pgSQL-Funktion insert_tarifliches_verguetungsbestandteil"
                                                 "(integer,character varying,character varying,character varying,"
                                                 "numeric,date) Zeile 34 bei RAISE\n")

        # Inhalt aus Tabelle ziehen, um zu pruefen, ob kein Datensatz angelegt wurde
        ergebnis = self.testfirma.get_nutzer("M100001").abfrage_ausfuehren("SELECT * FROM verguetungsbestandteile",
                                                                           self.testschema)
        self.assertEqual(str(ergebnis), "[]")

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
