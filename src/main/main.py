from src.main.Mandant import Mandant

testfirma = Mandant("testu")
testfirma.nutzer_anlegen("M100001", "Erika", "Musterfrau")

# personenbezogene Daten eingeben
testfirma.get_nutzer("M100001").insert_geschlecht('1 Geschlecht.xlsx')

testfirma.get_nutzer("M100001").insert_mitarbeitertyp('2 Mitarbeitertyp.xlsx')
testfirma.get_nutzer("M100001").insert_steuerklasse('3 Steuerklasse.xlsx')
testfirma.get_nutzer("M100001").insert_abteilung('4.1 Abteilung.xlsx')
testfirma.get_nutzer("M100001").insert_abteilung('4.2 Abteilung.xlsx')
testfirma.get_nutzer("M100001").insert_jobtitel('5 Jobtitel.xlsx')
testfirma.get_nutzer("M100001").insert_erfahrungsstufe('6 Erfahrungsstufe.xlsx')
testfirma.get_nutzer("M100001").insert_gesellschaft('7 Gesellschaft.xlsx')
testfirma.get_nutzer("M100001").insert_austrittsgrundkategorie('8 Austrittsgrundkategorie.xlsx')
testfirma.get_nutzer("M100001").insert_austrittsgrund('9 Austrittsgrund.xlsx')

# Krankenversicherungsdaten eingeben
testfirma.get_nutzer("M100001").insert_krankenversicherungsbeitraege('1 Krankenversicherungsbeitraege.xlsx')
testfirma.get_nutzer("M100001").insert_gesetzliche_krankenkasse('2 gesetzliche Krankenkasse.xlsx')
testfirma.get_nutzer("M100001").insert_private_krankenkasse('3 private Krankenkasse.xlsx')
testfirma.get_nutzer("M100001").insert_gemeldete_krankenkasse('4 gemeldete Krankenkasse.xlsx')
testfirma.get_nutzer("M100001").insert_anzahl_kinder_an_pv_beitrag('5 Anzahl Kinder Arbeitnehmer PV-Beitrag.xlsx')
testfirma.get_nutzer("M100001").insert_wohnhaft_sachsen_ag_pv_beitrag('6 wohnhaft Sachsen Arbeitgeber PV-Beitrag.xlsx')
testfirma.get_nutzer("M100001").insert_arbeitslosenversicherungsbeitraege('7 Arbeitslosenversicherungsbeitraege.xlsx')
testfirma.get_nutzer("M100001").insert_rentenversicherungsbeitraege('8 Rentenversicherungsbeitraege.xlsx')
testfirma.get_nutzer("M100001").insert_minijobbeitraege('9 Minijobbeitraege.xlsx')
testfirma.get_nutzer("M100001").insert_berufsgenossenschaft('10 Berufsgenossenschaft.xlsx')
testfirma.get_nutzer("M100001").insert_unfallversicherungsbeitrag('11 Unfallversicherungsbeitrag.xlsx')

# Entgeltdaten eingeben
testfirma.get_nutzer("M100001").insert_gewerkschaft('1 Gewerkschaft.xlsx')
testfirma.get_nutzer("M100001").insert_tarif('2 Tarif.xlsx')
testfirma.get_nutzer("M100001").insert_verguetungsbestandteil('3 Verguetungsbestandteil.xlsx')

# zentrale Funktion: neuen Mitarbeiter anlegen!
#testfirma.get_nutzer("M100001").insert_neuer_mitarbeiter('10.1 Mitarbeiter.xlsx')
testfirma.get_nutzer("M100001").insert_neuer_mitarbeiter('10.2 Mitarbeiter.xlsx')

# Entgeltbestandteil fuer aussertariflichen Mitarbeiter anlegen
testfirma.get_nutzer("M100001").insert_aussertariflicher_verguetungsbestandteil('11 aussertariflicher Verguetungsbestandteil.xlsx')

# Update personenbezogene Daten
testfirma.get_nutzer("M100001").update_adresse('1 Update Adresse.xlsx')
testfirma.get_nutzer("M100001").update_mitarbeiterentlassung('2 Update Mitarbeiterentlassung.xlsx')
testfirma.get_nutzer("M100001").update_erstelle_abteilungshierarchie('3 Update Abteilungshierarchie.xlsx')

# Update Sozialversicherungsdaten
testfirma.get_nutzer("M100001").update_krankenversicherungsbeitraege('1 Krankenversicherungsbeitraege.xlsx')

#select update_krankenversicherungsbeitraege(1, false, 7.8, 7.8, 80000, 82000.75,'2024-12-31', '2025-01-01');

# Delete Daten
#testfirma.get_nutzer("M100001").delete_mitarbeiterdaten('Personalnummer.xlsx')
#testfirma.get_nutzer("M100001").delete_mandantendaten()




