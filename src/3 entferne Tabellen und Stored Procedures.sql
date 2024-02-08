set role postgres;

-- Erstellung der Datenbankstruktur
drop table if exists wohnt_in;
drop table if exists Strassenbezeichnungen;
drop table if exists Postleitzahlen;
drop table if exists Staedte;
drop table if exists Regionen;
drop table if exists Laender;

drop table if exists hat_Geschlecht;
drop table if exists Geschlechter;

drop table if exists ist_mitarbeitertyp;
drop table if exists Mitarbeitertypen;

drop table if exists in_Steuerklasse;
drop table if exists Steuerklassen;

drop table if exists arbeitet_x_Wochenstunden;
drop table if exists Wochenarbeitsstunden;

drop table if exists eingesetzt_in;
drop table if exists Abteilungen;

drop table if exists hat_Jobtitel;
drop table if exists Jobtitel;
drop table if exists Erfahrungsstufen;

drop table if exists Unfallversicherungsbeitraege;
drop table if exists Berufsgenossenschaften;

drop table if exists in_Unternehmen;
drop table if exists Unternehmen;

drop table if exists hat_Tarif;
drop table if exists hat_Verguetungsbestandteil_Tarif;
drop table if exists Tarife;
drop table if exists Gewerkschaften;
drop table if exists hat_Verguetungsbestandteil_AT;
drop table if exists Verguetungsbestandteile;
drop table if exists Aussertarifliche;

drop table if exists hat_Privatkrankenkasse;
drop table if exists hat_Umlagen_privat;
drop table if exists Privatkrankenkassen;

drop table if exists hat_GKV_Beitraege;
drop table if exists hat_gesetzliche_Krankenversicherung;
drop table if exists Krankenversicherungen;
drop table if exists GKV_Beitraege;

drop table if exists ist_in_GKV;
drop table if exists hat_GKV_Zusatzbeitrag;
drop table if exists GKV_Zusatzbeitraege;
drop table if exists hat_Umlagen_gesetzlich;
drop table if exists gesetzliche_Krankenkassen;

drop table if exists hat_Umlagen_anderweitig;
drop table if exists ist_anderweitig_versichert;
drop table if exists gemeldete_Krankenkassen;
drop table if exists Umlagen;

drop table if exists hat_x_Kinder_unter_25;
drop table if exists hat_gesetzlichen_AN_PV_Beitragssatz;
drop table if exists Anzahl_Kinder_unter_25;
drop table if exists AN_Pflegeversicherungsbeitraege_gesetzlich;

drop table if exists hat_gesetzlichen_AG_PV_Beitragssatz;
drop table if exists arbeitet_in_sachsen;
drop table if exists arbeitsort_sachsen;
drop table if exists AG_Pflegeversicherungsbeitraege_gesetzlich;

drop table if exists hat_gesetzliche_Arbeitslosenversicherung;
drop table if exists hat_AV_Beitraege;
drop table if exists Arbeitslosenversicherungsbeitraege;
drop table if exists Arbeitslosenversicherungen;

drop table if exists hat_gesetzliche_Rentenversicherung;
drop table if exists hat_RV_Beitraege;
drop table if exists Rentenversicherungsbeitraege;
drop table if exists Rentenversicherungen;

drop table if exists ist_Minijobber;
drop table if exists hat_Pauschalabgaben;
drop table if exists Minijobs;
drop table if exists Pauschalabgaben;

drop table if exists mitarbeiter;
drop table if exists Austrittsgruende;
drop table if exists Kategorien_Austrittsgruende;
drop table if exists Nutzer;
drop table if exists Administratoren;
drop table if exists Mandanten;

-- Loeschung der Stored Procedures fuer Use Case "Mandant- und Administrator-Account erstellen"
drop function if exists mandant_anlegen(varchar(128), varchar(128));
drop function if exists mandantenpasswort_pruefen(integer, varchar(128));
drop function if exists administrator_anlegen(integer, varchar(32), varchar(64), varchar(64), varchar(128));
drop function if exists adminpasswort_pruefen(integer, varchar(32), varchar(128), varchar(128));

