from src.main.Datenbankverbindung import datenbankbverbindung_aufbauen


class Mandant:

    def __init__(self, mandantenname, passwort, passwortwiederholung, schema='public'):

        if str(mandantenname) == "":
            raise(ValueError(f"Der Name des Mandanten muss aus mindestens einem Zeichen bestehen."))

        if len(str(mandantenname)) > 128:
            raise(ValueError(f"Der Name des Mandanten darf hoechstens 128 Zeichen lang sein."
                             f"'{mandantenname}' besitzt {len(mandantenname)} Zeichen!"))

        if len(str(passwort)) > 128:
            raise(ValueError("Passwort darf hoechstens 128 Zeichen haben!"))

        if passwort != passwortwiederholung:
            raise(ValueError("Passwoerter stimmen nicht ueberein!"))

        self.mandantenname = str(mandantenname)
        self.schema = schema
        self.mandant_id = self._in_datenbank_anlegen(str(passwort))
        self.liste_nutzer = []

    def get_mandant_id(self):
        return self.mandant_id

    def get_mandantenname(self):
        return self.mandantenname

    def get_nutzerliste(self):
        return self.liste_nutzer

    def _in_datenbank_anlegen(self, passwort):
        """
        Methode ruft die Stored Procedure 'mandant_anlegen' auf, welche die Daten des Mandanten in der
        Personalstammdatenbank speichert.
        :param passwort: Passwort, welches fuer den Mandanten angelegt werden soll
        """
        conn = datenbankbverbindung_aufbauen()

        mandant_insert_query = f"set search_path to {self.schema};SELECT mandant_anlegen('{self.mandantenname}', " \
                               f"'{passwort}')"
        cur = conn.cursor()
        cur.execute(mandant_insert_query)

        # Commit der Aenderungen
        conn.commit()

        mandant_id = cur.fetchone()[0]

        # Cursor und Konnektor zu Datenbank schliessen
        cur.close()
        conn.close()

        return mandant_id
