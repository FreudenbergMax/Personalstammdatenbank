set role postgres;
--create role tenant_user;
-- Quelle: https://adityamattos.com/multi-tenancy-in-python-fastapi-and-sqlalchemy-using-postgres-row-level-security
-- Abschaffung der Rolle 'tenant-user' und dessen Privilegien
-- 'tenant-user' kann zukünftig erstellte Sequenzen (bspw. Serial) NICHT mehr nutzen benutzen 
alter default privileges in schema temp_test_schema revoke usage on sequences from tenant_user;
-- 'tenant-user' kann SELECT-, INSERT-, UPDATE- und DELETE-Befehle auf alle Tabellen im Schema 'public' (auch auf zukünftige Tabellen) NICHT mehr ausführen
alter default privileges in schema temp_test_schema revoke select, insert, update, delete on tables from tenant_user;
-- Berechtigungen auf Sequenzen für 'tenant'-user aufheben
revoke usage on all sequences in schema temp_test_schema from tenant_user;
-- Berechtigungen auf Tabellen für tenant-user aufheben
revoke select, insert, update, delete on all tables in schema temp_test_schema from tenant_user;
-- 'tenant_user' darf nicht mehr im Schema 'public' operieren 
revoke usage on schema temp_test_schema from tenant_user;
-- 'tenant-user' wird quasi enterbt
revoke tenant_user from postgres;
-- Rolle 'tenant_user' entfernen
drop role tenant_user;

-- Erstellung der Rolle 'tenant-user' mit diversen Zugriffsrechten
-- Rolle für die user erstellen, welcher RLS unterliegt
create role tenant_user;
-- tenant-user erbt Berechtigungen von postgres (=Admin)
grant tenant_user to postgres;
-- Rolle 'tenant-user' darf im Schema 'public' operieren
grant usage on schema temp_test_schema to tenant_user;
-- 'tenant-user' hat Lese- und Schreibberechtigung auf alle Tabellen im Schema 'public'
grant select, insert, update, delete on all tables in schema temp_test_schema to tenant_user;
-- 'tenant-user' kann Sequenzen verwenden. So soll bspw. Tabellen mit Serial-Spalten nutzbar sein
grant usage on all sequences in schema temp_test_schema to tenant_user;
-- 'tenant-user' kann SELECT-, INSERT-, UPDATE- und DELETE-Befehle auf alle Tabellen im Schema 'public' ausführen (auch auf zukünftige Tabellen)
alter default privileges in schema temp_test_schema grant select, insert, update, delete on tables to tenant_user;
-- 'tenant-user' kann zukünftig erstellte Sequenzen (bspw. Serial) benutzen 
alter default privileges in schema temp_test_schema grant usage on sequences to tenant_user;

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

drop table if exists in_Gesellschaft;
drop table if exists Gesellschaften;

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
drop table if exists Mandanten;

drop function if exists mandant_anlegen(varchar(128));
drop function if exists nutzer_anlegen(integer, varchar(32), varchar(64), varchar(64));
drop function if exists nutzer_entfernen(integer, varchar(32));
drop function if exists pruefe_einmaligkeit_personalnummer(integer, varchar(64), varchar(32));

-- Loeschung der Stored Procedure für Use Case "Eintrag neue Krankenversicherungsbeitraege"
drop function if exists insert_krankenversicherungsbeitraege(integer, boolean, decimal(5, 3), decimal(5, 3), decimal(10, 2), decimal(10, 2), date);

-- Loeschung der Stored Procedure für Use Case "Eintrag neue gesetzliche Krankenkasse"
drop function if exists insert_gesetzliche_Krankenkasse(integer, varchar(128), varchar(16), decimal(5, 3), decimal(5, 3), decimal(5, 3), decimal(5, 3), varchar(16), date);

-- Loeschung der Stored Procedure fuer Use Case "Eintrag neue private Krankenkasse"
drop function if exists insert_private_Krankenkasse(integer, varchar(128), varchar(16), decimal(5, 3), decimal(5, 3), decimal(5, 3), varchar(16), date);

-- Loeschung der Stored Procedure fuer Use Case "Eintrag neue gemeldete Krankenkasse fuer anderweitig Versicherte"
drop function if exists insert_gemeldete_Krankenkasse(integer, varchar(128), varchar(16), decimal(5, 3), decimal(5, 3), decimal(5, 3), varchar(16), date);

-- Loeschung der Stored Procedure für Use Case "Eintrag neue Kinderanzahl"
drop function if exists insert_anzahl_kinder_an_pv_beitrag(integer, integer, decimal(5, 3), decimal(10, 2), decimal(10, 2), date);

-- Loeschung der Stored Procedure für Use Case "Eintrag Sachsen"
drop function if exists insert_Sachsen(integer, boolean, decimal(5, 3), date);

-- Loeschung der Stored Procedure für Use Case "Eintrag neue Arbeitslosenversicherungsbeitraege"
drop function if exists insert_arbeitslosenversicherungsbeitraege(integer, decimal(5, 3), decimal(5, 3), decimal(10, 2), decimal(10, 2), date);

-- Loeschung der Stored Procedure für Use Case "Eintrag neue Rentenversicherungsbeitraege"
drop function if exists insert_rentenversicherungsbeitraege(integer, decimal(5, 3), decimal(5, 3), decimal(10, 2), decimal(10, 2), date);

-- Loeschung der Stored Procedure für Use Case "Eintrag neue Minijobdaten"
drop function if exists insert_Minijob(integer, boolean, decimal(5, 3), decimal(5, 3), decimal(5, 3), decimal(5, 3), decimal(5, 3), decimal(5, 3), decimal(5, 3), date);

-- Loeschung der Stored Procedures für Use Case "Eintrag neuer Tarif mit Verguetung"
drop function if exists insert_gewerkschaft(integer, varchar(64), varchar(64));
drop function if exists insert_tarif(integer, varchar(16), varchar(64), varchar(64));
drop function if exists insert_tarifliches_verguetungsbestandteil(integer, varchar(64), varchar(16), varchar(16), decimal(10, 2), date);

-- Loeschung der Stored Procedure fuer Use Case "Eintrag neues Geschlecht"
drop function if exists insert_geschlecht(integer, varchar(32));

-- Loeschung Stored Procedure fuer Use Case "Eintrag neuer Mitarbeitertyp"
drop function if exists insert_mitarbeitertyp(integer,varchar(32));

-- Loeschung der Stored Procedure fuer Use Case "Eintrag neue Steuerklasse"
drop function if exists insert_steuerklasse(integer, char(1));

-- Loeschung der Stored Procedure fuer Use Case "Eintrag neue Abteilung"
drop function if exists insert_abteilung(integer, varchar(64), varchar(16));

-- Loeschung der Stored Procedure fuer Use Case "Eintrag neuer Jobtitel" 
drop function if exists insert_jobtitel(integer, varchar(32));

-- Loeschung der Stored Procedure fuer Use Case "Eintrag neue Erfahrungsstufe" 
drop function if exists insert_erfahrungsstufe(integer, varchar(32));

-- Loeschung Stored Procedure fuer Use Case "Eintrag neue Gesellschaft" 
drop function if exists insert_gesellschaft(integer, varchar(128), varchar (16));

-- Loeschung der Stored Procedure fuer Use Case "Eintrag neue Austrittsgrundkategorie" 
drop function if exists insert_kategorien_austrittsgruende(integer, varchar(16));

-- Loeschung der Stored Procedure fuer Use Case "Eintrag neuer Austrittsgrund" 
drop function if exists insert_austrittsgruende(integer, varchar(32), varchar(16));

-- Loeschung Stored Procedure fuer Use Case "Eintrag neue Berufsgenossenschaft" 
drop function if exists insert_berufsgenossenschaft(integer, varchar(128), varchar(16));

--Loeschung Stored Procedure fuer Use Case "Eintrag neue Unfallversicherungsbeitraege" 
drop function if exists insert_unfallversicherungsbeitrag(integer, varchar(128), varchar (16), varchar(128), varchar(16), decimal(12, 2), integer);

-- Loeschung der Stored Procedures für Use Case "Eintrag neuer Mitarbeiter"
drop function if exists insert_mitarbeiterdaten(integer, varchar(32), varchar(64), varchar(128), varchar(64), date, date, varchar(32), varchar(32), varchar(32), 
varchar(16), varchar(64), varchar(16), varchar(64), date, varchar(64), varchar(8), varchar(16), varchar(128), varchar(128), varchar(128), varchar(32), varchar(32), 
char(1), decimal(4, 2), varchar(64), varchar(16), boolean, varchar(32), varchar(32), varchar(128), boolean, varchar(16), boolean, varchar(128), varchar(16), 
boolean, boolean, integer, boolean, boolean, decimal(6, 2), decimal(6, 2), boolean, boolean, boolean, boolean);
drop function if exists insert_tbl_mitarbeiter(integer, varchar(32), varchar(64), varchar(128), varchar(64), date, date,  varchar(32), varchar(32), 
varchar(32), varchar(16), varchar(64), varchar(16), varchar(64), date);
drop function if exists insert_tbl_laender(integer, varchar(128));
drop function if exists insert_tbl_regionen(integer, varchar(128), varchar(128));
drop function if exists insert_tbl_staedte(integer, varchar(128), varchar(128));
drop function if exists insert_tbl_postleitzahlen(integer, varchar(16), varchar(128));
drop function if exists insert_tbl_strassenbezeichnungen(integer, varchar(64), varchar(8), varchar(16));
drop function if exists insert_tbl_wohnt_in(integer, varchar(32), varchar(64), varchar(8), date);
drop function if exists insert_tbl_hat_geschlecht(integer, varchar(32), varchar(32), date);
drop function if exists insert_tbl_ist_mitarbeitertyp(integer, varchar(32), varchar(32), date);
drop function if exists insert_tbl_in_steuerklasse(integer, varchar(32), char(1), date);
drop function if exists insert_tbl_wochenarbeitsstunden(integer, decimal(4, 2));
drop function if exists insert_tbl_arbeitet_x_wochenarbeitsstunden(integer, varchar(32), decimal(4, 2), date);
drop function if exists insert_tbl_eingesetzt_in(integer, varchar(32), varchar(64), varchar(16), boolean, date);
drop function if exists insert_tbl_hat_jobtitel(integer, varchar(32), varchar(32), varchar(32), date);
drop function if exists insert_tbl_in_gesellschaft(integer, varchar(32), varchar(128), date);
drop function if exists insert_tbl_hat_tarif(integer, varchar(32), varchar(16), date);
drop function if exists insert_tbl_aussertarifliche(varchar(32), integer, date);
drop function if exists insert_tbl_hat_private_krankenversicherung(integer, varchar(32), varchar(128), decimal(6, 2), date);
drop function if exists insert_tbl_ist_Minijobber(integer, varchar(32), boolean, date);
drop function if exists insert_tbl_hat_gesetzliche_Krankenversicherung(integer, varchar(32), boolean, date);
drop function if exists insert_tbl_ist_in_gkv(integer, varchar(32), varchar(128), varchar(16), date);
drop function if exists insert_tbl_hat_x_kinder_unter_25(integer, varchar(32), integer, date);
drop function if exists insert_tbl_arbeitet_in_sachsen(integer, varchar(32), boolean, date);
drop function if exists insert_tbl_hat_gesetzliche_arbeitslosenversicherung(integer, varchar(32), date);
drop function if exists insert_tbl_hat_gesetzliche_rentenversicherung(integer, varchar(32), date);
drop function if exists insert_tbl_ist_anderweitig_versichert(integer, varchar(32), varchar(128), varchar(16), date);

-- Loeschung der Stored Procedure fuer Use Case "Eintrag Verguetungsbestandteil fuer aussertariflicher Mitarbeiter"
drop function if exists insert_aussertarifliche_verguetungsbestandteil(integer, varchar(32), varchar(64), decimal(8, 2), date);

-- Loeschung der Stored Procedure für Use Case "Update Adresse Mitarbeiter"
drop function if exists update_adresse(integer, varchar(32), date, date, varchar(64), varchar(8), varchar(16), varchar(128), varchar(128), varchar(128));

-- Loeschung der Stored Procedure für Use Case "Update Kuendigung Mitarbeiter"
drop function if exists update_mitarbeiterentlassung(integer, varchar(32), date, varchar(32));

-- Loeschung der Stored Procedure für Use Case "Update Krankenversicherungsbeitraege"
drop function if exists update_krankenversicherungsbeitraege( integer, boolean, decimal(5, 3), decimal(5, 3), decimal(10, 2), decimal(10, 2), date, date);

-- Loeschung der Stored Procedure für Use Case "Update Abteilungshierarchie"
drop function if exists update_erstelle_abteilungshierarchie(integer, varchar(64), varchar(64));

-- Loeschung der Stored Procedure für Use Case "Update Kuendigung Mitarbeiter"
drop function if exists delete_mitarbeiterdaten(integer, varchar(32));

-- Loeschung der Stored Procedure für Use Case  "Entferne Daten eines Mandanten aus Datenbank"
drop function if exists delete_mandantendaten(integer);

----------------------------------------------------------------------------------------------------------------
-- Erstellung der Tabellen mit Row-Level-Security (RLS)

create table Mandanten(
	Mandant_ID serial primary key,
	Firma varchar(128) unique not null
);
alter table Mandanten enable row level security;
create policy FilterMandant_Mandanten
    on Mandanten
    using (Mandant_ID = current_setting('app.current_tenant')::int);

create table Nutzer(
	Nutzer_ID serial primary key,
	Mandant_ID integer not null,
	Personalnummer varchar(32) not null,
	Vorname varchar(64) not null,
	Nachname varchar(64) not null,
	constraint fk_Nutzer_mandanten
		foreign key (Mandant_ID) 
			references Mandanten(Mandant_ID)
);
create unique index nutzer_idx on Nutzer(lower(Personalnummer));
alter table Nutzer enable row level security;
create policy FilterMandant_Nutzer
    on Nutzer
    using (Mandant_ID = current_setting('app.current_tenant')::int);

-- Tabellen, die den Bereich "Austrittsgruende" behandeln, erstellen
create table Kategorien_Austrittsgruende (
	Kategorie_Austrittsgruende_ID serial primary key,
	Mandant_ID integer not null,
	Austrittsgrundkategorie varchar(16) not null check(Austrittsgrundkategorie in ('verhaltensbedingt', 'personenbedingt', 'betriebsbedingt')),
	unique(Mandant_ID, Austrittsgrundkategorie),
	constraint fk_austrittsgrundkategorien_mandanten
		foreign key (Mandant_ID) 
			references Mandanten(Mandant_ID)
);
create unique index austrittsgrundkategorie_idx on Kategorien_Austrittsgruende(lower(Austrittsgrundkategorie));
alter table Kategorien_Austrittsgruende enable row level security;
create policy FilterMandant_kategorien_austrittsgruende
    on Kategorien_Austrittsgruende
    using (Mandant_ID = current_setting('app.current_tenant')::int);

create table Austrittsgruende (
	Austrittsgrund_ID serial primary key,
	Mandant_ID integer not null,
	Austrittsgrund varchar(32) not null,
	Kategorie_Austrittsgruende_ID integer not null,
	unique(Mandant_ID, Austrittsgrund),
	constraint fk_Austrittsgruende_mandanten
		foreign key (Mandant_ID) 
			references Mandanten(Mandant_ID),
	constraint fk_austrittsgruende_austrittsgrundkategorien 
		foreign key (Kategorie_Austrittsgruende_ID) 
			references Kategorien_Austrittsgruende(Kategorie_Austrittsgruende_ID)
);
create unique index austrittsgrund_idx on Austrittsgruende(lower(Austrittsgrund));
alter table Austrittsgruende enable row level security;
create policy FilterMandant_austrittsgruende
    on Austrittsgruende
    using (Mandant_ID = current_setting('app.current_tenant')::int);

-- Zentrale Tabelle 'Mitarbeiter' erstellen  
create table Mitarbeiter (
    Mitarbeiter_ID serial primary key,
    Mandant_ID integer not null,
    Personalnummer varchar(32) not null,
    Vorname varchar(64) not null,
    Zweitname varchar(128),
    Nachname varchar(64) not null,
    Geburtsdatum date not null,
    Eintrittsdatum date not null, 
    Steuernummer varchar(32),
    Sozialversicherungsnummer varchar(32),
    IBAN varchar(32),
    Private_Telefonnummer varchar(16),
    Private_Emailadresse varchar(64),
    Dienstliche_Telefonnummer varchar(16),
    Dienstliche_Emailadresse varchar(64),
    Befristet_Bis date,
    Austrittsdatum date,
    Austrittsgrund_ID integer,
    constraint fk_mitarbeiter_mandanten
		foreign key (Mandant_ID) 
			references Mandanten(Mandant_ID),
    constraint fk_mitarbeiter_austrittsgruende
		foreign key (Austrittsgrund_ID) 
			references Austrittsgruende(Austrittsgrund_ID)
);
alter table Mitarbeiter enable row level security;
create policy FilterMandant_Mitarbeiter
    on Mitarbeiter
    using (Mandant_ID = current_setting('app.current_tenant')::int);
--revoke update (Mandant_ID) on table Mitarbeiter from tenant_user;

-- Tabellen, die den Bereich "Adresse" behandeln, erstellen
create table Laender (
	Land_ID serial primary key,
	Mandant_ID integer not null,
	Land varchar(128) not null,
	unique(Mandant_ID, Land),
    constraint fk_laender_mandanten
		foreign key (Mandant_ID) 
			references Mandanten(Mandant_ID)
);
create unique index land_idx on Laender(lower(Land));
alter table Laender enable row level security;
create policy FilterMandant_Laender
    on Laender
    using (Mandant_ID = current_setting('app.current_tenant')::int);

create table Regionen (
	Region_ID serial primary key,
	Mandant_ID integer not null,
	Region varchar(128) not null,
	Land_ID integer not null,
	unique(Mandant_ID, Region),
    constraint fk_regionen_mandanten
		foreign key (Mandant_ID) 
			references Mandanten(Mandant_ID),
	constraint fk_regionen_laender
		foreign key (Land_ID)
			references Laender(Land_ID)
);
create unique index region_idx on Regionen(lower(Region));
alter table Regionen enable row level security;
create policy FilterMandant_Regionen
    on Regionen
    using (Mandant_ID = current_setting('app.current_tenant')::int);

create table Staedte (
	Stadt_ID serial primary key,
	Mandant_ID integer not null,
	Stadt varchar(128) not null,
	Region_ID integer not null,
	unique(Mandant_ID, Stadt),
	constraint fk_staedte_mandanten
		foreign key (Mandant_ID) 
			references Mandanten(Mandant_ID),
	constraint fk_staedte_regionen
		foreign key (Region_ID)
			references Regionen(Region_ID)
);
create unique index stadt_idx on Staedte(lower(Stadt));
alter table Staedte enable row level security;
create policy FilterMandant_Staedte
    on Staedte
    using (Mandant_ID = current_setting('app.current_tenant')::int);

create table Postleitzahlen (
	Postleitzahl_ID serial primary key,
	Mandant_ID integer not null,
	Postleitzahl varchar(16) not null,
	Stadt_ID integer not null,
	unique(Mandant_ID, Postleitzahl),
	constraint fk_postleitzahlen_mandanten
		foreign key (Mandant_ID) 
			references Mandanten(Mandant_ID),
	constraint fk_postleitzahlen_staedte
		foreign key (Stadt_ID)
			references Staedte(Stadt_ID)
);
create unique index postleitzahl_idx on Postleitzahlen(lower(Postleitzahl));
alter table Postleitzahlen enable row level security;
create policy FilterMandant_Postleitzahlen
    on Postleitzahlen
    using (Mandant_ID = current_setting('app.current_tenant')::int);

create table Strassenbezeichnungen (
	Strassenbezeichnung_ID serial primary key,
	Mandant_ID integer not null,
	Strasse varchar(64) not null,
	Hausnummer varchar(8) not null,
	Postleitzahl_ID integer not null,
	unique(Mandant_ID, Strasse, Hausnummer),
	constraint fk_erstwohnsitze_mandanten
		foreign key (Mandant_ID) 
			references Mandanten(Mandant_ID),
	constraint fk_erstwohnsitze_postleitzahlen
		foreign key (Postleitzahl_ID)
			references Postleitzahlen(Postleitzahl_ID)
);
create unique index strassenbezeichnungen_idx on Strassenbezeichnungen(lower(Strasse));
create unique index hausnummer_idx on Strassenbezeichnungen(lower(Hausnummer));
alter table Strassenbezeichnungen enable row level security;
create policy FilterMandant_Strassenbezeichnungen
    on Strassenbezeichnungen
    using (Mandant_ID = current_setting('app.current_tenant')::int);

-- Assoziationstabelle zwischen Mitarbeiter und Adressenbereich
create table wohnt_in (
	Mitarbeiter_ID integer not null,
	Strassenbezeichnung_ID integer not null,
	Mandant_ID integer not null,
	Datum_Von date not null,
    Datum_Bis date not null,
    primary key (Mitarbeiter_ID, Datum_Bis),
    constraint fk_wohntin_mitarbeiter
    	foreign key (Mitarbeiter_ID) 
    		references Mitarbeiter(Mitarbeiter_ID),
    constraint fk_wohntin_Strassenbezeichnungen
    	foreign key (Strassenbezeichnung_ID) 
    		references Strassenbezeichnungen(Strassenbezeichnung_ID),
	constraint fk_wohntin_mandanten
		foreign key (Mandant_ID) 
			references Mandanten(Mandant_ID)
);
alter table wohnt_in enable row level security;
create policy FilterMandant_wohnt_in
    on wohnt_in
    using (Mandant_ID = current_setting('app.current_tenant')::int);

-- Tabellen, die den Bereich "Geschlechter" behandeln, erstellen
create table Geschlechter(
	Geschlecht_ID serial primary key,
	Mandant_ID integer not null,
	Geschlecht varchar(32) not null check(Geschlecht in ('maennlich', 'weiblich', 'divers')),
	unique(Mandant_ID, Geschlecht),
	constraint fk_geschlechter_mandanten
		foreign key (Mandant_ID) 
			references Mandanten(Mandant_ID)
);
alter table Geschlechter enable row level security;
create policy FilterMandant_Geschlechter
    on Geschlechter
    using (Mandant_ID = current_setting('app.current_tenant')::int);

create table hat_Geschlecht(
	Mitarbeiter_ID integer not null,
	Geschlecht_ID integer not null,
	Mandant_ID integer not null,
	Datum_Von date not null,
	Datum_Bis date not null,
	primary key(Mitarbeiter_ID, Datum_Bis),
	constraint fk_hatgeschlecht_mitarbeiter
    	foreign key (Mitarbeiter_ID) 
    		references Mitarbeiter(Mitarbeiter_ID),
	constraint fk_hatgeschlecht_Geschlechter
    	foreign key (Geschlecht_ID) 
    		references Geschlechter(Geschlecht_ID),
	constraint fk_hatgeschlecht_mandanten
		foreign key (Mandant_ID) 
			references Mandanten(Mandant_ID)
);
alter table hat_Geschlecht enable row level security;
create policy FilterMandant_hat_geschlecht
    on hat_Geschlecht
    using (Mandant_ID = current_setting('app.current_tenant')::int);

-- Tabellen, die den Bereich "Mitarbeitertyp" (Angestellter, Arbeiter, Praktikant, Werkstudent etc.) behandeln, erstellen
create table Mitarbeitertypen (
	Mitarbeitertyp_ID serial primary key,
	Mandant_ID integer not null,
	Mitarbeitertyp varchar(32),
	unique(Mandant_ID, Mitarbeitertyp),
	constraint fk_mitarbeitertypen_mandanten
		foreign key (Mandant_ID) 
			references Mandanten(Mandant_ID)
);
create unique index mitarbeitertyp_idx on Mitarbeitertypen(lower(Mitarbeitertyp));
alter table Mitarbeitertypen enable row level security;
create policy FilterMandant_mitarbeitertypen
    on Mitarbeitertypen
    using (Mandant_ID = current_setting('app.current_tenant')::int);

-- Assoziationstabelle zwischen Mitarbeiter und Mitarbeitertyp
create table ist_Mitarbeitertyp (
	Mitarbeiter_ID integer not null,
	Mitarbeitertyp_ID integer not null,
	Mandant_ID integer not null,
	Datum_Von date not null,
    Datum_Bis date not null,
    primary key (Mitarbeiter_ID, Datum_Bis),
    constraint fk_istmitarbeitertyp_mitarbeiter
    	foreign key (Mitarbeiter_ID) 
    		references Mitarbeiter(Mitarbeiter_ID),
    constraint fk_istmitarbeitertyp_mitarbeitertypen
    	foreign key (Mitarbeitertyp_ID) 
    		references Mitarbeitertypen(Mitarbeitertyp_ID),
	constraint fk_istmitarbeitertyp_mandanten
		foreign key (Mandant_ID) 
			references Mandanten(Mandant_ID)
);
alter table ist_Mitarbeitertyp enable row level security;
create policy FilterMandant_ist_mitarbeitertyp
    on ist_Mitarbeitertyp
    using (Mandant_ID = current_setting('app.current_tenant')::int);

-- Tabellen, die den Bereich "Steuerklasse" behandeln, erstellen
create table Steuerklassen (
    Steuerklasse_ID serial primary key,
    Mandant_ID integer not null,
    Steuerklasse char(1) not null check(Steuerklasse in ('1', '2', '3', '4', '5', '6')),
    unique(Mandant_ID, Steuerklasse),
    constraint fk_steuerklassen_mandanten
		foreign key (Mandant_ID) 
			references Mandanten(Mandant_ID)
);
alter table Steuerklassen enable row level security;
create policy FilterMandant_steuerklassen
    on Steuerklassen
    using (Mandant_ID = current_setting('app.current_tenant')::int);

-- Assoziationstabelle zwischen Mitarbeiter und Steuerklasse
create table in_Steuerklasse (
    Mitarbeiter_ID integer not null,
    Steuerklasse_ID integer not null,
    Mandant_ID integer not null,
    Datum_Von date not null,
    Datum_Bis date not null,
    primary key (Mitarbeiter_ID, Datum_Bis),
    constraint fk_insteuerklasse_mitarbeiter
    	foreign key (Mitarbeiter_ID) 
    		references Mitarbeiter(Mitarbeiter_ID),
    constraint fk_insteuerklasse_steuerklassen
    	foreign key (Steuerklasse_ID) 
    		references Steuerklassen(Steuerklasse_ID),
    constraint fk_insteuerklasse_mandanten
		foreign key (Mandant_ID) 
			references Mandanten(Mandant_ID)
);
alter table in_Steuerklasse enable row level security;
create policy FilterMandant_in_steuerklasse
    on in_Steuerklasse
    using (Mandant_ID = current_setting('app.current_tenant')::int);

-- Tabellen, die den Bereich "Wochenstunden" behandeln, erstellen
create table Wochenarbeitsstunden(
	Wochenarbeitsstunden_ID serial primary key,
	Mandant_ID integer not null,
	Anzahl_Wochenstunden decimal(4, 2) not null,
	unique(Mandant_ID, Anzahl_Wochenstunden),
    constraint fk_wochenarbeitsstunden_mandanten
		foreign key (Mandant_ID) 
			references Mandanten(Mandant_ID)
);
alter table Wochenarbeitsstunden enable row level security;
create policy FilterMandant_wochenarbeitsstunden
    on Wochenarbeitsstunden
    using (Mandant_ID = current_setting('app.current_tenant')::int);

-- Assoziationstabelle zwischen Mitarbeiter und Wochenstunden
create table arbeitet_x_Wochenstunden (
    Mitarbeiter_ID integer not null,
    Wochenarbeitsstunden_ID integer not null,
    Mandant_ID integer not null,
    Datum_Von date not null,
    Datum_Bis date not null,
    primary key (Mitarbeiter_ID, Datum_Bis),
    constraint fk_arbeitetxwochenstunden_mitarbeiter
    	foreign key (Mitarbeiter_ID) 
    		references Mitarbeiter(Mitarbeiter_ID),
    constraint fk_arbeitetxwochenstunden_wochenarbeitsstunden
    	foreign key (Wochenarbeitsstunden_ID) 
    		references Wochenarbeitsstunden(Wochenarbeitsstunden_ID),
    constraint fk_arbeitetxwochenstunden_mandanten
		foreign key (Mandant_ID) 
			references Mandanten(Mandant_ID)
);
alter table arbeitet_x_Wochenstunden enable row level security;
create policy FilterMandant_arbeitet_x_wochenstunden
    on arbeitet_x_Wochenstunden
    using (Mandant_ID = current_setting('app.current_tenant')::int);
   
-- Tabellen, die den Bereich "Abteilung" behandeln, erstellen
create table Abteilungen (
	Abteilung_ID serial primary key,
	Mandant_ID integer not null,
	Abteilung varchar(64) not null,
	Abkuerzung varchar(16),
	untersteht_Abteilung integer,
	unique (Mandant_ID, Abteilung),
	unique (Mandant_ID, Abkuerzung),
	constraint fk_abteilungen_mandanten
		foreign key (Mandant_ID) 
			references Mandanten(Mandant_ID),
	constraint fk_abteilungen_abteilungen
		foreign key (untersteht_Abteilung)
			references Abteilungen(Abteilung_ID)
);
create unique index abteilung_idx on Abteilungen(lower(Abteilung));
create unique index abteilung_abk_idx on Abteilungen(lower(Abkuerzung));
alter table Abteilungen enable row level security;
create policy FilterMandant_abteilungen
    on Abteilungen
    using (Mandant_ID = current_setting('app.current_tenant')::int);

