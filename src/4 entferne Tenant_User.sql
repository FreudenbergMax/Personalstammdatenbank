-- Quelle: https://adityamattos.com/multi-tenancy-in-python-fastapi-and-sqlalchemy-using-postgres-row-level-security
-- Abschaffung der Rolle 'tenant-user' und dessen Privilegien
-- 'tenant-user' kann (auch zukünftig) erstellte Sequenzen (bspw. Serial) NICHT mehr benutzen 
alter default privileges in schema public revoke usage on sequences from tenant_user;
-- 'tenant-user' kann SELECT-, INSERT-, UPDATE- und DELETE-Befehle auf alle (auch zukünftig) erstellte Tabellen im Schema 'public' NICHT mehr ausführen
alter default privileges in schema public revoke select, insert, update, delete on tables from tenant_user;
-- 'tenant_user' darf nicht mehr im Schema 'public' operieren 
revoke usage on schema public from tenant_user;
-- Rolle 'tenant_user' entfernen
drop role tenant_user;