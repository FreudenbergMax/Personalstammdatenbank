-- Quelle: https://adityamattos.com/multi-tenancy-in-python-fastapi-and-sqlalchemy-using-postgres-row-level-security
set role postgres;

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
drop role tenant_user;

-- Erstellung der Rolle 'tenant-user' mit diversen Zugriffsrechten
-- Rolle für die user erstellen, welcher RLS unterliegt
create role tenant_user;
-- tenant-user erbt Berechtigungen von postgres (=Admin)
--grant tenant_user to postgres;
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

set role postgres;

drop table if exists Nutzer;
drop table if exists wohnt_in;
drop table if exists Strassenbezeichnungen;
drop table if exists Postleitzahlen;
drop table if exists Staedte;
drop table if exists Regionen;
drop table if exists Laender;
drop table if exists Mandanten;
drop table if exists mitarbeiter;
drop function if exists erstelle_neue_id(varchar(64), varchar(64));
drop function if exists mandant_anlegen(integer, varchar(128));
drop function if exists nutzer_anlegen(integer, varchar(64), varchar(64), integer);
drop function if exists nutzer_entfernen(integer, varchar(64), varchar(64), integer);
drop function if exists select_ausfuehren(varchar(64), integer);
drop function if exists insert_mitarbeiter(integer,varchar(64),varchar(128),varchar(64),date,date,varchar(32),varchar(32),varchar(32),varchar(16),varchar(64),varchar(16),varchar(64),date,varchar(64),varchar(8),varchar(16),varchar(128),varchar(128),varchar(128));

create table mandanten(
	mandant_id integer primary key,
	firma varchar(128) not null
);

alter table mandanten enable row level security;

-- Erstellung der RLS-Policy mit anschließender Aktivieriung der RLS-Fähigkeit der Tabelle "Mitarbeiter"
create policy filter_mandanten
    on mandanten
    using (mandant_id = current_setting('app.current_tenant')::int);

create table nutzer(
	nutzer_id integer primary key,
	vorname varchar(64) not null,
	nachname varchar(64) not null,
	mandant_id integer not null,
	constraint fk_Nutzer_mandanten
		foreign key (mandant_id) 
			references mandanten(mandant_id)
);

alter table nutzer enable row level security;

-- Erstellung der RLS-Policy mit anschließender Aktivieriung der RLS-Fähigkeit der Tabelle "Mitarbeiter"
create policy filter_nutzer
    on nutzer
    using (mandant_id = current_setting('app.current_tenant')::int);
   
create table Mitarbeiter (
    Mitarbeiter_ID serial primary key,
    Mandant_ID integer not null,
    Vorname varchar(64) not null,
    Zweitname varchar(128),
    Nachname varchar(64) not null,
    Geburtsdatum date,
    Eintrittsdatum date, 
    Steuernummer varchar(32),
    Sozialversicherungsnummer varchar(32),
    IBAN varchar(32),
    Private_Telefonnummer varchar(16),
    Private_Emailadresse varchar(64),
    dienstliche_Telefonnummer varchar(16),
    dienstliche_Emailadresse varchar(64),
    Austrittsdatum date
);

alter table Mitarbeiter enable row level security;

-- Erstellung der RLS-Policy mit anschließender Aktivieriung der RLS-Fähigkeit der Tabelle "Mitarbeiter"
create policy FilterMandant_Mitarbeiter
    on mitarbeiter
    using (mandant_id = current_setting('app.current_tenant')::int);

-- Tabellen, die den Bereich "Adresse" behandeln, erstellen
create table Laender (
	Land_ID serial primary key,
	Mandant_ID integer not null,
	Land varchar(128) not null,
    constraint fk_laender_mandanten
		foreign key (Mandant_ID) 
			references Mandanten(Mandant_ID)
);
alter table Laender enable row level security;
create policy FilterMandant_Laender
    on Laender
    using (mandant_id = current_setting('app.current_tenant')::int);

