import decimal
import pandas as pd
import re
from datetime import datetime, timedelta

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
        :param abfrage: enthaelt den SQL-SELECT-Befehl.
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

    def insert_geschlecht(self, neuanlage_geschlecht):
        """
        Diese Methode uebertraegt ein Geschlecht (im Rahmen der Bachelorarbeit dargestellt durch eine Excel-Datei) in
        die Datenbank, in dem die Stored Procedure 'insert_geschlecht' aufgerufen wird.
        :param neuanlage_geschlecht: Name der Excel-Datei, dessen Daten in die Datenbank
        eingetragen werden sollen.
        """

        # Import der Daten aus der Excel-Datei in das Pandas-Dataframe und Uebertragung in Liste "liste_ma_daten"
        df_ma_daten = pd.read_excel(f"insert personenbezogene Daten/{neuanlage_geschlecht}",
                                    index_col='Daten', na_filter=False)
        liste_ma_daten = list(df_ma_daten.iloc[:, 0])

        # Daten aus importierter Excel-Tabelle '1 Geschlecht.xlsx' pruefen
        geschlecht = self._existenz_str_daten_feststellen(liste_ma_daten[0], 'Geschlecht', 32, True)

        conn = self._datenbankbverbindung_aufbauen()
        cur = conn.cursor()

        # Stored Procedure aufrufen und Daten an Datenbank uebergeben
        cur.callproc('insert_geschlecht', [self.mandant_id, geschlecht])

        # Commit der Aenderungen
        conn.commit()

        # Cursor und Konnektor zu Datenbank schließen
        cur.close()
        conn.close()

    def insert_mitarbeitertyp(self, neuanlage_mitarbeitertyp):
        """
        Diese Methode uebertraegt ein Mitarbeitertyp wie bspw. 'Angestellter' oder 'Praktikant' (im Rahmen der
        Bachelorarbeit dargestellt durch eine Excel-Datei) in die Datenbank, in dem die Stored Procedure
        'insert_mitarbeitertyp' aufgerufen wird.
        :param neuanlage_mitarbeitertyp: Name der Excel-Datei, dessen Daten in die Datenbank
        eingetragen werden sollen.
        """

        # Import der Daten aus der Excel-Datei in das Pandas-Dataframe und Uebertragung in Liste "liste_ma_daten"
        df_ma_daten = pd.read_excel(f"insert personenbezogene Daten/{neuanlage_mitarbeitertyp}",
                                    index_col='Daten', na_filter=False)
        liste_ma_daten = list(df_ma_daten.iloc[:, 0])

        # Daten aus importierter Excel-Tabelle '2 Mitarbeitertyp.xlsx' pruefen
        mitarbeitertyp = self._existenz_str_daten_feststellen(liste_ma_daten[0], 'Geschlecht', 32, True)

        conn = self._datenbankbverbindung_aufbauen()
        cur = conn.cursor()

        # Stored Procedure aufrufen und Daten an Datenbank uebergeben
        cur.callproc('insert_mitarbeitertyp', [self.mandant_id, mitarbeitertyp])

        # Commit der Aenderungen
        conn.commit()

        # Cursor und Konnektor zu Datenbank schließen
        cur.close()
        conn.close()

    def insert_steuerklasse(self, neuanlage_steuerklasse):
        """
        Diese Methode uebertraegt Steuerklasse (im Rahmen der Bachelorarbeit dargestellt durch eine Excel-Datei) in die
        Datenbank, in dem die Stored Procedure 'insert_steuerklasse' aufgerufen wird.
        :param neuanlage_steuerklasse: Name der Excel-Datei, dessen Daten in die Datenbank
        eingetragen werden sollen.
        """

        # Import der Daten aus der Excel-Datei in das Pandas-Dataframe und Uebertragung in Liste "liste_ma_daten"
        df_ma_daten = pd.read_excel(f"insert personenbezogene Daten/{neuanlage_steuerklasse}",
                                    index_col='Daten', na_filter=False)
        liste_ma_daten = list(df_ma_daten.iloc[:, 0])

        # Daten aus importierter Excel-Tabelle '3 Steuerklasse.xlsx' pruefen
        steuerklasse = self._existenz_str_daten_feststellen(liste_ma_daten[0], 'Steuerklasse', 1, True)

        conn = self._datenbankbverbindung_aufbauen()
        cur = conn.cursor()

        # Stored Procedure aufrufen und Daten an Datenbank uebergeben
        cur.callproc('insert_steuerklasse', [self.mandant_id, steuerklasse])

        # Commit der Aenderungen
        conn.commit()

        # Cursor und Konnektor zu Datenbank schließen
        cur.close()
        conn.close()

    def insert_abteilung(self, neuanlage_abteilung):
        """
        Diese Methode uebertraegt eine Abteilung und deren Abkuerzung in die Datenbank (im Rahmen der Bachelorarbeit
        dargestellt durch eine Excel-Datei), in dem die Stored Procedure 'insert_abteilung' aufgerufen wird.
        :param neuanlage_abteilung: Name der Excel-Datei, dessen Daten in die Datenbank
        eingetragen werden sollen.
        """

        # Import der Daten aus der Excel-Datei in das Pandas-Dataframe und Uebertragung in Liste "liste_ma_daten"
        df_ma_daten = pd.read_excel(f"insert personenbezogene Daten/{neuanlage_abteilung}",
                                    index_col='Daten', na_filter=False)
        liste_ma_daten = list(df_ma_daten.iloc[:, 0])

        # Daten aus importierter Excel-Tabelle '4 Abteilung.xlsx' pruefen
        abteilung = self._existenz_str_daten_feststellen(liste_ma_daten[0], 'Abteilung', 64, True)
        abkuerzung = self._existenz_str_daten_feststellen(liste_ma_daten[1], 'Abteilungskuerzel', 16, True)

        conn = self._datenbankbverbindung_aufbauen()
        cur = conn.cursor()

        # Stored Procedure aufrufen und Daten an Datenbank uebergeben
        cur.callproc('insert_abteilung', [self.mandant_id, abteilung, abkuerzung])

        # Commit der Aenderungen
        conn.commit()

        # Cursor und Konnektor zu Datenbank schließen
        cur.close()
        conn.close()

    def insert_jobtitel(self, neuanlage_jobtitel):
        """
        Diese Methode uebertraegt einen Jobtitel (im Rahmen der Bachelorarbeit dargestellt durch eine Excel-Datei),
        in dem die Stored Procedure 'insert_jobtitel' aufgerufen wird.
        :param neuanlage_jobtitel: Name der Excel-Datei, dessen Daten in die Datenbank eingetragen werden sollen.
        """

        # Import der Daten aus der Excel-Datei in das Pandas-Dataframe und Uebertragung in Liste "liste_ma_daten"
        df_ma_daten = pd.read_excel(f"insert personenbezogene Daten/{neuanlage_jobtitel}",
                                    index_col='Daten', na_filter=False)
        liste_ma_daten = list(df_ma_daten.iloc[:, 0])

        # Daten aus importierter Excel-Tabelle '5 Jobtitel.xlsx' pruefen
        jobtitel = self._existenz_str_daten_feststellen(liste_ma_daten[0], 'Jobtitel', 32, True)

        conn = self._datenbankbverbindung_aufbauen()
        cur = conn.cursor()

        # Stored Procedure aufrufen und Daten an Datenbank uebergeben
        cur.callproc('insert_jobtitel', [self.mandant_id, jobtitel])

        # Commit der Aenderungen
        conn.commit()

        # Cursor und Konnektor zu Datenbank schließen
        cur.close()
        conn.close()

    def insert_erfahrungsstufe(self, neuanlage_erfahrungsstufe):
        """
        Diese Methode uebertraegt eine Erfahrungsstufe wie bspw. 'Junior', 'Senior' etc. (im Rahmen der Bachelorarbeit
        dargestellt durch eine Excel-Datei), in dem die Stored Procedure 'insert_erfahrungsstufe' aufgerufen wird.
        :param neuanlage_jobtitel: Name der Excel-Datei, dessen Daten in die Datenbank eingetragen werden sollen.
        """

        # Import der Daten aus der Excel-Datei in das Pandas-Dataframe und Uebertragung in Liste "liste_ma_daten"
        df_ma_daten = pd.read_excel(f"insert personenbezogene Daten/{neuanlage_erfahrungsstufe}",
                                    index_col='Daten', na_filter=False)
        liste_ma_daten = list(df_ma_daten.iloc[:, 0])

        # Daten aus importierter Excel-Tabelle '6 Erfahrungsstufe.xlsx' pruefen
        erfahrungsstufe = self._existenz_str_daten_feststellen(liste_ma_daten[0], 'Erfahrungsstufe', 32, True)

        conn = self._datenbankbverbindung_aufbauen()
        cur = conn.cursor()

        # Stored Procedure aufrufen und Daten an Datenbank uebergeben
        cur.callproc('insert_erfahrungsstufe', [self.mandant_id, erfahrungsstufe])

        # Commit der Aenderungen
        conn.commit()

        # Cursor und Konnektor zu Datenbank schließen
        cur.close()
        conn.close()

    def insert_gesellschaft(self, neuanlage_gesellschaft):
        """
        Diese Methode uebertraegt eine Unternehmensgesellschaft und deren Abkuerzung in die Datenbank (im Rahmen der
        Bachelorarbeit dargestellt durch eine Excel-Datei), in dem die Stored Procedure 'insert_gesellschaft' aufgerufen
        wird.
        :param neuanlage_gesellschaft: Name der Excel-Datei, dessen Daten in die Datenbank eingetragen werden sollen.
        """

        # Import der Daten aus der Excel-Datei in das Pandas-Dataframe und Uebertragung in Liste "liste_ma_daten"
        df_ma_daten = pd.read_excel(f"insert personenbezogene Daten/{neuanlage_gesellschaft}",
                                    index_col='Daten', na_filter=False)
        liste_ma_daten = list(df_ma_daten.iloc[:, 0])

        # Daten aus importierter Excel-Tabelle '7 Gesellschaft.xlsx' pruefen
        gesellschaft = self._existenz_str_daten_feststellen(liste_ma_daten[0], 'Gesellschaft', 128, True)
        abkuerzung = self._existenz_str_daten_feststellen(liste_ma_daten[1], 'Gesellschaftskuerzel', 16, True)

        conn = self._datenbankbverbindung_aufbauen()
        cur = conn.cursor()

        # Stored Procedure aufrufen und Daten an Datenbank uebergeben
        cur.callproc('insert_gesellschaft', [self.mandant_id, gesellschaft, abkuerzung])

        # Commit der Aenderungen
        conn.commit()

        # Cursor und Konnektor zu Datenbank schließen
        cur.close()
        conn.close()

    def insert_austrittsgrundkategorie(self, neuanlage_austrittsgrundkategorie):
        """
        Diese Methode uebertraegt eine Austrittsgrundkategorie wie bspw. 'betriebsbedingt' in die Datenbank (im Rahmen
        der Bachelorarbeit dargestellt durch eine Excel-Datei), in dem die Stored Procedure
        'insert_kategorien_austrittsgruende' aufgerufen wird.
        :param neuanlage_austrittsgrundkategorie: Name der Excel-Datei, dessen Daten in die Datenbank eingetragen werden
        sollen.
        """

        # Import der Daten aus der Excel-Datei in das Pandas-Dataframe und Uebertragung in Liste "liste_ma_daten"
        df_ma_daten = pd.read_excel(f"insert personenbezogene Daten/{neuanlage_austrittsgrundkategorie}",
                                    index_col='Daten', na_filter=False)
        liste_ma_daten = list(df_ma_daten.iloc[:, 0])

        # Daten aus importierter Excel-Tabelle '8 Austrittsgrundkategorie.xlsx' pruefen
        austrittsgrundkategorie = self._existenz_str_daten_feststellen(liste_ma_daten[0],
                                                                       'Austrittsgrundkategorie',
                                                                       16,
                                                                       True)

        conn = self._datenbankbverbindung_aufbauen()
        cur = conn.cursor()

        # Stored Procedure aufrufen und Daten an Datenbank uebergeben
        cur.callproc('insert_kategorien_austrittsgruende', [self.mandant_id, austrittsgrundkategorie])

        # Commit der Aenderungen
        conn.commit()

        # Cursor und Konnektor zu Datenbank schließen
        cur.close()
        conn.close()

    def insert_austrittsgrund(self, neuanlage_austrittsgrund):
        """
        Diese Methode uebertraegt eine Austrittsgrund wie bspw. 'Umsatzrueckgang' in die Datenbank (im Rahmen
        der Bachelorarbeit dargestellt durch eine Excel-Datei), in dem die Stored Procedure 'insert_austrittsgruende'
        aufgerufen wird.
        :param neuanlage_austrittsgrund: Name der Excel-Datei, dessen Daten in die Datenbank eingetragen werden sollen.
        """

        # Import der Daten aus der Excel-Datei in das Pandas-Dataframe und Uebertragung in Liste "liste_ma_daten"
        df_ma_daten = pd.read_excel(f"insert personenbezogene Daten/{neuanlage_austrittsgrund}",
                                    index_col='Daten', na_filter=False)
        liste_ma_daten = list(df_ma_daten.iloc[:, 0])

        # Daten aus importierter Excel-Tabelle '9 Austrittsgrund.xlsx' pruefen
        austrittsgrund = self._existenz_str_daten_feststellen(liste_ma_daten[0], 'Austrittsgrund', 16, True)
        austrittsgrundkategorie = self._existenz_str_daten_feststellen(liste_ma_daten[1],
                                                                       'Austrittsgrundkategorie',
                                                                       16,
                                                                       True)

        conn = self._datenbankbverbindung_aufbauen()
        cur = conn.cursor()

        # Stored Procedure aufrufen und Daten an Datenbank uebergeben
        cur.callproc('insert_austrittsgruende', [self.mandant_id, austrittsgrund, austrittsgrundkategorie])

        # Commit der Aenderungen
        conn.commit()

        # Cursor und Konnektor zu Datenbank schließen
        cur.close()
        conn.close()

    def insert_krankenversicherungsbeitraege(self, neuanlage_krankenversicherungsbeitraege):
        """
        Diese Methode überträgt die eingetragenen Krankenversicherungsbeitraege (im Rahmen der Bachelorarbeit
        dargestellt durch eine Excel-Datei) in die Datenbank, in dem der Stored Procedure
        'insert_krankenversicherungsbeitraege' aufgerufen wird.
        :param neuanlage_krankenversicherungsbeitraege: Name der Excel-Datei, dessen Daten in die Datenbank eingetragen
        werden sollen.
        """

        # Import der Daten aus der Excel-Datei in das Pandas-Dataframe und Uebertragung in Liste "liste_ma_daten"
        df_ma_daten = pd.read_excel(f"insert Sozialversicherungsdaten/{neuanlage_krankenversicherungsbeitraege}",
                                    index_col='Daten', na_filter=False)
        liste_ma_daten = list(df_ma_daten.iloc[:, 0])

        # Daten aus importierter Excel-Tabelle '1 Krankenversicherungsbeitraege.xlsx' pruefen
        ermaessigter_beitragssatz = self._existenz_boolean_daten_feststellen(liste_ma_daten[0],
                                                                             'ermaessigter Beitragssatz',
                                                                             True)
        an_gkv_beitrag_in_prozent = self._existenz_zahlen_daten_feststellen(liste_ma_daten[1],
                                                                            99,
                                                                            'Arbeitnehmerbeitrag GKV in Prozent',
                                                                            True)
        ag_gkv_beitrag_in_prozent = self._existenz_zahlen_daten_feststellen(liste_ma_daten[2],
                                                                            99,
                                                                            'Arbeitgeberbeitrag GKV in Prozent',
                                                                            True)
        beitragsbemessungsgrenze_gkv_ost = self._existenz_zahlen_daten_feststellen(liste_ma_daten[3],
                                                                                   99999999,
                                                                                   'Beitragsbemessungsgrenze GKV Ost',
                                                                                   True)
        beitragsbemessungsgrenze_gkv_west = self._existenz_zahlen_daten_feststellen(liste_ma_daten[4],
                                                                                    99999999,
                                                                                    'Beitragsbemessungsgrenze GKV West',
                                                                                    True)
        eintragungsdatum = self._existenz_date_daten_feststellen(liste_ma_daten[5], 'Eintragungsdatum', True)

        conn = self._datenbankbverbindung_aufbauen()
        cur = conn.cursor()

        # Stored Procedure aufrufen und Daten an Datenbank uebergeben
        cur.callproc('insert_krankenversicherungsbeitraege', [self.mandant_id,
                                                              ermaessigter_beitragssatz,
                                                              an_gkv_beitrag_in_prozent,
                                                              ag_gkv_beitrag_in_prozent,
                                                              beitragsbemessungsgrenze_gkv_ost,
                                                              beitragsbemessungsgrenze_gkv_west,
                                                              eintragungsdatum])

        # Commit der Aenderungen
        conn.commit()

        # Cursor und Konnektor zu Datenbank schließen
        cur.close()
        conn.close()

    def insert_gesetzliche_krankenkasse(self, neuanlage_gesetzliche_krankenkasse):
        """
        Diese Methode uebertraegt die eingetragene gesetzliche Krankenkasse mit deren Zusatzbeitrag und Umlagen (im
        Rahmen der Bachelorarbeit dargestellt durch eine Excel-Datei) in die Datenbank, in dem der Stored Procedure
        'insert_gesetzliche_Krankenkasse' aufgerufen wird.
        :param neuanlage_gesetzliche_krankenkasse: Name der Excel-Datei, dessen Daten in die Datenbank eingetragen
        werden sollen.
        """

        # Import der Daten aus der Excel-Datei in das Pandas-Dataframe und Uebertragung in Liste "liste_ma_daten"
        df_ma_daten = pd.read_excel(f"insert Sozialversicherungsdaten/{neuanlage_gesetzliche_krankenkasse}",
                                    index_col='Daten', na_filter=False)
        liste_ma_daten = list(df_ma_daten.iloc[:, 0])

        # Daten aus importierter Excel-Tabelle '2 gesetzliche Krankenkasse.xlsx' pruefen
        krankenkasse_voller_name = self._existenz_str_daten_feststellen(liste_ma_daten[0],
                                                                        'Krankenkasse voller Name',
                                                                        128,
                                                                        True)
        krankenkasse_abkuerzung = self._existenz_str_daten_feststellen(liste_ma_daten[1],
                                                                       'Krankenkasse Abkuerzung',
                                                                       16,
                                                                       True)
        zusatzbeitrag = self._existenz_zahlen_daten_feststellen(liste_ma_daten[2],
                                                                99,
                                                                'Zusatzbeitrag Krankenkasse',
                                                                True)
        u1_umlage = self._existenz_zahlen_daten_feststellen(liste_ma_daten[3], 99, 'U1-Umlage', True)
        u2_umlage = self._existenz_zahlen_daten_feststellen(liste_ma_daten[4], 99, 'U2-Umlage', True)
        insolvenzgeldumlage = self._existenz_zahlen_daten_feststellen(liste_ma_daten[5],
                                                                      99,
                                                                      'Insolvenzgeldumlage',
                                                                      True)
        eintragungsdatum = self._existenz_date_daten_feststellen(liste_ma_daten[6], 'Eintragungsdatum', True)

        conn = self._datenbankbverbindung_aufbauen()
        cur = conn.cursor()

        # Stored Procedure aufrufen und Daten an Datenbank uebergeben
        cur.callproc('insert_gesetzliche_Krankenkasse', [self.mandant_id,
                                                         krankenkasse_voller_name,
                                                         krankenkasse_abkuerzung,
                                                         zusatzbeitrag,
                                                         u1_umlage,
                                                         u2_umlage,
                                                         insolvenzgeldumlage,
                                                         'gesetzlich',
                                                         eintragungsdatum])

        # Commit der Aenderungen
        conn.commit()

        # Cursor und Konnektor zu Datenbank schließen
        cur.close()
        conn.close()

    def insert_private_krankenkasse(self, neuanlage_private_krankenkasse):
        """
        Diese Methode uebertraegt die eingetragene private Krankenkasse mit deren Umlagen (im Rahmen
        der Bachelorarbeit dargestellt durch eine Excel-Datei) in die Datenbank, in dem der Stored Procedure
        'insert_private_Krankenkasse' aufgerufen wird.
        :param neuanlage_private_krankenkasse: Name der Excel-Datei, dessen Daten in die Datenbank
        eingetragen werden sollen.
        """

        # Import der Daten aus der Excel-Datei in das Pandas-Dataframe und Uebertragung in Liste "liste_ma_daten"
        df_ma_daten = pd.read_excel(f"insert Sozialversicherungsdaten/{neuanlage_private_krankenkasse}",
                                    index_col='Daten', na_filter=False)
        liste_ma_daten = list(df_ma_daten.iloc[:, 0])

        # Daten aus importierter Excel-Tabelle '3 private Krankenkasse.xlsx' pruefen
        krankenkasse_voller_name = self._existenz_str_daten_feststellen(liste_ma_daten[0],
                                                                        'Krankenkasse voller Name',
                                                                        128,
                                                                        True)
        krankenkasse_abkuerzung = self._existenz_str_daten_feststellen(liste_ma_daten[1],
                                                                       'Krankenkasse Abkuerzung',
                                                                       16,
                                                                       True)
        u1_umlage = self._existenz_zahlen_daten_feststellen(liste_ma_daten[2], 99, 'U1-Umlage', True)
        u2_umlage = self._existenz_zahlen_daten_feststellen(liste_ma_daten[3], 99, 'U2-Umlage', True)
        insolvenzgeldumlage = self._existenz_zahlen_daten_feststellen(liste_ma_daten[4],
                                                                      99,
                                                                      'Insolvenzgeldumlage',
                                                                      True)
        eintragungsdatum = self._existenz_date_daten_feststellen(liste_ma_daten[5], 'Eintragungsdatum', True)

        conn = self._datenbankbverbindung_aufbauen()
        cur = conn.cursor()

        # Stored Procedure aufrufen und Daten an Datenbank uebergeben
        cur.callproc('insert_private_Krankenkasse', [self.mandant_id,
                                                     krankenkasse_voller_name,
                                                     krankenkasse_abkuerzung,
                                                     u1_umlage,
                                                     u2_umlage,
                                                     insolvenzgeldumlage,
                                                     'privat',
                                                     eintragungsdatum])

        # Commit der Aenderungen
        conn.commit()

        # Cursor und Konnektor zu Datenbank schließen
        cur.close()
        conn.close()

    def insert_gemeldete_krankenkasse(self, neuanlage_gemeldete_krankenkasse):
        """
        Diese Methode uebertraegt die eingetragene gemeldete Krankenkasse fuer Mitarbeiter, die anderweitig
        krankenversichert sein muessen (z.B. Werkstudenten, unbezahlte Praktikanten etc.) mit deren Umlagen (im Rahmen
        der Bachelorarbeit dargestellt durch eine Excel-Datei) in die Datenbank, in dem der Stored Procedure
        'insert_gemeldete_Krankenkasse' aufgerufen wird.
        :param neuanlage_gemeldete_krankenkasse: Name der Excel-Datei, dessen Daten in die Datenbank
        eingetragen werden sollen.
        """

        # Import der Daten aus der Excel-Datei in das Pandas-Dataframe und Uebertragung in Liste "liste_ma_daten"
        df_ma_daten = pd.read_excel(f"insert Sozialversicherungsdaten/{neuanlage_gemeldete_krankenkasse}",
                                    index_col='Daten', na_filter=False)
        liste_ma_daten = list(df_ma_daten.iloc[:, 0])

        # Daten aus importierter Excel-Tabelle '4 gemeldete Krankenkasse.xlsx' pruefen
        krankenkasse_voller_name = self._existenz_str_daten_feststellen(liste_ma_daten[0],
                                                                        'Krankenkasse voller Name',
                                                                        128,
                                                                        True)
        krankenkasse_abkuerzung = self._existenz_str_daten_feststellen(liste_ma_daten[1],
                                                                       'Krankenkasse Abkuerzung',
                                                                       16,
                                                                       True)
        u1_umlage = self._existenz_zahlen_daten_feststellen(liste_ma_daten[2], 99, 'U1-Umlage', True)
        u2_umlage = self._existenz_zahlen_daten_feststellen(liste_ma_daten[3], 99, 'U2-Umlage', True)
        insolvenzgeldumlage = self._existenz_zahlen_daten_feststellen(liste_ma_daten[4],
                                                                      99,
                                                                      'Insolvenzgeldumlage',
                                                                      True)
        eintragungsdatum = self._existenz_date_daten_feststellen(liste_ma_daten[5], 'Eintragungsdatum', True)

        conn = self._datenbankbverbindung_aufbauen()
        cur = conn.cursor()

        # Stored Procedure aufrufen und Daten an Datenbank uebergeben
        cur.callproc('insert_gemeldete_Krankenkasse', [self.mandant_id,
                                                       krankenkasse_voller_name,
                                                       krankenkasse_abkuerzung,
                                                       u1_umlage,
                                                       u2_umlage,
                                                       insolvenzgeldumlage,
                                                       'anders',
                                                       eintragungsdatum])

        # Commit der Aenderungen
        conn.commit()

        # Cursor und Konnektor zu Datenbank schließen
        cur.close()
        conn.close()

    def insert_anzahl_kinder_an_pv_beitrag(self, neuanlage_anzahl_kinder):
        """
        Diese Methode uebertraegt die Anzahl der Kinder und der daraus resultierende Arbeitnehmerbeitrag zur
        Pflegeversicherung (im Rahmen der Bachelorarbeit dargestellt durch eine Excel-Datei) in die Datenbank, in dem
        der Stored Procedure 'insert_anzahl_kinder_an_pv_beitrag' aufgerufen wird.
        :param neuanlage_anzahl_kinder: Name der Excel-Datei, dessen Daten in die Datenbank
        eingetragen werden sollen.
        """
        # Import der Daten aus der Excel-Datei in das Pandas-Dataframe und Uebertragung in Liste "liste_ma_daten"
        df_ma_daten = pd.read_excel(f"insert Sozialversicherungsdaten/{neuanlage_anzahl_kinder}",
                                    index_col='Daten', na_filter=False)
        liste_ma_daten = list(df_ma_daten.iloc[:, 0])

        # Daten aus importierter Excel-Tabelle '5 Anzahl Kinder Arbeitnehmer PV-Beitrag.xlsx' pruefen
        anzahl_kinder = self._existenz_zahlen_daten_feststellen(liste_ma_daten[0], 99, 'Anzahl Kinder', True)
        an_beitrag_pv_in_prozent = self._existenz_zahlen_daten_feststellen(liste_ma_daten[1],
                                                                           99,
                                                                           'AN-Beitrag PV in %',
                                                                           True)
        beitragsbemessungsgrenze_pv_ost = self._existenz_zahlen_daten_feststellen(liste_ma_daten[2],
                                                                                  99999999,
                                                                                  'Beitragsbemessungsgrenze PV Ost',
                                                                                  True)
        beitragsbemessungsgrenze_pv_west = self._existenz_zahlen_daten_feststellen(liste_ma_daten[3],
                                                                                   99999999,
                                                                                   'Beitragsbemessungsgrenze PV West',
                                                                                   True)

        eintragungsdatum = self._existenz_date_daten_feststellen(liste_ma_daten[4], 'Eintragungsdatum', True)

        conn = self._datenbankbverbindung_aufbauen()
        cur = conn.cursor()

        # Stored Procedure aufrufen und Daten an Datenbank uebergeben
        cur.callproc('insert_anzahl_kinder_an_pv_beitrag', [self.mandant_id,
                                                            anzahl_kinder,
                                                            an_beitrag_pv_in_prozent,
                                                            beitragsbemessungsgrenze_pv_ost,
                                                            beitragsbemessungsgrenze_pv_west,
                                                            eintragungsdatum])

        # Commit der Aenderungen
        conn.commit()

        # Cursor und Konnektor zu Datenbank schließen
        cur.close()
        conn.close()

    def insert_wohnhaft_sachsen_ag_pv_beitrag(self, neuanlage_wohnhaft_sachsen):
        """
        Diese Methode uebertraegt den Arbeitgeberbeitrag zur Pflichtversicherung in Abhaengigkeit des Wohnortes
        (im Rahmen der Bachelorarbeit dargestellt durch eine Excel-Datei) in die Datenbank, in dem
        der Stored Procedure 'insert_Sachsen' aufgerufen wird.
        :param neuanlage_wohnhaft_sachsen: Name der Excel-Datei, dessen Daten in die Datenbank
        eingetragen werden sollen.
        """

        # Import der Daten aus der Excel-Datei in das Pandas-Dataframe und Uebertragung in Liste "liste_ma_daten"
        df_ma_daten = pd.read_excel(f"insert Sozialversicherungsdaten/{neuanlage_wohnhaft_sachsen}",
                                    index_col='Daten', na_filter=False)
        liste_ma_daten = list(df_ma_daten.iloc[:, 0])

        # Daten aus importierter Excel-Tabelle '6 wohnhaft Sachsen Arbeitgeber PV-Beitrag.xlsx' pruefen
        wohnhaft_sachsen = self._existenz_boolean_daten_feststellen(liste_ma_daten[0], 'wohnhaft_Sachsen', True)
        ag_beitrag_pv_in_prozent = self._existenz_zahlen_daten_feststellen(liste_ma_daten[1],
                                                                           99,
                                                                           'AG-Beitrag PV in %',
                                                                           True)
        eintragungsdatum = self._existenz_date_daten_feststellen(liste_ma_daten[2], 'Eintragungsdatum', True)

        conn = self._datenbankbverbindung_aufbauen()
        cur = conn.cursor()

        # Stored Procedure aufrufen und Daten an Datenbank uebergeben
        cur.callproc('insert_Sachsen', [self.mandant_id, wohnhaft_sachsen, ag_beitrag_pv_in_prozent, eintragungsdatum])

        # Commit der Aenderungen
        conn.commit()

        # Cursor und Konnektor zu Datenbank schließen
        cur.close()
        conn.close()

    def insert_arbeitslosenversicherungsbeitraege(self, neuanlage_arbeitslosenversicherungsbeitraege):
        """
        Diese Methode uebertraegt die Arbeitslosenversicheurngsbeitragssaetze von Arbeitnehmer und Arbeitgeber sowie die
        Beitragsbemessungsgrenzen (im Rahmen der Bachelorarbeit dargestellt durch eine Excel-Datei) in die Datenbank, in
        dem der Stored Procedure 'insert_arbeitslosenversicherungsbeitraege' aufgerufen wird.
        :param neuanlage_arbeitslosenversicherungsbeitraege: Name der Excel-Datei, dessen Daten in die Datenbank
        eingetragen werden sollen.
        """

        # Import der Daten aus der Excel-Datei in das Pandas-Dataframe und Uebertragung in Liste "liste_ma_daten"
        df_ma_daten = pd.read_excel(f"insert Sozialversicherungsdaten/{neuanlage_arbeitslosenversicherungsbeitraege}",
                                    index_col='Daten', na_filter=False)
        liste_ma_daten = list(df_ma_daten.iloc[:, 0])

        # Daten aus importierter Excel-Tabelle '7 Arbeitslosenversicherungsbeitraege.xlsx' pruefen
        an_beitrag_av_in_prozent = self._existenz_zahlen_daten_feststellen(liste_ma_daten[0],
                                                                           99,
                                                                           'AN-Beitrag AV in %',
                                                                           True)
        ag_beitrag_av_in_prozent = self._existenz_zahlen_daten_feststellen(liste_ma_daten[1],
                                                                           99,
                                                                           'AG-Beitrag AV in %',
                                                                           True)
        beitragsbemessungsgrenze_av_ost = self._existenz_zahlen_daten_feststellen(liste_ma_daten[2],
                                                                                  99999999,
                                                                                  'Beitragsbemessungsgrenze AV Ost',
                                                                                  True)
        beitragsbemessungsgrenze_av_west = self._existenz_zahlen_daten_feststellen(liste_ma_daten[3],
                                                                                   99999999,
                                                                                   'Beitragsbemessungsgrenze AV West',
                                                                                   True)
        eintragungsdatum = self._existenz_date_daten_feststellen(liste_ma_daten[4], 'Eintragungsdatum', True)

        conn = self._datenbankbverbindung_aufbauen()
        cur = conn.cursor()

        # Stored Procedure aufrufen und Daten an Datenbank uebergeben
        cur.callproc('insert_arbeitslosenversicherungsbeitraege', [self.mandant_id,
                                                                   an_beitrag_av_in_prozent,
                                                                   ag_beitrag_av_in_prozent,
                                                                   beitragsbemessungsgrenze_av_ost,
                                                                   beitragsbemessungsgrenze_av_west,
                                                                   eintragungsdatum])

        # Commit der Aenderungen
        conn.commit()

        # Cursor und Konnektor zu Datenbank schließen
        cur.close()
        conn.close()

    def insert_rentenversicherungsbeitraege(self, neuanlage_rentenversicherungsbeitraege):
        """
        Diese Methode uebertraegt die Rentenversicherungsbeitragssaetze von Arbeitnehmer und Arbeitgeber sowie die
        Beitragsbemessungsgrenzen (im Rahmen der Bachelorarbeit dargestellt durch eine Excel-Datei) in die Datenbank, in
        dem der Stored Procedure 'insert_arbeitslosenversicherungsbeitraege' aufgerufen wird.
        :param neuanlage_rentenversicherungsbeitraege: Name der Excel-Datei, dessen Daten in die Datenbank
        eingetragen werden sollen.
        """

        # Import der Daten aus der Excel-Datei in das Pandas-Dataframe und Uebertragung in Liste "liste_ma_daten"
        df_ma_daten = pd.read_excel(f"insert Sozialversicherungsdaten/{neuanlage_rentenversicherungsbeitraege}",
                                    index_col='Daten', na_filter=False)
        liste_ma_daten = list(df_ma_daten.iloc[:, 0])

        # Daten aus importierter Excel-Tabelle '8 Rentenversicherungsbeitraege.xlsx' pruefen
        an_beitrag_rv_in_prozent = self._existenz_zahlen_daten_feststellen(liste_ma_daten[0],
                                                                           99,
                                                                           'AN-Beitrag RV in %',
                                                                           True)
        ag_beitrag_rv_in_prozent = self._existenz_zahlen_daten_feststellen(liste_ma_daten[1],
                                                                           99,
                                                                           'AG-Beitrag RV in %',
                                                                           True)
        beitragsbemessungsgrenze_rv_ost = self._existenz_zahlen_daten_feststellen(liste_ma_daten[2],
                                                                                  99999999,
                                                                                  'Beitragsbemessungsgrenze RV Ost',
                                                                                  True)
        beitragsbemessungsgrenze_rv_west = self._existenz_zahlen_daten_feststellen(liste_ma_daten[3],
                                                                                   99999999,
                                                                                   'Beitragsbemessungsgrenze RV West',
                                                                                   True)
        eintragungsdatum = self._existenz_date_daten_feststellen(liste_ma_daten[4], 'Eintragungsdatum', True)

        conn = self._datenbankbverbindung_aufbauen()
        cur = conn.cursor()

        # Stored Procedure aufrufen und Daten an Datenbank uebergeben
        cur.callproc('insert_rentenversicherungsbeitraege', [self.mandant_id,
                                                             an_beitrag_rv_in_prozent,
                                                             ag_beitrag_rv_in_prozent,
                                                             beitragsbemessungsgrenze_rv_ost,
                                                             beitragsbemessungsgrenze_rv_west,
                                                             eintragungsdatum])

        # Commit der Aenderungen
        conn.commit()

        # Cursor und Konnektor zu Datenbank schließen
        cur.close()
        conn.close()

    def insert_minijobbeitraege(self, neuanlage_minijobbeitraege):
        """
        Diese Methode uebertraegt Minijobbeitragssaetze von Arbeitnehmer und Arbeitgeber sowie die Umlagen und
         Pauschalsteuer (im Rahmen der Bachelorarbeit dargestellt durch eine Excel-Datei) in die Datenbank, in
        dem der Stored Procedure 'insert_Minijob' aufgerufen wird.
        :param neuanlage_minijobbeitraege: Name der Excel-Datei, dessen Daten in die Datenbank
        eingetragen werden sollen.
        """

        # Import der Daten aus der Excel-Datei in das Pandas-Dataframe und Uebertragung in Liste "liste_ma_daten"
        df_ma_daten = pd.read_excel(f"insert Sozialversicherungsdaten/{neuanlage_minijobbeitraege}",
                                    index_col='Daten', na_filter=False)
        liste_ma_daten = list(df_ma_daten.iloc[:, 0])

        # Daten aus importierter Excel-Tabelle '9 Minijobbeitraege.xlsx' pruefen
        kurzfristig_beschaeftigt = self._existenz_boolean_daten_feststellen(liste_ma_daten[0],
                                                                            'kurzfristige Minijobtaetigkeit?',
                                                                            True)
        ag_beitrag_kv_in_prozent = self._existenz_zahlen_daten_feststellen(liste_ma_daten[1],
                                                                           99,
                                                                           'AG-Beitrag KV Minijob in %',
                                                                           True)
        ag_beitrag_rv_in_prozent = self._existenz_zahlen_daten_feststellen(liste_ma_daten[2],
                                                                           99,
                                                                           'AG-Beitrag RV Minijob in %',
                                                                           True)
        an_beitrag_rv_in_prozent = self._existenz_zahlen_daten_feststellen(liste_ma_daten[3],
                                                                           99,
                                                                           'AN-Beitrag RV Minijob in %',
                                                                           True)
        u1_umlage = self._existenz_zahlen_daten_feststellen(liste_ma_daten[4], 99, 'U1-Umlage Minijob in %', True)
        u2_umlage = self._existenz_zahlen_daten_feststellen(liste_ma_daten[5], 99, 'U2-Umlage Minijob in %', True)
        insolvenzgeldumlage = self._existenz_zahlen_daten_feststellen(liste_ma_daten[6],
                                                                      99,
                                                                      'Insolvenzgeldumlage Minijob in %',
                                                                      True)
        pauschalsteuer = self._existenz_zahlen_daten_feststellen(liste_ma_daten[7],
                                                                 99,
                                                                 'Pauschalsteuer Minijob in %',
                                                                 True)
        eintragungsdatum = self._existenz_date_daten_feststellen(liste_ma_daten[8], 'Eintragungsdatum', True)

        conn = self._datenbankbverbindung_aufbauen()
        cur = conn.cursor()

        # Stored Procedure aufrufen und Daten an Datenbank uebergeben
        cur.callproc('insert_Minijob', [self.mandant_id,
                                        kurzfristig_beschaeftigt,
                                        ag_beitrag_kv_in_prozent,
                                        ag_beitrag_rv_in_prozent,
                                        an_beitrag_rv_in_prozent,
                                        u1_umlage,
                                        u2_umlage,
                                        insolvenzgeldumlage,
                                        pauschalsteuer,
                                        eintragungsdatum])

        # Commit der Aenderungen
        conn.commit()

        # Cursor und Konnektor zu Datenbank schließen
        cur.close()
        conn.close()

    def insert_berufsgenossenschaft(self, neuanlage_berufsgenossenschaft):
        """
        Diese Methode uebertraegt eine Berufsgenossenschaft in die Datenbank (im Rahmen der Bachelorarbeit dargestellt
        durch eine Excel-Datei), in dem die Stored Procedure 'insert_berufsgenossenschaft' aufgerufen wird.
        :param neuanlage_berufsgenossenschaft: Name der Excel-Datei, dessen Daten in die Datenbank eingetragen werden
        sollen.
        """

        # Import der Daten aus der Excel-Datei in das Pandas-Dataframe und Uebertragung in Liste "liste_ma_daten"
        df_ma_daten = pd.read_excel(f"insert Sozialversicherungsdaten/{neuanlage_berufsgenossenschaft}",
                                    index_col='Daten', na_filter=False)
        liste_ma_daten = list(df_ma_daten.iloc[:, 0])

        # Daten aus importierter Excel-Tabelle '10 Berufsgenossenschaft.xlsx' pruefen
        berufsgenossenschaft = self._existenz_str_daten_feststellen(liste_ma_daten[0],
                                                                    'Berufsgenossenschaft',
                                                                    128,
                                                                    True)
        abkuerzung = self._existenz_str_daten_feststellen(liste_ma_daten[1],
                                                          'Berufsgenossenschaftskuerzel',
                                                          16,
                                                          True)

        conn = self._datenbankbverbindung_aufbauen()
        cur = conn.cursor()

        # Stored Procedure aufrufen und Daten an Datenbank uebergeben
        cur.callproc('insert_berufsgenossenschaft', [self.mandant_id, berufsgenossenschaft, abkuerzung])

        # Commit der Aenderungen
        conn.commit()

        # Cursor und Konnektor zu Datenbank schließen
        cur.close()
        conn.close()

    def insert_unfallversicherungsbeitrag(self, neuanlage_unfallversicherungsbeitrag):
        """
        Diese Methode uebertraegt eine Berufsgenossenschaft in die Datenbank (im Rahmen der Bachelorarbeit dargestellt
        durch eine Excel-Datei), in dem die Stored Procedure 'insert_unfallversicherungsbeitrag' aufgerufen wird.
        :param neuanlage_unfallversicherungsbeitrag: Name der Excel-Datei, dessen Daten in die Datenbank eingetragen
        werden sollen.
        """

        # Import der Daten aus der Excel-Datei in das Pandas-Dataframe und Uebertragung in Liste "liste_ma_daten"
        df_ma_daten = pd.read_excel(f"insert Sozialversicherungsdaten/{neuanlage_unfallversicherungsbeitrag}",
                                    index_col='Daten', na_filter=False)
        liste_ma_daten = list(df_ma_daten.iloc[:, 0])

        # Daten aus importierter Excel-Tabelle '11 Unfallversicherungsbeitrag.xlsx' pruefen
        gesellschaft = self._existenz_str_daten_feststellen(liste_ma_daten[0], 'Gesellschaft', 128, True)
        gesellschaftskuerzel = self._existenz_str_daten_feststellen(liste_ma_daten[1], 'Gesellschaftskuerzel', 16, True)
        berufsgenossenschaft = self._existenz_str_daten_feststellen(liste_ma_daten[2],
                                                                    'Berufsgenossenschaft',
                                                                    128,
                                                                    True)
        berufsgenossenschaftskuerzel = self._existenz_str_daten_feststellen(liste_ma_daten[3],
                                                                            'Berufsgenossenschaftskuerzel',
                                                                            16,
                                                                            True)
        jahresbeitrag_unfallversicherung = self._existenz_zahlen_daten_feststellen(liste_ma_daten[4],
                                                                                   9999999999,
                                                                                   'Betrag',
                                                                                   True)
        beitragsjahrjahr_uv = self._existenz_zahlen_daten_feststellen(liste_ma_daten[5],
                                                                      9999,
                                                                      'Beitragsjahr Unfallversicherung',
                                                                      True)

        conn = self._datenbankbverbindung_aufbauen()
        cur = conn.cursor()

        # Stored Procedure aufrufen und Daten an Datenbank uebergeben
        cur.callproc('insert_unfallversicherungsbeitrag', [self.mandant_id,
                                                           gesellschaft,
                                                           gesellschaftskuerzel,
                                                           berufsgenossenschaft,
                                                           berufsgenossenschaftskuerzel,
                                                           jahresbeitrag_unfallversicherung,
                                                           beitragsjahrjahr_uv])

        # Commit der Aenderungen
        conn.commit()

        # Cursor und Konnektor zu Datenbank schließen
        cur.close()
        conn.close()

    def insert_gewerkschaft(self, neuanlage_gewerkschaft):
        """
        Diese Methode uebertraegt den Namen der Gewerkschaft (im Rahmen der Bachelorarbeit dargestellt durch eine
        Excel-Datei) in die Datenbank, in dem der Stored Procedure 'insert_tarif' aufgerufen wird.
        :param neuanlage_gewerkschaft: Name der Excel-Datei, dessen Daten in die Datenbank
        eingetragen werden sollen.
        """

        # Import der Daten aus der Excel-Datei in das Pandas-Dataframe und Uebertragung in Liste "liste_ma_daten"
        df_ma_daten = pd.read_excel(f"insert Entgeltdaten/{neuanlage_gewerkschaft}", index_col='Daten', na_filter=False)
        liste_ma_daten = list(df_ma_daten.iloc[:, 0])

        # Daten aus importierter Excel-Tabelle '2 Tarif.xlsx' pruefen
        gewerkschaft = self._existenz_str_daten_feststellen(liste_ma_daten[0], 'Gewerkschaft', 64, True)
        branche = self._existenz_str_daten_feststellen(liste_ma_daten[1], 'Branche', 64, True)

        conn = self._datenbankbverbindung_aufbauen()
        cur = conn.cursor()

        # Stored Procedure aufrufen und Daten an Datenbank uebergeben
        cur.callproc('insert_gewerkschaft', [self.mandant_id, gewerkschaft, branche])

        # Commit der Aenderungen
        conn.commit()

        # Cursor und Konnektor zu Datenbank schließen
        cur.close()
        conn.close()

    def insert_tarif(self, neuanlage_tarif):
        """
        Diese Methode uebertraegt den Namen eines Tarifs und verknuepft diese mit der Gewerkschaft (im Rahmen der
        Bachelorarbeit dargestellt durch eine Excel-Datei), die fuer diese zustaendig ist, in die Datenbank, in dem der
        Stored Procedure 'insert_Tarif' aufgerufen wird.
        :param neuanlage_tarif: Name der Excel-Datei, dessen Daten in die Datenbank
        eingetragen werden sollen.
        """

        # Import der Daten aus der Excel-Datei in das Pandas-Dataframe und Uebertragung in Liste "liste_ma_daten"
        df_ma_daten = pd.read_excel(f"insert Entgeltdaten/{neuanlage_tarif}", index_col='Daten', na_filter=False)
        liste_ma_daten = list(df_ma_daten.iloc[:, 0])

        # Daten aus importierter Excel-Tabelle '2 Tarif.xlsx' pruefen
        tarifbezeichnung = self._existenz_str_daten_feststellen(liste_ma_daten[0], 'Tarifbezeichnung', 16, True)
        gewerkschaft = self._existenz_str_daten_feststellen(liste_ma_daten[1], 'Gewerkschaft', 64, True)
        branche = self._existenz_str_daten_feststellen(liste_ma_daten[2], 'Branche', 64, True)

        conn = self._datenbankbverbindung_aufbauen()
        cur = conn.cursor()

        # Stored Procedure aufrufen und Daten an Datenbank uebergeben
        cur.callproc('insert_tarif', [self.mandant_id, tarifbezeichnung, gewerkschaft, branche])

        # Commit der Aenderungen
        conn.commit()

        # Cursor und Konnektor zu Datenbank schließen
        cur.close()
        conn.close()

    def insert_verguetungsbestandteil(self, neuanlage_verguetungsbestandteil):
        """
        Diese Methode uebertraegt einen Verguetungsbestandteil wie bspw. Grundgehalt, Urlaubsgeld etc. und verknuepft
        sie mit dem entsprechenden Tarif (im Rahmen der Bachelorarbeit dargestellt durch eine Excel-Datei), in die
        Datenbank, in dem die Stored Procedure 'insert_verguetungsbestandteil' aufgerufen wird.
        :param neuanlage_verguetungsbestandteil: Name der Excel-Datei, dessen Daten in die Datenbank
        eingetragen werden sollen.
        """

        # Import der Daten aus der Excel-Datei in das Pandas-Dataframe und Uebertragung in Liste "liste_ma_daten"
        df_ma_daten = pd.read_excel(f"insert Entgeltdaten/{neuanlage_verguetungsbestandteil}",
                                    index_col='Daten', na_filter=False)
        liste_ma_daten = list(df_ma_daten.iloc[:, 0])

        # Daten aus importierter Excel-Tabelle '3 Verguetungsbestandteil.xlsx' pruefen
        verguetungsbestandteil = self._existenz_str_daten_feststellen(liste_ma_daten[0],
                                                                      'Verguetungsbestandteil',
                                                                      64,
                                                                      True)
        auszahlungsmonat = self._existenz_str_daten_feststellen(liste_ma_daten[1], 'Auszahlungsmonat', 16, True)
        tarifbezeichnung = self._existenz_str_daten_feststellen(liste_ma_daten[2], 'Tarifbezeichnung', 16, True)
        betrag = self._existenz_zahlen_daten_feststellen(liste_ma_daten[3], 99999999, 'Betrag', True)
        gueltig_ab = self._existenz_date_daten_feststellen(liste_ma_daten[4], 'Tarifentgelt gueltig ab', True)

        conn = self._datenbankbverbindung_aufbauen()
        cur = conn.cursor()

        # Stored Procedure aufrufen und Daten an Datenbank uebergeben
        cur.callproc('insert_tarifliches_verguetungsbestandteil', [self.mandant_id,
                                                                   verguetungsbestandteil,
                                                                   auszahlungsmonat,
                                                                   tarifbezeichnung,
                                                                   betrag,
                                                                   gueltig_ab])

        # Commit der Aenderungen
        conn.commit()

        # Cursor und Konnektor zu Datenbank schließen
        cur.close()
        conn.close()

    def insert_neuer_mitarbeiter(self, mitarbeiterdaten):
        """
        Diese Methode überträgt die eingetragenen Mitarbeiterdaten (im Rahmen der Bachelorarbeit
        dargestellt durch eine Excel-Datei) in die Datenbank, in dem der Stored Procedure
        'insert_neuer_mitarbeiter' aufgerufen wird.
        :param mitarbeiterdaten: Name der Excel-Datei, dessen Mitarbeiterdaten in die Datenbank
        eingetragen werden sollen.
        """

        # Import der Daten aus der Excel-Datei in das Pandas-Dataframe und Uebertragung in Liste "liste_ma_daten"
        df_ma_daten = pd.read_excel(f"Mitarbeiterdaten/{mitarbeiterdaten}", index_col='Daten', na_filter=False)
        liste_ma_daten = list(df_ma_daten.iloc[:, 0])

        # Daten aus importierter Excel-Tabelle 'Neuanlage Mitarbeiter.xlsx' pruefen
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

        # Beitraege fuer gesetzliche Kranken- und Pflege-Versicherungen
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
        anzahl_kinder = self._existenz_zahlen_daten_feststellen(liste_ma_daten[49], 99, 'Anzahl Kinder', False)
        an_anteil_pv_beitrag_in_prozent = self._existenz_zahlen_daten_feststellen(liste_ma_daten[50],
                                                                                  99,
                                                                                  'AN-Anteil Pflegeversicherung in %',
                                                                                  False)
        beitragsbemessungsgrenze_pv_ost = self._existenz_zahlen_daten_feststellen(liste_ma_daten[51],
                                                                                  99999999,
                                                                                  'Beitragsbemessungsgrenze PV Ost',
                                                                                  False)
        beitragsbemessungsgrenze_pv_west = self._existenz_zahlen_daten_feststellen(liste_ma_daten[52],
                                                                                   99999999,
                                                                                   'Beitragsbemessungsgrenze PV West',
                                                                                   False)
        wohnhaft_sachsen = self._existenz_boolean_daten_feststellen(liste_ma_daten[53], 'wohnhaft Sachsen', False)
        ag_anteil_pv_beitrag_in_prozent = self._existenz_zahlen_daten_feststellen(liste_ma_daten[54],
                                                                                  99,
                                                                                  'AG-Anteil Pflegeversicherung in %',
                                                                                  False)
        # Werte für gesetzliche Arbeitslosenversicherung
        arbeitslosenversichert = self._existenz_boolean_daten_feststellen(liste_ma_daten[55],
                                                                          'arbeitslosenversichert?',
                                                                          False)
        ag_anteil_av_beitrag_in_prozent = self._existenz_zahlen_daten_feststellen(liste_ma_daten[56],
                                                                                  99,
                                                                                  'AG-Anteil Arbeitslosenvers. in %',
                                                                                  False)
        an_anteil_av_beitrag_in_prozent = self._existenz_zahlen_daten_feststellen(liste_ma_daten[57],
                                                                                  99,
                                                                                  'AN-Anteil Arbeitslosenvers. in %',
                                                                                  False)
        beitragsbemessungsgrenze_av_ost = self._existenz_zahlen_daten_feststellen(liste_ma_daten[58],
                                                                                  99999999,
                                                                                  'Beitragsbemessungsgrenze AV Ost',
                                                                                  False)
        beitragsbemessungsgrenze_av_west = self._existenz_zahlen_daten_feststellen(liste_ma_daten[59],
                                                                                   99999999,
                                                                                   'Beitragsbemessungsgrenze AV West',
                                                                                   False)

        # Werte für gesetzliche Rentenversicherung
        rentenversichert = self._existenz_boolean_daten_feststellen(liste_ma_daten[60], 'rentenversichert?', False)
        ag_anteil_rv_beitrag_in_prozent = self._existenz_zahlen_daten_feststellen(liste_ma_daten[61],
                                                                                  99,
                                                                                  'AG-Anteil Rentenversicherung in %',
                                                                                  False)
        an_anteil_rv_beitrag_in_prozent = self._existenz_zahlen_daten_feststellen(liste_ma_daten[62],
                                                                                  99,
                                                                                  'AN-Anteil Rentenversicherung in %',
                                                                                  False)
        beitragsbemessungsgrenze_rv_ost = self._existenz_zahlen_daten_feststellen(liste_ma_daten[63],
                                                                                  99999999,
                                                                                  'Beitragsbemessungsgrenze RV Ost',
                                                                                  False)
        beitragsbemessungsgrenze_rv_west = self._existenz_zahlen_daten_feststellen(liste_ma_daten[64],
                                                                                   99999999,
                                                                                   'Beitragsbemessungsgrenze RV West',
                                                                                   False)

        conn = self._datenbankbverbindung_aufbauen()
        cur = conn.cursor()

        # Stored Procedure aufrufen und Daten an Datenbank uebergeben
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
                                                 gkv_zusatzbeitrag_in_prozent,
                                                 anzahl_kinder,
                                                 an_anteil_pv_beitrag_in_prozent,
                                                 beitragsbemessungsgrenze_pv_ost,
                                                 beitragsbemessungsgrenze_pv_west,
                                                 wohnhaft_sachsen,
                                                 ag_anteil_pv_beitrag_in_prozent,
                                                 arbeitslosenversichert,
                                                 ag_anteil_av_beitrag_in_prozent,
                                                 an_anteil_av_beitrag_in_prozent,
                                                 beitragsbemessungsgrenze_av_ost,
                                                 beitragsbemessungsgrenze_av_west,
                                                 rentenversichert,
                                                 ag_anteil_rv_beitrag_in_prozent,
                                                 an_anteil_rv_beitrag_in_prozent,
                                                 beitragsbemessungsgrenze_rv_ost,
                                                 beitragsbemessungsgrenze_rv_west
                                                 ])

        # Commit der Aenderungen
        conn.commit()

        # Cursor und Konnektor zu Datenbank schließen
        cur.close()
        conn.close()

    def update_adresse(self, adressdaten):
        """
        Diese Methode überträgt die neue Adresse eines Mitarbeiters (im Rahmen der Bachelorarbeit
        dargestellt durch eine Excel-Datei) in die Datenbank, in dem der Stored Procedure
        'update_adresse' aufgerufen wird.
        :param adressdaten: Name der Excel-Datei, dessen Adressdaten in die Datenbank
        eingetragen werden sollen.
        """

        # Import der Daten aus der Excel-Datei in das Pandas-Dataframe und Uebertragung in Liste "liste_ma_daten"
        df_ma_daten = pd.read_excel(f"Mitarbeiterdaten/{adressdaten}", index_col='Daten', na_filter=False)
        liste_ma_daten = list(df_ma_daten.iloc[:, 0])

        personalnummer = self._existenz_str_daten_feststellen(liste_ma_daten[0], 'Personalnummer', 32, True)
        neuer_eintrag_gueltig_ab = self._existenz_date_daten_feststellen(liste_ma_daten[1], 'Gueltig ab', True)
        alter_eintrag_gueltig_bis = self._vorherigen_tag_berechnen(neuer_eintrag_gueltig_ab)
        strasse = self._existenz_str_daten_feststellen(liste_ma_daten[2], 'Strasse', 64, True)
        hausnummer = self._existenz_str_daten_feststellen(liste_ma_daten[3], 'Hausnummer', 8, True)
        postleitzahl = self._existenz_str_daten_feststellen(liste_ma_daten[4], 'Postleitzahl', 16, True)
        stadt = self._existenz_str_daten_feststellen(liste_ma_daten[5], 'Stadt', 128, True)
        region = self._existenz_str_daten_feststellen(liste_ma_daten[6], 'Region', 128, True)
        land = self._existenz_str_daten_feststellen(liste_ma_daten[7], 'Land', 128, True)

        conn = self._datenbankbverbindung_aufbauen()
        cur = conn.cursor()

        # Stored Procedure aufrufen
        cur.callproc('update_adresse', [self.mandant_id,
                                        personalnummer,
                                        neuer_eintrag_gueltig_ab,
                                        alter_eintrag_gueltig_bis,
                                        strasse,
                                        hausnummer,
                                        postleitzahl,
                                        stadt,
                                        region,
                                        land
                                        ])

        conn = self._datenbankbverbindung_aufbauen()
        conn.commit()

        # Cursor und Konnektor zu Datenbank schließen
        cur.close()
        conn.close()

    def delete_mandantendaten(self):
        """
        Methode ruft die Stored Procedure 'delete_mandantendaten' auf, welche alle Daten des Mandanten aus allen
        Tabellen entfernt.
        """
        conn = self._datenbankbverbindung_aufbauen()

        # Ein Cursor-Objekt erstellen
        cur = conn.cursor()

        # Stored Procedure aufrufen
        cur.callproc('delete_mandantendaten', [self.mandant_id])

        # Commit der Änderungen
        conn.commit()

        # Cursor und Konnektor zu Datenbank schließen
        cur.close()
        conn.close()

    def delete_mitarbeiterdaten(self, mitarbeiter):
        """
        Methode ruft die Stored Procedure 'delete_mitarbeiterdaten' auf, welche alle personenbezogenen Daten
        eines Mitarbeiters aus den Assoziationstabellen, der Tabelle 'Privat_Krankenversicherte' und der
        zentralen Tabelle entfernt
        :param mitarbeiter: Name der Excel-Datei, die die Personalnummer des Mitarbeiters enthaelt, der entfernt
                            werden soll
        """

        # Import der Daten aus der Excel-Datei in das Pandas-Dataframe und Übertrag in Liste "liste_ma_daten"
        df_ma_daten = pd.read_excel(f"Mitarbeiterdaten/{mitarbeiter}", index_col='Daten', na_filter=False)
        liste_ma_daten = list(df_ma_daten.iloc[:, 0])

        personalnummer = self._existenz_str_daten_feststellen(liste_ma_daten[0], 'Personalnummer', 32, True)

        conn = self._datenbankbverbindung_aufbauen()
        cur = conn.cursor()

        # Stored Procedure aufrufen
        cur.callproc('delete_mitarbeiterdaten', [self.mandant_id, personalnummer])

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
        elif not isinstance(zahlen_daten, int) and not isinstance(zahlen_daten, float):
            raise (TypeError(f"Der übergebene Wert '{zahlen_daten}' konnte nicht in eine Gleitkommazahl "
                             f"konvertiert werden!"))
        elif zahlen_daten > hoechstbetrag:
            raise (ValueError(f"'{art}' ist mit '{zahlen_daten}' hoeher als der zulaessige Maximalbetrag von "
                              f"'{hoechstbetrag}'!"))
        elif art == 'Anzahl Kinder' or art == 'Beitragsjahr Unfallversicherung':
            zahlen_daten = int(zahlen_daten)
        else:
            zahlen_daten = round(decimal.Decimal(zahlen_daten), 2)

        return zahlen_daten

    def _existenz_boolean_daten_feststellen(self, boolean_daten, art, pflicht):
        """
            Methode stellt fest, ob optionale Daten vorliegen oder nicht und wenn ja, so sollen diese auf jeden Fall
            als boolean-Datentyp zurückgegeben werden. So soll sichergestellt werden, dass dem Datenbanksystem die Daten
            in dem Datentyp übergeben werden, in der sie in der Personalstammdatenbank gespeichert werden können.
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

    def _vorherigen_tag_berechnen(self, datum):
        """
        Methode berechnet den Vortag des Datums, ab dem ein neuer Eintrag gültig sein soll. Dies wird benoetigt,
        um in der Spalte "Datum_Bis" des vorherigen Eintrags (gilt für alle Assoziationstabellen) ein Datum eintragen
        zu koennen.
        :param datum: Datum, ab dem ein neuer Eintrag gueltig werden soll
        :return: Datum des Vortags, dass gleichzeitig das Enddatum des alten Eintrags ist
        """
        tag_abziehen = timedelta(1)

        try:
            letzter_tag_alter_eintrag = datum - tag_abziehen
        except ValueError:
            raise (ValueError(f"'{datum}' ist nicht möglich!"))
        except TypeError:
            raise (TypeError(f"'{datum}' ist kein datetime-Objekt!"))

        return letzter_tag_alter_eintrag
