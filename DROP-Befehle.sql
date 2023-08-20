-- entferne Assoziationstabellen
drop table in_Steuerklasse;
drop table hat_Jobtitel;
drop table wohnt_in;
drop table eingesetzt_in;
drop table ist_mitarbeitertyp;

-- entferne Tabellen, die den Bereich "Jobtitel" behandeln
drop table Jobtitel;
drop table Erfahrungsstufen;

-- entferne Tabellen, die den Bereich "Steuerklasse" behandeln
drop table Steuerklassen;

-- entferne Tabellen, die den Bereich "Adresse" behandeln
drop table Erstwohnsitze;
drop table Postleitzahlen;
drop table Staedte;
drop table Regionen;
drop table Laender;

-- entferne Tabellen, die den Bereich "Geschaeftseinheit" behandeln
drop table Geschaeftseinheiten;

-- entferne Tabellen, die den Bereich "Mitarbeitertyp" behandeln
drop table Mitarbeitertypen;

-- entferne restliche Klassen
drop table Mitarbeiter;
drop table Austrittsgruende;
drop table Kategorien_Austrittsgruende;
drop table Geschlechter;


