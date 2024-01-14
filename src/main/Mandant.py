import psycopg2
from src.main.Nutzer import Nutzer


class Mandant:

    def __init__(self, mandantenname, schema='public'):

        if not isinstance(mandantenname, str):
            raise(TypeError("Der Name des Mandanten muss ein String sein."))

        if "postgres" in str.lower(mandantenname):
            raise(ValueError(f"Dieser Name ist nicht erlaubt: {mandantenname}."))

        if mandantenname == "":
            raise(ValueError(f"Der Name des Mandanten muss aus mindestens einem Zeichen bestehen."))

        if len(mandantenname) > 128:
            raise(ValueError(f"Der Name des Mandanten darf höchstens 128 Zeichen lang sein."
                             f"'{mandantenname}' besitzt {len(mandantenname)} Zeichen!"))

        if schema != 'public' and schema != 'temp_test_schema':
            raise (ValueError("Diese Bezeichnung für ein Schema ist nicht erlaubt!"))

        self.mandantenname = mandantenname
        self.schema = schema
        self.mandant_id = self._in_datenbank_anlegen()
        self.liste_nutzer = []

    def get_mandant_id(self):
        """
        Standard-Getter-Methode für die Objektvariable 'mandant_id'
        :return: mandant_id
        """
        return self.mandant_id

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

    def _in_datenbank_anlegen(self):
        """
        Methode ruft die Stored Procedure 'mandant_anlegen' auf, welche die Daten des Mandanten in der
        Personalstammdatenbank speichert.
        """
        conn = self._datenbankbverbindung_aufbauen()

        mandant_insert_query = f"set search_path to {self.schema};SELECT mandant_anlegen('{self.mandantenname}')"
        cur = conn.cursor()
        cur.execute(mandant_insert_query)

        # Commit der Änderungen
        conn.commit()

        mandant_id = cur.fetchone()[0]

        # Cursor und Konnektor zu Datenbank schließen
        cur.close()
        conn.close()

        return mandant_id

    def nutzer_anlegen(self, personalnummer, vorname, nachname, schema='public'):
        """
        Da jeder Mandant mehrere Nutzer haben kann, werden alle Nutzer eines Mandanten hier erzeugt und in einer
        klasseneigenen Liste "liste_nutzer" gespeichert.
        :param personalnummer: des Nutzers
        :param vorname: Vorname des Nutzers
        :param nachname: Nachname des Nutzers
        :param schema: Datenbankschema, das verwendet werden soll
        """
        nutzer = Nutzer(self.mandant_id, personalnummer, vorname, nachname, schema)
        self.liste_nutzer.append(nutzer)
        print("Nutzer", self.liste_nutzer[len(self.liste_nutzer)-1].get_vorname(),
              self.liste_nutzer[len(self.liste_nutzer)-1].get_nachname(), "angelegt.")

    def get_nutzer(self, personalnummer):
        """
        Funktion sucht den angefragten Nutzer raus, mit dem dann Operationen auf der Datenbank durchgeführt werden
        können.
        :param personalnummer: des Nutzers
        :return: Nutzer-Objekt, der auf der Datenbank operieren soll
        """
        gesuchter_nutzer = None

        for i in range(len(self.liste_nutzer)):
            if self.liste_nutzer[i].get_personalnummer() == personalnummer:
                gesuchter_nutzer = self.liste_nutzer[i]

        if gesuchter_nutzer is None:
            raise ValueError(f"Nutzer mit Personalnummer {personalnummer} nicht vorhanden!")
        else:
            return gesuchter_nutzer

    def nutzer_entfernen(self, personalnummer):
        """
        Funktion entfernt einen Nutzer.
        :param personalnummer: des Nutzers, der entfernt werden soll
        """
        conn = self._datenbankbverbindung_aufbauen()

        nutzer_entfernt = False

        for i in range(len(self.liste_nutzer)):
            if self.liste_nutzer[i].get_personalnummer() == personalnummer:

                # Nutzer aus Datenbank entfernen
                nutzer_delete_query = f"set search_path to {self.schema};" \
                                      f"CALL nutzer_entfernen({self.mandant_id}, '{personalnummer}')"

                cur = conn.cursor()
                cur.execute(nutzer_delete_query)

                # Commit der Änderungen
                conn.commit()

                # Cursor und Konnektor zu Datenbank schließen
                cur.close()
                conn.close()

                # Nutzer aus Liste 'liste_nutzer' des Mandant-Objekt entfernen
                self.liste_nutzer.remove(self.liste_nutzer[i])

                nutzer_entfernt = True
                print(f"Nutzer {personalnummer} wurde entfernt!")

        if not nutzer_entfernt:
            print(f"Nutzer {personalnummer} existiert nicht!")