create table Regionen (
	Region_ID serial primary key,
	Mandant_ID integer not null,
	Region varchar(128) not null,
	Land_ID integer not null,
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
    using (mandant_id = current_setting('app.current_tenant')::int);

create table Staedte (
	Stadt_ID serial primary key,
	Mandant_ID integer not null,
	stadt varchar(128) not null,
	Region_ID integer not null,
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
    using (mandant_id = current_setting('app.current_tenant')::int);

create table Postleitzahlen (
	Postleitzahl_ID serial primary key,
	Mandant_ID integer not null,
	Postleitzahl varchar(16) not null,
	Stadt_ID integer not null,
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
    using (mandant_id = current_setting('app.current_tenant')::int);

create table Strassenbezeichnungen (
	Strassenbezeichnung_ID serial primary key,
	Mandant_ID integer not null,
	Strasse varchar(64) not null,
	Hausnummer varchar(8) not null,
	Postleitzahl_ID integer not null,
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
    using (mandant_id = current_setting('app.current_tenant')::int);

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
    using (mandant_id = current_setting('app.current_tenant')::int);

   
   
   
create or replace function erstelle_neue_id(
	p_id_spalte varchar(64),
	p_tabelle varchar(64)
) returns integer as
$$
declare 
	v_neue_id integer;
begin

    -- Neue ID erstellen
    execute 'SELECT MAX(' || p_id_spalte || ') + 1 FROM ' || p_tabelle into v_neue_id;
   
    if v_neue_id is null then
    	v_neue_id := 1;
	end if;

    return v_neue_id;
	
end;
$$
language plpgsql;



create or replace function bekomme_aktuelle_Mitarbeiter_ID(
) returns integer as
$$
declare 
	v_neue_id integer;
begin

    -- Neue ID erstellen
    execute 'SELECT MAX(Mitarbeiter_ID) FROM Mitarbeiter' into v_neue_id;
   
    if v_neue_id is null then
    	v_neue_id := 1;
	end if;

    return v_neue_id;
	
end;
$$
language plpgsql;



create or replace function mandant_anlegen(
	p_mandant_id integer,
	p_firma varchar(128)
) returns void as
$$
begin

    insert into Mandanten(Mandant_ID, Firma)
		values(p_mandant_id, p_firma);

end;
$$
language plpgsql;



create or replace function nutzer_anlegen(
	p_nutzer_id integer,
	p_vorname varchar(64),
	p_nachname varchar(64),
	p_mandant_id integer
) returns void as
$$
begin

    insert into Nutzer(nutzer_ID, vorname, Nachname, Mandant_ID)
		values(p_nutzer_id, p_vorname, p_nachname, p_mandant_id);

end;
$$
language plpgsql;



create or replace function nutzer_entfernen(
	p_nutzer_id integer,
	p_vorname varchar(64),
	p_nachname varchar(64),
	p_mandant_id integer
) returns void as
$$
begin
	
	set session role tenant_nutzer;
	execute 'SET app.current_tenant=' || p_mandant_id;
	
    delete from nutzer 
    where nutzer_id = p_nutzer_id 
    	and vorname = p_vorname 
    	and nachname = p_nachname 
    	and mandant_id = p_mandant_id;

end;
$$
language plpgsql;



-- Quelle: https://www.sqlines.com/postgresql/how-to/return_result_set_from_stored_procedure
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



create or replace function insert_mitarbeiterdaten(
	p_mandant_id integer,
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
	
	insert into mitarbeiter(Mandant_ID,
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
						    Austrittsdatum
	)values(p_mandant_id,
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

end;
$$
language plpgsql;



create or replace function insert_tbl_mitarbeiter(
	p_mandant_id integer,
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
	p_land varchar(128)	
) returns void as
$$
declare 
	v_mitarbeiter_id integer;
	v_id_tabelle1 integer;
	v_id_tabelle2 integer;
begin
	
	set session role tenant_user;
	execute 'SET app.current_tenant=' || p_mandant_id;
	
	-- Frage: soll noch eine extre Spalte "Personalnummer" dazukommen? Wenn ja, als Primärschlüssel verwenden? --> ausführlich erörtern!

	select insert_tbl_mitarbeiter(	p_mandant_id,
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
	
	v_mitarbeiter_id := bekomme_aktuelle_Mitarbeiter_ID();
	
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