-- Assoziationstabelle zwischen Mitarbeiter und Geschäftsbereich
create table eingesetzt_in (
	Mitarbeiter_ID integer not null,
	Abteilung_ID integer not null,
	Mandant_ID integer not null,
	Fuehrungskraft boolean not null,
	Datum_Von date not null,
    Datum_Bis date not null,
    primary key (Mitarbeiter_ID, Datum_Bis),
    constraint fk_eingesetztin_mitarbeiter
    	foreign key (Mitarbeiter_ID) 
    		references Mitarbeiter(Mitarbeiter_ID),
    constraint fk_eingesetztin_abteilungen
    	foreign key (Abteilung_ID) 
    		references Abteilungen(Abteilung_ID),
	constraint fk_eingesetztin_mandanten
		foreign key (Mandant_ID) 
			references Mandanten(Mandant_ID)
);
alter table eingesetzt_in enable row level security;
create policy FilterMandant_eingesetzt_in
    on eingesetzt_in
    using (Mandant_ID = current_setting('app.current_tenant')::int);
   
-- Tabellen, die den Bereich "Jobtitel" behandeln, erstellen
create table Jobtitel (
	Jobtitel_ID serial primary key,
	Mandant_ID integer not null,
	Jobtitel varchar(32) not null,
	unique(Mandant_ID, Jobtitel),
    constraint fk_jobtitel_mandanten
		foreign key (Mandant_ID) 
			references Mandanten(Mandant_ID)
);
create unique index jobtitel_idx on Jobtitel(lower(Jobtitel));
alter table Jobtitel enable row level security;
create policy FilterMandant_jobtitel
    on Jobtitel
    using (Mandant_ID = current_setting('app.current_tenant')::int);
   
create table Erfahrungsstufen (
	Erfahrungsstufe_ID serial primary key,
	Mandant_ID integer not null,
	Erfahrungsstufe varchar(32) not null,
	unique(Mandant_ID, Erfahrungsstufe),
    constraint fk_erfahrungsstufen_mandanten
		foreign key (Mandant_ID) 
			references Mandanten(Mandant_ID)
);
create unique index erfahrungsstufe_idx on Erfahrungsstufen(lower(Erfahrungsstufe));
alter table Erfahrungsstufen enable row level security;
create policy FilterMandant_erfahrungsstufen
    on Erfahrungsstufen
    using (Mandant_ID = current_setting('app.current_tenant')::int);

-- Assoziationstabelle zwischen Mitarbeiter und Jobtitel + Erfahrungsstufen
create table hat_Jobtitel (
	Mitarbeiter_ID integer not null,
	Jobtitel_ID integer not null,
	Erfahrungsstufe_ID integer not null,
	Mandant_ID integer not null,
	Datum_Von date not null,
    Datum_Bis date not null,
    primary key (Mitarbeiter_ID, Datum_Bis),
    constraint fk_hatjobtitel_mitarbeiter
    	foreign key (Mitarbeiter_ID) 
    		references Mitarbeiter(Mitarbeiter_ID),
    constraint fk_hatjobtitel_jobtitel
    	foreign key (Jobtitel_ID) 
    		references Jobtitel(Jobtitel_ID),
    constraint fk_hatjobtitel_erfahrungsstufen
		foreign key (Erfahrungsstufe_ID)
			references Erfahrungsstufen(Erfahrungsstufe_ID),
	constraint fk_hatjobtitel_mandanten
		foreign key (Mandant_ID) 
			references Mandanten(Mandant_ID)
);
alter table hat_Jobtitel enable row level security;
create policy FilterMandant_hat_jobtitel
    on hat_Jobtitel
    using (Mandant_ID = current_setting('app.current_tenant')::int);

-- Tabellen, die den Bereich "Gesellschaft" behandeln, erstellen
create table Gesellschaften (
	Gesellschaft_ID serial primary key,
	Mandant_ID integer not null,
	Gesellschaft varchar(128) not null,
	Abkuerzung varchar(16),
	untersteht_Gesellschaft integer,
	unique (Mandant_ID, Gesellschaft),
	unique (Mandant_ID, Abkuerzung),
	constraint fk_gesellschaften_mandanten
		foreign key (Mandant_ID) 
			references Mandanten(Mandant_ID),
	constraint fk_gesellschaften_gesellschaften
		foreign key (untersteht_Gesellschaft)
			references Gesellschaften(Gesellschaft_ID)
);
create unique index gesellschaft_idx on Gesellschaften(lower(Gesellschaft));
create unique index abk_gesellschaft_idx on Gesellschaften(lower(Abkuerzung));
alter table Gesellschaften enable row level security;
create policy FilterMandant_gesellschaften
    on Gesellschaften
    using (Mandant_ID = current_setting('app.current_tenant')::int);

-- Assoziationstabelle zwischen Mitarbeiter und Gesellschaft
create table in_Gesellschaft (
	Mitarbeiter_ID integer not null,
	Gesellschaft_ID integer not null,
	Mandant_ID integer not null,
	Datum_Von date not null,
    Datum_Bis date not null,
    primary key (Mitarbeiter_ID, Gesellschaft_ID, Datum_Bis),
    constraint fk_ingesellschaft_mitarbeiter
    	foreign key (Mitarbeiter_ID) 
    		references Mitarbeiter(Mitarbeiter_ID),
    constraint fk_ingesellschaft_gesellschaften
    	foreign key (Gesellschaft_ID) 
    		references Gesellschaften(Gesellschaft_ID),
	constraint fk_ingesellschaft_mandanten
		foreign key (Mandant_ID) 
			references Mandanten(Mandant_ID)
); 
alter table in_Gesellschaft enable row level security;
create policy FilterMandant_in_gesellschaft
    on in_Gesellschaft
    using (Mandant_ID = current_setting('app.current_tenant')::int); 

create table Berufsgenossenschaften(
	Berufsgenossenschaft_ID serial primary key,
	Mandant_ID integer not null,
	Berufsgenossenschaft varchar(128) not null,
	Abkuerzung varchar(16),
	unique(Mandant_ID, Berufsgenossenschaft),
	unique(Mandant_ID, Abkuerzung),
	constraint fk_berufsgenossenschaften_mandanten
		foreign key (Mandant_ID) 
			references Mandanten(Mandant_ID)
);
create unique index berufsgenossenschaft_idx on Berufsgenossenschaften(lower(Berufsgenossenschaft));
create unique index Berufsgenossenschaft_abk_idx on Berufsgenossenschaften(lower(Abkuerzung));
alter table Berufsgenossenschaften enable row level security;
create policy FilterMandant_berufsgenossenschaften
    on Berufsgenossenschaften
    using (Mandant_ID = current_setting('app.current_tenant')::int);

create table Unfallversicherungsbeitraege(
	Gesellschaft_ID integer not null,
	Berufsgenossenschaft_ID integer not null,
	Mandant_ID integer not null,
	Beitrag decimal(12,2) not null,
	Beitragsjahr integer not null,
	primary key(Gesellschaft_ID, Berufsgenossenschaft_ID, Beitragsjahr),
	constraint fk_unfallversicherungsbeitraege_gesellschaften
    	foreign key (Gesellschaft_ID) 
    		references Gesellschaften(Gesellschaft_ID),
    constraint fk_unfallversicherungsbeitraege_berufsgenossenschaften
    	foreign key (Berufsgenossenschaft_ID) 
    		references Berufsgenossenschaften(Berufsgenossenschaft_ID),
	constraint fk_unfallversicherungsbeitraege_mandanten
		foreign key (Mandant_ID) 
			references Mandanten(Mandant_ID)
);
alter table Unfallversicherungsbeitraege enable row level security;
create policy FilterMandant_unfallversicherungsbeitraege
    on Unfallversicherungsbeitraege
    using (Mandant_ID = current_setting('app.current_tenant')::int);
 
-- Tabellen, die den Bereich "Tarifentgelt" behandeln, erstellen
create table Gewerkschaften (
	Gewerkschaft_ID serial primary key,
	Mandant_ID integer not null,
	Gewerkschaft varchar(64) not null,
	Branche varchar(64) not null,
	unique (Mandant_ID, Gewerkschaft, Branche),
	constraint fk_gewerkschaften_mandanten
		foreign key (Mandant_ID) 
			references Mandanten(Mandant_ID)
);
alter table Gewerkschaften enable row level security;
create policy FilterMandant_gewerkschaften
    on Gewerkschaften
    using (Mandant_ID = current_setting('app.current_tenant')::int);  

create table Tarife (
	Tarif_ID serial primary key,
	Mandant_ID integer not null,
	Tarifbezeichnung varchar(16) not null,
	Gewerkschaft_ID integer not null,
	unique (Mandant_ID, Tarifbezeichnung),
	constraint fk_tarife_mandanten
		foreign key (Mandant_ID) 
			references Mandanten(Mandant_ID),
	constraint fk_tarife_gewerkschaften
		foreign key (Gewerkschaft_ID)
			references Gewerkschaften(Gewerkschaft_ID)
);
alter table Tarife enable row level security;
create policy FilterMandant_tarife
    on Tarife
    using (Mandant_ID = current_setting('app.current_tenant')::int);

create table Verguetungsbestandteile(
	Verguetungsbestandteil_ID serial primary key,
	Mandant_ID integer not null,
	Verguetungsbestandteil varchar(64) not null,
	Auszahlungsmonat varchar(16) not null check(Auszahlungsmonat in ('jeden Monat', 'Januar', 'Februar', 'Maerz', 'April', 'Mai', 'Juni', 'Juli', 'August', 'September', 
																	 'Oktober', 'November', 'Dezember')),
	unique(Mandant_ID, Verguetungsbestandteil, Auszahlungsmonat),
	constraint fk_verguetungsbestandteile_mandanten
		foreign key (Mandant_ID) 
			references Mandanten(Mandant_ID)
);
alter table Verguetungsbestandteile enable row level security;
create policy FilterMandant_verguetungsbestandteile
    on Verguetungsbestandteile
    using (Mandant_ID = current_setting('app.current_tenant')::int);

create table hat_Verguetungsbestandteil_Tarif(
	Tarif_ID integer not null,
	Verguetungsbestandteil_ID integer not null,
	Mandant_ID integer not null,
	Betrag decimal(10, 2) not null,
	Datum_Von date not null,
	Datum_Bis date not null,
	primary key(Tarif_ID, Verguetungsbestandteil_ID, Datum_Bis),
	constraint fk_hatverguetungsbestandteiltarif_verguetungsbestandteile
    	foreign key (Verguetungsbestandteil_ID) 
    		references Verguetungsbestandteile(Verguetungsbestandteil_ID),
    constraint fk_hatverguetungsbestandteiltarif_tarif
		foreign key (Tarif_ID) 
			references Tarife(Tarif_ID),
	constraint fk_hatverguetungsbestandteiltarif_mandanten
		foreign key (Mandant_ID) 
			references Mandanten(Mandant_ID)
);
alter table hat_Verguetungsbestandteil_Tarif enable row level security;
create policy FilterMandant_hatverguetungsbestandteiltarif
    on hat_Verguetungsbestandteil_Tarif
    using (Mandant_ID = current_setting('app.current_tenant')::int); 

create table hat_Tarif (
    Mitarbeiter_ID integer not null,
    Tarif_ID integer not null,
    Mandant_ID integer not null,
    Datum_Von date not null,
    Datum_Bis date not null,
	primary key (Mitarbeiter_ID, Datum_Bis),
	constraint fk_hattarif_mitarbeiter
    	foreign key (Mitarbeiter_ID) 
    		references Mitarbeiter(Mitarbeiter_ID),
    constraint fk_hattarif_tarif
		foreign key (Tarif_ID) 
			references Tarife(Tarif_ID),
	constraint fk_hattarif_mandanten
		foreign key (Mandant_ID) 
			references Mandanten(Mandant_ID)
);
alter table hat_Tarif enable row level security;
create policy FilterMandant_hat_tarif
    on hat_Tarif
    using (Mandant_ID = current_setting('app.current_tenant')::int);
   
create table Aussertarifliche (
	Aussertarif_ID serial primary key,
	Mitarbeiter_ID integer not null,
	Mandant_ID integer not null,
	Datum_Von date not null,
	Datum_Bis date not null,
	unique(Mitarbeiter_ID, Datum_Bis),
	constraint fk_aussertarifliche_mitarbeiter
		foreign key (Mitarbeiter_ID)
			references Mitarbeiter(Mitarbeiter_ID),
	constraint fk_aussertarifliche_mandanten
		foreign key (Mandant_ID) 
			references Mandanten(Mandant_ID)		
);
alter table Aussertarifliche enable row level security;
create policy FilterMandant_aussertarifliche
    on Aussertarifliche
    using (Mandant_ID = current_setting('app.current_tenant')::int);

create table hat_Verguetungsbestandteil_AT(
	Aussertarif_ID integer not null,
	Verguetungsbestandteil_ID integer not null,
	Mandant_ID integer not null,
	Betrag decimal(8, 2) not null,
	Datum_Von date not null,
	Datum_Bis date not null,
	primary key(Aussertarif_ID, Verguetungsbestandteil_ID, Datum_Bis),
	constraint fk_hatverguetungsbestandteilat_verguetungsbestandteile
    	foreign key (Verguetungsbestandteil_ID) 
    		references Verguetungsbestandteile(Verguetungsbestandteil_ID),
    constraint fk_hatverguetungsbestandteilat_aussertarifliche
		foreign key (Aussertarif_ID) 
			references Aussertarifliche(Aussertarif_ID),
	constraint fk_hatverguetungsbestandteilat_mandanten
		foreign key (Mandant_ID) 
			references Mandanten(Mandant_ID)
);
alter table hat_Verguetungsbestandteil_AT enable row level security;
create policy FilterMandant_hatverguetungsbestandteilat
    on hat_Verguetungsbestandteil_AT
    using (Mandant_ID = current_setting('app.current_tenant')::int); 

create table gemeldete_Krankenkassen(
	gemeldete_Krankenkasse_ID serial primary key,
	Mandant_ID integer not null,
	gemeldete_Krankenkasse varchar(128) not null,
	Krankenkassenkuerzel varchar(16) not null,
	unique(Mandant_ID, gemeldete_Krankenkasse),
	unique(Mandant_ID, Krankenkassenkuerzel),
	constraint fk_gemeldetekrankenkassen_mandanten
		foreign key (Mandant_ID) 
			references Mandanten(Mandant_ID)
);
create unique index gemeldete_krankenkasse_idx on gemeldete_Krankenkassen(lower(gemeldete_Krankenkasse));
create unique index abk_gemeldete_krankenkasse_idx on gemeldete_Krankenkassen(lower(Krankenkassenkuerzel));
alter table gemeldete_Krankenkassen enable row level security;
create policy FilterMandant_gemeldetekrankenkassen
    on gemeldete_Krankenkassen
    using (Mandant_ID = current_setting('app.current_tenant')::int); 
   
create table ist_anderweitig_versichert(
	Mitarbeiter_ID integer not null,
	gemeldete_Krankenkasse_ID integer not null,
	Mandant_ID integer not null,
	Datum_Von date not null,
	Datum_Bis date not null,
	primary key (Mitarbeiter_ID, Datum_Bis),
	constraint fk_istanderweitigversichert_mitarbeiter
		foreign key (Mitarbeiter_ID)
			references Mitarbeiter(Mitarbeiter_ID),
	constraint fk_istanderweitigversichert_gemeldetekrankenkassen
		foreign key (gemeldete_Krankenkasse_ID)
			references gemeldete_Krankenkassen(gemeldete_Krankenkasse_ID),
	constraint fk_istanderweitigversichert_mandanten
		foreign key (Mandant_ID) 
			references Mandanten(Mandant_ID)
);
alter table ist_anderweitig_versichert enable row level security;
create policy FilterMandant_istanderweitigversichert
    on ist_anderweitig_versichert
    using (Mandant_ID = current_setting('app.current_tenant')::int); 
   
create table Privatkrankenkassen(
	Privatkrankenkasse_ID serial primary key,
	Mandant_ID integer not null,
	Privatkrankenkasse varchar(128) not null,
	Privatkrankenkassenkuerzel varchar(16) not null,
	unique (Mandant_ID, Privatkrankenkasse),
	unique (Mandant_ID, Privatkrankenkassenkuerzel),
	constraint fk_privatkrankenkassen_mandanten
		foreign key (Mandant_ID) 
			references Mandanten(Mandant_ID)
);
create unique index private_krankenkasse_idx on Privatkrankenkassen(lower(Privatkrankenkasse));
create unique index abk_private_krankenkasse_idx on Privatkrankenkassen(lower(Privatkrankenkassenkuerzel));
alter table Privatkrankenkassen enable row level security;
create policy FilterMandant_privatkrankenkassen
    on Privatkrankenkassen
    using (Mandant_ID = current_setting('app.current_tenant')::int);
   
create table hat_Privatkrankenkasse(
	Mitarbeiter_ID integer not null,
	Privatkrankenkasse_ID integer not null,
	Mandant_ID integer not null,
	AG_Zuschuss_private_Krankenversicherung decimal(6, 2) not null,
	AG_Zuschuss_private_Pflegeversicherung decimal(6, 2) not null,
	Datum_Von date not null,
	Datum_Bis date not null,
	primary key (Mitarbeiter_ID, Datum_Bis),
	constraint fk_hatprivatkrankenkasse_mitarbeiter
		foreign key (Mitarbeiter_ID)
			references Mitarbeiter(Mitarbeiter_ID),
	constraint fk_hatprivatkrankenkasse_privatkrankenkasse
		foreign key (Privatkrankenkasse_ID)
			references Privatkrankenkassen(Privatkrankenkasse_ID),
	constraint fk_hatprivatkrankenkasse_mandanten
		foreign key (Mandant_ID) 
			references Mandanten(Mandant_ID)
);
alter table hat_Privatkrankenkasse enable row level security;
create policy FilterMandant_hatprivatkrankenkasse
    on hat_Privatkrankenkasse
    using (Mandant_ID = current_setting('app.current_tenant')::int); 

-- Tabellen, die den Bereich "Gesetzlich Krankenversicherte" behandeln, erstellen
create table Krankenversicherungen (
	Krankenversicherung_ID serial primary key,
	Mandant_ID integer not null,
	ermaessigter_beitragssatz boolean not null,
	unique(Mandant_ID, ermaessigter_beitragssatz),
	constraint fk_krankenversicherungen_mandanten
		foreign key (Mandant_ID) 
			references Mandanten(Mandant_ID)
);
alter table Krankenversicherungen enable row level security;
create policy FilterMandant_krankenversicherungen
    on Krankenversicherungen
    using (Mandant_ID = current_setting('app.current_tenant')::int);

create table hat_gesetzliche_Krankenversicherung(
	Mitarbeiter_ID integer not null,
	Krankenversicherung_ID integer not null,
	Mandant_ID integer not null,
	Datum_Von date not null,
	Datum_Bis date not null,
	primary key (Mitarbeiter_ID, Datum_Bis),
	constraint fk_hatgesetzlichekrankenversicherung_mitarbeiter
		foreign key (Mitarbeiter_ID)
			references Mitarbeiter(Mitarbeiter_ID),
	constraint fk_hatgesetzlichekrankenversicherung_krankenversicherungen
		foreign key (Krankenversicherung_ID)
			references Krankenversicherungen(Krankenversicherung_ID),
	constraint fk_hatgesetzlichekrankenversicherung_mandanten
		foreign key (Mandant_ID) 
			references Mandanten(Mandant_ID)
);
alter table hat_gesetzliche_Krankenversicherung enable row level security;
create policy FilterMandant_hatgesetzlichekrankenversicherung
    on hat_gesetzliche_Krankenversicherung
    using (Mandant_ID = current_setting('app.current_tenant')::int);  
   
create table GKV_Beitraege(
	Krankenversicherungsbeitrag_ID serial primary key,
	Mandant_ID integer not null,
	AG_Krankenversicherungsbeitrag_in_Prozent decimal(5, 3) not null,
	AN_Krankenversicherungsbeitrag_in_Prozent decimal(5, 3) not null,
	Beitragsbemessungsgrenze_KV_Ost decimal(10, 2) not null,
	Beitragsbemessungsgrenze_KV_West decimal(10, 2) not null,
	unique(Mandant_ID, AG_Krankenversicherungsbeitrag_in_Prozent, AN_Krankenversicherungsbeitrag_in_Prozent, Beitragsbemessungsgrenze_KV_Ost, Beitragsbemessungsgrenze_KV_West),
	constraint fk_gkvbeitraege_mandanten
		foreign key (Mandant_ID) 
			references Mandanten(Mandant_ID)
);
alter table GKV_Beitraege enable row level security;
create policy FilterMandant_gkvbeitraege
    on GKV_Beitraege
    using (Mandant_ID = current_setting('app.current_tenant')::int);
   
create table hat_GKV_Beitraege (
	Krankenversicherung_ID integer not null,
	Krankenversicherungsbeitrag_ID integer not null,
	Mandant_ID integer not null,
	Datum_Von date not null,
	Datum_Bis date not null,
	primary key (Krankenversicherung_ID, Datum_Bis),
	constraint fk_hatgkvbeitraege_krankenversicherungen
		foreign key (Krankenversicherung_ID)
			references Krankenversicherungen(Krankenversicherung_ID),
	constraint fk_hatgkvbeitraege_gkvbeitraege
		foreign key (Krankenversicherungsbeitrag_ID)
			references GKV_Beitraege(Krankenversicherungsbeitrag_ID),
	constraint fk_hatgkvbeitraege_mandanten
		foreign key (Mandant_ID) 
			references Mandanten(Mandant_ID)
);
alter table hat_GKV_Beitraege enable row level security;
create policy FilterMandant_hatgkvbeitraege
    on hat_GKV_Beitraege
    using (Mandant_ID = current_setting('app.current_tenant')::int);   
   
create table gesetzliche_Krankenkassen (
	gesetzliche_Krankenkasse_ID serial primary key,
	Mandant_ID integer not null,
	Krankenkasse_gesetzlich varchar(128) not null,
	Krankenkassenkuerzel varchar(16) not null,
	unique(Mandant_ID, Krankenkasse_gesetzlich),
	unique(Mandant_ID, Krankenkassenkuerzel),
	constraint fk_krankenkassen_mandanten
		foreign key (Mandant_ID) 
			references Mandanten(Mandant_ID)
);
create unique index ges_krankenkasse_idx on gesetzliche_Krankenkassen(lower(Krankenkasse_gesetzlich));
create unique index abk_ges_krankenkasse_idx on gesetzliche_Krankenkassen(lower(Krankenkassenkuerzel));
alter table gesetzliche_Krankenkassen enable row level security;
create policy FilterMandant_gesetzlichekrankenkassen
    on gesetzliche_Krankenkassen
    using (Mandant_ID = current_setting('app.current_tenant')::int);

-- GKV = gesetzliche Krankenversicherung
create table ist_in_GKV(
	Mitarbeiter_ID integer not null,
	gesetzliche_Krankenkasse_ID integer not null,
	Mandant_ID integer not null,
	Datum_Von date not null,
	Datum_Bis date not null,
	primary key (Mitarbeiter_ID, Datum_Bis),
	constraint fk_istingkv_mitarbeiter
		foreign key (Mitarbeiter_ID)
			references Mitarbeiter(Mitarbeiter_ID),
	constraint fk_istingkv_gesetzlichekrankenkassen
		foreign key (gesetzliche_Krankenkasse_ID)
			references gesetzliche_Krankenkassen(gesetzliche_Krankenkasse_ID),
	constraint fk_istingkv_mandanten
		foreign key (Mandant_ID) 
			references Mandanten(Mandant_ID)
);
alter table ist_in_GKV enable row level security;
create policy FilterMandant_istingkv
    on ist_in_GKV
    using (Mandant_ID = current_setting('app.current_tenant')::int);

create table GKV_Zusatzbeitraege (
	GKV_Zusatzbeitrag_ID serial primary key,
	Mandant_ID integer not null,
	GKV_Zusatzbeitrag_in_Prozent decimal(5, 3) not null,
	unique(Mandant_ID, GKV_Zusatzbeitrag_in_Prozent),
	constraint fk_gkvzusatzbeitraege_mandanten
		foreign key (Mandant_ID) 
			references Mandanten(Mandant_ID)
);
alter table GKV_Zusatzbeitraege enable row level security;
create policy FilterMandant_gkvzusatzbeitraege
    on GKV_Zusatzbeitraege
    using (Mandant_ID = current_setting('app.current_tenant')::int);

create table hat_GKV_Zusatzbeitrag (
	gesetzliche_Krankenkasse_ID integer not null,
	GKV_Zusatzbeitrag_ID integer not null,
	Mandant_ID integer not null,
	Datum_Von date not null,
	Datum_Bis date not null,
	primary key (gesetzliche_Krankenkasse_ID, Datum_Bis),
	constraint fk_hatgkvzusatzbeitrag_gesetzlichekrankenkassen
		foreign key (gesetzliche_Krankenkasse_ID)
			references gesetzliche_Krankenkassen(gesetzliche_Krankenkasse_ID),
	constraint fk_hatgkvzusatzbeitrag_gkvzusatzbeitraege
		foreign key (GKV_Zusatzbeitrag_ID)
			references GKV_Zusatzbeitraege(GKV_Zusatzbeitrag_ID),
	constraint fk_hatgkvzusatzbeitrag_mandanten
		foreign key (Mandant_ID) 
			references Mandanten(Mandant_ID)
);
alter table hat_GKV_Zusatzbeitrag enable row level security;
create policy FilterMandant_hatgkvzusatzbeitrag
    on hat_GKV_Zusatzbeitrag
    using (Mandant_ID = current_setting('app.current_tenant')::int);

create table Umlagen (
	Umlage_ID serial primary key,
	Mandant_ID integer not null,
	U1_Umlagesatz_in_Prozent decimal(5, 3) not null,
	U2_Umlagesatz_in_Prozent decimal(5, 3) not null,
	Insolvenzgeldumlagesatz_in_Prozent decimal(5, 3) not null,
	privat_gesetzlich_oder_anders varchar(16) not null check(privat_gesetzlich_oder_anders in ('privat', 'gesetzlich', 'anders')),
	unique(Mandant_ID, U1_Umlagesatz_in_Prozent, U2_Umlagesatz_in_Prozent, Insolvenzgeldumlagesatz_in_Prozent, privat_gesetzlich_oder_anders),
	constraint fk_gkvzusatzbeitraege_mandanten
		foreign key (Mandant_ID) 
			references Mandanten(Mandant_ID)
);
alter table Umlagen enable row level security;
create policy FilterMandant_umlagen
    on Umlagen
    using (Mandant_ID = current_setting('app.current_tenant')::int);

create table hat_Umlagen_gesetzlich (
	gesetzliche_Krankenkasse_ID integer not null,
	Umlage_ID integer not null,
	Mandant_ID integer not null,
	Datum_Von date not null,
	Datum_Bis date not null,
	primary key (gesetzliche_Krankenkasse_ID, Datum_Bis),
	constraint fk_hatumlagengesetzlich_gesetzlichekrankenkassen
		foreign key (gesetzliche_Krankenkasse_ID)
			references gesetzliche_Krankenkassen(gesetzliche_Krankenkasse_ID),
	constraint fk_hatumlagengesetzlich_umlagen
		foreign key (Umlage_ID)
			references Umlagen(Umlage_ID),
	constraint fk_hatumlagengesetzlich_mandanten
		foreign key (Mandant_ID) 
			references Mandanten(Mandant_ID)
);
alter table hat_Umlagen_gesetzlich enable row level security;
create policy FilterMandant_hatumlagengesetzlich
    on hat_Umlagen_gesetzlich
    using (Mandant_ID = current_setting('app.current_tenant')::int);

create table hat_Umlagen_privat (
	Privatkrankenkasse_ID integer not null,
	Umlage_ID integer not null,
	Mandant_ID integer not null,
	Datum_Von date not null,
	Datum_Bis date not null,
	primary key (Privatkrankenkasse_ID, Datum_Bis),
	constraint fk_hatumlagenprivat_privatkrankenkassen
		foreign key (Privatkrankenkasse_ID)
			references Privatkrankenkassen(Privatkrankenkasse_ID),
	constraint fk_hatumlagenprivat_umlagen
		foreign key (Umlage_ID)
			references Umlagen(Umlage_ID),
	constraint fk_hatumlagenprivat_mandanten
		foreign key (Mandant_ID) 
			references Mandanten(Mandant_ID)
);
alter table hat_Umlagen_privat enable row level security;
create policy FilterMandant_hatumlagenprivat
    on hat_Umlagen_privat
    using (Mandant_ID = current_setting('app.current_tenant')::int);
   
create table hat_Umlagen_anderweitig (
	gemeldete_Krankenkasse_ID integer not null,
	Umlage_ID integer not null,
	Mandant_ID integer not null,
	Datum_Von date not null,
	Datum_Bis date not null,
	primary key (gemeldete_Krankenkasse_ID, Datum_Bis),
	constraint fk_hatumlagenanderweitig_gemeldetekrankenkassen
		foreign key (gemeldete_Krankenkasse_ID)
			references gemeldete_Krankenkassen(gemeldete_Krankenkasse_ID),
	constraint fk_hatumlagenanderweitig_umlagen
		foreign key (Umlage_ID)
			references Umlagen(Umlage_ID),
	constraint fk_hatumlagenanderweitig_mandanten
		foreign key (Mandant_ID) 
			references Mandanten(Mandant_ID)
);
alter table hat_Umlagen_anderweitig enable row level security;
create policy FilterMandant_hatumlagenanderweitig 
    on hat_Umlagen_anderweitig
    using (Mandant_ID = current_setting('app.current_tenant')::int);
   
create table Anzahl_Kinder_unter_25 (
	Anzahl_Kinder_unter_25_ID serial primary key,
	Mandant_ID integer not null,
	Anzahl_Kinder integer not null,
	unique(Mandant_ID, Anzahl_Kinder),
	constraint fk_anzahlkinderunter25_mandanten
		foreign key (Mandant_ID) 
			references Mandanten(Mandant_ID)
);
alter table Anzahl_Kinder_unter_25 enable row level security;
create policy FilterMandant_anzahlkinderunter25
    on Anzahl_Kinder_unter_25
    using (Mandant_ID = current_setting('app.current_tenant')::int);

