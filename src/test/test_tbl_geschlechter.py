"""
Für jede Tabelle wird eine py-Testdatei erzeugt. Folgende Tests müssen mindestens für jede Tabelle durchgeführt werden:
- insert-Befehl wird erfolgreich ausgeführt, sofern übergegebener Datensatz noch nicht existiert
- insert-Befehl fügt keine Daten ein, wenn die einzufügenden Daten bereits existieren
- delete-Befehl wird erfolgreich ausgeführt
- RLS funktioniert --> Mandant A sieht keine Daten von Mandant B

Bei Assoziationen kommen noch hinzu:
- insert Fehlermeldung soll erscheinen, wenn zwei datensätze denselben primary key (zusammengesetzt aus 'Mitarbeiter_ID'
    und 'Datum_Bis') haben
- update-Befehl wird ausgeführt
    - "Datum_bis" wird von '9999-12-31' auf das letzte Datum umgestellt, wo der Eintrag gültig ist
    - die Änderung (=neuer Datensatz) wird erfolgreich eingefügt
    - Die Fremdschlüssel stimmen
"""

import unittest

from src.main.test_SetUp import test_set_up
from src.main.Mandant import Mandant


class TestExistenzStrDatenFeststellen(unittest.TestCase):

    def setUp(self):
        """
        Methode erstellt ein Testschema 'temp_test_schema' und darin die Personalstammdatenbank
        mit allen Tabellen und Stored Procedures. So können alle Tests ausgeführt werden, ohne die
        originale Datenbank zu manipulieren.
        """
        self.conn, self.cursor = test_set_up()
        self.testfirma = Mandant('Testfirma', self.conn)
        self.testunternehmen = Mandant('Testunternehmen', self.conn)

    def test_insert_neue_Daten(self):
        """
        Test prüft, ob die Stored-Procedure-Methode 'insert_tbl_geschlechter' die übergegebenen Daten richtig in der
        Datenbank in der Tabelle 'Geschlechter' anlegt.
        """
        p_mandant_id = self.testfirma.get_mandant_id()
        p_geschlecht = 'weiblich'

        # Befehl übergeben, ausführen, anschließend committen
        insert_query = f"SELECT insert_tbl_geschlechter({p_mandant_id}, '{p_geschlecht}')"
        self.cursor.execute(insert_query)
        self.conn.commit()

        # Daten aus Tabelle "Geschlechter" lesen
        select_query = f"SELECT * FROM geschlechter"
        self.cursor.execute(select_query)
        self.conn.commit()

        # Prüfung, ob die in der Tabelle 'Geschlechter' gespeicherten Daten wie übergeben gespeichert wurden
        geschlecht_id, mandant_id, geschlecht = self.cursor.fetchall()[0]
        self.assertEqual(geschlecht_id, 1)
        self.assertEqual(mandant_id, 1)
        self.assertEqual(geschlecht, 'weiblich')

    def test_bekannte_Daten(self):
        """
        Test prüft, ob die Notice geworfen wird, wenn ein Datensatz in die Tabelle 'Gechlechter' eingetragen werden
        soll, der inhaltlich bereits vorhanden ist.
        """
        p_mandant_id = self.testfirma.get_mandant_id()
        p_geschlecht = 'weiblich'

        # insert-Befehl zum ersten mal übergeben, ausführen, anschließend committen
        insert_query = f"SELECT insert_tbl_geschlechter({p_mandant_id}, '{p_geschlecht}')"
        self.cursor.execute(insert_query)
        self.conn.commit()

        # insert-Befehl ein weiteres Mal ausführen. Nun dürfte kein weiterer Eintrag erfolgen
        insert_query = f"SELECT insert_tbl_geschlechter({p_mandant_id}, '{p_geschlecht}')"
        self.cursor.execute(insert_query)
        self.conn.commit()

        # Daten aus Tabelle "Geschlechter" lesen
        select_query = f"SELECT * FROM geschlechter"
        self.cursor.execute(select_query)
        self.conn.commit()
        result = str(self.cursor.fetchall())

        # Wenn unique-constraint nicht funktionieren würde, wäre 'result' = '[(1, 1, 'weiblich'), (1, 1, 'weiblich')]'.
        #  Da der unique-constraint aber gelten soll, darf nur '[(1, 1, 'weiblich')]' rauskommen.
        self.assertNotEqual(result, "[(1, 1, 'weiblich'), (1, 1, 'weiblich')]")
        self.assertEqual(result, "[(1, 1, 'weiblich')]")

    def test_rls_in_tbl_geschlechter(self):
        """
        Test prueft, ob Row Level Security in Tabelle 'Geschlechter' funktioniert. Das bedeutet, dass Mandant
        'testfirma' keine Daten von Mandant 'testunternehmen' sehen kann und umgekehrt.
        """
        pass

    def test_alle_daten_entfernt(self):
        """
        Test prüft, ob alle Daten eines Mandanten nach Ausführung der entsprechenden Stored Procedures entfernt sind.
        """
        pass

    def tearDown(self):
        """
        Methode entfernt das Test-Schema 'temp_test_schema' inkl. der darin enthaltenen Test-
        Personalstammdatenbank mit allen ihren Tabellen, Stored Procedures und Daten, die während
        der Testfälle erzeugt wurden.
        """
        self.cursor.execute(f"set role postgres;\n DROP SCHEMA temp_test_schema CASCADE")
        self.conn.commit()
        self.cursor.close()
        self.conn.close()

