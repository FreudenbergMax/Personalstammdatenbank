import psycopg2


def test_set_up():
    """
    Methode erstellt eine Verbindung zur Datenbank in einem Testschema. So können die
    Unit- und Integrationstests so ausgeführt werden, dass die Produktivdatenbank nicht manipuliert wird
    :return: Connection zur Test-Datenbank
    """
    conn = psycopg2.connect(
        host="localhost",
        database="Personalstammdatenbank",
        user="postgres",
        password="@Postgres123",
        port=5432
    )

    cursor = conn.cursor()

    # SQL-code in Python einlesen und anschließend ausführen
    setup_sql = "create schema if not exists temp_test_schema;\n\nset search_path to temp_test_schema;\n\n"
    with open("SQL-Code.sql") as f:
        setup_sql = setup_sql + f.read()

    cursor.execute(setup_sql)
    conn.commit()

    return conn, cursor
