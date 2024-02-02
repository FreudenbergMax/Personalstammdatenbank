import psycopg2

from src.main.Nutzer import Nutzer


class Administrator:

    def __init__(self, mandant, personalnummer, vorname, nachname, passwort, passwort_wiederholen, schema='public'):

        if personalnummer == "":
            raise (ValueError(f"Die Personalnummer des Nutzers muss aus mindestens einem Zeichen bestehen."))

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
        self.mandant = mandant
        self.personalnummer = str(personalnummer)
        self.vorname = str(vorname)
        self.nachname = str(nachname)
        self.administrator_id = self._in_datenbank_anlegen(str(passwort))

    def get_personalnummer(self):
        return self.personalnummer

    def get_mandant(self):
        return self.mandant

    def _in_datenbank_anlegen(self, passwort):
        """
        Methode ruft die Stored Procedure 'administrator_anlegen' auf, welche die Daten des Nutzers in der
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

        # Commit der Aenderungen
        conn.commit()

        # Cursor und Konnektor zu Datenbank schliessen
        cur.close()
        conn.close()

        return nutzer_id

    def _datenbankbverbindung_aufbauen(self):
        """
        Baut eine Connection zur Datenbank auf.
        :return: conn-Variable, die die Verbindung zur Datenbank enthaelt
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
        Da jeder Mandant mehrere Nutzer haben kann, werden alle Nutzer eines Mandanten hier erzeugt und im
        Listen-Objekt "liste_nutzer" von 'Mandant' gespeichert.
        :param personalnummer: des Nutzers
        :param vorname: Vorname des Nutzers
        :param nachname: Nachname des Nutzers
        :param passwort: Passwort des Nutzers, welches fuer Login benoetigt wird
        :param passwort_wiederholen: Test, um zu pruefen, ob der Anmelder das Passwort fuer den Mandanten beim
                                     ersten Mal wie beabsichtigt geschrieben hat
        """
        nutzer = Nutzer(self.mandant.get_mandant_id(), personalnummer, vorname, nachname, passwort,
                        passwort_wiederholen, self.schema)
        nutzer.get_neues_passwort_geaendert = False
        self.mandant.get_nutzerliste().append(nutzer)

    def nutzer_entsperren(self, personalnummer, neues_passwort, neues_passwort_wiederholen):
        """
        Methode entsperrt einen Nutzer, nachdem er das Passwort dreimal hintereinander falsch eingegeben hat.
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

        gesuchter_nutzer = None

        for i in range(len(self.get_mandant().get_nutzerliste())):
            if self.get_mandant().get_nutzerliste()[i].get_personalnummer() == personalnummer:

                gesuchter_nutzer = self.get_mandant().get_nutzerliste()[i]

                # Nutzer aus Datenbank entfernen
                nutzer_delete_query = f"set search_path to {self.schema};" \
                                      f"CALL nutzer_entsperren({self.get_mandant().get_mandant_id()}, " \
                                      f"'{personalnummer}', '{neues_passwort}')"

                conn = self._datenbankbverbindung_aufbauen()

                cur = conn.cursor()
                cur.execute(nutzer_delete_query)

                # Commit der Aenderungen
                conn.commit()

                # Cursor und Konnektor zu Datenbank schliessen
                cur.close()
                conn.close()

                gesuchter_nutzer.get_neues_passwort_geaendert = False

        if gesuchter_nutzer is None:
            raise ValueError(f"Nutzer mit Personalnummer '{personalnummer}' nicht vorhanden!")

    def nutzer_entfernen(self, personalnummer):
        """
        Funktion entfernt einen Nutzer aus der Datenbank und aus der Liste "liste_nutzer" des jeweiligen Mandant-
        Objekts.
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

                # Commit der Aenderungen
                conn.commit()

                # Cursor und Konnektor zu Datenbank schliessen
                cur.close()
                conn.close()

                # Nutzer aus Liste 'liste_nutzer' des Mandant-Objekt entfernen
                self.get_mandant().get_nutzerliste().remove(self.get_mandant().get_nutzerliste()[i])

                nutzer_entfernt = True
                print(f"Nutzer {personalnummer} wurde entfernt!")

        if not nutzer_entfernt:
            raise (ValueError(f"Nutzer {personalnummer} existiert nicht!"))
