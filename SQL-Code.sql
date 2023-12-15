-- Leerung der kompletten Datenbank

set role postgres;

-- Quelle: https://adityamattos.com/multi-tenancy-in-python-fastapi-and-sqlalchemy-using-postgres-row-level-security
-- Abschaffung der Rolle 'tenant-user' und dessen Privilegien
-- 'tenant-user' kann zukünftig erstellte Sequenzen (bspw. Serial) NICHT mehr nutzen benutzen 
alter default privileges in schema public revoke usage on sequences from tenant_user;
-- 'tenant-user' kann SELECT-, INSERT-, UPDATE- und DELETE-Befehle auf alle Tabellen im Schema 'public' (auch auf zukünftige Tabellen) NICHT mehr ausführen
alter default privileges in schema public revoke select, insert, update, delete on tables from tenant_user;
-- Berechtigungen auf Sequenzen für 'tenant'-user aufheben
revoke usage on all sequences in schema public from tenant_user;
-- Berechtigungen auf Tabellen für tenant-user aufheben
revoke select, insert, update, delete on all tables in schema public from tenant_user;
-- 'tenant_user' darf nicht mehr im Schema 'public' operieren 
revoke usage on schema public from tenant_user;
-- 'tenant-user' wird quasi enterbt
revoke tenant_user from postgres;
-- Rolle 'tenant_user' entfernen
drop role if exists tenant_user;

-- Erstellung der Rolle 'tenant-user' mit diversen Zugriffsrechten
-- Rolle für die user erstellen, welcher RLS unterliegt
create role tenant_user;
-- tenant-user erbt Berechtigungen von postgres (=Admin)
grant tenant_user to postgres;
-- Rolle 'tenant-user' darf im Schema 'public' operieren
grant usage on schema public to tenant_user;
-- 'tenant-user' hat Lese- und Schreibberechtigung auf alle Tabellen im Schema 'public'
grant select, insert, update, delete on all tables in schema public to tenant_user;
-- 'tenant-user' kann Sequenzen verwenden. So soll bspw. Tabellen mit Serial-Spalten nutzbar sein
grant usage on all sequences in schema public to tenant_user;
-- 'tenant-user' kann SELECT-, INSERT-, UPDATE- und DELETE-Befehle auf alle Tabellen im Schema 'public' ausführen (auch auf zukünftige Tabellen)
alter default privileges in schema public grant select, insert, update, delete on tables to tenant_user;
-- 'tenant-user' kann zukünftig erstellte Sequenzen (bspw. Serial) benutzen 
alter default privileges in schema public grant usage on sequences to tenant_user;

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

drop table if exists in_Gesellschaft;
drop table if exists Gesellschaften;

drop table if exists hat_Tarif;
drop table if exists hat_Verguetung;
drop table if exists Verguetungen;
drop table if exists Tarife;
drop table if exists Gewerkschaften;
drop table if exists Aussertarifliche;

drop table if exists Privat_Krankenversicherte;

drop table if exists hat_GKV_Beitraege;
drop table if exists hat_gesetzliche_Krankenversicherung;
drop table if exists Krankenversicherungen;
drop table if exists GKV_Beitraege;

drop table if exists ist_in_GKV;
drop table if exists hat_GKV_Zusatzbeitrag;
drop table if exists GKV_Zusatzbeitraege;
drop table if exists Krankenkassen;

drop table if exists hat_x_Kinder_unter_25;
drop table if exists hat_gesetzlichen_AN_PV_Beitragssatz;
drop table if exists Anzahl_Kinder_unter_25;
drop table if exists AN_Pflegeversicherungsbeitraege_gesetzlich;

drop table if exists hat_gesetzlichen_AG_PV_Beitragssatz;
drop table if exists wohnt_in_Sachsen;
drop table if exists wohnhaft_Sachsen;
drop table if exists AG_Pflegeversicherungsbeitraege_gesetzlich;

drop table if exists hat_gesetzliche_Arbeitslosenversicherung;
drop table if exists hat_AV_Beitraege;
drop table if exists Arbeitslosenversicherungsbeitraege;
drop table if exists Arbeitslosenversicherungen;

drop table if exists hat_gesetzliche_Rentenversicherung;
drop table if exists hat_RV_Beitraege;
drop table if exists Rentenversicherungsbeitraege;
drop table if exists Rentenversicherungen;

drop table if exists mitarbeiter;
drop table if exists Austrittsgruende;
drop table if exists Kategorien_Austrittsgruende;
drop table if exists Nutzer;
drop table if exists Mandanten;

drop function if exists mandant_anlegen(varchar(128));
drop function if exists nutzer_anlegen(integer, varchar(32), varchar(64), varchar(64));
drop function if exists nutzer_entfernen(integer, varchar(32));
drop function if exists pruefe_einmaligkeit_personalnummer(integer, varchar(64), varchar(32));

-- Loeschung der Stored Procedures für Use Case "Eintrag neue Krankenversicherungsbeitraege"
drop function if exists insert_krankenversicherungsbeitraege(integer, decimal(5, 3), decimal(5, 3), decimal(10, 2), decimal(10, 2), date);

-- Loeschung der Stored Procedures für Use Case "Eintrag neue Krankenkasse"
drop function if exists insert_Krankenkasse(integer, varchar(128), varchar(16), decimal(5, 3), date);

-- Loeschung der Stored Procedures für Use Case "Eintrag neue Kinderanzahl"
drop function if exists insert_anzahl_kinder_an_pv_beitrag(integer, integer, decimal(5, 3), decimal(10, 2), decimal(10, 2), date);

-- Loeschung der Stored Procedures für Use Case "Eintrag Sachsen"
drop function if exists insert_Sachsen (integer, boolean, decimal(5, 3), date);

-- Loeschung der Stored Procedures für Use Case "Eintrag neue Arbeitslosenversicherungsbeitraege"
drop function if exists insert_arbeitslosenversicherungsbeitraege(integer, decimal(5, 3), decimal(5, 3), decimal(10, 2), decimal(10, 2), date);

-- Loeschung der Stored Procedures für Use Case "Eintrag neue Rentenversicherungsbeitraege"
drop function if exists insert_rentenversicherungsbeitraege(integer, decimal(5, 3), decimal(5, 3), decimal(10, 2), decimal(10, 2), date);

-- Loeschung der Stored Procedures für Use Case "Eintrag Tarif"
drop function if exists insert_Tarif(integer, varchar(16), varchar(64), decimal(10, 2), decimal(10,2), decimal(10, 2), date);

-- Löschung der Stored Procedures für Use Case "Eintrag neuer Mitarbeiter"
drop function if exists insert_mitarbeiterdaten(integer, varchar(32), varchar(64), varchar(128), varchar(64), date, date, varchar(32), varchar(32), 
varchar(32), varchar(16), varchar(64), varchar(16), varchar(64), date, varchar(64), varchar(8), varchar(16), varchar(128), varchar(128), varchar(128), 
varchar(32), varchar(32), char(1), decimal(4, 2), varchar(64), varchar(16), boolean, varchar(32), varchar(32), varchar(128), varchar(16), boolean, 
varchar(64), varchar(16), decimal(10, 2), decimal(10,2), decimal(10, 2), boolean, decimal(10, 2), decimal(10,2), decimal(10, 2), boolean, decimal(5, 3), 
decimal(5, 3), decimal(10, 2), decimal(10, 2), varchar(128), varchar(16), decimal(5, 3), integer, decimal(5, 3), decimal(10, 2), decimal(10, 2),
boolean, decimal(5, 3), boolean, decimal(5, 3), decimal(5, 3), decimal(10, 2), decimal(10, 2), boolean, decimal(5, 3), decimal(5, 3), decimal(10, 2), 
decimal(10, 2));
drop function if exists insert_tbl_mitarbeiter(integer, varchar(32), varchar(64), varchar(128), varchar(64), date, date,  varchar(32), varchar(32), 
varchar(32), varchar(16), varchar(64), varchar(16), varchar(64), date);

drop function if exists insert_tbl_kategorien_austrittsgruende(integer, varchar(16));
drop function if exists insert_tbl_austrittsgruende(integer, varchar(32), varchar(16));

drop function if exists insert_tbl_laender(integer, varchar(128));
drop function if exists insert_tbl_regionen(integer, varchar(128), varchar(128));
drop function if exists insert_tbl_staedte(integer, varchar(128), varchar(128));
drop function if exists insert_tbl_postleitzahlen(integer, varchar(16), varchar(128));
drop function if exists insert_tbl_strassenbezeichnungen(integer, varchar(64), varchar(8), varchar(16));
drop function if exists insert_tbl_wohnt_in(integer, varchar(32), varchar(64), varchar(8), date);

drop function if exists insert_tbl_geschlechter(integer, varchar(32));
drop function if exists insert_tbl_hat_geschlecht(integer, varchar(32), varchar(32), date);