-- Loeschung der Stored Procedures fuer Use Case "Nutzer anlegen"
drop function if exists nutzer_anlegen(integer, varchar(32), varchar(64), varchar(64), varchar(128));
drop function if exists nutzerpasswort_pruefen( integer, varchar(32), varchar(128), varchar(128));

-- Loeschung der Stored Procedure fuer Use Case "Entsperrung eines Nutzer-Accounts"
drop procedure if exists nutzer_entsperren(integer, varchar(32), varchar(128));

-- Loeschung der Stored Procedure fuer Use Case "Neuvergabe des Nutzerpassworts nach Entsperrung"
drop procedure if exists nutzerpasswort_aendern(integer, varchar(32), varchar(128));

-- Loeschung der Stored Procedure fuer Use Case "Nutzer-Account entfernen"
drop procedure if exists nutzer_entfernen(integer, varchar(32));

-- Loeschung der Stored Procedure fuer Use Case "Gesetzliche Krankenversicherungsbeitraege eintragen"
drop procedure if exists insert_krankenversicherungsbeitraege(integer, boolean, decimal(5, 3), decimal(5, 3), decimal(10, 2), decimal(10, 2), date);

-- Loeschung der Stored Procedure fuer Use Case "Gesetzliche Krankenkasse eintragen"
drop procedure if exists insert_gesetzliche_Krankenkasse(integer, varchar(128), varchar(16), decimal(5, 3), decimal(5, 3), decimal(5, 3), decimal(5, 3), decimal(5, 3), varchar(16), date);

-- Loeschung der Stored Procedure fuer Use Case "Private Krankenkasse eintragen"
drop procedure if exists insert_private_Krankenkasse(integer, varchar(128), varchar(16), decimal(5, 3), decimal(5, 3), decimal(5, 3), varchar(16), date);

-- Loeschung der Stored Procedure fuer Use Case "Gemeldete Krankenkasse eintragen"
drop procedure if exists insert_gemeldete_Krankenkasse(integer, varchar(128), varchar(16), decimal(5, 3), decimal(5, 3), decimal(5, 3), varchar(16), date);

-- Loeschung der Stored Procedure fuer Use Case "Arbeitnehmerbeitrag zur Pflegeversicherung eintragen"
drop procedure if exists insert_anzahl_kinder_an_pv_beitrag(integer, integer, boolean, decimal(5, 3), decimal(10, 2), decimal(10, 2), date);

-- Loeschung der Stored Procedure fuer Use Case "Arbeitgeberbeitrag zur Pflegeversicherung eintragen"
drop procedure if exists insert_arbeitsort_sachsen_ag_pv_beitrag(integer, boolean, decimal(5, 3), date);

-- Loeschung der Stored Procedure fuer Use Case "Arbeitslosenversicherungsbeitraege eintragen"
drop procedure if exists insert_arbeitslosenversicherungsbeitraege(integer, decimal(5, 3), decimal(5, 3), decimal(10, 2), decimal(10, 2), date);

-- Loeschung der Stored Procedure fuer Use Case "Rentenversicherungsbeitraege eintragen"
drop procedure if exists insert_rentenversicherungsbeitraege(integer, decimal(5, 3), decimal(5, 3), decimal(10, 2), decimal(10, 2), date);

-- Loeschung der Stored Procedure fuer Use Case "Minijobbeitraege eintragen"
drop procedure if exists insert_minijobbeitraege(integer, boolean, boolean, decimal(5, 3), decimal(5, 3), decimal(5, 3), decimal(5, 3), decimal(5, 3), decimal(5, 3), decimal(5, 3), date);

-- Loeschung der Stored Procedure fuer Use Case "Berufsgenossenschaft eintragen" 
drop procedure if exists insert_berufsgenossenschaft(integer, varchar(128), varchar(16));

