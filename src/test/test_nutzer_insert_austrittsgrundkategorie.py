import unittest
from src.main.Mandant import Mandant
from src.main.test_SetUp_TearDown import test_set_up, test_tear_down


class TestNutzerInsertAustrittsgrundkategorie(unittest.TestCase):

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
        Test prueft, ob eine Austrittsgrundkategorie eingetragen wird, sofern der Wert gueltig ist.
        """
        self.testfirma.get_nutzer("M100001").\
            insert_austrittsgrundkategorie('testdaten_insert_austrittsgrundkategorie/Austrittsgrundkategorie.xlsx',
                                           self.testschema)

        # Inhalt aus Tabelle ziehen, um zu pruefen, ob der Datensatz angelegt wurde
        ergebnis = self.testfirma.get_nutzer("M100001").\
            abfrage_ausfuehren("SELECT * FROM Kategorien_Austrittsgruende", self.testschema)

        self.assertEqual(str(ergebnis), "[(1, 1, 'betriebsbedingt')]")

    def test_kein_doppelter_eintrag(self):
        """
        Test prueft, ob bei wiederholtem Aufruf der Methode 'insert_austrittsgrundkategorie' mit derselben Austritts-
        grundkategorie dieser nicht mehrfach eingetragen wird. Beim zweiten Eintrag muss eine Exception geworfen werden.
        Ausloeser ist der unique-constraint, welcher in der Stored Procedure 'insert_kategorien_austrittsgruende'
        implementiert ist.
        """
        self.testfirma.get_nutzer("M100001"). \
            insert_austrittsgrundkategorie('testdaten_insert_austrittsgrundkategorie/Austrittsgrundkategorie.xlsx',
                                           self.testschema)

        # Versuch, denselben Wert noch einmal einzutragen
        with self.assertRaises(Exception) as context:
            self.testfirma.get_nutzer("M100001"). \
                insert_austrittsgrundkategorie('testdaten_insert_austrittsgrundkategorie/Austrittsgrundkategorie.xlsx',
                                               self.testschema)

        self.assertEqual(str(context.exception), "FEHLER:  Austrittsgrundkategorie 'betriebsbedingt' bereits "
                                                 "vorhanden!\n"
                                                 "CONTEXT:  PL/pgSQL-Funktion insert_kategorien_austrittsgruende"
                                                 "(integer,character varying) Zeile 16 bei RAISE\n")

        # Inhalt aus Tabelle ziehen, um zu pruefen, ob der Datensatz angelegt wurde
        ergebnis = self.testfirma.get_nutzer("M100001"). \
            abfrage_ausfuehren("SELECT * FROM Kategorien_Austrittsgruende", self.testschema)

        self.assertEqual(str(ergebnis), "[(1, 1, 'betriebsbedingt')]")

    def test_falscher_eintrag(self):
        """
        Test prueft, ob eine Exception geworfen wird, wenn die geforderte Rechtschreibung fuer die drei Austrittsgrund-
        kategorie-moeglichkeiten ('verhaltensbedingt', 'personenbedingt', 'betriebsbedingt') nicht eingehalten wird.
        Ausloeser der Exception ist der check-constraint, welcher in der Stored Procedure
        'insert_kategorien_austrittsgruende' implementiert ist.
        Hinweis: die Excel-Datei ist fuer gewoehnlich so praepariert, dass man nur die richtige Rechtschreibung
        eintragen kann. Dennoch soll getestet werden, ob im Ernstfall der constraint greift. Hierfuer wurde die Excel-
        Datei so umgestaltet, dass man auch falsch geschriebene Austrittsgrundkategorien eintragen kann.
        """

        # Versuch, falsch geschriebenes Geschlecht 'männlich' einzutragen
        with self.assertRaises(Exception) as context:
            self.testfirma.get_nutzer("M100001"). \
                insert_austrittsgrundkategorie('testdaten_insert_austrittsgrundkategorie/Austrittsgrundkategorie - '
                                               'falsch geschrieben.xlsx', self.testschema)

        self.assertEqual(str(context.exception), "FEHLER:  Fuer Austrittsgrundkategorien sind nur folgende Werte "
                                                 "erlaubt: 'verhaltensbedingt', 'personenbedingt', 'betriebsbedingt'!\n"
                                                 "CONTEXT:  PL/pgSQL-Funktion insert_kategorien_austrittsgruende"
                                                 "(integer,character varying) Zeile 19 bei RAISE\n")

        # Inhalt aus Tabelle ziehen, um zu pruefen, ob der Datensatz tatsaechlich nicht angelegt wurde
        ergebnis = self.testfirma.get_nutzer("M100001").abfrage_ausfuehren("SELECT * FROM kategorien_Austrittsgruende",
                                                                           self.testschema)

        self.assertEqual(str(ergebnis), "[]")

    def tearDown(self):
        """
        Methode ruft Funktion 'test_tear_down' auf, welches das Datenbankschema 'temp_test_schema' mit allen Daten
        entfernt.
        """
        test_tear_down()
