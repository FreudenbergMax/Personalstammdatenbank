create schema if not exists temp_test_schema;

set search_path to temp_test_schema;

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
	Mitarbeitertyp varchar(32)
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





CREATE OR REPLACE FUNCTION erstelle_mandant(
	p_mandant varchar(128)
) RETURNS void AS
$$
begin
	
    -- Überprüfen, ob der Benutzer bereits existiert
    IF NOT EXISTS (SELECT 1 FROM pg_user WHERE usename = p_mandant) THEN
        -- Benutzer erstellen, falls er nicht existiert
        EXECUTE 'CREATE USER ' || p_mandant;
        -- Benutzer der Mandantengruppe zuordnen
        execute 'alter group mandantengruppe add user ' || p_mandant;
        RAISE NOTICE 'Benutzer % wurde erfolgreich erstellt.', p_mandant;
    ELSE
        RAISE NOTICE 'Benutzer % existiert bereits.', p_mandant;
    END IF;
   
END;
$$
LANGUAGE plpgsql;





CREATE OR REPLACE FUNCTION erstelle_neue_id(
	p_mandant varchar(128),
	p_id_spalte varchar(64),
	p_tabelle varchar(64)
) RETURNS integer as
$$
declare 
	v_neue_id integer;
begin

    -- Neue ID erstellen
    EXECUTE 'SELECT MAX(' || p_id_spalte || ') + 1 FROM ' || p_tabelle INTO v_neue_id;
   
    IF v_neue_id IS NULL THEN
    	v_neue_id := 1;
	END IF;

    RETURN v_neue_id;
	
END;
$$
LANGUAGE plpgsql;





CREATE OR REPLACE FUNCTION insert_tbl_mitarbeiter(
	p_mandant varchar(128),
	p_vorname varchar(64), 
	p_nachname varchar(64), 
	p_geschlecht varchar(16), 
	p_geburtsdatum date, 
	p_eintrittsdatum date, 
	p_steuernummer varchar(32), 
	p_sozialversicherungsnummer varchar(32), 
	p_iban varchar(32), 
	p_telefonnummer varchar(16), 
	p_private_emailadresse varchar(64)
) RETURNS void AS
$$
declare 
	v_mitarbeiter_id integer;
begin
	
	-- neue Mitarbeiter-ID erstellen
    v_mitarbeiter_id := erstelle_neue_id(p_mandant, 'mitarbeiter_ID', 'mitarbeiter');
	
   	-- Daten in Tabelle Mitarbeiter eintragen 
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
		   p_mandant, 
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
   
END;
$$
LANGUAGE plpgsql;





CREATE OR REPLACE FUNCTION insert_tbl_mitarbeitertyp(
	p_mandant varchar(128),
	p_mitarbeitertyp varchar(32)
) RETURNS void AS
$$
declare 
	v_mitarbeitertyp_id integer;
begin
	
	-- neue Mitarbeiter-ID erstellen
    v_mitarbeitertyp_id := erstelle_neue_id(p_mandant, 'mitarbeitertyp_ID', 'mitarbeitertypen');
	
   	-- Daten in Tabelle Mitarbeitertyp eintragen 
    insert into mitarbeitertypen(Mitarbeitertyp_ID, Mandant, Mitarbeitertyp)
		values(v_mitarbeitertyp_id, p_mandant, p_mitarbeitertyp);
   
END;
$$
LANGUAGE plpgsql;





CREATE OR REPLACE FUNCTION insert_tbl_istmitarbeitertyp(
	p_mandant varchar(128),
	p_startdatum date,
	p_enddatum date
) RETURNS void AS
$$
declare 
	v_mitarbeiter_id integer;
	v_mitarbeitertyp_id integer;
begin
	
	-- IDs aus den Referenztabellen auslesen
	v_mitarbeiter_id := id_auslesen(p_mandant, 'mitarbeiter_ID', 'mitarbeiter');
    v_mitarbeitertyp_id := id_auslesen(p_mandant, 'mitarbeitertyp_ID', 'mitarbeitertypen');
	
   	-- Daten in Tabelle ist_Mitarbeitertyp eintragen 
    insert into ist_Mitarbeitertyp(Mitarbeiter_ID, Mitarbeitertyp_ID, Mandant, Datum_Von, Datum_Bis)
		values(v_mitarbeiter_id, v_mitarbeitertyp_id, p_mandant, p_startdatum, p_enddatum);
   
END;
$$
LANGUAGE plpgsql;





CREATE OR REPLACE FUNCTION id_auslesen(
	p_mandant varchar(128),
	p_id_spalte varchar(64),
	p_tabelle varchar(64)
) RETURNS integer as
$$
declare 
	v_id integer;
begin
	
	-- auf Mandantenrolle umstellen, um sicherzugehen, dass nur die ID des Mandanten berücksichtigt wird
	execute 'SET ROLE ' || p_mandant; 

    -- Neue ID erstellen
    EXECUTE 'SELECT MAX(' || p_id_spalte || ') FROM ' || p_tabelle INTO v_id;
	
   	set role postgres;
   	
    RETURN v_id;
	
END;
$$
LANGUAGE plpgsql;





CREATE OR REPLACE FUNCTION insert_neuer_mitarbeiter_alt(
	p_mandant varchar(128),
	p_vorname varchar(64), 
	p_nachname varchar(64), 
	p_geschlecht varchar(16), 
	p_geburtsdatum date, 
	p_eintrittsdatum date, 
	p_steuernummer varchar(32), 
	p_sozialversicherungsnummer varchar(32), 
	p_iban varchar(32), 
	p_telefonnummer varchar(16), 
	p_private_emailadresse varchar(64),
	p_mitarbeitertyp varchar(32)
) RETURNS void AS
$$
begin

	perform insert_tbl_mitarbeiter(p_mandant, p_vorname, p_nachname, p_geschlecht, p_geburtsdatum, p_eintrittsdatum, p_steuernummer, p_sozialversicherungsnummer, p_iban, p_telefonnummer, p_private_emailadresse);
	perform insert_tbl_mitarbeitertyp(p_mandant, p_mitarbeitertyp);
	perform insert_tbl_istmitarbeitertyp(p_mandant, p_eintrittsdatum, '9999-12-31');
	
END;
$$
LANGUAGE plpgsql;