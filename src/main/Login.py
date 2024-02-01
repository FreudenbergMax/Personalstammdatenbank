import psycopg2

from src.main.Mandant import Mandant
from src.main.Administrator import Administrator


class Login:

    def __init__(self, schema='public'):

        if schema != 'public' and schema != 'temp_test_schema':
            raise(ValueError("Diese Bezeichnung fuer ein Schema ist nicht erlaubt!"))

        self.schema = schema
        self.liste_mandanten = []
        self.liste_admins = []

    def registriere_mandant_und_admin(self, mandantenname, mandantenpasswort, mandantenpasswort_wiederholen,
                                      admin_personalnummer, admin_vorname, admin_nachname, adminpasswort,
                                      adminpasswort_wiederholen):
        """
        Methode erstellt einen neuen Mandanten
        :param mandantenname: Name der Firma, der als Mandant dienen soll
        :param mandantenpasswort: Passwort des Mandanten, welches fuer Login benoetigt wird
        :param mandantenpasswort_wiederholen: Test, um zu pruefen, ob der Anmelder das Passwort fuer den Mandanten beim
                                              ersten Mal wie beabsichtigt geschrieben hat
        :param admin_personalnummer: Personalnummer des Administrators
        :param admin_vorname: Vorname des Administrators
        :param admin_nachname: Nachname des Administrators
        :param adminpasswort: Passwort des Administrators, welches fuer Login benoetigt wird
        :param adminpasswort_wiederholen: Test, um zu pruefen, ob der Anmelder das Passwort fuer den Administrator beim
                                          ersten Mal wie beabsichtigt geschrieben hat
        """
        neuer_mandant = Mandant(mandantenname, mandantenpasswort, mandantenpasswort_wiederholen, self.schema)
        neuer_admin = Administrator(neuer_mandant, admin_personalnummer, admin_vorname, admin_nachname,
                                    adminpasswort, adminpasswort_wiederholen, self.schema)

        self.liste_mandanten.append(neuer_mandant)
        self.liste_admins.append(neuer_admin)

    def _datenbankbverbindung_aufbauen(self):
        """
        Baut eine Connection zur Datenbank auf. Diese Methode wird jedes Mal aufgerufen, bevor mit der Datenbank
        interagiert werden soll.
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

    def login_admin(self, mandantenname, mandantenpasswort, personalnummer, adminpasswort):
        """
        Ueber diese Funktion kann sich ein Admin einloggen und erhaelt Zugang zu seinem Administrator-Objekt
        :param mandantenname: Mandant, zu dem der Admin gehoert
        :param mandantenpasswort: Passwort des Mandanten
        :param personalnummer: Personalnummer des Administrators
        :param adminpasswort: Passwort des Administrators
        :return: Administrator-Objekt
        """
        gesuchter_admin = None

        # Admin aus Liste suchen
        for i in range(len(self.liste_admins)):
            if self.liste_admins[i].get_personalnummer() == personalnummer and \
                    self.liste_admins[i].get_mandant().get_mandantenname() == mandantenname:

                # Passwoerter in Datenbank abgleichen
                conn = self._datenbankbverbindung_aufbauen()

                passwort_query = f"set search_path to {self.schema};" \
                                 f"SELECT adminpasswort_pruefen('" \
                                 f"{self.liste_admins[i].get_mandant().get_mandant_id()}', " \
                                 f"'{personalnummer}', '{adminpasswort}', '{mandantenpasswort}')"
                cur = conn.cursor()
                cur.execute(passwort_query)
                boolean = cur.fetchone()[0]

                # Commit der Aenderungen
                conn.commit()

                # Cursor und Konnektor zu Datenbank schliessen
                cur.close()
                conn.close()

                if boolean:
                    gesuchter_admin = self.liste_admins[i]
                    return gesuchter_admin
                else:
                    raise ValueError("Eingegebene Passwoerter sind falsch!")

        if gesuchter_admin is None:
            raise ValueError(f"Admin mit Personalnummer '{personalnummer}' nicht vorhanden!")
        else:
            return gesuchter_admin

    def login_nutzer(self, mandantenname, mandantenpasswort, personalnummer, nutzerpasswort):
        """
        Ueber diese Funktion kann sich ein Nutzer einloggen und erhaelt Zugang zu seinem Nutzer-Objekt
        :param mandantenname: Mandant, zu dem der Admin gehoert
        :param mandantenpasswort: Passwort des Mandanten
        :param personalnummer: Personalnummer des Administrators
        :param nutzerpasswort: Passwort des Nutzers
        :return: Nutzer-Objekt
        """
        gesuchter_nutzer = None

        # Mandant aus Liste suchen, zu dem der Nutzer gehoert
        for i in range(len(self.liste_mandanten)):
            if self.liste_mandanten[i].get_mandantenname() == mandantenname:

                # Passwoerter in Datenbank abgleichen
                conn = self._datenbankbverbindung_aufbauen()

                passwort_query = f"set search_path to {self.schema};" \
                                 f"SELECT nutzerpasswort_pruefen('" \
                                 f"{self.liste_mandanten[i].get_mandant_id()}', " \
                                 f"'{personalnummer}', '{nutzerpasswort}', '{mandantenpasswort}')"
                cur = conn.cursor()
                cur.execute(passwort_query)
                boolean = cur.fetchone()[0]

                # Commit der Aenderungen
                conn.commit()

                # Cursor und Konnektor zu Datenbank schliessen
                cur.close()
                conn.close()

                # Nutzerobjekt aus Liste raussuchen und uebergeben
                if boolean:
                    for k in range(len(self.liste_mandanten[i].get_nutzerliste())):
                        if self.liste_mandanten[i].get_nutzerliste()[k].get_personalnummer() == personalnummer:
                            gesuchter_nutzer = self.liste_mandanten[i].get_nutzerliste()[k]

                    return gesuchter_nutzer
                else:
                    raise ValueError("Eingegebene Passwoerter sind falsch!")

        if gesuchter_nutzer is None:
            raise ValueError(f"Nutzer mit Personalnummer '{personalnummer}' nicht vorhanden!")

    def entferne_mandant_nutzer_und_admin(self, mandantenname, mandantenpasswort, mandantenpasswort_wiederholen,
                                          admin_personalnummer, adminpasswort, adminpasswort_wiederholen):
        """
        Methode entfernt alle Daten des Mandanten aus der Datenbank und entfernt den Mandanten und dessen Administrator
        aus den Listen "liste_mandanten" und "liste_admins". Diese Methode wird verwendet, wenn die Dienste der
        Personalstammdatenbank nicht mehr verwendet werden soll.
        :param mandantenname: Mandant, der entfernt werden soll
        :param mandantenpasswort: Passwort des Mandanten
        :param mandantenpasswort_wiederholen: Test, um zu pruefen, ob der Anmelder das Passwort fuer den Mandanten beim
                                              ersten Mal wie beabsichtigt geschrieben hat
        :param admin_personalnummer: Personalnummer des Admins des Mandanten, der entfernt werden soll
        :param adminpasswort: Passwort des Administrators
        :param adminpasswort_wiederholen: Test, um zu pruefen, ob der Anmelder das Passwort fuer den Administrator beim
                                          ersten Mal wie beabsichtigt geschrieben hat
        """
        if mandantenpasswort != mandantenpasswort_wiederholen or adminpasswort != adminpasswort_wiederholen:
            raise (ValueError("Passwort falsch eingegeben."))

        # Login des Admins
        admin = self.login_admin(mandantenname, mandantenpasswort, admin_personalnummer, adminpasswort)

        # Entfernung aller der Daten des Mandanten aus der Datenbank
        export_daten = [admin.get_mandant().get_mandant_id()]

        conn = self._datenbankbverbindung_aufbauen()
        cur = conn.cursor()

        cur.execute(f"set search_path to {self.schema}; call delete_mandantendaten(%s)", export_daten)

        # Commit der Aenderungen
        conn.commit()

        # Cursor und Konnektor zu Datenbank schliessen
        cur.close()
        conn.close()

        # Entfernung des Administrators aus Login_Liste "liste_admins"
        for i in range(len(self.liste_admins)):
            if self.liste_admins[i].get_personalnummer() == admin_personalnummer and \
                    self.liste_admins[i].get_mandant().get_mandantenname() == mandantenname:
                del self.liste_admins[i]

        # Entfernung des Mandanten aus Login-Liste "liste_mandanten"
        for i in range(len(self.liste_mandanten)):
            if self.liste_mandanten[i].get_mandantenname() == mandantenname:
                del self.liste_mandanten[i]
