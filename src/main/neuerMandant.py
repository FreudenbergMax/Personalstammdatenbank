import psycopg2


def neuer_mandant(conn, p_mandant, p_adresse):

    # Ein Cursor-Objekt erstellen
    cur = conn.cursor()

    # user erstellen
    sql_createUser = f"create user {p_mandant}"

    # user der Mandantengruppe hinzufügen
    sql_gruppeHinzufuegen = f"alter group mandantengruppe add user {p_mandant}"

    # SQL-Abfrage ausführen
    cur.execute(sql_createUser)

    # Stored Procedure aufrufen
    cur.callproc('anlage_neuermandant', (p_mandant, p_adresse))

    # Änderungen committen
    conn.commit()

