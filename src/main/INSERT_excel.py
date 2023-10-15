import psycopg2
import pandas as pd
import openpyxl

mitarbeiterdaten = "Max Mustermann.xlsx"
mandant = "testfirma"

df_ma_daten = pd.read_excel(f"Mitarbeiterdaten/{mitarbeiterdaten}", index_col='Daten')
liste_ma_daten = list(df_ma_daten.iloc[:, 0])
liste_ma_daten.insert(0, mandant)
print(type(liste_ma_daten))


# Verbindung zur PostgreSQL-Datenbank herstellen
conn = psycopg2.connect(
    host="localhost",
    database="postgres",
    user="postgres",
    password="@Postgres123"
)

# Ein Cursor-Objekt erstellen
cur = conn.cursor()

# Stored Procedure aufrufen
cur.callproc('insert_neuer_mitarbeiter', liste_ma_daten)

# Commit der Änderungen
conn.commit()

# Cursor schließen
cur.close()

# Verbindung zur Datenbank schließen
conn.close()
