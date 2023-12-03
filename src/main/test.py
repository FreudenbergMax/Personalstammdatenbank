import pandas as pd

data = {'mandant_id_1': [1, 2, 3],
        'mandant_id_2': [4, 5, 6],
        'nicht_mandant_id': [7, 8, 9]}
df = pd.DataFrame(data)

mandant_column = next((col for col in df.columns if "mandant_id" in col), None)

# Liste aller Spalten, die 'mandant_id' enthalten, außer 'mandant_column'
mandant_columns_to_remove = [col for col in df.columns if "mandant_id" in col and col != mandant_column]

# DataFrame bereinigen
df_result = df.drop(columns=mandant_columns_to_remove)

# DataFrame anzeigen
print(df_result)

print(f"Mandantenspalte: {mandant_column}")

'''
# Behalte die erste Spalte und lösche die anderen
columns_to_keep = [df.columns[0]] + [col for col in df.columns if col not in mandant_columns]
df_result = df[columns_to_keep]

# DataFrame anzeigen
print(df_result)
'''