import decimal
import pandas as pd
import re
from datetime import datetime

import psycopg2


class Nutzer:

    def __init__(self, mandant_id, personalnummer, vorname, nachname, schema='public'):

        if personalnummer == "":
            raise (ValueError(f"Die Personalnummer des Nutzers muss aus mindestens einem Zeichen bestehen."))

        if len(personalnummer) > 32:
            raise (ValueError(f"Die Personalnummer darf höchstens 32 Zeichen lang sein. "
                              f"'{personalnummer}' besitzt {len(personalnummer)} Zeichen!"))

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

        if schema != 'public' and schema != 'temp_test_schema':
            raise (ValueError("Diese Bezeichnung für ein Schema ist nicht erlaubt!"))

        self.schema = schema
        self.mandant_id = mandant_id
        self.personalnummer = str(personalnummer)
        self.vorname = vorname
        self.nachname = nachname
        self.nutzer_id = self._in_datenbank_anlegen()

    def get_nutzer_id(self):
        return self.nutzer_id

    def get_personalnummer(self):
        return self.personalnummer

    def get_vorname(self):
        return self.vorname

    def get_nachname(self):
        return self.nachname

    def _datenbankbverbindung_aufbauen(self):
        """
        Baut eine Connection zur Datenbank auf. Diese Methode wird jedes Mal aufgerufen, bevor mit der Datenbank
        interagiert werden soll.
        :return: conn-Variable, die die Verbindung zur Datenbank enthält
        """
        conn = psycopg2.connect(
            host="localhost",
            database="Personalstammdatenbank",
            user="postgres",
            password="@Postgres123",
            port=5432
        )

        return conn

    def _in_datenbank_anlegen(self):
        """
        Methode ruft die Stored Procedure 'nutzer_anlegen' auf, welche die Daten des Nutzers in der
        Personalstammdatenbank speichert.
        :return: Nutzer_ID, welche als Objekt-Variable gespeichert wird
        """

        conn = self._datenbankbverbindung_aufbauen()

        nutzer_insert_query = f"set search_path to {self.schema};" \
                              f"SELECT nutzer_anlegen('{self.mandant_id}', '{self.personalnummer}', " \
                              f"'{self.vorname}', '{self.nachname}')"
        cur = conn.cursor()
        nutzer_id = cur.execute(nutzer_insert_query)

        # Commit der Änderungen
        conn.commit()

        # Cursor und Konnektor zu Datenbank schließen
        cur.close()
        conn.close()

        return nutzer_id

    def abfrage_ausfuehren(self, abfrage):
        """
        Methode übermittelt ein SQL-Befehl an die Datenbank, wo sie ausgeführt und das Ergebnis zurückgegeben wird.
        :param abfrage: enthaelt den SQL-SELECT-Befehl, der an die Stored Procedure 'select_ausfuehren' uebergeben wird.
        :return: Ergebnis der Datenbankabfrage
        """
        conn = self._datenbankbverbindung_aufbauen()

        with conn.cursor() as cur:
            cur.execute(f"SET role postgres;"
                        f"SET session role tenant_user;"
                        # f"SET app.current_user_id='{self.mandant_id}';"
                        f"SET app.current_tenant='{self.mandant_id}';"
                        f"{abfrage}")
            ergebnis = cur.fetchall()

        # Commit der Änderungen
        conn.commit()

        # Cursor und Konnektor zu Datenbank schließen
        cur.close()
        conn.close()

        return ergebnis

    def insert_neuer_mitarbeiter(self, mitarbeiterdaten):
        """
        Diese Methode überträgt die eingetragenen Mitarbeiterdaten (im Rahmen der Bachelorarbeit
        dargestellt durch eine Excel-Datei) in die Datenbank, in dem der Stored Procedure
        'insert_neuer_mitarbeiter' aufgerufen wird.
        :param mitarbeiterdaten: Name der Excel-Datei, dessen Mitarbeiterdaten in die Datenbank
        eingetragen werden sollen.
        :return:
        """
        conn = self._datenbankbverbindung_aufbauen()

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
        dienstliche_telefonnummer = self._existenz_str_daten_feststellen(liste_ma_daten[11], 'dienstliche '
                                                                                             'Telefonnummer', 16, False)
        dienstliche_email = self._existenz_str_daten_feststellen(liste_ma_daten[12], 'dienstliche E-Mail', 64, False)
        austrittsdatum = self._existenz_date_daten_feststellen(liste_ma_daten[13], 'Austrittsdatum', False)
        strasse = self._existenz_str_daten_feststellen(liste_ma_daten[14], 'Strasse', 64, True)
        hausnummer = self._existenz_str_daten_feststellen(liste_ma_daten[15], 'Hausnummer', 8, True)
        postleitzahl = self._existenz_str_daten_feststellen(liste_ma_daten[16], 'Postleitzahl', 16, True)
        stadt = self._existenz_str_daten_feststellen(liste_ma_daten[17], 'Stadt', 128, True)
        region = self._existenz_str_daten_feststellen(liste_ma_daten[18], 'Region', 128, True)
        land = self._existenz_str_daten_feststellen(liste_ma_daten[19], 'Land', 128, True)
        geschlecht = self._existenz_str_daten_feststellen(liste_ma_daten[20], 'Geschlecht', 32, False)
        mitarbeitertyp = self._existenz_str_daten_feststellen(liste_ma_daten[21], 'Mitarbeitertyp', 32, False)
        steuerklasse = self._existenz_str_daten_feststellen(liste_ma_daten[22], 'Steuerklasse', 1, False)
        wochenarbeitsstunden = self._existenz_zahlen_daten_feststellen(liste_ma_daten[23], 50, 'Wochenarbeitsstunden',
                                                                       False)
        abteilung = self._existenz_str_daten_feststellen(liste_ma_daten[24], 'Abteilung', 64, False)
        abteilungskuerzel = self._existenz_str_daten_feststellen(liste_ma_daten[25], 'Abteilungskuerzel', 16, False)
        fuehrungskraft = self._existenz_boolean_daten_feststellen(liste_ma_daten[26], 'Fuehrungskraft', False)
        jobtitel = self._existenz_str_daten_feststellen(liste_ma_daten[27], 'Jobtitel', 32, False)
        erfahrungsstufe = self._existenz_str_daten_feststellen(liste_ma_daten[28], 'Erfahrungsstufe', 32, False)
        gesellschaft = self._existenz_str_daten_feststellen(liste_ma_daten[29], 'Gesellschaft', 128, False)
        abk_gesellschaft = self._existenz_str_daten_feststellen(liste_ma_daten[30], 'Abk. Gesellschaft', 16, False)

        tarifbeschaeftigt = self._existenz_boolean_daten_feststellen(liste_ma_daten[31], 'tarifbeschaeftigt', False)
        if tarifbeschaeftigt:
            gewerkschaft = self._existenz_str_daten_feststellen(liste_ma_daten[32], 'Gewerkschaft', 64, False)
            tarif = self._existenz_str_daten_feststellen(liste_ma_daten[33], 'Tarif', 16, False)
        else:
            gewerkschaft = None
            tarif = None

        grundgehalt_monat = self._existenz_zahlen_daten_feststellen(liste_ma_daten[34],
                                                                    99999999,
                                                                    'Grundgehalt monatlich',
                                                                    False)
        weihnachtsgeld = self._existenz_zahlen_daten_feststellen(liste_ma_daten[35],
                                                                 99999999,
                                                                 'Weihnachtsgeld',
                                                                 False)
        urlaubsgeld = self._existenz_zahlen_daten_feststellen(liste_ma_daten[36],
                                                              99999999,
                                                              'Urlaubsgeld',
                                                              False)

        privat_krankenversichert = self._existenz_boolean_daten_feststellen(liste_ma_daten[37],
                                                                            'privat Krankenversichert?',
                                                                            False)

        # Arbeitgeberbeitraege fuer privat Versicherte
        ag_zuschuss_krankenversicherung = self._existenz_zahlen_daten_feststellen(liste_ma_daten[38],
                                                                                  99999999,
                                                                                  'AG-Zuschuss Krankenversicherung',
                                                                                  False)
        ag_zuschuss_zusatzbeitrag = self._existenz_zahlen_daten_feststellen(liste_ma_daten[39],
                                                                            99999999,
                                                                            'AG-Zuschuss Zusatzbeitrag',
                                                                            False)
        ag_zuschuss_pflegeversicherung = self._existenz_zahlen_daten_feststellen(liste_ma_daten[40],
                                                                                 99999999,
                                                                                 'AG-Zuschuss Pflegeversicherung',
                                                                                 False)

        gesetzlich_krankenversichert = self._existenz_boolean_daten_feststellen(liste_ma_daten[41],
                                                                            'gesetzlich Krankenversichert?',
                                                                            False)

        # Ein Mitarbeiter kann zur selben Zeit entweder gesetzlich oder privat krankenversichert sein, niemals
        # beides gleichzeitig!
        if privat_krankenversichert and gesetzlich_krankenversichert:
            raise (ValueError(f"Der Mitarbeiter '{personalnummer}' kann nicht gleichzeitig gesetzlich und"
                              f"privat versichert sein!"))

        # Beitraege fuer gesetzliche Versicherungen
        ag_krankenversicherungsbeitrag_in_prozent = self._existenz_zahlen_daten_feststellen(liste_ma_daten[42],
                                                                                            99,
                                                                                            'AG-Beitrag GKV',
                                                                                            False)
        an_krankenversicherungsbeitrag_in_prozent = self._existenz_zahlen_daten_feststellen(liste_ma_daten[43],
                                                                                            99,
                                                                                            'AN-Beitrag GKV',
                                                                                            False)
        beitragsbemessungsgrenze_kv_ost = self._existenz_zahlen_daten_feststellen(liste_ma_daten[44],
                                                                                  99999999,
                                                                                  'Beitragsbemessungsgrenze GKV Ost',
                                                                                  False)
        beitragsbemessungsgrenze_kv_west = self._existenz_zahlen_daten_feststellen(liste_ma_daten[45],
                                                                                   99999999,
                                                                                   'Beitragsbemessungsgrenze GKV West',
                                                                                   False)
        bezeichnung_gesetzliche_krankenkasse = self._existenz_str_daten_feststellen(liste_ma_daten[46],
                                                                                    'Bezeichnung ges. Krankenkasse',
                                                                                    128,
                                                                                    False)
        abkuerzung_gesetzliche_krankenkasse = self._existenz_str_daten_feststellen(liste_ma_daten[47],
                                                                                    'Abkuerzung ges. Krankenkasse',
                                                                                    16,
                                                                                    False)
        gkv_zusatzbeitrag_in_prozent = self._existenz_zahlen_daten_feststellen(liste_ma_daten[48],
                                                                                            99,
                                                                                            'GKV Zusatzbeitrag in %',
                                                                                            False)

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
                                                 land,
                                                 geschlecht,
                                                 mitarbeitertyp,
                                                 steuerklasse,
                                                 wochenarbeitsstunden,
                                                 abteilung,
                                                 abteilungskuerzel,
                                                 fuehrungskraft,
                                                 jobtitel,
                                                 erfahrungsstufe,
                                                 gesellschaft,
                                                 abk_gesellschaft,
                                                 tarifbeschaeftigt,
                                                 gewerkschaft,
                                                 tarif,
                                                 grundgehalt_monat,
                                                 weihnachtsgeld,
                                                 urlaubsgeld,
                                                 privat_krankenversichert,
                                                 ag_zuschuss_krankenversicherung,
                                                 ag_zuschuss_zusatzbeitrag,
                                                 ag_zuschuss_pflegeversicherung,
                                                 gesetzlich_krankenversichert,
                                                 ag_krankenversicherungsbeitrag_in_prozent,
                                                 an_krankenversicherungsbeitrag_in_prozent,
                                                 beitragsbemessungsgrenze_kv_ost,
                                                 beitragsbemessungsgrenze_kv_west,
                                                 bezeichnung_gesetzliche_krankenkasse,
                                                 abkuerzung_gesetzliche_krankenkasse,
                                                 gkv_zusatzbeitrag_in_prozent])

        # Commit der Änderungen
        conn.commit()

        # Cursor und Konnektor zu Datenbank schließen
        cur.close()
        conn.close()

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
            raise (ValueError(f"'{art}' ist nicht vorhanden."))
        elif len(str(str_daten)) > anzahl_zeichen:
            raise (ValueError(f"'{art}' darf höchstens {anzahl_zeichen} Zeichen lang sein. "
                              f"Ihre Eingabe '{str_daten}' besitzt {len(str_daten)} Zeichen!"))
        else:
            str_daten = str(str_daten)

        return str_daten

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
            return date_daten

        if date_daten == '' and pflicht:
            raise (ValueError(f"'{art}' ist nicht vorhanden."))

        if not re.compile(r'\d{2}\.\d{2}\.\d{4}').fullmatch(date_daten):
            raise (ValueError(f"'{date_daten}' hat nicht das Muster 'TT.MM.JJJJ'!"))

        try:
            date_daten = datetime.strptime(date_daten, '%d.%m.%Y').date()
        except ValueError:
            raise (ValueError(f"'{date_daten}' ist nicht möglich!"))

        return date_daten

    def _existenz_zahlen_daten_feststellen(self, zahlen_daten, hoechstbetrag, art, pflicht):
        """
        Methode stellt fest, ob optionale Daten vorliegen oder nicht und wenn ja, so sollen diese auf jeden Fall
        als Decimal-Datentyp mit zwei Nachkommastellen zurückgegeben werden. So soll sichergestellt werden, dass dem
        Datenbanksystem die Daten in dem Datentyp übergeben werden, in der sie in der Personalstammdatenbank gespeichert
        werden können.
        :param zahlen_daten: wird untersucht, ob Daten darin enthalten sind
        :param hoechstbetrag: der Wert der Variablen 'zahlen_daten' darf nicht höher sein
        :param art: gibt an, um was für Daten es sich handeln soll
        :param pflicht: boolean, der bei 'True' angibt, dass 'zahlen_daten' kein leerer String sein darf
        :return: Falls Parameter 'daten' keine Daten enthält, wird None zurückgegeben, sonst Daten
        """
        if zahlen_daten == '' and not pflicht:
            zahlen_daten = None
            return zahlen_daten
        elif zahlen_daten == '' and pflicht:
            raise (ValueError(f"'{art}' ist nicht vorhanden."))
        else:
            try:
                zahlen_daten = round(decimal.Decimal(zahlen_daten), 2)
            except decimal.InvalidOperation:
                raise (TypeError(f"Der übergebene Wert '{zahlen_daten}' konnte nicht in eine Gleitkommazahl "
                                 f"konvertiert werden!"))

        return zahlen_daten

    def _existenz_boolean_daten_feststellen(self, boolean_daten, art, pflicht):
        """
            Methode stellt fest, ob optionale Daten vorliegen oder nicht und wenn ja, so sollen diese auf jeden Fall
            als boolean-Datentyp mit zwei Nachkommastellen zurückgegeben werden. So soll sichergestellt werden, dass dem
            Datenbanksystem die Daten in dem Datentyp übergeben werden, in der sie in der Personalstammdatenbank gespeichert
            werden können.
            :param boolean_daten: wird untersucht, ob Daten darin enthalten sind
            :param art: gibt an, um was für Daten es sich handeln soll
            :param pflicht: boolean, der bei 'True' angibt, dass 'boolean_daten' kein leerer String sein darf
            :return: Falls Parameter 'daten' keine Daten enthält, wird None zurückgegeben, sonst Daten
            """
        if boolean_daten == '' and not pflicht:
            boolean_daten = None
            return boolean_daten
        elif boolean_daten == '' and pflicht:
            raise (ValueError(f"'{art}' ist nicht vorhanden."))
        elif str.lower(boolean_daten) == 'ja':
            boolean_daten = True
            return boolean_daten
        elif str.lower(boolean_daten) == 'nein':
            boolean_daten = False
            return boolean_daten
        else:
            raise TypeError(f"Der übergebene Wert '{boolean_daten}' konnte nicht verarbeitet werden. Bitte geben "
                            f"Sie ausschließlich 'ja' oder 'nein' ein.")
