-- Kontrolle
set session role tenant_user;

set app.current_tenant=1;
select * from mandanten;
select * from nutzer;

set app.current_tenant=2;
select * from mandanten;
select * from nutzer;

set role postgres;
select * from mandanten;
select * from nutzer;
select * from mitarbeiter;

select insert_mitarbeiterdaten(1, 'Max', '', 'Mustermann', '1992-12-12', '2024-01-01', '11 111 111 111', '00 121292 F 00', 'DE00 0000 0000 0000 0000 00', '0175 1234567', 'maxmustermann@web.de', '030 987654321', 'Mustermann@testfirma.de', '2025-12-31', 'Musterstraße', '1', '12358', 'Berlin', 'Berlin', 'Deutschland');
select insert_mitarbeiterdaten(1, 'Max', '', 'Mustermann', '1992-12-12', '2024-01-01', '11 111 111 111', '00 121292 F 00', 'DE00 0000 0000 0000 0000 00', '0175 1234567', 'maxmustermann@web.de', '030 987654321', 'Mustermann@testfirma.de', '2025-12-31', 'Musterstraße', '1', '12358', 'Berlin', 'Berlin', 'Deutschland');
select insert_mitarbeiterdaten(1, 'Max', '', 'Mustermann', '1992-12-12', '2024-01-01', '11 111 111 111', '00 121292 F 00', 'DE00 0000 0000 0000 0000 00', '0175 1234567', 'maxmustermann@web.de', '030 987654321', 'Mustermann@testfirma.de', '2025-12-31', 'Musterstraße', '1', '12358', 'Berlin', 'Berlin', 'Deutschland');

select insert_mitarbeiterdaten(2, 'Max', '', 'Mustermann', '1992-12-12', '2024-01-01', '11 111 111 111', '00 121292 F 00', 'DE00 0000 0000 0000 0000 00', '0175 1234567', 'maxmustermann@web.de', '030 987654321', 'Mustermann@testfirma.de', '2025-12-31', 'Musterstraße', '1', '12358', 'Berlin', 'Berlin', 'Deutschland');

select bekomme_aktuelle_Mitarbeiter_ID();

set session role tenant_user;
set app.current_tenant=2;
select erstelle_neue_id('mitarbeiter_ID', 'mitarbeiter');