create table hat_x_Kinder_unter_25(
	Mitarbeiter_ID integer not null,
	Anzahl_Kinder_unter_25_ID integer not null,
	Mandant_ID integer not null,
	Datum_Von date not null,
	Datum_Bis date not null,
	primary key (Mitarbeiter_ID, Datum_Bis),
	constraint fk_hatxKinderunter25_mitarbeiter
		foreign key (Mitarbeiter_ID)
			references Mitarbeiter(Mitarbeiter_ID),
	constraint fk_hatxKinderunter25_anzahlkinderunter25
		foreign key (Anzahl_Kinder_unter_25_ID)
			references Anzahl_Kinder_unter_25(Anzahl_Kinder_unter_25_ID),
	constraint fk_hatxKinderunter25_mandanten
		foreign key (Mandant_ID) 
			references Mandanten(Mandant_ID)
);
alter table hat_x_Kinder_unter_25 enable row level security;
create policy FilterMandant_hatxKinderunter25
    on hat_x_Kinder_unter_25
    using (Mandant_ID = current_setting('app.current_tenant')::int);

-- PV = Pflegeversicherung
create table AN_Pflegeversicherungsbeitraege_gesetzlich (
	AN_PV_Beitrag_ID serial primary key,
	Mandant_ID integer not null,
	AN_Anteil_PV_Beitrag_in_Prozent decimal(5, 3) not null,
	Beitragsbemessungsgrenze_PV_Ost decimal(10, 2) not null,
	Beitragsbemessungsgrenze_PV_West decimal(10, 2) not null,
	unique(Mandant_ID, AN_Anteil_PV_Beitrag_in_Prozent, Beitragsbemessungsgrenze_PV_Ost, Beitragsbemessungsgrenze_PV_West),
	constraint fk_anpflegeversicherungsbeitraegegesetzlich_mandanten
		foreign key (Mandant_ID) 
			references Mandanten(Mandant_ID)
);
alter table AN_Pflegeversicherungsbeitraege_gesetzlich enable row level security;
create policy FilterMandant_anpflegeversicherungsbeitraegegesetzlich
    on AN_Pflegeversicherungsbeitraege_gesetzlich
    using (Mandant_ID = current_setting('app.current_tenant')::int);
   
create table hat_gesetzlichen_AN_PV_Beitragssatz(
	Anzahl_Kinder_unter_25_ID integer not null,
	AN_PV_Beitrag_ID integer not null,
	Mandant_ID integer not null,
	Datum_Von date not null,
	Datum_Bis date not null,
	primary key (Anzahl_Kinder_unter_25_ID, Datum_Bis),
	constraint fk_hatgesetzlichenanpvbeitragssatz_anzahlkinderunter25
		foreign key (Anzahl_Kinder_unter_25_ID)
			references Anzahl_Kinder_unter_25(Anzahl_Kinder_unter_25_ID),
	constraint fk_hatgesetzlichenanpvbeitragssatz_anpflegeversicherungsbeitraegegesetzlich
		foreign key (AN_PV_Beitrag_ID)
			references AN_Pflegeversicherungsbeitraege_gesetzlich(AN_PV_Beitrag_ID),
	constraint fk_hatgesetzlichenanpvbeitragssatz_mandanten
		foreign key (Mandant_ID) 
			references Mandanten(Mandant_ID)
);
alter table hat_gesetzlichen_AN_PV_Beitragssatz enable row level security;
create policy FilterMandant_hatgesetzlichenanpvbeitragssatz
    on hat_gesetzlichen_AN_PV_Beitragssatz
    using (Mandant_ID = current_setting('app.current_tenant')::int);

create table Arbeitsort_Sachsen(
	Arbeitsort_Sachsen_ID serial primary key,
	Mandant_ID integer not null,
	in_Sachsen boolean not null,
	unique(Mandant_ID, in_Sachsen),
	constraint fk_arbeitsortsachsen_mandanten
		foreign key (Mandant_ID) 
			references Mandanten(Mandant_ID)
);
alter table Arbeitsort_Sachsen enable row level security;
create policy FilterMandant_arbeitsortsachsen
    on arbeitsort_sachsen
    using (Mandant_ID = current_setting('app.current_tenant')::int);

create table arbeitet_in_sachsen(
	Mitarbeiter_ID integer not null,
	Arbeitsort_Sachsen_ID integer not null,
	Mandant_ID integer not null,
	Datum_Von date not null,
	Datum_Bis date not null,
	primary key (Mitarbeiter_ID, Datum_Bis),
	constraint fk_arbeitetinsachsen_mitarbeiter
		foreign key (Mitarbeiter_ID)
			references Mitarbeiter(Mitarbeiter_ID),
	constraint fk_arbeitetinsachsen_wohnhaftsachsen
		foreign key (arbeitsort_sachsen_ID)
			references arbeitsort_sachsen(arbeitsort_sachsen_ID),
	constraint fk_arbeitetinsachsen_mandanten
		foreign key (Mandant_ID) 
			references Mandanten(Mandant_ID)
);
alter table arbeitet_in_sachsen enable row level security;
create policy FilterMandant_arbeitetinsachsen
    on arbeitet_in_sachsen
    using (Mandant_ID = current_setting('app.current_tenant')::int);  

create table AG_Pflegeversicherungsbeitraege_gesetzlich (
	AG_PV_Beitrag_ID serial primary key,
	Mandant_ID integer not null,
	AG_Anteil_PV_Beitrag_in_Prozent decimal(5, 3) not null,
	unique(Mandant_ID, AG_Anteil_PV_Beitrag_in_Prozent),
	constraint fk_agpflegeversicherungsbeitraegegesetzlich_mandanten
		foreign key (Mandant_ID) 
			references Mandanten(Mandant_ID)
);
alter table AG_Pflegeversicherungsbeitraege_gesetzlich enable row level security;
create policy FilterMandant_agpflegeversicherungsbeitraegegesetzlich
    on AG_Pflegeversicherungsbeitraege_gesetzlich
    using (Mandant_ID = current_setting('app.current_tenant')::int);
   
create table hat_gesetzlichen_AG_PV_Beitragssatz(
	Arbeitsort_Sachsen_ID integer not null,
	AG_PV_Beitrag_ID integer not null,
	Mandant_ID integer not null,
	Datum_Von date not null,
	Datum_Bis date not null,
	primary key (arbeitsort_sachsen_ID, Datum_Bis),
	constraint fk_hatgesetzlichenagpvbeitragssatz_arbeitsortsachsen
		foreign key (arbeitsort_sachsen_ID)
			references arbeitsort_sachsen(arbeitsort_sachsen_ID),	
	constraint fk_hatgesetzlichenagpvbeitragssatz_agpflegeversicherungsbeitraegegesetzlich
		foreign key (AG_PV_Beitrag_ID)
			references AG_Pflegeversicherungsbeitraege_gesetzlich(AG_PV_Beitrag_ID),	
	constraint fk_hatgesetzlichenagpvbeitragssatz_mandanten
		foreign key (Mandant_ID) 
			references Mandanten(Mandant_ID)
);
alter table hat_gesetzlichen_AG_PV_Beitragssatz enable row level security;
create policy FilterMandant_hatgesetzlichenagpvbeitragssatz
    on hat_gesetzlichen_AG_PV_Beitragssatz
    using (Mandant_ID = current_setting('app.current_tenant')::int);

-- Tabellen, die den Bereich "Gesetzliche Arbeitslosenversicherung" behandeln, erstellen
-- AV = Arbeitslosenversicherung
create table Arbeitslosenversicherungen (
	Arbeitslosenversicherung_ID serial primary key,
	Mandant_ID integer not null,
	constraint fk_arbeitslosenversicherungen_mandanten
		foreign key (Mandant_ID) 
			references Mandanten(Mandant_ID)
);
alter table Arbeitslosenversicherungen enable row level security;
create policy FilterMandant_arbeitslosenversicherungen
    on Arbeitslosenversicherungen
    using (Mandant_ID = current_setting('app.current_tenant')::int);
   
create table hat_gesetzliche_Arbeitslosenversicherung(
	Mitarbeiter_ID integer not null,
	Arbeitslosenversicherung_ID integer not null,
	Mandant_ID integer not null,
	Datum_Von date not null,
	Datum_Bis date not null,
	primary key (Mitarbeiter_ID, Datum_Bis),
	constraint fk_hatgesetzlichearbeitslosenversicherung_mitarbeiter
		foreign key (Mitarbeiter_ID)
			references Mitarbeiter(Mitarbeiter_ID),
	constraint fk_hatgesetzlichearbeitslosenversicherung_arbeitslosenversicherungen
		foreign key (Arbeitslosenversicherung_ID)
			references Arbeitslosenversicherungen(Arbeitslosenversicherung_ID),
	constraint fk_hatgesetzlichearbeitslosenversicherung_mandanten
		foreign key (Mandant_ID) 
			references Mandanten(Mandant_ID)
);
alter table hat_gesetzliche_Arbeitslosenversicherung enable row level security;
create policy FilterMandant_hatgesetzlichearbeitslosenversicherung
    on hat_gesetzliche_Arbeitslosenversicherung
    using (Mandant_ID = current_setting('app.current_tenant')::int);

create table Arbeitslosenversicherungsbeitraege(
	Arbeitslosenversicherungsbeitrag_ID serial primary key,
	Mandant_ID integer not null,
	AG_Arbeitslosenversicherungsbeitrag_in_Prozent decimal(5, 3) not null,
	AN_Arbeitslosenversicherungsbeitrag_in_Prozent decimal(5, 3) not null,
	Beitragsbemessungsgrenze_AV_Ost decimal(10, 2) not null,
	Beitragsbemessungsgrenze_AV_West decimal(10, 2) not null,
	unique(Mandant_ID, AG_Arbeitslosenversicherungsbeitrag_in_Prozent, AN_Arbeitslosenversicherungsbeitrag_in_Prozent, Beitragsbemessungsgrenze_AV_Ost, Beitragsbemessungsgrenze_AV_West),
	constraint fk_arbeitslosenversicherungsbeitraege_mandanten
		foreign key (Mandant_ID) 
			references Mandanten(Mandant_ID)
);
alter table Arbeitslosenversicherungsbeitraege enable row level security;
create policy FilterMandant_arbeitslosenversicherungsbeitraege
    on Arbeitslosenversicherungsbeitraege
    using (Mandant_ID = current_setting('app.current_tenant')::int);
   
create table hat_AV_Beitraege (
	Arbeitslosenversicherung_ID integer not null,
	Arbeitslosenversicherungsbeitrag_ID integer not null,
	Mandant_ID integer not null,
	Datum_Von date not null,
	Datum_Bis date not null,
	primary key (Arbeitslosenversicherung_ID, Datum_Bis),
	constraint fk_hatavbeitraege_arbeitslosenversicherungen
		foreign key (Arbeitslosenversicherung_ID)
			references Arbeitslosenversicherungen(Arbeitslosenversicherung_ID),
	constraint fk_hatavbeitraege_arbeitslosenversicherungsbeitraege
		foreign key (Arbeitslosenversicherungsbeitrag_ID)
			references Arbeitslosenversicherungsbeitraege(Arbeitslosenversicherungsbeitrag_ID),
	constraint fk_hatavbeitraege_mandanten
		foreign key (Mandant_ID) 
			references Mandanten(Mandant_ID)
);
alter table hat_AV_Beitraege enable row level security;
create policy FilterMandant_hatavbeitraege
    on hat_AV_Beitraege
    using (Mandant_ID = current_setting('app.current_tenant')::int); 

-- Tabellen, die den Bereich "Gesetzliche Rentenversicherung" behandeln, erstellen
-- RV = Rentenversicherung
create table Rentenversicherungen (
	Rentenversicherung_ID serial primary key,
	Mandant_ID integer not null,
	constraint fk_rentenversicherungen_mandanten
		foreign key (Mandant_ID) 
			references Mandanten(Mandant_ID)
);
alter table Rentenversicherungen enable row level security;
create policy FilterMandant_rentenversicherungen
    on Rentenversicherungen
    using (Mandant_ID = current_setting('app.current_tenant')::int); 

create table hat_gesetzliche_Rentenversicherung(
	Mitarbeiter_ID integer not null,
	Rentenversicherung_ID integer not null,
	Mandant_ID integer not null,
	Datum_Von date not null,
	Datum_Bis date not null,
	primary key (Mitarbeiter_ID, Datum_Bis),
	constraint fk_hatgesetzlicherentenversicherung_mitarbeiter
		foreign key (Mitarbeiter_ID)
			references Mitarbeiter(Mitarbeiter_ID),
	constraint fk_hatgesetzlicherentenversicherung_rentenversicherungen
		foreign key (Rentenversicherung_ID)
			references Rentenversicherungen(Rentenversicherung_ID),
	constraint fk_hatgesetzlicherentenversicherung_mandanten
		foreign key (Mandant_ID) 
			references Mandanten(Mandant_ID)
);
alter table hat_gesetzliche_Rentenversicherung enable row level security;
create policy FilterMandant_hatgesetzlicherentenversicherung
    on hat_gesetzliche_Rentenversicherung
    using (Mandant_ID = current_setting('app.current_tenant')::int);  
   
create table Rentenversicherungsbeitraege (
	Rentenversicherungsbeitrag_ID serial primary key,
	Mandant_ID integer not null,
	AG_Rentenversicherungsbeitrag_in_Prozent decimal(5, 3) not null,
	AN_Rentenversicherungsbeitrag_in_Prozent decimal(5, 3) not null,
	Beitragsbemessungsgrenze_RV_Ost decimal(10, 2) not null,
	Beitragsbemessungsgrenze_RV_West decimal(10, 2) not null,
	unique(Mandant_ID, AG_Rentenversicherungsbeitrag_in_Prozent, AN_Rentenversicherungsbeitrag_in_Prozent, Beitragsbemessungsgrenze_RV_Ost, Beitragsbemessungsgrenze_RV_West),
	constraint fk_rentenversicherungsbeitraege_mandanten
		foreign key (Mandant_ID) 
			references Mandanten(Mandant_ID)
);
alter table Rentenversicherungsbeitraege enable row level security;
create policy FilterMandant_rentenversicherungsbeitraege
    on Rentenversicherungsbeitraege
    using (Mandant_ID = current_setting('app.current_tenant')::int);
   
create table hat_RV_Beitraege(
	Rentenversicherung_ID integer not null,
	Rentenversicherungsbeitrag_ID integer not null,
	Mandant_ID integer not null,
	Datum_Von date not null,
	Datum_Bis date not null,
	primary key (Rentenversicherung_ID, Datum_Bis),
	constraint fk_hatrvbeitraege_rentenversicherungen
		foreign key (Rentenversicherung_ID)
			references Rentenversicherungen(Rentenversicherung_ID),
	constraint fk_hatrvbeitraege_rentenversicherungsbeitraegegesetzlich
		foreign key (Rentenversicherungsbeitrag_ID)
			references Rentenversicherungsbeitraege(Rentenversicherungsbeitrag_ID),
	constraint fk_hatrvbeitraege_mandanten
		foreign key (Mandant_ID) 
			references Mandanten(Mandant_ID)
);
alter table hat_RV_Beitraege enable row level security;
create policy FilterMandant_hatrvbeitraege
    on hat_RV_Beitraege
    using (Mandant_ID = current_setting('app.current_tenant')::int);

-- Tabellen, die den Bereich 'Minijobs' behandeln, erstellen
create table Minijobs(
	Minijob_ID serial primary key,
	Mandant_ID integer not null,
	kurzfristig_beschaeftigt boolean not null,
	unique(Mandant_ID, kurzfristig_beschaeftigt),
	constraint fk_minijob_mandanten
		foreign key(Mandant_ID)
			references Mandanten(Mandant_ID)
);
alter table Minijobs enable row level security;
create policy FilterMandant_minijobs
    on Minijobs
    using (Mandant_ID = current_setting('app.current_tenant')::int);

create table ist_Minijobber(
	Mitarbeiter_ID integer not null,
	Minijob_ID integer not null,
	Mandant_ID integer not null,
	Datum_Von date not null,
	Datum_Bis date not null,
	primary key (Mitarbeiter_ID, Datum_Bis),
	constraint fk_istminijobber_mitarbeiter
		foreign key (Mitarbeiter_ID)
			references Mitarbeiter(Mitarbeiter_ID),
	constraint fk_istminijobber_minijob
		foreign key (Minijob_ID)
			references Minijobs(Minijob_ID),
	constraint fk_istminijobber_mandanten
		foreign key (Mandant_ID) 
			references Mandanten(Mandant_ID)
);
alter table ist_Minijobber enable row level security;
create policy FilterMandant_istminijobber
    on ist_Minijobber
    using (Mandant_ID = current_setting('app.current_tenant')::int);

create table Pauschalabgaben(
	Pauschalabgabe_ID serial primary key,
	Mandant_ID integer,
	AG_Krankenversicherungsbeitrag_in_Prozent decimal(5, 3) not null,
	AG_Rentenversicherungsbeitrag_in_Prozent decimal(5, 3) not null,
	AN_Rentenversicherungsbeitrag_in_Prozent decimal(5, 3) not null,
	U1_Umlage_in_Prozent decimal(5, 3) not null,
	U2_Umlage_in_Prozent decimal(5, 3) not null,
	Insolvenzgeldumlage_in_Prozent decimal(5, 3) not null,
	Pauschalsteuer_in_Prozent decimal(5, 3) not null,
	unique(Mandant_ID, AG_Krankenversicherungsbeitrag_in_Prozent, AG_Rentenversicherungsbeitrag_in_Prozent, AN_Rentenversicherungsbeitrag_in_Prozent, U1_Umlage_in_Prozent, 
		   U2_Umlage_in_Prozent, Insolvenzgeldumlage_in_Prozent, Pauschalsteuer_in_Prozent),
	constraint fk_Pauschalabgaben_mandanten
		foreign key(Mandant_ID)
			references Mandanten(Mandant_ID)
);
alter table Pauschalabgaben enable row level security;
create policy FilterMandant_pauschalabgaben
    on Pauschalabgaben
    using (Mandant_ID = current_setting('app.current_tenant')::int);

create table hat_Pauschalabgaben(
	Minijob_ID integer not null,
	Pauschalabgabe_ID integer not null,
	Mandant_ID integer not null,
	Datum_Von date not null,
	Datum_Bis date not null,
	primary key (Minijob_ID, Datum_Bis),
	constraint fk_hatpauschalabgaben_minijobs
		foreign key (Minijob_ID)
			references Minijobs(Minijob_ID),
	constraint fk_hatpauschalabgaben_pauschalabgaben
		foreign key (Pauschalabgabe_ID)
			references Pauschalabgaben(Pauschalabgabe_ID),
	constraint fk_hatpauschalabgaben_mandanten
		foreign key (Mandant_ID) 
			references Mandanten(Mandant_ID)
);
alter table hat_Pauschalabgaben enable row level security;
create policy FilterMandant_hatpauschalabgaben
    on hat_Pauschalabgaben
    using (Mandant_ID = current_setting('app.current_tenant')::int);  

  
----------------------------------------------------------------------------------------------------------------
-- Erstellung der Stored Procedures

/*
 * Funktion legt neuen Mandanten in der Datenbank an.
 */
create or replace function mandant_anlegen(
	p_firma varchar(128)
) returns integer as
$$
declare
	v_mandant varchar(128);
	v_mandant_id integer;
begin
	
	set role postgres;

	-- Prüfung, ob der Name des Mandanten (bzw. der Firma) bereits existiert. Falls ja, so soll eine Exception geworfen werden. Andernfalls soll der Mandant angelegt werden
	execute 'SELECT firma FROM mandanten WHERE firma = $1' INTO v_mandant USING p_firma;

	if v_mandant is not null then
		raise exception 'Dieser Mandant ist bereits angelegt!';
	else
		insert into Mandanten(Firma) values(p_firma);
	end if;
    
	-- Mandant_ID des soeben angelegten Mandanten abfragen, damit diese im Mandant-Objekt auf der Python-Seite gespeichert werden kann.
	execute 'SELECT mandant_id FROM mandanten WHERE firma = $1' INTO v_mandant_id USING p_firma;
	return v_mandant_id;

end;
$$
language plpgsql;

/*
 * Funktion trägt die Daten eines neuen Nutzers in die Datenbank ein.
 */
create or replace function nutzer_anlegen(
	p_mandant_id integer,
	p_personalnummer varchar(32),
	p_vorname varchar(64),
	p_nachname varchar(64)
) returns integer as
$$
declare
	v_nutzer_id integer;
begin
	
	set session role tenant_user;
	execute 'SET app.current_tenant=' || p_mandant_id;

	perform pruefe_einmaligkeit_personalnummer(p_mandant_id, 'nutzer', p_personalnummer);

    insert into Nutzer(Mandant_ID, Personalnummer, Vorname, Nachname)
		values(p_mandant_id, p_personalnummer, p_vorname, p_nachname);
	
	-- Mandant_ID des soeben angelegten Mandanten abfragen, damit diese im Mandant-Objekt auf der Python-Seite gespeichert werden kann.
	execute 'SELECT nutzer_id FROM nutzer WHERE personalnummer = $1' INTO v_nutzer_id USING p_personalnummer;

	set role postgres;
	
	return v_nutzer_id;
	
end;
$$
language plpgsql;

/*
 * Diese Funktion prüft, ob die Personalnummer für einen neuen Mitarbeiter bereits vergeben ist. Ist die Personalnummer vergeben, so 
 * wird eine Exception geworfen. Diese Funktion wird aufgerufen, wenn ein neuer Mitarbeiter in die Datenbank eingetragen werden soll.
 */
create or replace function pruefe_einmaligkeit_personalnummer(
	p_mandant_id integer,
	p_tabelle varchar(64),
	p_personalnummer varchar(32)
) returns void as
$$
declare
	v_vorhandene_personalnummer varchar(32);
begin

	set session role tenant_user;
	execute 'SET app.current_tenant=' || p_mandant_id;
	
    execute 'SELECT personalnummer FROM '|| p_tabelle ||' WHERE personalnummer = $1' INTO v_vorhandene_personalnummer USING p_personalnummer;

    if v_vorhandene_personalnummer is not null then
    	set role postgres;
    	raise exception 'Diese Personalnummer wird bereits verwendet!';
	end if;

	set role postgres;

end;
$$
language plpgsql;

/*
 * Funktion entfernt einen Nutzer aus der Datenbank.
 */
create or replace function nutzer_entfernen(
	p_mandant_id integer,
	p_personalnummer varchar(32)
) returns void as
$$
begin

	set session role tenant_user;
	execute 'SET app.current_tenant=' || p_mandant_id;
	
    delete from nutzer where Personalnummer = p_personalnummer and Mandant_ID = p_mandant_id;

	set role postgres;

end;
$$
language plpgsql;





----------------------------------------------------------------------------------------------------------------
-- Stored Procedure für Use Case "Eintrag neue Krankenversicherungsbeitraege"

/*
 * Funktion trägt neue Daten bzgl. Krankenversicherungsbeitraege und Beitragsbemessungsgrenzen ein
 */
create or replace function insert_krankenversicherungsbeitraege (
	p_mandant_id integer,
	p_ermaessigter_beitragssatz boolean,
	p_ag_krankenversicherungsbeitrag_in_prozent decimal(5, 3),
	p_an_krankenversicherungsbeitrag_in_prozent decimal(5, 3),
	p_beitragsbemessungsgrenze_kv_ost decimal(10, 2),
	p_beitragsbemessungsgrenze_kv_west decimal(10, 2),
	p_eintragungsdatum date
) returns void as
$$
declare
	v_krankenversicherungsbeitrag_id integer;
	v_krankenversicherung_id integer;
begin
    
    set session role tenant_user;
    execute 'SET app.current_tenant=' || p_mandant_id;
   
    -- Pruefen, ob in Tabelle 'Krankenversicherungen' bereits ein Eintrag mit bzw. ohne Ermaessigung angelegt ist...
   	execute 'SELECT krankenversicherung_id FROM krankenversicherungen WHERE ermaessigter_beitragssatz = $1' 
   		into v_krankenversicherung_id using p_ermaessigter_beitragssatz;
    
    -- ... und falls sie bereits existiert, Meldung ausgeben, dass die Daten nicht mehr eingetragen werden müssen,...
    if v_krankenversicherung_id is not null then
    
		set role postgres;
		raise exception 'Ermaessigung = ''%'' ist bereits vorhanden! Uebergebene Daten werden nicht eingetragen! Wenn Sie diese Daten aktualisieren wollen, nutzen Sie bitte die ''update_krankenversicherungsbeitraege''-Funktion!', p_ermaessigter_beitragssatz;   
    
	--... ansonsten neue Kinderanzahl eintragen und id ziehen, da als Schluessel fuer Assoziation 'hat_GKV_Beitraege' benoetigt
	else
	
		insert into Krankenversicherungen(Mandant_ID, ermaessigter_Beitragssatz)
	   		values (p_mandant_id, p_ermaessigter_beitragssatz);	
	   	
	   	execute 'SELECT krankenversicherung_id FROM krankenversicherungen WHERE ermaessigter_beitragssatz = $1' 
   			into v_krankenversicherung_id using p_ermaessigter_beitragssatz;
	
	end if;

   	-- Pruefen, ob die Beitrags- und Beitragsbemessungsgrenzen-Kombination bereits vorhanden ist...
   	execute 'SELECT 
				krankenversicherungsbeitrag_id
			 FROM 
				gkv_beitraege 
			 WHERE 
				ag_krankenversicherungsbeitrag_in_prozent = $1 AND
				an_krankenversicherungsbeitrag_in_prozent = $2 AND
				beitragsbemessungsgrenze_kv_ost = $3 AND
				beitragsbemessungsgrenze_kv_west = $4' 
   			into 
   				v_krankenversicherungsbeitrag_id 
			using 
				p_ag_krankenversicherungsbeitrag_in_prozent, 
				p_an_krankenversicherungsbeitrag_in_prozent,
				p_beitragsbemessungsgrenze_kv_ost,
				p_beitragsbemessungsgrenze_kv_west;
    
    -- ... und falls sie nicht existiert, dann eintragen
    if v_krankenversicherungsbeitrag_id is null then
		insert into
	   		GKV_Beitraege(Mandant_ID, 
				   		  AG_Krankenversicherungsbeitrag_in_Prozent,
						  AN_Krankenversicherungsbeitrag_in_Prozent,
						  Beitragsbemessungsgrenze_KV_Ost,
						  Beitragsbemessungsgrenze_KV_West)
	   	values
	   		(p_mandant_id, 
	   		 p_ag_krankenversicherungsbeitrag_in_prozent,
			 p_an_krankenversicherungsbeitrag_in_prozent,
			 p_beitragsbemessungsgrenze_kv_ost,
			 p_beitragsbemessungsgrenze_kv_west);
		
		-- Nochmal krankenversicherungsbeitrag_id ziehen, da diese als Schluessel fuer die Assoziation 'hat_GKV_Beitraege' benoetigt wird
		execute 'SELECT 
				krankenversicherungsbeitrag_id
			 FROM 
				gkv_beitraege 
			 WHERE 
				ag_krankenversicherungsbeitrag_in_prozent = $1 AND
				an_krankenversicherungsbeitrag_in_prozent = $2 AND
				beitragsbemessungsgrenze_kv_ost = $3 AND
				beitragsbemessungsgrenze_kv_west = $4' 
   			into 
   				v_krankenversicherungsbeitrag_id 
			using 
				p_ag_krankenversicherungsbeitrag_in_prozent, 
				p_an_krankenversicherungsbeitrag_in_prozent,
				p_beitragsbemessungsgrenze_kv_ost,
				p_beitragsbemessungsgrenze_kv_west;
    end if;
   
    -- Datensatz in Assoziation 'hat_GKV_Beitraege', welche die Tabellen 'Krankenversicherungen' und 'GKV_Beitraege' verbindet, eintragen
    insert into hat_GKV_Beitraege(Krankenversicherung_ID, Krankenversicherungsbeitrag_ID, Mandant_ID, Datum_Von, Datum_Bis)
   		values (v_krankenversicherung_id, v_krankenversicherungsbeitrag_id, p_mandant_id, p_eintragungsdatum, '9999-12-31');
   	
    set role postgres;

end;
$$
language plpgsql;





----------------------------------------------------------------------------------------------------------------
-- Stored Procedure für Use Case "Eintrag neue gesetzliche Krankenkasse"

/*
 * Funktion trägt neue Daten einer Krankenkasse mit dessen individuellen Zusatzbeitrag und Umlagesaetze ein.
 */
create or replace function insert_gesetzliche_Krankenkasse (
	p_mandant_id integer,
	p_krankenkasse varchar(128),
	p_krankenkassenkuerzel varchar(16),
	p_gkv_zusatzbeitrag_in_prozent decimal(5, 3),
	p_u1_umlagesatz_in_prozent decimal(5, 3),
	p_u2_umlagesatz_in_prozent decimal(5, 3),
	p_insolvenzgeldumlagesatz_in_prozent decimal(5, 3),
	p_gesetzlich varchar(16),
	p_eintragungsdatum date
) returns void as
$$
declare
	v_krankenkasse_id integer;
	v_gkvzusatzbeitrag_id integer;
	v_umlage_id integer;
