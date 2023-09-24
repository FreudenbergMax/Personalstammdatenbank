CREATE OR REPLACE FUNCTION insert_neuer_mitarbeiter(
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
BEGIN
	insert into mitarbeiter(vorname, nachname, geschlecht, geburtsdatum, eintrittsdatum, steuernummer, sozialversicherungsnummer, iban, telefonnummer, private_emailadresse) 
	values(p_vorname, p_nachname, p_geschlecht, p_geburtsdatum, p_eintrittsdatum, p_steuernummer, p_sozialversicherungsnummer, p_iban, p_telefonnummer, p_private_emailadresse);
END;
$$
LANGUAGE plpgsql;