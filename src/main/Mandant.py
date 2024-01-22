import psycopg2
from src.main.Nutzer import Nutzer


class Mandant:

    def __init__(self, mandantenname, passwort, passwortwiederholung, schema='public'):

        if not isinstance(mandantenname, str):
            raise(TypeError("Der Name des Mandanten muss ein String sein."))

        if "postgres" in str.lower(mandantenname):
            raise(ValueError(f"Dieser Name ist nicht erlaubt: {mandantenname}."))

        if mandantenname == "":
            raise(ValueError(f"Der Name des Mandanten muss aus mindestens einem Zeichen bestehen."))

        if len(mandantenname) > 128:
            raise(ValueError(f"Der Name des Mandanten darf höchstens 128 Zeichen lang sein."
                             f"'{mandantenname}' besitzt {len(mandantenname)} Zeichen!"))

        if len(str(passwort)) > 128:
            raise(ValueError("Passwort darf hoechstens 128 Zeichen haben!"))

        if passwort != passwortwiederholung:
            raise(ValueError("Passwoerter stimmen nicht ueberein!"))

        if schema != 'public' and schema != 'temp_test_schema':
            raise(ValueError("Diese Bezeichnung für ein Schema ist nicht erlaubt!"))

        self.mandantenname = mandantenname
        self.schema = schema
        self.mandant_id = self._in_datenbank_anlegen(str(passwort))
        self.liste_nutzer = []

    def get_mandant_id(self):
        return self.mandant_id

    def get_mandantenname(self):
        return self.mandantenname

    def get_nutzerliste(self):
        return self.liste_nutzer

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

    def _in_datenbank_anlegen(self, passwort):
        """
        Methode ruft die Stored Procedure 'mandant_anlegen' auf, welche die Daten des Mandanten in der
        Personalstammdatenbank speichert.
        :param passwort: Passwort, welches fuer den Mandanten angelegt werden soll
        """
        conn = self._datenbankbverbindung_aufbauen()

        mandant_insert_query = f"set search_path to {self.schema};SELECT mandant_anlegen('{self.mandantenname}', " \
                               f"'{passwort}')"
        cur = conn.cursor()
        cur.execute(mandant_insert_query)

        # Commit der Änderungen
        conn.commit()

        mandant_id = cur.fetchone()[0]

        # Cursor und Konnektor zu Datenbank schließen
        cur.close()
        conn.close()

        return mandant_id
