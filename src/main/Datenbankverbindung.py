import psycopg2


def datenbankbverbindung_aufbauen():
    """
    Baut eine Connection zur Datenbank auf.
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
