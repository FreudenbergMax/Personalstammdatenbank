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
drop role if exists tenant_user;

-- Erstellung der Rolle 'tenant-user' mit diversen Zugriffsrechten
-- Rolle für die user erstellen, welcher RLS unterliegt
create role tenant_user;
-- tenant-user erbt Berechtigungen von postgres (=Admin)
--grant tenant_user to postgres;
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
drop function if exists bekomme_aktuelle_Mitarbeiter_ID();
drop function if exists erstelle_neue_id(varchar(64), varchar(64));
drop function if exists mandant_anlegen(integer, varchar(128));
drop function if exists nutzer_anlegen(integer, integer, varchar(32), varchar(64), varchar(64));
drop function if exists nutzer_entfernen(integer, varchar(32));
drop function if exists select_ausfuehren(varchar(64), integer);
drop function if exists insert_mitarbeiterdaten(
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
	p_land varchar(128));
drop function if exists pruefe_einmaligkeit_personalnummer(integer, varchar(64), varchar(32));
drop function if exists insert_tbl_mitarbeiter(
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
    p_austrittsdatum date);
drop function if exists insert_tbl_laender(p_mandant_id integer, p_land varchar(128));
drop function if exists insert_tbl_regionen(p_mandant_id integer, p_region varchar(128), p_land varchar(128));
drop function if exists insert_tbl_staedte(p_mandant_id integer, p_stadt varchar(128), p_region varchar(128));
drop function if exists insert_tbl_postleitzahlen(p_mandant_id integer, p_postleitzahl varchar(16), p_stadt varchar(128));
drop function if exists insert_tbl_strassenbezeichnungen(p_mandant_id integer, p_strasse varchar(64), p_hausnummer varchar(8), p_postleitzahl varchar(16));
drop function if exists insert_tbl_wohnt_in(p_mandant_id integer, p_personalnummer varchar(32), p_strasse varchar(64), p_hausnummer varchar(8), p_eintrittsdatum date);
	

create table Mandanten(
	Mandant_ID integer primary key,
	Firma varchar(128) not null
);

alter table Mandanten enable row level security;

-- Erstellung der RLS-Policy mit anschließender Aktivieriung der RLS-Fähigkeit der Tabelle "Mitarbeiter"
create policy FilterMandant_Mandanten
    on Mandanten
    using (Mandant_ID = current_setting('app.current_tenant')::int);

create table Nutzer(
	Nutzer_ID integer primary key,
	Mandant_ID integer not null,
	Personalnummer varchar(32) not null,
	Vorname varchar(64) not null,
	Nachname varchar(64) not null,
	constraint fk_Nutzer_mandanten
		foreign key (Mandant_ID) 
			references Mandanten(Mandant_ID)
);

alter table Nutzer enable row level security;

-- Erstellung der RLS-Policy mit anschließender Aktivieriung der RLS-Fähigkeit der Tabelle "Mitarbeiter"
create policy FilterMandant_Nutzer
    on Nutzer
    using (Mandant_ID = current_setting('app.current_tenant')::int);
   
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

-- Erstellung der RLS-Policy mit anschließender Aktivieriung der RLS-Fähigkeit der Tabelle "Mitarbeiter"
create policy FilterMandant_Mitarbeiter
    on Mitarbeiter
    using (Mandant_ID = current_setting('app.current_tenant')::int);

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
    using (Mandant_ID = current_setting('app.current_tenant')::int);

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
    using (Mandant_ID = current_setting('app.current_tenant')::int);

