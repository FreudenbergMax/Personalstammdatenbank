"""
Für jede Tabelle wird eine py-Testdatei erzeugt. Folgende Tests müssen mindestens für jede Tabelle durchgeführt werden:
- insert-Befehl wird erfolgreich ausgeführt, sofern übergegebener Datensatz noch nicht existiert
- insert-Befehl fügt keine Daten ein, wenn die einzufügenden Daten bereits existieren
- delete: löschen aller Daten eines Mandanten wird erfolgreich ausgeführt
- delete: löschen aller Daten eines Mitarbeiters wird erfolgreich ausgeführt
- RLS funktioniert --> Mandant A sieht keine Daten von Mandant B

Bei Assoziationen kommen noch hinzu:
- insert Fehlermeldung soll erscheinen, wenn zwei datensätze denselben primary key (zusammengesetzt aus 'Mitarbeiter_ID'
    und 'Datum_Bis') haben
- update-Befehl wird ausgeführt
    - "Datum_bis" wird von '9999-12-31' auf das letzte Datum umgestellt, wo der Eintrag gültig ist
    - die Änderung (= neuer Datensatz) wird erfolgreich eingefügt
    - Die Fremdschlüssel stimmen
"""

