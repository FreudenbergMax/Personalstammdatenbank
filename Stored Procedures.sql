-- START DER SEQUENZ ---------------------------------------------------------------------------------------------------------------------------------
drop table if exists Mitarbeiter;

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

-- Erstellen Sie zuerst die Funktion, die das Filterprädikat definiert
CREATE OR REPLACE FUNCTION fn_RowLevelSecurity(Mandant text)
RETURNS boolean AS $$
BEGIN
  RETURN Mandant = current_user;
END;
$$ LANGUAGE plpgsql;

CREATE POLICY FilterMandant
    ON mitarbeiter
    FOR ALL
    USING (fn_RowLevelSecurity(Mandant));

-- Aktivieren Sie die Zeilenebene-Sicherheit für die Tabelle
ALTER TABLE Mitarbeiter ENABLE ROW LEVEL SECURITY;

-- User und Gruppe löschen, falls existent
drop user if exists testfirma;
drop user if exists testfirma2;
drop group if exists mandantengruppe;

-- Mandantengruppe erstellen und mit Privilegien ausstatten
create group mandantengruppe;
grant select, insert, update, delete on mitarbeiter to mandantengruppe;
--revoke select, insert, update, delete on mitarbeiter from mandantengruppe;

-- User "testfirma" und 'testfirma2' erstellen und der Mandantengruppe zuweisen
create user testfirma;
alter group mandantengruppe add user testfirma;

create user testfirma2;
alter group mandantengruppe add user testfirma2;

set role postgres;
select * from Mitarbeiter;

CREATE OR REPLACE FUNCTION erstelle_user(
	p_user varchar(100)
) RETURNS void AS
$$
BEGIN
    -- Überprüfen, ob der Benutzer bereits existiert
    IF NOT EXISTS (SELECT 1 FROM pg_user WHERE usename = p_user) THEN
        -- Benutzer erstellen, falls er nicht existiert
        EXECUTE 'CREATE USER ' || p_user;
        execute 'alter group mandantengruppe add user ' || p_user;
        RAISE NOTICE 'Benutzer % wurde erfolgreich erstellt.', p_user;
    ELSE
        RAISE NOTICE 'Benutzer % existiert bereits.', p_user;
    END IF;
END;
$$
LANGUAGE plpgsql;

-- Stored Procedures aufrufen
SELECT erstelle_user('testfirma');

CREATE OR REPLACE FUNCTION insert_neuer_mitarbeiter(
	--p_mitarbeiter_id integer,
	p_user varchar(100),
	p_vorname varchar(100), 
	p_nachname varchar(100), 
	p_geschlecht varchar(10), 
	p_geburtsdatum date, 
	p_eintrittsdatum date, 
	p_steuernummer varchar(50), 
	p_sozialversicherungsnummer varchar(50), 
	p_iban varchar(50), 
	p_telefonnummer varchar(50), 
	p_private_emailadresse varchar(100)
) RETURNS void AS
$$
declare 
	v_mitarbeiter_id integer;
begin
	
	EXECUTE 'SET ROLE ' || p_user;

	-- Mitarbeiter-ID erstellen
    v_mitarbeiter_id := erstelle_neue_id(p_user);
	
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
END;
$$
LANGUAGE plpgsql;

select insert_neuer_mitarbeiter('testfirma', 'Max', 'Freudenberg', 'maennlich', '12.12.1992', '01.11.2023', '11 111 111 111', '00 121292 F 00', 'DE00 0000 0000 0000 0000 00', '0175 2572025', 'maxfreudenberg@web.de');
select insert_neuer_mitarbeiter('testfirma2', 'Erika', 'Musterfrau', 'weiblich', '01.01.1995', '01.11.2023', '99 999 999 999', '00 010195 F 00', 'DE99 9999 9999 9999 9999 99', '0175 1234567', 'erikamusterfrau@web.de');

CREATE OR REPLACE FUNCTION erstelle_neue_id(
	p_user varchar(100)
) RETURNS integer as
$$
declare 
	v_neue_id integer;
begin
	
	-- Rolle setzen
    SET ROLE postgres;

    -- Neue ID erstellen
    SELECT MAX(mitarbeiter_ID) + 1 INTO v_neue_id FROM mitarbeiter;
   
    IF v_neue_id IS NULL THEN
    	v_neue_id := 1;
	END IF;
   
   	EXECUTE 'SET ROLE ' || p_user; 

    RETURN v_neue_id;
	
END;
$$
LANGUAGE plpgsql;

SELECT erstelle_neue_id('testfirma2');

/*
CREATE OR REPLACE FUNCTION SQLabfrage(
    p_user varchar(100),
    abfrage test
) RETURNS void AS
$$
BEGIN
    -- SET ROLE ausführen
    EXECUTE 'SET ROLE ' || p_user;

    -- Die vorbereitete SQL-Abfrage ausführen
    EXECUTE abfrage;
END;
$$
LANGUAGE plpgsql;

select sqlabfrage('testfirma', 'select * from Mitarbeiter');
*/

-- gibt alle existierende Users aus
SELECT * FROM pg_catalog.pg_user;
