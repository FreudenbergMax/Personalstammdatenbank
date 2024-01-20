from src.main.Mandant import Mandant

insert_personenbezogene_daten = "1 insert personenbezogene Daten"
insert_sozialversicherungsdaten = "2 insert Sozialversicherungsdaten"
insert_tarifliche_entgeltdaten = "3 insert tarifliche Entgeltdaten"
neuen_mitarbeiter_anlegen = "4 neuen Mitarbeiter anlegen"

# Mandant und Nutzer anlegen
testfirma = Mandant("testu")
testfirma.nutzer_anlegen("M100001", "Erika", "Musterfrau")
"""
# personenbezogene Daten eingeben
testfirma.get_nutzer("M100001").insert_geschlecht(f'{insert_personenbezogene_daten}/1 Geschlecht.xlsx')
testfirma.get_nutzer("M100001").insert_mitarbeitertyp(f'{insert_personenbezogene_daten}/2 Mitarbeitertyp.xlsx')
testfirma.get_nutzer("M100001").insert_steuerklasse(f'{insert_personenbezogene_daten}/3 Steuerklasse.xlsx')
testfirma.get_nutzer("M100001").insert_abteilung(f'{insert_personenbezogene_daten}/4 Abteilung.xlsx')
testfirma.get_nutzer("M100001").insert_jobtitel(f'{insert_personenbezogene_daten}/5 Jobtitel.xlsx')
testfirma.get_nutzer("M100001").insert_erfahrungsstufe(f'{insert_personenbezogene_daten}/6 Erfahrungsstufe.xlsx')
testfirma.get_nutzer("M100001").insert_gesellschaft(f'{insert_personenbezogene_daten}/7 Gesellschaft.xlsx')
testfirma.get_nutzer("M100001").insert_austrittsgrundkategorie(
    f'{insert_personenbezogene_daten}/8 Austrittsgrundkategorie.xlsx')
testfirma.get_nutzer("M100001").insert_austrittsgrund(f'{insert_personenbezogene_daten}/9 Austrittsgrund.xlsx')

# Krankenversicherungsdaten eingeben
testfirma.get_nutzer("M100001").insert_krankenversicherungsbeitraege(
    f'{insert_sozialversicherungsdaten}/1 Krankenversicherungsbeitraege.xlsx')
testfirma.get_nutzer("M100001").insert_gesetzliche_krankenkasse(
    f'{insert_sozialversicherungsdaten}/2 gesetzliche Krankenkasse.xlsx')
testfirma.get_nutzer("M100001").insert_private_krankenkasse(
    f'{insert_sozialversicherungsdaten}/3 private Krankenkasse.xlsx')
testfirma.get_nutzer("M100001").insert_gemeldete_krankenkasse(
    f'{insert_sozialversicherungsdaten}/4 gemeldete Krankenkasse.xlsx')
testfirma.get_nutzer("M100001").insert_anzahl_kinder_an_pv_beitrag(
    f'{insert_sozialversicherungsdaten}/5 Anzahl Kinder Arbeitnehmer PV-Beitrag.xlsx')
testfirma.get_nutzer("M100001").insert_arbeitsort_sachsen_ag_pv_beitrag(
    f'{insert_sozialversicherungsdaten}/6 Arbeitsort Sachsen Arbeitgeber PV-Beitrag.xlsx')
testfirma.get_nutzer("M100001").insert_arbeitslosenversicherungsbeitraege(
    f'{insert_sozialversicherungsdaten}/7 Arbeitslosenversicherungsbeitraege.xlsx')
testfirma.get_nutzer("M100001").insert_rentenversicherungsbeitraege(
    f'{insert_sozialversicherungsdaten}/8 Rentenversicherungsbeitraege.xlsx')
testfirma.get_nutzer("M100001").insert_minijobbeitraege(
    f'{insert_sozialversicherungsdaten}/9 Minijobbeitraege.xlsx')
testfirma.get_nutzer("M100001").insert_berufsgenossenschaft(
    f'{insert_sozialversicherungsdaten}/10 Berufsgenossenschaft.xlsx')
testfirma.get_nutzer("M100001").insert_unfallversicherungsbeitrag(
    f'{insert_sozialversicherungsdaten}/11 Unfallversicherungsbeitrag.xlsx')

# Entgeltdaten eingeben
testfirma.get_nutzer("M100001").insert_gewerkschaft(f'{insert_tarifliche_entgeltdaten}/1 Gewerkschaft.xlsx')
testfirma.get_nutzer("M100001").insert_tarif(f'{insert_tarifliche_entgeltdaten}/2 Tarif.xlsx')
testfirma.get_nutzer("M100001").insert_verguetungsbestandteil(
    f'{insert_tarifliche_entgeltdaten}/3 Verguetungsbestandteil.xlsx')

# zentrale Funktion: neuen Mitarbeiter anlegen!
testfirma.get_nutzer("M100001").insert_neuer_mitarbeiter(f'{neuen_mitarbeiter_anlegen}/1 Mitarbeiter.xlsx')

# Entgeltbestandteil fuer aussertariflichen Mitarbeiter anlegen
#testfirma.get_nutzer("M100001").\
#    insert_aussertarifliches_verguetungsbestandteil(f'{neuen_mitarbeiter_anlegen}/2 aussertariflicher Verguetungsbestandteil.xlsx')

# Update personenbezogene Daten
testfirma.get_nutzer("M100001").update_adresse('update personenbezogene Daten/1 Update Adresse.xlsx')
testfirma.get_nutzer("M100001").\
    update_mitarbeiterentlassung('update personenbezogene Daten/2 Update Mitarbeiterentlassung.xlsx')
testfirma.get_nutzer("M100001").\
    update_erstelle_abteilungshierarchie('update personenbezogene Daten/3 Update Abteilungshierarchie.xlsx')

# Update Sozialversicherungsdaten
testfirma.get_nutzer("M100001").\
    update_krankenversicherungsbeitraege('update Sozialversicherungsdaten/1 Krankenversicherungsbeitraege.xlsx')
"""
# Delete Daten
testfirma.get_nutzer("M100001").delete_mitarbeiterdaten('delete personenbezogene Daten/Personalnummer.xlsx')
#testfirma.get_nutzer("M100001").delete_mandantendaten()




