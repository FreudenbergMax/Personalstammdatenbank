import unittest
from src.main.Mandant import Mandant
from src.main.test_SetUp_TearDown import test_set_up, test_tear_down


class TestNutzerInsertGeschlecht(unittest.TestCase):

    def setUp(self):
        """
        Methode ruft Funktion 'test_set_up' der Klasse 'test_SetUp_TearDown' (siehe Ordner 'main') auf, welches das
        Datenbankschema 'temp_test_schema' erstellt.
        """
        self.testschema = test_set_up()
        self.testfirma = Mandant('Testfirma', self.testschema)
        self.testfirma.nutzer_anlegen('M100001', 'Max', 'Mustermann', self.testschema)

    def test_erfolgreicher_eintrag(self):
        """
        Test prueft, ob ein Geschlecht eingetragen wird, sofern der Wert gueltig.
        """
        self.testfirma.get_nutzer("M100001").\
            insert_geschlecht('testdaten_insert_geschlecht/Geschlecht.xlsx', self.testschema)

        # Inhalt aus Tabelle ziehen, um zu pruefen, ob der Datensatz angelegt wurde
        ergebnis = self.testfirma.get_nutzer("M100001").\
            abfrage_ausfuehren("SELECT * FROM geschlechter", self.testschema)

        self.assertEqual(str(ergebnis), "[(1, 1, 'maennlich')]")

    def test_kein_doppelter_eintrag(self):
        """
        Test prueft, ob bei wiederholtem Aufruf der Methode 'insert_geschlecht' mit demselben Geschlecht dieser nicht
        mehrfach eingetragen wird. Beim zweiten Eintrag muss eine Exception geworfen werden. Ausloeser ist der
        unique-constraint, welcher in der Stored Procedure 'insert_geschlecht' implementiert ist.
        """
        self.testfirma.get_nutzer("M100001").\
            insert_geschlecht('testdaten_insert_geschlecht/Geschlecht.xlsx', self.testschema)

        # Versuch, denselben Wert noch einmal einzutragen
        with self.assertRaises(Exception) as context:
            self.testfirma.get_nutzer("M100001"). \
                insert_geschlecht('testdaten_insert_geschlecht/Geschlecht.xlsx', self.testschema)

        self.assertEqual(str(context.exception), "FEHLER:  Geschlecht 'maennlich' bereits vorhanden!\n"
                                                 "CONTEXT:  PL/pgSQL-Funktion insert_geschlecht(integer,character "
                                                 "varying) Zeile 14 bei RAISE\n")

        # Inhalt aus Tabelle ziehen, um zu pruefen, ob der Datensatz auch nur einmal angelegt wurde
        ergebnis = self.testfirma.get_nutzer("M100001").abfrage_ausfuehren("SELECT * FROM geschlechter",
                                                                           self.testschema)

        self.assertEqual(str(ergebnis), "[(1, 1, 'maennlich')]")

    def test_falscher_eintrag(self):
        """
        Test prueft, ob eine Exception geworfen wird, wenn die geforderte Rechtschreibung fuer die drei Geschlechts-
        moeglichkeiten ('maennlich', 'weiblich', 'divers') nicht eingehalten wird. Ausloeser der Exception ist
        der check-constraint, welcher in der Stored Procedure 'insert_geschlecht' implementiert ist.
        Hinweis: die Excel-Datei ist fuer gewoehnlich so praepariert, dass man nur die richtige Rechtschreibung
        eintragen kann. Dennoch soll getestet werden, ob im Ernstfall der constraint greift. Hierfuer wurde die Excel-
        Datei so umgestaltet, dass man auch falsch geschriebene Geschlechter eintragen kann.
        """

        # Versuch, falsch geschriebenes Geschlecht 'männlich' einzutragen
        with self.assertRaises(Exception) as context:
            self.testfirma.get_nutzer("M100001"). \
                insert_geschlecht('testdaten_insert_geschlecht/Geschlecht - falsch geschrieben.xlsx', self.testschema)

        self.assertEqual(str(context.exception), "FEHLER:  Fuer Geschlechter sind nur folgende Werte erlaubt: "
                                                 "'maennlich', 'weiblich', 'divers'!\n"
                                                 "CONTEXT:  PL/pgSQL-Funktion insert_geschlecht(integer,character "
                                                 "varying) Zeile 16 bei RAISE\n")

        # Inhalt aus Tabelle ziehen, um zu pruefen, ob der Datensatz tatsaechlich nicht angelegt wurde
        ergebnis = self.testfirma.get_nutzer("M100001").abfrage_ausfuehren("SELECT * FROM geschlechter",
                                                                           self.testschema)

        self.assertEqual(str(ergebnis), "[]")

    def tearDown(self):
        """
        Methode ruft Funktion 'test_tear_down' auf, welches das Datenbankschema 'temp_test_schema' mit allen Daten
        entfernt.
        """
        test_tear_down()
