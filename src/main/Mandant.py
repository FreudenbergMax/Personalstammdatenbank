import psycopg2


class Mandant:

    def __init__(self, mandantenname, conn):
        self.mandantenname = mandantenname
        self._mandant_anlegen(conn)
        print(f"Neuer Mandant {self.mandantenname} erstellt!")

    def get_mandantenname(self):
        """
        gibt die Bezeichnung des Mandanten zurück
        """
        return self.mandantenname

    def _mandant_anlegen(self, conn):
        """
        Legt den Mandanten als User in der Datenbank an und fügt sie der Gruppe "Mandantengruppe" zu.
        So sit sichergestellt, dass der Mandant in der Datenbank hinterlegt sit und das Recht hat,
        SELECT-, INSERT-, UPDATE- und DELETE-Befehle an die Datenbank zu senden
        :param conn:
        :return:
        """
        # Ein Cursor-Objekt erstellen
        cur = conn.cursor()

        # Stored Procedure aufrufen, der den neuen User in der Datenbank erstellt
        cur.callproc('erstelle_user', [self.mandantenname])

        # Commit der Änderungen
        conn.commit()

        # Cursor schließen
        cur.close()

    def insert_neuer_mitarbeiter(self, vorname, nachname, geschlecht, geburtsdatum, eintrittsdatum, steuernummer, sozialversicherungsnummer, iban, telefonnummer, private_emailadresse):
        """
        legt einen neuen Mitarbeiter für den Mandanten in der Datenbank an
        :param vorname:
        :param nachname:
        :param geschlecht:
        :param geburtsdatum:
        :param eintrittsdatum:
        :param steuernummer:
        :param sozialversicherungsnummer:
        :param iban:
        :param telefonnummer:
        :param private_emailadresse:
        :return:
        """
        pass


# Verbindung zur PostgreSQL-Datenbank herstellen
conn = psycopg2.connect(
    host="localhost",
    database="postgres",
    user="postgres",
    password="@Postgres123"
)

testfirma = Mandant('testfirma', conn)

# Verbindung zur Datenbank schließen
conn.close()



