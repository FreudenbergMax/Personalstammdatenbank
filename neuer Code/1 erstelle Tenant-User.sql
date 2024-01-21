set role postgres;

-- Erstellung der Rolle 'tenant-user' mit diversen Zugriffsrechten
-- Rolle für die user erstellen, welcher RLS unterliegt
create role tenant_user;
-- Rolle 'tenant-user' darf im Schema 'public' operieren
grant usage on schema public to tenant_user;
-- 'tenant-user' kann SELECT-, INSERT-, UPDATE- und DELETE-Befehle auf alle (auch zukuenftig) erstellten Tabellen im Schema 'public' ausführen 
alter default privileges in schema public grant select, insert, update, delete on tables to tenant_user;
-- 'tenant-user' kann (auch zukünftig) erstellte Sequenzen (bspw. Serial) benutzen 
alter default privileges in schema public grant usage on sequences to tenant_user;