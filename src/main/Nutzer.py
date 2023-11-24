import pandas as pd
from datetime import datetime


class Nutzer:

    def __init__(self, vorname, nachname, mandant_id, conn):

        if not isinstance(vorname, str):
            raise (TypeError("Der Vorname des Nutzers muss ein String sein."))

        if "postgres" in str.lower(vorname):
            raise(ValueError(f"Dieser Vorname ist nicht erlaubt: {vorname}."))

        if vorname == "":
            raise(ValueError(f"Der Vorname des Nutzers muss aus mindestens einem Zeichen bestehen."))

        if len(vorname) > 64:
            raise(ValueError(f"Der Vorname darf höchstens 64 Zeichen lang sein."))

        if not isinstance(nachname, str):
            raise (TypeError("Der Nachname des Nutzers muss ein String sein."))

        if "postgres" in str.lower(nachname):
            raise(ValueError(f"Dieser Nachname ist nicht erlaubt: {nachname}."))

        if nachname == "":
            raise(ValueError(f"Der Nachname des Nutzers muss aus mindestens einem Zeichen bestehen."))

        if len(nachname) > 64:
            raise(ValueError(f"Der Nachname darf höchstens 64 Zeichen lang sein."))

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
        neue_id_query = "SELECT erstelle_neue_id('nutzer_id', 'Nutzer')"

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
        # Import der Daten aus der Excel-Datei in das Pandas-Dataframe und Übertrag in Liste "liste_ma_daten"
        df_ma_daten = pd.read_excel(f"Mitarbeiterdaten/{mitarbeiterdaten}", index_col='Daten', na_filter=False)
        liste_ma_daten = list(df_ma_daten.iloc[:, 0])
        liste_ma_daten.insert(0, self.mandant_id)

        if liste_ma_daten[5] == '':
            liste_ma_daten[5] = None
        else:
            liste_ma_daten[5] = datetime.strptime(liste_ma_daten[5], '%d.%m.%Y').date()

        if liste_ma_daten[6] == '':
            liste_ma_daten[6] = None
        else:
            liste_ma_daten[6] = datetime.strptime(liste_ma_daten[6], '%d.%m.%Y').date()

        if liste_ma_daten[14] == '':
            liste_ma_daten[14] = datetime.strptime('31.12.9999', '%d.%m.%Y').date()
        else:
            liste_ma_daten[14] = datetime.strptime(liste_ma_daten[14], '%d.%m.%Y').date()

        for i in range(0, len(liste_ma_daten)):
            print(f"{i}: {liste_ma_daten[i]}; Datentyp: {type(liste_ma_daten[i])}")

        # Ein Cursor-Objekt erstellen
        cur = conn.cursor()

        # Stored Procedure aufrufen
        cur.callproc('insert_mitarbeiterdaten', [liste_ma_daten[0], str(liste_ma_daten[1]), liste_ma_daten[2], liste_ma_daten[3], liste_ma_daten[4], liste_ma_daten[5], liste_ma_daten[6], liste_ma_daten[7], liste_ma_daten[8], liste_ma_daten[9], liste_ma_daten[10], liste_ma_daten[11], liste_ma_daten[12], liste_ma_daten[13], liste_ma_daten[14], liste_ma_daten[15], str(liste_ma_daten[16]), str(liste_ma_daten[17]), liste_ma_daten[18], liste_ma_daten[19], liste_ma_daten[20]])

        # Commit der Änderungen
        conn.commit()

        # Cursor schließen
        cur.close()

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

        conn.close()
