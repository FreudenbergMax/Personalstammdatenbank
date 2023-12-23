from src.main.Mandant import Mandant

testfirma = Mandant("testu")
testfirma.nutzer_anlegen("M100001", "Erika", "Musterfrau")

# personenbezogene Daten eingeben
testfirma.get_nutzer("M100001").insert_geschlecht('1 Geschlecht.xlsx')
testfirma.get_nutzer("M100001").insert_mitarbeitertyp('2 Mitarbeitertyp.xlsx')
testfirma.get_nutzer("M100001").insert_steuerklasse('3 Steuerklasse.xlsx')
testfirma.get_nutzer("M100001").insert_abteilung('4 Abteilung.xlsx')
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







#testfirma.get_nutzer("M100001").insert_neuer_mitarbeiter('Neuanlage Mitarbeiter1.xlsx')
#testfirma.get_nutzer("M100001").update_adresse('Update Adresse.xlsx')
#testfirma.get_nutzer("M100001").delete_mandantendaten()
#testfirma.get_nutzer("M100001").delete_mitarbeiterdaten('Delete Mitarbeiterdaten.xlsx')

'''
testfirma.get_nutzer("M100001").insert_neuer_mitarbeiter('Erika Musterfrau.xlsx')

testu = Mandant("testu")
testu.nutzer_anlegen("P666", "Erik", "Testu")
testu.get_nutzer("P666").insert_neuer_mitarbeiter('Erik Testu.xlsx')

print("Mandant-ID testu:", testu.get_mandant_id())
print(testu.get_nutzer("P666").abfrage_ausfuehren("SELECT "
                                            "mitarbeiter.mandant_id, "
                                            "mitarbeiter.personalnummer, "
                                            "Vorname,"
                                            "Nachname,"
                                            "Gesellschaft "
                                            "FROM "
                                            "mitarbeiter "
                                            "INNER JOIN in_gesellschaft ON mitarbeiter.mitarbeiter_id = in_gesellschaft.mitarbeiter_id "
                                            "INNER JOIN gesellschaften ON gesellschaften.gesellschaft_id = in_gesellschaft.gesellschaft_id;"))

print("Mandant-ID testfirma:", testfirma.get_mandant_id())
print(testfirma.get_nutzer("M100001").abfrage_ausfuehren("SELECT "
                                                   "mitarbeiter.mandant_id, "
                                                   "mitarbeiter.personalnummer, "
                                                   "Vorname,"
                                                   "Nachname,"
                                                   "Gesellschaft "
                                                   "FROM "
                                                   "mitarbeiter "
                                                   "INNER JOIN in_gesellschaft ON mitarbeiter.mitarbeiter_id = in_gesellschaft.mitarbeiter_id "
                                                   "INNER JOIN gesellschaften ON gesellschaften.gesellschaft_id = in_gesellschaft.gesellschaft_id;"))
'''




