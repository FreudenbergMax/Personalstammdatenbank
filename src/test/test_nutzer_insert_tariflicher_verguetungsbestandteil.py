import unittest

from src.main.Login import Login
from src.main.Mandant import Mandant
from src.main.test_SetUp_TearDown import test_set_up, test_tear_down


class TestNutzerInsertTariflicherVerguetungsbestandteil(unittest.TestCase):

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

        # Gewerkschaft, Tarif und Verguetungsbestandteil muessen angelegt sein, damit Verguetungsbestandteile mit Tarife
        # verknuepft werden koennen
        self.nutzer.insert_gewerkschaft('testdaten_insert_gewerkschaft/Gewerkschaft.xlsx')
        self.nutzer.insert_tarif('testdaten_insert_tarif/Tarif.xlsx')
        self.nutzer.insert_verguetungsbestandteil('testdaten_insert_verguetungsbestandteil/Verguetungsbestandteil.xlsx')

    def test_erfolgreicher_eintrag(self):
        """
        Test prueft, ob ein Verguetungsbestandteil eingetragen wird.
        """
        self.nutzer.insert_tarifliches_verguetungsbestandteil(
            'testdaten_insert_tariflicher_verguetungsbestandteil/tariflicher Verguetungsbestandteil.xlsx')

        # Inhalte aus Tabellen ziehen, um zu pruefen, ob der Datensatz angelegt wurde
        ergebnis = self.nutzer.abfrage_ausfuehren("SELECT * FROM verguetungsbestandteile")
        self.assertEqual(str(ergebnis), "[(1, 1, 'Grundgehalt', 'jeden Monat')]")

        ergebnis = self.nutzer.abfrage_ausfuehren("SELECT * FROM hat_Verguetungsbestandteil_Tarif")
        self.assertEqual(str(ergebnis), "[(1, 1, 1, Decimal('3330.18'), datetime.date(2023, 5, 1), "
                                        "datetime.date(9999, 12, 31))]")

    def test_kein_doppelter_eintrag(self):
        """
        Test prueft, ob bei wiederholtem Aufruf der Methode 'insert_tariflicher_verguetungsbestandteil' mit demselben
        Verguetungsbestandteil fuer einen Tarif dieser nicht erneut eingetragen wird. Beim zweiten Eintrag muss eine
        Exception geworfen werden. Ausloeser ist der unique-constraint der Tabelle "hat_Verguetungsbestandteil_Tarif"
        der fuer jeden Mandanten die mehrmalige identische Eintragung desselben Verguetungsbestandteils fuer einen Tarif
        verbietet. Falls der Verguetungsbestandteil fuer einen Tarif aktualisiert werden soll, so muss eine
        update-Funktion ausgefuehrt werden (welche im Rahmen dieser Bachelorarbeit nicht implementiert wurde).
        """
        self.nutzer.insert_tarifliches_verguetungsbestandteil(
            'testdaten_insert_tariflicher_verguetungsbestandteil/tariflicher Verguetungsbestandteil.xlsx')

        # Versuch, denselben Wert noch einmal einzutragen
        with self.assertRaises(Exception) as context:
            self.nutzer.insert_tarifliches_verguetungsbestandteil(
                'testdaten_insert_tariflicher_verguetungsbestandteil/tariflicher Verguetungsbestandteil.xlsx')

        erwartete_fehlermeldung = "FEHLER:  Verguetungsbestandteil 'Grundgehalt' fuer Tarif 'A5-1' bereits verknuepft!"
        tatsaechliche_fehlermeldung = str(context.exception)
        self.assertTrue(tatsaechliche_fehlermeldung.startswith(erwartete_fehlermeldung))

        # Inhalt aus Tabelle ziehen, um zu pruefen, ob der Datensatz nur einmal angelegt wurde
        ergebnis = self.nutzer.abfrage_ausfuehren("SELECT * FROM hat_Verguetungsbestandteil_Tarif")
        self.assertEqual(str(ergebnis), "[(1, 1, 1, Decimal('3330.18'), datetime.date(2023, 5, 1), "
                                        "datetime.date(9999, 12, 31))]")

    def test_erfolgreiche_eintraege_klein_geschrieben(self):
        """
        Test prueft, ob bei Aufruf der Methode 'insert_tariflicher_verguetungsbestandteil' eine Verknuepfung zwischen
        Verguetungsbestandteil und Tarif eingetragen wird, wenn der Tarif eine andere Grossschreibung hat, als in
        Tabelle 'Tarife' hinterlegt, aber ansonsten gleich geschrieben ist (in diesem Beispiel: "a5-1" statt wie in
        Tabelle 'Tarife' "A5-1") und der Verguetungsbestandteil eine andere Grossschriebung hat, als in Tabelle
        'Verguetungsbestandteile' hinterlegt, aber ansonsten gleich geschrieben ist (in diesem Beispiel: "grundgehalt"
        statt wie in Tabelle 'Verguetungsbestandteile' "Grundgehalt")
        """
        self.nutzer.insert_tarifliches_verguetungsbestandteil(
            'testdaten_insert_tariflicher_verguetungsbestandteil/tariflicher '
            'Verguetungsbestandteil - Eintraege klein geschrieben.xlsx')

        # Inhalte aus Tabellen ziehen, um zu pruefen, ob der Datensatz nur einmal angelegt wurde
        ergebnis = self.nutzer.abfrage_ausfuehren("SELECT * FROM hat_Verguetungsbestandteil_Tarif")
        self.assertEqual(str(ergebnis), "[(1, 1, 1, Decimal('3330.18'), datetime.date(2023, 5, 1), "
                                        "datetime.date(9999, 12, 31))]")

    def test_kein_eintrag_nicht_existenter_tarif(self):
        """
        Test prueft, ob eine Exception geworfen wird, wenn der Verguetungsbestandteil zu einem Tarif zugeordnet wird,
        die bisher nicht in der Datenbank eingetragen wurde.
        """
        with self.assertRaises(Exception) as context:
            self.nutzer.insert_tarifliches_verguetungsbestandteil(
                'testdaten_insert_tariflicher_verguetungsbestandteil/tariflicher Verguetungsbestandteil - '
                'nicht existenter Tarif.xlsx')

        erwartete_fehlermeldung = "FEHLER:  Bitte erst Tarif 'E8' anlegen!"
        tatsaechliche_fehlermeldung = str(context.exception)
        self.assertTrue(tatsaechliche_fehlermeldung.startswith(erwartete_fehlermeldung))

        # Pruefen, ob auch tatsaechlich aufgrund fehlenden Tarifs kein Datensatz angelegt wurde
        ergebnis = self.nutzer.abfrage_ausfuehren("SELECT * FROM hat_Verguetungsbestandteil_Tarif")
        self.assertEqual(str(ergebnis), "[]")

    def test_kein_eintrag_nicht_existenter_verguetungsbestandteil(self):
        """
        Test prueft, ob eine Exception geworfen wird, wenn ein Tarif zu einem Verguetungsbestandteil zugeordnet wird,
        die bisher nicht in der Datenbank eingetragen wurde.
        """
        with self.assertRaises(Exception) as context:
            self.nutzer.insert_tarifliches_verguetungsbestandteil(
                'testdaten_insert_tariflicher_verguetungsbestandteil/tariflicher Verguetungsbestandteil - '
                'nicht existenter Verguetungsbestandteil.xlsx')

        erwartete_fehlermeldung = "FEHLER:  Bitte erst Verguetungsbestandteil 'Sonderzahlung' anlegen!"
        tatsaechliche_fehlermeldung = str(context.exception)
        self.assertTrue(tatsaechliche_fehlermeldung.startswith(erwartete_fehlermeldung))

        # Pruefen, ob auch tatsaechlich aufgrund fehlenden Tarifs kein Datensatz angelegt wurde
        ergebnis = self.nutzer.abfrage_ausfuehren("SELECT * FROM hat_Verguetungsbestandteil_Tarif")
        self.assertEqual(str(ergebnis), "[]")

    def tearDown(self):
        """
        Methode ruft Funktion 'test_tear_down' auf, welches das Datenbankschema 'temp_test_schema' mit allen Daten
        entfernt.
        """
        test_tear_down()
