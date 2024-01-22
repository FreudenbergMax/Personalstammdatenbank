import psycopg2

from src.main.Mandant import Mandant
from src.main.Nutzer import Nutzer


class Administrator:

    def __init__(self, mandant, personalnummer, vorname, nachname, passwort, passwort_wiederholen, schema='public'):

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

        if len(str(passwort)) > 128:
            raise (ValueError("Passwort darf hoechstens 128 Zeichen haben!"))

        if passwort != passwort_wiederholen:
            raise (ValueError("Passwoerter stimmen nicht ueberein!"))

        if schema != 'public' and schema != 'temp_test_schema':
            raise (ValueError("Diese Bezeichnung für ein Schema ist nicht erlaubt!"))

        self.schema = schema
        self.mandant = mandant
        self.personalnummer = str(personalnummer)
        self.vorname = vorname
        self.nachname = nachname
        self.administrator_id = self._in_datenbank_anlegen(str(passwort))

    def get_personalnummer(self):
        return self.personalnummer

    def get_mandant(self):
        return self.mandant

    def _in_datenbank_anlegen(self, passwort):
        """
        Methode ruft die Stored Procedure 'nutzer_anlegen' auf, welche die Daten des Nutzers in der
        Personalstammdatenbank speichert.
        :param passwort: Passwort des Admins
        :return: Nutzer_ID, welche als Objekt-Variable gespeichert wird
        """

        conn = self._datenbankbverbindung_aufbauen()

        admin_insert_query = f"set search_path to {self.schema};" \
                             f"SELECT administrator_anlegen('{self.mandant.get_mandant_id()}', " \
                             f"'{self.personalnummer}', '{self.vorname}', '{self.nachname}', '{passwort}')"
        cur = conn.cursor()
        nutzer_id = cur.execute(admin_insert_query)

        # Commit der Änderungen
        conn.commit()

        # Cursor und Konnektor zu Datenbank schließen
        cur.close()
        conn.close()

        return nutzer_id

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

    def nutzer_anlegen(self, personalnummer, vorname, nachname, passwort, passwort_wiederholen):
        """
        Da jeder Mandant mehrere Nutzer haben kann, werden alle Nutzer eines Mandanten hier erzeugt und in einer
        klasseneigenen Liste "liste_nutzer" gespeichert.
        :param personalnummer: des Nutzers
        :param vorname: Vorname des Nutzers
        :param nachname: Nachname des Nutzers
        :param passwort: Passwort des Nutzers, welches für Login benoetigt wird
        :param passwort_wiederholen: Test, um zu pruefen, ob der Anmelder das Passwort fuer den Mandanten beim
                                     ersten Mal wie beabsichtigt geschrieben hat
        """
        nutzer = Nutzer(self.mandant.get_mandant_id(), personalnummer, vorname, nachname, passwort,
                        passwort_wiederholen, self.schema)
        self.mandant.get_nutzerliste().append(nutzer)

    def nutzer_entsperren(self, personalnummer, neues_passwort, neues_passwort_wiederholen):
        """
        Methode entsperrt einen Nutzer, nachdem er das Passwort dreimal falsch eingegeben hat.
        :param personalnummer: Personalnummer des Nutzers, der sich gesperrt hat
        :param neues_passwort: neues Passwort vom Administrator fuer den Nutzer. Nachdem die Sperre aufgehoben ist,
                               kann der Administrator dem wieder entsperrten Nutzer das Passwort uebergeben. Nutzer
                               wird, sobald er sich wieder einloggt, bei der ersten Operation dann aufgefordert,
                               ein neues Passwort zu waehlen, dass der Admin dann nicht mehr kennt.
        :param neues_passwort_wiederholen: Test, um zu pruefen, ob das gewaehlte Passwort des Administrators beim ersten
                                           Mal wie beabsichtigt eingegeben wurde
        """
        if neues_passwort != neues_passwort_wiederholen:
            raise(ValueError("Zweite Passworteingabe ist anders als erste Passworteingabe!"))

        for i in range(len(self.get_mandant().get_nutzerliste())):
            if self.get_mandant().get_nutzerliste()[i].get_personalnummer() == personalnummer:
                conn = self._datenbankbverbindung_aufbauen()

                # Nutzer aus Datenbank entfernen
                nutzer_delete_query = f"set search_path to {self.schema};" \
                                      f"CALL nutzer_entsperren({self.get_mandant().get_mandant_id()}, " \
                                      f"'{personalnummer}', '{neues_passwort}')"

                cur = conn.cursor()
                cur.execute(nutzer_delete_query)

                # Commit der Änderungen
                conn.commit()

                # Cursor und Konnektor zu Datenbank schließen
                cur.close()
                conn.close()

                self.get_mandant().get_nutzerliste()[i].get_neues_passwort_geaendert = False

    def nutzer_entfernen(self, personalnummer):
        """
        Funktion entfernt einen Nutzer.
        :param personalnummer: des Nutzers, der entfernt werden soll
        """

        nutzer_entfernt = False

        for i in range(len(self.get_mandant().get_nutzerliste())):
            if self.get_mandant().get_nutzerliste()[i].get_personalnummer() == personalnummer:

                conn = self._datenbankbverbindung_aufbauen()

                # Nutzer aus Datenbank entfernen
                nutzer_delete_query = f"set search_path to {self.schema};" \
                                      f"CALL nutzer_entfernen({self.get_mandant().get_mandant_id()}, " \
                                      f"'{personalnummer}')"

                cur = conn.cursor()
                cur.execute(nutzer_delete_query)

                # Commit der Änderungen
                conn.commit()

                # Cursor und Konnektor zu Datenbank schließen
                cur.close()
                conn.close()

                # Nutzer aus Liste 'liste_nutzer' des Mandant-Objekt entfernen
                self.get_mandant().get_nutzerliste().remove(self.get_mandant().get_nutzerliste()[i])

                nutzer_entfernt = True
                print(f"Nutzer {personalnummer} wurde entfernt!")

        if not nutzer_entfernt:
            print(f"Nutzer {personalnummer} existiert nicht!")

    def delete_mandantendaten(self):
        """
        Methode ruft die Stored Procedure 'delete_mandantendaten' auf, welche alle Daten des Mandanten aus allen
        Tabellen entfernt.
        :param schema: enthaelt das Schema, welches angesprochen werden soll
        """
        export_daten = [self.mandant.get_mandant_id()]

        conn = self._datenbankbverbindung_aufbauen()
        cur = conn.cursor()

        cur.execute(f"set search_path to {self.schema}; call delete_mandantendaten(%s)", export_daten)

        # Commit der Aenderungen
        conn.commit()

        # Cursor und Konnektor zu Datenbank schließen
        cur.close()
        conn.close()