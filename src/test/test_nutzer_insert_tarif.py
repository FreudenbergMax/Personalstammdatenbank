import unittest
from src.main.Mandant import Mandant
from src.main.test_SetUp_TearDown import test_set_up, test_tear_down


class TestNutzerInsertTarif(unittest.TestCase):

    def setUp(self):
        """
        Methode ruft Funktion 'test_set_up' der Klasse 'test_SetUp_TearDown' (siehe Ordner 'main') auf, welches das
        Datenbankschema 'temp_test_schema' erstellt.
        """
        self.testschema = test_set_up()
        self.testfirma = Mandant('Testfirma', self.testschema)
        self.testfirma.nutzer_anlegen('M100001', 'Max', 'Mustermann', self.testschema)

        self.testfirma.get_nutzer("M100001"). \
            insert_gewerkschaft('testdaten_insert_gewerkschaft/Gewerkschaft.xlsx', self.testschema)

    def test_erfolgreicher_eintrag(self):
        """
        Test prueft, ob ein Tarif eingetragen wird.
        """
        self.testfirma.get_nutzer("M100001").insert_tarif('testdaten_insert_tarif/Tarif.xlsx', self.testschema)

        # Inhalt aus Tabelle ziehen, um zu pruefen, ob der Datensatz angelegt wurde
        ergebnis = self.testfirma.get_nutzer("M100001").abfrage_ausfuehren("SELECT * FROM tarife", self.testschema)

        self.assertEqual(str(ergebnis), "[(1, 1, 'A5-1', 1)]")

    def test_kein_doppelter_eintrag(self):
        """
        Test prueft, ob bei wiederholtem Aufruf der Methode 'insert_tarife' mit demselben Tarif
        dieser nicht erneut eingetragen wird. Beim zweiten Eintrag muss eine Exception geworfen werden.
        Ausloeser ist der unique-constraint der Tabelle "Tarife" der fuer jeden Mandanten die mehrmalige
        identische Eintragung desselben Tarifs verbietet. Falls eine Tarifbezeichnung aktualisiert werden soll, so muss
        eine update-Funktion ausgefuehrt werden (welche im Rahmen dieser Bachelorarbeit nicht implementiert wurde).
        """
        self.testfirma.get_nutzer("M100001").insert_tarif('testdaten_insert_tarif/Tarif.xlsx', self.testschema)

        # Versuch, denselben Wert noch einmal einzutragen
        with self.assertRaises(Exception) as context:
            self.testfirma.get_nutzer("M100001").insert_tarif('testdaten_insert_tarif/Tarif.xlsx', self.testschema)

        self.assertEqual(str(context.exception), "FEHLER:  Tarif ist bereits vorhanden! Uebergebene Daten werden nicht "
                                                 "eingetragen! Wenn Sie diese Daten aktualisieren wollen, nutzen Sie "
                                                 "bitte die 'update_Tarif'-Funktion!\n"
                                                 "CONTEXT:  PL/pgSQL-Funktion insert_tarif(integer,character varying,"
                                                 "character varying) Zeile 24 bei RAISE\n")

        # Inhalt aus Tabelle ziehen, um zu pruefen, ob der Datensatz nur einmal angelegt wurde
        ergebnis = self.testfirma.get_nutzer("M100001").abfrage_ausfuehren("SELECT * FROM tarife", self.testschema)

        self.assertEqual(str(ergebnis), "[(1, 1, 'A5-1', 1)]")

    def test_kein_doppelter_eintrag_case_insensitive(self):
        """
        Test prueft, ob bei wiederholtem Aufruf der Methode 'insert_tarif' mit demselben Tarif aber mit Kleinschreibung
        dieser dennoch nicht erneut eingetragen wird. Beim zweiten Eintrag muss eine Exception geworfen werden.
        Ausloeser ist der unique-constraint in Kombination mit dem unique-Index 'tarifbezeichnung_idx'. Falls eine
        Tarifbezeichnung aktualisiert werden soll, so muss eine update-Funktion ausgefuehrt werden (welche im Rahmen
        dieser Bachelorarbeit nicht implementiert wurde).
        """
        self.testfirma.get_nutzer("M100001").insert_tarif('testdaten_insert_tarif/Tarif.xlsx', self.testschema)

        # Versuch, denselben Wert noch einmal einzutragen
        with self.assertRaises(Exception) as context:
            self.testfirma.get_nutzer("M100001").insert_tarif('testdaten_insert_tarif/'
                                                              'Tarif - Tarif klein geschrieben.xlsx',
                                                              self.testschema)

        self.assertEqual(str(context.exception), "FEHLER:  Tarif 'Verdi' bereits vorhanden!\n"
                                                 "CONTEXT:  PL/pgSQL-Funktion insert_tarif(integer,character varying,"
                                                 "character varying) Zeile 34 bei RAISE\n")

        # Inhalt aus Tabelle ziehen, um zu pruefen, ob der nur einmal Datensatz angelegt wurde
        ergebnis = self.testfirma.get_nutzer("M100001").abfrage_ausfuehren("SELECT * FROM tarife", self.testschema)

        self.assertEqual(str(ergebnis), "[(1, 1, 'A5-1', 1)]")

    def test_kein_eintrag_nicht_existente_gewerkschaft(self):
        """
        Test prueft, ob eine Exception geworfen wurde, wenn der Tarif zu einer Gewerkschaft zugeordnet wird, die
        bisher nicht in der Datenbank eingetragen wurde.
        """
        with self.assertRaises(Exception) as context:
            self.testfirma.get_nutzer("M100001").insert_tarif('testdaten_insert_tarif/'
                                                              'Tarif - Gewerkschaft nicht existent.xlsx',
                                                              self.testschema)

        self.assertEqual(str(context.exception), "FEHLER:  Gewerkschaft 'IG Metall' existiert nicht! Bitte tragen Sie "
                                                 "erst eine Gewerkschaft ein!\n"
                                                 "CONTEXT:  PL/pgSQL-Funktion insert_tarif(integer,character varying,"
                                                 "character varying) Zeile 16 bei RAISE\n")

        # Inhalt aus Tabelle ziehen, um zu pruefen, ob kein Datensatz angelegt wurde
        ergebnis = self.testfirma.get_nutzer("M100001").abfrage_ausfuehren("SELECT * FROM tarife", self.testschema)

        self.assertEqual(str(ergebnis), "[]")

    def tearDown(self):
        """
        Methode ruft Funktion 'test_tear_down' auf, welches das Datenbankschema 'temp_test_schema' mit allen Daten
        entfernt.
        """
        test_tear_down()
