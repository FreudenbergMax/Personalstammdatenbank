from src.main.Mandant import Mandant

testfirma = Mandant("testu")
testfirma.nutzer_anlegen("M100001", "Erika", "Musterfrau")
testfirma.get_nutzer("M100001").insert_neuer_mitarbeiter('Neuanlage Mitarbeiter1.xlsx')
testfirma.get_nutzer("M100001").insert_neuer_mitarbeiter('Neuanlage Mitarbeiter2.xlsx')
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




