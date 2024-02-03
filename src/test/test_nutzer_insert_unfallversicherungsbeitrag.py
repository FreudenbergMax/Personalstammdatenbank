import unittest

from src.main.Login import Login
from src.main.test_SetUp_TearDown import test_set_up, test_tear_down


class TestNutzerInsertUnfallversicherungsbeitrag(unittest.TestCase):

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

        self.nutzer.insert_berufsgenossenschaft('testdaten_insert_berufsgenossenschaft/Berufsgenossenschaft.xlsx')
        self.nutzer.insert_unternehmen('testdaten_insert_unternehmen/Unternehmen.xlsx')

    def test_erfolgreicher_eintrag(self):
        """
        Test prueft, ob der Unfallversicherungsbeitrag fuer ein Unternehmen eingetragen wird.
        """
        self.nutzer.insert_unfallversicherungsbeitrag(
            'testdaten_insert_unfallversicherungsbeitrag/Unfallversicherungsbeitrag.xlsx')

        # Inhalt aus Tabelle ziehen, um zu pruefen, ob der Datensatz angelegt wurde
        ergebnis = self.nutzer.abfrage_ausfuehren("SELECT * FROM unfallversicherungsbeitraege")

        self.assertEqual(str(ergebnis), "[(1, 1, 1, Decimal('6543123.89'), 2023)]")

    def test_kein_doppelter_eintrag(self):
        """
        Test prueft, ob bei wiederholtem Aufruf der Methode 'insert_unfallversicherungsbeitrag' mit derselben
        Berufsgenossenschaft dieser nicht erneut eingetragen wird. Beim zweiten Eintrag muss eine Fehlermeldung
        erscheinen.
        """
        self.nutzer.insert_unfallversicherungsbeitrag(
            'testdaten_insert_unfallversicherungsbeitrag/Unfallversicherungsbeitrag.xlsx')

        # Versuch, denselben Wert noch einmal einzutragen
        with self.assertRaises(Exception) as context:
            self.nutzer.insert_unfallversicherungsbeitrag(
                'testdaten_insert_unfallversicherungsbeitrag/Unfallversicherungsbeitrag.xlsx')

        erwartete_fehlermeldung = "FEHLER:  Unfallversicherungsbeitrag ist fuer das Jahr '2023' bereits vermerkt!"
        tatsaechliche_fehlermeldung = str(context.exception)
        self.assertTrue(tatsaechliche_fehlermeldung.startswith(erwartete_fehlermeldung))

        # Inhalt aus Tabelle ziehen, um zu pruefen, ob der Datensatz auch nur einmal angelegt wurde
        ergebnis = self.nutzer.abfrage_ausfuehren("SELECT * FROM unfallversicherungsbeitraege")

        self.assertEqual(str(ergebnis), "[(1, 1, 1, Decimal('6543123.89'), 2023)]")

    def test_Eintrag_Folgejahr_moeglich(self):
        """
        Test prueft, ob fuer das Folgejahr der Eintrag der Unfallversicheurngsbeitraege fuer dieselbe Gesellschaft mit
        derselben Berufsgenossenschaft moeglich ist.
        """
        self.nutzer.insert_unfallversicherungsbeitrag(
            'testdaten_insert_unfallversicherungsbeitrag/Unfallversicherungsbeitrag.xlsx')

        self.nutzer.insert_unfallversicherungsbeitrag(
            'testdaten_insert_unfallversicherungsbeitrag/Unfallversicherungsbeitrag - Folgejahr.xlsx')

        # Inhalt aus Tabelle ziehen, um zu pruefen, ob der Datensatz auch nur einmal angelegt wurde
        ergebnis = self.nutzer.abfrage_ausfuehren("SELECT * FROM unfallversicherungsbeitraege")

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
        self.nutzer.insert_unfallversicherungsbeitrag(
            'testdaten_insert_unfallversicherungsbeitrag/Unfallversicherungsbeitrag - klein geschrieben.xlsx')

        # Inhalt aus Tabelle ziehen, um zu pruefen, ob der Datensatz angelegt wurde
        ergebnis = self.nutzer.abfrage_ausfuehren("SELECT * FROM unfallversicherungsbeitraege")

        self.assertEqual(str(ergebnis), "[(1, 1, 1, Decimal('6543123.89'), 2023)]")

    def tearDown(self):
        """
        Methode ruft Funktion 'test_tear_down' auf, welches das Datenbankschema 'temp_test_schema' mit allen Daten
        entfernt.
        """
        test_tear_down()
