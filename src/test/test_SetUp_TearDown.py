from src.main.Datenbankverbindung import datenbankbverbindung_aufbauen


def test_set_up():
    """
    Methode erstellt eine Verbindung zur Datenbank in einem Testschema. So koennen die
    Unit- und Integrationstests so ausgefuehrt werden, dass die Produktivdatenbank im Schema 'public' nicht manipuliert
    wird.
    """
    testschema = 'temp_test_schema'

    # SQL-Code erstellen, mit dem das Testschema erstellt werden kann
    erstelle_schema = f"create schema if not exists {testschema};\n" \
                      f"set search_path to {testschema};\n"

    erstelle_tenant_user = "create role tenant_user;\n"

    berechtige_tenant_user_temp_test_schema = f"grant usage on schema {testschema} to tenant_user;\n" \
                                              f"alter default privileges in schema {testschema} grant select, " \
                                              f"insert, update, delete on tables to tenant_user;\n" \
                                              f"alter default privileges in schema {testschema} grant usage on " \
                                              f"sequences to tenant_user;"

    conn = datenbankbverbindung_aufbauen()

    cur = conn.cursor()

    # Auslesen, ob die Rolle 'tenant_user' bereits existiert...
    cur.execute("select rolname from pg_roles where rolname = 'tenant_user'")

    with open("../2 erstelle Tabellen und Stored Procedures.sql") as file:
        # ... falls Rolle 'tenant_user' nicht vorhanden, dann neben Testschema auch 'tenant_user' erstellen ...
        if cur.fetchone() is None:
            setup_testschema = erstelle_schema + \
                               erstelle_tenant_user + \
                               berechtige_tenant_user_temp_test_schema + \
                               file.read()
            cur.execute(setup_testschema)
        # ... falls ja, dann Testschema erstellen, ohne dass die Rolle 'tenant_user' erstellt wird
        else:
            setup_testschema = erstelle_schema + \
                               berechtige_tenant_user_temp_test_schema + \
                               file.read()
            cur.execute(setup_testschema)

    conn.commit()

    # Cursor und Konnektor zu Datenbank schliessen
    cur.close()
    conn.close()

    return testschema


def test_tear_down():
    """
    Methode entfernt das Testschema 'temp_test_schema' mit allen Daten, Tabellen und stored Procedures aus der
    Datenbank. Diese soll nur fuer die Unit-Tests aufgebaut werden. In der Praxis wuerden die Nutzer auf dem Schema
    'public' arbeiten.
    """
    conn = datenbankbverbindung_aufbauen()

    cur = conn.cursor()
    cur.execute(f"set role postgres;"
                f"DROP SCHEMA temp_test_schema CASCADE;")
    conn.commit()
    cur.close()
    conn.close()
