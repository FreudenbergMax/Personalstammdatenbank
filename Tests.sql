-- Kontrolle
set search_path to public;
set search_path to temp_test_schema;

set session role tenant_user;
SET app.current_tenant=1;

set role postgres;
select mandant_anlegen('testu');
select nutzer_anlegen(1, 'M00001', 'Max', 'Mustermann');

select insert_Krankenkasse(1, 'Kaufmaennische Krankenkasse', 'KKH', 1.5, '2023-12-15');
select insert_Krankenkasse(1, 'Technische Krankenkasse', 'TK', 1.5, '2023-12-15');
select * from krankenkassen;
select * from ist_in_gkv;
select * from GKV_Zusatzbeitraege;
select * from hat_GKV_Zusatzbeitrag;

select insert_krankenversicherungsbeitraege(1, 7.3, 7.3, 68000.00, 72000.45, '2023-12-15');
select * from Krankenversicherungen;
select * from GKV_Beitraege;
select * from hat_GKV_Beitraege;
select * from hat_gesetzliche_Krankenversicherung;

select * from insert_arbeitslosenversicherungsbeitraege (1, 3.0, 3.0, 57456.12, 60000, '2023-12-15');
select * from Arbeitslosenversicherungen;
select * from Arbeitslosenversicherungsbeitraege;
select * from hat_gesetzliche_Arbeitslosenversicherung;
select * from hat_AV_Beitraege;

select insert_mitarbeiterdaten(-- Tabelle Mitarbeiter
							   1,								-- Mandant_ID
							   'M100001',						-- Personalnummer	
							   'Max',							-- Vorname
							   '',								-- Zweitname
							   'Mustermann',					-- Nachname
							   '1992-12-12',					-- Geburtsdatum
							   '2024-01-01',					-- Eintrittsdatum
							   '11 111 111 111',				-- Steuernummer
							   '00 121292 F 00',				-- Sozialversicherungsnummer
							   'DE00 0000 0000 0000 0000 00',	-- IBAN
							   '0175 1234567',					-- private Telefonnummer
							   'maxmustermann@web.de',			-- private E-Mail
							   '030 987654321',					-- dienstliche Telefonnummer
							   'Mustermann@testfirma.de',		-- dienstliche E-Mail
							   null,							-- Austrittsdatum
							   -- Bereich 'Adresse'
							   'Musterstrasse',					-- Strasse
							   '1',								-- Hausnummer
							   '12358',							-- Postleitzahl
							   'Bernau',						-- Stadt
							   'Brandenburg',					-- Region
							   'Deutschland',					-- Land
							   -- Bereich 'Geschlecht'			
							   'maennlich',						-- Geschlecht
							   -- Bereich 'Mitarbeitertyp'
							   'Angestellter',					-- Mitarbeitertyp
							   -- Bereich 'Steuerklasse'		
							   '1',								-- Steuerklasse
							   -- Bereich 'Wochenarbeitszeit'	
							   40,							-- Wochenarbeitszeit
							   -- Bereich 'Abteilung'
							   'Personalcontrolling',			-- Abteilung
							   'PC',							-- Abteilungskuerzel
							   false,							-- Fuehrungskraft
							   -- Bereich 'Jobtitel'
							   'Personalcontroller',			-- Jobtitel
							   'Junior',						-- Erfahrungsstufe
							   -- Bereich 'Gesellschaft'
							   'Bundesdruckerei GmbH',			-- Gesellschaft
							   'BDr',							-- Abkuerzung Gesellschaft
							   -- Bereich 'Entgelt'	
							   true,							-- tarifbeschaeftigt?		
							   'Verdi',							-- Gewerkschaft				
							   'A5-1',							-- Tarif
							   3500.25,							-- Grundgehalt
							   null,							-- Weihnachtsgeld
							   null,							-- Urlaubsgeld
							   -- Bereich 'Kranken- und Pflegeversicherung'
							   false,							-- privat krankenversichert
							   200.25,							-- Zuschuss private Krankenversicherung
							   20.02,							-- Zuschuss privater Zusatzbeitrag
							   53.72,							-- Zuschuss private Pflegeversicherung
							   true,							-- gesetzlich versichert?
							   'Kaufmaennische Krankenkasse',	-- Mitglied gesetzliche Krankenkasse (vollständiger Name)
							   'KKH',							-- Mitglied gesetzliche Krankenkasse (Abkürzung)
							   0,								-- Anzahl Kinder
							   2.3,								-- AN-Pflegeversicherungsbeitrag in Prozent
							   65000,							-- Beitragsbemessungsgrenze Pflegeversicherung Ost
							   68000,							-- Beitragsbemessungsgrenze Pflegeversicherung West
							   true,							-- wohnhaft Sachsen?
							   1.2,								-- AG-Pflegeversicherungsbeitrag in Prozent
							   -- Bereich 'Arbeitslosenversicherung'
							   true,							-- Arbeitslosenversichert?
							   -- Bereich 'Rentenversicherung'
							   true,							-- Rentenversichert?
							   9.8,								-- AG-Rentenbeitrag in Prozent
							   9.8,								-- AN-Rentenbeitrag in Prozent
							   85000.25,						-- Beitragsbemessungsgrenze Rente Ost
							   88000							-- Beitragsbemessungsgrenze Rente West
							   );
					  
