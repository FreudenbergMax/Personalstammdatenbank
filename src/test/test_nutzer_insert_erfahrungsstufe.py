import unittest

from src.main.Login import Login
from src.main.test_SetUp_TearDown import test_set_up, test_tear_down


class TestNutzerInsertErfahrungsstufe(unittest.TestCase):

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
        Test prueft, ob eine Erfahrungsstufe eingetragen wird.
        """
        self.nutzer.insert_erfahrungsstufe('testdaten_insert_erfahrungsstufe/Erfahrungsstufe.xlsx')

        # Inhalt aus Tabelle ziehen, um zu pruefen, ob der Datensatz angelegt wurde
        ergebnis = self.nutzer.abfrage_ausfuehren("SELECT * FROM erfahrungsstufen")
        self.assertEqual(str(ergebnis), "[(1, 1, 'Junior')]")

    def test_kein_doppelter_eintrag(self):
        """
        Test prueft, ob bei wiederholtem Aufruf der Methode 'insert_erfahrungsstufe' mit derselben Erfahrungsstufe
        dieser nicht mehrfach eingetragen wird. Beim zweiten Eintrag muss eine Exception geworfen werden. Ausloeser ist
        der unique-constraint, welcher in der Stored Procedure 'insert_erfahrungsstufe' implementiert ist.
        """
        self.nutzer.insert_erfahrungsstufe('testdaten_insert_erfahrungsstufe/Erfahrungsstufe.xlsx')

        # Versuch, denselben Wert noch einmal einzutragen
        with self.assertRaises(Exception) as context:
            self.nutzer.insert_erfahrungsstufe('testdaten_insert_erfahrungsstufe/Erfahrungsstufe.xlsx')

        erwartete_fehlermeldung = "FEHLER:  Erfahrungsstufe 'Junior' bereits vorhanden!"
        tatsaechliche_fehlermeldung = str(context.exception)
        self.assertTrue(tatsaechliche_fehlermeldung.startswith(erwartete_fehlermeldung))

        # Inhalt aus Tabelle ziehen, um zu pruefen, ob der Datensatz auch nur einmal angelegt wurde
        ergebnis = self.nutzer.abfrage_ausfuehren("SELECT * FROM erfahrungsstufen")
        self.assertEqual(str(ergebnis), "[(1, 1, 'Junior')]")

    def test_kein_doppelter_eintrag_case_insensitive(self):
        """
        Test prueft, ob bei wiederholtem Aufruf der Methode 'insert_erfahrungsstufe' mit derselben Erfahrungsstufe aber
        mit Kleinschreibung dieser dennoch nicht mehrfach eingetragen wird. Beim zweiten Eintrag muss eine Exception
        geworfen werden. Ausloeser ist der unique-constraint, welcher in der Stored Procedure 'insert_erfahrungsstufe'
        implementiert ist, in Kombination mit dem unique-Index 'erfahrungsstufe_idx'.
        """
        self.nutzer.insert_erfahrungsstufe('testdaten_insert_erfahrungsstufe/Erfahrungsstufe.xlsx')

        # Versuch, denselben Wert noch einmal einzutragen (diesmal aber in Kleinschreibung)
        with self.assertRaises(Exception) as context:
            self.nutzer.insert_erfahrungsstufe(
                'testdaten_insert_erfahrungsstufe/Erfahrungsstufe - klein geschrieben.xlsx')

        erwartete_fehlermeldung = "FEHLER:  Erfahrungsstufe 'junior' bereits vorhanden!"
        tatsaechliche_fehlermeldung = str(context.exception)
        self.assertTrue(tatsaechliche_fehlermeldung.startswith(erwartete_fehlermeldung))

        # Inhalt aus Tabelle ziehen, um zu pruefen, ob der Datensatz auch nur einmal angelegt wurde
        ergebnis = self.nutzer.abfrage_ausfuehren("SELECT * FROM erfahrungsstufen")
        self.assertEqual(str(ergebnis), "[(1, 1, 'Junior')]")

    def tearDown(self):
        """
        Methode ruft Funktion 'test_tear_down' auf, welches das Datenbankschema 'temp_test_schema' mit allen Daten
        entfernt.
        """
        test_tear_down()
