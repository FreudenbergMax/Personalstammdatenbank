from src.main.Mandant import Mandant

testfirma = Mandant("testu")
testfirma.nutzer_anlegen("M100001", "Erika", "Musterfrau")

# personenbezogene Daten eingeben
testfirma.get_nutzer("M100001").insert_geschlecht('insert personenbezogene Daten/1 Geschlecht.xlsx')

testfirma.get_nutzer("M100001").insert_mitarbeitertyp('insert personenbezogene Daten/2 Mitarbeitertyp.xlsx')
testfirma.get_nutzer("M100001").insert_steuerklasse('insert personenbezogene Daten/3 Steuerklasse.xlsx')
testfirma.get_nutzer("M100001").insert_abteilung('insert personenbezogene Daten/4.1 Abteilung.xlsx')
testfirma.get_nutzer("M100001").insert_abteilung('insert personenbezogene Daten/4.2 Abteilung.xlsx')
testfirma.get_nutzer("M100001").insert_jobtitel('insert personenbezogene Daten/5 Jobtitel.xlsx')
testfirma.get_nutzer("M100001").insert_erfahrungsstufe('insert personenbezogene Daten/6 Erfahrungsstufe.xlsx')
testfirma.get_nutzer("M100001").insert_gesellschaft('insert personenbezogene Daten/7 Gesellschaft.xlsx')
testfirma.get_nutzer("M100001").\
    insert_austrittsgrundkategorie('insert personenbezogene Daten/8 Austrittsgrundkategorie.xlsx')
testfirma.get_nutzer("M100001").insert_austrittsgrund('insert personenbezogene Daten/9 Austrittsgrund.xlsx')

# Krankenversicherungsdaten eingeben
testfirma.get_nutzer("M100001").\
    insert_krankenversicherungsbeitraege('insert Sozialversicherungsdaten/1 Krankenversicherungsbeitraege.xlsx')
testfirma.get_nutzer("M100001").\
    insert_gesetzliche_krankenkasse('insert Sozialversicherungsdaten/2 gesetzliche Krankenkasse.xlsx')
testfirma.get_nutzer("M100001").\
    insert_private_krankenkasse('insert Sozialversicherungsdaten/3 private Krankenkasse.xlsx')
testfirma.get_nutzer("M100001").\
    insert_gemeldete_krankenkasse('insert Sozialversicherungsdaten/4 gemeldete Krankenkasse.xlsx')
testfirma.get_nutzer("M100001").\
    insert_anzahl_kinder_an_pv_beitrag('insert Sozialversicherungsdaten/5 Anzahl Kinder Arbeitnehmer PV-Beitrag.xlsx')
testfirma.get_nutzer("M100001").\
    insert_arbeitsort_sachsen_ag_pv_beitrag('insert Sozialversicherungsdaten/6 wohnhaft Sachsen Arbeitgeber PV-Beitrag.xlsx')
testfirma.get_nutzer("M100001").\
    insert_arbeitslosenversicherungsbeitraege('insert Sozialversicherungsdaten/7 Arbeitslosenversicherungsbeitraege.xlsx')
testfirma.get_nutzer("M100001").\
    insert_rentenversicherungsbeitraege('insert Sozialversicherungsdaten/8 Rentenversicherungsbeitraege.xlsx')
testfirma.get_nutzer("M100001").\
    insert_minijobbeitraege('insert Sozialversicherungsdaten/9 Minijobbeitraege.xlsx')
testfirma.get_nutzer("M100001").\
    insert_berufsgenossenschaft('insert Sozialversicherungsdaten/10 Berufsgenossenschaft.xlsx')
testfirma.get_nutzer("M100001").\
    insert_unfallversicherungsbeitrag('insert Sozialversicherungsdaten/11 Unfallversicherungsbeitrag.xlsx')

# Entgeltdaten eingeben
testfirma.get_nutzer("M100001").insert_gewerkschaft('insert Entgeltdaten/1 Gewerkschaft.xlsx')
testfirma.get_nutzer("M100001").insert_tarif('insert Entgeltdaten/2 Tarif.xlsx')
testfirma.get_nutzer("M100001").insert_verguetungsbestandteil('insert Entgeltdaten/3 Verguetungsbestandteil.xlsx')

# zentrale Funktion: neuen Mitarbeiter anlegen!
testfirma.get_nutzer("M100001").insert_neuer_mitarbeiter('insert personenbezogene Daten/Mitarbeiter.xlsx')

# Entgeltbestandteil fuer aussertariflichen Mitarbeiter anlegen
testfirma.get_nutzer("M100001").\
    insert_aussertariflicher_verguetungsbestandteil('insert personenbezogene Daten/11 aussertariflicher Verguetungsbestandteil.xlsx')

# Update personenbezogene Daten
testfirma.get_nutzer("M100001").update_adresse('update personenbezogene Daten/1 Update Adresse.xlsx')
testfirma.get_nutzer("M100001").\
    update_mitarbeiterentlassung('update personenbezogene Daten/2 Update Mitarbeiterentlassung.xlsx')
testfirma.get_nutzer("M100001").\
    update_erstelle_abteilungshierarchie('update personenbezogene Daten/3 Update Abteilungshierarchie.xlsx')

# Update Sozialversicherungsdaten
testfirma.get_nutzer("M100001").\
    update_krankenversicherungsbeitraege('update Sozialversicherungsdaten/1 Krankenversicherungsbeitraege.xlsx')

# Delete Daten
testfirma.get_nutzer("M100001").delete_mitarbeiterdaten('delete personenbezogene Daten/Personalnummer.xlsx')
testfirma.get_nutzer("M100001").delete_mandantendaten()




