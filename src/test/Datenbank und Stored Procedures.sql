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
-- Rolle für die User erstellen, welcher RLS unterliegt
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
drop table if exists Mandanten;
drop table if exists mitarbeiter;
drop function if exists erstelle_neue_id(varchar(64), varchar(64));
drop function if exists mandant_anlegen(integer, varchar(128));
drop function if exists nutzer_anlegen(integer, varchar(64), varchar(64), integer);
drop function if exists nutzer_entfernen(integer, varchar(64), varchar(64), integer);
drop function if exists select_ausfuehren(varchar(64), integer);
drop function if exists insert_mitarbeiter(integer, integer);

create table mandanten(
	mandant_id integer primary key,
	firma varchar(128)
);

alter table mandanten enable row level security;

-- Erstellung der RLS-Policy mit anschließender Aktivieriung der RLS-Fähigkeit der Tabelle "Mitarbeiter"
create policy filter_mandanten
    on mandanten
    using (mandant_id = current_setting('app.current_tenant')::int);

create table nutzer(
	user_id integer primary key,
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
    Mitarbeiter_ID integer primary key,
    Mandant_ID integer not null,
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

alter table Mitarbeiter enable row level security;

-- Erstellung der RLS-Policy mit anschließender Aktivieriung der RLS-Fähigkeit der Tabelle "Mitarbeiter"
create policy FilterMandant_Mitarbeiter
    on mitarbeiter
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
	p_user_id integer,
	p_vorname varchar(64),
	p_nachname varchar(64),
	p_mandant_id integer
) returns void as
$$
begin

    insert into Nutzer(User_ID, vorname, Nachname, Mandant_ID)
		values(p_user_id, p_vorname, p_nachname, p_mandant_id);

end;
$$
language plpgsql;



create or replace function nutzer_entfernen(
	p_user_id integer,
	p_vorname varchar(64),
	p_nachname varchar(64),
	p_mandant_id integer
) returns void as
$$
begin
	
	set session role tenant_user;
	execute 'SET app.current_tenant=' || p_mandant_id;
	
    delete from nutzer 
    where user_id = p_user_id 
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



create or replace function insert_mitarbeiter(
	p_mitarbeiter_id integer,
	p_mandant_id integer
) returns text as
$$
begin
	
	set session role tenant_user;
	execute 'SET app.current_tenant=' || p_mandant_id;
    
	-- Code, der die Mitarbeiterdaten in die Datenbank schreibt

end;
$$
language plpgsql;