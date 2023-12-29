import unittest
from src.main.Mandant import Mandant
from src.main.test_SetUp_TearDown import test_set_up, test_tear_down


class TestNutzerInsertUnfallversicherungsbeitraege(unittest.TestCase):

    def setUp(self):
        """
        Methode ruft Funktion 'test_set_up' der Klasse 'test_SetUp_TearDown' (siehe Ordner 'main') auf, welches das
        Datenbankschema 'temp_test_schema' erstellt.
        """
        self.conn, self.cur, self.testschema = test_set_up()
        self.testfirma = Mandant('Testfirma', self.testschema)
        self.testfirma.nutzer_anlegen('M100001', 'Max', 'Mustermann', self.testschema)

        self.testfirma.get_nutzer("M100001"). \
            insert_berufsgenossenschaft('testdaten_insert_berufsgenossenschaft/Berufsgenossenschaft.xlsx',
                                        self.testschema)

        self.testfirma.get_nutzer("M100001").\
            insert_gesellschaft('testdaten_insert_gesellschaft/Gesellschaft.xlsx', self.testschema)

    def test_erfolgreicher_eintrag(self):
        """
        Test prueft, ob der Unfallversicherungsbeitrag fuer ein Unternehmen eingetragen wird.
        """
        self.testfirma.get_nutzer("M100001").\
            insert_unfallversicherungsbeitrag('testdaten_insert_unfallversicherungsbeitrag/'
                                              'Unfallversicherungsbeitrag.xlsx',
                                              self.testschema)

        # Inhalt aus Tabelle ziehen, um zu pruefen, ob der Datensatz angelegt wurde
        ergebnis = self.testfirma.get_nutzer("M100001").\
            abfrage_ausfuehren("SELECT * FROM unfallversicherungsbeitraege", self.testschema)

        self.assertEqual(str(ergebnis), "[(1, 1, 1, Decimal('6543123.89'), 2023)]")

    def test_kein_doppelter_eintrag(self):
        """
        Test prueft, ob bei wiederholtem Aufruf der Methode 'insert_unfallversicherungsbeitrag' mit derselben
        Berufsgenossenschaft und Abkuerzung dieser nicht erneut eingetragen wird. Beim zweiten Eintrag muss eine
        Exception geworfen werden, da der unique-constraint missachtet wurde.
        """
        self.testfirma.get_nutzer("M100001"). \
            insert_unfallversicherungsbeitrag('testdaten_insert_unfallversicherungsbeitrag/'
                                              'Unfallversicherungsbeitrag.xlsx',
                                              self.testschema)

        # Versuch, denselben Wert noch einmal einzutragen
        with self.assertRaises(Exception) as context:
            self.testfirma.get_nutzer("M100001"). \
                insert_unfallversicherungsbeitrag('testdaten_insert_unfallversicherungsbeitrag/'
                                                  'Unfallversicherungsbeitrag.xlsx',
                                                  self.testschema)

        self.assertEqual(str(context.exception), "FEHLER:  Unfallversicherungsbeitrag ist fuer das Jahr '2023' "
                                                 "bereits vermerkt!\n"
                                                 "CONTEXT:  PL/pgSQL-Funktion insert_unfallversicherungsbeitrag"
                                                 "(integer,character varying,character varying,character varying,"
                                                 "character varying,numeric,integer) Zeile 38 bei RAISE\n")

        # Inhalt aus Tabelle ziehen, um zu pruefen, ob der Datensatz auch nur einmal angelegt wurde
        ergebnis = self.testfirma.get_nutzer("M100001"). \
            abfrage_ausfuehren("SELECT * FROM unfallversicherungsbeitraege", self.testschema)

        self.assertEqual(str(ergebnis), "[(1, 1, 1, Decimal('6543123.89'), 2023)]")

    def test_Eintrag_Folgejahr_moeglich(self):
        """
        Test prueft, ob fuer das Folgejahr der Eintrag der Unfallversicheurngsbeitraege fuer dieselbe Gesellschaft mit
        derselben Berufsgenossenschaft moeglich ist. Der Eintrag muss erfolgen koennen, da der unique-constraint nur
        greift, wenn die Spalten 'Gesellschaft_ID', 'Berufsgenossenschaft_ID' und 'Beitragsjahr' in Kombination
        identisch sind.
        """
        self.testfirma.get_nutzer("M100001"). \
            insert_unfallversicherungsbeitrag('testdaten_insert_unfallversicherungsbeitrag/'
                                              'Unfallversicherungsbeitrag.xlsx',
                                              self.testschema)

        self.testfirma.get_nutzer("M100001"). \
            insert_unfallversicherungsbeitrag('testdaten_insert_unfallversicherungsbeitrag/'
                                              'Unfallversicherungsbeitrag - Folgejahr.xlsx',
                                              self.testschema)

        # Inhalt aus Tabelle ziehen, um zu pruefen, ob der Datensatz auch nur einmal angelegt wurde
        ergebnis = self.testfirma.get_nutzer("M100001"). \
            abfrage_ausfuehren("SELECT * FROM unfallversicherungsbeitraege", self.testschema)

        self.assertEqual(str(ergebnis), "[(1, 1, 1, Decimal('6543123.89'), 2023), "
                                        "(1, 1, 1, Decimal('6748512.31'), 2024)]")

    def test_Eintrag_trotz_kleinschreibung(self):
        """
        Test prueft, ob Eintrag in Tabelle 'Unfallversicherungsbeitraege' gelingt, obwohl bei Eingabe der Gesellschaft,
        der Berufsgenossenschaft und deren Abkuerzungen in der Excel-Datei 'Unfallversicherungsbeitrag -
        klein geschrieben.xlsx' alles klein geschrieben wurde (waehrend Gesellschaft und Berufsgenossenschaft in ihren
        Tabellen gross geschrieben sind). Ziel ist, dass die Methode eine gewisse Toleranz bei der Gross- und Klein-
        schreibung hat.
        """
        self.testfirma.get_nutzer("M100001"). \
            insert_unfallversicherungsbeitrag('testdaten_insert_unfallversicherungsbeitrag/'
                                              'Unfallversicherungsbeitrag - klein geschrieben.xlsx',
                                              self.testschema)

        # Inhalt aus Tabelle ziehen, um zu pruefen, ob der Datensatz angelegt wurde
        ergebnis = self.testfirma.get_nutzer("M100001"). \
            abfrage_ausfuehren("SELECT * FROM unfallversicherungsbeitraege", self.testschema)

        self.assertEqual(str(ergebnis), "[(1, 1, 1, Decimal('6543123.89'), 2023)]")

    def tearDown(self):
        """
        Methode ruft Funktion 'test_tear_down' auf, welches das Datenbankschema 'temp_test_schema' mit allen Daten
        entfernt.
        """
        test_tear_down(self.conn, self.cur)
