import pandas as pd


class Nutzer:

    def __init__(self, vorname, nachname, mandant_id, conn):
        self.vorname = vorname
        self.nachname = nachname
        self.mandant_id = mandant_id
        self.nutzer_id = self._id_erstellen(conn)
        self._in_datenbank_anlegen(conn)

    def get_vorname(self):
        return self.vorname

    def get_nachname(self):
        return self.nachname

    def _id_erstellen(self, conn):
        """
        Methode ruft die stored Procedure 'erstelle_neue_id' auf, welche eine neue Nutzer_ID berechnet und den Wert
        zurückgibt.
        :param conn: Connection zur Personalstammdatenbank
        :return: berechnete Mandant_ID
        """
        neue_id_query = "SELECT erstelle_neue_id('User_ID', 'Nutzer')"

        cur = conn.cursor()
        cur.execute(neue_id_query)
        nutzer_id = cur.fetchall()[0][0]

        return nutzer_id

    def _in_datenbank_anlegen(self, conn):
        """
        Methode ruft die Stored Procedure 'nutzer_anlegen' auf, welche die Daten des Nutzers in der
        Personalstammdatenbank speichert.
        :param conn: Connection zur Personalstammdatenbank
        """
        nutzer_insert_query = f"SELECT nutzer_anlegen({self.nutzer_id}, '{self.vorname}', '{self.nachname}', '{self.mandant_id}')"
        cur = conn.cursor()
        cur.execute(nutzer_insert_query)

        # Commit der Änderungen
        conn.commit()

        # Cursor schließen
        cur.close()

    def select_ausfuehren(self, tabelle, conn):
        """

        :param tabelle:
        :param conn: Connection zur Personalstammdatenbank
        :return:
        """
        cur = conn.cursor()
        cur.execute(f"SELECT select_ausfuehren('{tabelle}', {self.mandant_id})")

    def insert_neuer_mitarbeiter(self, mitarbeiterdaten, conn):
        """
        Diese Methode überträgt die eingetragenen Mitarbeiterdaten (im Rahmen der Bachelorarbeit
        dargestellt durch eine Excel-Datei) in die Datenbank, in dem der Stored Procedure
        'insert_neuer_mitarbeiter' aufgerufen wird.
        :param mitarbeiterdaten: Name der Excel-Datei, dessen Mitarbeiterdaten in die Datenbank
        eingetragen werden sollen.
        :param conn: Connection zur Personalstammdatenbank
        :return:
        """
        pass
        '''
        # Erstellung der Daten wird noch automatisiert
        mandant = self.mandantenname

        # Import der Daten aus der Excel-Datei in das Pandas-Dataframe und Übertrag in Liste "liste_ma_daten"
        df_ma_daten = pd.read_excel(f"Mitarbeiterdaten/{mitarbeiterdaten}", index_col='Daten')
        liste_ma_daten = list(df_ma_daten.iloc[:, 0])
        liste_ma_daten.insert(0, mandant)

        # Ein Cursor-Objekt erstellen
        cur = conn.cursor()

        # Stored Procedure aufrufen
        cur.callproc('insert_neuer_mitarbeiter', liste_ma_daten)

        # Commit der Änderungen
        conn.commit()

        # Cursor schließen
        cur.close()
        '''

    def nutzer_aus_datenbank_entfernen(self, conn):
        """
        Funktion entfernt einen Nutzer aus der Tabelle "Nutzer" der Personalstammdatenbank
        :param conn: Connection zur Personalstammdatenbank
        """
        nutzer_delete_query = f"SELECT nutzer_entfernen({self.nutzer_id}, '{self.vorname}', '{self.nachname}', '{self.mandant_id}')"
        cur = conn.cursor()
        cur.execute(nutzer_delete_query)

        # Commit der Änderungen
        conn.commit()

        # Cursor schließen
        cur.close()
