from src.main.Nutzer import Nutzer


class Mandant:

    def __init__(self, mandantenname, conn):

        if not isinstance(mandantenname, str):
            raise(TypeError("Der Name des Mandanten muss ein String sein."))

        if "postgres" in str.lower(mandantenname):
            raise(ValueError(f"Dieser Name ist nicht erlaubt: {mandantenname}."))

        if mandantenname == "":
            raise(ValueError(f"Der Name des Mandanten muss aus mindestens einem Zeichen bestehen."))

        if len(mandantenname) > 128:
            raise(ValueError(f"Der Name des Mandanten darf höchstens 128 Zeichen lang sein."
                             f"'{mandantenname}' besitzt {len(mandantenname)} Zeichen!"))

        self.mandantenname = mandantenname
        self.mandant_id = self._in_datenbank_anlegen(conn)
        #print("Mandant_ID:", self.mandant_id)
        self.liste_nutzer = []

    def _in_datenbank_anlegen(self, conn):
        """
        Methode ruft die Stored Procedure 'mandant_anlegen' auf, welche die Daten des Mandanten in der
        Personalstammdatenbank speichert.
        :param conn: Connection zur Personalstammdatenbank
        """
        mandant_insert_query = f"SELECT mandant_anlegen('{self.mandantenname}')"
        cur = conn.cursor()
        cur.execute(mandant_insert_query)

        mandant_id = cur.fetchone()[0]

        # Commit der Änderungen
        conn.commit()

        # Cursor schließen
        cur.close()

        return mandant_id

    def nutzer_anlegen(self, personalnummer, vorname, nachname, conn):
        """
        Da jeder Mandant mehrere Nutzer haben kann, werden alle Nutzer eines Mandanten hier erzeugt und in einer
        klasseneigenen Liste "liste_nutzer" gespeichert.
        :param personalnummer: des Nutzers
        :param vorname: Vorname des Nutzers
        :param nachname: Nachname des Nutzers
        :param conn: Connection zur Datenbank
        """
        nutzer = Nutzer(self.mandant_id, personalnummer, vorname, nachname, conn)
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

    def nutzer_entfernen(self, personalnummer, conn):
        """
        Funktion entfernt einen Nutzer.
        :param personalnummer: des Nutzers, der entfernt werden soll
        :param conn: Connection zur Datenbank
        """
        nutzer_entfernt = False

        for i in range(len(self.liste_nutzer)):
            if self.liste_nutzer[i].get_personalnummer() == personalnummer:

                # Nutzer aus Datenbank entfernen
                nutzer_delete_query = f"SELECT nutzer_entfernen({self.mandant_id}, '{personalnummer}')"

                cur = conn.cursor()
                cur.execute(nutzer_delete_query)

                # Commit der Änderungen
                conn.commit()

                # Cursor schließen
                cur.close()

                #conn.close()

                # Nutzer aus Liste 'liste_nutzer' des Mandant-Objekt entfernen
                self.liste_nutzer.remove(self.liste_nutzer[i])

                nutzer_entfernt = True
                print(f"Nutzer {personalnummer} wurde entfernt!")

        if not nutzer_entfernt:
            print(f"Nutzer {personalnummer} existiert nicht!")