begin
    
    set session role tenant_user;
    execute 'SET app.current_tenant=' || p_mandant_id;
   
    -- Pruefen, ob gesetzliche Krankenkasse bereits vorhanden ist...
   	execute 'SELECT gesetzliche_krankenkasse_ID FROM gesetzliche_krankenkassen WHERE krankenkasse_gesetzlich = $1' into v_krankenkasse_id using p_krankenkasse;
    
    -- ... und falls sie bereits existiert, Meldung ausgeben, dass die Daten nicht mehr eingetragen werden müssen, ...
    if v_krankenkasse_id is not null then
    
		set role postgres;
		raise exception 'Gesetzliche Krankenkasse ''%'' ist bereits vorhanden! Uebergebene Daten werden nicht eingetragen! Wenn Sie diese Daten aktualisieren wollen, nutzen Sie bitte die ''update_gesetzliche_krankenkasse''-Funktion!', p_krankenkasse;   
    
	--... ansonsten neue gesetzliche Krankenkasse eintragen und id ziehen, da als Schluessel fuer Assoziation 'hat_GKV_Zusatzbeitrag' benoetigt
	else
	
		insert into gesetzliche_krankenkassen(Mandant_ID, Krankenkasse_gesetzlich, Krankenkassenkuerzel)
    		values(p_mandant_id, p_krankenkasse, p_krankenkassenkuerzel);
    
		execute 'SELECT gesetzliche_krankenkasse_ID FROM gesetzliche_krankenkassen WHERE krankenkasse_gesetzlich = $1' into v_krankenkasse_id using p_krankenkasse;
	
	end if;
   
    -- Pruefen, ob der GKV_Zusatzbeitrag bereits vorhanden ist...
   	execute 'SELECT gkv_zusatzbeitrag_id FROM gkv_zusatzbeitraege WHERE gkv_zusatzbeitrag_in_prozent = $1'
	   		into v_gkvzusatzbeitrag_id using p_gkv_zusatzbeitrag_in_prozent;
	
	-- ... falls nicht, dann eintragen
   	if v_gkvzusatzbeitrag_id is null then
		
		insert into GKV_Zusatzbeitraege(Mandant_ID, GKV_Zusatzbeitrag_in_Prozent)
   			values (p_mandant_id, p_gkv_zusatzbeitrag_in_prozent);
   		
   		-- Nochmal gkv_zusatzbeitrag_id ziehen, da diese als Schluessel fuer die Assoziation 'hat_GKV_Zusatzbeitrag' benoetigt wird
   		execute 'SELECT gkv_zusatzbeitrag_id FROM gkv_zusatzbeitraege WHERE gkv_zusatzbeitrag_in_prozent = $1'
	   		into v_gkvzusatzbeitrag_id using p_gkv_zusatzbeitrag_in_prozent;
   		
	end if;
    
   	-- Datensatz in Assoziation 'hat_GKV_Zusatzbeitrag', welche die Tabellen 'gesetzliche_Krankenkassen' und 'GKV_Zusatzbeitraege' verbindet, eintragen
    insert into hat_GKV_Zusatzbeitrag(gesetzliche_Krankenkasse_ID, GKV_Zusatzbeitrag_ID, Mandant_ID, Datum_Von, Datum_Bis)
   		values (v_krankenkasse_id, v_gkvzusatzbeitrag_id, p_mandant_id, p_eintragungsdatum, '9999-12-31');
   	
   	
   	-- Pruefen, ob die Umlagesaetze bereits vorhanden sind...
   	execute 'SELECT umlage_id FROM umlagen WHERE u1_umlagesatz_in_prozent = $1 AND u2_umlagesatz_in_prozent = $2 AND insolvenzgeldumlagesatz_in_prozent = $3 AND privat_gesetzlich_oder_anders = $4'
	   		into v_umlage_id using p_u1_umlagesatz_in_prozent, p_u2_umlagesatz_in_prozent, p_insolvenzgeldumlagesatz_in_prozent, p_gesetzlich;
	
	-- ... falls nicht, dann eintragen
   	if v_umlage_id is null then
		
		insert into Umlagen(Mandant_ID, U1_Umlagesatz_in_Prozent, U2_Umlagesatz_in_Prozent, Insolvenzgeldumlagesatz_in_Prozent, privat_gesetzlich_oder_anders)
   			values (p_mandant_id, p_u1_umlagesatz_in_prozent, p_u2_umlagesatz_in_prozent, p_insolvenzgeldumlagesatz_in_prozent, p_gesetzlich);
   		
   		-- Nochmal v_umlage_id ziehen, da diese als Schluessel fuer die Assoziation 'hat_Umlagen_gesetzlich' benoetigt wird
   		execute 'SELECT umlage_id FROM umlagen WHERE u1_umlagesatz_in_prozent = $1 AND u2_umlagesatz_in_prozent = $2 AND insolvenzgeldumlagesatz_in_prozent = $3 AND privat_gesetzlich_oder_anders = $4'
	   		into v_umlage_id using p_u1_umlagesatz_in_prozent, p_u2_umlagesatz_in_prozent, p_insolvenzgeldumlagesatz_in_prozent, p_gesetzlich;
   		
	end if;
    
   	-- Datensatz in Assoziation 'hat_Umlagen_gesetzlich', welche die Tabellen 'gesetzliche_Krankenkassen' und 'Umlagen' verbindet, eintragen
    insert into hat_Umlagen_gesetzlich(gesetzliche_Krankenkasse_ID, Umlage_ID, Mandant_ID, Datum_Von, Datum_Bis)
   		values (v_krankenkasse_id, v_umlage_id, p_mandant_id, p_eintragungsdatum, '9999-12-31');

    set role postgres;

exception
    when unique_violation then
    	set role postgres;
        raise exception 'Gesetzliche Krankenkasse ''%'' oder dessen Kuerzel ''%'' bereits vorhanden!', p_krankenkasse, p_krankenkassenkuerzel;

end;
$$
language plpgsql;





----------------------------------------------------------------------------------------------------------------
-- Stored Procedure für Use Case "Eintrag neue private Krankenkasse"

/*
 * Funktion trägt neue Daten einer privaten Krankenkasse mit dessen Umlagesaetze ein.
 */
create or replace function insert_private_Krankenkasse (
	p_mandant_id integer,
	p_krankenkasse varchar(128),
	p_krankenkassenkuerzel varchar(16),
	p_u1_umlagesatz_in_prozent decimal(5, 3),
	p_u2_umlagesatz_in_prozent decimal(5, 3),
	p_insolvenzgeldumlagesatz_in_prozent decimal(5, 3),
	p_privat varchar(16),
	p_eintragungsdatum date
) returns void as
$$
declare
	v_krankenkasse_id integer;
	v_umlage_id integer;
begin
    
    set session role tenant_user;
    execute 'SET app.current_tenant=' || p_mandant_id;
   
    -- Pruefen, ob Privatkrankenkasse bereits vorhanden ist...
   	execute 'SELECT privatkrankenkasse_id FROM privatkrankenkassen WHERE privatkrankenkasse = $1' into v_krankenkasse_id using p_krankenkasse;
    
    -- ... und falls sie bereits existiert, Meldung ausgeben, dass die Daten nicht mehr eingetragen werden muessen, ...
    if v_krankenkasse_id is not null then
    
		set role postgres;
		raise exception 'Private Krankenkasse ''%'' ist bereits vorhanden! Uebergebene Daten werden nicht eingetragen! Wenn Sie diese Daten aktualisieren wollen, nutzen Sie bitte die ''update_privatkrankenkasse''-Funktion!', p_krankenkasse;   
    
	--... ansonsten neue Privatkrankenkasse eintragen und id ziehen, da als Schluessel fuer Assoziation 'hat_Umlagen_privat' benoetigt
	else
	
		insert into Privatkrankenkassen(Mandant_ID, Privatkrankenkasse, Privatkrankenkassenkuerzel)
    		values(p_mandant_id, p_krankenkasse, p_krankenkassenkuerzel);
    
		execute 'SELECT privatkrankenkasse_id FROM privatkrankenkassen WHERE privatkrankenkasse = $1' into v_krankenkasse_id using p_krankenkasse;
	
	end if;
   	
   	-- Pruefen, ob die Umlagesaetze bereits vorhanden sind...
   	execute 'SELECT umlage_id FROM umlagen WHERE u1_umlagesatz_in_prozent = $1 AND u2_umlagesatz_in_prozent = $2 AND insolvenzgeldumlagesatz_in_prozent = $3 AND privat_gesetzlich_oder_anders = $4'
	   		into v_umlage_id using p_u1_umlagesatz_in_prozent, p_u2_umlagesatz_in_prozent, p_insolvenzgeldumlagesatz_in_prozent, p_privat;
	
	-- ... falls nicht, dann eintragen
   	if v_umlage_id is null then
		
		insert into Umlagen(Mandant_ID, U1_Umlagesatz_in_Prozent, U2_Umlagesatz_in_Prozent, Insolvenzgeldumlagesatz_in_Prozent, privat_gesetzlich_oder_anders)
   			values (p_mandant_id, p_u1_umlagesatz_in_prozent, p_u2_umlagesatz_in_prozent, p_insolvenzgeldumlagesatz_in_prozent, p_privat);
   		
   		-- Nochmal v_umlage_id ziehen, da diese als Schluessel fuer die Assoziation 'hat_Umlagen_gesetzlich' benoetigt wird
   		execute 'SELECT umlage_id FROM umlagen WHERE u1_umlagesatz_in_prozent = $1 AND u2_umlagesatz_in_prozent = $2 AND insolvenzgeldumlagesatz_in_prozent = $3 AND privat_gesetzlich_oder_anders = $4'
	   		into v_umlage_id using p_u1_umlagesatz_in_prozent, p_u2_umlagesatz_in_prozent, p_insolvenzgeldumlagesatz_in_prozent, p_privat;
   		
	end if;
    
   	-- Datensatz in Assoziation 'hat_Umlagen_privat', welche die Tabellen 'Privatkrankenkassen' und 'Umlagen' verbindet, eintragen
    insert into hat_Umlagen_privat(Privatkrankenkasse_ID, Umlage_ID, Mandant_ID, Datum_Von, Datum_Bis)
   		values (v_krankenkasse_id, v_umlage_id, p_mandant_id, p_eintragungsdatum, '9999-12-31');

    set role postgres;

exception
    when unique_violation then
    	set role postgres;
        raise exception 'Private Krankenkasse ''%'' oder dessen Kuerzel ''%'' bereits vorhanden!', p_krankenkasse, p_krankenkassenkuerzel;

end;
$$
language plpgsql;





----------------------------------------------------------------------------------------------------------------
-- Stored Procedure für Use Case "Eintrag neue gemeldete Krankenkasse fuer anderweitig Versicherte"

/*
 * Funktion trägt neue Daten einer privaten Krankenkasse mit dessen Umlagesaetze ein.
 */
create or replace function insert_gemeldete_Krankenkasse(
	p_mandant_id integer,
	p_krankenkasse varchar(128),
	p_krankenkassenkuerzel varchar(16),
	p_u1_umlagesatz_in_prozent decimal(5, 3),
	p_u2_umlagesatz_in_prozent decimal(5, 3),
	p_insolvenzgeldumlagesatz_in_prozent decimal(5, 3),
	p_anders varchar(16),
	p_eintragungsdatum date
) returns void as
$$
declare
	v_krankenkasse_id integer;
	v_umlage_id integer;
begin
    
    set session role tenant_user;
    execute 'SET app.current_tenant=' || p_mandant_id;
   
    -- Pruefen, ob gemeldete Krankenkasse bereits vorhanden ist...
   	execute 'SELECT gemeldete_krankenkasse_id FROM gemeldete_krankenkassen WHERE gemeldete_krankenkasse = $1' into v_krankenkasse_id using p_krankenkasse;
    
    -- ... und falls sie bereits existiert, Meldung ausgeben, dass die Daten nicht mehr eingetragen werden muessen, ...
    if v_krankenkasse_id is not null then
    
		set role postgres;
		raise exception 'Gemeldete Krankenkasse ''%'' ist bereits vorhanden! Uebergebene Daten werden nicht eingetragen! Wenn Sie diese Daten aktualisieren wollen, nutzen Sie bitte die ''update_gemeldete_Krankenkasse''-Funktion!', p_krankenkasse;   
    
	--... ansonsten neue Krankenkasse eintragen und id ziehen, da als Schluessel fuer Assoziation 'hat_Umlagen_anderweitig' benoetigt
	else
	
		insert into gemeldete_Krankenkassen(Mandant_ID, gemeldete_Krankenkasse, Krankenkassenkuerzel)
    		values(p_mandant_id, p_krankenkasse, p_krankenkassenkuerzel);
    
		execute 'SELECT gemeldete_krankenkasse_id FROM gemeldete_krankenkassen WHERE gemeldete_krankenkasse = $1' into v_krankenkasse_id using p_krankenkasse;
	
	end if;
   	
   	-- Pruefen, ob die Umlagesaetze bereits vorhanden sind...
   	execute 'SELECT umlage_id FROM umlagen WHERE u1_umlagesatz_in_prozent = $1 AND u2_umlagesatz_in_prozent = $2 AND insolvenzgeldumlagesatz_in_prozent = $3 AND privat_gesetzlich_oder_anders = $4'
	   		into v_umlage_id using p_u1_umlagesatz_in_prozent, p_u2_umlagesatz_in_prozent, p_insolvenzgeldumlagesatz_in_prozent, p_anders;
	
	-- ... falls nicht, dann eintragen
   	if v_umlage_id is null then
		
		insert into Umlagen(Mandant_ID, U1_Umlagesatz_in_Prozent, U2_Umlagesatz_in_Prozent, Insolvenzgeldumlagesatz_in_Prozent, privat_gesetzlich_oder_anders)
   			values (p_mandant_id, p_u1_umlagesatz_in_prozent, p_u2_umlagesatz_in_prozent, p_insolvenzgeldumlagesatz_in_prozent, p_anders);
   		
   		-- Nochmal v_umlage_id ziehen, da diese als Schluessel fuer die Assoziation 'hat_Umlagen_gesetzlich' benoetigt wird
   		execute 'SELECT umlage_id FROM umlagen WHERE u1_umlagesatz_in_prozent = $1 AND u2_umlagesatz_in_prozent = $2 AND insolvenzgeldumlagesatz_in_prozent = $3 AND privat_gesetzlich_oder_anders = $4'
	   		into v_umlage_id using p_u1_umlagesatz_in_prozent, p_u2_umlagesatz_in_prozent, p_insolvenzgeldumlagesatz_in_prozent, p_anders;
   		
	end if;
    
   	-- Datensatz in Assoziation 'hat_Umlagen_anders', welche die Tabellen 'gemeldete_Krankenkassen' und 'Umlagen' verbindet, eintragen
    insert into hat_Umlagen_anderweitig(gemeldete_Krankenkasse_ID, Umlage_ID, Mandant_ID, Datum_Von, Datum_Bis)
   		values (v_krankenkasse_id, v_umlage_id, p_mandant_id, p_eintragungsdatum, '9999-12-31');

    set role postgres;

exception
    when unique_violation then
    	set role postgres;
        raise exception 'Gemeldete Krankenkasse ''%'' oder dessen Kuerzel ''%'' bereits vorhanden!', p_krankenkasse, p_krankenkassenkuerzel;

end;
$$
language plpgsql;





----------------------------------------------------------------------------------------------------------------
-- Stored Procedure für Use Case "Eintrag neue Kinderanzahl"

/*
 * Funktion trägt neue Daten bzgl. der Anzahl der Kinder ein.
 */
create or replace function insert_anzahl_kinder_an_pv_beitrag (
	p_mandant_id integer,
	p_anzahl_kinder integer,
	p_an_anteil_pv_beitrag_in_prozent decimal(5, 3),
	p_beitragsbemessungsgrenze_pv_ost decimal(10, 2),
	p_beitragsbemessungsgrenze_pv_west decimal(10, 2),
	p_eintragungsdatum date
) returns void as
$$
declare
	v_anzahl_kinder_unter_25_id integer;
	v_an_pv_beitrag_id integer;
begin
    
    set session role tenant_user;
    execute 'SET app.current_tenant=' || p_mandant_id;
    
   	-- Pruefen, ob Anzahl Kinder unter 25 bereits vorhanden ist...
   	execute 'SELECT anzahl_kinder_unter_25_id FROM anzahl_kinder_unter_25 WHERE anzahl_kinder = $1' 
   		into v_anzahl_kinder_unter_25_id using p_anzahl_kinder;
    
    -- ... und falls sie bereits existiert, Meldung ausgeben, dass die Daten nicht mehr eingetragen werden müssen
    if v_anzahl_kinder_unter_25_id is not null then
    
		set role postgres;
		raise exception 'Kinderanzahl ''%'' ist bereits vorhanden! Uebergebene Daten werden nicht eingetragen! Wenn Sie diese Daten aktualisieren wollen, nutzen Sie bitte die ''update_anzahl_kinder''-Funktion!', p_anzahl_kinder; 
	
	--... ansonsten neue Kinderanzahl eintragen und id ziehen, da als Schluessel fuer Assoziation 'hat_gesetzlichen_AN_PV_Beitragssatz' benoetigt
	else
	
		insert into Anzahl_Kinder_unter_25(Mandant_ID, Anzahl_Kinder)
   			values (p_mandant_id, p_anzahl_kinder);

		execute 'SELECT anzahl_kinder_unter_25_id FROM anzahl_kinder_unter_25 WHERE anzahl_kinder = $1' 
			into v_anzahl_kinder_unter_25_id using p_anzahl_kinder;
	
    end if;
    
	-- Pruefen, ob die Beitrags- und Beitragsbemessungsgrenzen-Kombination bereits vorhanden ist...
   	execute 'SELECT 
				an_pv_beitrag_id
			 FROM 
				an_pflegeversicherungsbeitraege_gesetzlich
			 WHERE 
				an_anteil_pv_beitrag_in_prozent = $1 AND
				beitragsbemessungsgrenze_pv_ost = $2 AND
				beitragsbemessungsgrenze_pv_west = $3' 
   			into 
   				v_an_pv_beitrag_id
			using 
				p_an_anteil_pv_beitrag_in_prozent,
				p_beitragsbemessungsgrenze_pv_ost,
				p_beitragsbemessungsgrenze_pv_west;
   	
	-- ... falls nicht, dann eintragen
   	if v_an_pv_beitrag_id is null then
	   	insert into AN_Pflegeversicherungsbeitraege_gesetzlich(Mandant_ID, 
	   														   AN_Anteil_PV_Beitrag_in_Prozent, 
	   														   Beitragsbemessungsgrenze_PV_Ost, 
	   														   Beitragsbemessungsgrenze_PV_West)
	   		values (p_mandant_id, 
	   				p_an_anteil_pv_beitrag_in_prozent,
					p_beitragsbemessungsgrenze_pv_ost,
					p_beitragsbemessungsgrenze_pv_west);
		
		-- Nochmal an_pv_beitrag_id ziehen, da diese als Schluessel fuer die Assoziation 'hat_GKV_Zusatzbeitrag' benoetigt wird
		execute 'SELECT 
					an_pv_beitrag_id
				 FROM 
					an_pflegeversicherungsbeitraege_gesetzlich
				 WHERE 
					an_anteil_pv_beitrag_in_prozent = $1 AND
					beitragsbemessungsgrenze_pv_ost = $2 AND
					beitragsbemessungsgrenze_pv_west = $3' 
	   			into 
	   				v_an_pv_beitrag_id
				using 
					p_an_anteil_pv_beitrag_in_prozent,
					p_beitragsbemessungsgrenze_pv_ost,
					p_beitragsbemessungsgrenze_pv_west;
	end if;
	
	-- Datensatz in Assoziation 'hat_gesetzlichen_AN_PV_Beitragssatz', welche die Tabellen 'Anzahl_Kinder_unter_25' und 
	-- 'AN_Pflegeversicherungsbeitraege_gesetzlich' verbindet, eintragen
	insert into hat_gesetzlichen_AN_PV_Beitragssatz(Anzahl_Kinder_unter_25_ID, AN_PV_Beitrag_ID, Mandant_ID, Datum_Von, Datum_Bis)
   		values (v_anzahl_kinder_unter_25_id, v_an_pv_beitrag_id, p_mandant_id, p_eintragungsdatum, '9999-12-31');
   	
    set role postgres;

end;
$$
language plpgsql;





----------------------------------------------------------------------------------------------------------------
-- Stored Procedure für Use Case "Eintrag Sachsen"

/*
 * Funktion trägt neue Daten in Bezug auf die Frage ein, ob jemand in Sachsen wohnhaft ist. (Wichtig für Bestimmung des AG-Anteil zur Pflegeversicherung).
 */
create or replace function insert_sachsen(
	p_mandant_id integer,
	p_in_sachsen boolean,
	p_ag_anteil_pv_beitrag_in_prozent decimal(5, 3),
	p_eintragungsdatum date
) returns void as
$$
declare
	v_arbeitsort_sachsen_id integer;
	v_ag_pv_beitrag_id integer;
begin
    
    set session role tenant_user;
    execute 'SET app.current_tenant=' || p_mandant_id;
    
   	-- Pruefen, ob Wahrheitswert für Sachsen-Frage bereits vorhanden ist...
   	execute 'SELECT arbeitsort_sachsen_id FROM arbeitsort_sachsen WHERE in_sachsen = $1' into v_arbeitsort_sachsen_id using p_in_sachsen;
    
    -- ... und falls sie bereits existiert, Meldung ausgeben, dass die Daten nicht mehr eingetragen werden muessen
    if v_arbeitsort_sachsen_id is not null then
    
		set role postgres;
		raise exception 'arbeitsort_sachsen = ''%'' ist bereits vorhanden! Uebergebene Daten werden nicht eingetragen! Wenn Sie diese Daten aktualisieren wollen, nutzen Sie bitte die ''update_arbeitsort_sachsen''-Funktion!', p_in_sachsen;   
	
	--... ansonsten eintragen und id ziehen, da als Schluessel fuer Assoziation 'hat_gesetzlichen_AG_PV_Beitragssatz' benoetigt
	else
	
		insert into arbeitsort_sachsen(Mandant_ID, in_Sachsen)
   			values (p_mandant_id, p_in_sachsen);
		
		execute 'SELECT arbeitsort_sachsen_id FROM arbeitsort_sachsen WHERE in_sachsen = $1' into v_arbeitsort_sachsen_id using p_in_sachsen;
	
    end if;
    
    -- Pruefen, ob der AG-PV-Beitragssatz bereits vorhanden ist...
   	execute 'SELECT ag_pv_beitrag_id FROM ag_pflegeversicherungsbeitraege_gesetzlich WHERE ag_anteil_pv_beitrag_in_prozent = $1'
	   		into v_ag_pv_beitrag_id using p_ag_anteil_pv_beitrag_in_prozent;
	
	-- ... falls nicht, dann eintragen
   	if v_ag_pv_beitrag_id is null then
		
		insert into AG_Pflegeversicherungsbeitraege_gesetzlich(Mandant_ID, AG_Anteil_PV_Beitrag_in_Prozent)
   			values (p_mandant_id, p_ag_anteil_pv_beitrag_in_prozent);
   		
   		-- Nochmal ag_pv_beitrag_id ziehen, da diese als Schluessel fuer die Assoziation 'hat_gesetzlichen_AG_PV_Beitragssatz' benoetigt wird
   		execute 'SELECT ag_pv_beitrag_id FROM ag_pflegeversicherungsbeitraege_gesetzlich WHERE ag_anteil_pv_beitrag_in_prozent = $1'
	   		into v_ag_pv_beitrag_id using p_ag_anteil_pv_beitrag_in_prozent;
   		
	end if;
    
	-- Datensatz in Assoziation 'hat_gesetzlichen_AG_PV_Beitragssatz', welche die Tabellen 'arbeitsort_sachsen' und 
	-- 'AG_Pflegeversicherungsbeitraege_gesetzlich' verbindet, eintragen
    insert into hat_gesetzlichen_AG_PV_Beitragssatz(arbeitsort_sachsen_ID, AG_PV_Beitrag_ID, Mandant_ID, Datum_Von, Datum_Bis)
   		values (v_arbeitsort_sachsen_id, v_ag_pv_beitrag_id, p_mandant_id, p_eintragungsdatum, '9999-12-31');

    set role postgres;

end;
$$
language plpgsql;






----------------------------------------------------------------------------------------------------------------
-- Stored Procedure für Use Case "Eintrag neue Arbeitslosenversicherungsbeitraege"

/*
 * Funktion trägt neue Daten bzgl. Arbeitslosenversicherungsbeitraege und Beitragsbemessungsgrenzen ein
 */
create or replace function insert_arbeitslosenversicherungsbeitraege (
	p_mandant_id integer,
	p_ag_arbeitslosenversicherungsbeitrag_in_prozent decimal(5, 3),
	p_an_arbeitslosenversicherungsbeitrag_in_prozent decimal(5, 3),
	p_beitragsbemessungsgrenze_av_ost decimal(10, 2),
	p_beitragsbemessungsgrenze_av_west decimal(10, 2),
	p_eintragungsdatum date
) returns void as
$$
declare
	v_arbeitslosenversicherungsbeitrag_id integer;
	v_arbeitslosenversicherung_id integer;
begin
    
    set session role tenant_user;
    execute 'SET app.current_tenant=' || p_mandant_id;
   
   	-- Jeder Mandant hat nur maximal einen Eintrag. Prüfen, ob dieser bereits vorhanden ist...
   	execute 'SELECT arbeitslosenversicherung_id FROM Arbeitslosenversicherungen' into v_arbeitslosenversicherung_id;
    
    -- ... und falls sie bereits existiert, Meldung ausgeben, dass die Daten nicht mehr eingetragen werden muessen
    if v_arbeitslosenversicherung_id is not null then
    
		set role postgres;
		raise exception 'Arbeitslosenversicherung ist bereits vorhanden! Uebergebene Daten werden nicht eingetragen! Wenn Sie diese Daten aktualisieren wollen, nutzen Sie bitte die ''update_arbeitslosenversicherung''-Funktion!';   
	
	--... ansonsten eintragen und id ziehen, da als Schluessel fuer Assoziation 'hat_AV_Beitraege' benoetigt
	else
	
		insert into Arbeitslosenversicherungen(Mandant_ID)
	   		values (p_mandant_id);	
		
		execute 'SELECT arbeitslosenversicherung_id FROM Arbeitslosenversicherungen' into v_arbeitslosenversicherung_id;
	
    end if;

    -- Pruefen, ob die Beitrags- und Beitragsbemessungsgrenzen-Kombination bereits vorhanden ist...
   	execute 'SELECT 
				arbeitslosenversicherungsbeitrag_id
			 FROM 
				arbeitslosenversicherungsbeitraege 
			 WHERE 
				ag_arbeitslosenversicherungsbeitrag_in_prozent = $1 AND
				an_arbeitslosenversicherungsbeitrag_in_prozent = $2 AND
				beitragsbemessungsgrenze_av_ost = $3 AND
				beitragsbemessungsgrenze_av_west = $4' 
   			into 
   				v_arbeitslosenversicherungsbeitrag_id
			using 
				p_ag_arbeitslosenversicherungsbeitrag_in_prozent, 
				p_an_arbeitslosenversicherungsbeitrag_in_prozent,
				p_beitragsbemessungsgrenze_av_ost,
				p_beitragsbemessungsgrenze_av_west;
	
	-- ... falls nicht, dann eintragen
   	if v_arbeitslosenversicherungsbeitrag_id is null then
		
		insert into
	   		Arbeitslosenversicherungsbeitraege(Mandant_ID, 
									   		   AG_Arbeitslosenversicherungsbeitrag_in_Prozent,
											   AN_Arbeitslosenversicherungsbeitrag_in_Prozent,
											   Beitragsbemessungsgrenze_AV_Ost,
											   Beitragsbemessungsgrenze_AV_West)
	   	values
	   		(p_mandant_id,
	   		 p_ag_arbeitslosenversicherungsbeitrag_in_prozent, 
			 p_an_arbeitslosenversicherungsbeitrag_in_prozent,
			 p_beitragsbemessungsgrenze_av_ost,
			 p_beitragsbemessungsgrenze_av_west);
   		
   		-- Nochmal v_arbeitslosenversicherungsbeitrag_id ziehen , da diese als Schluessel fuer die Assoziation 'hat_AV_Beitraege' benoetigt wird
   		execute 'SELECT 
					arbeitslosenversicherungsbeitrag_id
				 FROM 
					arbeitslosenversicherungsbeitraege 
				 WHERE 
					ag_arbeitslosenversicherungsbeitrag_in_prozent = $1 AND
					an_arbeitslosenversicherungsbeitrag_in_prozent = $2 AND
					beitragsbemessungsgrenze_av_ost = $3 AND
					beitragsbemessungsgrenze_av_west = $4' 
	   			into 
	   				v_arbeitslosenversicherungsbeitrag_id
				using 
					p_ag_arbeitslosenversicherungsbeitrag_in_prozent, 
					p_an_arbeitslosenversicherungsbeitrag_in_prozent,
					p_beitragsbemessungsgrenze_av_ost,
					p_beitragsbemessungsgrenze_av_west;
   		
	end if;

	-- Datensatz in Assoziation 'hat_AV_Beitraege', welche die Tabellen 'Arbeitslosenversicherungen' und 
	-- 'Arbeitslosenversicherungsbeitraege' verbindet, eintragen
    insert into hat_AV_Beitraege(Arbeitslosenversicherung_ID, Arbeitslosenversicherungsbeitrag_ID, Mandant_ID, Datum_Von, Datum_Bis)
   		values (v_arbeitslosenversicherung_id, v_arbeitslosenversicherungsbeitrag_id, p_mandant_id, p_eintragungsdatum, '9999-12-31');
    
    set role postgres;

end;
$$
language plpgsql;





----------------------------------------------------------------------------------------------------------------
-- Stored Procedure für Use Case "Eintrag neue Rentenversicherungsbeitraege"

/*
 * Funktion trägt neue Daten bzgl. Rentenversicherungsbeitraege und Beitragsbemessungsgrenzen ein
 */
create or replace function insert_rentenversicherungsbeitraege(
	p_mandant_id integer,
	p_ag_rentenversicherungsbeitrag_in_prozent decimal(5, 3),
	p_an_rentenversicherungsbeitrag_in_prozent decimal(5, 3),
	p_beitragsbemessungsgrenze_rv_ost decimal(10, 2),
	p_beitragsbemessungsgrenze_rv_west decimal(10, 2),
	p_eintragungsdatum date
) returns void as
$$
declare
	v_rentenversicherungsbeitrag_id integer;
	v_rentenversicherung_id integer;
