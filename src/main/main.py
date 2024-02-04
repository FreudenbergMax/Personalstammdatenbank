from src.main.Login import Login

"""
Diese main-Funktion dient nur als Beispiel, wie man Daten in die Datenbank eintragen kann.
"""

# Erstellung eines Mandanten, Administrator und Nutzer
login = Login()
login.registriere_mandant_und_admin('Testfirma', 'mandantenpw', 'mandantenpw', 'M100000', 'Otto', 'Normalverbraucher',
                                    'adminpw', 'adminpw')
admin = login.login_admin('Testfirma', 'mandantenpw', 'M100000', 'adminpw')
admin.nutzer_anlegen("M100001", "Erika", "Musterfrau", "nutzerpw", "nutzerpw")

nutzer = login.login_nutzer('Testfirma', 'mandantenpw', "M100001", "nutzerpw")


insert_personenbezogene_daten = "1 insert personenbezogene Daten"
insert_sozialversicherungsdaten = "2 insert Sozialversicherungsdaten"
insert_tarifliche_entgeltdaten = "3 insert tarifliche Entgeltdaten"
neuen_mitarbeiter_anlegen = "4 neuen Mitarbeiter anlegen"


# personenbezogene Daten eingeben
nutzer.insert_geschlecht(f'{insert_personenbezogene_daten}/1 Geschlecht.xlsx')
nutzer.insert_mitarbeitertyp(f'{insert_personenbezogene_daten}/2 Mitarbeitertyp.xlsx')
nutzer.insert_steuerklasse(f'{insert_personenbezogene_daten}/3 Steuerklasse.xlsx')
nutzer.insert_abteilung(f'{insert_personenbezogene_daten}/4 Abteilung.xlsx')
nutzer.insert_jobtitel(f'{insert_personenbezogene_daten}/5 Jobtitel.xlsx')
nutzer.insert_erfahrungsstufe(f'{insert_personenbezogene_daten}/6 Erfahrungsstufe.xlsx')
nutzer.insert_gesellschaft(f'{insert_personenbezogene_daten}/7 Gesellschaft.xlsx')
nutzer.insert_austrittsgrundkategorie(f'{insert_personenbezogene_daten}/8 Austrittsgrundkategorie.xlsx')
nutzer.insert_austrittsgrund(f'{insert_personenbezogene_daten}/9 Austrittsgrund.xlsx')

# Krankenversicherungsdaten eingeben
nutzer.insert_krankenversicherungsbeitraege(f'{insert_sozialversicherungsdaten}/1 Krankenversicherungsbeitraege.xlsx')
nutzer.insert_gesetzliche_krankenkasse(f'{insert_sozialversicherungsdaten}/2 gesetzliche Krankenkasse.xlsx')
nutzer.insert_private_krankenkasse(f'{insert_sozialversicherungsdaten}/3 private Krankenkasse.xlsx')
nutzer.insert_gemeldete_krankenkasse(f'{insert_sozialversicherungsdaten}/4 gemeldete Krankenkasse.xlsx')
nutzer.insert_anzahl_kinder_an_pv_beitrag(f'{insert_sozialversicherungsdaten}/5 Anzahl Kinder Arbeitnehmer PV-Beitrag.xlsx')
nutzer.insert_arbeitsort_sachsen_ag_pv_beitrag(f'{insert_sozialversicherungsdaten}/6 Arbeitsort Sachsen Arbeitgeber PV-Beitrag.xlsx')
nutzer.insert_arbeitslosenversicherungsbeitraege(f'{insert_sozialversicherungsdaten}/7 Arbeitslosenversicherungsbeitraege.xlsx')
nutzer.insert_rentenversicherungsbeitraege(f'{insert_sozialversicherungsdaten}/8 Rentenversicherungsbeitraege.xlsx')
nutzer.insert_minijobbeitraege(f'{insert_sozialversicherungsdaten}/9 Minijobbeitraege.xlsx')
nutzer.insert_berufsgenossenschaft(f'{insert_sozialversicherungsdaten}/10 Berufsgenossenschaft.xlsx')
nutzer.insert_unfallversicherungsbeitrag(f'{insert_sozialversicherungsdaten}/11 Unfallversicherungsbeitrag.xlsx')

# Entgeltdaten eingeben
nutzer.insert_gewerkschaft(f'{insert_tarifliche_entgeltdaten}/1 Gewerkschaft.xlsx')
nutzer.insert_tarif(f'{insert_tarifliche_entgeltdaten}/2 Tarif.xlsx')
nutzer.insert_verguetungsbestandteil(f'{insert_tarifliche_entgeltdaten}/3 Verguetungsbestandteil.xlsx')
nutzer.insert_tarifliches_verguetungsbestandteil(f'{insert_tarifliche_entgeltdaten}/4 tariflicher Verguetungsbestandteil.xlsx')

# zentrale Funktion: neuen Mitarbeiter anlegen!
nutzer.insert_neuer_mitarbeiter(f'{neuen_mitarbeiter_anlegen}/1 Mitarbeiter.xlsx')

# Entgeltbestandteil fuer aussertariflichen Mitarbeiter anlegen
nutzer.insert_aussertarifliches_verguetungsbestandteil(f'{neuen_mitarbeiter_anlegen}/2 aussertariflicher Verguetungsbestandteil.xlsx')

# Update personenbezogene Daten
nutzer.update_adresse('update personenbezogene Daten/1 Update Adresse.xlsx')
nutzer.update_mitarbeiterentlassung('update personenbezogene Daten/2 Update Mitarbeiterentlassung.xlsx')
nutzer.update_erstelle_abteilungshierarchie('update personenbezogene Daten/3 Update Abteilungshierarchie.xlsx')

# Update Sozialversicherungsdaten
nutzer.update_krankenversicherungsbeitraege('update Sozialversicherungsdaten/1 Krankenversicherungsbeitraege.xlsx')