drop function if exists insert_tbl_ist_mitarbeitertyp(integer, varchar(32), varchar(32), date);
drop function if exists insert_tbl_mitarbeitertypen(integer,varchar(32));

drop function if exists insert_tbl_steuerklassen(integer, char(1));
drop function if exists insert_tbl_in_steuerklasse(integer, varchar(32), char(1), date);

drop function if exists insert_tbl_wochenarbeitsstunden(integer, decimal(4, 2));
drop function if exists insert_tbl_arbeitet_x_wochenarbeitsstunden(integer, varchar(32), decimal(4, 2), date);

drop function if exists insert_tbl_abteilungen(integer, varchar(64), varchar(16));
drop function if exists insert_tbl_eingesetzt_in(integer, varchar(32), varchar(64), varchar(16), boolean, date);

drop function if exists insert_tbl_jobtitel(integer, varchar(32));
drop function if exists insert_tbl_erfahrungsstufen(integer, varchar(32));
drop function if exists insert_tbl_hat_jobtitel(integer, varchar(32), varchar(32), varchar(32), date);

drop function if exists insert_tbl_gesellschaften(integer, varchar(128), varchar (16));
drop function if exists insert_tbl_in_gesellschaft(integer, varchar(32), varchar(128), date);

drop function if exists insert_tbl_hat_tarif(integer, varchar(32), varchar(16), date);
drop function if exists insert_tbl_aussertarifliche(varchar(32), integer, date, decimal(10, 2), decimal(10,2), decimal(10, 2));

drop function if exists insert_tbl_privat_krankenversicherte (varchar(32), integer, date, decimal(10, 2), decimal(10,2), decimal(10, 2));
drop function if exists insert_tbl_ist_in_gkv(integer, varchar(32), varchar(128), varchar(16), date);
drop function if exists insert_tbl_hat_gesetzliche_Krankenversicherung(integer, varchar(32), date);
drop function if exists insert_tbl_hat_gesetzliche_arbeitslosenversicherung(integer, varchar(32), date);
drop function if exists insert_tbl_hat_gesetzliche_rentenversicherung(integer, varchar(32), date);
drop function if exists insert_tbl_hat_x_kinder_unter_25(integer, varchar(32), integer, date);
drop function if exists insert_tbl_wohnt_in_sachsen(integer, varchar(32), boolean, date);

-- Löschung der Stored Procedures für Use Case "Update Kündigung Mitarbeiter"
drop function if exists update_adresse(integer, varchar(32), date, date, varchar(64), varchar(8), varchar(16), varchar(128), varchar(128), varchar(128));
drop function if exists update_mitarbeiterentlassung(integer, varchar(32), date, varchar(32), varchar(16));

-- Löschung der Stored Procedures für Use Case "Update Kündigung Mitarbeiter"
drop function if exists delete_mandantendaten(integer);
drop function if exists delete_mitarbeiterdaten(integer, varchar(32));

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
alter table Nutzer enable row level security;
create policy FilterMandant_Nutzer
    on Nutzer
    using (Mandant_ID = current_setting('app.current_tenant')::int);

-- Tabellen, die den Bereich "Austrittsgruende" behandeln, erstellen
create table Kategorien_Austrittsgruende (
	Kategorie_Austrittsgruende_ID serial primary key,
	Mandant_ID integer not null,
	Austrittsgrundkategorie varchar(16) not null,
	unique(Mandant_ID, Austrittsgrundkategorie),
	constraint fk_austrittsgrundkategorien_mandanten
		foreign key (Mandant_ID) 
			references Mandanten(Mandant_ID)
);
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
	Geschlecht varchar(32),
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
    Steuerklasse char(1) not null,
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
	unique (Mandant_ID, Abteilung, Abkuerzung),
	constraint fk_abteilungen_mandanten
		foreign key (Mandant_ID) 
			references Mandanten(Mandant_ID),
	constraint fk_abteilungen_abteilungen
		foreign key (untersteht_Abteilung)
			references Abteilungen(Abteilung_ID)
);
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
	unique (Mandant_ID, Gesellschaft, Abkuerzung),
	constraint fk_gesellschaften_mandanten
		foreign key (Mandant_ID) 
			references Mandanten(Mandant_ID),
	constraint fk_gesellschaften_gesellschaften
		foreign key (untersteht_Gesellschaft)
			references Gesellschaften(Gesellschaft_ID)
);
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
   