begin
    
    set session role tenant_user;
    execute 'SET app.current_tenant=' || p_mandant_id;
   
   
   
	-- Jeder Mandant hat nur maximal einen Eintrag. Prüfen, ob dieser bereits vorhanden ist...
   	execute 'SELECT rentenversicherung_id FROM Rentenversicherungen' into v_rentenversicherung_id;
    
    -- ... und falls sie bereits existiert, Meldung ausgeben, dass die Daten nicht mehr eingetragen werden muessen
    if v_rentenversicherung_id is not null then
    
		set role postgres;
		raise exception 'Rentenversicherung ist bereits vorhanden! Uebergebene Daten werden nicht eingetragen! Wenn Sie diese Daten aktualisieren wollen, nutzen Sie bitte die ''update_rentenversicherung''-Funktion!';   
	
	--... ansonsten eintragen und id ziehen, da als Schluessel fuer Assoziation 'hat_RV_Beitraege' benoetigt
	else
	
		insert into Rentenversicherungen(Mandant_ID)
	   		values (p_mandant_id);	
		
		execute 'SELECT rentenversicherung_id FROM Rentenversicherungen' into v_rentenversicherung_id;
	
    end if;   
   
   	-- Pruefen, ob die Beitrags- und Beitragsbemessungsgrenzen-Kombination bereits vorhanden ist...
   	execute 'SELECT 
				rentenversicherungsbeitrag_id
			 FROM 
				rentenversicherungsbeitraege 
			 WHERE 
				ag_rentenversicherungsbeitrag_in_prozent = $1 AND
				an_rentenversicherungsbeitrag_in_prozent = $2 AND
				beitragsbemessungsgrenze_rv_ost = $3 AND
				beitragsbemessungsgrenze_rv_west = $4' 
   			into 
   				v_rentenversicherungsbeitrag_id
			using 
				p_ag_rentenversicherungsbeitrag_in_prozent, 
				p_an_rentenversicherungsbeitrag_in_prozent,
				p_beitragsbemessungsgrenze_rv_ost,
				p_beitragsbemessungsgrenze_rv_west;
	
	-- ... falls nicht, dann eintragen
   	if v_rentenversicherungsbeitrag_id is null then
		
		insert into
	   		Rentenversicherungsbeitraege(Mandant_ID, 
							   		     AG_Rentenversicherungsbeitrag_in_Prozent,
									     AN_Rentenversicherungsbeitrag_in_Prozent,
									     Beitragsbemessungsgrenze_RV_Ost,
									     Beitragsbemessungsgrenze_RV_West)
	   	values
	   		(p_mandant_id,
	   		 p_ag_rentenversicherungsbeitrag_in_prozent, 
			 p_an_rentenversicherungsbeitrag_in_prozent,
			 p_beitragsbemessungsgrenze_rv_ost,
			 p_beitragsbemessungsgrenze_rv_west);
   		
   		-- Nochmal v_rentenversicherungsbeitrag_id ziehen, da diese als Schluessel fuer die Assoziation 'hat_RV_Beitraege' benoetigt wird
   		execute 'SELECT 
					rentenversicherungsbeitrag_id
				 FROM 
					rentenversicherungsbeitraege 
				 WHERE 
					ag_rentenversicherungsbeitrag_in_prozent = $1 AND
					an_rentenversicherungsbeitrag_in_prozent = $2 AND
					beitragsbemessungsgrenze_rv_ost = $3 AND
					beitragsbemessungsgrenze_rv_west = $4' 
	   			into 
	   				v_rentenversicherungsbeitrag_id
				using 
					p_ag_rentenversicherungsbeitrag_in_prozent, 
					p_an_rentenversicherungsbeitrag_in_prozent,
					p_beitragsbemessungsgrenze_rv_ost,
					p_beitragsbemessungsgrenze_rv_west;
   		
	end if;
    
	-- Datensatz in Assoziation 'hat_RV_Beitraege', welche die Tabellen 'Rentenversicherungen' und 
	-- 'Rentenversicherungsbeitraege' verbindet, eintragen
    insert into hat_RV_Beitraege(Rentenversicherung_ID, Rentenversicherungsbeitrag_ID, Mandant_ID, Datum_Von, Datum_Bis)
   		values (v_rentenversicherung_id, v_rentenversicherungsbeitrag_id, p_mandant_id, p_eintragungsdatum, '9999-12-31');
    
    set role postgres;

end;
$$
language plpgsql;





----------------------------------------------------------------------------------------------------------------
-- Stored Procedure für Use Case "Eintrag neue Minijobdaten"

/*
 * Funktion trägt neue Daten bzgl. Rentenversicherungsbeitraege und Beitragsbemessungsgrenzen ein
 */
create or replace function insert_Minijob(
	p_mandant_id integer,
	p_kurzfristig_beschaeftigt boolean,
	p_ag_krankenversicherungsbeitrag_in_prozent decimal(5, 3),
	p_ag_rentenversicherungsbeitrag_in_prozent decimal(5, 3),
	p_an_rentenversicherungsbeitrag_in_prozent decimal(5, 3),
	p_u1_umlage_in_prozent decimal(5, 3),
	p_u2_umlage_in_prozent decimal(5, 3),
	p_insolvenzgeldumlage_in_prozent decimal(5, 3),
	p_pauschalsteuer_in_prozent decimal(5, 3),
	p_eintragungsdatum date
) returns void as
$$
declare
	v_minijob_id integer;
	v_pauschalabgabe_id integer;
begin
    
    set session role tenant_user;
    execute 'SET app.current_tenant=' || p_mandant_id;
   
	-- Pruefen, ob Wahrheitswert für Frage, ob kurzfristige BEschaeftigung vorliegt, bereits vorhanden ist...
   	execute 'SELECT minijob_id FROM minijobs WHERE kurzfristig_beschaeftigt = $1' into v_minijob_id using p_kurzfristig_beschaeftigt;
    
    -- ... und falls sie bereits existiert, Meldung ausgeben, dass die Daten nicht mehr eingetragen werden muessen
    if v_minijob_id is not null then
    
		set role postgres;
		raise exception 'Kurzfristige Beschaeftigung = ''%'' ist bereits vorhanden! Uebergebene Daten werden nicht eingetragen! Wenn Sie diese Daten aktualisieren wollen, nutzen Sie bitte die ''update_Minijob''-Funktion!', p_kurzfristig_beschaeftigt;   
	
	--... ansonsten eintragen und id ziehen, da als Schluessel fuer Assoziation 'hat_Pauschalabgaben' benoetigt
	else
	
		insert into Minijobs(Mandant_ID, kurzfristig_beschaeftigt)
	   		values (p_mandant_id, p_kurzfristig_beschaeftigt);	
		
		execute 'SELECT minijob_id FROM minijobs WHERE kurzfristig_beschaeftigt = $1' into v_minijob_id using p_kurzfristig_beschaeftigt;
	
    end if;   
   
   	-- Pruefen, ob die BeitragsKombination bereits vorhanden ist...
   	execute 'SELECT 
				pauschalabgabe_id
			 FROM 
				pauschalabgaben
			 WHERE 
				ag_krankenversicherungsbeitrag_in_prozent = $1 AND
				ag_rentenversicherungsbeitrag_in_prozent = $2 AND
				an_rentenversicherungsbeitrag_in_prozent = $3 AND
				u1_umlage_in_prozent = $4 AND
				u2_umlage_in_prozent = $5 AND
				insolvenzgeldumlage_in_prozent = $6 AND
				pauschalsteuer_in_prozent = $7' 
   			into 
   				v_pauschalabgabe_id
			using 
				p_ag_krankenversicherungsbeitrag_in_prozent,
				p_ag_rentenversicherungsbeitrag_in_prozent,
				p_an_rentenversicherungsbeitrag_in_prozent,
				p_u1_umlage_in_prozent,
				p_u2_umlage_in_prozent,
				p_insolvenzgeldumlage_in_prozent,
				p_pauschalsteuer_in_prozent;
	
	-- ... falls nicht, dann eintragen
   	if v_pauschalabgabe_id is null then
		
		insert into
	   		Pauschalabgaben(Mandant_ID,
							AG_Krankenversicherungsbeitrag_in_Prozent,
							AG_Rentenversicherungsbeitrag_in_Prozent,
							AN_Rentenversicherungsbeitrag_in_Prozent,
							U1_Umlage_in_Prozent,
							U2_Umlage_in_Prozent,
							Insolvenzgeldumlage_in_Prozent,
							Pauschalsteuer_in_Prozent)
	   	values
	   		(p_mandant_id,
	   		 p_ag_krankenversicherungsbeitrag_in_prozent,
			 p_ag_rentenversicherungsbeitrag_in_prozent,
			 p_an_rentenversicherungsbeitrag_in_prozent,
			 p_u1_umlage_in_prozent,
			 p_u2_umlage_in_prozent,
			 p_insolvenzgeldumlage_in_prozent,
			 p_pauschalsteuer_in_prozent
			);
   		
   		-- Nochmal v_pauschalabgabe_id ziehen, da diese als Schluessel fuer die Assoziation 'hat_Pauschalabgaben' benoetigt wird
   		execute 'SELECT 
					pauschalabgabe_id
				 FROM 
					pauschalabgaben
				 WHERE 
					ag_krankenversicherungsbeitrag_in_prozent = $1 AND
					ag_rentenversicherungsbeitrag_in_prozent = $2 AND
					an_rentenversicherungsbeitrag_in_prozent = $3 AND
					u1_umlage_in_prozent = $4 AND
					u2_umlage_in_prozent = $5 AND
					insolvenzgeldumlage_in_prozent = $6 AND
					pauschalsteuer_in_prozent = $7' 
	   			into 
	   				v_pauschalabgabe_id
				using 
					p_ag_krankenversicherungsbeitrag_in_prozent,
					p_ag_rentenversicherungsbeitrag_in_prozent,
					p_an_rentenversicherungsbeitrag_in_prozent,
					p_u1_umlage_in_prozent,
					p_u2_umlage_in_prozent,
					p_insolvenzgeldumlage_in_prozent,
					p_pauschalsteuer_in_prozent;
   		
	end if;
    
	-- Datensatz in Assoziation 'hat_Pauschalabgaben', welche die Tabellen 'Minijobs' und 'Pauschalabgaben' verbindet, eintragen
    insert into hat_Pauschalabgaben(Minijob_ID, Pauschalabgabe_ID, Mandant_ID, Datum_Von, Datum_Bis)
   		values (v_minijob_id, v_pauschalabgabe_id, p_mandant_id, p_eintragungsdatum, '9999-12-31');
    
    set role postgres;

end;
$$
language plpgsql;





----------------------------------------------------------------------------------------------------------------
-- Stored Procedures für Use Case "Eintrag neuer Tarif inkl. Gewerkschaft, Verguetung und. evtl. Beihilfen"

/*
 * Funktion trägt neue Daten in Tabelle 'Gewerkschaften' ein.
 */
create or replace function insert_gewerkschaft(
	p_mandant_id integer,
	p_gewerkschaft varchar(64),
	p_branche varchar(64)
) returns void as
$$
begin
    
    set session role tenant_user;
    execute 'SET app.current_tenant=' || p_mandant_id;

    insert into 
   		Gewerkschaften(Mandant_ID, Gewerkschaft, Branche)
   	values 
   		(p_mandant_id, p_gewerkschaft, p_branche);
    
    set role postgres;
   
exception
    when unique_violation then
        raise notice 'Gewerkschaft ''%'' bereits vorhanden!', p_gewerkschaft;
           
end;
$$
language plpgsql;

/*
 * Funktion trägt neue Tarif-Daten ein.
 */
create or replace function insert_tarif(
	p_mandant_id integer,
	p_tarifbezeichnung varchar(16),
	p_gewerkschaft varchar(64),
	p_branche varchar(64)
) returns void as
$$
declare
	v_gewerkschaft_id integer;
	v_tarif_id integer;
begin
    
    set session role tenant_user;
    execute 'SET app.current_tenant=' || p_mandant_id;
    
   	-- Pruefen, ob Gewerkschaft bereits vorhanden ist...
   	execute 'SELECT gewerkschaft_id FROM gewerkschaften WHERE gewerkschaft = $1 AND branche = $2' 
   		into v_gewerkschaft_id using p_gewerkschaft, p_branche;
    
    -- ... und falls sie noch nicht existiert, dann Meldung ausgeben
    if v_gewerkschaft_id is null then
    	set role postgres;
		raise exception 'Gewerkschaft ''%'' existiert nicht! Bittae tragen Sie erst eine Gewerkschaft ein!', p_gewerkschaft; 
    end if;
   
   	-- Pruefen, ob Tarif bereits vorhanden ist...
   	execute 'SELECT tarif_id FROM tarife WHERE tarifbezeichnung = $1' into v_tarif_id using p_tarifbezeichnung;
    
    -- ... und falls sie bereits existiert, Meldung ausgeben
    if v_tarif_id is not null then
    
		set role postgres;
		raise exception 'Tarif ist bereits vorhanden! Übergebene Daten werden nicht eingetragen! Wenn Sie diese Daten aktualisieren wollen, nutzen Sie bitte die ''update_Tarif''-Funktion!';   
	
    end if; 
   
   	-- ... ansonsten eintragen
	insert into Tarife(Mandant_ID, Tarifbezeichnung, Gewerkschaft_ID)
		values(p_mandant_id, p_tarifbezeichnung, v_gewerkschaft_id);

    set role postgres;

end;
$$
language plpgsql;

/*
 * Funktion verknuepft Tarif mit (diversen) Verguetungsbestandteilen- Darunter fallen neben Monatsgehalt, Weihnachtsgeld etc. auch Beamtenbeihilfen, da der Staat verpflichtet ist, 
 * Beamten Beihilfen zu zahlen z.B. für (private) Krankenversicherung, Kinder etc..
 */
create or replace function insert_tarifliches_verguetungsbestandteil(
	p_mandant_id integer,
	p_Verguetungsbestandteil varchar(64),
	p_auszahlungsmonat varchar(16),
	p_tarifbezeichnung varchar(16),
	p_betrag decimal(10, 2),
	p_gueltig_ab date
) returns void as
$$
declare
	v_tarif_id integer;
	v_verguetungsbestandteil_id integer;
begin
    
    set session role tenant_user;
	execute 'SET app.current_tenant=' || p_mandant_id;
	
	insert into Verguetungsbestandteile(Mandant_ID, Verguetungsbestandteil, Auszahlungsmonat) values (p_mandant_id, p_verguetungsbestandteil, p_auszahlungsmonat);

	execute 'SELECT verguetungsbestandteil_id FROM verguetungsbestandteile WHERE Verguetungsbestandteil = $1' 
		into v_verguetungsbestandteil_id using p_Verguetungsbestandteil;


	-- Tarif_ID ziehen, da diese benoetigt wird, um einen Datensatz in der Assoziation 'hat_Verguetungsbestandteil_Tarif' anzulegen
	execute 'SELECT tarif_id FROM tarife WHERE tarifbezeichnung = $1' into v_tarif_id using p_tarifbezeichnung;

	-- ... falls Tarif nicht vorhanden ist, dann Meldung ausgeben, dass dieser erst hinterlegt werden muss!
	if v_tarif_id is null then
		set role postgres;
		raise exception 'Bitte erst Tarif ''%'' anlegen!', p_tarifbezeichnung;
	end if;
	
    insert into hat_Verguetungsbestandteil_Tarif(Tarif_ID, Verguetungsbestandteil_ID, Mandant_ID, Betrag, Datum_Von, Datum_Bis) 
   		values (v_tarif_id, v_verguetungsbestandteil_id, p_mandant_id, p_betrag, p_gueltig_ab, '9999-12-31');
   	
   	set role postgres;

exception
    when unique_violation then
        raise notice 'Tarif ''%'' oder Verguetungsbestandteil ''%'' bereits vorhanden!', p_tarifbezeichnung, p_Verguetungsbestandteil;
    when check_violation then
        raise exception 'Auszahlungsmonat ''%'' nicht vorhanden! Bitte wählen Sie zwischen folgenden Moeglichkeiten: ''jeden Monat'', ''Januar'', ''Februar'', ''Maerz'', ''April'', ''Mai'', ''Juni'', ''Juli'', ''August'', ''September'', ''Oktober'', ''November'', ''Dezember''!', p_auszahlungsmonat;    

end;
$$
language plpgsql;









----------------------------------------------------------------------------------------------------------------
-- Stored Procedure für Use Case "Eintrag neues Geschlecht"
/*
 * Funktion trägt neue Daten in Tabelle 'Geschlechter' ein.
 */
create or replace function insert_geschlecht(
    p_mandant_id integer,
    p_geschlecht varchar(32)
) returns void as
$$
begin
    
    set session role tenant_user;
    execute 'SET app.current_tenant=' || p_mandant_id;

    insert into 
   		Geschlechter(Mandant_ID, Geschlecht) 
   	values 
   		(p_mandant_id, p_geschlecht);
    
    set role postgres;

exception
    when unique_violation then
    	set role postgres;
        raise exception 'Geschlecht ''%'' bereits vorhanden!', p_geschlecht;
    when check_violation then
    	set role postgres;
    	raise exception 'Fuer Geschlechter sind nur folgende Werte erlaubt: ''maennlich'', ''weiblich'', ''divers''!';

end;
$$
language plpgsql;





----------------------------------------------------------------------------------------------------------------
-- Stored Procedure für Use Case "Eintrag neuer Mitarbeitertyp"
/*
 * Funktion trägt neue Daten in Tabelle 'Mitarbeitertypen' ein.
 */
create or replace function insert_mitarbeitertyp(
    p_mandant_id integer,
    p_mitarbeitertyp varchar(32)
) returns void as
$$
begin
    
    set session role tenant_user;
    execute 'SET app.current_tenant=' || p_mandant_id;

    insert into 
   		Mitarbeitertypen(Mandant_ID, Mitarbeitertyp) 
   	values 
   		(p_mandant_id, p_mitarbeitertyp);
    
    set role postgres;

exception
    when unique_violation then
        raise exception 'Mitarbeitertyp ''%'' bereits vorhanden!', p_mitarbeitertyp;

end;
$$
language plpgsql;

----------------------------------------------------------------------------------------------------------------
-- Stored Procedure für Use Case "Eintrag neue Steuerklasse"
/*
 * Funktion trägt neue Daten in Tabelle 'Steuerklasse' ein.
 */
create or replace function insert_steuerklasse(
    p_mandant_id integer,
    p_steuerklasse char(1)
) returns void as
$$
begin
    
    set session role tenant_user;
    execute 'SET app.current_tenant=' || p_mandant_id;

    insert into 
   		Steuerklassen(Mandant_ID, Steuerklasse) 
   	values 
   		(p_mandant_id, p_steuerklasse);
    
    set role postgres;
   	
exception
    when unique_violation then
    	set role postgres;
        raise exception 'Steuerklasse ''%'' bereits vorhanden!', p_steuerklasse;
    when check_violation then
    	set role postgres;
    	raise exception 'Fuer Steuerklassen sind nur folgende Werte erlaubt: 1, 2, 3, 4, 5, 6!';
    
end;
$$
language plpgsql;





----------------------------------------------------------------------------------------------------------------
-- Stored Procedure für Use Case "Eintrag neue Abteilung"
/*
 * Funktion trägt neue Daten in Tabelle 'Abteilungen' ein.
 */
create or replace function insert_abteilung(
    p_mandant_id integer,
    p_abteilung varchar(64),
	p_abkuerzung varchar(16)
) returns void as
$$
begin
    
    set session role tenant_user;
    execute 'SET app.current_tenant=' || p_mandant_id;

    insert into 
   		Abteilungen(Mandant_ID, Abteilung, Abkuerzung, untersteht_Abteilung)
   	values 
   		(p_mandant_id, p_abteilung, p_abkuerzung, null);
    
    set role postgres;

exception
    when unique_violation then
    	set role postgres;
        raise exception 'Abteilung ''%'' oder Abteilungskuerzel ''%'' bereits vorhanden!', p_abteilung, p_abkuerzung;
end;
$$
language plpgsql;





----------------------------------------------------------------------------------------------------------------
--Stored Procedure fuer Use Case "Eintrag neuer Jobtitel" 
/*
 * Funktion trägt neue Daten in Tabelle 'Jobtitel' ein.
 */
create or replace function insert_jobtitel (
	p_mandant_ID integer,
	p_jobtitel varchar(32)
) returns void as
$$
begin
    
    set session role tenant_user;
    execute 'SET app.current_tenant=' || p_mandant_id;

    insert into 
   		Jobtitel(Mandant_ID, Jobtitel)
   	values 
   		(p_mandant_id, p_jobtitel);
    
    set role postgres;

exception
    when unique_violation then
    	set role postgres;
        raise exception 'Jobtitel ''%'' bereits vorhanden!', p_jobtitel;

end;
$$
language plpgsql;





----------------------------------------------------------------------------------------------------------------
--Stored Procedure fuer Use Case "Eintrag neue Erfahrungsstufe" 
/*
 * Funktion trägt neue Daten in Tabelle 'Erfahrungsstufen' ein.
 */
create or replace function insert_erfahrungsstufe (
	p_Mandant_ID integer,
	p_erfahrungsstufe varchar(32) 
) returns void as
$$
begin
    
    set session role tenant_user;
    execute 'SET app.current_tenant=' || p_mandant_id;

    insert into 
   		Erfahrungsstufen(Mandant_ID, Erfahrungsstufe)
   	values 
   		(p_mandant_id, p_erfahrungsstufe);
    
    set role postgres;
   
exception
    when unique_violation then
        raise exception 'Erfahrungsstufe ''%'' bereits vorhanden!', p_erfahrungsstufe;

end;
$$
language plpgsql;





----------------------------------------------------------------------------------------------------------------
--Stored Procedure fuer Use Case "Eintrag neue Gesellschaft" 
/*
 * Funktion trägt neue Daten in Tabelle 'Gesellschaften' ein.
 */
create or replace function insert_gesellschaft(
	p_mandant_id integer,
	p_gesellschaft varchar(128),
	p_abkuerzung varchar (16)
) returns void as
$$
begin
    
    set session role tenant_user;
    execute 'SET app.current_tenant=' || p_mandant_id;

    insert into 
   		Gesellschaften(Mandant_ID, Gesellschaft, Abkuerzung, untersteht_Gesellschaft)
   	values 
   		(p_mandant_id, p_gesellschaft, p_abkuerzung, null);
    
    set role postgres;
   
exception
    when unique_violation then
        raise exception 'Gesellschaft ''%'' oder ''%'' bereits vorhanden!', p_gesellschaft, p_abkuerzung;
           
end;
$$
language plpgsql;





----------------------------------------------------------------------------------------------------------------
-- Stored Procedure fuer Use Case "Eintrag neue Austrottsgrundkategorie" 
/*
 * Funktion trägt die Daten in die Tabelle "Kategorien_Austrittsgruende" ein
 */
create or replace function insert_kategorien_austrittsgruende(
	p_mandant_id integer,
	p_austrittsgrundkategorie varchar(16)
) returns void as
$$
begin

	set session role tenant_user;
    execute 'SET app.current_tenant=' || p_mandant_id;

    insert into 
   		Kategorien_Austrittsgruende(Mandant_ID, Austrittsgrundkategorie) 
   	values 
   		(p_mandant_id, p_austrittsgrundkategorie);

    set role postgres;

exception
    when unique_violation then
        raise exception 'Austrittsgrundkategorie ''%'' bereits vorhanden!', p_austrittsgrundkategorie;
    when check_violation then
    	set role postgres;
    	raise exception 'Fuer Austrittsgrundkategorien sind nur folgende Werte erlaubt: ''verhaltensbedingt'', ''personenbedingt'', ''betriebsbedingt''!';

end;
$$
language plpgsql;





----------------------------------------------------------------------------------------------------------------
-- Stored Procedure fuer Use Case "Eintrag neuer Austrittsgrund" 
/*
 * Funktion trägt die Daten in die Tabelle "Austrittsgruende" ein
 */
create or replace function insert_austrittsgruende(
	p_mandant_id integer,
	p_austrittsgrund varchar(32),
	p_austrittsgrundkategorie varchar(16)
) returns void as
$$
declare
	v_kategorie_austrittsgruende_id integer;
begin

	set session role tenant_user;
    execute 'SET app.current_tenant=' || p_mandant_id;

    execute 'SELECT kategorie_austrittsgruende_id FROM kategorien_austrittsgruende WHERE austrittsgrundkategorie = $1' 
   		into v_kategorie_austrittsgruende_id using lower(p_austrittsgrundkategorie);
    
   	insert into 
   		Austrittsgruende(Mandant_ID, Austrittsgrund, Kategorie_Austrittsgruende_ID) 
   	values 
   		(p_mandant_id, p_austrittsgrund, v_kategorie_austrittsgruende_id);

    set role postgres;
 
exception
    when unique_violation then
        raise exception 'Austrittsgrund ''%'' bereits vorhanden!', p_austrittsgrund;

end;
$$
language plpgsql;





----------------------------------------------------------------------------------------------------------------
--Stored Procedure fuer Use Case "Eintrag neue Berufsgenossenschaft" 
/*
 * Funktion trägt neue Daten in Tabelle 'Berufsgenossenschaften' ein.
 */
create or replace function insert_berufsgenossenschaft(
	p_mandant_id integer,
	p_berufsgenossenschaft varchar(128),
	p_abkuerzung varchar(16)
) returns void as
$$
begin
    
    set session role tenant_user;
    execute 'SET app.current_tenant=' || p_mandant_id;

    insert into 
   		Berufsgenossenschaften(Mandant_ID, Berufsgenossenschaft, Abkuerzung)
   	values 
   		(p_mandant_id, p_berufsgenossenschaft, p_abkuerzung);
    
    set role postgres;
   
exception
    when unique_violation then
        raise exception 'Berufsgenossenschaft ''%'' oder Abkuerzung ''%'' bereits vorhanden!', p_berufsgenossenschaft, p_abkuerzung;
           
end;
$$
language plpgsql;





----------------------------------------------------------------------------------------------------------------
--Stored Procedure fuer Use Case "Eintrag neue Unfallversicherungsbeitraege" 
/*
 * Funktion trägt neue Daten in Tabelle 'Unfallversicherungsbeitraege' ein.
 */
create or replace function insert_unfallversicherungsbeitrag(
	p_mandant_id integer,
	p_gesellschaft varchar(128),
	p_abkuerzung_gesellschaft varchar(16),
	p_berufsgenossenschaft varchar(128),
	p_abkuerzung_berufsgenossenschaft varchar(16),
	p_beitrag decimal(12, 2),
	p_beitragsjahr integer
) returns void as
$$
declare
	v_gesellschaft_id integer;
	v_berufsgenossenschaft_id integer;
begin
	
	set session role tenant_user;
	execute 'SET app.current_tenant=' || p_mandant_id;

	-- Pruefen, ob Gesellschaft bereits in Tabelle 'Gesellschaften' hinterlegt ist...
	execute 'SELECT gesellschaft_id FROM gesellschaften WHERE gesellschaft = $1 AND abkuerzung = $2' into v_gesellschaft_id using p_gesellschaft, p_abkuerzung_gesellschaft;

	-- ... und falls sie nicht existiert, Meldung ausgeben, dass erst die Gesellschaft hinterlegt werden muss!
    if v_gesellschaft_id is null then
		set role postgres;
		raise exception 'Gesellschaft ''%'' mit Abkuerzung ''%'' nicht vorhanden!', p_gesellschaft, p_abkuerzung_gesellschaft;   
    end if;
   
   	-- Pruefen, ob Berufsgenossenschaft bereits in Tabelle 'Berufsgenossenschaften' hinterlegt ist...
	execute 'SELECT berufsgenossenschaft_id FROM berufsgenossenschaften WHERE berufsgenossenschaft = $1 AND abkuerzung = $2' 
		into v_berufsgenossenschaft_id using p_berufsgenossenschaft, p_abkuerzung_berufsgenossenschaft;

	-- ... und falls sie nicht existiert, Meldung ausgeben, dass erst die Berufsgenossenschaft hinterlegt werden muss!
    if v_berufsgenossenschaft_id is null then
		set role postgres;
		raise exception 'Berufsgenossenschaft ''%'' mit Abkkuerzung ''%'' nicht vorhanden!', p_berufsgenossenschaft, p_abkuerzung_berufsgenossenschaft;   
    end if;
    
    insert into Unfallversicherungsbeitraege(Gesellschaft_ID, Berufsgenossenschaft_ID, Mandant_ID, Beitrag, Beitragsjahr) 
   		values (v_gesellschaft_id, v_berufsgenossenschaft_id, p_mandant_id, p_beitrag, p_beitragsjahr);
	
   	set role postgres;

exception
    when unique_violation then
    	set role postgres;
        raise notice 'Unfallversicherungsbeitrag ist fuer das Jahr ''%'' bereits vermerkt!', p_beitragsjahr;
end;
$$
language plpgsql;





----------------------------------------------------------------------------------------------------------------
-- Stored Procedures für Use Case "Eintrag neuer Mitarbeiter"

/*
 * Mit dieser Funktion sollen die Daten eines neuen Mitarbeiters in die Tabelle eingetragen werden
 */
