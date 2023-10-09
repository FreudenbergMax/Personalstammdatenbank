-- entferne Tabellen, die den Bereich "Jobtitel" behandeln
drop table hat_Jobtitel;
drop table Jobtitel;
drop table Erfahrungsstufen;

-- entferne Tabellen, die den Bereich "Wochenarbeitsstunden" behandeln
drop table arbeitet_x_Wochenstunden;
drop table Wochenarbeitsstunden;

-- entferne Tabellen, die den Bereich "Steuerklasse" behandeln
drop table in_Steuerklasse;
drop table Steuerklassen;

-- entferne Tabellen, die den Bereich "Gesellschaft" behandeln
drop table in_Gesellschaft;
drop table sitzt_in;
drop table Gesellschaften;

-- entferne Tabellen, die den Bereich "Adresse" behandeln
drop table wohnt_in;
drop table Erstwohnsitze;
drop table Postleitzahlen;
drop table Staedte;
drop table Regionen;
drop table Laender;

-- entferne Tabellen, die den Bereich "Geschaeftseinheit" behandeln
drop table eingesetzt_in;
drop table Abteilungen;

-- entferne Tabellen, die den Bereich "Mitarbeitertyp" behandeln
drop table ist_mitarbeitertyp;
drop table Mitarbeitertypen;

-- entferne Tabellen, die den Bereich "Entgelt/Tarif" behandeln
drop table Aussertarifliche;
drop table hat_Tarif; --
drop table hat_Verguetung; --
drop table Tarife; --
drop table Verguetungen; --
drop table Gewerkschaften; --

-- entferne Tabellen, die den Bereich "Beamte" behandeln
drop table bekommt_Beamtenzuschuesse;
drop table Beamte;
drop table Beamtenzuschuesse;

-- entferne Tabellen, die den Bereich "SV-Angestellte" behandeln
drop table ist_in_Unfallversicherung;
drop table Unfallversicherungen;
drop table Risikoklassen;
drop table hat_RVBeitraege;
drop table Rentenversicherungsbeitraege;
drop table hat_AVBeitraege;
drop table Arbeitslosenversicherungsbeitraege;

drop table KV_PV_Privat;

drop table hat_KV_Zusatzbeitrag;
drop table ist_in_GKV;
drop table KV_Zusatzbeitraege;
drop table Krankenkassen;

drop table hat_gesetzlichen_AG_PV_Beitragssatz;
drop table wohnt_in_Sachsen;
drop table AG_Pflegeversicherungsbeitraege_gesetzlich;
drop table wohnhaft_Sachsen;

drop table hat_gesetzlichen_AN_PV_Beitragssatz;
drop table hat_x_Kinder_unter25;
drop table AN_Pflegeversicherungsbeitraege_gesetzlich;
drop table Anzahl_Kinder_unter_25;

drop table hat_KVBeitraege;
drop table Krankenversicherungsbeitraege;

drop table KV_PV_Gesetzlich;

drop table SVpflichtige_Angestellte;

-- entferne Mitarbeiter
drop table Mitarbeiter;

-- entferne Tabellen, die den Bereich "Austritt" behandeln
drop table Austrittsgruende;
drop table Kategorien_Austrittsgruende;

-- entferne Mandantentabelle
drop table Mandanten;
