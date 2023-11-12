import psycopg2
import pandas as pd
import openpyxl

from src.main.Nutzer import Nutzer


class Mandant:

    def __init__(self, mandantenname, conn):

        if str.lower(mandantenname) == "postgres":
            raise(ValueError(f"Dieser Name ist nicht erlaubt: {mandantenname}."))

        if mandantenname == "":
            raise(ValueError(f"Der Name des Mandanten muss aus mindestens einem Zeichen bestehen."))

        if len(mandantenname) > 128:
            raise(ValueError(f"Der Name des Mandanten darf höchstens 128 Zeichen lang sein."))

        self.mandantenname = mandantenname
        self.mandant_id = self._id_erstellen(conn)
        self._in_datenbank_anlegen(conn)
        self.liste_nutzer = []

    def _id_erstellen(self, conn):
        """
        Methode ruft die stored Procedure 'erstelle_neue_id' auf, welche eine neue Mandant_ID berechnet und den Wert
        zurückgibt.
        :param conn: Connection zur Personalstammdatenbank
        :return: berechnete Mandant_ID
        """
        neue_id_query = "SELECT erstelle_neue_id('Mandant_ID', 'Mandanten')"

        cur = conn.cursor()
        cur.execute(neue_id_query)
        mandant_id = cur.fetchall()[0][0]

        return mandant_id

    def _in_datenbank_anlegen(self, conn):
        """
        Methode ruft die Stored Procedure 'mandant_anlegen' auf, welche die Daten des Mandanten in der
        Personalstammdatenbank speichert.
        :param conn: Connection zur Personalstammdatenbank
        """
        mandant_insert_query = f"SELECT mandant_anlegen({self.mandant_id}, '{self.mandantenname}')"
        cur = conn.cursor()
        cur.execute(mandant_insert_query)

        # Commit der Änderungen
        conn.commit()

        # Cursor schließen
        cur.close()

    def nutzer_anlegen(self, vorname, nachname, conn):
        """
        Da jeder Mandant mehrere Nutzer haben kann, werden alle Nutzer eines Mandanten hier erzeugt und in einer
        klasseneigenen Liste "liste_nutzer" gespeichert.
        :param vorname: Vorname des Nutzers
        :param nachname: Nachname des Nutzers
        :param conn: Connection zur Datenbank
        """
        nutzer = Nutzer(vorname, nachname, self.mandant_id, conn)
        self.liste_nutzer.append(nutzer)
        print("Nutzer", self.liste_nutzer[len(self.liste_nutzer)-1].get_vorname(), self.liste_nutzer[len(self.liste_nutzer)-1].get_nachname(), "angelegt.")

    def get_nutzer(self, vorname, nachname):
        """
        Funktion sucht den angefragten Nutzer raus, mit dem dann Operationen auf der Datenbank durchgeführt werden
        können.
        :param vorname: Vorname des Nutzers
        :param nachname: Nachname des Nutzers
        :return: Nutzer-Objekt, der auf der Datenbank operieren soll
        """
        for i in range(len(self.liste_nutzer)):
            if self.liste_nutzer[i].get_vorname() == vorname and self.liste_nutzer[i].get_nachname() == nachname:
                return self.liste_nutzer[i]

    def nutzer_entfernen(self, vorname, nachname, conn):
        """
        Funktion entfernt einen Nutzer.
        :param vorname: Vorname des zu löschenden Nutzers
        :param nachname: Nachname des zu löschenden Nutzers
        :param conn: Connection zur Datenbank
        """
        for i in range(len(self.liste_nutzer)):
            if self.liste_nutzer[i].get_vorname == vorname and self.liste_nutzer[i].get_nachname == nachname:
                self.liste_nutzer.remove(self.liste_nutzer[i])
                self.liste_nutzer[i].nutzer_aus_db_entfernen(conn)
                print("Nutzer", vorname, nachname, "entfernt.")




