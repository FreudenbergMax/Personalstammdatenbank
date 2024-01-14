import psycopg2


def test_set_up():
    """
    Methode erstellt eine Verbindung zur Datenbank in einem Testschema. So können die
    Unit- und Integrationstests so ausgeführt werden, dass die Produktivdatenbank im Schema 'public' nicht manipuliert
    wird.
    """
    testschema = 'temp_test_schema'

    conn = psycopg2.connect(
        host="localhost",
        database="Personalstammdatenbank",
        user="postgres",
        password="@Postgres123",
        port=5432
    )

    cur = conn.cursor()

    # SQL-code in Python einlesen und anschließend ausführen
    setup_sql = f"create schema if not exists {testschema};\n\nset search_path to {testschema};\n\n"
    with open("../SQL-Code.sql") as file:
        setup_sql = setup_sql + file.read()

    cur.execute(setup_sql)
    conn.commit()

    # Cursor und Konnektor zu Datenbank schließen
    cur.close()
    conn.close()

    return testschema


def test_tear_down():
    """
    Methode entfernt das Testschema 'temp_test_schema' mit allen Daten, Tabellen und stored Procedures aus der
    Datenbank. Diese soll nur für die Unit-Tests aufgebaut werden. In der Praxis würden die Nutzer auf dem Schema
    'public' arbeiten.
    """
    conn = psycopg2.connect(
        host="localhost",
        database="Personalstammdatenbank",
        user="postgres",
        password="@Postgres123",
        port=5432
    )

    cur = conn.cursor()
    cur.execute(f"set role postgres;DROP SCHEMA temp_test_schema CASCADE")
    conn.commit()
    cur.close()
    conn.close()
