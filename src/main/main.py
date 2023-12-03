from src.main.Mandant import Mandant

testfirma = Mandant("testfirma")
testfirma.nutzer_anlegen("M100001", "Max", "Mustermann")
testfirma.get_nutzer("M100001").insert_neuer_mitarbeiter('Max Mustermann.xlsx')
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





