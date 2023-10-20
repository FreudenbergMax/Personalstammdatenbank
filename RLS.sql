set role postgres;
drop table if exists ist_Mitarbeitertyp;
drop table if exists Mitarbeitertypen;
drop table if exists Mitarbeiter;

-- Funktion soll sicherstellen, dass für ein Mandant nur die Datensätze sichtbar sind, wenn in der Spalte "Mandant" dessen Name steht 
create or replace function fn_RowLevelSecurity(Mandant text)
returns boolean as $$
begin
  return Mandant = current_user;
end;
$$ language plpgsql;

create table Mitarbeiter (
    Mitarbeiter_ID integer primary key,
    Mandant varchar(128) not null,
    Vorname varchar(64) not null,
    Nachname varchar(64) not null,
    Geschlecht varchar(16) check (Geschlecht in ('weiblich', 'maennlich', 'divers')) not null,
    Geburtsdatum date not null,
    Eintrittsdatum date not null, 
    Steuernummer varchar(32) not null,
    Sozialversicherungsnummer varchar(32) not null,
    IBAN varchar(32) not null,
    Telefonnummer varchar(16) not null,
    Private_Emailadresse varchar(64) not null,
    Austrittsdatum date
);

-- Erstellung der RLS-Policy mit anschließender Aktivieriung der RLS-Fähigkeit der Tabelle "Mitarbeiter"
create policy FilterMandant_Mitarbeiter
    on mitarbeiter
    for all
    using (fn_RowLevelSecurity(Mandant));

alter table Mitarbeiter enable row level security;

-- Tabellen, die den Bereich "Mitarbeitertyp" (Angestellter, Arbeiter, Praktikant, Werkstudent etc.) behandeln, erstellen
create table Mitarbeitertypen (
	Mitarbeitertyp_ID integer primary key,
	Mandant varchar(128) not null,
	Bezeichnung varchar(32)
);

-- Erstellung der RLS-Policy mit anschließender Aktivieriung der RLS-Fähigkeit der Tabelle "Mitarbeitertypen"
create policy FilterMandant_Mitarbeitertypen
    on mitarbeitertypen
    for all
    using (fn_RowLevelSecurity(Mandant));

alter table Mitarbeitertypen enable row level security;

-- Assoziationstabelle zwischen Mitarbeiter und Mitarbeitertyp
create table ist_Mitarbeitertyp (
	Mitarbeiter_ID integer not null,
	Mitarbeitertyp_ID integer not null,
	Mandant varchar(128) not null,
	Datum_Von date not null,
    Datum_Bis date not null,
    primary key (Mitarbeiter_ID, Datum_Bis),
    constraint fk_istmitarbeitertyp_mitarbeiter
    	foreign key (Mitarbeiter_ID) 
    		references Mitarbeiter(Mitarbeiter_ID),
    constraint fk_istmitarbeitertyp_mitarbeitertypen
    	foreign key (Mitarbeitertyp_ID) 
    		references Mitarbeitertypen(Mitarbeitertyp_ID)
);

-- Erstellung der RLS-Policy mit anschließender Aktivieriung der RLS-Fähigkeit der Tabelle "ist_Mitarbeitertyp"
create policy FilterMandant_istMitarbeitertyp
    on ist_Mitarbeitertyp
    for all
    using (fn_RowLevelSecurity(Mandant));

alter table ist_Mitarbeitertyp enable row level security;

-- User und Gruppe löschen, falls existent
drop user if exists firma;
drop user if exists unternehmen;
drop group if exists mandantengruppe;

-- Mandantengruppe erstellen und mit Privilegien ausstatten
create group mandantengruppe;
grant select, insert, update, delete on mitarbeiter to mandantengruppe;
grant select, insert, update, delete on Mitarbeitertypen to mandantengruppe;
grant select, insert, update, delete on ist_Mitarbeitertyp to mandantengruppe;





CREATE OR REPLACE FUNCTION erstelle_user(
	p_user varchar(128)
) RETURNS void AS
$$
begin
	
	set role postgres;
	
    -- Überprüfen, ob der Benutzer bereits existiert
    IF NOT EXISTS (SELECT 1 FROM pg_user WHERE usename = p_user) THEN
        -- Benutzer erstellen, falls er nicht existiert
        EXECUTE 'CREATE USER ' || p_user;
        -- Benutzer der Mandantengruppe zuordnen
        execute 'alter group mandantengruppe add user ' || p_user;
        RAISE NOTICE 'Benutzer % wurde erfolgreich erstellt.', p_user;
    ELSE
        RAISE NOTICE 'Benutzer % existiert bereits.', p_user;
    END IF;
   
    EXECUTE 'SET ROLE ' || p_user; 
   
END;
$$
LANGUAGE plpgsql;

select erstelle_user('firma');
select erstelle_user('unternehmen');
set role postgres;





CREATE OR REPLACE FUNCTION erstelle_neue_id(
	p_user varchar(128),
	p_id_spalte varchar(64),
	p_tabelle varchar(64)
) RETURNS integer as
$$
declare 
	v_neue_id integer;
begin
	
	-- Rolle auf admin setzen, damit folgende Abfrage den höchsten ID-Wert berechnen kann
    SET ROLE postgres;

    -- Neue ID erstellen
    EXECUTE 'SELECT MAX(' || p_id_spalte || ') + 1 FROM ' || p_tabelle INTO v_neue_id;
   
    IF v_neue_id IS NULL THEN
    	v_neue_id := 1;
	END IF;
   	
	-- Zurück auf Rolle des Anfragestellers setzen, damit er nicht die Zugriffsrechte das Admins hat
   	EXECUTE 'SET ROLE ' || p_user; 

    RETURN v_neue_id;
	
