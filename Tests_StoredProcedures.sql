insert into mitarbeiter(vorname, nachname, geschlecht, geburtsdatum, eintrittsdatum, wochenarbeitszeit, steuernummer, sozialversicherungsnummer, iban, telefonnummer, private_emailadresse) 
	values('Max', 'Freudenberg', 'maennlich', '12.12.1992', '01.11.2023', 35, '11 111 111 111', '00 121292 F 00', 'DE00 0000 0000 0000 0000 00', '0175 2572025', 'maxfreudenberg@web.de');

select 
	*
from 
	mitarbeiter;
	
delete from 
	mitarbeiter 
where 
	nachname = 'Freudenberg';
	
SELECT proname, proargnames, proargtypes FROM pg_proc WHERE proname = 'insert_neuer_mitarbeiter';