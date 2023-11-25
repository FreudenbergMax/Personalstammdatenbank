from datetime import datetime
import pandas as pd
'''
def datenexistenz_feststellen(daten):
    """
    Funktion stellt fest, ob Daten vorliegen oder nicht
    :param daten: wird untersucht, ob Daten darin enthalten sind
    :return: Falls Parameter 'daten' keine Daten enthält, wird None zurückgegeben, sonst Daten
    """
    if daten == '':
        daten = None

    return daten


daten = ''
daten = datenexistenz_feststellen(daten)

print(daten)
print(type(daten))

daten = 'hallo'
daten = str(datenexistenz_feststellen(daten))

print(daten)
print(type(daten))

daten = 5
daten = str(datenexistenz_feststellen(daten))

print(daten)
print(type(daten))

daten = '12.12.1992'
daten = datetime.strptime(datenexistenz_feststellen(daten), '%d.%m.%Y').date()

print(daten)
print(type(daten))
'''

df_ma_daten = pd.read_excel(f"Mitarbeiterdaten/Max Mustermann.xlsx", index_col='Daten', na_filter=False)
liste_ma_daten = list(df_ma_daten.iloc[:, 0])
print(liste_ma_daten)