create or replace function insert_mitarbeiterdaten(
	p_mandant_id integer,
	-- Tabelle Mitarbeiterdaten
	p_personalnummer varchar(32),
	p_vorname varchar(64),
	p_zweitname varchar(128),
	p_nachname varchar(64),
	p_geburtsdatum date,
	p_eintrittsdatum date, 
	p_steuernummer varchar(32),
	p_sozialversicherungsnummer varchar(32),
	p_iban varchar(32),
	p_private_telefonnummer varchar(16),
    p_private_emailadresse varchar(64),
    p_dienstliche_telefonnummer varchar(16),
    p_dienstliche_emailadresse varchar(64),
    p_befristet_bis date,
    -- Bereich 'Adresse'
    p_strasse varchar(64),
	p_hausnummer varchar(8),
	p_postleitzahl varchar(16),
	p_stadt varchar(128),
	p_region varchar(128),
	p_land varchar(128),
	-- Bereich 'Geschlecht' 
	p_geschlecht varchar(32),
	-- Bereich 'Mitarbeitertyp'
	p_mitarbeitertyp varchar(32),
	-- Bereich 'Steuerklasse'
	p_steuerklasse char(1),
	-- Bereich 'Wochenarbeitszeit'
	p_wochenarbeitsstunden decimal(4, 2),
	-- Bereich 'p_Abteilung'
	p_abteilung varchar(64),
	p_abk_abteilung varchar(16),
	p_fuehrungskraft boolean,
	-- Bereich 'Jobtitel'
	p_jobtitel varchar(32),
	p_erfahrungsstufe varchar(32),
	-- Bereich 'Gesellschaft'
	p_gesellschaft varchar(128),
	-- Bereich 'Entgelt'
	p_tarifbeschaeftigt boolean,
	p_tarifbezeichnung varchar(16),
	-- Bereich 'Kranken- und Pflegeversicherung'
	p_ist_kurzfristig_beschaeftigt boolean,
	p_krankenkasse varchar(128),
	p_krankenkassenkuerzel varchar(16),
	p_gesetzlich_krankenversichert boolean,
	p_ermaessigter_kv_beitrag boolean,
	p_anzahl_kinder integer,
	p_in_sachsen boolean,
	p_privat_krankenversichert boolean,
	p_ag_zuschuss_krankenversicherung decimal(6, 2),
	p_ag_zuschuss_pflegeversicherung decimal(6, 2),
	p_ist_minijobber boolean,
	p_anderweitig_versichert boolean,
	-- Bereich 'Arbeitslosenversicherung'
	p_arbeitslosenversichert boolean,
	-- Bereich 'Rentenversicherung'
	p_rentenversichert boolean
) returns void as
$$
begin
	
	set session role tenant_user;
	execute 'SET app.current_tenant=' || p_mandant_id;
	
	perform pruefe_einmaligkeit_personalnummer(p_mandant_id, 'mitarbeiter', p_personalnummer);
	
	-- Daten in Tabelle 'Mitarbeiter' eintragen
	perform insert_tbl_mitarbeiter(p_mandant_id, 
								   p_personalnummer, 
								   p_vorname, 
								   p_zweitname, 
								   p_nachname, 
								   p_geburtsdatum, 
								   p_eintrittsdatum, 
								   p_steuernummer, 
								   p_sozialversicherungsnummer, 
								   p_iban, 
								   p_private_telefonnummer, 
								   p_private_emailadresse, 
								   p_dienstliche_telefonnummer, 
								   p_dienstliche_emailadresse,
								   p_befristet_bis
								  );
	
	-- Sofern keines der Adress-Parameter 'null' ist, den Bereich 'Adresse' mit Daten befüllen
	if p_land is not null and p_region is not null and p_stadt is not null and p_postleitzahl is not null and p_strasse is not null and p_hausnummer is not null then
		perform insert_tbl_laender(p_mandant_id, p_land);
		perform insert_tbl_regionen(p_mandant_id, p_region, p_land);
		perform insert_tbl_staedte(p_mandant_id, p_stadt, p_region);
		perform insert_tbl_postleitzahlen(p_mandant_id, p_postleitzahl, p_stadt);
		perform insert_tbl_strassenbezeichnungen(p_mandant_id, p_strasse, p_hausnummer, p_postleitzahl);
		perform insert_tbl_wohnt_in(p_mandant_id, p_personalnummer, p_strasse, p_hausnummer, p_eintrittsdatum);
	end if;
	
	
	-- Sofern p_geschlecht nicht 'null' ist, den Bereich 'Geschlecht' mit Daten befüllen
	if p_geschlecht is not null then
		perform insert_tbl_hat_geschlecht(p_mandant_id, p_personalnummer, p_geschlecht, p_eintrittsdatum);
	end if;
	
	-- Sofern p_mitarbeitertyp nicht 'null' ist, den Bereich 'Mitarbeitertyp' mit Daten befüllen
	if p_mitarbeitertyp is not null then
		perform insert_tbl_ist_mitarbeitertyp(p_mandant_id, p_personalnummer, p_mitarbeitertyp, p_eintrittsdatum);
	end if;

	-- Sofern p_steuerklasse nicht 'null' ist, den Bereich 'Steuerklasse' mit Daten befüllen
	if p_steuerklasse is not null then
		perform insert_tbl_in_steuerklasse(p_mandant_id, p_personalnummer, p_steuerklasse, p_eintrittsdatum);
	end if;
	
	-- Sofern p_wochenarbeitsstunden nicht 'null' ist, den Bereich 'Wochenarbeitsstunden' mit Daten befüllen
	if p_wochenarbeitsstunden is not null then
		perform insert_tbl_wochenarbeitsstunden(p_mandant_id, p_wochenarbeitsstunden);
		perform insert_tbl_arbeitet_x_wochenarbeitsstunden(p_mandant_id, p_personalnummer, p_wochenarbeitsstunden, p_eintrittsdatum);
	end if;

	-- Sofern p_abteilung und p_fuehrungskraft nicht 'null' sind, den Bereich 'Abteilung' mit Daten befüllen
	if p_abteilung is not null and p_fuehrungskraft is not null then
		perform insert_tbl_eingesetzt_in(p_mandant_id, p_personalnummer, p_abteilung, p_abk_abteilung, p_fuehrungskraft, p_eintrittsdatum);
	end if;

	-- Sofern p_jobtitel und p_erfahrungsstufe nicht 'null' sind, den Bereich 'Jobtitel' mit Daten befüllen
	if p_jobtitel is not null and p_erfahrungsstufe is not null then
		perform insert_tbl_hat_jobtitel(p_mandant_id, p_personalnummer, p_jobtitel, p_erfahrungsstufe, p_eintrittsdatum);
	end if;
	
	-- Sofern p_gesellschaft nicht 'null' ist, den Bereich 'Gesellschaft' mit Daten befüllen
	if p_gesellschaft is not null then
		perform insert_tbl_in_gesellschaft(p_mandant_id, p_personalnummer, p_gesellschaft, p_eintrittsdatum);
	end if;
	
	-- sofern neuer Mitarbeiter tariflich bezahlt wird, dann Tarif zuordnen...
	if p_tarifbeschaeftigt is true and p_tarifbezeichnung is not null then 
		perform insert_tbl_hat_tarif(p_mandant_id, p_personalnummer, p_tarifbezeichnung, p_eintrittsdatum);
	end if;
	
	-- ... alternativ ist Mitarbeiter aussertariflich
	if p_tarifbeschaeftigt is false then
		perform insert_tbl_Aussertarifliche(p_personalnummer, 
											p_mandant_id, 
											p_eintrittsdatum);
	end if;
	
	-- Man kann niemals über den Arbeitgeber gesetzlich kranken- und pflegeversichert sein, wenn man kurzfristig beschaeftigt ist.
	-- Der kurzfristig Beschaeftigte muss sich anderweitig um Krankenversicherung kuemmern
	if p_gesetzlich_krankenversichert and p_ist_kurzfristig_beschaeftigt is false then
	
		perform insert_tbl_hat_gesetzliche_Krankenversicherung(p_mandant_id, p_personalnummer, p_ermaessigter_kv_beitrag, p_eintrittsdatum);
		perform insert_tbl_ist_in_gkv(p_mandant_id, p_personalnummer, p_krankenkasse, p_krankenkassenkuerzel, p_eintrittsdatum);
		perform insert_tbl_hat_x_kinder_unter_25(p_mandant_id, p_personalnummer, p_anzahl_kinder, p_eintrittsdatum);
		perform insert_tbl_arbeitet_in_sachsen(p_mandant_id, p_personalnummer, p_in_sachsen, p_eintrittsdatum);									  

	end if;
	
	-- Ein kurzfristig Beschaeftigter ist niemals privat ueber den Arbeitgeber versichert (womit auch kein Anspruch auf Arbeitgeberzuschuss einhergeht)
	if p_privat_krankenversichert and p_ist_kurzfristig_beschaeftigt is false then
		perform insert_tbl_hat_private_krankenversicherung(p_mandant_id, p_personalnummer, p_krankenkasse, p_ag_zuschuss_krankenversicherung, p_ag_zuschuss_krankenversicherung, p_eintrittsdatum);
	end if;

	if p_ist_minijobber then
		perform insert_tbl_ist_Minijobber(p_mandant_id, p_personalnummer, p_ist_kurzfristig_beschaeftigt, p_eintrittsdatum);
	end if;

	-- if-Bedingung für kurzfristig beschaeftigte Nicht-Minijobber, denn die zahlen keine SV, aber Umlagen! Das der Kurzfristig Beschaeftigte aber
	-- aber anderweitig krankenversichert ist, dass muss der Arbeitgeber sicherstellen, weswegen die Krankenkasse vermerkt wird 
	if p_anderweitig_versichert then
		perform insert_tbl_ist_anderweitig_versichert(p_mandant_id, p_personalnummer, p_krankenkasse, p_krankenkassenkuerzel, p_eintrittsdatum);
	end if;

	if p_arbeitslosenversichert and p_ist_kurzfristig_beschaeftigt is not true then
		perform insert_tbl_hat_gesetzliche_arbeitslosenversicherung(p_mandant_id, p_personalnummer, p_eintrittsdatum);
	end if;
	
	if p_rentenversichert and p_ist_kurzfristig_beschaeftigt is not true then
		perform insert_tbl_hat_gesetzliche_rentenversicherung(p_mandant_id, p_personalnummer, p_eintrittsdatum);
	end if;
	
	set role postgres;

end;
$$
language plpgsql;

/*
 * Funktion trägt die Daten in die Tabelle "Mitarbeiter" ein
 */
create or replace function insert_tbl_mitarbeiter(
	p_mandant_id integer,
	p_personalnummer varchar(32),
	p_vorname varchar(64),
	p_zweitname varchar(128),
	p_nachname varchar(64),
	p_geburtsdatum date,
	p_eintrittsdatum date, 
	p_steuernummer varchar(32),
	p_sozialversicherungsnummer varchar(32),
	p_iban varchar(32),
	p_private_telefonnummer varchar(16),
    p_private_emailadresse varchar(64),
    p_dienstliche_telefonnummer varchar(16),
    p_dienstliche_emailadresse varchar(64),
    p_befristet_bis date
) returns void as
$$
begin
	
	set session role tenant_user;
	execute 'SET app.current_tenant=' || p_mandant_id;

	insert into mitarbeiter(Mandant_ID,
							Personalnummer,
						    Vorname,
						    Zweitname,
						    Nachname,
						    Geburtsdatum,
						    Eintrittsdatum, 
						    Steuernummer,
						    Sozialversicherungsnummer,
						    IBAN,
						    Private_Telefonnummer,
						    Private_Emailadresse,
						    dienstliche_Telefonnummer,
						    dienstliche_Emailadresse,
						    Befristet_Bis)
		values(p_mandant_id,
			   p_personalnummer,
			   p_vorname,
			   p_zweitname,
			   p_nachname,
			   p_geburtsdatum,
			   p_eintrittsdatum, 
			   p_steuernummer,
			   p_sozialversicherungsnummer,
			   p_iban,
			   p_private_telefonnummer,
			   p_private_emailadresse,
			   p_dienstliche_telefonnummer,
			   p_dienstliche_emailadresse,
			   p_befristet_bis);    
           
	set role postgres;

exception
    when unique_violation then
    	set role postgres;
        raise exception 'Personalnummer ''%'' bereits vorhanden!', p_personalnummer;  
	
end;
$$
language plpgsql;

/*
 * Funktion trägt die Daten in die Tabelle "Laender" ein
 */
create or replace function insert_tbl_laender(
	p_mandant_id integer,
	p_land varchar(128)
) returns void as
$$
begin

	set session role tenant_user;
    execute 'SET app.current_tenant=' || p_mandant_id;

    insert into 
   		Laender(Mandant_ID, Land) 
   	values 
   		(p_mandant_id, p_land);

    set role postgres;

exception
    when unique_violation then
    	set role postgres;
        raise notice 'Land ''%'' bereits vorhanden!', p_land;
   
end;
$$
language plpgsql;

/*
 * Funktion trägt die Daten in die Tabelle "Regionen" ein
 */
create or replace function insert_tbl_regionen(
	p_mandant_id integer,
	p_region varchar(128),
	p_land varchar(128)
) returns void as
$$
declare
	v_land_id integer;
begin

	set session role tenant_user;
    execute 'SET app.current_tenant=' || p_mandant_id;

    execute 'SELECT land_id FROM laender WHERE land = $1' into v_land_id using p_land;
    
   	insert into 
   		Regionen(Mandant_ID, Region, Land_ID) 
   	values 
   		(p_mandant_id, p_region, v_land_id);

    set role postgres;

exception
    when unique_violation then
    	set role postgres;
        raise notice 'Region ''%'' bereits vorhanden!', p_region;

end;
$$
language plpgsql;

/*
 * Funktion trägt die Daten in die Tabelle "Staedte" ein
 */
create or replace function insert_tbl_staedte(
	p_mandant_id integer,
	p_stadt varchar(128),
	p_region varchar(128)
) returns void as
$$
declare
	v_region_id integer;
begin
	
	set session role tenant_user;
    execute 'SET app.current_tenant=' || p_mandant_id;

    execute 'SELECT region_id FROM regionen WHERE region = $1' into v_region_id using p_region;
    
   	insert into 
   		Staedte(Mandant_ID, Stadt, Region_ID) 
   	values 
   		(p_mandant_id, p_stadt, v_region_id);
    
    set role postgres;

exception
    when unique_violation then
    	set role postgres;
        raise notice 'Stadt ''%'' bereits vorhanden!', p_stadt;

end;
$$
language plpgsql;

/*
 * Funktion trägt die Daten in die Tabelle "Postleitzahlen" ein
 */
create or replace function insert_tbl_postleitzahlen(
	p_mandant_id integer,
	p_postleitzahl varchar(16),
	p_stadt varchar(128)
) returns void as
$$
declare
	v_stadt_id integer;
begin
	
	set session role tenant_user;
    execute 'SET app.current_tenant=' || p_mandant_id;

    execute 'SELECT stadt_id FROM staedte WHERE stadt = $1' into v_stadt_id using p_stadt;
    
   	insert into 
   		Postleitzahlen(Mandant_ID, Postleitzahl, Stadt_ID) 
   	values 
   		(p_mandant_id, p_postleitzahl, v_stadt_id);
    
    set role postgres;
 
exception
    when unique_violation then
    	set role postgres;
        raise notice 'Postleitzahl ''%'' bereits vorhanden!', p_postleitzahl;

end;
$$
language plpgsql;

/*
 * Funktion trägt die Daten in die Tabelle "Strassenbezeichnungen" ein
 */
create or replace function insert_tbl_strassenbezeichnungen(
	p_mandant_id integer,
	p_strasse varchar(64),
	p_hausnummer varchar(8),
	p_postleitzahl varchar(16)
) returns void as
$$
declare
	v_strassenbezeichnung varchar(128);
	v_postleitzahlen_id integer;
begin

	set session role tenant_user;
    execute 'SET app.current_tenant=' || p_mandant_id;

    execute 'SELECT postleitzahl_id FROM postleitzahlen WHERE Postleitzahl = $1' into v_postleitzahlen_id using p_postleitzahl;
	
   	insert into 
		strassenbezeichnungen(Mandant_ID, Strasse, Hausnummer, Postleitzahl_ID) 
	values 
		(p_mandant_id, p_strasse, p_hausnummer, v_postleitzahlen_id);
    
    set role postgres;

exception
        when unique_violation then
        	set role postgres;
        	v_strassenbezeichnung := p_strasse || p_hausnummer;
            raise notice 'Strassenbezeichnung ''%'' bereits vorhanden!', v_strassenbezeichnung;

end;
$$
language plpgsql;

/*
 * Funktion trägt die Daten in die Assoziation "wohnt_in" ein
 */
create or replace function insert_tbl_wohnt_in(
	p_mandant_id integer,
	p_personalnummer varchar(32),
	p_strasse varchar(64),
	p_hausnummer varchar(8),
	p_eintrittsdatum date
) returns void as
$$
declare
	v_mitarbeiter_ID integer;
	v_strassenbezeichnung_id integer;
begin
	
	set session role tenant_user;
	execute 'SET app.current_tenant=' || p_mandant_id;
	
	execute 'SELECT mitarbeiter_ID FROM mitarbeiter WHERE personalnummer = $1' into v_mitarbeiter_ID using p_personalnummer;
	execute 'SELECT strassenbezeichnung_ID FROM strassenbezeichnungen WHERE strasse = $1 AND hausnummer = $2' into v_strassenbezeichnung_id using p_strasse, p_hausnummer;
    
    insert into 
    	wohnt_in(Mitarbeiter_ID, Strassenbezeichnung_ID, Mandant_ID, Datum_Von, Datum_Bis) 
   	values 
   		(v_mitarbeiter_ID, v_strassenbezeichnung_id, p_mandant_id, p_eintrittsdatum, '9999-12-31');
	
   	set role postgres;

exception
    when unique_violation then
    	set role postgres;
        raise notice 'Mitarbeiter ist bereits mit diesem aktuellen Wohnort vermerkt!';
           
end;
$$
language plpgsql;

/*
 * Funktion trägt die Daten in die Assoziation "hat_Geschlecht" ein
 */
create or replace function insert_tbl_hat_geschlecht(
	p_mandant_id integer,
	p_personalnummer varchar(32),
	p_geschlecht varchar(32),
	p_eintrittsdatum date
) returns void as
$$
declare
	v_mitarbeiter_id integer;
	v_geschlecht_id integer;
begin
	
	set session role tenant_user;
	execute 'SET app.current_tenant=' || p_mandant_id;
	
	-- Pruefen, ob Geschlecht bereits in Tabelle 'Geschlechter' hinterlegt ist
	execute 'SELECT geschlecht_ID FROM geschlechter WHERE geschlecht = $1' into v_geschlecht_id using p_geschlecht;

	-- ... und falls nicht, dann Meldung ausgeben, dass das Geschlecht erst hinterlegt werden muss!
	if v_geschlecht_id is null then
		set role postgres;
		raise exception 'Bitte erst Geschlecht ''%'' anlegen!', p_geschlecht;
	end if;

	-- Mitarbeiter_ID ziehen, da diese benoetigt wird, um einen Datensatz in der Assoziation 'in_Steuerklasse' anzulegen
	execute 'SELECT mitarbeiter_ID FROM mitarbeiter WHERE personalnummer = $1' into v_mitarbeiter_ID using p_personalnummer;
	
    insert into hat_Geschlecht(Mitarbeiter_ID, Geschlecht_ID, Mandant_ID, Datum_Von, Datum_Bis) 
   		values (v_mitarbeiter_id, v_geschlecht_id, p_mandant_id, p_eintrittsdatum, '9999-12-31');
   	
   	set role postgres;

exception
        when unique_violation then
            raise notice 'Mitarbeiter ist bereits aktuell Geschlecht ''%''!', p_geschlecht;
   
end;
$$
language plpgsql;

/*
 * Funktion trägt die Daten in die Assoziation "ist_Mitarbeitertyp" ein
 */
create or replace function insert_tbl_ist_mitarbeitertyp(
	p_mandant_id integer,
	p_personalnummer varchar(32),
	p_mitarbeitertyp varchar(32),
	p_eintrittsdatum date
) returns void as
$$
declare
	v_mitarbeiter_id integer;
	v_mitarbeitertyp_id integer;
begin
	
	set session role tenant_user;
	execute 'SET app.current_tenant=' || p_mandant_id;
	
	-- Pruefen, ob Mitarbeitertyp bereits in Tabelle 'Mitarbeitertypen' hinterlegt ist
	execute 'SELECT mitarbeitertyp_ID FROM mitarbeitertypen WHERE mitarbeitertyp = $1' into v_mitarbeitertyp_id using p_mitarbeitertyp;

	-- ... und falls nicht, dann Meldung ausgeben, dass der Mitarbeitertyp erst hinterlegt werden muss!
	if v_mitarbeitertyp_id is null then
		set role postgres;
		raise exception 'Bitte erst Mitarbeitertyp ''%'' anlegen!', p_mitarbeitertyp;
	end if;

	-- Mitarbeiter_ID ziehen, da diese benoetigt wird, um einen Datensatz in der Assoziation 'ist_Mitarbeitertyp' anzulegen
	execute 'SELECT mitarbeiter_ID FROM mitarbeiter WHERE personalnummer = $1' into v_mitarbeiter_ID using p_personalnummer;
    
    insert into ist_Mitarbeitertyp(Mitarbeiter_ID, Mitarbeitertyp_ID, Mandant_ID, Datum_Von, Datum_Bis) 
   		values (v_mitarbeiter_id, v_mitarbeitertyp_id, p_mandant_id, p_eintrittsdatum, '9999-12-31');
	
   	set role postgres;

exception
    when unique_violation then
    	set role postgres;
        raise notice 'Mitarbeiter ist bereits aktuell Mitarbeitertyp''%''!', p_mitarbeitertyp;
   	
end;
$$
language plpgsql;

/*
 * Funktion trägt die Daten in die Assoziation "in_steuerklasse" ein
 */
create or replace function insert_tbl_in_steuerklasse(
	p_mandant_id integer,
	p_personalnummer varchar(32),
	p_steuerklasse char(1),
	p_eintrittsdatum date
) returns void as
$$
declare
	v_mitarbeiter_id integer;
	v_steuerklasse_id integer;
begin
	
	set session role tenant_user;
	execute 'SET app.current_tenant=' || p_mandant_id;
		
	-- Pruefen, ob Steuerklasse bereits in Tabelle 'Steuerklassen' hinterlegt ist...
	execute 'SELECT steuerklasse_id FROM steuerklassen WHERE steuerklasse = $1' into v_steuerklasse_id using p_steuerklasse;
    
    -- ... und falls sie nicht existiert, Meldung ausgeben, dass erst die Steuerklasse hinterlegt werden muss!
    if v_steuerklasse_id is null then
		set role postgres;
			raise exception 'Sie muessen erst die Steuerklasse ''%'' anlegen!', p_steuerklasse;   
    end if;
   
   	-- Mitarbeiter_ID ziehen, da diese benoetigt wird, um einen Datensatz in der Assoziation 'in_Steuerklasse' anzulegen
    execute 'SELECT mitarbeiter_ID FROM mitarbeiter WHERE personalnummer = $1' into v_mitarbeiter_ID using p_personalnummer;
    
    insert into in_Steuerklasse(Mitarbeiter_ID, Steuerklasse_ID, Mandant_ID, Datum_Von, Datum_Bis)
   		values (v_mitarbeiter_id, v_steuerklasse_id, p_mandant_id, p_eintrittsdatum, '9999-12-31');
	
   	set role postgres;

exception
    when unique_violation then
    	set role postgres;
        raise notice 'Es ist bereits vermerkt, dass der Mitarbeiter aktuell in Steuerklasse ''%'' ist!', p_steuerklasse;
   	
end;
$$
language plpgsql;

/*
 * Funktion trägt neue Daten in Tabelle 'Wochenarbeitsstunden' ein.
 */
create or replace function insert_tbl_wochenarbeitsstunden(
    p_mandant_id integer,
    p_wochenarbeitsstunden decimal(4, 2)
) returns void as
$$
begin
    
    set session role tenant_user;
    execute 'SET app.current_tenant=' || p_mandant_id;

    insert into 
   		Wochenarbeitsstunden(Mandant_ID, Anzahl_Wochenstunden) 
   	values 
   		(p_mandant_id, p_wochenarbeitsstunden);
    
    set role postgres;
  
exception
    when unique_violation then
        raise notice 'Wochenarbeitsstunden ''%'' bereits vorhanden!', p_wochenarbeitsstunden;

end;
$$
language plpgsql;

/*
 * Funktion trägt die Daten in die Assoziation "arbeitet_x_Wochenarbeitsstunden" ein
 */
create or replace function insert_tbl_arbeitet_x_wochenarbeitsstunden(
	p_mandant_id integer,
	p_personalnummer varchar(32),
	p_wochenarbeitsstunden decimal(4, 2),
	p_eintrittsdatum date
) returns void as
$$
declare
	v_mitarbeiter_id integer;
	v_wochenarbeitsstunden_id integer;
begin
	
	set session role tenant_user;
	execute 'SET app.current_tenant=' || p_mandant_id;
	
	execute 'SELECT mitarbeiter_ID FROM mitarbeiter WHERE personalnummer = $1' into v_mitarbeiter_ID using p_personalnummer;
	execute 'SELECT wochenarbeitsstunden_ID FROM wochenarbeitsstunden WHERE anzahl_wochenstunden = $1' into v_wochenarbeitsstunden_id using p_wochenarbeitsstunden;
    
    insert into arbeitet_x_Wochenstunden(Mitarbeiter_ID, Wochenarbeitsstunden_ID, Mandant_ID, Datum_Von, Datum_Bis) 
   		values (v_mitarbeiter_id, v_wochenarbeitsstunden_id, p_mandant_id, p_eintrittsdatum, '9999-12-31');
	
   	set role postgres;
   
exception
    when unique_violation then
        raise notice 'Wochenarbeitsstunden von aktuell ''%'' für diesen Mitarbeiter ist bereits vermerkt!', p_wochenarbeitsstunden;
   	
end;
$$
language plpgsql;

/*
 * Funktion trägt die Daten in die Assoziation "eingesetzt_in" ein
 */
create or replace function insert_tbl_eingesetzt_in(
	p_mandant_id integer,
	p_personalnummer varchar(32),
	p_abteilung varchar(64),
	p_abkuerzung varchar(16),
	p_fuehrungskraft boolean,
	p_eintrittsdatum date
) returns void as
$$
declare
	v_mitarbeiter_id integer;
	v_abteilung_id integer;
begin
	
	set session role tenant_user;
	execute 'SET app.current_tenant=' || p_mandant_id;

	-- Pruefen, ob Abteilung bereits in Tabelle 'Abteilungen' hinterlegt ist...
	execute 'SELECT abteilung_id FROM abteilungen WHERE abteilung = $1 AND abkuerzung = $2' into v_abteilung_id using p_abteilung, p_abkuerzung;

	-- ... und falls sie nicht existiert, Meldung ausgeben, dass erst die Abteilung hinterlegt werden muss!
    if v_abteilung_id is null then
		set role postgres;
		raise exception 'Sie muessen erst die Abteilung ''%'' anlegen!', p_abteilung;   
    end if;
   
   	-- Mitarbeiter_ID ziehen, da diese benoetigt wird, um einen Datensatz in der Assoziation 'in_Steuerklasse' anzulegen
    execute 'SELECT mitarbeiter_ID FROM mitarbeiter WHERE personalnummer = $1' into v_mitarbeiter_ID using p_personalnummer;
    
    insert into eingesetzt_in(Mitarbeiter_ID, Abteilung_ID, Mandant_ID, Fuehrungskraft, Datum_Von, Datum_Bis) 
   		values (v_mitarbeiter_id, v_abteilung_id, p_mandant_id, p_fuehrungskraft, p_eintrittsdatum, '9999-12-31');
	
   	set role postgres;

exception
    when unique_violation then
    	set role postgres;
        raise notice 'Mitarbeiter ist bereits in der aktuellen Abteilung ''%'' vermerkt!', p_abteilung;
   
end;
$$
language plpgsql;

/*
 * Funktion trägt die Daten in die Assoziation "hat_Jobtitel" ein
 */
create or replace function insert_tbl_hat_jobtitel(
	p_mandant_id integer,
	p_personalnummer varchar(32),
	p_jobtitel varchar(32),
	p_erfahrungsstufe varchar(32),
	p_eintrittsdatum date
) returns void as
$$
declare
	v_mitarbeiter_id integer;
	v_jobtitel_id integer;
	v_erfahrungsstufe_id integer;
begin
	
	set session role tenant_user;
	execute 'SET app.current_tenant=' || p_mandant_id;
	
	-- Pruefen, ob Jobtitel bereits in Tabelle 'Jobtitel' hinterlegt ist...
	execute 'SELECT jobtitel_ID FROM jobtitel WHERE jobtitel = $1' into v_jobtitel_id using p_jobtitel;

	-- ... und falls sie nicht existiert, Meldung ausgeben, dass erst der Jobtitel hinterlegt werden muss!
    if v_jobtitel_id is null then
		set role postgres;
		raise exception 'Sie muessen erst den Jobtitel ''%'' anlegen!', p_jobtitel;   
    end if;

   	-- Pruefen, ob Erfahrungsstufe bereits in Tabelle 'Erfahrungsstufen' hinterlegt ist...
	execute 'SELECT erfahrungsstufe_ID FROM erfahrungsstufen WHERE erfahrungsstufe = $1' into v_erfahrungsstufe_id using p_erfahrungsstufe;

	-- ... und falls sie nicht existiert, Meldung ausgeben, dass erst die Erfahrungsstufe hinterlegt werden muss!
    if v_erfahrungsstufe_id is null then
		set role postgres;
		raise exception 'Sie muessen erst die Erfahrungsstufe ''%'' anlegen!', p_erfahrungsstufe;   
    end if;
    
   	-- Mitarbeiter_ID ziehen, da diese benoetigt wird, um einen Datensatz in der Assoziation 'hat_Jobtitel' anzulegen
	execute 'SELECT mitarbeiter_ID FROM mitarbeiter WHERE personalnummer = $1' into v_mitarbeiter_ID using p_personalnummer;
	
	-- Mitarbeiter_ID ziehen, da diese benoetigt wird, um einen Datensatz in der Assoziation 'in_Steuerklasse' anzulegen
    insert into hat_Jobtitel(Mitarbeiter_ID, Jobtitel_ID, Erfahrungsstufe_ID, Mandant_ID, Datum_Von, Datum_Bis)
   		values(v_mitarbeiter_ID, v_jobtitel_id, v_erfahrungsstufe_id, p_mandant_id, p_eintrittsdatum, '9999-12-31');
	
   	set role postgres;

exception
    when unique_violation then
        raise notice 'Mitarbeiter hat bereits diesen Jobtitel und Erfahrungsstufe vermerkt!';
   	
end;
$$
language plpgsql;

/*
 * Funktion trägt die Daten in die Assoziation "in_Gesellschaft" ein
 */
