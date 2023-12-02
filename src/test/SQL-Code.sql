set role postgres;

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

drop table if exists mitarbeiter;
drop table if exists Austrittsgruende;
drop table if exists Kategorien_Austrittsgruende;
drop table if exists Nutzer;
drop table if exists Mandanten;

drop function if exists mandant_anlegen(varchar(128));
drop function if exists nutzer_anlegen(integer, varchar(32), varchar(64), varchar(64));
drop function if exists nutzer_entfernen(integer, varchar(32));
drop function if exists select_ausfuehren(varchar(64), integer);
drop function if exists insert_mitarbeiterdaten(integer, varchar(32), varchar(64), varchar(128), varchar(64), date, date, varchar(32), varchar(32), varchar(32),
varchar(16), varchar(64), varchar(16), varchar(64), date, varchar(64), varchar(8), varchar(16), varchar(128), varchar(128), varchar(128), varchar(32), varchar(32),
char(1), decimal(4, 2), varchar(64), varchar(16), boolean, varchar(32), varchar(32));
drop function if exists pruefe_einmaligkeit_personalnummer(integer, varchar(64), varchar(32));
drop function if exists insert_tbl_mitarbeiter(integer, varchar(32), varchar(64), varchar(128), varchar(64), date, date,  varchar(32), varchar(32), varchar(32), 
varchar(16), varchar(64), varchar(16), varchar(64), date);
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





----------------------------------------------------------------------------------------------------------------
-- Erstellung der Tabellen einschließlich von Row-Level-Security (RLS)

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
	Austrittsgrund varchar(64) not null,
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
    Austrittsdatum date
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
	Bezeichnung varchar(64) not null,
	Abkuerzung varchar(16),
	untersteht_Abteilung integer,
	unique (Mandant_ID, Bezeichnung, Abkuerzung),
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
   		Abteilungen(Mandant_ID, Bezeichnung, Abkuerzung, untersteht_Abteilung)
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
	execute 'SELECT abteilung_ID FROM abteilungen WHERE bezeichnung = $1 AND abkuerzung = $2' into v_abteilung_id using p_abteilung, p_abkuerzung;
    
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
 * Mit dieser Funktion sollen die Daten eines neuen Mitarbeiters in die Tabelle eingetragen werden
 */
create or replace function insert_mitarbeiterdaten(
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
    p_austrittsdatum date,
    p_strasse varchar(64),
	p_hausnummer varchar(8),
	p_postleitzahl varchar(16),
	p_stadt varchar(128),
	p_region varchar(128),
	p_land varchar(128),
	p_geschlecht varchar(32),
	p_mitarbeitertyp varchar(32),
	p_steuerklasse char(1),
	p_wochenarbeitsstunden decimal(4, 2),
	p_abteilung varchar(64),
	p_abkuerzung varchar(16),
	p_fuehrungskraft boolean,
	p_jobtitel varchar(32),
	p_erfahrungsstufe varchar(32)
) returns void as
$$
begin
	
	set session role tenant_user;
	execute 'SET app.current_tenant=' || p_mandant_id;
	
	perform pruefe_einmaligkeit_personalnummer(p_mandant_id, 'mitarbeiter', p_personalnummer);
	
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
								   p_austrittsdatum);
	
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
		perform insert_tbl_abteilungen(p_mandant_id, p_abteilung, p_abkuerzung);
		perform insert_tbl_eingesetzt_in(p_mandant_id, p_personalnummer, p_abteilung, p_abkuerzung, p_fuehrungskraft, p_eintrittsdatum);
	end if;

	-- Sofern p_jobtitel und p_erfahrungsstufe nicht 'null' sind, den Bereich 'Jobtitel' mit Daten befüllen
	if p_jobtitel is not null and p_erfahrungsstufe is not null then
		perform insert_tbl_jobtitel (p_mandant_ID, p_jobtitel);
		perform insert_tbl_erfahrungsstufen (p_Mandant_ID, p_erfahrungsstufe);
		perform insert_tbl_hat_jobtitel(p_mandant_id, p_personalnummer, p_jobtitel, p_erfahrungsstufe, p_eintrittsdatum);
	end if;
	
	-- Pseudocode Tarif oder AT
	-- if Tarifbezeichnung not null:
		-- Tabellen des Bereichs "Tarif" bearbeiten
	-- else:
		-- Tabelle "Aussertarifliche" bearbeiten

	-- Pseudocode gesetzlich oder privat versichert
	-- if privat versichert:
		-- befülle Tabelle "privat_krankenversichert"
		-- befülle Tabellen im Bereich "Arbeitslosenversicherung", falls notwendig
		-- befülle Tabellen im Bereich "Rentenversicherung", falls notwendig
		-- befülle Tabellen im Bereich "Unfallversicherung", falls notwendig
	-- else:
		-- befülle alle Tabellen im Bereich "Sozialversicherungen"

end;
$$
language plpgsql;



/*
 * Diese Funktion nimmt eine SELECT-Anfrage (z.B. zwecks Abfrage für eine Datenanalyse) 
 * entgegen. Sie soll sicherstellen, dass dabei nur die Daten berücksichtigt werden,
 * die die entsprechende Mandant_ID des Nutzers hat.
 * 
 * Quelle: https://www.sqlines.com/postgresql/how-to/return_result_set_from_stored_procedure
 */
create or replace function select_ausfuehren(
	p_tabelle varchar(64),
	p_mandant_id integer
) returns text as
$$
declare 
	resultset text;
begin
	
	set session role tenant_user;
	execute 'SET app.current_tenant=' || p_mandant_id;
    execute 'SELECT firma FROM ' || p_tabelle into resultset;

    return resultset;

end;
$$
language plpgsql;