create table Staedte (
	Stadt_ID serial primary key,
	Mandant_ID integer not null,
	Stadt varchar(128) not null,
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
    using (Mandant_ID = current_setting('app.current_tenant')::int);

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
    using (Mandant_ID = current_setting('app.current_tenant')::int);

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

/*
 * Funktion erstellt eine neue ID. Sie wird verwendet, um für neu anzulegende Mandanten und Nutzer die 
 * entsprechende Mandant_ID bzw. Nutzer_ID zu erzeugen.
 */
create or replace function erstelle_neue_id(
	p_id_spalte varchar(64),
	p_tabelle varchar(64)
) returns integer as
$$
declare 
	v_neue_id integer;
begin

	set role postgres;

    -- Neue ID erstellen
    execute 'SELECT MAX(' || p_id_spalte || ') + 1 FROM ' || p_tabelle into v_neue_id;
   
    if v_neue_id is null then
    	v_neue_id := 1;
	end if;

    return v_neue_id;
	
end;
$$
language plpgsql;

/*
 * Funktion trägt die Daten eines neuen Mandanten in die Datenbank ein.
 */
create or replace function mandant_anlegen(
	p_mandant_id integer,
	p_firma varchar(128)
) returns void as
$$
begin

	set session role tenant_user;
	execute 'SET app.current_tenant=' || p_mandant_id;

    insert into Mandanten(Mandant_ID, Firma)
		values(p_mandant_id, p_firma);

	set role postgres;

end;
$$
language plpgsql;

/*
 * Funktion trägt die Daten eines neuen Nutzers in die Datenbank ein.
 */
create or replace function nutzer_anlegen(
	p_nutzer_id integer,
	p_mandant_id integer,
	p_personalnummer varchar(32),
	p_vorname varchar(64),
	p_nachname varchar(64)
) returns void as
$$
begin

	set session role tenant_user;
	execute 'SET app.current_tenant=' || p_mandant_id;
	
	perform pruefe_einmaligkeit_personalnummer(p_mandant_id, 'nutzer', p_personalnummer);

    insert into Nutzer(Nutzer_ID, Mandant_ID, Personalnummer, Vorname, Nachname)
		values(p_nutzer_id, p_mandant_id, p_personalnummer, p_vorname, p_nachname);
	
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
declare
	v_land_vorhanden varchar(128);
begin
	
	set session role tenant_user;
	execute 'SET app.current_tenant=' || p_mandant_id;

	execute 'SELECT land FROM laender WHERE land = $1' INTO v_land_vorhanden USING p_land;
    
    if v_land_vorhanden is null then
    	insert into Laender(Mandant_ID, Land) values (p_mandant_id, p_land);
	else
		raise notice 'Land % ist bereits vorhanden!', v_land_vorhanden;
	end if;

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
	v_region_vorhanden varchar(128);
	v_land_id integer;
begin
	
	set session role tenant_user;
	execute 'SET app.current_tenant=' || p_mandant_id;

	execute 'SELECT region FROM regionen WHERE region = $1' INTO v_region_vorhanden USING p_region;
    
    if v_region_vorhanden is null then
    	execute 'SELECT land_id FROM laender WHERE land = $1' into v_land_id using p_land;
    	insert into Regionen(Mandant_ID, Region, Land_ID) values (p_mandant_id, p_region, v_land_id);
	else
		raise notice 'Region % ist bereits vorhanden!', v_region_vorhanden;
	end if;

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
	v_stadt_vorhanden varchar(128);
	v_region_id integer;
begin
	
	set session role tenant_user;
	execute 'SET app.current_tenant=' || p_mandant_id;

	execute 'SELECT stadt FROM staedte WHERE stadt = $1' INTO v_stadt_vorhanden USING p_stadt;
    
    if v_stadt_vorhanden is null then
    	execute 'SELECT region_id FROM regionen WHERE region = $1' into v_region_id using p_region;
    	insert into Staedte(Mandant_ID, Stadt, Region_ID) values (p_mandant_id, p_stadt, v_region_id);
	else
		raise notice 'Stadt % ist bereits vorhanden!', v_stadt_vorhanden;
	end if;

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
	v_postleitzahl_vorhanden varchar(16);
	v_stadt_id integer;
begin
	
	set session role tenant_user;
	execute 'SET app.current_tenant=' || p_mandant_id;

	execute 'SELECT postleitzahl FROM postleitzahlen WHERE postleitzahl = $1' INTO v_postleitzahl_vorhanden USING p_postleitzahl;
    
    if v_postleitzahl_vorhanden is null then
    	execute 'SELECT stadt_id FROM staedte WHERE stadt = $1' into v_stadt_id using p_stadt;
    	insert into Postleitzahlen(Mandant_ID, Postleitzahl, Stadt_ID) values (p_mandant_id, p_postleitzahl, v_stadt_id);
	else
		raise notice 'Postleitzahl % ist bereits vorhanden!', v_postleitzahl_vorhanden;
	end if;

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
	v_strasse_vorhanden varchar(64);
	v_hausnummer_vorhanden varchar(8);
	v_strassenbezeichnung varchar(128);
	v_postleitzahlen_id integer;
begin
	
	set session role tenant_user;
	execute 'SET app.current_tenant=' || p_mandant_id;

	execute 'SELECT strasse FROM strassenbezeichnungen WHERE strasse = $1' into v_strasse_vorhanden using p_strasse;
	execute 'SELECT hausnummer FROM strassenbezeichnungen WHERE hausnummer = $1' into v_hausnummer_vorhanden using p_hausnummer;
    
	-- Neuer Eintrag, wenn Strassenbezeichnung nicht oder nur unvollständig vorhanden 
    if (v_strasse_vorhanden is null and v_hausnummer_vorhanden is null) or (v_strasse_vorhanden is null and v_hausnummer_vorhanden is not null) or (v_strasse_vorhanden is not null and v_hausnummer_vorhanden is null) then
    	execute 'SELECT postleitzahl_id FROM postleitzahlen WHERE Postleitzahl = $1' into v_postleitzahlen_id using p_postleitzahl;
		insert into strassenbezeichnungen(Mandant_ID, Strasse, Hausnummer, Postleitzahl_ID) values (p_mandant_id, p_strasse, p_hausnummer, v_postleitzahlen_id);
	else
		v_strassenbezeichnung := v_strasse_vorhanden || v_hausnummer_vorhanden;
		raise notice 'Strassenbezeichnung % ist bereits vorhanden!', v_strassenbezeichnung;
	end if;

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
    
    insert into wohnt_in(Mitarbeiter_ID, Strassenbezeichnung_ID, Mandant_ID, Datum_Von, Datum_Bis) 
   		values (v_mitarbeiter_ID, v_strassenbezeichnung_id, p_mandant_id, p_eintrittsdatum, '9999-12-31');

end;
$$
language plpgsql;



/*
 * Zentrale Funktion, mit der die Daten eines neuen Mitarbeiters in die Datenbank eingetragen werden soll.
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
	p_land varchar(128)
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
	
	
	-- wenn einer dieser Werte 'null' ist, dann dürfen die Adress-Tabellen nicht befüllt werden!
	perform insert_tbl_laender(p_mandant_id, p_land);
	perform insert_tbl_regionen(p_mandant_id, p_region, p_land);
	perform insert_tbl_staedte(p_mandant_id, p_stadt, p_region);
	perform insert_tbl_postleitzahlen(p_mandant_id, p_postleitzahl,p_stadt);
	perform insert_tbl_strassenbezeichnungen(p_mandant_id, p_strasse, p_hausnummer, p_postleitzahl);
	perform insert_tbl_wohnt_in(p_mandant_id, p_personalnummer, p_strasse, p_hausnummer, p_eintrittsdatum);
	
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

