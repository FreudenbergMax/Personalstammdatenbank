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

        personalnummer = str(self._existenz_pflichtdaten_pruefen(liste_ma_daten[0], 'Personalnummer'))
        vorname = str(self._existenz_pflichtdaten_pruefen(liste_ma_daten[1], 'Vorname'))
        zweitname = self._existenz_optionale_str_daten_feststellen(liste_ma_daten[2])
        nachname = str(self._existenz_pflichtdaten_pruefen(liste_ma_daten[3], 'Nachname'))
        geburtsdatum = datetime.strptime(self._existenz_pflichtdaten_pruefen(liste_ma_daten[4], 'Geburtsdatum'), '%d.%m.%Y').date()
        eintrittsdatum = datetime.strptime(self._existenz_pflichtdaten_pruefen(liste_ma_daten[5], 'Eintrittsdatum'), '%d.%m.%Y').date()
        steuernummer = self._existenz_optionale_str_daten_feststellen(liste_ma_daten[6])
        sozialversicherungsnummer = self._existenz_optionale_str_daten_feststellen(liste_ma_daten[7])
        iban = self._existenz_optionale_str_daten_feststellen(liste_ma_daten[8])
        private_telefonnummer = self._existenz_optionale_str_daten_feststellen(liste_ma_daten[9])
        private_email = self._existenz_optionale_str_daten_feststellen(liste_ma_daten[10])
        dienstliche_telefonnummer = self._existenz_optionale_str_daten_feststellen(liste_ma_daten[11])
        dienstliche_email = self._existenz_optionale_str_daten_feststellen(liste_ma_daten[12])
        austrittsdatum = self._existenz_optionale_date_daten_feststellen(liste_ma_daten[13])
        strasse = str(self._existenz_pflichtdaten_pruefen(liste_ma_daten[14], 'Strasse'))
        hausnummer = str(self._existenz_pflichtdaten_pruefen(liste_ma_daten[15], 'Hausnummer'))
        postleitzahl = str(self._existenz_pflichtdaten_pruefen(liste_ma_daten[16], 'Postleitzahl'))
        stadt = str(self._existenz_pflichtdaten_pruefen(liste_ma_daten[17], 'Stadt'))
        region = str(self._existenz_pflichtdaten_pruefen(liste_ma_daten[18], 'Region'))
        land = str(self._existenz_pflichtdaten_pruefen(liste_ma_daten[19], 'Land'))

        # Ein Cursor-Objekt erstellen
        cur = conn.cursor()

        # Stored Procedure aufrufen
        cur.callproc('insert_mitarbeiterdaten', [self.mandant_id,
                                                 personalnummer,
                                                 vorname,
                                                 zweitname,
                                                 nachname,
                                                 geburtsdatum,
                                                 eintrittsdatum,
                                                 steuernummer,
                                                 sozialversicherungsnummer,
                                                 iban,
                                                 private_telefonnummer,
                                                 private_email,
                                                 dienstliche_telefonnummer,
                                                 dienstliche_email,
                                                 austrittsdatum,
                                                 strasse,
                                                 hausnummer,
                                                 postleitzahl,
                                                 stadt,
                                                 region,
                                                 land])

        # Commit der Änderungen
        conn.commit()

        # Cursor schließen
        cur.close()

    def _existenz_optionale_str_daten_feststellen(self, str_daten):
        """
        Funktion stellt fest, ob optionale Daten vorliegen oder nicht
        :param str_daten: wird untersucht, ob Daten darin enthalten sind
        :return: Falls Parameter 'daten' keine Daten enthält, wird None zurückgegeben, sonst Daten
        """
        if str_daten == '':
            str_daten = None
        else:
            str_daten = str(str_daten)

        return str_daten

    def _existenz_optionale_date_daten_feststellen(self, date_daten):
        """
        Funktion stellt fest, ob optionale Daten vorliegen oder nicht
        :param date_daten: wird untersucht, ob Daten darin enthalten sind
        :return: Falls Parameter 'daten' keine Daten enthält, wird None zurückgegeben, sonst Daten
        """
        if date_daten == '':
            date_daten = None
        else:
            date_daten = datetime.strptime(date_daten, '%d.%m.%Y').date()

        return date_daten

    def _existenz_pflichtdaten_pruefen(self, dateninhalt, art):
        """
        prüft, ob Daten, die zwingend für den Dateneintrag notwendig sind (z.B. Name, Adresse) , auch vorhanden sind
        :param dateninhalt: zu prüfende Pflichtdaten
        :param art: gibt an, um was für Daten es sich handeln soll
        :return: Daten, sofern sie in Ordnung sind
        """
        if dateninhalt == '':
            raise(ValueError(f"{art} ist nicht vorhanden."))

        return dateninhalt

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
