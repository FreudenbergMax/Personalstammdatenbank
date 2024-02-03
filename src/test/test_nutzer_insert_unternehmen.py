import unittest

from src.main.Login import Login
from src.main.test_SetUp_TearDown import test_set_up, test_tear_down


class TestNutzerInsertUnternehmen(unittest.TestCase):

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

    def test_erfolgreicher_eintrag_mit_abkuerzung(self):
        """
        Test prueft, ob ein Unternehmen mit ihrer Abkuerzung eingetragen wird.
        """
        self.nutzer.insert_unternehmen('testdaten_insert_unternehmen/Unternehmen.xlsx')

        # Inhalt aus Tabelle ziehen, um zu pruefen, ob der Datensatz angelegt wurde
        ergebnis = self.nutzer.abfrage_ausfuehren("SELECT * FROM unternehmen")

        self.assertEqual(str(ergebnis), "[(1, 1, 'Beispielfirma GmbH', 'Bf GmbH', None)]")

    def test_erfolgreicher_eintrag_ohne_abkuerzung(self):
        """
        Test prueft, ob ein Unternehmen ohne ihrer Abkuerzung eingetragen wird.
        """
        self.nutzer.insert_unternehmen('testdaten_insert_unternehmen/Unternehmen - ohne Abkuerzung.xlsx')

        # Inhalt aus Tabelle ziehen, um zu pruefen, ob der Datensatz angelegt wurde
        ergebnis = self.nutzer.abfrage_ausfuehren("SELECT * FROM unternehmen")

        self.assertEqual(str(ergebnis), "[(1, 1, 'Beispielfirma GmbH', None, None)]")

    def test_kein_doppelter_eintrag_unternehmen_und_abkuerzung_identisch(self):
        """
        Test prueft, ob bei wiederholtem Aufruf der Methode 'insert_unternehmen' mit demselben Unternehmen dieser nicht
        mehrfach eingetragen wird. Beim zweiten Eintrag muss eine Fehlermeldung erscheinen.
        """
        self.nutzer.insert_unternehmen('testdaten_insert_unternehmen/Unternehmen.xlsx')

        # Versuch, denselben Wert noch einmal einzutragen
        with self.assertRaises(Exception) as context:
            self.nutzer.insert_unternehmen('testdaten_insert_unternehmen/Unternehmen.xlsx')

        erwartete_fehlermeldung = "FEHLER:  Unternehmen 'Beispielfirma GmbH' bereits vorhanden!"
        tatsaechliche_fehlermeldung = str(context.exception)
        self.assertTrue(tatsaechliche_fehlermeldung.startswith(erwartete_fehlermeldung))

        # Inhalt aus Tabelle ziehen, um zu pruefen, ob der Datensatz auch nur einmal angelegt wurde
        ergebnis = self.nutzer.abfrage_ausfuehren("SELECT * FROM unternehmen")

        self.assertEqual(str(ergebnis), "[(1, 1, 'Beispielfirma GmbH', 'Bf GmbH', None)]")

    def test_kein_doppelter_eintrag_unternehmen_case_insensitive(self):
        """
        Test prueft, ob bei wiederholtem Aufruf der Methode 'insert_unternehmen' mit demselben Unternehmen aber mit
        Kleinschreibung dieser dennoch nicht mehrfach eingetragen wird. Beim zweiten Eintrag muss eine Fehlermeldung
        erscheinen.
        """
        self.nutzer.insert_unternehmen('testdaten_insert_unternehmen/Unternehmen.xlsx')

        # Versuch, denselben Wert noch einmal einzutragen (diesmal aber in Kleinschreibung)
        with self.assertRaises(Exception) as context:
            self.nutzer.insert_unternehmen('testdaten_insert_unternehmen/Unternehmen - '
                                           'Unternehmen klein geschrieben.xlsx')

        erwartete_fehlermeldung = "FEHLER:  Unternehmen 'beispielfirma gmbh' bereits vorhanden!"
        tatsaechliche_fehlermeldung = str(context.exception)
        self.assertTrue(tatsaechliche_fehlermeldung.startswith(erwartete_fehlermeldung))

        # Inhalt aus Tabelle ziehen, um zu pruefen, ob der Datensatz auch nur einmal angelegt wurde
        ergebnis = self.nutzer.abfrage_ausfuehren("SELECT * FROM unternehmen")

        self.assertEqual(str(ergebnis), "[(1, 1, 'Beispielfirma GmbH', 'Bf GmbH', None)]")

    def tearDown(self):
        """
        Methode ruft Funktion 'test_tear_down' auf, welches das Datenbankschema 'temp_test_schema' mit allen Daten
        entfernt.
        """
        test_tear_down()