select update_adresse(1, 'M100001', '2026-01-01', '2025-12-31', 'Hofzeichendamm', '5', '13125', 'Berlin', 'Berlin', 'Deutschland');

select insert_tbl_mitarbeiter(1,
							   'M100002',
							   'Erika',
							   '',
							   'Musterfrau',
							   '1992-12-12',
							   '2024-01-01',
							   '11 111 111 111',
							   '00 121292 F 00',
							   'DE00 0000 0000 0000 0000 00',
							   '0175 1234567',
							   'maxmustermann@web.de',
							   '030 987654321',
							   'Mustermann@testfirma.de',
							   null);

select update_adresse(1,
						'M100002',
						'2024-01-01',
						'2023-12-31',
						'neue Straße',
						'42',
						'10369',
						'Berlin',
						'Berlin',
						'Deutschland'
);

select update_mitarbeiterentlassung(1, 'M100002', '2024-12-31', 'Umsatzrueckgang', 'betrieblich');



select delete_mitarbeiterdaten(1, 'M100002');

select delete_mandantendaten(1);

select * from mandanten;
select * from nutzer;
select * from mitarbeiter;

-- Bereich 'Austritt'
select * from austrittsgruende;
select * from kategorien_austrittsgruende; 

-- Bereich 'Adresse'
select * from laender;
select * from regionen;
select * from staedte;
select * from postleitzahlen;
select * from strassenbezeichnungen;
select * from wohnt_in;

-- Bereich 'Geschlecht'
select * from geschlechter;
select * from hat_geschlecht;

-- Bereich 'Mitarbeitertyp'
select * from mitarbeitertypen;
select * from ist_mitarbeitertyp;

-- Bereich 'Steuerklasse'
select * from steuerklassen;
select * from in_steuerklasse;

-- Bereich 'Wochenarbeitszeit'
select * from wochenarbeitsstunden;
select * from arbeitet_x_wochenstunden;

-- Bereich 'Abteilung'
select * from Abteilungen;
select * from eingesetzt_in;

-- Bereich 'Jobtitel'
select * from jobtitel;
select * from erfahrungsstufen;
select * from hat_Jobtitel;

-- Bereich 'Gesellschaft'
select * from Gesellschaften;
select * from in_Gesellschaft;

-- Bereich 'Entgelt'
select * from gewerkschaften;
select * from tarife;
select * from hat_tarif;
select * from verguetungen;
select * from hat_Verguetung;
select * from Aussertarifliche;

-- Bereich 'Kranken- und Pflegeversicherung'
select * from privat_krankenversicherte;


select * from anzahl_kinder_unter_25;
select * from hat_x_kinder_unter25;
select * from an_pflegeversicherungsbeitraege_gesetzlich;
select * from hat_gesetzlichen_AN_PV_Beitragssatz;
select * from wohnhaft_sachsen;
select * from wohnt_in_sachsen;
select * from ag_pflegeversicherungsbeitraege_gesetzlich apg ;
select * from hat_gesetzlichen_ag_pv_beitragssatz; 

-- Bereich 'Rentenversicherung'
select * from hat_RVBeitraege;
select * from Rentenversicherungsbeitraege_gesetzlich;

select 
	vorname,
	nachname
from
	mitarbeiter
	inner join in_gesellschaft on mitarbeiter.mitarbeiter_id = in_Gesellschaft.mitarbeiter_id
	inner join gesellschaften on gesellschaften.gesellschaft_id = in_Gesellschaft.gesellschaft_id
	inner join hat_geschlecht on mitarbeiter.mitarbeiter_id = hat_geschlecht.mitarbeiter_id
	inner join geschlechter on geschlechter.geschlecht_id = hat_geschlecht.geschlecht_id
where 
	geschlecht = 'weiblich'
	and gesellschaft = 'Bundesdruckerei GmbH';


select 
	in_gesellschaft.mitarbeiter_id
from
	mitarbeiter
	inner join in_gesellschaft on mitarbeiter.mitarbeiter_id = in_Gesellschaft.mitarbeiter_id
	inner join gesellschaften on gesellschaften.gesellschaft_id = in_Gesellschaft.gesellschaft_id
	inner join hat_geschlecht on mitarbeiter.mitarbeiter_id = hat_geschlecht.mitarbeiter_id
	inner join geschlechter on geschlechter.geschlecht_id = hat_geschlecht.geschlecht_id
where 
	in_gesellschaft.datum_von <= '2024-01-16'
	and in_gesellschaft.datum_bis > '2024-01-17'
	--and gesellschaft = 'Bundesdruckerei GmbH'
	and geschlecht = 'weiblich';

select 
	vorname,
	nachname,
	eintrittsdatum,
	austrittsdatum
from
	mitarbeiter
where 
	eintrittsdatum <= '2024-01-15'
	and austrittsdatum > '2024-01-15';