-- inspiriert von diesem Tutorial: https://www.youtube.com/watch?v=eD0z7zysu4I

drop table if exists customers;

create table customers (
	FullName varchar(50) not null,
	EmailAdress varchar(50) not null,
	SecurityUserName varchar(20) not null
);

-- User löschen, sofern vorhanden
drop user if exists Frank;
--drop user if exists Chris;
--drop user if exists Denials;

-- neuen User erstellen
create user Frank;
--create user Chris;
--create user Denials;

insert into customers values
	('Company1', 'Manger@ABC.COM', 'frank'),
	('Company2', 'info@AInfaSerice.COM', 'chris'),
	('Company3', 'HeadWasher@washrus.COM', 'denials'),
	('Company4', 'marketing@bluewater.COM', 'denials'),
	('Company5', 'steve@starbright.COM', 'frank');


-- User das Recht zugestehen, Daten auf Tabelle customers auszulesen (mit SELECT)
grant select on customers to Frank;
--grant select on customers to Chris;
--grant select on customers to Denials;

-- Erstellen Sie zuerst die Funktion, die das Filterprädikat definiert
CREATE OR REPLACE FUNCTION fn_RowLevelSecurity(SecurityUserName text)
RETURNS boolean AS $$
BEGIN
  RETURN SecurityUserName = current_user;
END;
$$ LANGUAGE plpgsql;

CREATE POLICY FilterCustomer
    ON customers
    FOR ALL
    USING (fn_RowLevelSecurity(SecurityUserName));

-- Aktivieren Sie die Zeilenebene-Sicherheit für die Tabelle
ALTER TABLE customers ENABLE ROW LEVEL SECURITY;

set role postgres;
set role Frank;
--set role Chris;
--set role Denials;
--set role postgres;
--select current_user;

select * from customers;





-- Ausgabe aller existierenden User
--select * from pg_catalog.pg_user;