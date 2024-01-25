def insert_austrittsgrund(self, neuanlage_austrittsgrund):
    """
    Diese Methode uebertraegt eine Austrittsgrund wie bspw. 'Umsatzrueckgang' in die Datenbank (im Rahmen
    der Bachelorarbeit dargestellt durch eine Excel-Datei), in dem die Stored Procedure 'insert_austrittsgruende'
    aufgerufen wird.
    :param neuanlage_austrittsgrund: Name der Excel-Datei, dessen Daten in die Datenbank eingetragen werden sollen.
    :param schema: enthaelt das Schema, welches angesprochen werden soll
    """
    # Import der Daten aus der Excel-Datei in das Pandas-Dataframe und Uebertragung in Liste "daten"
    daten = self._import_excel_daten(neuanlage_austrittsgrund)

    # Daten aus importierter Excel-Tabelle '9 Austrittsgrund.xlsx' pruefen
    austrittsgrund = self._existenz_str_daten_feststellen(daten[0], 'Austrittsgrund', 16, True)
    austrittsgrundkategorie = self._existenz_str_daten_feststellen(daten[1], 'Austrittsgrundkategorie', 16, True)

    export_daten = [self.mandant_id, austrittsgrund, austrittsgrundkategorie]
    self._export_zu_db('insert_austrittsgrund(%s,%s,%s)', export_daten)