END;
$$
LANGUAGE plpgsql;

select erstelle_neue_id('firma', 'mitarbeiter_ID', 'mitarbeiter');
set role postgres;




CREATE OR REPLACE FUNCTION insert_neuer_mitarbeiter(
	p_user varchar(128),
	p_vorname varchar(100), 
	p_nachname varchar(100), 
	p_geschlecht varchar(10), 
	p_geburtsdatum date, 
	p_eintrittsdatum date, 
	p_steuernummer varchar(50), 
	p_sozialversicherungsnummer varchar(50), 
	p_iban varchar(50), 
	p_telefonnummer varchar(50), 
	p_private_emailadresse varchar(100),
	p_mitarbeitertyp varchar(32)
) RETURNS void AS
$$
declare 
	v_mitarbeiter_id integer;
	v_mitarbeitertyp_id integer;
begin
	
	EXECUTE 'SET ROLE ' || p_user;

	-- neue Mitarbeiter-ID erstellen
    v_mitarbeiter_id := erstelle_neue_id(p_user, 'mitarbeiter_ID', 'mitarbeiter');
	
	insert into mitarbeiter(Mitarbeiter_ID, 
							mandant, 
							vorname, 
							nachname, 
							geschlecht, 
							geburtsdatum, 
							eintrittsdatum, 
							steuernummer, 
							sozialversicherungsnummer, 
							iban, 
							telefonnummer, 
							private_emailadresse) 
	values(v_mitarbeiter_id,
		   p_user, 
		   p_vorname, 
		   p_nachname, 
		   p_geschlecht, 
		   p_geburtsdatum, 
		   p_eintrittsdatum, 
		   p_steuernummer, 
		   p_sozialversicherungsnummer, 
		   p_iban, 
		   p_telefonnummer, 
		   p_private_emailadresse);
	
	-- neue Mitarbeitertyp-ID erstellen
	v_mitarbeitertyp_id := erstelle_neue_id(p_user, 'mitarbeitertyp_ID', 'mitarbeitertypen');

	insert into mitarbeitertypen(Mitarbeitertyp_ID, mandant, bezeichnung)
		values(v_mitarbeitertyp_id, p_user, p_mitarbeitertyp);
	
	insert into ist_Mitarbeitertyp(Mitarbeiter_ID, Mitarbeitertyp_ID, Mandant, Datum_Von, Datum_Bis)
		values(v_mitarbeiter_id, v_mitarbeitertyp_id, p_user, p_eintrittsdatum, '9999-12-31');
	
END;
$$
LANGUAGE plpgsql;

set role firma;
select insert_neuer_mitarbeiter('firma', 
								'Max', 
								'Freudenberg', 
								'maennlich', 
								'12.12.1992', 
								'01.11.2023', 
								'11 111 111 111', 
								'00 121292 F 00', 
								'DE00 0000 0000 0000 0000 00', 
								'0175 2572025', 
								'maxfreudenberg@web.de',
								'Angestellter');

set role unternehmen;
select insert_neuer_mitarbeiter('unternehmen', 
								'Erika', 
								'Musterfrau', 
								'weiblich', 
								'01.01.1995', 
								'01.01.2024', 
								'99 999 999 999', 
								'00 010195 F 00', 
								'DE99 9999 9999 9999 9999 99', 
								'0175 1234567', 
								'erikamusterfrau@web.de',
								'Werkstudent');


							
							

-- Test 1: Mandant 'firma' darf nur seinen Datensatz sehen
set role firma;

select 
	*
from 
	mitarbeiter;

select 
	*
from 
	mitarbeitertypen;

select 
	* 
from 
	ist_Mitarbeitertyp;

select 
	* 
from 
	mitarbeiter
	inner join ist_Mitarbeitertyp on ist_Mitarbeitertyp.Mitarbeiter_ID = Mitarbeiter.Mitarbeiter_ID
	inner join mitarbeitertypen on ist_Mitarbeitertyp.Mitarbeitertyp_ID = Mitarbeitertypen.Mitarbeitertyp_ID;


-- Test 2: Mandant 'unternehmen' darf nur seinen Datensatz sehen
set role unternehmen;

select 
	*
from 
	mitarbeiter;

select 
	*
from 
	mitarbeitertypen;

select 
	* 
from 
	ist_Mitarbeitertyp;

select 
	* 
from 
	mitarbeiter
	inner join ist_Mitarbeitertyp on ist_Mitarbeitertyp.Mitarbeiter_ID = Mitarbeiter.Mitarbeiter_ID
	inner join mitarbeitertypen on ist_Mitarbeitertyp.Mitarbeitertyp_ID = Mitarbeitertypen.Mitarbeitertyp_ID;

							
-- Test 3: Superuser 'postgres' sieht beide Datensätze
set role postgres;

select 
	*
from 
	mitarbeiter;

select 
	*
from 
	mitarbeitertypen;

select 
	* 
from 
	ist_Mitarbeitertyp;

select 
	* 
from 
	mitarbeiter
	inner join ist_Mitarbeitertyp on ist_Mitarbeitertyp.Mitarbeiter_ID = Mitarbeiter.Mitarbeiter_ID
	inner join mitarbeitertypen on ist_Mitarbeitertyp.Mitarbeitertyp_ID = Mitarbeitertypen.Mitarbeitertyp_ID;
	
SELECT * FROM pg_catalog.pg_user;