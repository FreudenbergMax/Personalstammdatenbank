import psycopg2
import pandas as pd
import openpyxl


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

    def insert_neuer_mitarbeiter(self, mitarbeiterdaten, conn):
        """
        Diese Methode überträgt die eingetragenen Mitarbeiterdaten (im Rahmen der Bachelorarbeit
        dargestellt durch eine Excel-Datei) in die Datenbank, in dem der Stored Procedure
        'insert_neuer_mitarbeiter' aufgerufen wird.
        :param mitarbeiterdaten: Name der Excel-Datei, dessen Mitarbeiterdaten in die Datenbank
        eingetragen werden sollen.
        :param conn:
        :return:
        """

        # Erstellung der Daten wird noch automatisiert
        mandant = self.mandantenname

        # Import der Daten aus der Excel-Datei in das Pandas-Dataframe und Übertrag in Liste "liste_ma_daten"
        df_ma_daten = pd.read_excel(f"Mitarbeiterdaten/{mitarbeiterdaten}", index_col='Daten')
        liste_ma_daten = list(df_ma_daten.iloc[:, 0])
        liste_ma_daten.insert(0, mandant)

        # Ein Cursor-Objekt erstellen
        cur = conn.cursor()

        # Stored Procedure aufrufen
        cur.callproc('insert_neuer_mitarbeiter', liste_ma_daten)

        # Commit der Änderungen
        conn.commit()

        # Cursor schließen
        cur.close()


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