create or replace function insert_tbl_in_gesellschaft(
	p_mandant_id integer,
	p_personalnummer varchar(32),
	p_gesellschaft varchar(128),
	p_eintrittsdatum date
) returns void as
$$
declare
	v_mitarbeiter_id integer;
	v_gesellschaft_id integer;
begin
	
	set session role tenant_user;
	execute 'SET app.current_tenant=' || p_mandant_id;

	-- Pruefen, ob Jobtitel bereits in Tabelle 'Jobtitel' hinterlegt ist...
	execute 'SELECT gesellschaft_ID FROM gesellschaften WHERE gesellschaft = $1' into v_gesellschaft_id using p_gesellschaft;
	
	-- ... und falls sie nicht existiert, Meldung ausgeben, dass erst die Gesellschaft hinterlegt werden muss!
    if v_gesellschaft_id is null then
		set role postgres;
		raise exception 'Sie muessen erst die Gesellschaft ''%'' anlegen!', p_gesellschaft;   
    end if;

	-- Mitarbeiter_ID ziehen, da diese benoetigt wird, um einen Datensatz in der Assoziation 'in_Gesellschaft' anzulegen
	execute 'SELECT mitarbeiter_ID FROM mitarbeiter WHERE personalnummer = $1' into v_mitarbeiter_ID using p_personalnummer;
	
    insert into in_Gesellschaft (Mitarbeiter_ID, Gesellschaft_ID, Mandant_ID, Datum_Von, Datum_Bis)
   		values (v_mitarbeiter_ID, v_gesellschaft_id, p_mandant_id, p_eintrittsdatum, '9999-12-31');
	
   	set role postgres;

exception
    when unique_violation then
        raise notice 'Mitarbeiter ist bereits in dieser Gesellschaft!';
   	
end;
$$
language plpgsql;

/*
 * Funktion trägt die Daten in die Assoziation "hat_Tarif" ein
 */
create or replace function insert_tbl_hat_tarif(
	p_mandant_id integer,
	p_personalnummer varchar(32),
	p_tarifbezeichnung varchar(16),
	p_eintrittsdatum date
) returns void as
$$
declare
	v_mitarbeiter_id integer;
	v_tarif_id integer;
begin
	
	set session role tenant_user;
	execute 'SET app.current_tenant=' || p_mandant_id;
	
	execute 'SELECT mitarbeiter_ID FROM mitarbeiter WHERE personalnummer = $1' into v_mitarbeiter_ID using p_personalnummer;
	execute 'SELECT tarif_ID FROM tarife WHERE tarifbezeichnung = $1' into v_tarif_id using p_tarifbezeichnung;
    
    insert into hat_Tarif(Mitarbeiter_ID, Tarif_ID, Mandant_ID, Datum_Von, Datum_Bis)
   		values (v_mitarbeiter_ID, v_tarif_id, p_mandant_id, p_eintrittsdatum, '9999-12-31');
   	
   	exception
        when unique_violation then
            raise notice 'Mitarbeiter ist bereits in dieser Gesellschaft!';
	
   	set role postgres;
   	
end;
$$
language plpgsql;

/*
 * Funktion trägt neue Daten in Tabelle 'Aussertarifliche' ein.
 */
create or replace function insert_tbl_aussertarifliche (
	p_personalnummer varchar(32),
	p_mandant_id integer,
	p_eintrittsdatum date
) returns void as
$$
declare
	v_mitarbeiter_id integer;
begin
    
    set session role tenant_user;
    execute 'SET app.current_tenant=' || p_mandant_id;
   
    execute 'SELECT mitarbeiter_ID FROM mitarbeiter WHERE personalnummer = $1' into v_mitarbeiter_ID using p_personalnummer;

    insert into 
   		Aussertarifliche(Mitarbeiter_ID, Mandant_ID, Datum_Von, Datum_Bis)
   	values 
   		(v_mitarbeiter_ID, p_mandant_id, p_eintrittsdatum, '9999-12-31');
    
    set role postgres;
exception
    when unique_violation then
    	set role postgres;
        raise notice 'Mitarbeiter bereits als Aussertariflicher eingetragen!';

end;
$$
language plpgsql;

/*
 * Funktion trägt die Daten in die Assoziation "hat_private_Krankenversicherung" ein
 */
create or replace function insert_tbl_hat_private_krankenversicherung(
	p_mandant_id integer,
	p_personalnummer varchar(32),
	p_krankenkasse varchar(128),
	p_ag_zuschuss_krankenversicherung decimal(6, 2),
	p_ag_zuschuss_pflegeversicherung decimal(6, 2),
	p_eintrittsdatum date
) returns void as
$$
declare
	v_privatkrankenkasse_id integer;
	v_mitarbeiter_id integer;
begin
	
	set session role tenant_user;
	execute 'SET app.current_tenant=' || p_mandant_id;
		
	-- Pruefen, ob Privatkrankenkasse bereits in Tabelle 'Privatkrankenkassen' hinterlegt ist...
	execute 'SELECT privatkrankenkasse_id FROM privatkrankenkassen WHERE privatkrankenkasse = $1' into v_privatkrankenkasse_id using p_krankenkasse;
    
    -- ... und falls sie nicht existiert, Meldung ausgeben, dass erst die Privatkrankenkasse hinterlegt werden muss!
    if v_privatkrankenkasse_id is null then
		set role postgres;
		raise exception 'Privatkrankenkasse ''%'' nicht angelegt. Bitte legen Sie zuerst diese Privatkrankenkasse an!', p_krankenkasse;   
    end if;
   	
   	-- Pruefen, ob Mitarbeiter vorhanden ist...
    execute 'SELECT mitarbeiter_ID FROM mitarbeiter WHERE personalnummer = $1' into v_mitarbeiter_ID using p_personalnummer;
   
    -- ... und falls nicht existiert, Meldung ausgeben, dass erst der Mitarbeiter hinterlegt werden muss!
    if v_mitarbeiter_id is null then
		set role postgres;
		raise exception 'Mitarbeiter ''%'' ist nicht eingetragen!', p_personalnummer;   
    end if;
   	
   	-- Assoziation 'hat_Privatkrankenkasse', welche die Tabellen 'Mitarbeiter' und 'Privatkrankenkassen' miteinander verknuepft, mit Daten befuellen
    insert into hat_Privatkrankenkasse(Mitarbeiter_ID, Privatkrankenkasse_ID, Mandant_ID, AG_Zuschuss_private_Krankenversicherung, AG_Zuschuss_private_Pflegeversicherung, Datum_Von, Datum_Bis)
   		values (v_mitarbeiter_id, v_privatkrankenkasse_id, p_mandant_id, p_ag_zuschuss_krankenversicherung, p_ag_zuschuss_pflegeversicherung, p_eintrittsdatum, '9999-12-31');
	
   	set role postgres;
   	
end;
$$
language plpgsql;

/*
 * Funktion trägt die Daten in die Assoziation "hat_gesetzliche_Krankenversicherung" ein
 */
create or replace function insert_tbl_hat_gesetzliche_Krankenversicherung(
	p_mandant_id integer,
	p_personalnummer varchar(32),
	p_ermaessigter_kv_beitrag boolean,
	p_eintrittsdatum date
) returns void as
$$
declare
	v_mitarbeiter_id integer;
	v_krankenversicherung_id integer;
begin
	
	set session role tenant_user;
	execute 'SET app.current_tenant=' || p_mandant_id;
		
	-- Pruefen, ob Wahrheitswert fuer ermaessigten Beitragssatz bereits in Tabelle 'Krankenversicherungen' hinterlegt ist...
	execute 'SELECT krankenversicherung_id FROM krankenversicherungen WHERE ermaessigter_beitragssatz = $1' into v_krankenversicherung_id using p_ermaessigter_kv_beitrag;
    
    -- ... und falls sie nicht existiert, Meldung ausgeben, dass erst die Krankenversicherung hinterlegt werden muss!
    if v_krankenversicherung_id is null then
		set role postgres;
		if p_ermaessigter_kv_beitrag then
			raise exception 'Sie muessen erst noch die Moeglichkeit, ermaessigte Beitragssaetze zu beruecksichtigen, anlegen!';   
		else
			raise exception 'Sie muessen erst noch die Moeglichkeit, nicht ermaessigte Beitragssaetze zu beruecksichtigen, anlegen!'; 
		end if;
    end if;
   
    execute 'SELECT mitarbeiter_ID FROM mitarbeiter WHERE personalnummer = $1' into v_mitarbeiter_ID using p_personalnummer;
    
    insert into hat_gesetzliche_Krankenversicherung(Mitarbeiter_ID, Krankenversicherung_ID, Mandant_ID, Datum_Von, Datum_Bis)
   		values (v_mitarbeiter_id, v_krankenversicherung_id, p_mandant_id, p_eintrittsdatum, '9999-12-31');
	
   	set role postgres;

exception
    when unique_violation then
    	set role postgres;
        raise notice 'Es ist bereits vermerkt, dass der Mitarbeiter gesetzlich krankenversichert ist!';
   	
end;
$$
language plpgsql;

/*
 * Funktion trägt die Daten in die Assoziation "ist_in_GKV" ein
 */
create or replace function insert_tbl_ist_in_gkv(
	p_mandant_id integer,
	p_personalnummer varchar(32),
	p_krankenkasse varchar(128),
	p_krankenkassenkuerzel varchar(16),
	p_eintrittsdatum date
) returns void as
$$
declare
	v_mitarbeiter_id integer;
	v_krankenkasse_id integer;
begin
	
	set session role tenant_user;
	execute 'SET app.current_tenant=' || p_mandant_id;
		
	-- Pruefen, ob Krankenkasse bereits vorhanden ist...
	execute 'SELECT gesetzliche_krankenkasse_id FROM gesetzliche_krankenkassen WHERE krankenkasse_gesetzlich = $1 AND krankenkassenkuerzel = $2'
		into v_krankenkasse_id using p_krankenkasse, p_krankenkassenkuerzel;
    
    -- ... und falls sie nicht existiert, Meldung ausgeben, dass erst die Krankenkasse hinterlegt werden muss!
    if v_krankenkasse_ID is null then
		set role postgres;
		raise exception 'Krankenkasse ''%'' noch nicht hinterlegt! Bitte tragen Sie zuerst die Krankenkasse ein!', p_krankenkasse;   
    end if;
   
    execute 'SELECT mitarbeiter_ID FROM mitarbeiter WHERE personalnummer = $1' into v_mitarbeiter_ID using p_personalnummer;
    
    insert into ist_in_GKV(Mitarbeiter_ID, gesetzliche_Krankenkasse_ID, Mandant_ID, Datum_Von, Datum_Bis)
   		values (v_mitarbeiter_id, v_Krankenkasse_id, p_mandant_id, p_eintrittsdatum, '9999-12-31');
	
   	set role postgres;

exception
    when unique_violation then
    	set role postgres;
        raise notice 'Mitarbeiter ist bereits aktuell in Krankenkasse ''%'' vermerkt!', p_krankenkasse;
   	
end;
$$
language plpgsql;


/*
 * Funktion trägt die Daten in die Assoziation "hat_x_Kinder_unter_25" ein
 */
create or replace function insert_tbl_hat_x_kinder_unter_25(
	p_mandant_id integer,
	p_personalnummer varchar(32),
	p_anzahl_kinder integer,
	p_eintrittsdatum date
) returns void as
$$
declare
	v_mitarbeiter_id integer;
	v_anzahl_kinder_unter25_id integer;
begin
	
	set session role tenant_user;
	execute 'SET app.current_tenant=' || p_mandant_id;
	
	execute 'SELECT mitarbeiter_ID FROM mitarbeiter WHERE personalnummer = $1' into v_mitarbeiter_ID using p_personalnummer;
	
	execute 'SELECT anzahl_kinder_unter_25_id FROM anzahl_kinder_unter_25 WHERE anzahl_kinder = $1'
			into v_anzahl_kinder_unter25_id using p_anzahl_kinder;
    
    insert into hat_x_Kinder_unter_25(Mitarbeiter_ID, Anzahl_Kinder_unter_25_ID, Mandant_ID, Datum_Von, Datum_Bis)
   		values (v_mitarbeiter_id, v_anzahl_kinder_unter25_id, p_mandant_id, p_eintrittsdatum, '9999-12-31');
	
   	set role postgres;

exception
    when unique_violation then
    	set role postgres;
        raise notice 'Aktuelle Anzahl der Kinder für Mitarbeiter ''%'' ist bereits vermerkt!', p_personalnummer;
   	
end;
$$
language plpgsql;

/*
 * Funktion trägt die Daten in die Assoziation "arbeitet_in_sachsen" ein
 */
create or replace function insert_tbl_arbeitet_in_sachsen(
	p_mandant_id integer,
	p_personalnummer varchar(32),
	p_in_sachsen boolean,
	p_eintrittsdatum date
) returns void as
$$
declare
	v_mitarbeiter_id integer;
	v_arbeitsort_sachsen_id integer;
begin
	
	set session role tenant_user;
	execute 'SET app.current_tenant=' || p_mandant_id;
	
	execute 'SELECT mitarbeiter_ID FROM mitarbeiter WHERE personalnummer = $1' into v_mitarbeiter_ID using p_personalnummer;
	execute 'SELECT arbeitsort_sachsen_id FROM arbeitsort_sachsen WHERE in_sachsen = $1' into v_arbeitsort_sachsen_id using p_in_sachsen;
    
    insert into arbeitet_in_sachsen(Mitarbeiter_ID, arbeitsort_sachsen_ID, Mandant_ID, Datum_Von, Datum_Bis)
   		values (v_mitarbeiter_id, v_arbeitsort_sachsen_id, p_mandant_id, p_eintrittsdatum, '9999-12-31');
	
   	set role postgres;

exception
    when unique_violation then
    	set role postgres;
        raise notice 'Es ist bereits vermerkt, ob Mitarbeiter ''%'' in Sachsen wohnt!', p_personalnummer;
   	
end;
$$
language plpgsql;

/*
 * Funktion trägt die Daten in die Assoziation "hat_gesetzliche_arbeitslosenversicherung" ein
 */
create or replace function insert_tbl_hat_gesetzliche_arbeitslosenversicherung(
	p_mandant_id integer,
	p_personalnummer varchar(32),
	p_eintrittsdatum date
) returns void as
$$
declare
	v_mitarbeiter_id integer;
	v_arbeitslosenversicherung_id integer;
begin
	
	set session role tenant_user;
	execute 'SET app.current_tenant=' || p_mandant_id;
		
	-- Pruefen, ob Mandant bereits Eintrag in Tabelle 'Arbeitslosenversicherungen' hat (jeder Mandant hat nur maximal einen Eintrag in diese Tabelle)...
	execute 'SELECT arbeitslosenversicherung_id FROM arbeitslosenversicherungen WHERE mandant_id = $1' 
		into v_arbeitslosenversicherung_id using p_mandant_id;
    
    -- ... und falls sie nicht existiert, Meldung ausgeben, dass erst die Arbeitslosenversicherungsdaten hinterlegt werden muessen!
    if v_arbeitslosenversicherung_id is null then
		set role postgres;
		raise exception 'Sie muessen erst AV-Beitraege und Beitragsbemessungsgrenzen anlegen, bevor Sie Mitarbeiter anlegen!';   
    end if;
   
    execute 'SELECT mitarbeiter_ID FROM mitarbeiter WHERE personalnummer = $1' into v_mitarbeiter_ID using p_personalnummer;
    
    insert into hat_gesetzliche_Arbeitslosenversicherung(Mitarbeiter_ID, Arbeitslosenversicherung_ID, Mandant_ID, Datum_Von, Datum_Bis)
   		values (v_mitarbeiter_id, v_arbeitslosenversicherung_id, p_mandant_id, p_eintrittsdatum, '9999-12-31');
	
   	set role postgres;

exception
    when unique_violation then
    	set role postgres;
        raise notice 'Es ist bereits vermerkt, dass der Mitarbeiter gesetzlich arbeitslosenversichert ist!';
   	
end;
$$
language plpgsql;

/*
 * Funktion trägt neue Daten in Tabelle 'hat_gesetzliche_Rentenversicherung' ein.
 */
create or replace function insert_tbl_hat_gesetzliche_rentenversicherung(
	p_mandant_id integer,
	p_personalnummer varchar(32),
	p_eintrittsdatum date
) returns void as
$$
declare
	v_mitarbeiter_id integer;
	v_rentenversicherung_id integer;
begin
	
	set session role tenant_user;
	execute 'SET app.current_tenant=' || p_mandant_id;
		
	-- Pruefen, ob Mandant bereits Eintrag in Tabelle 'Rentenversicherungen' hat (jeder Mandant hat nur maximal einen Eintrag in diese Tabelle)...
	execute 'SELECT rentenversicherung_id FROM rentenversicherungen WHERE mandant_id = $1' 
		into v_rentenversicherung_id using p_mandant_id;
    
    -- ... und falls sie nicht existiert, Meldung ausgeben, dass erst die Rentenversicherungsdaten hinterlegt werden muessen!
    if v_rentenversicherung_id is null then
		set role postgres;
		raise exception 'Sie muessen erst RV-Beitraege und Beitragsbemessungsgrenzen anlegen, bevor Sie Mitarbeiter anlegen!';   
    end if;
   
    execute 'SELECT mitarbeiter_ID FROM mitarbeiter WHERE personalnummer = $1' into v_mitarbeiter_ID using p_personalnummer;
    
    insert into hat_gesetzliche_Rentenversicherung(Mitarbeiter_ID, Rentenversicherung_ID, Mandant_ID, Datum_Von, Datum_Bis)
   		values (v_mitarbeiter_id, v_rentenversicherung_id, p_mandant_id, p_eintrittsdatum, '9999-12-31');
	
   	set role postgres;

exception
    when unique_violation then
    	set role postgres;
        raise notice 'Es ist bereits vermerkt, dass der Mitarbeiter gesetzlich rentenversichert ist!';
   	
end;
$$
language plpgsql;

/*
 * Funktion trägt die Daten in die Assoziation "ist_anderweitig_versichert" ein
 */
create or replace function insert_tbl_ist_anderweitig_versichert(
	p_mandant_id integer,
	p_personalnummer varchar(32),
	p_krankenkasse varchar(128),
	p_krankenkassenkuerzel varchar(16),
	p_eintrittsdatum date
) returns void as
$$
declare
	v_mitarbeiter_id integer;
	v_krankenkasse_id integer;
begin
	
	set session role tenant_user;
	execute 'SET app.current_tenant=' || p_mandant_id;
		
	-- Pruefen, ob Krankenkasse bereits vorhanden ist...
	execute 'SELECT gemeldete_krankenkasse_id FROM gemeldete_krankenkassen WHERE gemeldete_krankenkasse = $1 AND krankenkassenkuerzel = $2'
		into v_krankenkasse_id using p_krankenkasse, p_krankenkassenkuerzel;
    
    -- ... und falls sie nicht existiert, Meldung ausgeben, dass erst die Krankenkasse hinterlegt werden muss!
    if v_krankenkasse_ID is null then
		set role postgres;
		raise exception 'Diese Krankenkasse ''%'' ist noch nicht hinterlegt! Bitte tragen Sie zuerst die Krankenkasse ein!', p_krankenkasse;   
    end if;
   
    execute 'SELECT mitarbeiter_ID FROM mitarbeiter WHERE personalnummer = $1' into v_mitarbeiter_ID using p_personalnummer;
    
    insert into ist_anderweitig_versichert(Mitarbeiter_ID, gemeldete_Krankenkasse_ID, Mandant_ID, Datum_Von, Datum_Bis)
   		values (v_mitarbeiter_id, v_krankenkasse_id, p_mandant_id, p_eintrittsdatum, '9999-12-31');
	
   	set role postgres;

exception
    when unique_violation then
    	set role postgres;
        raise notice 'Mitarbeiter ist bereits aktuell in Krankenkasse ''%'' vermerkt!', p_krankenkasse;
   	
end;
$$
language plpgsql;

/*
 * Funktion trägt die Daten in die Assoziation "ist_Minijobber" ein
 */
create or replace function insert_tbl_ist_Minijobber(
	p_mandant_id integer,
	p_personalnummer varchar(32),
	p_ist_kurzfristig_beschaeftigt boolean,
	p_eintrittsdatum date
) returns void as
$$
declare
	v_mitarbeiter_id integer;
	v_minijob_id integer;
begin
	
	set session role tenant_user;
	execute 'SET app.current_tenant=' || p_mandant_id;
		
	-- Pruefen, ob Wahrheitswert fuer kurzfristige Beschaeftigung bereits in Tabelle 'Minijobs' hinterlegt ist...
	execute 'SELECT minijob_id FROM minijobs WHERE kurzfristig_beschaeftigt = $1' into v_minijob_id using p_ist_kurzfristig_beschaeftigt;
    
    -- ... und falls sie nicht existiert, Meldung ausgeben, dass erst die Krankenversicherung hinterlegt werden muss!
    if v_minijob_id is null then
		set role postgres;
		if p_ist_kurzfristig_beschaeftigt then
			raise exception 'Sie muessen erst noch die Moeglichkeit, kurzfristige Minijobs zu beruecksichtigen, anlegen!';   
		else
			raise exception 'Sie muessen erst noch die Moeglichkeit, nicht kurzfristige Minijobs zu beruecksichtigen, anlegen!'; 
		end if;
    end if;
   
    execute 'SELECT mitarbeiter_ID FROM mitarbeiter WHERE personalnummer = $1' into v_mitarbeiter_ID using p_personalnummer;
    
    insert into ist_Minijobber(Mitarbeiter_ID, Minijob_ID, Mandant_ID, Datum_Von, Datum_Bis)
   		values (v_mitarbeiter_id, v_minijob_id, p_mandant_id, p_eintrittsdatum, '9999-12-31');
	
   	set role postgres;

exception
    when unique_violation then
    	set role postgres;
        raise notice 'Es ist bereits vermerkt, dass der Mitarbeiter Minijobber ist!';
   	
end;
$$
language plpgsql;





----------------------------------------------------------------------------------------------------------------
-- Stored Procedure fuer Use Case "Eintrag Verguetungsbestandteil fuer aussertariflicher Mitarbeiter"
/*
 * Funktion verknuepft aussertariflichen Mitarbeiter mit (diversen) Verguetungsbestandteilen- Darunter fallen neben Monatsgehalt, Weihnachtsgeld etc. auch Beamtenbeihilfen, da der Staat verpflichtet ist, 
 * Beamten Beihilfen zu zahlen z.B. für (private) Krankenversicherung, Kinder etc..
 */
create or replace function insert_aussertarifliche_verguetungsbestandteil(
	p_mandant_id integer,
	p_personalnummer varchar(32),
	p_Verguetungsbestandteil varchar(64),
	p_betrag decimal(8, 2),
	p_eintragungsdatum date
) returns void as
$$
declare
	v_mitarbeiter_id integer;
	v_aussertarifliche_id integer;
	v_verguetungsbestandteil_id integer;
begin
    
    set session role tenant_user;
	execute 'SET app.current_tenant=' || p_mandant_id;
	
	-- Pruefen, ob Verguetungsbestandteil bereits in Tabelle 'monatliche_Beihilfen' hinterlegt ist
	execute 'SELECT verguetungsbestandteil_id FROM verguetungsbestandteile WHERE Verguetungsbestandteil = $1' into v_verguetungsbestandteil_id using p_Verguetungsbestandteil;

	-- ... und falls nicht, dann Meldung ausgeben, dass dieser Verguetungsbestandteil erst hinterlegt werden muss!
	if v_verguetungsbestandteil_id is null then
		set role postgres;
		raise exception 'Bitte erst Verguetungsbestandteil ''%'' anlegen!', p_Verguetungsbestandteil;
	end if;

	-- Mitarbeiter_ID ziehen, da diese als Vorbereitung benoetigt wird, um einen Datensatz in der Assoziation 'hat_Verguetungsbestandteil_AT' anzulegen
	execute 'SELECT mitarbeiter_id FROM mitarbeiter WHERE personalnummer = $1' into v_mitarbeiter_id using p_personalnummer;

	-- ... falls Mitarbeiter nicht vorhanden ist, dann Meldung ausgeben, dass dieser erst hinterlegt werden muss!
	if v_mitarbeiter_id is null then
		set role postgres;
		raise exception 'Bitte erst Mitarbeiter ''%'' anlegen!', p_personalnummer;
	end if;

	-- Aussertarif_ID ziehen, da diese benoetigt wird, um einen Datensatz in der Assoziation 'hat_Verguetungsbestandteil_AT' anzulegen
	execute 'SELECT aussertarif_id FROM aussertarifliche WHERE mitarbeiter_ID = $1 AND Datum_Bis = ''9999-12-31''' into v_aussertarifliche_id using v_mitarbeiter_id;

	-- ... falls Mitarbeiter nicht als aussertariflicher Mitarbeiter vorhanden ist, dann Meldung ausgeben, dass dieser erst hinterlegt werden muss!
	if v_aussertarifliche_id is null then
		set role postgres;
		raise exception 'Mitarbeiter ''%'' ist nicht als aussertariflicher Beschaeftigter hinterlegt!', p_personalnummer;
	end if;
	
    insert into hat_Verguetungsbestandteil_AT(Aussertarif_ID, Verguetungsbestandteil_ID, Mandant_ID, Betrag, Datum_Von, Datum_Bis) 
   		values (v_aussertarifliche_id, v_verguetungsbestandteil_id, p_mandant_id, p_betrag, p_eintragungsdatum, '9999-12-31');
   	
   	set role postgres;

exception
    when unique_violation then
        raise notice 'Aussertariflicher Mitarbeiter ''%'' hat bereits aktuellen Verguetungsbestandteil ''%''!', p_personalnummer, p_Verguetungsbestandteil;

end;
$$
language plpgsql;





----------------------------------------------------------------------------------------------------------------
-- Stored Procedure für Use Case "Update neue Adresse für bestehenden Mitarbeiter"

/*
 * Methode schreibt die Daten einer neuen Wohnadresse fuer einen Mitarbeiter ein. Zudem wird der letzte Tag des alten Wohnsitzes im entsprechenden
 * Datensatz der Tabelle 'wohnt_in' eingetragen (zuvor steht dort standardmaessig '9999-12-31'). Die Methode wird auch benutzt, um bei einem neuen
 * Mitarbeiter, wo noch keine Adressdaten hinterlegt sind, dessen Adresse anzulegen. 
 */
create or replace function update_adresse(
	p_mandant_id integer,
	p_personalnummer varchar(32),
	p_alter_eintrag_gueltig_bis date,
	p_neuer_eintrag_gueltig_ab date,
	p_strasse varchar(64),
	p_hausnummer varchar(8),
	p_postleitzahl varchar(16),
	p_stadt varchar(128),
	p_region varchar(128),
	p_land varchar(128)
) returns void as
$$
declare
	v_mitarbeiter_id integer;
	v_anzahl_eintraege_id integer;
begin
	
	set session role tenant_user;
	execute 'SET app.current_tenant=' || p_mandant_id;

	-- Pruefung, ob der Mitarbeiter ueberhaupt existiert und falls ja, dann Mitarbeiter_ID in Variable speichern
	execute 'SELECT mitarbeiter_id FROM mitarbeiter WHERE personalnummer = $1' into v_mitarbeiter_id using p_personalnummer;
	if v_mitarbeiter_id is null then
		set role postgres;
		raise exception 'Mitarbeiter ''%'' existiert nicht!', p_personalnummer;
	end if;

	-- Eintrag der neuen Wohnadresse
	perform insert_tbl_laender(p_mandant_id, p_land);
	perform insert_tbl_regionen(p_mandant_id, p_region, p_land);
	perform insert_tbl_staedte(p_mandant_id, p_stadt, p_region);
	perform insert_tbl_postleitzahlen(p_mandant_id, p_postleitzahl, p_stadt);
	perform insert_tbl_strassenbezeichnungen(p_mandant_id, p_strasse, p_hausnummer, p_postleitzahl);
	
	-- Pruefung, ob für Mitarbeiter bereits ein Datensatz in 'wohnt_in' existiert. Falls nicht, so wurde für den Mitarbeiter noch kein Wohnort angelegt.
	-- Notwendig, da es moeglich sein soll, einen neuen Mitarbeiter vorerst auch ohne Adresse in der Datenbank anzulegen. Damit im Nachhinein
	-- die Adresse eingetragen werden kann, kann diese Update-Funktion verwendet werden.
	execute 'SELECT count(*) FROM wohnt_in WHERE mitarbeiter_id = $1' into v_anzahl_eintraege_id using v_mitarbeiter_ID;
	
	-- falls bereits Adresszuordnungen für Mitarbeiter besteht, dann die aktuelle, in der in Spalte 'Datum_Bis' der Wert '9999-12-31' steht, updaten.
	if v_anzahl_eintraege_id != 0 then
		execute 'UPDATE wohnt_in SET Datum_Bis = $1 WHERE mitarbeiter_ID = $2 AND Datum_Bis = ''9999-12-31''' 
				using p_alter_eintrag_gueltig_bis, v_mitarbeiter_ID;
	end if;
	
	-- neue Adresse mit Mitarbeiter verknuepfen
	perform insert_tbl_wohnt_in(p_mandant_id, p_personalnummer, p_strasse, p_hausnummer, p_neuer_eintrag_gueltig_ab);
	
   	set role postgres;
   	
end;
$$
language plpgsql;





----------------------------------------------------------------------------------------------------------------
-- Stored Procedure für Use Case "Update Kündigung Mitarbeiter"
/*
 * Methode ändert die Angaben aufgrund von Kündigung eines bestimmten Mitarbeiters. Es wird das Austrittsdatum in Tabelle 'Mitarbeiter' auf
 * den letzten Arbeitstag geupdatet und der Austrittsgrund bzw. dessen Kategorie in dessen Tabellen vermerkt. 
 */
create or replace function update_mitarbeiterentlassung(
	p_mandant_id integer,
	p_personalnummer varchar(32),
	p_letzter_arbeitstag date,
	p_austrittsgrund varchar(32)
) returns void as
$$
declare
	v_mitarbeiter_id integer;
	v_austrittsgrund_id integer;
