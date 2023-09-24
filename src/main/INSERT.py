import psycopg2

# Verbindung zur PostgreSQL-Datenbank herstellen
conn = psycopg2.connect(
    host="localhost",
    database="postgres",
    user="postgres",
    password="@Postgres123"
)

# Ein Cursor-Objekt erstellen
cur = conn.cursor()

# Parameter für die Erstellung eines neuen Mitarbeiters
p_vorname = 'Max'
p_nachname = 'Freudenberg'
p_geschlecht = 'maennlich'
p_geburtsdatum = '1992-12-12'
p_eintrittsdatum = '2023-11-01'
p_steuernummer = '11 111 111 111'
p_sozialversicherungsnummer = '00 121292 F 00'
p_iban = 'DE00 0000 0000 0000 0000 00'
p_telefonnummer = '0175 2572025'
p_private_emailadresse = 'maxfreudenberg@web.de'

# Stored Procedure aufrufen
cur.callproc('insert_neuer_mitarbeiter', (p_vorname,
                                          p_nachname,
                                          p_geschlecht,
                                          p_geburtsdatum,
                                          p_eintrittsdatum,
                                          p_steuernummer,
                                          p_sozialversicherungsnummer,
                                          p_iban,
                                          p_telefonnummer,
                                          p_private_emailadresse))

# Commit der Änderungen
conn.commit()

# Cursor schließen
cur.close()

# Verbindung zur Datenbank schließen
conn.close()