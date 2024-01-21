import psycopg2

from src.main.Nutzer import Nutzer
from src.main.Mandant import Mandant
from src.main.Administrator import Administrator


class Login:

    def __init__(self):
        self.liste_mandanten = []
        self.liste_admins = []

    def registriere_mandant_und_admin(self, mandantenname, mandantenpasswort, mandantenpasswort_wiederholen,
                                      admin_personalnummer, admin_vorname, admin_nachname, adminpasswort,
                                      adminpasswort_wiederholen, schema='public'):
        """
        Methode erstellt einen neuen Mandanten
        :param mandantenname: Name der Firma, der als Mandant dienen soll
        :param mandantenpasswort: Passwort des Mandanten, welches für Login benoetigt wird
        :param mandantenpasswort_wiederholen: Test, um zu pruefen, ob der Anmelder das Passwort fuer den Mandanten beim
                                              ersten Mal wie beabsichtigt geschrieben hat
        :param admin_personalnummer: Personalnummer des Administrators
        :param admin_vorname: Vorname des Administrators
        :param admin_nachname: Nachname des Administrators
        :param adminpasswort: Passwort des Administrators, welches für Login benoetigt wird
        :param adminpasswort_wiederholen: Test, um zu pruefen, ob der Anmelder das Passwort fuer den Administrator beim
                                          ersten Mal wie beabsichtigt geschrieben hat
        :param schema: enthaelt das Schema, welches angesprochen werden soll
        """
        try:
            neuer_mandant = Mandant(mandantenname, mandantenpasswort, mandantenpasswort_wiederholen, schema)
            neuer_admin = Administrator(neuer_mandant, admin_personalnummer, admin_vorname, admin_nachname,
                                        adminpasswort, adminpasswort_wiederholen, schema)
        except ValueError:
            raise (ValueError(f"Registrierung wurde nicht durchgefuehrt!"))

        self.liste_mandanten.append(neuer_mandant)
        self.liste_admins.append(neuer_admin)

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

    def login_admin(self, mandantenname, mandantenpasswort, personalnummer, adminpasswort, schema='public'):
        """
        Ueber diese Funktion kann sich ein Admin einloggen und erhaelt Zugang zu seinem Administrator-Objekt
        :param mandantename: Mandant, zu dem der Admin gehoert
        :param mandantenpasswort: Passwort des Mandanten
        :param personalnummer: Personalnummer des Administrators
        :param adminpasswort: Passwort des Administrators
        :param schema: enthaelt das Schema, welches angesprochen werden soll
        :return: Administrator-Objekt
        """
        gesuchter_admin = None

        # Admin aus Liste suchen
        for i in range(len(self.liste_admins)):
            if self.liste_admins[i].get_personalnummer() == personalnummer and \
                    self.liste_admins[i].get_mandant().get_mandantenname() == mandantenname:

                # Passwoerter in Datenbank abgleichen
                conn = self._datenbankbverbindung_aufbauen()

                passwort_query = f"set search_path to {schema};" \
                                 f"SELECT adminpasswort_pruefen('" \
                                 f"{self.liste_admins[i].get_mandant().get_mandant_id()}', " \
                                 f"'{personalnummer}', '{adminpasswort}', '{mandantenpasswort}')"
                cur = conn.cursor()
                cur.execute(passwort_query)
                boolean = cur.fetchone()[0]

                # Commit der Änderungen
                conn.commit()

                # Cursor und Konnektor zu Datenbank schließen
                cur.close()
                conn.close()

                if boolean:
                    gesuchter_admin = self.liste_admins[i]
                    return gesuchter_admin
                else:
                    raise ValueError("Eingegebene Passwoerter sind falsch!")

        if gesuchter_admin is None:
            raise ValueError(f"Admin mit Personalnummer {personalnummer} nicht vorhanden!")
        else:
            return gesuchter_admin

    def login_nutzer(self, mandantenname, mandantenpasswort, personalnummer, nutzerpasswort, schema='public'):
        """
        Ueber diese Funktion kann sich ein Nutzer einloggen und erhaelt Zugang zu seinem Nutzer-Objekt
        :param mandantenname: Mandant, zu dem der Admin gehoert
        :param mandantenpasswort: Passwort des Mandanten
        :param personalnummer: Personalnummer des Administrators
        :param nutzerpasswort: Passwort des Nutzers
        :param schema: enthaelt das Schema, welches angesprochen werden soll
        :return: Nutzer-Objekt
        """
        gesuchter_nutzer = None

        # Mandant aus Liste suchen, zu dem der Nutzer gehoert
        for i in range(len(self.liste_mandanten)):
            if self.liste_mandanten[i].get_mandantenname() == mandantenname:

                # Passwoerter in Datenbank abgleichen
                conn = self._datenbankbverbindung_aufbauen()

                passwort_query = f"set search_path to {schema};" \
                                 f"SELECT nutzerpasswort_pruefen('" \
                                 f"{self.liste_mandanten[i].get_mandant_id()}', " \
                                 f"'{personalnummer}', '{nutzerpasswort}', '{mandantenpasswort}')"
                cur = conn.cursor()
                cur.execute(passwort_query)
                boolean = cur.fetchone()[0]

                # Commit der Änderungen
                conn.commit()

                # Cursor und Konnektor zu Datenbank schließen
                cur.close()
                conn.close()

                # Nutzerobjekt aus Liste raussuchen und uebergeben
                if boolean:
                    for k in range(len(self.liste_mandanten[i].get_nutzerliste())):
                        if self.liste_mandanten[i].get_nutzerliste()[k].get_personalnummer() == personalnummer:
                            gesuchter_nutzer = self.liste_mandanten[i].get_nutzerliste()[k]

                            # falls nach einer Entsperrung der Administrator ein neues Passwort vergeben musste,
                            # muss der Nutzer das Passwort nochmal aendern, damit er ein Passwort hat, welches nur der
                            # Nutzer kennt



                    return gesuchter_nutzer
                else:
                    print("Eingegebene Passwoerter sind falsch!")