begin
	
	set session role tenant_user;
	execute 'SET app.current_tenant=' || p_mandant_id;

	-- Pruefung, ob der Mitarbeiter überhaupt existiert und falls ja, dann Mitarbeiter_ID in Variable speichern
	execute 'SELECT mitarbeiter_id FROM mitarbeiter WHERE personalnummer = $1' into v_mitarbeiter_id using p_personalnummer;
	if v_mitarbeiter_id is null then
		set role postgres;
		raise exception 'Mitarbeiter ''%'' existiert nicht!', p_personalnummer;
	end if;

	-- Pruefen, ob Austrittsgrund in Datenbank hinterlegt ist
	execute 'SELECT austrittsgrund_id FROM austrittsgruende WHERE austrittsgrund = $1' into v_austrittsgrund_id using p_austrittsgrund;

	-- ... und falls nicht, Meldung ausgeben, dass Ausstrittsgrund noch in Datenbank eingetragen werden muss
	if v_austrittsgrund_id is null then
		set role postgres;
		raise exception 'Austrittsgrund ''%'' ist nicht in Datenbank vorhanden. Bitte erst anlegen!', p_austrittsgrund;
	end if;
	
	-- Austrittsgrund mit Mitarbeiter verknuepfen
	execute 'UPDATE mitarbeiter SET austrittsdatum = $1, austrittsgrund_id = $2 WHERE personalnummer = $3' using p_letzter_arbeitstag, v_austrittsgrund_id, p_personalnummer;
	
	-- in allen Assoziationstabellen muss fuer den aktuellen Eintrag in Spalte "Bis_Datum" das '9999-12-31' durch den letzten Arbeitstag ersetzt werden
	execute 'UPDATE Aussertarifliche SET Datum_Bis = $1 WHERE mitarbeiter_id = $2 AND Datum_Bis = ''9999-12-31''' using p_letzter_arbeitstag, v_mitarbeiter_id;
	execute 'UPDATE hat_tarif SET Datum_Bis = $1 WHERE mitarbeiter_id = $2 AND Datum_Bis = ''9999-12-31''' using p_letzter_arbeitstag, v_mitarbeiter_id;	
	execute 'UPDATE wohnt_in SET Datum_Bis = $1 WHERE mitarbeiter_id = $2 AND Datum_Bis = ''9999-12-31''' using p_letzter_arbeitstag, v_mitarbeiter_id;
	execute 'UPDATE hat_geschlecht SET Datum_Bis = $1 WHERE mitarbeiter_id = $2 AND Datum_Bis = ''9999-12-31''' using p_letzter_arbeitstag, v_mitarbeiter_id;
	execute 'UPDATE ist_mitarbeitertyp SET Datum_Bis = $1 WHERE mitarbeiter_id = $2 AND Datum_Bis = ''9999-12-31''' using p_letzter_arbeitstag, v_mitarbeiter_id;
	execute 'UPDATE in_gesellschaft SET Datum_Bis = $1 WHERE mitarbeiter_id = $2 AND Datum_Bis = ''9999-12-31''' using p_letzter_arbeitstag, v_mitarbeiter_id;
	execute 'UPDATE in_steuerklasse SET Datum_Bis = $1 WHERE mitarbeiter_id = $2 AND Datum_Bis = ''9999-12-31''' using p_letzter_arbeitstag, v_mitarbeiter_id;
	execute 'UPDATE arbeitet_x_wochenstunden SET Datum_Bis = $1 WHERE mitarbeiter_id = $2 AND Datum_Bis = ''9999-12-31''' using p_letzter_arbeitstag, v_mitarbeiter_id;
	execute 'UPDATE arbeitet_x_wochenstunden SET Datum_Bis = $1 WHERE mitarbeiter_id = $2 AND Datum_Bis = ''9999-12-31''' using p_letzter_arbeitstag, v_mitarbeiter_id;
	execute 'UPDATE hat_jobtitel SET Datum_Bis = $1 WHERE mitarbeiter_id = $2 AND Datum_Bis = ''9999-12-31''' using p_letzter_arbeitstag, v_mitarbeiter_id;
	execute 'UPDATE ist_minijobber SET Datum_Bis = $1 WHERE mitarbeiter_id = $2 AND Datum_Bis = ''9999-12-31''' using p_letzter_arbeitstag, v_mitarbeiter_id;
	execute 'UPDATE ist_anderweitig_versichert SET Datum_Bis = $1 WHERE mitarbeiter_id = $2 AND Datum_Bis = ''9999-12-31''' using p_letzter_arbeitstag, v_mitarbeiter_id;
	execute 'UPDATE hat_privatkrankenkasse SET Datum_Bis = $1 WHERE mitarbeiter_id = $2 AND Datum_Bis = ''9999-12-31''' using p_letzter_arbeitstag, v_mitarbeiter_id;
	execute 'UPDATE ist_in_gkv SET Datum_Bis = $1 WHERE mitarbeiter_id = $2 AND Datum_Bis = ''9999-12-31''' using p_letzter_arbeitstag, v_mitarbeiter_id;
	execute 'UPDATE hat_gesetzliche_krankenversicherung SET Datum_Bis = $1 WHERE mitarbeiter_id = $2 AND Datum_Bis = ''9999-12-31''' using p_letzter_arbeitstag, v_mitarbeiter_id;
	execute 'UPDATE hat_x_kinder_unter_25 SET Datum_Bis = $1 WHERE mitarbeiter_id = $2 AND Datum_Bis = ''9999-12-31''' using p_letzter_arbeitstag, v_mitarbeiter_id;
	execute 'UPDATE arbeitet_in_sachsen SET Datum_Bis = $1 WHERE mitarbeiter_id = $2 AND Datum_Bis = ''9999-12-31''' using p_letzter_arbeitstag, v_mitarbeiter_id;
	execute 'UPDATE hat_gesetzliche_arbeitslosenversicherung SET Datum_Bis = $1 WHERE mitarbeiter_id = $2 AND Datum_Bis = ''9999-12-31''' using p_letzter_arbeitstag, v_mitarbeiter_id;
	execute 'UPDATE hat_gesetzliche_Rentenversicherung SET Datum_Bis = $1 WHERE mitarbeiter_id = $2 AND Datum_Bis = ''9999-12-31''' using p_letzter_arbeitstag, v_mitarbeiter_id;
	execute 'UPDATE in_Steuerklasse SET Datum_Bis = $1 WHERE mitarbeiter_id = $2 AND Datum_Bis = ''9999-12-31''' using p_letzter_arbeitstag, v_mitarbeiter_id;
	execute 'UPDATE arbeitet_x_wochenstunden SET Datum_Bis = $1 WHERE mitarbeiter_id = $2 AND Datum_Bis = ''9999-12-31''' using p_letzter_arbeitstag, v_mitarbeiter_id;
	execute 'UPDATE eingesetzt_in SET Datum_Bis = $1 WHERE mitarbeiter_id = $2 AND Datum_Bis = ''9999-12-31''' using p_letzter_arbeitstag, v_mitarbeiter_id;
	execute 'UPDATE hat_Jobtitel SET Datum_Bis = $1 WHERE mitarbeiter_id = $2 AND Datum_Bis = ''9999-12-31''' using p_letzter_arbeitstag, v_mitarbeiter_id;

   	set role postgres;
   	
end;
$$
language plpgsql;





----------------------------------------------------------------------------------------------------------------
-- Stored Procedures für Use Case "Update Krankenversicherungsbeitraege"

/*
 * Funktion traegt die neuen Versicherungsbeitraege in Prozent und Beitragsbemessungsgrenzen der Krankenversicherungen
 */
create or replace function update_krankenversicherungsbeitraege (
	p_mandant_id integer,
	p_ermaessigter_beitragssatz boolean,
	p_ag_krankenversicherungsbeitrag_in_prozent decimal(5, 3),
	p_an_krankenversicherungsbeitrag_in_prozent decimal(5, 3),
	p_beitragsbemessungsgrenze_kv_ost decimal(10, 2),
	p_beitragsbemessungsgrenze_kv_west decimal(10, 2),
	p_alter_eintrag_gueltig_bis date,
	p_neuer_eintrag_gueltig_ab date
) returns void as
$$
declare
	v_krankenversicherungsbeitrag_id integer;
	v_krankenversicherung_id integer;
begin
    
    set session role tenant_user;
    execute 'SET app.current_tenant=' || p_mandant_id;
   
    -- Pruefung, ob Wahrheitswert zur Frage, ob ermaessigter Beitragssatz oder nicht, vorhanden ist
	execute 'SELECT krankenversicherung_ID FROM krankenversicherungen WHERE ermaessigter_beitragssatz = $1' 
		into v_krankenversicherung_id using p_ermaessigter_beitragssatz;
	if v_krankenversicherung_id is null then
		set role postgres;
		raise exception 'Ermaessigter Beitragssatz = ''%'' ist nicht angelegt!', p_ermaessigter_beitragssatz;
	end if;
    
   	-- Pruefen, ob die Beitrags- und Beitragsbemessungsgrenzen-Kombination bereits vorhanden ist...
	-- (Es kann sein, dass die neuen Beitragssaetze in der Vergangenheit schonmal gueltig waren und die Regierung sie wieder darauf zuruecksetzt)
   	execute 'SELECT 
				krankenversicherungsbeitrag_id
			 FROM 
				gkv_beitraege 
			 WHERE 
				ag_krankenversicherungsbeitrag_in_prozent = $1 AND
				an_krankenversicherungsbeitrag_in_prozent = $2 AND
				beitragsbemessungsgrenze_kv_ost = $3 AND
				beitragsbemessungsgrenze_kv_west = $4' 
   			into 
   				v_krankenversicherungsbeitrag_id 
			using 
				p_ag_krankenversicherungsbeitrag_in_prozent, 
				p_an_krankenversicherungsbeitrag_in_prozent,
				p_beitragsbemessungsgrenze_kv_ost,
				p_beitragsbemessungsgrenze_kv_west;
    
    -- ... und falls sie nicht existiert, dann eintragen
    if v_krankenversicherungsbeitrag_id is null then
		insert into
	   		GKV_Beitraege(Mandant_ID, 
				   		  AG_Krankenversicherungsbeitrag_in_Prozent,
						  AN_Krankenversicherungsbeitrag_in_Prozent,
						  Beitragsbemessungsgrenze_KV_Ost,
						  Beitragsbemessungsgrenze_KV_West)
	   	values
	   		(p_mandant_id, 
	   		 p_ag_krankenversicherungsbeitrag_in_prozent,
			 p_an_krankenversicherungsbeitrag_in_prozent,
			 p_beitragsbemessungsgrenze_kv_ost,
			 p_beitragsbemessungsgrenze_kv_west);
		
		-- Nochmal krankenversicherungsbeitrag_id abfragen, da diese als Schluessel fuer die Assoziation 'hat_GKV_Beitraege' benoetigt wird
		execute 'SELECT 
				krankenversicherungsbeitrag_id
			 FROM 
				gkv_beitraege 
			 WHERE 
				ag_krankenversicherungsbeitrag_in_prozent = $1 AND
				an_krankenversicherungsbeitrag_in_prozent = $2 AND
				beitragsbemessungsgrenze_kv_ost = $3 AND
				beitragsbemessungsgrenze_kv_west = $4' 
   			into 
   				v_krankenversicherungsbeitrag_id 
			using 
				p_ag_krankenversicherungsbeitrag_in_prozent, 
				p_an_krankenversicherungsbeitrag_in_prozent,
				p_beitragsbemessungsgrenze_kv_ost,
				p_beitragsbemessungsgrenze_kv_west;
    end if;
   	
   	-- beim veralteten Eintrag das 'Bis_Datum' auf den letzten Tag der Gueltigkeit updaten...
    execute 'UPDATE hat_gkv_beitraege SET Datum_Bis = $1 WHERE krankenversicherung_id = $2 AND Datum_Bis = ''9999-12-31''' 
			using p_alter_eintrag_gueltig_bis, v_krankenversicherung_id;
    
    -- ... und Eintrag fuer die neuen Daten erstellen
    insert into hat_GKV_Beitraege(Krankenversicherung_ID, Krankenversicherungsbeitrag_ID, Mandant_ID, Datum_Von, Datum_Bis)
   		values (v_krankenversicherung_id, v_krankenversicherungsbeitrag_id, p_mandant_id, p_neuer_eintrag_gueltig_ab, '9999-12-31');

    set role postgres;
   
exception

    when unique_violation then
    	set role postgres;
        raise notice 'Diese GKV-Beitragssätze und GKV-Beitragsbemessungsgrenzen sind bereits aktuell!';
end;
$$
language plpgsql;





----------------------------------------------------------------------------------------------------------------
-- Stored Procedures für Use Case "Update Abteilungshierarchie"

/*
 * Funktion unterstellt Abteilung einer uebergeordneten Abteilung 
 */
create or replace function update_erstelle_abteilungshierarchie (
	p_mandant_id integer,
	p_untere_abteilung varchar(64),
	p_obere_abteilung varchar(64)
) returns void as
$$
declare
	v_untere_abteilung_id integer;
	v_obere_abteilung_id integer;
begin
    
    set session role tenant_user;
    execute 'SET app.current_tenant=' || p_mandant_id;
   
    -- Pruefung, ob untergeordnete Abteilung vorhanden ist
	execute 'SELECT abteilung_id FROM abteilungen WHERE abteilung = $1' into v_untere_abteilung_id using p_untere_abteilung;
	if v_untere_abteilung_id is null then
		set role postgres;
		raise exception 'Die untergeordnete Abteilung ''%'' ist nicht angelegt!', p_untere_abteilung;
	end if;

	-- Pruefung, ob uebergeordnete Abteilung vorhanden ist
	execute 'SELECT abteilung_id FROM abteilungen WHERE abteilung = $1' into v_obere_abteilung_id using p_obere_abteilung;
	if v_obere_abteilung_id is null then
		set role postgres;
		raise exception 'Die uebergeordnete Abteilung ''%'' ist nicht angelegt!', p_obere_abteilung;
	end if;
   	
   	-- Im Datensatz der untergeordneten Abteilung soll die ID der uebergeordneten Abteilung in die Fremdschluessel-Spalte 'untersteht_Abteilung'  eingetragen werden
    execute 'UPDATE abteilungen SET untersteht_abteilung = $1 WHERE abteilung_id = $2' using v_obere_abteilung_id, v_untere_abteilung_id;

    set role postgres;
   
exception

    when unique_violation then
    	set role postgres;
        raise notice 'Diese GKV-Beitragssätze und GKV-Beitragsbemessungsgrenzen sind bereits aktuell!';
end;
$$
language plpgsql;





----------------------------------------------------------------------------------------------------------------
-- Stored Procedure für Use Case "Update Kuendigung Mitarbeiter"
/*
 * Methode loescht alle Eintraege eines Mitarbeiters aus den Assoziationstabellen, der Tabelle 'Privat_Krankenversicherte' 
 * und der zentralen Tabelle 'Mitarbeiter'. 
 */
create or replace function delete_mitarbeiterdaten(
	p_mandant_id integer,
	p_personalnummer varchar(32)
) returns void as
$$
declare
	v_mitarbeiter_id integer;
	v_aussertarif_id integer;
begin
	
	set session role tenant_user;
	execute 'SET app.current_tenant=' || p_mandant_id;

	-- Pruefung, ob der Mitarbeiter überhaupt existiert und falls ja, dann Mitarbeiter_ID in Variable speichern
	execute 'SELECT mitarbeiter_id FROM mitarbeiter WHERE personalnummer = $1' into v_mitarbeiter_id using p_personalnummer;
	if v_mitarbeiter_id is null then
		set role postgres;
		raise exception 'Mitarbeiter ''%'' existiert nicht!', p_personalnummer;
	end if;
	
	-- personenbezogene Mitarbeiterdaten aus Bereich 'Entgelt' entfernen

	-- Es muss geprueft werden, ob der Mitarbeiter aussertariflich angestellt war. Falls ja, muss neben den Eintraegen in der Tabelle
	-- 'Aussertarif' auch die Eintraege in der Assoziation 'hat_verguetungsbestandteil_at' entfernt werden. Dort ist der Schluessel 
	-- fuer den Mitarbeiter aber nicht mehr 'Mitarbeiter_ID', sondern 'Aussertarif_ID'. 
	execute 'SELECT aussertarif_id FROM aussertarifliche WHERE mitarbeiter_ID = $1' into v_aussertarif_id using v_mitarbeiter_id;
	if v_aussertarif_id is not null then
		execute 'DELETE FROM hat_verguetungsbestandteil_at WHERE aussertarif_id = $1' using v_aussertarif_id;
		execute 'DELETE FROM aussertarifliche WHERE mitarbeiter_id = $1' using v_mitarbeiter_id;
	end if;
	execute 'DELETE FROM hat_tarif WHERE mitarbeiter_id = $1' using v_mitarbeiter_id;
	
	-- personenbezogene Mitarbeiterdaten aus Bereich 'Adresse' entfernen
	execute 'DELETE FROM wohnt_in WHERE mitarbeiter_id = $1' using v_mitarbeiter_id;

	-- personenbezogene Mitarbeiterdaten aus Bereich 'Geschlechter' entfernen
	execute 'DELETE FROM hat_geschlecht WHERE mitarbeiter_id = $1' using v_mitarbeiter_id;

	-- personenbezogene Mitarbeiterdaten aus Bereich 'Mitarbeiteryp' entfernen
	execute 'DELETE FROM ist_mitarbeitertyp WHERE mitarbeiter_id = $1' using v_mitarbeiter_id;

	-- personenbezogene Mitarbeiterdaten aus Bereich 'Gesellschaften' entfernen
	execute 'DELETE FROM in_gesellschaft WHERE mitarbeiter_id = $1' using v_mitarbeiter_id;

	-- personenbezogene Mitarbeiterdaten aus Bereich 'Kranken- und Pflegeversicherung' entfernen
	execute 'DELETE FROM ist_minijobber WHERE mitarbeiter_id = $1' using v_mitarbeiter_id;
	execute 'DELETE FROM ist_anderweitig_versichert WHERE mitarbeiter_id = $1' using v_mitarbeiter_id;
	execute 'DELETE FROM hat_privatkrankenkasse WHERE mitarbeiter_id = $1' using v_mitarbeiter_id;
	execute 'DELETE FROM ist_in_gkv WHERE mitarbeiter_id = $1' using v_mitarbeiter_id;
	execute 'DELETE FROM hat_gesetzliche_krankenversicherung WHERE mitarbeiter_id = $1' using v_mitarbeiter_id;
	execute 'DELETE FROM hat_x_kinder_unter_25 WHERE mitarbeiter_id = $1' using v_mitarbeiter_id;
	execute 'DELETE FROM arbeitet_in_sachsen WHERE mitarbeiter_id = $1' using v_mitarbeiter_id;

	-- personenbezogene Mitarbeiterdaten aus Bereich 'Arbeitslosenversicherung' entfernen
	execute 'DELETE FROM hat_gesetzliche_arbeitslosenversicherung WHERE mitarbeiter_id = $1' using v_mitarbeiter_id;

	-- personenbezogene Mitarbeiterdaten aus Bereich 'Rentenversicherung' entfernen
	execute 'DELETE FROM hat_gesetzliche_rentenversicherung WHERE mitarbeiter_id = $1' using v_mitarbeiter_id;

	-- personenbezogene Mitarbeiterdaten aus Bereich 'Steuerklasse' entfernen
	execute 'DELETE FROM in_steuerklasse WHERE mitarbeiter_id = $1' using v_mitarbeiter_id;

	-- personenbezogene Mitarbeiterdaten aus Bereich 'Wochenarbeitsstunden' entfernen
	execute 'DELETE FROM arbeitet_x_wochenstunden WHERE mitarbeiter_id = $1' using v_mitarbeiter_id;

	-- personenbezogene Mitarbeiterdaten aus Bereich 'Wochenarbeitsstunden' entfernen
	execute 'DELETE FROM eingesetzt_in WHERE mitarbeiter_id = $1' using v_mitarbeiter_id;
	
	-- personenbezogene Mitarbeiterdaten aus Bereich 'Jobtitel' entfernen
	execute 'DELETE FROM hat_jobtitel WHERE mitarbeiter_id = $1' using v_mitarbeiter_id;

	-- personenbezogene Mitarbeiterdaten aus zentraler Tabelle 'Mitarbeiter' entfernen
	execute 'DELETE FROM mitarbeiter WHERE mitarbeiter_id = $1' using v_mitarbeiter_id;
	
   	set role postgres;
   	
end;
$$
language plpgsql;





----------------------------------------------------------------------------------------------------------------
-- Stored Procedure für Use Case "Entferne Daten eines Mandanten aus Datenbank"
/*
 * Methode loescht alle Eintraege eines Mandanten aus allen Tabellen. 
 */
create or replace function delete_mandantendaten(
	p_mandant_id integer
) returns void as
$$
begin
	
	set session role tenant_user;
	execute 'SET app.current_tenant=' || p_mandant_id;

	-- Daten aus Bereich 'Entgelt' entfernen
	execute 'DELETE FROM hat_verguetungsbestandteil_at WHERE mandant_id = $1' using p_mandant_id;
	execute 'DELETE FROM hat_verguetungsbestandteil_tarif WHERE mandant_id = $1' using p_mandant_id;
	execute 'DELETE FROM verguetungsbestandteile WHERE mandant_id = $1' using p_mandant_id;
	execute 'DELETE FROM aussertarifliche WHERE mandant_id = $1' using p_mandant_id;
	execute 'DELETE FROM hat_tarif WHERE mandant_id = $1' using p_mandant_id;
	execute 'DELETE FROM tarife WHERE mandant_id = $1' using p_mandant_id;
	execute 'DELETE FROM gewerkschaften WHERE mandant_id = $1' using p_mandant_id;

	-- Daten aus Bereich 'Adresse' entfernen
	execute 'DELETE FROM wohnt_in WHERE mandant_id = $1' using p_mandant_id;
	execute 'DELETE FROM strassenbezeichnungen WHERE mandant_id = $1' using p_mandant_id;
	execute 'DELETE FROM postleitzahlen WHERE mandant_id = $1' using p_mandant_id;
	execute 'DELETE FROM staedte WHERE mandant_id = $1' using p_mandant_id;
	execute 'DELETE FROM regionen WHERE mandant_id = $1' using p_mandant_id;
	execute 'DELETE FROM laender WHERE mandant_id = $1' using p_mandant_id;

	-- Daten aus Bereich 'Geschlecht' entfernen
	execute 'DELETE FROM hat_geschlecht WHERE mandant_id = $1' using p_mandant_id;
	execute 'DELETE FROM geschlechter WHERE mandant_id = $1' using p_mandant_id;
	
	-- Daten aus Bereich 'Mitarbeiteryp' entfernen
	execute 'DELETE FROM ist_mitarbeitertyp WHERE mandant_id = $1' using p_mandant_id;
	execute 'DELETE FROM mitarbeitertypen WHERE mandant_id = $1' using p_mandant_id;

	-- Daten aus Bereich 'Gesellschaften' entfernen
	execute 'DELETE FROM in_gesellschaft WHERE mandant_id = $1' using p_mandant_id;
	execute 'DELETE FROM unfallversicherungsbeitraege WHERE mandant_id = $1' using p_mandant_id;
	execute 'DELETE FROM gesellschaften WHERE mandant_id = $1' using p_mandant_id;
	execute 'DELETE FROM berufsgenossenschaften WHERE mandant_id = $1' using p_mandant_id;

	-- Daten aus Bereich 'Kranken- und Pflegeversicherung' entfernen
	execute 'DELETE FROM ist_minijobber WHERE mandant_id = $1' using p_mandant_id;
	execute 'DELETE FROM hat_pauschalabgaben WHERE mandant_id = $1' using p_mandant_id;
	execute 'DELETE FROM minijobs WHERE mandant_id = $1' using p_mandant_id;
	execute 'DELETE FROM pauschalabgaben WHERE mandant_id = $1' using p_mandant_id;

	execute 'DELETE FROM ist_anderweitig_versichert WHERE mandant_id = $1' using p_mandant_id;
	execute 'DELETE FROM hat_umlagen_anderweitig WHERE mandant_id = $1' using p_mandant_id;
	execute 'DELETE FROM gemeldete_krankenkassen WHERE mandant_id = $1' using p_mandant_id;

	execute 'DELETE FROM hat_privatkrankenkasse WHERE mandant_id = $1' using p_mandant_id;
	execute 'DELETE FROM hat_umlagen_privat WHERE mandant_id = $1' using p_mandant_id;
	execute 'DELETE FROM privatkrankenkassen WHERE mandant_id = $1' using p_mandant_id;

	execute 'DELETE FROM ist_in_gkv WHERE mandant_id = $1' using p_mandant_id;
	execute 'DELETE FROM hat_gkv_zusatzbeitrag WHERE mandant_id = $1' using p_mandant_id;
	execute 'DELETE FROM hat_umlagen_gesetzlich WHERE mandant_id = $1' using p_mandant_id;
	execute 'DELETE FROM gesetzliche_krankenkassen WHERE mandant_id = $1' using p_mandant_id;
	execute 'DELETE FROM gkv_zusatzbeitraege WHERE mandant_id = $1' using p_mandant_id;
	execute 'DELETE FROM umlagen WHERE mandant_id = $1' using p_mandant_id;
	
	execute 'DELETE FROM hat_gesetzliche_krankenversicherung WHERE mandant_id = $1' using p_mandant_id;
	execute 'DELETE FROM hat_gkv_beitraege WHERE mandant_id = $1' using p_mandant_id;
	execute 'DELETE FROM krankenversicherungen WHERE mandant_id = $1' using p_mandant_id;
	execute 'DELETE FROM gkv_beitraege WHERE mandant_id = $1' using p_mandant_id;

	execute 'DELETE FROM hat_x_kinder_unter_25 WHERE mandant_id = $1' using p_mandant_id;
	execute 'DELETE FROM hat_gesetzlichen_an_pv_beitragssatz WHERE mandant_id = $1' using p_mandant_id;
	execute 'DELETE FROM anzahl_kinder_unter_25 WHERE mandant_id = $1' using p_mandant_id;
	execute 'DELETE FROM an_pflegeversicherungsbeitraege_gesetzlich WHERE mandant_id = $1' using p_mandant_id;
	
	execute 'DELETE FROM arbeitet_in_sachsen WHERE mandant_id = $1' using p_mandant_id;
	execute 'DELETE FROM hat_gesetzlichen_ag_pv_beitragssatz WHERE mandant_id = $1' using p_mandant_id;
	execute 'DELETE FROM arbeitsort_sachsen WHERE mandant_id = $1' using p_mandant_id;
	execute 'DELETE FROM ag_pflegeversicherungsbeitraege_gesetzlich WHERE mandant_id = $1' using p_mandant_id;

	-- Daten aus Bereich 'Arbeitslosenversicherung' entfernen
	execute 'DELETE FROM hat_gesetzliche_arbeitslosenversicherung WHERE mandant_id = $1' using p_mandant_id;
	execute 'DELETE FROM hat_av_beitraege WHERE mandant_id = $1' using p_mandant_id;
	execute 'DELETE FROM arbeitslosenversicherungen WHERE mandant_id = $1' using p_mandant_id;
	execute 'DELETE FROM arbeitslosenversicherungsbeitraege WHERE mandant_id = $1' using p_mandant_id;

	-- Daten aus Bereich 'Rentenversicherung' entfernen
	execute 'DELETE FROM hat_gesetzliche_rentenversicherung WHERE mandant_id = $1' using p_mandant_id;
	execute 'DELETE FROM hat_rv_beitraege WHERE mandant_id = $1' using p_mandant_id;
	execute 'DELETE FROM rentenversicherungen WHERE mandant_id = $1' using p_mandant_id;
	execute 'DELETE FROM rentenversicherungsbeitraege WHERE mandant_id = $1' using p_mandant_id;

	-- Daten aus Bereich 'Steuerklasse' entfernen
	execute 'DELETE FROM in_steuerklasse WHERE mandant_id = $1' using p_mandant_id;
	execute 'DELETE FROM steuerklassen WHERE mandant_id = $1' using p_mandant_id;
	
	-- Daten aus Bereich 'Wochenarbeitszeit' entfernen
	execute 'DELETE FROM arbeitet_x_wochenstunden WHERE mandant_id = $1' using p_mandant_id;
	execute 'DELETE FROM wochenarbeitsstunden WHERE mandant_id = $1' using p_mandant_id;

		-- Daten aus Bereich 'Abteilung' entfernen
	execute 'DELETE FROM eingesetzt_in WHERE mandant_id = $1' using p_mandant_id;
	execute 'DELETE FROM abteilungen WHERE mandant_id = $1' using p_mandant_id;

	-- Daten aus Bereich 'Jobtitel' entfernen
	execute 'DELETE FROM hat_jobtitel WHERE mandant_id = $1' using p_mandant_id;
	execute 'DELETE FROM jobtitel WHERE mandant_id = $1' using p_mandant_id;
	execute 'DELETE FROM erfahrungsstufen WHERE mandant_id = $1' using p_mandant_id;

	-- Daten aus zentraler Tabelle 'Mitarbeiter' entfernen
	execute 'DELETE FROM mitarbeiter WHERE mandant_id = $1' using p_mandant_id;

	-- Daten aus Bereich 'Austrittsgruende' entfernen
	execute 'DELETE FROM austrittsgruende WHERE mandant_id = $1' using p_mandant_id;
	execute 'DELETE FROM kategorien_austrittsgruende WHERE mandant_id = $1' using p_mandant_id;

	-- Daten aus Tabellen 'Nutzer' und zuletzt 'Mandanten' loeschen
	execute 'DELETE FROM nutzer WHERE mandant_id = $1' using p_mandant_id;
	execute 'DELETE FROM mandanten WHERE mandant_id = $1' using p_mandant_id;
	
   	set role postgres;
   	
end;
$$
language plpgsql;