--Loeschung der Stored Procedure fuer Use Case "Unfallversicherungsbeitraege eintragen" 
drop procedure if exists insert_unfallversicherungsbeitrag(integer, varchar(128), varchar (16), varchar(128), varchar(16), decimal(12, 2), integer);

-- Loeschung der Stored Procedure fuer Use Case "Gewerkschaft eintragen"
drop procedure if exists insert_gewerkschaft(integer, varchar(64));

-- Loeschung der Stored Procedures fuer Use Case "Tarif eintragen"
drop procedure if exists insert_tarif(integer, varchar(16), varchar(64));

-- Loeschung der Stored Procedures fuer Use Case "Verguetungsbestandteil eintragen"
drop procedure if exists insert_verguetungsbestandteil(integer, varchar(64), varchar(16));

-- Loeschung der Stored Procedures fuer Use Case "Tarif mit Verguetungsbestandteil verknuepfen"
drop procedure if exists insert_tarifliches_verguetungsbestandteil(integer, varchar(64), varchar(16), decimal(10, 2), date);

-- Loeschung der Stored Procedure fuer Use Case "Geschlecht anlegen"
drop procedure if exists insert_geschlecht(integer, varchar(32));

-- Loeschung der Stored Procedure fuer Use Case "Mitarbeitertyp eintragen"
drop procedure if exists insert_mitarbeitertyp(integer,varchar(32));

-- Loeschung der Stored Procedure fuer Use Case "Steuerklasse eintragen"
drop procedure if exists insert_steuerklasse(integer, char(1));

-- Loeschung der Stored Procedure fuer Use Case "Abteilung eintragen"
drop procedure if exists insert_abteilung(integer, varchar(64), varchar(16));

-- Loeschung der Stored Procedure fuer Use Case "Jobtitel eintragen" 
drop procedure if exists insert_jobtitel(integer, varchar(32));

-- Loeschung der Stored Procedure fuer Use Case "Erfahrungsstufe eintragen" 
drop procedure if exists insert_erfahrungsstufe(integer, varchar(32));

-- Loeschung der Stored Procedure fuer Use Case "Unternehmen eintragen" 
drop procedure if exists insert_unternehmen(integer, varchar(128), varchar(16));

-- Loeschung der Stored Procedure fuer Use Case "Austrittsgrundkategorie eintragen" 
drop procedure if exists insert_austrittsgrundkategorie(integer, varchar(16));

-- Loeschung der Stored Procedure fuer Use Case "Austrittsgrund eintragen" 
drop procedure if exists insert_austrittsgrund(integer, varchar(32), varchar(16));

