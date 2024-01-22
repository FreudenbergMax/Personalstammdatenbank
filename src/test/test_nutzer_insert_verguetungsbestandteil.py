import unittest

from src.main.Login import Login
from src.main.Mandant import Mandant
from src.main.test_SetUp_TearDown import test_set_up, test_tear_down


class TestNutzerInsertVerguetungsbestandteil(unittest.TestCase):

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
        Test prueft, ob ein Verguetungsbestandteil eingetragen wird.
        """
        self.nutzer.insert_verguetungsbestandteil('testdaten_insert_verguetungsbestandteil/Verguetungsbestandteil.xlsx')

        # Inhalte aus Tabellen ziehen, um zu pruefen, ob der Datensatz angelegt wurde
        ergebnis = self.nutzer.abfrage_ausfuehren("SELECT * FROM verguetungsbestandteile")
        self.assertEqual(str(ergebnis), "[(1, 1, 'Grundgehalt', 'jeden Monat')]")

    def test_kein_doppelter_eintrag(self):
        """
        Test prueft, ob bei wiederholtem Aufruf der Methode 'insert_verguetungsbestandteil' mit demselben Verguetungs-
        bestandteil dieser nicht erneut eingetragen wird. Beim zweiten Eintrag muss eine Exception geworfen werden.
        Ausloeser ist der unique-constraint der Tabelle "Verguetungsbestandteile" der fuer jeden Mandanten die
        mehrmalige identische Eintragung desselben Verguetungsbestandteile und Auszahlungsmonats verbietet. Falls ein
        Verguetungsbestandteil aktualisiert werden soll, so muss eine update-Funktion ausgefuehrt werden (welche im
        Rahmen dieser Bachelorarbeit nicht implementiert wurde).
        """
        self.nutzer.insert_verguetungsbestandteil('testdaten_insert_verguetungsbestandteil/Verguetungsbestandteil.xlsx')

        # Versuch, denselben Wert noch einmal einzutragen
        with self.assertRaises(Exception) as context:
            self.nutzer.insert_verguetungsbestandteil(
                'testdaten_insert_verguetungsbestandteil/Verguetungsbestandteil.xlsx')

        erwartete_fehlermeldung = "FEHLER:  Verguetungsbestandteil 'Grundgehalt' bereits vorhanden!"
        tatsaechliche_fehlermeldung = str(context.exception)
        self.assertTrue(tatsaechliche_fehlermeldung.startswith(erwartete_fehlermeldung))

        # Inhalte aus Tabellen ziehen, um zu pruefen, ob der Datensatz nur einmal angelegt wurde
        ergebnis = self.nutzer.abfrage_ausfuehren("SELECT * FROM verguetungsbestandteile")
        self.assertEqual(str(ergebnis), "[(1, 1, 'Grundgehalt', 'jeden Monat')]")

    def test_kein_doppelter_eintrag_case_insensitive(self):
        """
        Test prueft, ob bei wiederholtem Aufruf der Methode 'insert_verguetungsbestandteil' mit demselben Verguetungs-
        bestandteil aber mit Kleinschreibung dieser dennoch nicht erneut eingetragen wird. Beim zweiten Eintrag muss
        eine Exception geworfen werden. Ausloeser ist der unique-constraint in Kombination mit dem unique-Index
        'verguetungsbestandteil_idx'. Falls ein Verguetungsbestandteil aktualisiert werden soll, so muss eine
        update-Funktion ausgefuehrt werden (welche im Rahmen dieser Bachelorarbeit nicht implementiert wurde).
        """
        self.nutzer.insert_verguetungsbestandteil('testdaten_insert_verguetungsbestandteil/Verguetungsbestandteil.xlsx')

        # Versuch, denselben Wert noch einmal einzutragen
        with self.assertRaises(Exception) as context:
            self.nutzer.insert_verguetungsbestandteil(
                'testdaten_insert_verguetungsbestandteil/Verguetungsbestandteil - Verguetungsbestandteil klein '
                'geschrieben.xlsx')

        erwartete_fehlermeldung = "FEHLER:  Verguetungsbestandteil 'grundgehalt' bereits vorhanden!"
        tatsaechliche_fehlermeldung = str(context.exception)
        self.assertTrue(tatsaechliche_fehlermeldung.startswith(erwartete_fehlermeldung))

        # Inhalte aus Tabellen ziehen, um zu pruefen, ob der Datensatz nur einmal angelegt wurde
        ergebnis = self.nutzer.abfrage_ausfuehren("SELECT * FROM verguetungsbestandteile")
        self.assertEqual(str(ergebnis), "[(1, 1, 'Grundgehalt', 'jeden Monat')]")

    def test_falscher_eintrag(self):
        """
        Test prueft, ob eine Exception geworfen wird, wenn die geforderte Rechtschreibung fuer den Auszahlungsmonat
        nicht eingehalten wird. Ausloeser der Exception ist der check-constraint, welcher in der Stored Procedure
        'insert_verguetungsbestandteil' implementiert ist bzw. in der Tabelle 'Verguetungsbestandteile'.
        Hinweis: die Excel-Datei ist fuer gewoehnlich so praepariert, dass man nur die richtige Rechtschreibung
        eintragen kann. Dennoch soll getestet werden, ob im Ernstfall der constraint greift. Hierfuer wurde die Excel-
        Datei so umgestaltet, dass man auch falsch geschriebene Auszahlungamonate eintragen kann.
        """
        # Versuch, falsch geschriebenes Auszahlungsmonat 'in jedem Monat' einzutragen
        with self.assertRaises(Exception) as context:
            self.nutzer.insert_verguetungsbestandteil(
                'testdaten_insert_verguetungsbestandteil/Verguetungsbestandteil - Auszahlungsmonat falsch.xlsx')

        # Inhalt aus Tabelle ziehen, um zu pruefen, ob kein Datensatz angelegt wurde
        ergebnis = self.nutzer.abfrage_ausfuehren("SELECT * FROM verguetungsbestandteile")
        self.assertEqual(str(ergebnis), "[]")

    def tearDown(self):
        """
        Methode ruft Funktion 'test_tear_down' auf, welches das Datenbankschema 'temp_test_schema' mit allen Daten
        entfernt.
        """
        test_tear_down()
