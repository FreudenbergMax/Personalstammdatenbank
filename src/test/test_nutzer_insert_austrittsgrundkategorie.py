import unittest

from src.main.Login import Login
from src.main.test_SetUp_TearDown import test_set_up, test_tear_down


class TestNutzerInsertAustrittsgrundkategorie(unittest.TestCase):

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

    def test_erfolgreicher_eintrag(self):
        """
        Test prueft, ob eine Austrittsgrundkategorie eingetragen wird, sofern der Wert gueltig ist.
        """
        self.nutzer.insert_austrittsgrundkategorie(
            'testdaten_insert_austrittsgrundkategorie/Austrittsgrundkategorie.xlsx')

        # Inhalt aus Tabelle ziehen, um zu pruefen, ob der Datensatz angelegt wurde
        ergebnis = self.nutzer.abfrage_ausfuehren("SELECT * FROM Kategorien_Austrittsgruende")
        self.assertEqual(str(ergebnis), "[(1, 1, 'betriebsbedingt')]")

    def test_kein_doppelter_eintrag(self):
        """
        Test prueft, ob bei wiederholtem Aufruf der Methode 'insert_austrittsgrundkategorie' mit derselben Austritts-
        grundkategorie dieser nicht mehrfach eingetragen wird. Beim zweiten Eintrag muss eine Fehlermeldung erscheinen.
        """
        self.nutzer.insert_austrittsgrundkategorie(
            'testdaten_insert_austrittsgrundkategorie/Austrittsgrundkategorie.xlsx')

        # Versuch, denselben Wert noch einmal einzutragen
        with self.assertRaises(Exception) as context:
            self.nutzer.insert_austrittsgrundkategorie(
                'testdaten_insert_austrittsgrundkategorie/Austrittsgrundkategorie.xlsx')

        erwartete_fehlermeldung = "FEHLER:  Austrittsgrundkategorie 'betriebsbedingt' bereits vorhanden!"
        tatsaechliche_fehlermeldung = str(context.exception)
        self.assertTrue(tatsaechliche_fehlermeldung.startswith(erwartete_fehlermeldung))

        # Inhalt aus Tabelle ziehen, um zu pruefen, ob der Datensatz angelegt wurde
        ergebnis = self.nutzer.abfrage_ausfuehren("SELECT * FROM Kategorien_Austrittsgruende")
        self.assertEqual(str(ergebnis), "[(1, 1, 'betriebsbedingt')]")

    def test_falscher_eintrag(self):
        """
        Test prueft, ob eine Fehlermeldung erscheint, wenn die geforderte Rechtschreibung fuer die drei Austrittsgrund-
        kategorie-moeglichkeiten ('verhaltensbedingt', 'personenbedingt', 'betriebsbedingt') nicht eingehalten wird.
        Hinweis: die Excel-Datei ist fuer gewoehnlich so praepariert, dass man nur die richtige Rechtschreibung
        eintragen kann. Dennoch soll getestet werden, ob im Ernstfall der constraint greift. Hierfuer wurde die Excel-
        Datei so umgestaltet, dass man auch falsch geschriebene Austrittsgrundkategorien eintragen kann.
        """

        # Versuch, falsch geschriebenes Geschlecht 'männlich' einzutragen
        with self.assertRaises(Exception) as context:
            self.nutzer.insert_austrittsgrundkategorie(
                'testdaten_insert_austrittsgrundkategorie/Austrittsgrundkategorie - falsch geschrieben.xlsx')

        erwartete_fehlermeldung = "FEHLER:  Fuer Austrittsgrundkategorien sind nur folgende Werte erlaubt: " \
                                  "'verhaltensbedingt', 'personenbedingt', 'betriebsbedingt'!"
        tatsaechliche_fehlermeldung = str(context.exception)
        self.assertTrue(tatsaechliche_fehlermeldung.startswith(erwartete_fehlermeldung))

        # Inhalt aus Tabelle ziehen, um zu pruefen, ob der Datensatz tatsaechlich nicht angelegt wurde
        ergebnis = self.nutzer.abfrage_ausfuehren("SELECT * FROM kategorien_Austrittsgruende")
        self.assertEqual(str(ergebnis), "[]")

    def tearDown(self):
        """
        Methode ruft Funktion 'test_tear_down' auf, welches das Datenbankschema 'temp_test_schema' mit allen Daten
        entfernt.
        """
        test_tear_down()
