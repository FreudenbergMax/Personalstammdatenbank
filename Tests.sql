-- Kontrolle
set search_path to public;
set search_path to temp_test_schema;

set session role tenant_user;
SET app.current_tenant=2;

set role postgres;
select mandant_anlegen('beispielfirma');
select mandant_anlegen('testu');
select nutzer_anlegen(1, 'M00001', 'Max', 'Mustermann');

select insert_krankenversicherungsbeitraege(1, false, 7.3, 7.3, 68000.00, 72000.45, '2023-12-15');
select insert_krankenversicherungsbeitraege(1, true, 7.3, 7.3, 68000.00, 72000.45, '2023-12-15');
select * from Krankenversicherungen;
select * from GKV_Beitraege;
select * from hat_GKV_Beitraege;
select * from hat_gesetzliche_Krankenversicherung;
select update_krankenversicherungsbeitraege(1, false, 7.8, 7.8, 80000, 82000.75,'2024-12-31', '2025-01-01');


select insert_Krankenkasse(1, 'Kaufmaennische Krankenkasse', 'KKH', 1.6, '2023-12-15');
select insert_Krankenkasse(1, 'Technische Krankenkasse', 'TK', 1.5, '2023-12-15');
select insert_Krankenkasse(1, 'BARMER', 'BAR', 1.5, '2023-12-15');
select * from krankenkassen;
select * from GKV_Zusatzbeitraege;
select * from hat_GKV_Zusatzbeitrag;
select * from ist_in_gkv;

select insert_anzahl_kinder_an_pv_beitrag(1, 0, 1.9, 68000.00, 72000.45, '2023-12-15');
select insert_anzahl_kinder_an_pv_beitrag(1, 1, 1.9, 68000.00, 72000.45, '2023-12-15');
select * from Anzahl_Kinder_unter_25;
select * from AN_Pflegeversicherungsbeitraege_gesetzlich;
select * from hat_gesetzlichen_AN_PV_Beitragssatz;
select * from hat_x_Kinder_unter_25;

select insert_Sachsen(1, true, 1.2, '2023-12-15');
select insert_Sachsen(1, false, 1.2, '2023-12-15');
select * from wohnhaft_Sachsen;
select * from AG_Pflegeversicherungsbeitraege_gesetzlich;
select * from hat_gesetzlichen_AG_PV_Beitragssatz;
select * from wohnt_in_Sachsen;

select insert_arbeitslosenversicherungsbeitraege(1, 3.2, 3.2, 57456.12, 60000, '2023-12-15');
select * from Arbeitslosenversicherungen;
select * from Arbeitslosenversicherungsbeitraege;
select * from hat_AV_Beitraege;
select * from hat_gesetzliche_Arbeitslosenversicherung;

select insert_rentenversicherungsbeitraege(1, 9.8, 9.8, 78564.12, 81245.65, '2023-12-15');
select * from Rentenversicherungen;
select * from Rentenversicherungsbeitraege;
select * from hat_RV_Beitraege;
select * from hat_gesetzliche_Rentenversicherung;

select insert_Tarif(1,'A5-1', 'Verdi', 3449.63, 2000, 2000, '9999-12-31');
select insert_Tarif(1,'A5-2', 'Verdi', 3863.12, 2200, 2200, '9999-12-31');
select * from Verguetungen;
select * from Tarife;
select * from Gewerkschaften;
select * from hat_Verguetung;
select * from hat_Tarif;
select * from Aussertarifliche;

select insert_Minijob(1, false, 13.0, 15, 3.6, 1.1, 0.24, 0.06, 2.0, '2023-12-15');
select * from minijobs;
select * from pauschalabgaben;
select * from hat_Pauschalabgaben;

SELECT 
				pauschalabgabe_id
			 FROM 
				pauschalabgaben
			 WHERE 
				ag_krankenversicherungsbeitrag_in_prozent,
				ag_rentenversicherungsbeitrag_in_prozent,
				an_rentenversicherungsbeitrag_in_prozent,
				u1_umlage_in_prozent,
				u2_umlage_in_prozent,
				insolvenzgeldumlage_in_prozent,
				pauschalsteuer_in_prozent;

select insert_mitarbeiterdaten(-- Tabelle Mitarbeiter
							   1,								-- Mandant_ID 
							   'M100002',						-- Personalnummer 
							   'Erika',							-- Vorname
							   '',								-- Zweitname
							   'Musterfrau',					-- Nachname
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
							   'A5-1',							-- Tarif
							   'Verdi',							-- Gewerkschaft	
							   3500.25,							-- Grundgehalt
							   0,								-- Weihnachtsgeld
							   0,								-- Urlaubsgeld
							   -- Bereich 'Kranken- und Pflegeversicherung'
							   false,							-- privat krankenversichert
							   200.25,							-- Zuschuss private Krankenversicherung
							   53.72,							-- Zuschuss private Pflegeversicherung
							   true,							-- gesetzlich versichert?
							   false,							-- ermaessigter KV_Beitragssatz?
							   'Kaufmaennische Krankenkasse',	-- Mitglied gesetzliche Krankenkasse (vollständiger Name)
							   'KKH',							-- Mitglied gesetzliche Krankenkasse (Abkürzung)
							   0,								-- Anzahl Kinder
							   true,							-- wohnhaft Sachsen?
							   -- Bereich 'Arbeitslosenversicherung'
							   true,							-- Arbeitslosenversichert?
							   -- Bereich 'Rentenversicherung'
							   true								-- Rentenversichert?
							   );
					  
select update_adresse(1, 'M100002', '2025-12-31', '2026-01-01', 'Hofzeichendamm', '5', '13125', 'Berlin', 'Berlin', 'Deutschland');

select insert_tbl_mitarbeiter(1,
							   'M100001',
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

select update_mitarbeiterentlassung(1, 'M100002', '2026-12-31', 'Umsatzrueckgang', 'betrieblich');



select delete_mitarbeiterdaten(1, 'M100002');

select delete_mandantendaten(1);

select * from mandanten;
select * from nutzer;
select * from mitarbeiter;

UPDATE mitarbeiter SET vorname = 'Maria' where mitarbeiter_id = 1;

set role postgres;
set session role tenant_user;
SET app.current_tenant=1;
UPDATE mitarbeiter SET mandant_id = 2 where mitarbeiter_id = 1;

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
