import unittest
from src.main.Mandant import Mandant
from src.main.test_SetUp_TearDown import test_set_up, test_tear_down


class TestNutzerInsertSteuerklasse(unittest.TestCase):

    def setUp(self):
        """
        Methode ruft Funktion 'test_set_up' der Klasse 'test_SetUp_TearDown' (siehe Ordner 'main') auf, welches das
        Datenbankschema 'temp_test_schema' erstellt.
        """
        self.conn, self.cur, self.testschema = test_set_up()
        self.testfirma = Mandant('Testfirma', self.testschema)
        self.testfirma.nutzer_anlegen('M100001', 'Max', 'Mustermann', self.testschema)

    def test_erfolgreicher_eintrag(self):
        """
        Test prueft, ob eine Steuerklasse eingetragen wird, sofern die Wert gueltig ist.
        """
        self.testfirma.get_nutzer("M100001").\
            insert_steuerklasse('testdaten_insert_steuerklasse/Steuerklasse.xlsx', self.testschema)

        # Inhalt aus Tabelle ziehen, um zu pruefen, ob der Datensatz angelegt wurde
        ergebnis = self.testfirma.get_nutzer("M100001").\
            abfrage_ausfuehren("SELECT * FROM steuerklassen", self.testschema)

        self.assertEqual(str(ergebnis), "[(1, 1, '1')]")

    def test_kein_doppelter_eintrag(self):
        """
        Test prueft, ob bei wiederholtem Aufruf der Methode 'insert_steuerklasse' mit derselben Steuerklasse dieser
        nicht mehrfach eingetragen wird. Beim zweiten Eintrag muss eine Exception geworfen werden. Ausloeser ist der
        unique-constraint, welcher in der Stored Procedure 'insert_steuerklasse' implementiert ist.
        """
        self.testfirma.get_nutzer("M100001"). \
            insert_steuerklasse('testdaten_insert_steuerklasse/Steuerklasse.xlsx', self.testschema)

        # Versuch, denselben Wert noch einmal einzutragen
        with self.assertRaises(Exception) as context:
            self.testfirma.get_nutzer("M100001"). \
                insert_steuerklasse('testdaten_insert_steuerklasse/Steuerklasse.xlsx', self.testschema)

        self.assertEqual(str(context.exception), "FEHLER:  Steuerklasse '1' bereits vorhanden!\n"
                                                 "CONTEXT:  PL/pgSQL-Funktion insert_steuerklasse(integer,character) "
                                                 "Zeile 17 bei RAISE\n")

        # Inhalt aus Tabelle ziehen, um zu pruefen, ob der Datensatz auch nur einmal angelegt wurde
        ergebnis = self.testfirma.get_nutzer("M100001").abfrage_ausfuehren("SELECT * FROM steuerklassen",
                                                                           self.testschema)

        self.assertEqual(str(ergebnis), "[(1, 1, '1')]")

    def test_falscher_eintrag(self):
        """
        Test prueft, ob eine Exception geworfen wird, wenn eine nicht gueltige Steuerklasse (z.B. '7', welche nicht
        existiert) nicht eingehalten wird. Ausloeser der Exception ist der check-constraint, welcher in der Stored
        Procedure 'insert_steuerklasse' implementiert ist.
        Hinweis: die Excel-Datei ist fuer gewoehnlich so praepariert, dass man nur gueltige Steuerklassen
        eintragen kann. Dennoch soll getestet werden, ob im Ernstfall der constraint greift. Hierfuer wurde die Excel-
        Datei so umgestaltet, dass man nicht existente Steuerklassen eintragen kann.
        """

        # Versuch, nicht existente Steuerklasse '7' einzutragen
        with self.assertRaises(Exception) as context:
            self.testfirma.get_nutzer("M100001"). \
                insert_steuerklasse('testdaten_insert_steuerklasse/Steuerklasse - ungueltiger Wert.xlsx',
                                    self.testschema)

        self.assertEqual(str(context.exception), "FEHLER:  Fuer Steuerklassen sind nur folgende Werte erlaubt: "
                                                 "1, 2, 3, 4, 5, 6!\n"
                                                 "CONTEXT:  PL/pgSQL-Funktion insert_steuerklasse(integer,character) "
                                                 "Zeile 20 bei RAISE\n")

        # Inhalt aus Tabelle ziehen, um zu pruefen, ob der Datensatz tatsaechlich nicht angelegt wurde
        ergebnis = self.testfirma.get_nutzer("M100001").abfrage_ausfuehren("SELECT * FROM steuerklassen",
                                                                           self.testschema)

        self.assertEqual(str(ergebnis), "[]")

    def tearDown(self):
        """
        Methode ruft Funktion 'test_tear_down' auf, welches das Datenbankschema 'temp_test_schema' mit allen Daten
        entfernt.
        """
        test_tear_down(self.conn, self.cur)
