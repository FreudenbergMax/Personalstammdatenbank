import unittest

from src.main.Login import Login
from src.main.Mandant import Mandant
from src.main.test_SetUp_TearDown import test_set_up, test_tear_down


class TestNutzerUpdateAbteilungshierarchie(unittest.TestCase):

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

        self.nutzer.insert_abteilung('testdaten_update_abteilungshierarchie/Unterabteilung.xlsx')

        self.nutzer.insert_abteilung('testdaten_update_abteilungshierarchie/Oberabteilung.xlsx')

    def test_erfolgreicher_eintrag(self):
        """
        Test prueft, ob eine Abteilungshierarchie erstellt wird
        """
        self.nutzer.update_erstelle_abteilungshierarchie(
            'testdaten_update_abteilungshierarchie/Update Abteilungshierarchie.xlsx')

        # pruefen, in fuer Abteilung "HR PC" der Fremdschluessel fuer uebergeordnete Abteilung "HR" hinterlegt ist
        ergebnis = self.nutzer.abfrage_ausfuehren("SELECT * FROM abteilungen")
        self.assertEqual(str(ergebnis), "[(1, 1, 'Human Resources Personalcontrolling', 'HR PC', 2), "
                                        "(2, 1, 'Human Resources', 'HR', None)]")

    def test_erfolgreicher_eintrag_case_insensitive(self):
        """
        Test prueft, ob eine Abteilungshierarchie erstellt wird, wenn in der Excel-Datei die Abteilungen klein- in der
        Tabelle "Abteilungen" aber gross geschrieben sind. Beispiel: "human resources" statt "Human Resources"
        """
        self.nutzer.update_erstelle_abteilungshierarchie(
            'testdaten_update_abteilungshierarchie/Update Abteilungshierarchie - klein geschrieben.xlsx')

        # pruefen, in fuer Abteilung "HR PC" der Fremdschluessel fuer uebergeordnete Abteilung "HR" hinterlegt ist
        ergebnis = self.nutzer.abfrage_ausfuehren("SELECT * FROM abteilungen")
        self.assertEqual(str(ergebnis), "[(1, 1, 'Human Resources Personalcontrolling', 'HR PC', 2), "
                                        "(2, 1, 'Human Resources', 'HR', None)]")

    def test_unterabteilung_existiert_nicht(self):
        """
        Test prueft, ob eine Exception geworfen wird, wenn Unterabteilung nicht existiert. Beispiel: "Human Resources
        Personal Controlling" statt "Human Resources Personalcontrolling" (fehlerhafterweise Leerzeichen zwischen
        "Personal" und "Controlling")
        """
        with self.assertRaises(Exception) as context:
            self.nutzer.update_erstelle_abteilungshierarchie(
                'testdaten_update_abteilungshierarchie/Update Abteilungshierarchie - '
                'Unterabteilung nicht existent.xlsx')

        erwartete_fehlermeldung = "FEHLER:  Die untergeordnete Abteilung 'Human Resources Personal Controlling' ist " \
                                  "nicht angelegt!"
        tatsaechliche_fehlermeldung = str(context.exception)
        self.assertTrue(tatsaechliche_fehlermeldung.startswith(erwartete_fehlermeldung))

    def test_oberabteilung_existiert_nicht(self):
        """
        Test prueft, ob eine Exception geworfen wird, wenn Oberabteilung nicht existiert. Beispiel: "HumanResources"
        statt "Human Resources " (fehlerhafterweise kein Leerzeichen zwischen "Human" und "Resources")
        """
        with self.assertRaises(Exception) as context:
            self.nutzer.update_erstelle_abteilungshierarchie(
                'testdaten_update_abteilungshierarchie/Update Abteilungshierarchie - Oberabteilung nicht existent.xlsx')

        erwartete_fehlermeldung = "FEHLER:  Die uebergeordnete Abteilung 'HumanResources' ist nicht angelegt!"
        tatsaechliche_fehlermeldung = str(context.exception)
        self.assertTrue(tatsaechliche_fehlermeldung.startswith(erwartete_fehlermeldung))

    def tearDown(self):
        """
        Methode ruft Funktion 'test_tear_down' auf, welches das Datenbankschema 'temp_test_schema' mit allen Daten
        entfernt.
        """
        test_tear_down()
