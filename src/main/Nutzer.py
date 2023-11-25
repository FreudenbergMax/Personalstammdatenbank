import pandas as pd
import re
from datetime import datetime


class Nutzer:

    def __init__(self, vorname, nachname, mandant_id, conn):

        if not isinstance(vorname, str):
            raise (TypeError("Der Vorname des Nutzers muss ein String sein."))

        if "postgres" in str.lower(vorname):
            raise (ValueError(f"Dieser Vorname ist nicht erlaubt: {vorname}."))

        if vorname == "":
            raise (ValueError(f"Der Vorname des Nutzers muss aus mindestens einem Zeichen bestehen."))

        if len(vorname) > 64:
            raise (ValueError(f"Der Vorname darf höchstens 64 Zeichen lang sein. "
                              f"'{vorname}' besitzt {len(vorname)} Zeichen!"))

        if not isinstance(nachname, str):
            raise (TypeError("Der Nachname des Nutzers muss ein String sein."))

        if "postgres" in str.lower(nachname):
            raise (ValueError(f"Dieser Nachname ist nicht erlaubt: {nachname}."))

        if nachname == "":
            raise (ValueError(f"Der Nachname des Nutzers muss aus mindestens einem Zeichen bestehen."))

        if len(nachname) > 64:
            raise (ValueError(f"Der Nachname darf höchstens 64 Zeichen lang sein. "
                              f"'{nachname}' besitzt {len(nachname)} Zeichen!"))

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

        personalnummer = self._existenz_str_daten_feststellen(liste_ma_daten[0], 'Personalnummer', 32, True)
        vorname = self._existenz_str_daten_feststellen(liste_ma_daten[1], 'Vorname', 64, True)
        zweitname = self._existenz_str_daten_feststellen(liste_ma_daten[2], 'Zweitname', 128, False)
        nachname = self._existenz_str_daten_feststellen(liste_ma_daten[3], 'Nachname', 64, True)
        geburtsdatum = self._existenz_date_daten_feststellen(liste_ma_daten[4], 'Geburtsdatum', True)
        eintrittsdatum = self._existenz_date_daten_feststellen(liste_ma_daten[5], 'Eintrittsdatum', True)
        steuernummer = self._existenz_str_daten_feststellen(liste_ma_daten[6], 'Steuernummer', 32, False)
        sozialversicherungsnummer = self._existenz_str_daten_feststellen(liste_ma_daten[7], 'Sozialversicherungsnummer',
                                                                         32, False)
        iban = self._existenz_str_daten_feststellen(liste_ma_daten[8], 'IBAN', 32, False)
        private_telefonnummer = self._existenz_str_daten_feststellen(liste_ma_daten[9], 'private Telefonnummer',
                                                                     16, False)
        private_email = self._existenz_str_daten_feststellen(liste_ma_daten[10], 'private E-Mail', 64, True)
        dienstliche_telefonnummer = self._existenz_str_daten_feststellen(liste_ma_daten[11], 'dienstliche Telefonnummer'
                                                                         , 16, False)
        dienstliche_email = self._existenz_str_daten_feststellen(liste_ma_daten[12], 'dienstliche E-Mail', 64, False)
        austrittsdatum = self._existenz_date_daten_feststellen(liste_ma_daten[13], 'Austrittsdatum', False)
        strasse = self._existenz_str_daten_feststellen(liste_ma_daten[14], 'Strasse', 64, True)
        hausnummer = self._existenz_str_daten_feststellen(liste_ma_daten[15], 'Hausnummer', 8, True)
        postleitzahl = self._existenz_str_daten_feststellen(liste_ma_daten[16], 'Postleitzahl', 16, True)
        stadt = self._existenz_str_daten_feststellen(liste_ma_daten[17], 'Stadt', 128, True)
        region = self._existenz_str_daten_feststellen(liste_ma_daten[18], 'Region', 128, True)
        land = self._existenz_str_daten_feststellen(liste_ma_daten[19], 'Land', 128, True)

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

    def _existenz_str_daten_feststellen(self, str_daten, art, anzahl_zeichen, pflicht):
        """
        Methode stellt fest, ob optionale Daten vorliegen oder nicht und wenn ja, so sollen diese auf jeden Fall
        als String zurückgegeben werden. So soll sichergestellt werden, dass dem Datenbanksystem die Daten in dem
        Datentyp übergeben werden, in der sie in der Personalstammdatenbank gespeichert werden können.
        :param str_daten: wird untersucht, ob Daten darin enthalten sind
        :param art: gibt an, um was für Daten es sich handeln soll
        :param anzahl_zeichen: Anzahl der Zeichen, die der Inhalt von 'str_daten' höchstens besitzen darf
        :param pflicht: boolean, der bei 'True' angibt, dass 'str_daten' kein leerer String sein darf
        :return: Falls Parameter 'daten' keine Daten enthält, wird None zurückgegeben, sonst Daten
        """
        if str_daten == '' and not pflicht:
            str_daten = None
        elif str_daten == '' and pflicht:
            raise (ValueError(f"{art} ist nicht vorhanden."))
        else:
            str_daten = str(str_daten)
            if len(str_daten) > anzahl_zeichen:
                raise (ValueError(f"{art} darf höchstens {anzahl_zeichen} Zeichen lang sein. "
                                  f"{str_daten} besitzt {len(str_daten)} Zeichen!"))

        return str_daten

    '''
    def _existenz_optionale_str_daten_feststellen(self, str_daten, art, anzahl_zeichen):
        """
        Methode stellt fest, ob optionale Daten vorliegen oder nicht und wenn ja, so sollen diese auf jeden Fall
        als String zurückgegeben werden. So soll sichergestellt werden, dass dem Datenbanksystem die Daten in dem
        Datentyp übergeben werden, in der sie in der Personalstammdatenbank gespeichert werden können.
        :param str_daten: wird untersucht, ob Daten darin enthalten sind
        :param art: gibt an, um was für Daten es sich handeln soll
        :param anzahl_zeichen: Anzahl der Zeichen, die der Inhalt von 'str_daten' höchstens besitzen darf
        :return: Falls Parameter 'daten' keine Daten enthält, wird None zurückgegeben, sonst Daten
        """
        if str_daten == '':
            str_daten = None
        else:
            str_daten = str(str_daten)
            if len(str_daten) > anzahl_zeichen:
                raise (ValueError(f"{art} darf höchstens {anzahl_zeichen} Zeichen lang sein. "
                                  f"{str_daten} besitzt {len(str_daten)} Zeichen!"))

        return str_daten

    def existenz_str_pflichtdaten_pruefen(self, str_daten, art, anzahl_zeichen):
        """
        prüft, ob Daten, die zwingend für den Dateneintrag notwendig sind (z.B. Name, Adresse) , auch vorhanden sind
        :param str_daten: zu prüfende Pflichtdaten
        :param art: gibt an, um was für Daten es sich handeln soll
        :param anzahl_zeichen: Anzahl der Zeichen, die der Inhalt von 'str_daten' höchstens besitzen darf.
                               Standarddatentyp ist 'None', damit dieser Parameter optional ist, diese Methode auch für
                               Nicht-Strings verwendet wird. Zahlen bspw. haben keine Zeichenlänge.
        :return: Daten, sofern sie in Ordnung sind
        """
        if str_daten == '':
            raise (ValueError(f"{art} ist nicht vorhanden."))
        else:
            str_daten = str(str_daten)
            if len(str_daten) > anzahl_zeichen:
                raise (ValueError(f"{art} darf höchstens {anzahl_zeichen} Zeichen lang sein. "
                                  f"{str_daten} besitzt {len(str_daten)} Zeichen!"))

        return str_daten
    '''

    def _existenz_date_daten_feststellen(self, date_daten, art, pflicht):
        """
        Methode stellt fest, ob optionale Daten vorliegen oder nicht und wenn ja, so sollen diese auf jeden Fall
        als Date-Datentyp zurückgegeben werden. So soll sichergestellt werden, dass dem Datenbanksystem die Daten in dem
        Datentyp übergeben werden, in der sie in der Personalstammdatenbank gespeichert werden können.
        :param date_daten: wird untersucht, ob Daten darin enthalten sind
        :param art: gibt an, um was für Daten es sich handeln soll
        :param pflicht: boolean, der bei 'True' angibt, dass 'date_daten' kein leerer String sein darf
        :return: Falls Parameter 'daten' keine Daten enthält, wird None zurückgegeben, sonst Daten
        """
        if date_daten == '' and not pflicht:
            date_daten = None
        elif date_daten == '' and pflicht:
            raise (ValueError(f"{art} ist nicht vorhanden."))
        elif not re.compile(r'\d{2}\.\d{2}\.\d{4}').fullmatch(date_daten):
            raise (ValueError(f"{date_daten} hat nicht das Muster 'TT.MM.JJJJ'!"))
        else:
            date_daten = datetime.strptime(date_daten, '%d.%m.%Y').date()

        return date_daten
    '''
    def _existenz_optionale_date_daten_feststellen(self, date_daten):
        """
        Methode stellt fest, ob optionale Daten vorliegen oder nicht und wenn ja, so sollen diese auf jeden Fall
        als Date-Datentyp zurückgegeben werden. So soll sichergestellt werden, dass dem Datenbanksystem die Daten in dem
        Datentyp übergeben werden, in der sie in der Personalstammdatenbank gespeichert werden können.
        :param date_daten: wird untersucht, ob Daten darin enthalten sind
        :return: Falls Parameter 'daten' keine Daten enthält, wird None zurückgegeben, sonst Daten
        """
        if date_daten == '':
            date_daten = None
        elif not re.compile(r'\d{2}\.\d{2}\.\d{4}').fullmatch(date_daten):
            raise (ValueError(f"{date_daten} hat nicht das Muster 'TT.MM.JJJJ'!"))
        else:
            date_daten = datetime.strptime(date_daten, '%d.%m.%Y').date()

        return date_daten

    def existenz_date_pflichtdaten_pruefen(self, date_daten, art):
        """
        prüft, ob Daten, die zwingend für den Dateneintrag notwendig sind (z.B. Name, Adresse) , auch vorhanden sind
        :param date_daten: zu prüfende Pflichtdaten
        :param art: gibt an, um was für Daten es sich handeln soll
        :return: Daten, sofern sie in Ordnung sind
        """
        if date_daten == '':
            raise (ValueError(f"{art} ist nicht vorhanden."))
        elif not re.compile(r'\d{2}\.\d{2}\.\d{4}').fullmatch(date_daten):
            raise (ValueError(f"{date_daten} hat nicht das Muster 'TT.MM.JJJJ'!"))
        else:
            date_daten = datetime.strptime(date_daten, '%d.%m.%Y').date()

        return date_daten

    def pruefe_zeichenlaenge(self, string, art, anzahl_zeichen):
        """
        Methode prueft, ob eine Zeichenkette nicht das Maximum der erlaubten Anzahl an Zeichen übersteigt.
        Begrenzung ist notwendig, da varchar-Attribute der Datenbank nur eine bestimmte Zeichenlänge haben dürfen.
        :param string: Zeichenkette, welche geprüft werden soll
        :param art: gibt an, um was für Daten es sich handeln soll
        :param anzahl_zeichen: maximale Anzahl an Zeichen, die der zu prüfende String besitzen darf
        """
        if len(string) > anzahl_zeichen:
            raise (ValueError(f"{art} darf höchstens {anzahl_zeichen} Zeichen lang sein. "
                              f"{string} besitzt {len(string)} Zeichen!"))
    '''

    def nutzer_aus_datenbank_entfernen(self, conn):
        """
        Methode entfernt einen Nutzer aus der Tabelle "Nutzer" der Personalstammdatenbank
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