-- Loeschung der Stored Procedures fuer Use Case "Neuen Mitarbeiter anlegen"
drop procedure if exists insert_neuer_mitarbeiter(integer, varchar(32), varchar(64), varchar(128), varchar(64), date, date, 
varchar(32), varchar(32), varchar(32), varchar(16), varchar(64), varchar(16), varchar(64), date, varchar(64), varchar(8), 
varchar(16), varchar(8), varchar(128), varchar(128), varchar(128), varchar(32), varchar(32), char(1), decimal(4, 2), 
varchar(64), varchar(16), boolean, varchar(32), varchar(32), varchar(128), boolean, varchar(16), boolean, varchar(128), 
varchar(16), boolean, boolean, integer, boolean, boolean, boolean, decimal(6, 2), decimal(6, 2), boolean, boolean, boolean, boolean);
drop procedure if exists insert_tbl_mitarbeiter(integer, varchar(32), varchar(64), varchar(128), varchar(64), date, date, varchar(32), varchar(32), 
varchar(32), varchar(16), varchar(64), varchar(16), varchar(64), date);
drop procedure if exists insert_tbl_laender(integer, varchar(128));
drop procedure if exists insert_tbl_regionen(integer, varchar(128), varchar(128));
drop procedure if exists insert_tbl_staedte(integer, varchar(128), varchar(128));
drop procedure if exists insert_tbl_postleitzahlen(integer, varchar(16), varchar(8), varchar(128));
drop procedure if exists insert_tbl_strassenbezeichnungen(integer, varchar(64), varchar(8), varchar(16));
drop procedure if exists insert_tbl_wohnt_in(integer, varchar(32), varchar(64), varchar(8), date);
drop procedure if exists insert_tbl_hat_geschlecht(integer, varchar(32), varchar(32), date);
drop procedure if exists insert_tbl_ist_mitarbeitertyp(integer, varchar(32), varchar(32), date);
drop procedure if exists insert_tbl_in_steuerklasse(integer, varchar(32), char(1), date);
drop procedure if exists insert_tbl_wochenarbeitsstunden(integer, decimal(4, 2));
drop procedure if exists insert_tbl_arbeitet_x_wochenarbeitsstunden(integer, varchar(32), decimal(4, 2), date);
drop procedure if exists insert_tbl_eingesetzt_in(integer, varchar(32), varchar(64), varchar(16), boolean, date);
drop procedure if exists insert_tbl_hat_jobtitel(integer, varchar(32), varchar(32), varchar(32), date);
drop procedure if exists insert_tbl_in_unternehmen(integer, varchar(32), varchar(128), date);
drop procedure if exists insert_tbl_hat_tarif(integer, varchar(32), varchar(16), date);
drop procedure if exists insert_tbl_aussertarifliche(varchar(32), integer, date);
drop procedure if exists insert_tbl_hat_private_krankenversicherung(integer, varchar(32), varchar(128), decimal(6, 2), decimal(6, 2), date);
drop procedure if exists insert_tbl_hat_gesetzliche_Krankenversicherung(integer, varchar(32), boolean, date);
drop procedure if exists insert_tbl_ist_in_gkv(integer, varchar(32), varchar(128), varchar(16), date);
drop procedure if exists insert_tbl_hat_x_kinder_unter_25(integer, varchar(32), integer, boolean, date);
drop procedure if exists insert_tbl_arbeitet_in_sachsen(integer, varchar(32), boolean, date);
drop procedure if exists insert_tbl_hat_gesetzliche_arbeitslosenversicherung(integer, varchar(32), date);
drop procedure if exists insert_tbl_hat_gesetzliche_rentenversicherung(integer, varchar(32), date);
drop procedure if exists insert_tbl_ist_anderweitig_versichert(integer, varchar(32), varchar(128), varchar(16), date);
drop procedure if exists insert_tbl_ist_Minijobber(integer, varchar(32), boolean, date);

-- Loeschung der Stored Procedure fuer Use Case "Aussertariflichen Verguetungsbestandteil einfuegen"
drop procedure if exists insert_aussertarifliches_verguetungsbestandteil(integer, varchar(32), varchar(64), decimal(8, 2), date);

-- Loeschung der Stored Procedure fuer Use Case "Adresse aktualisieren"
drop procedure if exists update_adresse(integer, varchar(32), date, date, varchar(64), varchar(8), varchar(16), varchar(8), varchar(128), varchar(128), varchar(128));

-- Loeschung der Stored Procedure fuer Use Case "Mitarbeiterentlassung eintragen"
drop procedure if exists update_mitarbeiterentlassung(integer, varchar(32), date, varchar(32));

-- Loeschung der Stored Procedure fuer Use Case "Krankenversicherungsbeitraege aktualisieren"
drop procedure if exists update_krankenversicherungsbeitraege( integer, boolean, decimal(5, 3), decimal(5, 3), decimal(10, 2), decimal(10, 2), date, date);

-- Loeschung der Stored Procedure fuer Use Case "Abteilungshierarchie erstellen"
drop procedure if exists update_erstelle_abteilungshierarchie(integer, varchar(64), varchar(64));

-- Loeschung der Stored Procedure fuer Use Case "Mitarbeiterdaten entfernen"
drop procedure if exists delete_mitarbeiterdaten(integer, varchar(32));

-- Loeschung der Stored Procedure fuer Use Case  "Nutzung der Personalstammdatenbank beenden"
drop procedure if exists delete_mandantendaten(integer);