-- Tabellen, die den Bereich "Tarifentgelt" behandeln, erstellen
create table Gewerkschaften (
	Gewerkschaft_ID serial primary key,
	Mandant_ID integer not null,
	Gewerkschaft varchar(64) not null,
	unique (Mandant_ID, Gewerkschaft),
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

create table Verguetungen (
	Verguetung_ID serial primary key,
	Mandant_ID integer not null,
	Grundgehalt_monat decimal(10, 2) not null,
	Weihnachtsgeld decimal(10,2) not null,
	Urlaubsgeld decimal (10, 2) not null,
	unique(Mandant_ID, Grundgehalt_monat, Weihnachtsgeld, Urlaubsgeld),
	constraint fk_verguetungen_mandanten
		foreign key (Mandant_ID) 
			references Mandanten(Mandant_ID)
);
alter table Verguetungen enable row level security;
create policy FilterMandant_verguetungen
    on Verguetungen
    using (Mandant_ID = current_setting('app.current_tenant')::int);

create table hat_Verguetung(
	Tarif_ID integer not null,
	Verguetung_ID integer not null,
	Mandant_ID integer not null,
	Datum_Von date not null,
	Datum_Bis date not null,
	primary key (Tarif_ID, Datum_Bis),
	constraint fk_hatverguetung_tarife
		foreign key (Tarif_ID)
			references Tarife(Tarif_ID),
	constraint fk_hatverguetung_verguetungen
		foreign key (Verguetung_ID)
			references Verguetungen(Verguetung_ID),
	constraint fk_hatverguetung_mandanten
		foreign key (Mandant_ID) 
			references Mandanten(Mandant_ID)
);
alter table hat_Verguetung enable row level security;
create policy FilterMandant_hat_verguetung
    on hat_Verguetung
    using (Mandant_ID = current_setting('app.current_tenant')::int);

create table Aussertarifliche (
	Aussertarif_ID serial primary key,
	Mitarbeiter_ID integer not null,
	Mandant_ID integer not null,
	Datum_Von date not null,
	Datum_Bis date not null,
	Grundgehalt_monat decimal(10, 2) not null,
	Weihnachtsgeld decimal(10,2) not null,
	Urlaubsgeld decimal(10, 2) not null,
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

-- Tabellen, die den Bereich "Privat Krankenversicherte" behandeln, erstellen
create table Privat_Krankenversicherte (
	Privat_Krankenversichert_ID serial primary key,
	Mitarbeiter_ID integer not null,
	Mandant_ID integer not null,
	Datum_Von date not null,
	Datum_Bis date not null, 
	AG_Zuschuss_Krankenversicherung decimal(10,2) not null,
	AG_Zuschuss_Zusatzbeitrag decimal(10,2) not null,
	AG_Zuschuss_Pflegeversicherung decimal(10,2) not null,
	unique(Mitarbeiter_ID, Datum_Bis),
	constraint fk_privatkrankenversicherte_mitarbeiter
		foreign key (Mitarbeiter_ID)
			references Mitarbeiter(Mitarbeiter_ID),
	constraint fk_privatkrankenversicherte_mandanten
		foreign key (Mandant_ID) 
			references Mandanten(Mandant_ID)	
);
alter table Privat_Krankenversicherte enable row level security;
create policy FilterMandant_privat_krankenversicherte
    on Privat_Krankenversicherte
    using (Mandant_ID = current_setting('app.current_tenant')::int);

-- Tabellen, die den Bereich "Gesetzlich Krankenversicherte" behandeln, erstellen
create table Krankenversicherungen (
	Krankenversicherung_ID serial primary key,
	Mandant_ID integer not null,
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

   
create table Krankenkassen (
	Krankenkasse_ID serial primary key,
	Mandant_ID integer not null,
	Krankenkasse varchar(128) not null,
	Krankenkassenkuerzel varchar(16) not null,
	unique(Mandant_ID, Krankenkasse, Krankenkassenkuerzel),
	constraint fk_krankenkassen_mandanten
		foreign key (Mandant_ID) 
			references Mandanten(Mandant_ID)
);
alter table Krankenkassen enable row level security;
create policy FilterMandant_krankenkassen
    on Krankenkassen
    using (Mandant_ID = current_setting('app.current_tenant')::int);

-- GKV = gesetzliche Krankenversicherung
create table ist_in_GKV(
	Mitarbeiter_ID integer not null,
	Krankenkasse_ID integer not null,
	Mandant_ID integer not null,
	Datum_Von date not null,
	Datum_Bis date not null,
	primary key (Mitarbeiter_ID, Datum_Bis),
	constraint fk_istingkv_mitarbeiter
		foreign key (Mitarbeiter_ID)
			references Mitarbeiter(Mitarbeiter_ID),
	constraint fk_istingkv_krankenkassen
		foreign key (Krankenkasse_ID)
			references Krankenkassen(Krankenkasse_ID),
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
	Krankenkasse_ID integer not null,
	GKV_Zusatzbeitrag_ID integer not null,
	Mandant_ID integer not null,
	Datum_Von date not null,
	Datum_Bis date not null,
	primary key (Krankenkasse_ID, Datum_Bis),
	constraint fk_hatgkvzusatzbeitrag_krankenkassen
		foreign key (Krankenkasse_ID)
			references Krankenkassen(Krankenkasse_ID),
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

   
   
   
   
   
create table wohnhaft_Sachsen(
	wohnhaft_Sachsen_ID serial primary key,
	Mandant_ID integer not null,
	in_Sachsen boolean not null,
	unique(Mandant_ID, in_Sachsen),
	constraint fk_wohnhaftsachsen_mandanten
		foreign key (Mandant_ID) 
			references Mandanten(Mandant_ID)
);
alter table wohnhaft_Sachsen enable row level security;
create policy FilterMandant_wohnhaftsachsen
    on wohnhaft_Sachsen
    using (Mandant_ID = current_setting('app.current_tenant')::int);

create table wohnt_in_Sachsen(
	Mitarbeiter_ID integer not null,
	wohnhaft_Sachsen_ID integer not null,
	Mandant_ID integer not null,
	Datum_Von date not null,
	Datum_Bis date not null,
	primary key (Mitarbeiter_ID, Datum_Bis),
	constraint fk_wohntinsachsen_mitarbeiter
		foreign key (Mitarbeiter_ID)
			references Mitarbeiter(Mitarbeiter_ID),
	constraint fk_wohntinsachsen_wohnhaftsachsen
		foreign key (wohnhaft_Sachsen_ID)
			references wohnhaft_Sachsen(wohnhaft_Sachsen_ID),
	constraint fk_wohntinsachsen_mandanten
		foreign key (Mandant_ID) 
			references Mandanten(Mandant_ID)
);
alter table wohnt_in_Sachsen enable row level security;
create policy FilterMandant_wohntinsachsen
    on wohnt_in_Sachsen
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
	wohnhaft_Sachsen_ID integer not null,
	AG_PV_Beitrag_ID integer not null,
	Mandant_ID integer not null,
	Datum_Von date not null,
	Datum_Bis date not null,
	primary key (wohnhaft_Sachsen_ID, Datum_Bis),
	constraint fk_hatgesetzlichenagpvbeitragssatz_wohnhaftsachsen
		foreign key (wohnhaft_Sachsen_ID)
			references wohnhaft_Sachsen(wohnhaft_Sachsen_ID),	
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
-- Stored Procedures für Use Case "Eintrag neue Krankenkasse"

/*
 * Funktion trägt neue Daten einer Krankenkasse mit dessen individuellen Zusatzbeitrag ein.
 */
create or replace function insert_Krankenkasse (
	p_mandant_id integer,
	p_krankenkasse varchar(128),
	p_krankenkassenkuerzel varchar(16),
	p_gkv_zusatzbeitrag_in_prozent decimal(5, 3),
	p_eintragungsdatum date
) returns void as
$$
declare
	v_krankenkasse_ID integer;
	v_gkvzusatzbeitrag_id integer;
begin
    
    set session role tenant_user;
    execute 'SET app.current_tenant=' || p_mandant_id;
    
   	-- Pruefen, ob Krankenkasse bereits vorhanden ist...
   	execute 'SELECT krankenkasse_ID FROM krankenkassen WHERE krankenkasse = $1' into v_krankenkasse_ID using p_krankenkasse;
    
    -- ... und falls sie bereits existiert, Meldung ausgeben, dass die Daten nicht mehr eingetragen werden müssen
    if v_krankenkasse_ID is not null then
		set role postgres;
		raise exception 'Krankenkasse ''%'' ist bereits vorhanden! Übergebene Daten werden nicht eingetragen!', p_krankenkasse;   
    end if;
    
    -- ... ansonsten die Daten in den entsprechenden Tabellen eintragen
    -- Pruefen, ob die Beitrags- und Beitragsbemessungsgrenzen-Kombination bereits vorhanden ist...
   	execute 'SELECT gkv_zusatzbeitrag_id FROM gkv_zusatzbeitraege WHERE gkv_zusatzbeitrag_in_prozent = $1'
	   		into v_gkvzusatzbeitrag_id using p_gkv_zusatzbeitrag_in_prozent;
	
	-- ... falls nicht, dann eintragen
   	if v_gkvzusatzbeitrag_id is null then
		
		insert into GKV_Zusatzbeitraege(Mandant_ID, GKV_Zusatzbeitrag_in_Prozent)
   			values (p_mandant_id, p_gkv_zusatzbeitrag_in_prozent);
   		
   		execute 'SELECT gkv_zusatzbeitrag_id FROM gkv_zusatzbeitraege WHERE gkv_zusatzbeitrag_in_prozent = $1'
	   		into v_gkvzusatzbeitrag_id using p_gkv_zusatzbeitrag_in_prozent;
   		
	end if;

	insert into Krankenkassen(Mandant_ID, Krankenkasse, Krankenkassenkuerzel)
   		values (p_mandant_id, p_krankenkasse, p_krankenkassenkuerzel);
		
	execute 'SELECT krankenkasse_ID FROM krankenkassen WHERE krankenkasse = $1' into v_krankenkasse_ID using p_krankenkasse;
    
    insert into hat_GKV_Zusatzbeitrag(Krankenkasse_ID, GKV_Zusatzbeitrag_ID, Mandant_ID, Datum_Von, Datum_Bis)
   		values (v_krankenkasse_id, v_gkvzusatzbeitrag_id, p_mandant_id, p_eintragungsdatum, '9999-12-31');

    set role postgres;

end;
$$
language plpgsql;





----------------------------------------------------------------------------------------------------------------
-- Stored Procedures für Use Case "Eintrag neue Kinderanzahl"

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
		raise exception 'Kinderanzahl ''%'' ist bereits vorhanden! Übergebene Daten werden nicht eingetragen!', p_anzahl_kinder;   
    end if;
    
    -- ... ansonsten die Daten in den entsprechenden Tabellen eintragen
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

	insert into anzahl_kinder_unter_25(Mandant_ID, Anzahl_Kinder)
   		values (p_mandant_id, p_anzahl_kinder);

	execute 'SELECT anzahl_kinder_unter_25_id FROM anzahl_kinder_unter_25 WHERE anzahl_kinder = $1' 
   		into v_anzahl_kinder_unter_25_id using p_anzahl_kinder;
		
	insert into hat_gesetzlichen_AN_PV_Beitragssatz(Anzahl_Kinder_unter_25_ID, AN_PV_Beitrag_ID, Mandant_ID, Datum_Von, Datum_Bis)
   		values (v_anzahl_kinder_unter_25_id, v_an_pv_beitrag_id, p_mandant_id, p_eintragungsdatum, '9999-12-31');
   	
    set role postgres;

end;
$$
language plpgsql;





----------------------------------------------------------------------------------------------------------------
-- Stored Procedures für Use Case "Eintrag neue Krankenversicherungsbeitraege"

/*
 * Funktion trägt neue Daten bzgl. Krankenversicherungsbeitraege und Beitragsbemessungsgrenzen ein
 */
create or replace function insert_krankenversicherungsbeitraege (
	p_mandant_id integer,
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
    
    -- ... und falls sie bereits existiert, Meldung ausgeben, dass die Daten nicht mehr eingetragen werden müssen
    if v_krankenversicherungsbeitrag_id is not null then
		set role postgres;
		raise exception 'Diese Kombination der Krankenversicherungsbeitragssaetze ist bereits vorhanden! Übergebene Daten werden nicht eingetragen!';   
    end if;
   
    -- Jeder Mandant hat nur maximal einen Eintrag. Prüfen, ob dieser bereits vorhanden ist...
   	execute 'SELECT krankenversicherung_id FROM krankenversicherungen' into v_krankenversicherung_id;
    
    -- ... und falls nicht, dann Eintrag anlegen
    if v_krankenversicherung_id is null then
		insert into 
   			Krankenversicherungen(Mandant_ID)
	   	values 
	   		(p_mandant_id);		
    end if;
    
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
		
	execute 'SELECT krankenversicherung_id FROM krankenversicherungen' into v_krankenversicherung_id;

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
    
    insert into hat_GKV_Beitraege(Krankenversicherung_ID, Krankenversicherungsbeitrag_ID, Mandant_ID, Datum_Von, Datum_Bis)
   		values (v_krankenversicherung_id, v_krankenversicherungsbeitrag_id, p_mandant_id, p_eintragungsdatum, '9999-12-31');
   	
   	exception
        when unique_violation then
        	set role postgres;
            raise notice 'Diese GKV-Beitragssätze und GKV-Beitragsbemessungsgrenzen sind bereits aktuell!';
    
    set role postgres;

end;
$$
language plpgsql;





----------------------------------------------------------------------------------------------------------------
-- Stored Procedures für Use Case "Eintrag Sachsen"

/*
 * Funktion trägt neue Daten in Bezug auf die Frage ein, ob jemand in Sachsen wohnhaft ist. (Wichtig für Bestimmung des AG-Anteil zur Pflegeversicherung).
 */
create or replace function insert_Sachsen (
	p_mandant_id integer,
	p_in_sachsen boolean,
	p_ag_anteil_pv_beitrag_in_prozent decimal(5, 3),
	p_eintragungsdatum date
) returns void as
$$
declare
	v_wohnhaft_sachsen_id integer;
	v_ag_pv_beitrag_id integer;
begin
    
    set session role tenant_user;
    execute 'SET app.current_tenant=' || p_mandant_id;
    
   	-- Pruefen, ob Wahrheitswert für Sachsen-Frage bereits vorhanden ist...
   	execute 'SELECT wohnhaft_sachsen_id FROM wohnhaft_sachsen WHERE in_sachsen = $1' into v_wohnhaft_sachsen_id using p_in_sachsen;
    
    -- ... und falls sie bereits existiert, Meldung ausgeben, dass die Daten nicht mehr eingetragen werden müssen
    if v_wohnhaft_sachsen_id is not null then
		set role postgres;
		raise exception 'wohnhaft_Sachsen = ''%'' ist bereits vorhanden! Übergebene Daten werden nicht eingetragen!', p_in_sachsen;   
    end if;
    
    -- ... ansonsten die Daten in den entsprechenden Tabellen eintragen
    -- Pruefen, ob der AG-PV-Beitragssatz bereits vorhanden ist...
   	execute 'SELECT ag_pv_beitrag_id FROM ag_pflegeversicherungsbeitraege_gesetzlich WHERE ag_anteil_pv_beitrag_in_prozent = $1'
	   		into v_ag_pv_beitrag_id using p_ag_anteil_pv_beitrag_in_prozent;
	
	-- ... falls nicht, dann eintragen
   	if v_ag_pv_beitrag_id is null then
		
		insert into AG_Pflegeversicherungsbeitraege_gesetzlich(Mandant_ID, AG_Anteil_PV_Beitrag_in_Prozent)
   			values (p_mandant_id, p_ag_anteil_pv_beitrag_in_prozent);
   		
   		execute 'SELECT ag_pv_beitrag_id FROM ag_pflegeversicherungsbeitraege_gesetzlich WHERE ag_anteil_pv_beitrag_in_prozent = $1'
	   		into v_ag_pv_beitrag_id using p_ag_anteil_pv_beitrag_in_prozent;
   		
	end if;

	insert into wohnhaft_Sachsen(Mandant_ID, in_Sachsen)
   		values (p_mandant_id, p_in_sachsen);
		
	execute 'SELECT wohnhaft_sachsen_id FROM wohnhaft_sachsen WHERE in_sachsen = $1' into v_wohnhaft_sachsen_id using p_in_sachsen;
    
    insert into hat_gesetzlichen_AG_PV_Beitragssatz(wohnhaft_Sachsen_ID, AG_PV_Beitrag_ID, Mandant_ID, Datum_Von, Datum_Bis)
   		values (v_wohnhaft_sachsen_id, v_ag_pv_beitrag_id, p_mandant_id, p_eintragungsdatum, '9999-12-31');

    set role postgres;

end;
$$
language plpgsql;






----------------------------------------------------------------------------------------------------------------
-- Stored Procedures für Use Case "Eintrag neue Arbeitslosenversicherungsbeitraege"

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
    
    -- ... und falls sie bereits existiert, Meldung ausgeben, dass die Daten nicht mehr eingetragen werden müssen
    if v_arbeitslosenversicherungsbeitrag_id is not null then
		set role postgres;
		raise exception 'Diese Kombination der Arbeitslosenversicherungsbeitragssaetze ist bereits vorhanden! Übergebene Daten werden nicht eingetragen!';   
    end if;
   
    -- Jeder Mandant hat nur maximal einen Eintrag. Prüfen, ob dieser bereits vorhanden ist...
   	execute 'SELECT arbeitslosenversicherung_id FROM Arbeitslosenversicherungen' into v_arbeitslosenversicherung_id;
    
    -- ... und falls nicht, dann Eintrag anlegen
    if v_arbeitslosenversicherung_id is null then
		insert into 
   			Arbeitslosenversicherungen(Mandant_ID)
	   	values 
	   		(p_mandant_id);		
    end if;
    
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
		
	execute 'SELECT arbeitslosenversicherung_id FROM Arbeitslosenversicherungen' into v_arbeitslosenversicherung_id;

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
    
    insert into hat_AV_Beitraege(Arbeitslosenversicherung_ID, Arbeitslosenversicherungsbeitrag_ID, Mandant_ID, Datum_Von, Datum_Bis)
   		values (v_arbeitslosenversicherung_id, v_arbeitslosenversicherungsbeitrag_id, p_mandant_id, p_eintragungsdatum, '9999-12-31');
   	
   	exception
        when unique_violation then
        	set role postgres;
            raise notice 'Diese AV-Beitragssätze und AV-Beitragsbemessungsgrenzen sind bereits aktuell!';
    
    set role postgres;

end;
$$
language plpgsql;





----------------------------------------------------------------------------------------------------------------
-- Stored Procedures für Use Case "Eintrag neue Rentenversicherungsbeitraege"

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
    
    -- ... und falls sie bereits existiert, Meldung ausgeben, dass die Daten nicht mehr eingetragen werden müssen
    if v_rentenversicherungsbeitrag_id is not null then
		set role postgres;
		raise exception 'Diese Kombination der Rentenversicherungsbeitragssaetze ist bereits vorhanden! Übergebene Daten werden nicht eingetragen!';   
    end if;
   
    -- Jeder Mandant hat nur maximal einen Eintrag. Prüfen, ob dieser bereits vorhanden ist...
   	execute 'SELECT rentenversicherung_id FROM Rentenversicherungen' into v_rentenversicherung_id;
    
    -- ... und falls nicht, dann Eintrag anlegen
    if v_rentenversicherung_id is null then
		insert into 
   			Rentenversicherungen(Mandant_ID)
	   	values 
	   		(p_mandant_id);		
    end if;
    
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
		
	execute 'SELECT rentenversicherung_id FROM Rentenversicherungen' into v_rentenversicherung_id;

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
    
    insert into hat_RV_Beitraege(Rentenversicherung_ID, Rentenversicherungsbeitrag_ID, Mandant_ID, Datum_Von, Datum_Bis)
   		values (v_rentenversicherung_id, v_rentenversicherungsbeitrag_id, p_mandant_id, p_eintragungsdatum, '9999-12-31');
   	
   	exception
        when unique_violation then
        	set role postgres;
            raise notice 'Diese RV-Beitragssätze und RV-Beitragsbemessungsgrenzen sind bereits aktuell!';
    
    set role postgres;

end;
$$
language plpgsql;





----------------------------------------------------------------------------------------------------------------
-- Stored Procedures für Use Case "Eintrag Tarif"

/*
 * Funktion trägt neue Tarif-Daten ein.
 */
create or replace function insert_Tarif (
	p_mandant_id integer,
	p_tarifbezeichnung varchar(16),
	p_gewerkschaft varchar(64),
	p_grundgehalt_monat decimal(10, 2),
	p_weihnachtsgeld decimal(10,2),
	p_urlaubsgeld decimal(10, 2),
	p_eintragungsdatum date
) returns void as
$$
declare
	v_gewerkschaft_id integer;
	v_tarif_id integer;
	v_verguetung_id integer;
begin
    
    set session role tenant_user;
    execute 'SET app.current_tenant=' || p_mandant_id;
    
   	-- Pruefen, ob Gewerkschaft bereits vorhanden ist...
   	execute 'SELECT gewerkschaft_id FROM gewerkschaften WHERE gewerkschaft = $1' into v_gewerkschaft_id using p_gewerkschaft;
    
    -- ... und falls sie noch nicht existiert, dann eintragen
    if v_gewerkschaft_id is null then
		insert into Gewerkschaften(Mandant_ID, Gewerkschaft)
			values(p_mandant_id, p_gewerkschaft);
		
		-- Gewerkschaft_ID in Variable speichern, da diese als Fremdschluessel in Tabelle 'Tarife' benoetigt wird
		execute 'SELECT gewerkschaft_id FROM gewerkschaften WHERE gewerkschaft = $1' into v_gewerkschaft_id using p_gewerkschaft;
    end if;
   
    -- Pruefen, ob Tarif bereits vorhanden ist...
    execute 'SELECT tarif_id FROM Tarife WHERE tarifbezeichnung = $1' into v_tarif_id using p_tarifbezeichnung;
   
    if v_tarif_id is null then
   		insert into Tarife(Mandant_ID, Tarifbezeichnung, Gewerkschaft_ID)
   			values(p_mandant_id, p_tarifbezeichnung, v_gewerkschaft_id);
   		
   		-- Tarif_ID in Variable speichern, da diese als Teil des Primaerschluessels in Tabelle 'hat_Verguetung' benoetigt wird
   		execute 'SELECT tarif_id FROM Tarife WHERE tarifbezeichnung = $1' into v_tarif_id using p_tarifbezeichnung;
    end if;
   
    -- Pruefen, ob Verguetung bereits vorhanden ist,
    execute 'SELECT verguetung_id FROM verguetungen WHERE grundgehalt_monat = $1 AND weihnachtsgeld = $2 AND urlaubsgeld = $3'
   		into v_verguetung_id using p_grundgehalt_monat, p_weihnachtsgeld, p_urlaubsgeld;
   	
   	-- ... und falls sie noch nicht existiert, dann eintragen
   	if v_verguetung_id is null then
   		insert into Verguetungen(Mandant_ID, Grundgehalt_monat, Weihnachtsgeld, Urlaubsgeld)
   			values(p_mandant_id, p_grundgehalt_monat, p_weihnachtsgeld, p_urlaubsgeld);
   		
   		-- Verguetung_ID in Variable speichern, weil sie als Fremdschluessel in Tabelle 'hat_Verguetung' benoetigt wird
   		execute 'SELECT verguetung_id FROM verguetungen WHERE grundgehalt_monat = $1 AND weihnachtsgeld = $2 AND urlaubsgeld = $3'
   			into v_verguetung_id using p_grundgehalt_monat, p_weihnachtsgeld, p_urlaubsgeld;
   	end if;
   
    -- Assoziationstabelle 'hat_Verguetung', welche die Tabellen 'Tarife' und 'Verguetungen' verbindet. mit entsprechenden Daten befuellen,
    insert into hat_Verguetung(Tarif_ID, Verguetung_ID, Mandant_ID, Datum_Von, Datum_Bis)
    	values(v_tarif_id, v_verguetung_id, p_mandant_id, p_eintragungsdatum, '9999-12-31');
   
 	exception
        when unique_violation then
        	set role postgres;
            raise notice 'Diese RV-Beitragssätze und RV-Beitragsbemessungsgrenzen sind bereits aktuell!';

    set role postgres;

end;
$$
language plpgsql;





----------------------------------------------------------------------------------------------------------------
-- Stored Procedures für Use Case "Eintrag neuer Mitarbeiter"

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
    p_austrittsdatum date
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
						    Austrittsdatum)
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
			   p_austrittsdatum);
	
	exception
        when unique_violation then
            raise exception 'Personalnummer ''%'' bereits vorhanden!', p_personalnummer;      
           
	set role postgres;
	
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
   	
    exception
        when unique_violation then
            raise notice 'Land ''%'' bereits vorhanden!', p_land;

    set role postgres;
   
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
   	
    exception
        when unique_violation then
            raise notice 'Region ''%'' bereits vorhanden!', p_region;

    set role postgres;

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
   	
    exception
        when unique_violation then
            raise notice 'Stadt ''%'' bereits vorhanden!', p_stadt;
    
    set role postgres;

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
   	
    exception
        when unique_violation then
            raise notice 'Postleitzahl ''%'' bereits vorhanden!', p_postleitzahl;
    
    set role postgres;

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
   	
    exception
        when unique_violation then
        	v_strassenbezeichnung := p_strasse || p_hausnummer;
            raise notice 'Strassenbezeichnung ''%'' bereits vorhanden!', v_strassenbezeichnung;
    
    set role postgres;

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
   	
   	exception
        when unique_violation then
            raise notice 'Mitarbeiter ist bereits mit diesem aktuellen Wohnort vermerkt!';
	
   	set role postgres;
end;
$$
language plpgsql;


/*
 * Funktion trägt neue Daten in Tabelle 'Geschlechter' ein.
 */
create or replace function insert_tbl_geschlechter(
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
   	
    exception
        when unique_violation then
            raise notice 'Geschlecht ''%'' bereits vorhanden!', p_geschlecht;
    
    set role postgres;

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
	
	execute 'SELECT mitarbeiter_ID FROM mitarbeiter WHERE personalnummer = $1' into v_mitarbeiter_ID using p_personalnummer;
	execute 'SELECT geschlecht_ID FROM geschlechter WHERE geschlecht = $1' into v_geschlecht_id using p_geschlecht;
    
    insert into hat_Geschlecht(Mitarbeiter_ID, Geschlecht_ID, Mandant_ID, Datum_Von, Datum_Bis) 
   		values (v_mitarbeiter_id, v_geschlecht_id, p_mandant_id, p_eintrittsdatum, '9999-12-31');
   	
   	exception
        when unique_violation then
            raise notice 'Mitarbeiter ist bereits aktuell Geschlecht ''%''!', p_geschlecht;
	
   	set role postgres;
   
end;
$$
language plpgsql;

/*
 * Funktion trägt neue Daten in Tabelle 'Mitarbeitertypen' ein.
 */
create or replace function insert_tbl_mitarbeitertypen(
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
   	
    exception
        when unique_violation then
            raise notice 'Mitarbeitertyp ''%'' bereits vorhanden!', p_mitarbeitertyp;
    
    set role postgres;

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
	
	execute 'SELECT mitarbeiter_ID FROM mitarbeiter WHERE personalnummer = $1' into v_mitarbeiter_ID using p_personalnummer;
	execute 'SELECT mitarbeitertyp_ID FROM mitarbeitertypen WHERE mitarbeitertyp = $1' into v_mitarbeitertyp_id using p_mitarbeitertyp;
    
    insert into ist_Mitarbeitertyp(Mitarbeiter_ID, Mitarbeitertyp_ID, Mandant_ID, Datum_Von, Datum_Bis) 
   		values (v_mitarbeiter_id, v_mitarbeitertyp_id, p_mandant_id, p_eintrittsdatum, '9999-12-31');
   	
   	exception
        when unique_violation then
            raise notice 'Mitarbeiter ist bereits aktuell Mitarbeitertyp''%''!', p_mitarbeitertyp;
	
   	set role postgres;
   	
end;
$$
language plpgsql;

/*
 * Funktion trägt neue Daten in Tabelle 'Mitarbeitertypen' ein.
 */
create or replace function insert_tbl_steuerklassen(
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
   	
    exception
        when unique_violation then
            raise notice 'Steuerklasse ''%'' bereits vorhanden!', p_steuerklasse;
    
    set role postgres;

end;
$$
language plpgsql;

/*
 * Funktion trägt die Daten in die Assoziation "in_Steuerklasse" ein
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
	
	execute 'SELECT mitarbeiter_ID FROM mitarbeiter WHERE personalnummer = $1' into v_mitarbeiter_ID using p_personalnummer;
	execute 'SELECT steuerklasse_ID FROM steuerklassen WHERE steuerklasse = $1' into v_steuerklasse_id using p_steuerklasse;
    
    insert into in_Steuerklasse(Mitarbeiter_ID, Steuerklasse_ID, Mandant_ID, Datum_Von, Datum_Bis) 
   		values (v_mitarbeiter_id, v_steuerklasse_id, p_mandant_id, p_eintrittsdatum, '9999-12-31');
   	
   	exception
        when unique_violation then
            raise notice 'Mitarbeiter ist bereits aktuell in Steuerklasse ''%''!', p_steuerklasse;
	
   	set role postgres;
   	
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
   	
    exception
        when unique_violation then
            raise notice 'Wochenarbeitsstunden ''%'' bereits vorhanden!', p_wochenarbeitsstunden;
    
    set role postgres;

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
   	
   	exception
        when unique_violation then
            raise notice 'Wochenarbeitsstunden von aktuell ''%'' für diesen Mitarbeiter ist bereits vermerkt!', p_steuerklasse;
	
   	set role postgres;
   	
end;
$$
language plpgsql;

/*
 * Funktion trägt neue Daten in Tabelle 'Abteilungen' ein.
 */
create or replace function insert_tbl_abteilungen(
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
   	
    exception
        when unique_violation then
            raise notice 'Abteilung ''%'' bereits vorhanden!', p_abteilung;
    
    set role postgres;

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
	
	execute 'SELECT mitarbeiter_ID FROM mitarbeiter WHERE personalnummer = $1' into v_mitarbeiter_ID using p_personalnummer;
	execute 'SELECT abteilung_ID FROM abteilungen WHERE abteilung = $1 AND abkuerzung = $2' into v_abteilung_id using p_abteilung, p_abkuerzung;
    
    insert into eingesetzt_in(Mitarbeiter_ID, Abteilung_ID, Mandant_ID, Fuehrungskraft, Datum_Von, Datum_Bis) 
   		values (v_mitarbeiter_id, v_abteilung_id, p_mandant_id, p_fuehrungskraft, p_eintrittsdatum, '9999-12-31');
   	
   	exception
        when unique_violation then
            raise notice 'Mitarbeiter ist bereits in der aktuellen Abteilung ''%'' vermerkt!', p_abteilung;
	
   	set role postgres;
   	
end;
$$
language plpgsql;

/*
 * Funktion trägt neue Daten in Tabelle 'Jobtitel' ein.
 */
create or replace function insert_tbl_jobtitel (
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
   	
    exception
        when unique_violation then
            raise notice 'Jobtitel ''%'' bereits vorhanden!', p_jobtitel;
    
    set role postgres;

end;
$$
language plpgsql;

/*
 * Funktion trägt neue Daten in Tabelle 'Erfahrungsstufen' ein.
 */
create or replace function insert_tbl_erfahrungsstufen (
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
   	
    exception
        when unique_violation then
            raise notice 'Erfahrungsstufe ''%'' bereits vorhanden!', p_erfahrungsstufe;
    
    set role postgres;

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
	
	execute 'SELECT mitarbeiter_ID FROM mitarbeiter WHERE personalnummer = $1' into v_mitarbeiter_ID using p_personalnummer;
	execute 'SELECT jobtitel_ID FROM jobtitel WHERE jobtitel = $1' into v_jobtitel_id using p_jobtitel;
	execute 'SELECT erfahrungsstufe_ID FROM erfahrungsstufen WHERE erfahrungsstufe = $1' into v_erfahrungsstufe_id using p_erfahrungsstufe;
    
    insert into hat_Jobtitel (Mitarbeiter_ID, Jobtitel_ID, Erfahrungsstufe_ID, Mandant_ID, Datum_Von, Datum_Bis)
   		values (v_mitarbeiter_ID, v_jobtitel_id, v_erfahrungsstufe_id, p_mandant_id, p_eintrittsdatum, '9999-12-31');
   	
   	exception
        when unique_violation then
            raise notice 'Mitarbeiter hat bereits diesen Jobtitel und Erfahrungsstufe vermerkt!';
	
   	set role postgres;
   	
end;
$$
language plpgsql;

/*
 * Funktion trägt neue Daten in Tabelle 'Gesellschaften' ein.
 */
create or replace function insert_tbl_gesellschaften (
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
   	
    exception
        when unique_violation then
            raise notice 'Gesellschaft ''%'' bereits vorhanden!', p_gesellschaft;
    
    set role postgres;

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
	
	execute 'SELECT mitarbeiter_ID FROM mitarbeiter WHERE personalnummer = $1' into v_mitarbeiter_ID using p_personalnummer;
	execute 'SELECT gesellschaft_ID FROM gesellschaften WHERE gesellschaft = $1' into v_gesellschaft_id using p_gesellschaft;
    
    insert into in_Gesellschaft (Mitarbeiter_ID, Gesellschaft_ID, Mandant_ID, Datum_Von, Datum_Bis)
   		values (v_mitarbeiter_ID, v_gesellschaft_id, p_mandant_id, p_eintrittsdatum, '9999-12-31');
   	
   	exception
        when unique_violation then
            raise notice 'Mitarbeiter ist bereits in dieser Gesellschaft!';
	
   	set role postgres;
   	
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
	p_eintrittsdatum date, 
	p_grundgehalt_monat decimal(10, 2),
	p_weihnachtsgeld decimal(10,2),
	p_urlaubsgeld decimal(10, 2)
) returns void as
$$
declare
	v_mitarbeiter_id integer;
begin
    
    set session role tenant_user;
    execute 'SET app.current_tenant=' || p_mandant_id;
   
    execute 'SELECT mitarbeiter_ID FROM mitarbeiter WHERE personalnummer = $1' into v_mitarbeiter_ID using p_personalnummer;

    insert into 
   		Aussertarifliche(Mitarbeiter_ID, Mandant_ID, Datum_Von, Datum_Bis, Grundgehalt_monat, Weihnachtsgeld, Urlaubsgeld)
   	values 
   		(v_mitarbeiter_ID, p_mandant_id, p_eintrittsdatum, '9999-12-31', p_grundgehalt_monat, p_weihnachtsgeld, p_urlaubsgeld);
   	
    exception
        when unique_violation then
            raise notice 'Diese Verguetungszahlen sind bereits vorhanden!';
    
    set role postgres;

end;
$$
language plpgsql;

/*
 * Funktion trägt neue Daten in Tabelle 'Privat_Krankenversicherte' ein.
 */
create or replace function insert_tbl_privat_krankenversicherte (
	p_personalnummer varchar(32),
	p_mandant_id integer,
	p_eintrittsdatum date, 
	p_ag_zuschuss_krankenversicherung decimal(10, 2),
	p_ag_zuschuss_zusatzbeitrag decimal(10,2),
	p_ag_zuschuss_pflegeversicherung decimal(10, 2)
) returns void as
$$
declare
	v_mitarbeiter_id integer;
begin
    
    set session role tenant_user;
    execute 'SET app.current_tenant=' || p_mandant_id;
   
    execute 'SELECT mitarbeiter_ID FROM mitarbeiter WHERE personalnummer = $1' into v_mitarbeiter_ID using p_personalnummer;

    insert into 
   		Privat_Krankenversicherte(Mitarbeiter_ID, Mandant_ID, Datum_Von, Datum_Bis, AG_Zuschuss_Krankenversicherung, AG_Zuschuss_Zusatzbeitrag, AG_Zuschuss_Pflegeversicherung)
   	values 
   		(v_mitarbeiter_ID, p_mandant_id, p_eintrittsdatum, '9999-12-31', p_ag_zuschuss_krankenversicherung, p_ag_zuschuss_zusatzbeitrag, p_ag_zuschuss_pflegeversicherung);
   	
    exception
        when unique_violation then
            raise notice 'Dieser Mitarbeiter hat bereits aktuelle Zuschüsse zur privaten Krankenversicherung!';
    
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
	p_eintrittsdatum date
) returns void as
$$
declare
	v_mitarbeiter_id integer;
	v_krankenversicherung_id integer;
begin
	
	set session role tenant_user;
	execute 'SET app.current_tenant=' || p_mandant_id;
		
	-- Pruefen, ob Mandant bereits Eintrag in Tabelle Krankenversicherungen hat...
	execute 'SELECT krankenversicherung_id FROM krankenversicherungen WHERE mandant_id = $1' into v_krankenversicherung_id using p_mandant_id;
    
    -- ... und falls sie nicht existiert, Meldung ausgeben, dass erst die Krankenversicherung hinterlegt werden muss!
    if v_krankenversicherung_id is null then
		set role postgres;
		raise exception 'Sie muessen erst KV-Beitraege und Beitragsbemessungsgrenzen anlegen, bevor Sie Mitarbeiter anlegen!';   
    end if;
   
    execute 'SELECT mitarbeiter_ID FROM mitarbeiter WHERE personalnummer = $1' into v_mitarbeiter_ID using p_personalnummer;
    
    insert into hat_gesetzliche_Krankenversicherung(Mitarbeiter_ID, Krankenversicherung_ID, Mandant_ID, Datum_Von, Datum_Bis)
   		values (v_mitarbeiter_id, v_krankenversicherung_id, p_mandant_id, p_eintrittsdatum, '9999-12-31');
   	
   	exception
        when unique_violation then
        	set role postgres;
            raise notice 'Es ist bereits vermerkt, dass der Mitarbeiter gesetzlich krankenversichert ist!';
	
   	set role postgres;
   	
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
	execute 'SELECT krankenkasse_id FROM krankenkassen WHERE krankenkasse = $1 AND krankenkassenkuerzel = $2'
		into v_krankenkasse_id using p_krankenkasse, p_krankenkassenkuerzel;
    
    -- ... und falls sie nicht existiert, Meldung ausgeben, dass erst die Krankenkasse hinterlegt werden muss!
    if v_krankenkasse_ID is null then
		set role postgres;
		raise exception 'Krankenkasse ''%'' noch nicht hinterlegt! Bitte tragen Sie zuerst die Krankenkasse ein!', p_krankenkasse;   
    end if;
   
    execute 'SELECT mitarbeiter_ID FROM mitarbeiter WHERE personalnummer = $1' into v_mitarbeiter_ID using p_personalnummer;
    
    insert into ist_in_GKV(Mitarbeiter_ID, Krankenkasse_ID, Mandant_ID, Datum_Von, Datum_Bis)
   		values (v_mitarbeiter_id, v_Krankenkasse_id, p_mandant_id, p_eintrittsdatum, '9999-12-31');
   	
   	exception
        when unique_violation then
        	set role postgres;
            raise notice 'Mitarbeiter ist bereits aktuell in Krankenkasse ''%'' vermerkt!', p_krankenkasse;
	
   	set role postgres;
   	
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
   	
   	exception
        when unique_violation then
            raise notice 'Aktuelle Anzahl der Kinder für Mitarbeiter ''%'' ist bereits vermerkt!', p_personalnummer;
	
   	set role postgres;
   	
end;
$$
language plpgsql;

/*
 * Funktion trägt die Daten in die Assoziation "wohnt_in_Sachsen" ein
 */
create or replace function insert_tbl_wohnt_in_sachsen(
	p_mandant_id integer,
	p_personalnummer varchar(32),
	p_in_sachsen boolean,
	p_eintrittsdatum date
) returns void as
$$
declare
	v_mitarbeiter_id integer;
	v_wohnhaft_sachsen_id integer;
begin
	
	set session role tenant_user;
	execute 'SET app.current_tenant=' || p_mandant_id;
	
	execute 'SELECT mitarbeiter_ID FROM mitarbeiter WHERE personalnummer = $1' into v_mitarbeiter_ID using p_personalnummer;
	execute 'SELECT wohnhaft_sachsen_id FROM wohnhaft_sachsen WHERE in_sachsen = $1' into v_wohnhaft_sachsen_id using p_in_sachsen;
    
    insert into wohnt_in_sachsen(Mitarbeiter_ID, wohnhaft_Sachsen_ID, Mandant_ID, Datum_Von, Datum_Bis)
   		values (v_mitarbeiter_id, v_wohnhaft_sachsen_id, p_mandant_id, p_eintrittsdatum, '9999-12-31');
   	
   	exception
        when unique_violation then
            raise notice 'Es ist bereits vermerkt, ob Mitarbeiter ''%'' in Sachsen wohnt!', p_personalnummer;
	
   	set role postgres;
   	
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
   	
   	exception
        when unique_violation then
        	set role postgres;
            raise notice 'Es ist bereits vermerkt, dass der Mitarbeiter gesetzlich arbeitslosenversichert ist!';
	
   	set role postgres;
   	
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
   	
   	exception
        when unique_violation then
        	set role postgres;
            raise notice 'Es ist bereits vermerkt, dass der Mitarbeiter gesetzlich rentenversichert ist!';
	
   	set role postgres;
   	
end;
$$
language plpgsql;

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
    p_austrittsdatum date,
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
	p_abk_gesellschaft varchar(16),
	-- Bereich 'Entgelt'
	p_tarifbeschaeftigt boolean,
	p_tarifbezeichnung varchar(16),
	--p_gewerkschaft varchar(64),
	p_grundgehalt_monat_aussertariflich decimal(10, 2),
	p_weihnachtsgeld_aussertariflich decimal(10,2),
	p_urlaubsgeld_aussertariflich decimal(10, 2),
	-- Bereich 'Kranken- und Pflegeversicherung'
	p_privat_krankenversichert boolean,
	p_ag_zuschuss_krankenversicherung decimal(10, 2),
	p_ag_zuschuss_zusatzbeitrag decimal(10,2),
	p_ag_zuschuss_pflegeversicherung decimal(10, 2),
	
	p_gesetzlich_krankenversichert boolean,
	p_krankenkasse varchar(128),
	p_krankenkassenkuerzel varchar(16),
	p_anzahl_kinder integer,
	p_in_sachsen boolean,
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
								   p_austrittsdatum
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
		perform insert_tbl_geschlechter(p_mandant_id, p_geschlecht);
		perform insert_tbl_hat_geschlecht(p_mandant_id, p_personalnummer, p_geschlecht, p_eintrittsdatum);
	end if;
	
	-- Sofern p_mitarbeitertyp nicht 'null' ist, den Bereich 'Mitarbeitertyp' mit Daten befüllen
	if p_mitarbeitertyp is not null then
		perform insert_tbl_mitarbeitertypen(p_mandant_id, p_mitarbeitertyp);
		perform insert_tbl_ist_mitarbeitertyp(p_mandant_id, p_personalnummer, p_mitarbeitertyp, p_eintrittsdatum);
	end if;

	-- Sofern p_steuerklasse nicht 'null' ist, den Bereich 'Steuerklasse' mit Daten befüllen
	if p_steuerklasse is not null then
		perform insert_tbl_steuerklassen(p_mandant_id, p_steuerklasse);
		perform insert_tbl_in_steuerklasse(p_mandant_id, p_personalnummer, p_steuerklasse, p_eintrittsdatum);
	end if;
	
	-- Sofern p_wochenarbeitsstunden nicht 'null' ist, den Bereich 'Wochenarbeitsstunden' mit Daten befüllen
	if p_wochenarbeitsstunden is not null then
		perform insert_tbl_wochenarbeitsstunden(p_mandant_id, p_wochenarbeitsstunden);
		perform insert_tbl_arbeitet_x_wochenarbeitsstunden(p_mandant_id, p_personalnummer, p_wochenarbeitsstunden, p_eintrittsdatum);
	end if;

	-- Sofern p_abteilung und p_fuehrungskraft nicht 'null' sind, den Bereich 'Abteilung' mit Daten befüllen
	if p_abteilung is not null and p_fuehrungskraft is not null then
		perform insert_tbl_abteilungen(p_mandant_id, p_abteilung, p_abk_abteilung);
		perform insert_tbl_eingesetzt_in(p_mandant_id, p_personalnummer, p_abteilung, p_abk_abteilung, p_fuehrungskraft, p_eintrittsdatum);
	end if;

	-- Sofern p_jobtitel und p_erfahrungsstufe nicht 'null' sind, den Bereich 'Jobtitel' mit Daten befüllen
	if p_jobtitel is not null and p_erfahrungsstufe is not null then
		perform insert_tbl_jobtitel (p_mandant_ID, p_jobtitel);
		perform insert_tbl_erfahrungsstufen (p_Mandant_ID, p_erfahrungsstufe);
		perform insert_tbl_hat_jobtitel(p_mandant_id, p_personalnummer, p_jobtitel, p_erfahrungsstufe, p_eintrittsdatum);
	end if;
	
	-- Sofern p_gesellschaft nicht 'null' ist, den Bereich 'Gesellschaft' mit Daten befüllen
	if p_gesellschaft is not null then
		perform insert_tbl_gesellschaften(p_mandant_id, p_gesellschaft, p_abk_gesellschaft);
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
											p_eintrittsdatum, 
											p_grundgehalt_monat_aussertariflich, 
											p_weihnachtsgeld_aussertariflich, 
											p_urlaubsgeld_aussertariflich);
	end if;

	
	if p_privat_krankenversichert then
		perform insert_tbl_privatkrankenversicherte(p_personalnummer, p_mandant_id, p_eintrittsdatum,  p_ag_zuschuss_krankenversicherung, p_ag_zuschuss_zusatzbeitrag, p_ag_zuschuss_pflegeversicherung);
	end if;

	if p_gesetzlich_krankenversichert then
	
		perform insert_tbl_hat_gesetzliche_Krankenversicherung(p_mandant_id, p_personalnummer, p_eintrittsdatum);
		perform insert_tbl_ist_in_gkv(p_mandant_id, p_personalnummer, p_krankenkasse, p_krankenkassenkuerzel, p_eintrittsdatum);
		perform insert_tbl_hat_x_kinder_unter_25(p_mandant_id, p_personalnummer, p_anzahl_kinder, p_eintrittsdatum);
		perform insert_tbl_wohnt_in_sachsen(p_mandant_id, p_personalnummer, p_in_sachsen, p_eintrittsdatum);									  

	end if;

	if p_arbeitslosenversichert then
			perform insert_tbl_hat_gesetzliche_arbeitslosenversicherung(p_mandant_id, p_personalnummer, p_eintrittsdatum);
	end if;
	
	if p_rentenversichert then
		perform insert_tbl_hat_gesetzliche_rentenversicherung(p_mandant_id, p_personalnummer, p_eintrittsdatum);
	end if;
	
	set role postgres;

end;
$$
language plpgsql;

----------------------------------------------------------------------------------------------------------------
-- Stored Procedures für Use Case "Update neue Adresse für bestehenden Mitarbeiter"

/*
 * Methode schreibt die Daten einer neuen Wohnadresse fuer einen Mitarbeiter ein. Zudem wird der letzte Tag des alten Wohnsitzes im entsprechenden
 * Datensatz der Tabelle 'wohnt_in' eingetragen (zuvor steht dort standardmaessig '9999-12-31'). Die Methode wird auch benutzt, um bei einem neuen
 * Mitarbeiter, wo noch keine Adressdaten hinterlegt sind, dessen Adresse anzulegen. 
 */
create or replace function update_adresse(
	p_mandant_id integer,
	p_personalnummer varchar(32),
	p_neuer_eintrag_gueltig_ab date,
	p_alter_eintrag_gueltig_bis date,
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

	-- Pruefung, ob der Mitarbeiter überhaupt existiert und falls ja, dann Mitarbeiter_ID in Variable speichern
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
	
	-- Pruefung, ob für Mitarbeiter bereits ein Datensatz in 'wohnt_in' existiert. Falls nicht, so wurde für den Mitarbeiter noch kein Wohnort angelegt
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
-- Stored Procedures für Use Case "Update Kündigung Mitarbeiter"
/*
 * Methode ändert die Angaben aufgrund von Kündigung eines bestimmten Mitarbeiters. Es wird das Austrittsdatum in Tabelle 'Mitarbeiter' auf
 * den letzten Arbeitstag geupdatet und der Austrittsgrund bzw. dessen Kategorie in dessen Tabellen vermerkt. 
 */
create or replace function update_mitarbeiterentlassung(
	p_mandant_id integer,
	p_personalnummer varchar(32),
	p_letzter_arbeitstag date,
	p_austrittsgrund varchar(32),
	p_austrittsgrundkategorie varchar(16)
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
	
	-- Austrittsgrund und dessen Kategorie in Datenbank eintragen, sofern noch nicht vorhanden
	perform insert_tbl_kategorien_austrittsgruende(p_mandant_id, p_austrittsgrundkategorie);
	perform insert_tbl_austrittsgruende(p_mandant_id, p_austrittsgrund , p_austrittsgrundkategorie);
	
	-- ID des soeben erstellen Austrittsgrund in Variable speichern, da diese bei der Update-Funktion benötigt wird
	execute 'SELECT austrittsgrund_id FROM austrittsgruende WHERE austrittsgrund = $1' into v_austrittsgrund_id using p_austrittsgrund;
	
	-- Austrittsgrund mit Mitarbeiter verknuepfen
	execute 'UPDATE mitarbeiter SET austrittsdatum = $1, austrittsgrund_id = $2 WHERE personalnummer = $3' 
			using p_letzter_arbeitstag, v_austrittsgrund_id, p_personalnummer;

   	set role postgres;
   	
end;
$$
language plpgsql;

/*
 * Funktion trägt die Daten in die Tabelle "Kategorien_Austrittsgruende" ein
 */
create or replace function insert_tbl_kategorien_austrittsgruende(
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
   	
    exception
        when unique_violation then
            raise notice 'Austrittsgrundkategorie ''%'' bereits vorhanden!', p_austrittsgrundkategorie;

    set role postgres;
   
end;
$$
language plpgsql;

/*
 * Funktion trägt die Daten in die Tabelle "Austrittsgruende" ein
 */
create or replace function insert_tbl_austrittsgruende(
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
   		into v_kategorie_austrittsgruende_id using p_austrittsgrundkategorie;
    
   	insert into 
   		Austrittsgruende(Mandant_ID, Austrittsgrund, Kategorie_Austrittsgruende_ID) 
   	values 
   		(p_mandant_id, p_austrittsgrund, v_kategorie_austrittsgruende_id);
   	
    exception
        when unique_violation then
            raise notice 'Austrittsgrund ''%'' bereits vorhanden!', p_austrittsgrund;

    set role postgres;

end;
$$
language plpgsql;

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

	-- Daten aus Bereich 'Gesellschaften' entfernen
	execute 'DELETE FROM in_gesellschaft WHERE mandant_id = $1' using p_mandant_id;
	execute 'DELETE FROM gesellschaften WHERE mandant_id = $1' using p_mandant_id;

	-- Daten aus Bereich 'Entgelt' entfernen
	execute 'DELETE FROM hat_verguetung WHERE mandant_id = $1' using p_mandant_id;
	execute 'DELETE FROM hat_tarif WHERE mandant_id = $1' using p_mandant_id;
	execute 'DELETE FROM tarife WHERE mandant_id = $1' using p_mandant_id;
	execute 'DELETE FROM gewerkschaften WHERE mandant_id = $1' using p_mandant_id;
	execute 'DELETE FROM verguetungen WHERE mandant_id = $1' using p_mandant_id;
	execute 'DELETE FROM aussertarifliche WHERE mandant_id = $1' using p_mandant_id;

	-- Daten aus Bereich 'Kranken- und Pflegeversicherung' entfernen
	execute 'DELETE FROM privat_krankenversicherte WHERE mandant_id = $1' using p_mandant_id;
	execute 'DELETE FROM hat_kvbeitraege WHERE mandant_id = $1' using p_mandant_id;
	execute 'DELETE FROM krankenversicherungsbeitraege_gesetzlich WHERE mandant_id = $1' using p_mandant_id;
	execute 'DELETE FROM ist_in_gkv WHERE mandant_id = $1' using p_mandant_id;
	execute 'DELETE FROM hat_gkv_zusatzbeitrag WHERE mandant_id = $1' using p_mandant_id;
	execute 'DELETE FROM GKV_zusatzbeitraege WHERE mandant_id = $1' using p_mandant_id;
	execute 'DELETE FROM krankenkassen WHERE mandant_id = $1' using p_mandant_id;
	execute 'DELETE FROM hat_x_kinder_unter_25 WHERE mandant_id = $1' using p_mandant_id;
	execute 'DELETE FROM hat_gesetzlichen_an_pv_beitragssatz WHERE mandant_id = $1' using p_mandant_id;
	execute 'DELETE FROM an_pflegeversicherungsbeitraege_gesetzlich WHERE mandant_id = $1' using p_mandant_id;
	execute 'DELETE FROM anzahl_kinder_unter_25 WHERE mandant_id = $1' using p_mandant_id;
	execute 'DELETE FROM wohnt_in_sachsen WHERE mandant_id = $1' using p_mandant_id;
	execute 'DELETE FROM hat_gesetzlichen_ag_pv_beitragssatz WHERE mandant_id = $1' using p_mandant_id;
	execute 'DELETE FROM ag_pflegeversicherungsbeitraege_gesetzlich WHERE mandant_id = $1' using p_mandant_id;
	execute 'DELETE FROM wohnhaft_sachsen WHERE mandant_id = $1' using p_mandant_id;

	-- Daten aus Bereich 'Arbeitslosenversicherung' entfernen
	execute 'DELETE FROM hat_avbeitraege WHERE mandant_id = $1' using p_mandant_id;
	execute 'DELETE FROM arbeitslosenversicherungsbeitraege_gesetzlich WHERE mandant_id = $1' using p_mandant_id;

	-- Daten aus Bereich 'Rentenversicherung' entfernen
	execute 'DELETE FROM hat_rvbeitraege WHERE mandant_id = $1' using p_mandant_id;
	execute 'DELETE FROM rentenversicherungsbeitraege_gesetzlich WHERE mandant_id = $1' using p_mandant_id;






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
	execute 'DELETE FROM hat_tarif WHERE mitarbeiter_id = $1' using v_mitarbeiter_id;
	
	-- personenbezogene Mitarbeiterdaten aus Bereich 'Adresse' entfernen
	execute 'DELETE FROM wohnt_in WHERE mitarbeiter_id = $1' using v_mitarbeiter_id;

	-- personenbezogene Mitarbeiterdaten aus Bereich 'Gesellschaften' entfernen
	execute 'DELETE FROM in_gesellschaft WHERE mitarbeiter_id = $1' using v_mitarbeiter_id;
	
	-- personenbezogene Mitarbeiterdaten aus Bereich 'Geschlechter' entfernen
	execute 'DELETE FROM hat_geschlecht WHERE mitarbeiter_id = $1' using v_mitarbeiter_id;
	
	-- personenbezogene Mitarbeiterdaten aus Bereich 'Mitarbeiteryp' entfernen
	execute 'DELETE FROM ist_mitarbeitertyp WHERE mitarbeiter_id = $1' using v_mitarbeiter_id;

	-- personenbezogene Mitarbeiterdaten aus Bereich 'Kranken- und Pflegeversicherung' entfernen
	execute 'DELETE FROM privat_krankenversicherte WHERE mitarbeiter_id = $1' using v_mitarbeiter_id;
	execute 'DELETE FROM hat_kvbeitraege WHERE mitarbeiter_id = $1' using v_mitarbeiter_id;
	execute 'DELETE FROM ist_in_gkv WHERE mitarbeiter_id = $1' using v_mitarbeiter_id;
	execute 'DELETE FROM hat_x_kinder_unter_25 WHERE mitarbeiter_id = $1' using v_mitarbeiter_id;
	execute 'DELETE FROM wohnt_in_sachsen WHERE mitarbeiter_id = $1' using v_mitarbeiter_id;

	-- personenbezogene Mitarbeiterdaten aus Bereich 'Arbeitslosenversicherung' entfernen
	execute 'DELETE FROM hat_avbeitraege WHERE mitarbeiter_id = $1' using v_mitarbeiter_id;

	-- personenbezogene Mitarbeiterdaten aus Bereich 'Rentenversicherung' entfernen
	execute 'DELETE FROM hat_rvbeitraege WHERE mitarbeiter_id = $1' using v_mitarbeiter_id;

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