import decimal
import pandas as pd
import re
from datetime import datetime, timedelta
from src.main.Datenbankverbindung import datenbankbverbindung_aufbauen


class Nutzer:

    def __init__(self, mandant_id, personalnummer, vorname, nachname, passwort, passwort_wiederholen, schema='public'):

        if personalnummer == "":
            raise (ValueError("Die Personalnummer des Nutzers muss aus mindestens einem Zeichen bestehen."))

        if len(str(personalnummer)) > 32:
            raise (ValueError(f"Die Personalnummer darf hoechstens 32 Zeichen lang sein. "
                              f"'{personalnummer}' besitzt {len(str(personalnummer))} Zeichen!"))

        if str(vorname) == "":
            raise (ValueError(f"Der Vorname des Nutzers muss aus mindestens einem Zeichen bestehen."))

        if len(str(vorname)) > 64:
            raise (ValueError(f"Der Vorname darf hoechstens 64 Zeichen lang sein. "
                              f"'{vorname}' besitzt {len(vorname)} Zeichen!"))

        if str(nachname) == "":
            raise (ValueError(f"Der Nachname des Nutzers muss aus mindestens einem Zeichen bestehen."))

        if len(str(nachname)) > 64:
            raise (ValueError(f"Der Nachname darf hoechstens 64 Zeichen lang sein. "
                              f"'{nachname}' besitzt {len(nachname)} Zeichen!"))

        if len(str(passwort)) > 128:
            raise (ValueError("Passwort darf hoechstens 128 Zeichen haben!"))

        if passwort != passwort_wiederholen:
            raise (ValueError("Passwoerter stimmen nicht ueberein!"))

        self.schema = schema
        self.mandant_id = mandant_id
        self.personalnummer = str(personalnummer)
        self.vorname = str(vorname)
        self.nachname = str(nachname)
        self.nutzer_id = self._in_datenbank_anlegen(str(passwort))
        self.neues_passwort_geaendert = False

    def get_nutzer_id(self):
        return self.nutzer_id

    def get_personalnummer(self):
        return self.personalnummer

    def get_vorname(self):
        return self.vorname

    def get_nachname(self):
        return self.nachname

    def _in_datenbank_anlegen(self, passwort):
        """
        Methode ruft die Stored Procedure 'nutzer_anlegen' auf, welche die Daten des Nutzers in der
        Personalstammdatenbank speichert.
        :param passwort: Passwort des Nutzers, welches in die Datenbank gespeichert wird
        :return: Nutzer_ID, welche als Objekt-Variable gespeichert wird
        """

        conn = datenbankbverbindung_aufbauen()

        nutzer_insert_query = f"set search_path to {self.schema};" \
                              f"SELECT nutzer_anlegen('{self.mandant_id}', '{self.personalnummer}', " \
                              f"'{self.vorname}', '{self.nachname}', '{passwort}')"
        cur = conn.cursor()
        nutzer_id = cur.execute(nutzer_insert_query)

        # Commit der Aenderungen
        conn.commit()

        # Cursor und Konnektor zu Datenbank schliessen
        cur.close()
        conn.close()

        return nutzer_id

    def passwort_aendern(self, neues_passwort, neues_passwort_wiederholen):
        """
        Diese Funktion wird aufgerufen, wenn der Administrator den Nutzer entsperren und das Passwort zurueckgesetzt
        hat. In dem Zuge vergibt der Administrator ein neues Passwort, welches er dann aber kennt. Mit dieser Funktion
        ist der Nutzer gezwungen, daraufhin ein neues Passwort zu vergeben, womit der Administrator das dann gueltige
        Passwort des Nutzers nicht mehr kennt
        :param neues_passwort: Passwort des Nutzers
        :param neues_passwort_wiederholen: Test, um zu pruefen, ob das gewaehlte Passwort des Administrators beim ersten
                                           Mal wie beabsichtigt eingegeben wurde
        """
        if neues_passwort != neues_passwort_wiederholen:
            raise(ValueError("Zweite Passworteingabe ist anders als erste Passworteingabe!"))

        conn = datenbankbverbindung_aufbauen()

        nutzer_insert_query = f"set search_path to {self.schema};" \
                              f"CALL nutzerpasswort_aendern('{self.mandant_id}', '{self.personalnummer}', " \
                              f"'{neues_passwort}')"
        cur = conn.cursor()
        cur.execute(nutzer_insert_query)

        # Commit der Aenderungen
        conn.commit()

        # Cursor und Konnektor zu Datenbank schliessen
        cur.close()
        conn.close()

        self.neues_passwort_geaendert = True

    def abfrage_ausfuehren(self, abfrage):
        """
        Methode uebermittelt ein SQL-Befehl an die Datenbank, wo sie ausgefuehrt und das Ergebnis zurueckgegeben wird.
        :param abfrage: enthaelt den SQL-SELECT-Befehl.
        :return: Ergebnis der Datenbankabfrage
        """
        if not self.neues_passwort_geaendert:
            raise(ValueError("Ihr Administrator hat ein neues Passwort vergeben. Bitte wechseln Sie Ihr Passwort!"))

        conn = datenbankbverbindung_aufbauen()

        with conn.cursor() as cur:
            cur.execute(f"set search_path to {self.schema};"
                        f"SET session role tenant_user;"
                        f"SET app.current_tenant='{self.mandant_id}';"
                        f"{abfrage}")
            ergebnis = cur.fetchall()

        # Commit der Aenderungen
        conn.commit()

        # Cursor und Konnektor zu Datenbank schliessen
        cur.close()
        conn.close()

        return ergebnis

    def insert_krankenversicherungsbeitraege(self, neuanlage_krankenversicherungsbeitraege):
        """
        Diese Methode uebertraegt die eingetragenen Krankenversicherungsbeitraege in die Datenbank, in dem der Stored
        Procedure 'insert_krankenversicherungsbeitraege' aufgerufen wird.
        :param neuanlage_krankenversicherungsbeitraege: Name der Excel-Datei, dessen Daten in die Datenbank eingetragen
                                                        werden sollen.
        """
        if not self.neues_passwort_geaendert:
            raise(ValueError("Ihr Administrator hat ein neues Passwort vergeben. Bitte wechseln Sie Ihr Passwort!"))

        # Import der Daten aus der Excel-Datei in das Pandas-Dataframe und Uebertragung in Liste "daten"
        daten = self._import_excel_daten(neuanlage_krankenversicherungsbeitraege)

        # Daten aus importierter Excel-Tabelle '2 insert Sozialversicherungsdaten/1 Krankenversicherungsbeitraege.xlsx'
        # pruefen
        ermaessigter_beitragssatz = self._existenz_boolean_daten_feststellen(daten[0],
                                                                             'ermaessigter Beitragssatz',
                                                                             True)
        ag_gkv_beitrag_in_prozent = self._existenz_zahlen_daten_feststellen(daten[1],
                                                                            99,
                                                                            'Arbeitgeberbeitrag GKV in Prozent',
                                                                            True)
        an_gkv_beitrag_in_prozent = self._existenz_zahlen_daten_feststellen(daten[2],
                                                                            99,
                                                                            'Arbeitnehmerbeitrag GKV in Prozent',
                                                                            True)
        beitragsbemessungsgrenze_gkv = self._existenz_zahlen_daten_feststellen(daten[3],
                                                                               99999999,
                                                                               'Beitragsbemessungsgrenze GKV',
                                                                               True)
        jahresarbeitsentgeltgrenze_gkv = self._existenz_zahlen_daten_feststellen(daten[4],
                                                                                 99999999,
                                                                                 'Jahresarbeitsentgeltgrenze GKV',
                                                                                 True)
        eintragungsdatum = self._existenz_date_daten_feststellen(daten[5], 'Eintragungsdatum', True)

        export_daten = [self.mandant_id,
                        ermaessigter_beitragssatz,
                        ag_gkv_beitrag_in_prozent,
                        an_gkv_beitrag_in_prozent,
                        beitragsbemessungsgrenze_gkv,
                        jahresarbeitsentgeltgrenze_gkv,
                        eintragungsdatum]

        self._export_zu_db('insert_krankenversicherungsbeitraege(%s,%s,%s,%s,%s,%s,%s)', export_daten)

    def insert_gesetzliche_krankenkasse(self, neuanlage_gesetzliche_krankenkasse):
        """
        Diese Methode uebertraegt die eingetragene gesetzliche Krankenkasse mit deren Zusatzbeitrag und Umlagen in die
        Datenbank, in dem der Stored Procedure 'insert_gesetzliche_Krankenkasse' aufgerufen wird.
        :param neuanlage_gesetzliche_krankenkasse: Name der Excel-Datei, dessen Daten in die Datenbank eingetragen
                                                   werden sollen.
        """
        if not self.neues_passwort_geaendert:
            raise(ValueError("Ihr Administrator hat ein neues Passwort vergeben. Bitte wechseln Sie Ihr Passwort!"))

        # Import der Daten aus der Excel-Datei in das Pandas-Dataframe und Uebertragung in Liste "daten"
        daten = self._import_excel_daten(neuanlage_gesetzliche_krankenkasse)

        # Daten aus importierter Excel-Tabelle '2 insert Sozialversicherungsdaten/2 gesetzliche Krankenkasse.xlsx'
        # pruefen
        krankenkasse_voller_name = self._existenz_str_daten_feststellen(daten[0], 'Krankenkasse voller Name', 128, True)
        krankenkasse_abkuerzung = self._existenz_str_daten_feststellen(daten[1], 'Krankenkasse Abkuerzung', 16, False)
        zusatzbeitrag_ag_anteil = self._existenz_zahlen_daten_feststellen(daten[2],
                                                                          99,
                                                                          'Zusatzbeitrag Krankenkasse AG-Anteil',
                                                                          True)
        zusatzbeitrag_an_anteil = self._existenz_zahlen_daten_feststellen(daten[3],
                                                                          99,
                                                                          'Zusatzbeitrag Krankenkasse AN-Anteil',
                                                                          True)
        u1_umlage = self._existenz_zahlen_daten_feststellen(daten[4], 99, 'U1-Umlage', True)
        u2_umlage = self._existenz_zahlen_daten_feststellen(daten[5], 99, 'U2-Umlage', True)
        insolvenzgeldumlage = self._existenz_zahlen_daten_feststellen(daten[6], 99, 'Insolvenzgeldumlage', True)
        eintragungsdatum = self._existenz_date_daten_feststellen(daten[7], 'Eintragungsdatum', True)

        export_daten = [self.mandant_id,
                        krankenkasse_voller_name,
                        krankenkasse_abkuerzung,
                        zusatzbeitrag_ag_anteil,
                        zusatzbeitrag_an_anteil,
                        u1_umlage,
                        u2_umlage,
                        insolvenzgeldumlage,
                        'gesetzlich',
                        eintragungsdatum]

        self._export_zu_db('insert_gesetzliche_Krankenkasse(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)', export_daten)

    def insert_private_krankenkasse(self, neuanlage_private_krankenkasse):
        """
        Diese Methode uebertraegt die eingetragene private Krankenkasse mit deren Umlagen in die Datenbank, in dem der
        Stored Procedure 'insert_private_Krankenkasse' aufgerufen wird.
        :param neuanlage_private_krankenkasse: Name der Excel-Datei, dessen Daten in die Datenbank
                                               eingetragen werden sollen.
        """
        if not self.neues_passwort_geaendert:
            raise(ValueError("Ihr Administrator hat ein neues Passwort vergeben. Bitte wechseln Sie Ihr Passwort!"))

        # Import der Daten aus der Excel-Datei in das Pandas-Dataframe und Uebertragung in Liste "daten"
        daten = self._import_excel_daten(neuanlage_private_krankenkasse)

        # Daten aus importierter Excel-Tabelle '2 insert Sozialversicherungsdaten/3 private Krankenkasse.xlsx' pruefen
        krankenkasse_voller_name = self._existenz_str_daten_feststellen(daten[0], 'Krankenkasse voller Name', 128, True)
        krankenkasse_abkuerzung = self._existenz_str_daten_feststellen(daten[1], 'Krankenkasse Abkuerzung', 16, False)
        u1_umlage = self._existenz_zahlen_daten_feststellen(daten[2], 99, 'U1-Umlage', True)
        u2_umlage = self._existenz_zahlen_daten_feststellen(daten[3], 99, 'U2-Umlage', True)
        insolvenzgeldumlage = self._existenz_zahlen_daten_feststellen(daten[4], 99, 'Insolvenzgeldumlage', True)
        eintragungsdatum = self._existenz_date_daten_feststellen(daten[5], 'Eintragungsdatum', True)

        export_daten = [self.mandant_id,
                        krankenkasse_voller_name,
                        krankenkasse_abkuerzung,
                        u1_umlage,
                        u2_umlage,
                        insolvenzgeldumlage,
                        'privat',
                        eintragungsdatum]

        self._export_zu_db('insert_private_Krankenkasse(%s,%s,%s,%s,%s,%s,%s,%s)', export_daten)

    def insert_gemeldete_krankenkasse(self, neuanlage_gemeldete_krankenkasse):
        """
        Diese Methode uebertraegt die eingetragene gemeldete Krankenkasse fuer Mitarbeiter, die anderweitig
        krankenversichert sein muessen (z.B. Werkstudenten, unbezahlte Praktikanten etc.) mit deren Umlagen in die
        Datenbank, in dem der Stored Procedure 'insert_gemeldete_Krankenkasse' aufgerufen wird.
        :param neuanlage_gemeldete_krankenkasse: Name der Excel-Datei, dessen Daten in die Datenbank
                                                 eingetragen werden sollen.
        """

        if not self.neues_passwort_geaendert:
            raise(ValueError("Ihr Administrator hat ein neues Passwort vergeben. Bitte wechseln Sie Ihr Passwort!"))

        # Import der Daten aus der Excel-Datei in das Pandas-Dataframe und Uebertragung in Liste "daten"
        daten = self._import_excel_daten(neuanlage_gemeldete_krankenkasse)

        # Daten aus importierter Excel-Tabelle '2 insert Sozialversicherungsdaten/4 gemeldete Krankenkasse.xlsx' pruefen
        krankenkasse_voller_name = self._existenz_str_daten_feststellen(daten[0], 'Krankenkasse voller Name', 128, True)
        krankenkasse_abkuerzung = self._existenz_str_daten_feststellen(daten[1], 'Krankenkasse Abkuerzung', 16, False)
        u1_umlage = self._existenz_zahlen_daten_feststellen(daten[2], 99, 'U1-Umlage', True)
        u2_umlage = self._existenz_zahlen_daten_feststellen(daten[3], 99, 'U2-Umlage', True)
        insolvenzgeldumlage = self._existenz_zahlen_daten_feststellen(daten[4], 99, 'Insolvenzgeldumlage', True)
        eintragungsdatum = self._existenz_date_daten_feststellen(daten[5], 'Eintragungsdatum', True)

        export_daten = [self.mandant_id,
                        krankenkasse_voller_name,
                        krankenkasse_abkuerzung,
                        u1_umlage,
                        u2_umlage,
                        insolvenzgeldumlage,
                        'anders',
                        eintragungsdatum]

        self._export_zu_db('insert_gemeldete_Krankenkasse(%s,%s,%s,%s,%s,%s,%s,%s)', export_daten)

    def insert_anzahl_kinder_an_pv_beitrag(self, neuanlage_anzahl_kinder):
        """
        Diese Methode uebertraegt die Anzahl der Kinder und der daraus resultierende Arbeitnehmerbeitrag zur
        Pflegeversicherung in die Datenbank, in dem der Stored Procedure 'insert_anzahl_kinder_an_pv_beitrag' aufgerufen
        wird.
        :param neuanlage_anzahl_kinder: Name der Excel-Datei, dessen Daten in die Datenbank eingetragen werden sollen.
        """
        if not self.neues_passwort_geaendert:
            raise(ValueError("Ihr Administrator hat ein neues Passwort vergeben. Bitte wechseln Sie Ihr Passwort!"))

        # Import der Daten aus der Excel-Datei in das Pandas-Dataframe und Uebertragung in Liste "daten"
        daten = self._import_excel_daten(neuanlage_anzahl_kinder)

        # Daten aus importierter Excel-Tabelle '2 insert Sozialversicherungsdaten/5 Anzahl Kinder Arbeitnehmer
        # PV-Beitrag.xlsx' pruefen
        anzahl_kinder = self._existenz_zahlen_daten_feststellen(daten[0], 99, 'Anzahl Kinder', True)
        juenger_als_23_oder_vor_1940_geboren = self._existenz_boolean_daten_feststellen(daten[1],
                                                                                        'juenger als 23/'
                                                                                        'vor 1940 geboren',
                                                                                        True)
        an_beitrag_pv_in_prozent = self._existenz_zahlen_daten_feststellen(daten[2], 99, 'AN-Beitrag PV in %', True)
        beitragsbemessungsgrenze_pv = self._existenz_zahlen_daten_feststellen(daten[3],
                                                                              99999999,
                                                                              'Beitragsbemessungsgrenze PV',
                                                                              True)
        jahresarbeitsentgeltgrenze_pv = self._existenz_zahlen_daten_feststellen(daten[4],
                                                                                99999999,
                                                                                'Jahresarbeitsentgeltgrenze PV',
                                                                                True)

        eintragungsdatum = self._existenz_date_daten_feststellen(daten[5], 'Eintragungsdatum', True)

        export_daten = [self.mandant_id,
                        anzahl_kinder,
                        juenger_als_23_oder_vor_1940_geboren,
                        an_beitrag_pv_in_prozent,
                        beitragsbemessungsgrenze_pv,
                        jahresarbeitsentgeltgrenze_pv,
                        eintragungsdatum]

        self._export_zu_db('insert_anzahl_kinder_an_pv_beitrag(%s,%s,%s,%s,%s,%s,%s)', export_daten)

    def insert_arbeitsort_sachsen_ag_pv_beitrag(self, neuanlage_wohnhaft_sachsen):
        """
        Diese Methode uebertraegt den Arbeitgeberbeitrag zur Pflichtversicherung in Abhaengigkeit des Wohnortes in die
        Datenbank, in dem der Stored Procedure 'insert_arbeitsort_sachsen_ag_pv_beitrag' aufgerufen wird.
        :param neuanlage_wohnhaft_sachsen: Name der Excel-Datei, dessen Daten in die Datenbank
                                           eingetragen werden sollen.
        """
        if not self.neues_passwort_geaendert:
            raise(ValueError("Ihr Administrator hat ein neues Passwort vergeben. Bitte wechseln Sie Ihr Passwort!"))

        # Import der Daten aus der Excel-Datei in das Pandas-Dataframe und Uebertragung in Liste "daten"
        daten = self._import_excel_daten(neuanlage_wohnhaft_sachsen)

        # Daten aus importierter Excel-Tabelle '2 insert Sozialversicherungsdaten/6 Arbeitsort Sachsen Arbeitgeber
        # PV-Beitrag.xlsx' pruefen
        wohnhaft_sachsen = self._existenz_boolean_daten_feststellen(daten[0], 'wohnhaft_Sachsen', True)
        ag_beitrag_pv_in_prozent = self._existenz_zahlen_daten_feststellen(daten[1], 99, 'AG-Beitrag PV in %', True)
        eintragungsdatum = self._existenz_date_daten_feststellen(daten[2], 'Eintragungsdatum', True)

        export_daten = [self.mandant_id, wohnhaft_sachsen, ag_beitrag_pv_in_prozent, eintragungsdatum]
        self._export_zu_db('insert_arbeitsort_sachsen_ag_pv_beitrag(%s,%s,%s,%s)', export_daten)

    def insert_arbeitslosenversicherungsbeitraege(self, neuanlage_arbeitslosenversicherungsbeitraege):
        """
        Diese Methode uebertraegt die Arbeitslosenversicheurngsbeitragssaetze von Arbeitnehmer und Arbeitgeber sowie die
        Beitragsbemessungsgrenzen in die Datenbank, in dem der Stored Procedure
        'insert_arbeitslosenversicherungsbeitraege' aufgerufen wird.
        :param neuanlage_arbeitslosenversicherungsbeitraege: Name der Excel-Datei, dessen Daten in die Datenbank
                                                             eingetragen werden sollen.
        """
        if not self.neues_passwort_geaendert:
            raise(ValueError("Ihr Administrator hat ein neues Passwort vergeben. Bitte wechseln Sie Ihr Passwort!"))

        # Import der Daten aus der Excel-Datei in das Pandas-Dataframe und Uebertragung in Liste "daten"
        daten = self._import_excel_daten(neuanlage_arbeitslosenversicherungsbeitraege)

        # Daten aus importierter Excel-Tabelle '2 insert Sozialversicherungsdaten/
        # 7 Arbeitslosenversicherungsbeitraege.xlsx' pruefen
        an_beitrag_av_in_prozent = self._existenz_zahlen_daten_feststellen(daten[0], 99, 'AN-Beitrag AV in %', True)
        ag_beitrag_av_in_prozent = self._existenz_zahlen_daten_feststellen(daten[1], 99, 'AG-Beitrag AV in %', True)
        beitragsbemessungsgrenze_av_ost = self._existenz_zahlen_daten_feststellen(daten[2],
                                                                                  99999999,
                                                                                  'Beitragsbemessungsgrenze AV Ost',
                                                                                  True)
        beitragsbemessungsgrenze_av_west = self._existenz_zahlen_daten_feststellen(daten[3],
                                                                                   99999999,
                                                                                   'Beitragsbemessungsgrenze AV West',
                                                                                   True)
        eintragungsdatum = self._existenz_date_daten_feststellen(daten[4], 'Eintragungsdatum', True)

        export_daten = [self.mandant_id,
                        an_beitrag_av_in_prozent,
                        ag_beitrag_av_in_prozent,
                        beitragsbemessungsgrenze_av_ost,
                        beitragsbemessungsgrenze_av_west,
                        eintragungsdatum]
        self._export_zu_db('insert_arbeitslosenversicherungsbeitraege(%s,%s,%s,%s,%s,%s)', export_daten)

    def insert_rentenversicherungsbeitraege(self, neuanlage_rentenversicherungsbeitraege):
        """
        Diese Methode uebertraegt die Rentenversicherungsbeitragssaetze von Arbeitnehmer und Arbeitgeber sowie die
        Beitragsbemessungsgrenzen in die Datenbank, in dem der Stored Procedure
        'insert_arbeitslosenversicherungsbeitraege' aufgerufen wird.
        :param neuanlage_rentenversicherungsbeitraege: Name der Excel-Datei, dessen Daten in die Datenbank
                                                       eingetragen werden sollen.
        """
        if not self.neues_passwort_geaendert:
            raise(ValueError("Ihr Administrator hat ein neues Passwort vergeben. Bitte wechseln Sie Ihr Passwort!"))

        # Import der Daten aus der Excel-Datei in das Pandas-Dataframe und Uebertragung in Liste "daten"
        daten = self._import_excel_daten(neuanlage_rentenversicherungsbeitraege)

        # Daten aus importierter Excel-Tabelle '2 insert Sozialversicherungsdaten/8 Rentenversicherungsbeitraege.xlsx'
        # pruefen
        an_beitrag_rv_in_prozent = self._existenz_zahlen_daten_feststellen(daten[0], 99, 'AN-Beitrag RV in %', True)
        ag_beitrag_rv_in_prozent = self._existenz_zahlen_daten_feststellen(daten[1], 99, 'AG-Beitrag RV in %', True)
        beitragsbemessungsgrenze_rv_ost = self._existenz_zahlen_daten_feststellen(daten[2],
                                                                                  99999999,
                                                                                  'Beitragsbemessungsgrenze RV Ost',
                                                                                  True)
        beitragsbemessungsgrenze_rv_west = self._existenz_zahlen_daten_feststellen(daten[3],
                                                                                   99999999,
                                                                                   'Beitragsbemessungsgrenze RV West',
                                                                                   True)
        eintragungsdatum = self._existenz_date_daten_feststellen(daten[4], 'Eintragungsdatum', True)

        export_daten = [self.mandant_id,
                        an_beitrag_rv_in_prozent,
                        ag_beitrag_rv_in_prozent,
                        beitragsbemessungsgrenze_rv_ost,
                        beitragsbemessungsgrenze_rv_west,
                        eintragungsdatum]
        self._export_zu_db('insert_rentenversicherungsbeitraege(%s,%s,%s,%s,%s,%s)', export_daten)

    def insert_minijobbeitraege(self, neuanlage_minijobbeitraege):
        """
        Diese Methode uebertraegt Minijobbeitragssaetze von Arbeitnehmer und Arbeitgeber sowie die Umlagen und
        Pauschalsteuer in die Datenbank, in dem der Stored Procedure 'insert_minijobbeitraege' aufgerufen wird.
        :param neuanlage_minijobbeitraege: Name der Excel-Datei, dessen Daten in die Datenbank
                                           eingetragen werden sollen.
        """
        if not self.neues_passwort_geaendert:
            raise(ValueError("Ihr Administrator hat ein neues Passwort vergeben. Bitte wechseln Sie Ihr Passwort!"))

        # Import der Daten aus der Excel-Datei in das Pandas-Dataframe und Uebertragung in Liste "daten"
        daten = self._import_excel_daten(neuanlage_minijobbeitraege)

        # Daten aus importierter Excel-Tabelle '2 insert Sozialversicherungsdaten/9 Minijobbeitraege.xlsx' pruefen
        kurzfristig_beschaeftigt = self._existenz_boolean_daten_feststellen(daten[0],
                                                                            'kurzfristige Minijobtaetigkeit?',
                                                                            True)
        an_beitrag_rentenpauschale = self._existenz_boolean_daten_feststellen(daten[1],
                                                                            'Zahlt Arbeitnehmer Rentenpauschale?',
                                                                            True)
        ag_beitrag_kv_in_prozent = self._existenz_zahlen_daten_feststellen(daten[2],
                                                                           99,
                                                                           'AG-Beitrag KV Minijob in %',
                                                                           True)
        ag_beitrag_rv_in_prozent = self._existenz_zahlen_daten_feststellen(daten[3],
                                                                           99,
                                                                           'AG-Beitrag RV Minijob in %',
                                                                           True)

        # Wenn der Minijobber sich von der AN-Rentenpauschale befreien laesst, wird die Variable auf 0 gesetzt
        if an_beitrag_rentenpauschale:
            an_beitrag_rv_in_prozent = self._existenz_zahlen_daten_feststellen(daten[4],
                                                                               99,
                                                                               'AN-Beitrag RV Minijob in %',
                                                                               True)
        else:
            an_beitrag_rv_in_prozent = 0

        u1_umlage = self._existenz_zahlen_daten_feststellen(daten[5], 99, 'U1-Umlage Minijob in %', True)
        u2_umlage = self._existenz_zahlen_daten_feststellen(daten[6], 99, 'U2-Umlage Minijob in %', True)
        insolvenzgeldumlage = self._existenz_zahlen_daten_feststellen(daten[7],
                                                                      99,
                                                                      'Insolvenzgeldumlage Minijob in %',
                                                                      True)
        pauschalsteuer = self._existenz_zahlen_daten_feststellen(daten[8],
                                                                 99,
                                                                 'Pauschalsteuer Minijob in %',
                                                                 True)
        eintragungsdatum = self._existenz_date_daten_feststellen(daten[9], 'Eintragungsdatum', True)

        # Da kurzfristig beschaeftigte Minijobber rechtlich keine AN-Rentenpauschale zahlen koennen, muss sichergestellt
        # sein, dass eine fehlerhafte Eingabe abgefangen wird
        if kurzfristig_beschaeftigt and an_beitrag_rentenpauschale:
            raise (ValueError("Ein kurzfristig beschaeftiger Minijobber zahlt keine AN-Rentenpauschale!"))

        export_daten = [self.mandant_id,
                        kurzfristig_beschaeftigt,
                        an_beitrag_rentenpauschale,
                        ag_beitrag_kv_in_prozent,
                        ag_beitrag_rv_in_prozent,
                        an_beitrag_rv_in_prozent,
                        u1_umlage,
                        u2_umlage,
                        insolvenzgeldumlage,
                        pauschalsteuer,
                        eintragungsdatum]
        self._export_zu_db('insert_minijobbeitraege(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)', export_daten)

    def insert_berufsgenossenschaft(self, neuanlage_berufsgenossenschaft):
        """
        Diese Methode uebertraegt eine Berufsgenossenschaft in die Datenbank, in dem die Stored Procedure
        'insert_berufsgenossenschaft' aufgerufen wird.
        :param neuanlage_berufsgenossenschaft: Name der Excel-Datei, dessen Daten in die Datenbank eingetragen werden
        sollen.
        """
        if not self.neues_passwort_geaendert:
            raise(ValueError("Ihr Administrator hat ein neues Passwort vergeben. Bitte wechseln Sie Ihr Passwort!"))
        # Import der Daten aus der Excel-Datei in das Pandas-Dataframe und Uebertragung in Liste "daten"
        daten = self._import_excel_daten(neuanlage_berufsgenossenschaft)

        # Daten aus importierter Excel-Tabelle '2 insert Sozialversicherungsdaten/10 Berufsgenossenschaft.xlsx' pruefen
        berufsgenossenschaft = self._existenz_str_daten_feststellen(daten[0], 'Berufsgenossenschaft', 128, True)
        abkuerzung = self._existenz_str_daten_feststellen(daten[1], 'Berufsgenossenschaftskuerzel', 16, False)

        export_daten = [self.mandant_id, berufsgenossenschaft, abkuerzung]
        self._export_zu_db('insert_berufsgenossenschaft(%s,%s,%s)', export_daten)

    def insert_unfallversicherungsbeitrag(self, neuanlage_unfallversicherungsbeitrag):
        """
        Diese Methode verknuepft eine Berufsgenossenschaft mit einem Unternehmen und traegt den Jahresbeitrag der
        Gesellschaft in die Datenbank ein, in dem die Stored Procedure 'insert_unfallversicherungsbeitrag' aufgerufen
        wird.
        :param neuanlage_unfallversicherungsbeitrag: Name der Excel-Datei, dessen Daten in die Datenbank eingetragen
                                                     werden sollen.
        """
        if not self.neues_passwort_geaendert:
            raise(ValueError("Ihr Administrator hat ein neues Passwort vergeben. Bitte wechseln Sie Ihr Passwort!"))

        # Import der Daten aus der Excel-Datei in das Pandas-Dataframe und Uebertragung in Liste "daten"
        daten = self._import_excel_daten(neuanlage_unfallversicherungsbeitrag)

        # Daten aus importierter Excel-Tabelle '2 insert Sozialversicherungsdaten/11 Unfallversicherungsbeitrag.xlsx'
        # pruefen
        unternehmen = self._existenz_str_daten_feststellen(daten[0], 'Unternehmen', 128, True)
        unternehmenskuerzel = self._existenz_str_daten_feststellen(daten[1], 'Unternehmenskuerzel', 16, False)
        berufsgenossenschaft = self._existenz_str_daten_feststellen(daten[2], 'Berufsgenossenschaft', 128, True)
        berufsgenossenschaftskuerzel = self._existenz_str_daten_feststellen(daten[3],
                                                                            'Berufsgenossenschaftskuerzel',
                                                                            16,
                                                                            False)
        jahresbeitrag_unfallversicherung = self._existenz_zahlen_daten_feststellen(daten[4], 9999999999, 'Betrag', True)
        beitragsjahr_uv = self._existenz_zahlen_daten_feststellen(daten[5],
                                                                  9999,
                                                                  'Beitragsjahr Unfallversicherung',
                                                                  True)

        export_daten = [self.mandant_id,
                        unternehmen,
                        unternehmenskuerzel,
                        berufsgenossenschaft,
                        berufsgenossenschaftskuerzel,
                        jahresbeitrag_unfallversicherung,
                        beitragsjahr_uv]
        self._export_zu_db('insert_unfallversicherungsbeitrag(%s,%s,%s,%s,%s,%s,%s)', export_daten)

    def insert_gewerkschaft(self, neuanlage_gewerkschaft):
        """
        Diese Methode uebertraegt den Namen der Gewerkschaft in die Datenbank, in dem der Stored Procedure
        'insert_gewerkschaft' aufgerufen wird.
        :param neuanlage_gewerkschaft: Name der Excel-Datei, dessen Daten in die Datenbank
        """
        if not self.neues_passwort_geaendert:
            raise(ValueError("Ihr Administrator hat ein neues Passwort vergeben. Bitte wechseln Sie Ihr Passwort!"))

        # Import der Daten aus der Excel-Datei in das Pandas-Dataframe und Uebertragung in Liste "daten"
        daten = self._import_excel_daten(neuanlage_gewerkschaft)

        # Daten aus importierter Excel-Tabelle '3 insert Entgeltdaten/1 Gewerkschaft.xlsx' pruefen
        gewerkschaft = self._existenz_str_daten_feststellen(daten[0], 'Gewerkschaft', 64, True)

        export_daten = [self.mandant_id, gewerkschaft]
        self._export_zu_db('insert_gewerkschaft(%s,%s)', export_daten)

    def insert_tarif(self, neuanlage_tarif):
        """
        Diese Methode uebertraegt den Namen eines Tarifs und verknuepft diese mit der Gewerkschaft, die fuer diese
        zustaendig ist, in die Datenbank, in dem der Stored Procedure 'insert_tarif' aufgerufen wird.
        :param neuanlage_tarif: Name der Excel-Datei, dessen Daten in die Datenbank eingetragen werden sollen.
        """
        if not self.neues_passwort_geaendert:
            raise(ValueError("Ihr Administrator hat ein neues Passwort vergeben. Bitte wechseln Sie Ihr Passwort!"))

        # Import der Daten aus der Excel-Datei in das Pandas-Dataframe und Uebertragung in Liste "daten"
        daten = self._import_excel_daten(neuanlage_tarif)

        # Daten aus importierter Excel-Tabelle '3 insert Entgeltdaten/2 Tarif.xlsx' pruefen
        tarifbezeichnung = self._existenz_str_daten_feststellen(daten[0], 'Tarifbezeichnung', 16, True)
        gewerkschaft = self._existenz_str_daten_feststellen(daten[1], 'Gewerkschaft', 64, True)

        export_daten = [self.mandant_id, tarifbezeichnung, gewerkschaft]
        self._export_zu_db('insert_tarif(%s,%s,%s)', export_daten)

    def insert_verguetungsbestandteil(self, neuanalage_verguetungsbestandteil):
        """
        Methode schreibt ein neues Verguetungsbestandteil und dessen Auszahlungsmonat in die Datenbank ein.
        :param neuanalage_verguetungsbestandteil: Name der Excel-Datei, dessen Daten in die Datenbank
                                                  eingetragen werden sollen.
        """
        if not self.neues_passwort_geaendert:
            raise(ValueError("Ihr Administrator hat ein neues Passwort vergeben. Bitte wechseln Sie Ihr Passwort!"))

        # Import der Daten aus der Excel-Datei in das Pandas-Dataframe und Uebertragung in Liste "daten"
        daten = self._import_excel_daten(neuanalage_verguetungsbestandteil)

        # Daten aus importierter Excel-Tabelle '3 insert Entgeltdaten/3 Verguetungsbestandteil.xlsx' pruefen
        verguetungsbestandteil = self._existenz_str_daten_feststellen(daten[0], 'Verguetungsbestandteil', 64, True)
        auszahlungsmonat = self._existenz_str_daten_feststellen(daten[1], 'Auszahlungsmonat', 16, True)

        export_daten = [self.mandant_id, verguetungsbestandteil, auszahlungsmonat]
        self._export_zu_db('insert_verguetungsbestandteil(%s,%s,%s)', export_daten)

    def insert_tarifliches_verguetungsbestandteil(self, neuanlage_tarifliches_verguetungsbestandteil):
        """
        Diese Methode uebertraegt einen Verguetungsbestandteil wie bspw. Grundgehalt, Urlaubsgeld etc. und verknuepft
        sie mit dem entsprechenden Tarif, in die Datenbank, in dem die Stored Procedure
        'insert_tarifliches_verguetungsbestandteil' aufgerufen wird.
        :param neuanlage_tarifliches_verguetungsbestandteil: Name der Excel-Datei, dessen Daten in die Datenbank
                                                             eingetragen werden sollen.
        """
        if not self.neues_passwort_geaendert:
            raise(ValueError("Ihr Administrator hat ein neues Passwort vergeben. Bitte wechseln Sie Ihr Passwort!"))

        # Import der Daten aus der Excel-Datei in das Pandas-Dataframe und Uebertragung in Liste "daten"
        daten = self._import_excel_daten(neuanlage_tarifliches_verguetungsbestandteil)

        # Daten aus importierter Excel-Tabelle '3 insert Entgeltdaten/4 tariflicher Verguetungsbestandteil.xlsx' pruefen
        verguetungsbestandteil = self._existenz_str_daten_feststellen(daten[0], 'Verguetungsbestandteil', 64, True)
        tarifbezeichnung = self._existenz_str_daten_feststellen(daten[1], 'Tarifbezeichnung', 16, True)
        betrag = self._existenz_zahlen_daten_feststellen(daten[2], 99999999, 'Betrag', True)
        gueltig_ab = self._existenz_date_daten_feststellen(daten[3], 'Tarifentgelt gueltig ab', True)

        export_daten = [self.mandant_id, verguetungsbestandteil, tarifbezeichnung, betrag, gueltig_ab]
        self._export_zu_db('insert_tarifliches_verguetungsbestandteil(%s,%s,%s,%s,%s)', export_daten)

    def insert_geschlecht(self, neuanlage_geschlecht):
        """
        Diese Methode uebertraegt ein Geschlecht in die Datenbank, in dem die Stored Procedure 'insert_geschlecht'
        aufgerufen wird.
        :param neuanlage_geschlecht: Name der Excel-Datei, dessen Daten in die Datenbank eingetragen werden sollen.
        """
        if not self.neues_passwort_geaendert:
            raise(ValueError("Ihr Administrator hat ein neues Passwort vergeben. Bitte wechseln Sie Ihr Passwort!"))

        # Import der Daten aus der Excel-Datei in das Pandas-Dataframe und Uebertragung in Liste "daten"
        daten = self._import_excel_daten(neuanlage_geschlecht)

        # Daten aus importierter Excel-Tabelle '1 insert personenbezogene Daten/1 Geschlecht.xlsx' pruefen
        geschlecht = self._existenz_str_daten_feststellen(daten[0], 'Geschlecht', 32, True)

        export_daten = [self.mandant_id, geschlecht]
        self._export_zu_db('insert_geschlecht(%s,%s)', export_daten)

    def insert_mitarbeitertyp(self, neuanlage_mitarbeitertyp):
        """
        Diese Methode uebertraegt ein Mitarbeitertyp wie bspw. 'Angestellter' oder 'Praktikant' in die Datenbank, in
        dem die Stored Procedure 'insert_mitarbeitertyp' aufgerufen wird.
        :param neuanlage_mitarbeitertyp: Name der Excel-Datei, dessen Daten in die Datenbank eingetragen werden sollen.
        """
        # Import der Daten aus der Excel-Datei in das Pandas-Dataframe und Uebertragung in Liste "daten"
        daten = self._import_excel_daten(neuanlage_mitarbeitertyp)

        # Daten aus importierter Excel-Tabelle '1 insert personenbezogene Daten/2 Mitarbeitertyp.xlsx' pruefen
        mitarbeitertyp = self._existenz_str_daten_feststellen(daten[0], 'Geschlecht', 32, True)

        export_daten = [self.mandant_id, mitarbeitertyp]
        self._export_zu_db('insert_mitarbeitertyp(%s,%s)', export_daten)

    def insert_steuerklasse(self, neuanlage_steuerklasse):
        """
        Diese Methode uebertraegt Steuerklasse in die Datenbank, in dem die Stored Procedure 'insert_steuerklasse'
        aufgerufen wird.
        :param neuanlage_steuerklasse: Name der Excel-Datei, dessen Daten in die Datenbank eingetragen werden sollen.
        """
        if not self.neues_passwort_geaendert:
            raise(ValueError("Ihr Administrator hat ein neues Passwort vergeben. Bitte wechseln Sie Ihr Passwort!"))

        # Import der Daten aus der Excel-Datei in das Pandas-Dataframe und Uebertragung in Liste "daten"
        daten = self._import_excel_daten(neuanlage_steuerklasse)

        # Daten aus importierter Excel-Tabelle '1 insert personenbezogene Daten/3 Steuerklasse.xlsx' pruefen
        steuerklasse = self._existenz_str_daten_feststellen(daten[0], 'Steuerklasse', 1, True)

        export_daten = [self.mandant_id, steuerklasse]
        self._export_zu_db('insert_steuerklasse(%s,%s)', export_daten)

    def insert_abteilung(self, neuanlage_abteilung):
        """
        Diese Methode uebertraegt eine Abteilung und deren Abkuerzung in die Datenbank , in dem die Stored Procedure
        'insert_abteilung' aufgerufen wird.
        :param neuanlage_abteilung: Name der Excel-Datei, dessen Daten in die Datenbank eingetragen werden sollen.
        """
        if not self.neues_passwort_geaendert:
            raise(ValueError("Ihr Administrator hat ein neues Passwort vergeben. Bitte wechseln Sie Ihr Passwort!"))

        # Import der Daten aus der Excel-Datei in das Pandas-Dataframe und Uebertragung in Liste "daten"
        daten = self._import_excel_daten(neuanlage_abteilung)

        # Daten aus importierter Excel-Tabelle '1 insert personenbezogene Daten/4 Abteilung.xlsx' pruefen
        abteilung = self._existenz_str_daten_feststellen(daten[0], 'Abteilung', 64, True)
        abkuerzung = self._existenz_str_daten_feststellen(daten[1], 'Abteilungskuerzel', 16, False)

        export_daten = [self.mandant_id, abteilung, abkuerzung]
        self._export_zu_db('insert_abteilung(%s,%s,%s)', export_daten)

    def insert_jobtitel(self, neuanlage_jobtitel):
        """
        Diese Methode uebertraegt einen Jobtitel, in dem die Stored Procedure 'insert_jobtitel' aufgerufen wird.
        :param neuanlage_jobtitel: Name der Excel-Datei, dessen Daten in die Datenbank eingetragen werden sollen.
        """
        if not self.neues_passwort_geaendert:
            raise(ValueError("Ihr Administrator hat ein neues Passwort vergeben. Bitte wechseln Sie Ihr Passwort!"))

        # Import der Daten aus der Excel-Datei in das Pandas-Dataframe und Uebertragung in Liste "daten"
        daten = self._import_excel_daten(neuanlage_jobtitel)

        # Daten aus importierter Excel-Tabelle '1 insert personenbezogene Daten/5 Jobtitel.xlsx' pruefen
        jobtitel = self._existenz_str_daten_feststellen(daten[0], 'Jobtitel', 32, True)

        export_daten = [self.mandant_id, jobtitel]
        self._export_zu_db('insert_jobtitel(%s,%s)', export_daten)

    def insert_erfahrungsstufe(self, neuanlage_erfahrungsstufe):
        """
        Diese Methode uebertraegt eine Erfahrungsstufe wie bspw. 'Junior', 'Senior' etc., in dem die Stored Procedure
        'insert_erfahrungsstufe' aufgerufen wird.
        :param neuanlage_erfahrungsstufe: Name der Excel-Datei, dessen Daten in die Datenbank eingetragen werden sollen.
        """
        if not self.neues_passwort_geaendert:
            raise(ValueError("Ihr Administrator hat ein neues Passwort vergeben. Bitte wechseln Sie Ihr Passwort!"))

        # Import der Daten aus der Excel-Datei in das Pandas-Dataframe und Uebertragung in Liste "daten"
        daten = self._import_excel_daten(neuanlage_erfahrungsstufe)

        # Daten aus importierter Excel-Tabelle '1 insert personenbezogene Daten/6 Erfahrungsstufe.xlsx' pruefen
        erfahrungsstufe = self._existenz_str_daten_feststellen(daten[0], 'Erfahrungsstufe', 32, True)

        export_daten = [self.mandant_id, erfahrungsstufe]
        self._export_zu_db('insert_erfahrungsstufe(%s,%s)', export_daten)

    def insert_unternehmen(self, neuanlage_unternehmen):
        """
        Diese Methode uebertraegt ein Unternehmen und evtl. deren Abkuerzung in die Datenbank, in dem die Stored
        Procedure 'insert_unternehmen' aufgerufen wird.
        :param neuanlage_unternehmen: Name der Excel-Datei, dessen Daten in die Datenbank eingetragen werden sollen.
        """
        if not self.neues_passwort_geaendert:
            raise(ValueError("Ihr Administrator hat ein neues Passwort vergeben. Bitte wechseln Sie Ihr Passwort!"))

        # Import der Daten aus der Excel-Datei in das Pandas-Dataframe und Uebertragung in Liste "daten"
        daten = self._import_excel_daten(neuanlage_unternehmen)

        # Daten aus importierter Excel-Tabelle '1 insert personenbezogene Daten/7 Gesellschaft.xlsx' pruefen
        unternehmen = self._existenz_str_daten_feststellen(daten[0], 'Unternehmen', 128, True)
        abkuerzung = self._existenz_str_daten_feststellen(daten[1], 'Gesellschaftskuerzel', 16, False)

        export_daten = [self.mandant_id, unternehmen, abkuerzung]
        self._export_zu_db('insert_unternehmen(%s,%s,%s)', export_daten)

    def insert_austrittsgrundkategorie(self, neuanlage_austrittsgrundkategorie):
        """
        Diese Methode uebertraegt eine Austrittsgrundkategorie wie bspw. 'betriebsbedingt' in die Datenbank, in dem die
        Stored Procedure 'insert_austrittsgrundkategorie' aufgerufen wird.
        :param neuanlage_austrittsgrundkategorie: Name der Excel-Datei, dessen Daten in die Datenbank eingetragen werden
                                                  sollen.
        """
        if not self.neues_passwort_geaendert:
            raise(ValueError("Ihr Administrator hat ein neues Passwort vergeben. Bitte wechseln Sie Ihr Passwort!"))

        # Import der Daten aus der Excel-Datei in das Pandas-Dataframe und Uebertragung in Liste "daten"
        daten = self._import_excel_daten(neuanlage_austrittsgrundkategorie)

        # Daten aus importierter Excel-Tabelle '1 insert personenbezogene Daten/8 Austrittsgrundkategorie.xlsx' pruefen
        austrittsgrundkategorie = self._existenz_str_daten_feststellen(daten[0], 'Austrittsgrundkategorie', 16, True)

        export_daten = [self.mandant_id, austrittsgrundkategorie]
        self._export_zu_db('insert_austrittsgrundkategorie(%s,%s)', export_daten)

    def insert_austrittsgrund(self, neuanlage_austrittsgrund):
        """
        Diese Methode uebertraegt eine Austrittsgrund wie bspw. 'Umsatzrueckgang' in die Datenbank, in dem die Stored
        Procedure 'insert_austrittsgruende' aufgerufen wird.
        :param neuanlage_austrittsgrund: Name der Excel-Datei, dessen Daten in die Datenbank eingetragen werden sollen.
        """
        if not self.neues_passwort_geaendert:
            raise(ValueError("Ihr Administrator hat ein neues Passwort vergeben. Bitte wechseln Sie Ihr Passwort!"))

        # Import der Daten aus der Excel-Datei in das Pandas-Dataframe und Uebertragung in Liste "daten"
        daten = self._import_excel_daten(neuanlage_austrittsgrund)

        # Daten aus importierter Excel-Tabelle '1 insert personenbezogene Daten/9 Austrittsgrund.xlsx' pruefen
        austrittsgrund = self._existenz_str_daten_feststellen(daten[0], 'Austrittsgrund', 16, True)
        austrittsgrundkategorie = self._existenz_str_daten_feststellen(daten[1], 'Austrittsgrundkategorie', 16, True)

        export_daten = [self.mandant_id, austrittsgrund, austrittsgrundkategorie]
        self._export_zu_db('insert_austrittsgrund(%s,%s,%s)', export_daten)

    def insert_neuer_mitarbeiter(self, mitarbeiterdaten):
        """
        Diese Methode uebertraegt die eingetragenen Mitarbeiterdaten in die Datenbank, in dem der Stored Procedure
        'insert_neuer_mitarbeiter' aufgerufen wird.
        :param mitarbeiterdaten: Name der Excel-Datei, dessen Mitarbeiterdaten in die Datenbank
                                 eingetragen werden sollen.
        """
        if not self.neues_passwort_geaendert:
            raise (ValueError("Ihr Administrator hat ein neues Passwort vergeben. Bitte wechseln Sie Ihr Passwort!"))

            # Import der Daten aus der Excel-Datei in das Pandas-Dataframe und Uebertragung in Liste "daten"
        daten = self._import_excel_daten(mitarbeiterdaten)

        # Daten aus importierter Excel-Tabelle '4 neuen Mitarbeiter anlegen/1 Mitarbeiter.xlsx' pruefen
        personalnummer = self._existenz_str_daten_feststellen(daten[0], 'Personalnummer', 32, True)
        vorname = self._existenz_str_daten_feststellen(daten[1], 'Vorname', 64, True)
        zweitname = self._existenz_str_daten_feststellen(daten[2], 'Zweitname', 128, False)
        nachname = self._existenz_str_daten_feststellen(daten[3], 'Nachname', 64, True)
        geburtsdatum = self._existenz_date_daten_feststellen(daten[4], 'Geburtsdatum', True)
        eintrittsdatum = self._existenz_date_daten_feststellen(daten[5], 'Eintrittsdatum', True)
        steuernummer = self._existenz_str_daten_feststellen(daten[6], 'Steuernummer', 32, False)
        sozialversicherungsnummer = self._existenz_str_daten_feststellen(daten[7], 'Sozialversicherungsnummer', 32,
                                                                         False)
        iban = self._existenz_str_daten_feststellen(daten[8], 'IBAN', 32, False)
        private_telefonnummer = self._existenz_str_daten_feststellen(daten[9], 'private Telefonnummer', 16, True)
        private_email = self._existenz_str_daten_feststellen(daten[10], 'private E-Mail', 64, True)
        dienstliche_telefonnummer = self._existenz_str_daten_feststellen(daten[11], 'dienstliche Telefonnummer', 16,
                                                                         False)
        dienstliche_email = self._existenz_str_daten_feststellen(daten[12], 'dienstliche E-Mail', 64, False)
        befristet_bis = self._existenz_date_daten_feststellen(daten[13], 'Befristet Bis', False)

        strasse = self._existenz_str_daten_feststellen(daten[14], 'Strasse', 64, True)
        hausnummer = self._existenz_str_daten_feststellen(daten[15], 'Hausnummer', 8, True)
        postleitzahl = self._existenz_str_daten_feststellen(daten[16], 'Postleitzahl', 16, True)
        ost_west_ausland = self._existenz_str_daten_feststellen(daten[17], 'Postleitzahl', 8, True)
        stadt = self._existenz_str_daten_feststellen(daten[18], 'Stadt', 128, True)
        region = self._existenz_str_daten_feststellen(daten[19], 'Region', 128, True)
        land = self._existenz_str_daten_feststellen(daten[20], 'Land', 128, True)

        geschlecht = self._existenz_str_daten_feststellen(daten[21], 'Geschlecht', 32, True)

        mitarbeitertyp = self._existenz_str_daten_feststellen(daten[22], 'Mitarbeitertyp', 32, True)

        steuerklasse = self._existenz_str_daten_feststellen(daten[23], 'Steuerklasse', 1, False)

        wochenarbeitsstunden = self._existenz_zahlen_daten_feststellen(daten[24],
                                                                       48,
                                                                       'Wochenarbeitsstunden',
                                                                       True)

        abteilung = self._existenz_str_daten_feststellen(daten[25], 'Abteilung', 64, True)
        abteilungskuerzel = self._existenz_str_daten_feststellen(daten[26], 'Abteilungskuerzel', 16, True)

        fuehrungskraft = self._existenz_boolean_daten_feststellen(daten[27], 'Fuehrungskraft', True)
        jobtitel = self._existenz_str_daten_feststellen(daten[28], 'Jobtitel', 32, True)
        erfahrungsstufe = self._existenz_str_daten_feststellen(daten[29], 'Erfahrungsstufe', 32, True)

        unternehmen = self._existenz_str_daten_feststellen(daten[30], 'Unternehmen', 128, True)

        tarifbeschaeftigt = self._existenz_boolean_daten_feststellen(daten[31], 'tarifbeschaeftigt', True)

        # Wenn angegeben wird, dass neuer Mitarbeiter tarifbeschaeftigt ist, muss der Tarif angegeben werden
        if tarifbeschaeftigt:
            tarif = self._existenz_str_daten_feststellen(daten[32], 'Tarif', 16, True)
        else:
            tarif = None

        kurzfristig_beschaeftigt = self._existenz_boolean_daten_feststellen(daten[33], 'Kurzfristig_beschaeftigt?',
                                                                            False)

        bezeichnung_krankenkasse = self._existenz_str_daten_feststellen(daten[34], 'Bezeichnung Krankenkasse', 128,
                                                                        False)

        abkuerzung_krankenkasse = self._existenz_str_daten_feststellen(daten[35], 'Abkuerzung Krankenkasse', 16, False)

        gesetzlich_krankenversichert = self._existenz_boolean_daten_feststellen(daten[36],
                                                                                'gesetzlich Krankenversichert?',
                                                                                False)

        # Wenn angegeben ist, dass neuer Mitarbeiter gesetzlich krankenversichert ist, muessen folgende Daten vorhanden
        # sein
        if gesetzlich_krankenversichert:
            ermaessigter_gkv_beitragssatz = self._existenz_boolean_daten_feststellen(daten[37],
                                                                                     'ermaessigter GKV-Beitragssatz?',
                                                                                     True)

            anzahl_kinder = self._existenz_zahlen_daten_feststellen(daten[38], 99, 'Anzahl Kinder', True)

            juenger_als_23_oder_vor_1940_geboren = self._existenz_boolean_daten_feststellen(daten[39],
                                                                                            'juenger als 23/'
                                                                                            'vor 1940 geboren',
                                                                                            True)

            wohnhaft_sachsen = self._existenz_boolean_daten_feststellen(daten[40], 'AG-Standort Sachsen', True)
        else:
            ermaessigter_gkv_beitragssatz = None
            anzahl_kinder = None
            juenger_als_23_oder_vor_1940_geboren = None
            wohnhaft_sachsen = None

        privat_krankenversichert = self._existenz_boolean_daten_feststellen(daten[41],
                                                                            'privat Krankenversichert?',
                                                                            False)

        # Wenn angegeben ist, dass neuer Mitarbeiter privat krankenversichert ist, muessen folgende Daten vorhanden
        # sein
        if privat_krankenversichert:
            ag_zuschuss_private_krankenversicherung = self._existenz_zahlen_daten_feststellen(daten[42],
                                                                                              99999999,
                                                                                              'AG-Zuschuss PKV',
                                                                                              True)

            ag_zuschuss_private_pflegeversicherung = self._existenz_zahlen_daten_feststellen(daten[43],
                                                                                             99999999,
                                                                                             'AG-Zuschuss PPV',
                                                                                             True)
        else:
            ag_zuschuss_private_krankenversicherung = None
            ag_zuschuss_private_pflegeversicherung = None

        minijob = self._existenz_boolean_daten_feststellen(daten[44], 'Minijob?', False)

        # Wenn Mitarbeiter ein Minijobber ist, muss angegeben sein, ob er Rentenpauschale zahlt
        if minijob:
            minijob_an_rentenpauschale = self._existenz_boolean_daten_feststellen(daten[45],
                                                                                  'Minijob-AN-Rentenpauschale?',
                                                                                  True)
        else:
            minijob_an_rentenpauschale = None

        anderweitig_versichert = self._existenz_boolean_daten_feststellen(daten[46], 'anderweitig_versichert?', False)
        arbeitslosenversichert = self._existenz_boolean_daten_feststellen(daten[47], 'arbeitslosenversichert?', False)
        rentenversichert = self._existenz_boolean_daten_feststellen(daten[48], 'rentenversichert?', False)

        # Ein Mitarbeiter darf nur entweder gesetzlich krankenversichert ODER privat versichert mit Anspruch auf
        # Arbeitgeberzuschuss ODER Minijobber ODER anderweitig versichert (z.B. kufzfristig Beschaeftigte, Werkstudenten
        # etc.) sein. Es darf also nur genau eines der vier boolean-Variablen 'True' sein
        true_zaehler = 0

        # Anzahl der 'True'-Werte zaehlen
        for i in [gesetzlich_krankenversichert, privat_krankenversichert, minijob, anderweitig_versichert]:
            if i:
                true_zaehler += 1

        if true_zaehler != 1:
            raise (ValueError(f"Ein Mitarbeiter kann nur gesetzlich oder privat krankenversichert oder Minijobber oder "
                              f"anderweitig versichert sein. Sie haben {true_zaehler} Angaben bejaht. Das ist falsch!"))

        # Ein Minijobber ist niemals ueber den Arbeitgeber gesetzlich arbeitslosen- und rentenversichert. Arbeitgeber
        # zahlt lediglich pauschale Minijob-Abgaben.
        if (minijob and arbeitslosenversichert) or (minijob and rentenversichert):
            raise (ValueError(f"Ein Minijobber ist niemals ueber den Arbeitgeber arbeitslosen- und rentenversichert!"))

        # Kurzfristig beschaeftigte Minijobber duerfen keine Rentenpauschale abfuehren
        if kurzfristig_beschaeftigt and minijob and minijob_an_rentenpauschale:
            raise (ValueError(f"Ein kurzfristig beschaeftigter Minijobber zahlt kein AN-Rentenpauschale!"))

        # Ein Kurzfristig Beschaeftigter ist niemals ueber den Arbeitgeber gesetzlich arbeitslosen- und rentenversichert
        if (kurzfristig_beschaeftigt and arbeitslosenversichert) or (kurzfristig_beschaeftigt and rentenversichert):
            raise (ValueError(f"Ein kurzfristig Beschaeftigter ist niemals ueber den Arbeitgeber arbeitslosen- und "
                              f"rentenversichert!"))

        # Ein kurzfristig Beschaeftigter ist entweder anderweitig versichert oder Minijobber. Niemals ist er beim
        # Arbeitgeber gesetzlich versichert oder privat versichert mit Anspruch auf AG-Zuschuss
        if kurzfristig_beschaeftigt and gesetzlich_krankenversichert:
            raise (ValueError(f"Sie haben angegeben, dass dieser Mitarbeiter kurzfristig beschaeftigt und gleichzeitig"
                              f" bei Ihnen gesetzlich versichert ist. Das ist rechtlich nicht moeglich!"))

        if kurzfristig_beschaeftigt and privat_krankenversichert:
            raise (ValueError("Sie haben angegeben, dass dieser Mitarbeiter kurzfristig beschaeftigt und gleichzeitig"
                              " bei Ihnen privat versichert ist und somit Anspruch auf Arbeitgeberzuschuss hat. "
                              "Das ist rechtlich nicht moeglich!"))

        export_daten = [self.mandant_id,
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
                        befristet_bis,
                        strasse,
                        hausnummer,
                        postleitzahl,
                        ost_west_ausland,
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
                        unternehmen,
                        tarifbeschaeftigt,
                        tarif,
                        kurzfristig_beschaeftigt,
                        bezeichnung_krankenkasse,
                        abkuerzung_krankenkasse,
                        gesetzlich_krankenversichert,
                        ermaessigter_gkv_beitragssatz,
                        anzahl_kinder,
                        juenger_als_23_oder_vor_1940_geboren,
                        wohnhaft_sachsen,
                        privat_krankenversichert,
                        ag_zuschuss_private_krankenversicherung,
                        ag_zuschuss_private_pflegeversicherung,
                        minijob,
                        minijob_an_rentenpauschale,
                        anderweitig_versichert,
                        arbeitslosenversichert,
                        rentenversichert]
        self._export_zu_db('insert_neuer_mitarbeiter('
                           '%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,'
                           '%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,'
                           '%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,'
                           '%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,'
                           '%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)', export_daten)

    def insert_aussertarifliches_verguetungsbestandteil(self, neuanlage_aussertariflicher_verguetungsbestandteil):
        """
        Diese Methode uebertraegt einen Verguetungsbestandteil wie bspw. Grundgehalt, Urlaubsgeld etc. und verknuepft
        sie mit dem entsprechenden aussertariflich angestellten Mitarbeiter, in die Datenbank, in dem die Stored
        Procedure 'insert_aussertarifliches_verguetungsbestandteil' aufgerufen wird.
        :param neuanlage_aussertariflicher_verguetungsbestandteil: Name der Excel-Datei, dessen Daten in die Datenbank
                                                                   eingetragen werden sollen.
        """
        if not self.neues_passwort_geaendert:
            raise(ValueError("Ihr Administrator hat ein neues Passwort vergeben. Bitte wechseln Sie Ihr Passwort!"))

        # Import der Daten aus der Excel-Datei in das Pandas-Dataframe und Uebertragung in Liste "daten"
        daten = self._import_excel_daten(neuanlage_aussertariflicher_verguetungsbestandteil)

        # Daten aus importierter Excel-Tabelle '4 neuen Mitarbeiter anlegen/2 aussertariflicher
        # Verguetungsbestandteil.xlsx' pruefen
        personalnummer = self._existenz_str_daten_feststellen(daten[0], 'Personalnummer', 32, True)
        verguetungsbestandteil = self._existenz_str_daten_feststellen(daten[1], 'Verguetungsbestandteil', 64, True)
        betrag = self._existenz_zahlen_daten_feststellen(daten[2], 99999999, 'Betrag', True)
        gueltig_ab = self._existenz_date_daten_feststellen(daten[3], 'Entgelt gueltig ab', True)

        export_daten = [self.mandant_id, personalnummer, verguetungsbestandteil, betrag, gueltig_ab]
        self._export_zu_db('insert_aussertarifliches_verguetungsbestandteil(%s,%s,%s,%s,%s)', export_daten)

    def update_adresse(self, update_adressdaten):
        """
        Diese Methode uebertraegt die neue Adresse eines Mitarbeiters in die Datenbank, in dem der Stored Procedure
        'update_adresse' aufgerufen wird.
        :param update_adressdaten: Name der Excel-Datei, dessen Adressdaten in die Datenbank
                                   eingetragen werden sollen.
        """
        if not self.neues_passwort_geaendert:
            raise(ValueError("Ihr Administrator hat ein neues Passwort vergeben. Bitte wechseln Sie Ihr Passwort!"))

        # Import der Daten aus der Excel-Datei in das Pandas-Dataframe und Uebertragung in Liste "daten"
        daten = self._import_excel_daten(update_adressdaten)

        # Daten aus importierter Excel-Tabelle 'update personenbezogene Daten/1 Update Adresse.xlsx' pruefen
        personalnummer = self._existenz_str_daten_feststellen(daten[0], 'Personalnummer', 32, True)
        neuer_eintrag_gueltig_ab = self._existenz_date_daten_feststellen(daten[1], 'Gueltig ab', True)
        alter_eintrag_gueltig_bis = self._vorherigen_tag_berechnen(neuer_eintrag_gueltig_ab)
        strasse = self._existenz_str_daten_feststellen(daten[2], 'Strasse', 64, True)
        hausnummer = self._existenz_str_daten_feststellen(daten[3], 'Hausnummer', 8, True)
        postleitzahl = self._existenz_str_daten_feststellen(daten[4], 'Postleitzahl', 16, True)
        ost_west_ausland = self._existenz_str_daten_feststellen(daten[5], 'Postleitzahl', 8, True)
        stadt = self._existenz_str_daten_feststellen(daten[6], 'Stadt', 128, True)
        region = self._existenz_str_daten_feststellen(daten[7], 'Region', 128, True)
        land = self._existenz_str_daten_feststellen(daten[8], 'Land', 128, True)

        export_daten = [self.mandant_id,
                        personalnummer,
                        alter_eintrag_gueltig_bis,
                        neuer_eintrag_gueltig_ab,
                        strasse,
                        hausnummer,
                        postleitzahl,
                        ost_west_ausland,
                        stadt,
                        region,
                        land]
        self._export_zu_db('update_adresse(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)', export_daten)

    def update_mitarbeiterentlassung(self, update_mitarbeiterentlassung):
        """
        Diese Methode traegt die Entlassung und dessen Grund in die Datenbank in die Datenbank, in dem der Stored
        Procedure 'update_mitarbeiterentlassung' aufgerufen wird.
        :param update_mitarbeiterentlassung: Name der Excel-Datei, dessen Daten in die Datenbank
                                             eingetragen werden sollen.
        """
        if not self.neues_passwort_geaendert:
            raise(ValueError("Ihr Administrator hat ein neues Passwort vergeben. Bitte wechseln Sie Ihr Passwort!"))

        # Import der Daten aus der Excel-Datei in das Pandas-Dataframe und Uebertragung in Liste "daten"
        daten = self._import_excel_daten(update_mitarbeiterentlassung)

        # Daten aus importierter Excel-Tabelle 'update personenbezogene Daten/2 Update Mitarbeiterentlassung.xlsx'
        # pruefen
        personalnummer = self._existenz_str_daten_feststellen(daten[0], 'Personalnummer', 32, True)
        letzter_arbeitstag = self._existenz_date_daten_feststellen(daten[1], 'letzter Arbeitstag', True)
        austrittsgrund = self._existenz_str_daten_feststellen(daten[2], 'Austrittsgrund', 16, True)

        export_daten = [self.mandant_id, personalnummer, letzter_arbeitstag, austrittsgrund]
        self._export_zu_db('update_mitarbeiterentlassung(%s,%s,%s,%s)', export_daten)

    def update_krankenversicherungsbeitraege(self, update_krankenversicherungsbeitraege):
        """
        Diese Methode ordnet in der Datenbanke eine Abteilung einer anderen unter, in dem der Stored Procedure
        'update_krankenversicherungsbeitraege' aufgerufen wird.
        :param update_krankenversicherungsbeitraege: Name der Excel-Datei, dessen Daten in die Datenbank
        eingetragen werden sollen.
        """
        if not self.neues_passwort_geaendert:
            raise(ValueError("Ihr Administrator hat ein neues Passwort vergeben. Bitte wechseln Sie Ihr Passwort!"))

        # Import der Daten aus der Excel-Datei in das Pandas-Dataframe und Uebertragung in Liste "daten"
        daten = self._import_excel_daten(update_krankenversicherungsbeitraege)

        # Daten aus importierter Excel-Tabelle 'update Sozialversicherungsdaten/1 Krankenversicherungsbeitraege.xlsx'
        # pruefen
        ermaessigter_beitragssatz = self._existenz_boolean_daten_feststellen(daten[0],
                                                                             'ermaessigter Beitragssatz',
                                                                             True)
        ag_gkv_beitrag_in_prozent = self._existenz_zahlen_daten_feststellen(daten[1],
                                                                            99,
                                                                            'Arbeitgeberbeitrag GKV in Prozent',
                                                                            True)
        an_gkv_beitrag_in_prozent = self._existenz_zahlen_daten_feststellen(daten[2],
                                                                            99,
                                                                            'Arbeitnehmerbeitrag GKV in Prozent',
                                                                            True)
        beitragsbemessungsgrenze_gkv = self._existenz_zahlen_daten_feststellen(daten[3],
                                                                               99999999,
                                                                               'Beitragsbemessungsgrenze GKV',
                                                                               True)
        jahresarbeitsentgeltgrenze_gkv = self._existenz_zahlen_daten_feststellen(daten[4],
                                                                                 99999999,
                                                                                 'Jahresarbeitsentgeltgrenze GKV',
                                                                                 True)
        neuer_eintrag_gueltig_ab = self._existenz_date_daten_feststellen(daten[5], 'Gueltig ab', True)
        alter_eintrag_gueltig_bis = self._vorherigen_tag_berechnen(neuer_eintrag_gueltig_ab)

        export_daten = [self.mandant_id,
                        ermaessigter_beitragssatz,
                        ag_gkv_beitrag_in_prozent,
                        an_gkv_beitrag_in_prozent,
                        beitragsbemessungsgrenze_gkv,
                        jahresarbeitsentgeltgrenze_gkv,
                        alter_eintrag_gueltig_bis,
                        neuer_eintrag_gueltig_ab]
        self._export_zu_db('update_krankenversicherungsbeitraege(%s,%s,%s,%s,%s,%s,%s,%s)', export_daten)

    def update_erstelle_abteilungshierarchie(self, update_abteilungshierarchie):
        """
        Diese Methode ordnet in der Datenbanke eine Abteilung einer anderen unter, in dem der Stored Procedure
        'update_erstelle_abteilungshierarchie' aufgerufen wird.
        :param update_abteilungshierarchie: Name der Excel-Datei, dessen Daten in die Datenbank
                                            eingetragen werden sollen.
        """
        if not self.neues_passwort_geaendert:
            raise(ValueError("Ihr Administrator hat ein neues Passwort vergeben. Bitte wechseln Sie Ihr Passwort!"))

        # Import der Daten aus der Excel-Datei in das Pandas-Dataframe und Uebertragung in Liste "daten"
        daten = self._import_excel_daten(update_abteilungshierarchie)

        # Daten aus importierter Excel-Tabelle 'update personenbezogene Daten/3 Update Abteilungshierarchie.xlsx'
        # pruefen
        abteilung_unter = self._existenz_str_daten_feststellen(daten[0], 'untergeordnete Abteilung', 64, True)
        abteilung_ueber = self._existenz_str_daten_feststellen(daten[1], 'uebergeordnete Abteilung', 64, True)

        export_daten = [self.mandant_id, abteilung_unter, abteilung_ueber]
        self._export_zu_db('update_erstelle_abteilungshierarchie(%s,%s,%s)', export_daten)

    def delete_mitarbeiterdaten(self, mitarbeiter):
        """
        Methode ruft die Stored Procedure 'delete_mitarbeiterdaten' auf, welche alle personenbezogenen Daten
        eines Mitarbeiters aus den Assoziationstabellen, der Tabelle 'Aussertarifliche' und der
        Tabelle 'Mitarbeiter' entfernt
        :param mitarbeiter: Name der Excel-Datei, die die Personalnummer des Mitarbeiters enthaelt, der entfernt
                            werden soll
        """
        if not self.neues_passwort_geaendert:
            raise(ValueError("Ihr Administrator hat ein neues Passwort vergeben. Bitte wechseln Sie Ihr Passwort!"))

        # Import der Daten aus der Excel-Datei in das Pandas-Dataframe und Uebertragung in Liste "daten"
        daten = self._import_excel_daten(mitarbeiter)

        # Daten aus importierter Excel-Tabelle 'delete personenbezogene Daten/Personalnummer.xlsx' pruefen
        personalnummer = self._existenz_str_daten_feststellen(daten[0], 'Personalnummer', 32, True)

        export_daten = [self.mandant_id, personalnummer]
        self._export_zu_db('delete_mitarbeiterdaten(%s,%s)', export_daten)

    def _import_excel_daten(self, excel_datei_pfad):
        """
        Methode importiert die Daten aus der Excel-Datei.
        :param excel_datei_pfad: Pfade zur Excel-Datei, dessen Daten importiert werden sollen
        :return: importierte Daten
        """
        df_daten = pd.read_excel(f"{excel_datei_pfad}", index_col='Daten', na_filter=False)
        daten = list(df_daten.iloc[:, 0])

        return daten

    def _export_zu_db(self, stored_procedure, export_daten):
        """
        Methode uebergibt Liste mit Daten an die Personalstammdatenbank, indem die entsprechende Stored Procedure
        aufgerufen wird.
        :param stored_procedure: datenbankseitige Methode, welche die uebergebenen Daten in die Datenbank schreibt
        :param export_daten: Daten, welche in die Personalstammdatenbank eingetragen werden sollen
        """
        conn = datenbankbverbindung_aufbauen()
        cur = conn.cursor()

        cur.execute(f"set search_path to {self.schema}; call {stored_procedure}", export_daten)

        # Commit der Aenderungen
        conn.commit()

        # Cursor und Konnektor zu Datenbank schliessen
        cur.close()
        conn.close()

    def _existenz_str_daten_feststellen(self, str_daten, art, anzahl_zeichen, pflicht):
        """
        Methode stellt fest, ob optionale Daten vorliegen oder nicht und wenn ja, so sollen diese auf jeden Fall
        als String zurueckgegeben werden. So soll sichergestellt werden, dass dem Datenbanksystem die Daten in dem
        Datentyp uebergeben werden, in der sie in der Personalstammdatenbank gespeichert werden koennen.
        :param str_daten: wird untersucht, ob Daten darin enthalten sind
        :param art: gibt an, um was fuer Daten es sich handeln soll
        :param anzahl_zeichen: Anzahl der Zeichen, die der Inhalt von 'str_daten' hoechstens besitzen darf
        :param pflicht: boolean, der bei 'True' angibt, dass 'str_daten' kein leerer String sein darf
        :return: Falls Parameter 'daten' keine Daten enthaelt, wird None zurueckgegeben, sonst Daten
        """
        if str_daten == '' and not pflicht:
            str_daten = None
        elif str_daten == '' and pflicht:
            raise (ValueError(f"'{art}' ist nicht vorhanden."))
        elif len(str(str_daten)) > anzahl_zeichen:
            raise (ValueError(f"'{art}' darf hoechstens {anzahl_zeichen} Zeichen lang sein. "
                              f"Ihre Eingabe '{str_daten}' besitzt {len(str_daten)} Zeichen!"))
        else:
            str_daten = str(str_daten)

        return str_daten

    def _existenz_date_daten_feststellen(self, date_daten, art, pflicht):
        """
        Methode stellt fest, ob optionale Daten vorliegen oder nicht und wenn ja, so sollen diese auf jeden Fall
        als Date-Datentyp zurueckgegeben werden. So soll sichergestellt werden, dass dem Datenbanksystem die Daten in
        dem Datentyp uebergeben werden, in der sie in der Personalstammdatenbank gespeichert werden koennen.
        :param date_daten: wird untersucht, ob Daten darin enthalten sind
        :param art: gibt an, um was fuer Daten es sich handeln soll
        :param pflicht: boolean, der bei 'True' angibt, dass 'date_daten' kein leerer String sein darf
        :return: Falls Parameter 'daten' keine Daten enthaelt, wird None zurueckgegeben, sonst Daten
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
            raise (ValueError(f"'{date_daten}' ist nicht moeglich!"))

        return date_daten

    def _existenz_zahlen_daten_feststellen(self, zahlen_daten, hoechstbetrag, art, pflicht):
        """
        Methode stellt fest, ob optionale Daten vorliegen oder nicht und wenn ja, so sollen diese auf jeden Fall
        als Decimal-Datentyp zurueckgegeben werden. So soll sichergestellt werden, dass dem Datenbanksystem die Daten
        in dem Datentyp uebergeben werden, in der sie in der Personalstammdatenbank gespeichert werden koennen.
        :param zahlen_daten: wird untersucht, ob Daten darin enthalten sind
        :param hoechstbetrag: der Wert der Variablen 'zahlen_daten' darf nicht hoeher sein
        :param art: gibt an, um was fuer Daten es sich handeln soll
        :param pflicht: boolean, der bei 'True' angibt, dass 'zahlen_daten' kein leerer String sein darf
        :return: Falls Parameter 'daten' keine Daten enthaelt, wird None zurueckgegeben, sonst Daten
        """
        if zahlen_daten == '' and not pflicht:
            zahlen_daten = None
            return zahlen_daten
        elif zahlen_daten == '' and pflicht:
            raise (ValueError(f"'{art}' ist nicht vorhanden."))
        elif not isinstance(zahlen_daten, int) and not isinstance(zahlen_daten, float):
            raise (TypeError(f"Der uebergebene Wert '{zahlen_daten}' konnte nicht in eine Gleitkommazahl "
                             f"konvertiert werden!"))
        elif zahlen_daten > hoechstbetrag:
            raise (ValueError(f"'{art}' ist mit '{zahlen_daten}' hoeher als der zulaessige Maximalbetrag von "
                              f"'{hoechstbetrag}'!"))
        elif zahlen_daten < 0:
            raise (ValueError(f"'{art}' ist mit '{zahlen_daten}' kleiner als 0!"))
        elif art == 'Anzahl Kinder' or art == 'Beitragsjahr Unfallversicherung':
            zahlen_daten = int(zahlen_daten)
        else:
            zahlen_daten = round(decimal.Decimal(zahlen_daten), 3)

        return zahlen_daten

    def _existenz_boolean_daten_feststellen(self, boolean_daten, art, pflicht):
        """
            Methode stellt fest, ob optionale Daten vorliegen oder nicht und wenn ja, so sollen diese auf jeden Fall
            als boolean-Datentyp zurueckgegeben werden. So soll sichergestellt werden, dass dem Datenbanksystem die
            Daten in dem Datentyp uebergeben werden, in der sie in der Personalstammdatenbank gespeichert werden
            koennen.
            :param boolean_daten: wird untersucht, ob Daten darin enthalten sind
            :param art: gibt an, um was fuer Daten es sich handeln soll
            :param pflicht: boolean, der bei 'True' angibt, dass 'boolean_daten' kein leerer String sein darf
            :return: Falls Parameter 'daten' keine Daten enthaelt, wird None zurueckgegeben, sonst Daten
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
            raise TypeError(f"Der uebergebene Wert '{boolean_daten}' konnte nicht verarbeitet werden. Bitte geben "
                            f"Sie ausschliesslich 'ja' oder 'nein' ein.")

    def _vorherigen_tag_berechnen(self, datum):
        """
        Methode berechnet den Vortag des Datums, ab dem ein neuer Eintrag gueltig sein soll. Dies wird benoetigt,
        um fuer diverse 'update'-Methoden in der Spalte "Datum_Bis" des vorherigen Eintrags (gilt fuer alle
        Assoziationstabellen) ein Datum eintragen zu koennen.
        :param datum: Datum, ab dem ein neuer Eintrag gueltig werden soll
        :return: Datum des Vortags, dass gleichzeitig das Enddatum des alten Eintrags ist
        """
        tag_abziehen = timedelta(1)

        try:
            letzter_tag_alter_eintrag = datum - tag_abziehen
        except TypeError:
            raise (TypeError(f"'{datum}' ist kein datetime-Objekt!"))

        return letzter_tag_alter_eintrag
