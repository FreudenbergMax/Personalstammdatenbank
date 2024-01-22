import unittest

from src.main.Login import Login
from src.main.Mandant import Mandant
from src.main.test_SetUp_TearDown import test_set_up, test_tear_down


class TestNutzerInsertGesellschaft(unittest.TestCase):

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
        Test prueft, ob eine Gesellschaft eingetragen wird.
        """
        self.nutzer.insert_gesellschaft('testdaten_insert_gesellschaft/Gesellschaft.xlsx')

        # Inhalt aus Tabelle ziehen, um zu pruefen, ob der Datensatz angelegt wurde
        ergebnis = self.nutzer.abfrage_ausfuehren("SELECT * FROM gesellschaften")

        self.assertEqual(str(ergebnis), "[(1, 1, 'Beispielfirma GmbH', 'Bf GmbH', None)]")

    def test_kein_doppelter_eintrag_Abteilung_und_abkuerzung_identisch(self):
        """
        Test prueft, ob bei wiederholtem Aufruf der Methode 'insert_gesellschaft' mit derselben Gesellschaft und
        Abkuerzung dieser nicht mehrfach eingetragen wird. Beim zweiten Eintrag muss eine Exception geworfen werden.
        Ausloeser ist der unique-constraint, welcher in der Stored Procedure 'insert_gesellschaft' implementiert ist.
        """
        self.nutzer.insert_gesellschaft('testdaten_insert_gesellschaft/Gesellschaft.xlsx')

        # Versuch, denselben Wert noch einmal einzutragen
        with self.assertRaises(Exception) as context:
            self.nutzer.insert_gesellschaft('testdaten_insert_gesellschaft/Gesellschaft.xlsx')

        erwartete_fehlermeldung = "FEHLER:  Gesellschaft 'Beispielfirma GmbH' oder 'Bf GmbH' bereits vorhanden!"
        tatsaechliche_fehlermeldung = str(context.exception)
        self.assertTrue(tatsaechliche_fehlermeldung.startswith(erwartete_fehlermeldung))

        # Inhalt aus Tabelle ziehen, um zu pruefen, ob der Datensatz auch nur einmal angelegt wurde
        ergebnis = self.nutzer.abfrage_ausfuehren("SELECT * FROM gesellschaften")

        self.assertEqual(str(ergebnis), "[(1, 1, 'Beispielfirma GmbH', 'Bf GmbH', None)]")

    def test_kein_doppelter_eintrag_Abteilung_identisch(self):
        """
        Test prueft, ob bei wiederholtem Aufruf der Methode 'insert_gesellschaft' mit derselben Gesellschaft aber
        anderer Abkuerzung dieser nicht eingetragen wird. Beim zweiten Eintrag muss eine Exception geworfen werden.
        Ausloeser ist  der unique-constraint, welcher in der Stored Procedure 'insert_gesellschaft' implementiert ist.
        """
        self.nutzer.insert_gesellschaft('testdaten_insert_gesellschaft/Gesellschaft.xlsx')

        # Versuch, denselben Wert noch einmal einzutragen
        with self.assertRaises(Exception) as context:
            self.nutzer.insert_gesellschaft('testdaten_insert_gesellschaft/Gesellschaft - Gesellschaft identisch.xlsx')

        erwartete_fehlermeldung = "FEHLER:  Gesellschaft 'Beispielfirma GmbH' oder 'BfGmbH' bereits vorhanden!"
        tatsaechliche_fehlermeldung = str(context.exception)
        self.assertTrue(tatsaechliche_fehlermeldung.startswith(erwartete_fehlermeldung))

        # Inhalt aus Tabelle ziehen, um zu pruefen, ob der Datensatz auch nur einmal angelegt wurde
        ergebnis = self.nutzer.abfrage_ausfuehren("SELECT * FROM gesellschaften")

        self.assertEqual(str(ergebnis), "[(1, 1, 'Beispielfirma GmbH', 'Bf GmbH', None)]")

    def test_kein_doppelter_eintrag_Abkuerzung_identisch(self):
        """
        Test prueft, ob bei wiederholtem Aufruf der Methode 'insert_geellschaft' mit anderer Gesellschaft aber
        identischer Abkuerzung dieser nicht eingetragen wird. Beim zweiten Eintrag muss eine Exception geworfen werden.
        Ausloeser ist  der unique-constraint, welcher in der Stored Procedure 'insert_gesellschaft' implementiert ist.
        """
        self.nutzer.insert_gesellschaft('testdaten_insert_gesellschaft/Gesellschaft.xlsx')

        # Versuch, denselben Wert noch einmal einzutragen
        with self.assertRaises(Exception) as context:
            self.nutzer.insert_gesellschaft('testdaten_insert_gesellschaft/Gesellschaft - Abkuerzung identisch.xlsx')

        erwartete_fehlermeldung = "FEHLER:  Gesellschaft 'BeispielfirmaGmbH' oder 'Bf GmbH' bereits vorhanden!"
        tatsaechliche_fehlermeldung = str(context.exception)
        self.assertTrue(tatsaechliche_fehlermeldung.startswith(erwartete_fehlermeldung))

        # Inhalt aus Tabelle ziehen, um zu pruefen, ob der Datensatz auch nur einmal angelegt wurde
        ergebnis = self.nutzer.abfrage_ausfuehren("SELECT * FROM gesellschaften")

        self.assertEqual(str(ergebnis), "[(1, 1, 'Beispielfirma GmbH', 'Bf GmbH', None)]")

    def test_kein_doppelter_eintrag_abteilung_case_insensitive(self):
        """
        Test prueft, ob bei wiederholtem Aufruf der Methode 'insert_gesellschaft' mit derselben Abteilung aber mit
        Kleinschreibung dieser dennoch nicht mehrfach eingetragen wird. Beim zweiten Eintrag muss eine Exception
        geworfen werden. Ausloeser ist der unique-constraint, welcher in der Stored Procedure 'insert_gesellschaft'
        implementiert ist, in Kombination mit dem unique-Index 'gesellschaft_idx'.
        """
        self.nutzer.insert_gesellschaft('testdaten_insert_gesellschaft/Gesellschaft.xlsx')

        # Versuch, denselben Wert noch einmal einzutragen (diesmal aber in Kleinschreibung)
        with self.assertRaises(Exception) as context:
            self.nutzer.insert_gesellschaft('testdaten_insert_gesellschaft/Gesellschaft - '
                                            'Gesellschaft klein geschrieben.xlsx')

        erwartete_fehlermeldung = "FEHLER:  Gesellschaft 'beispielfirma gmbh' oder 'Bf GmbH' bereits vorhanden!"
        tatsaechliche_fehlermeldung = str(context.exception)
        self.assertTrue(tatsaechliche_fehlermeldung.startswith(erwartete_fehlermeldung))

        # Inhalt aus Tabelle ziehen, um zu pruefen, ob der Datensatz auch nur einmal angelegt wurde
        ergebnis = self.nutzer.abfrage_ausfuehren("SELECT * FROM gesellschaften")

        self.assertEqual(str(ergebnis), "[(1, 1, 'Beispielfirma GmbH', 'Bf GmbH', None)]")

    def test_kein_doppelter_eintrag_abkuerzung_case_insensitive(self):
        """
        Test prueft, ob bei wiederholtem Aufruf der Methode 'insert_gesellschaft' mit derselben Abkuerzung aber mit
        Kleinschreibung dieser dennoch nicht mehrfach eingetragen wird. Beim zweiten Eintrag muss eine Exception
        geworfen werden. Ausloeser ist der unique-constraint, welcher in der Stored Procedure 'insert_gesellschaft'
        implementiert ist, in Kombination mit dem unique-Index 'abk_gesellschaft_idx'.
        """
        self.nutzer.insert_gesellschaft('testdaten_insert_gesellschaft/Gesellschaft.xlsx')

        # Versuch, denselben Wert noch einmal einzutragen (diesmal aber in Kleinschreibung)
        with self.assertRaises(Exception) as context:
            self.nutzer.insert_gesellschaft('testdaten_insert_gesellschaft/Gesellschaft - '
                                            'Abkuerzung klein geschrieben.xlsx')

        erwartete_fehlermeldung = "FEHLER:  Gesellschaft 'Beispielfirma GmbH' oder 'bf gmbh' bereits vorhanden!"
        tatsaechliche_fehlermeldung = str(context.exception)
        self.assertTrue(tatsaechliche_fehlermeldung.startswith(erwartete_fehlermeldung))

        # Inhalt aus Tabelle ziehen, um zu pruefen, ob der Datensatz auch nur einmal angelegt wurde
        ergebnis = self.nutzer.abfrage_ausfuehren("SELECT * FROM gesellschaften")

        self.assertEqual(str(ergebnis), "[(1, 1, 'Beispielfirma GmbH', 'Bf GmbH', None)]")

    def tearDown(self):
        """
        Methode ruft Funktion 'test_tear_down' auf, welches das Datenbankschema 'temp_test_schema' mit allen Daten
        entfernt.
        """
        test_tear_down()
