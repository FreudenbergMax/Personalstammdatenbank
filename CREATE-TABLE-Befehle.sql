-- Mandantentabelle erstellen
create table Mandanten (
	Mandant_ID serial primary key,
	Firma varchar (128) not null,
	Adresse varchar(256) not null,
	Passwort varchar(256) not null
);

-- Tabellen, die den Bereich "Austrittsgruende" behandeln, erstellen
create table Kategorien_Austrittsgruende (
	Kategorie_Austrittsgruende_ID serial primary key,
	Mandant_ID integer not null,
	Bezeichnung varchar(16) not null,
	constraint fk_austrittsgrundkategorien_mandanten
		foreign key (Mandant_ID) 
			references Mandanten(Mandant_ID)
);

create table Austrittsgruende (
	Austrittsgrund_ID serial primary key,
	Mandant_ID integer not null,
	Bezeichnung varchar(64) not null,
	Kategorie_Austrittsgruende_ID integer not null,
	constraint fk_Austrittsgruende_mandanten
		foreign key (Mandant_ID) 
			references Mandanten(Mandant_ID),
	constraint fk_austrittsgruende_austrittsgrundkategorien 
		foreign key (Kategorie_Austrittsgruende_ID) 
			references Kategorien_Austrittsgruende(Kategorie_Austrittsgruende_ID)
);

-- Zentrale Tabelle "Mitarbeiter"
create table Mitarbeiter (
    Mitarbeiter_ID serial primary key,
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
    Austrittsdatum date,
    Austrittsgrund_ID integer,
    constraint fk_mitarbeiter_mandanten
		foreign key (Mandant_ID) 
			references Mandanten(Mandant_ID),
    constraint fk_mitarbeiter_austrittsgruende 
    	foreign key (Austrittsgrund_ID) 
    		references Austrittsgruende(Austrittsgrund_ID)
);

-- Tabellen, die den Bereich "Wochenarbeitsstunden" behandeln, erstellen
create table Wochenarbeitsstunden(
	Wochenarbeitsstunden_ID serial primary key,
	Mandant_ID integer not null,
	in_Stunden decimal(4, 2) not null,
    constraint fk_wochenarbeitsstunden_mandanten
		foreign key (Mandant_ID) 
			references Mandanten(Mandant_ID)
);

create table arbeitet_x_Wochenstunden (
    Mitarbeiter_ID integer not null,
    Wochenarbeitsstunden_ID integer not null,
    Mandant_ID integer not null,
    Datum_Von date not null,
    Datum_Bis date not null,
    primary key (Mitarbeiter_ID, Datum_Bis),
    constraint fk_arbeitetxwochenstunden_mitarbeiter
    	foreign key (Mitarbeiter_ID) 
    		references Mitarbeiter(Mitarbeiter_ID),
    constraint fk_arbeitetxwochenstunden_wochenarbeitsstunden
    	foreign key (Wochenarbeitsstunden_ID) 
    		references Wochenarbeitsstunden(Wochenarbeitsstunden_ID),
    constraint fk_arbeitetxwochenstunden_mandanten
		foreign key (Mandant_ID) 
			references Mandanten(Mandant_ID)
);

-- Tabellen, die den Bereich "Steuerklasse" behandeln, erstellen
create table Steuerklassen (
    Steuerklasse_ID serial primary key,
    Mandant_ID integer not null,
    Beschreibung varchar(256) not null,
    constraint fk_steuerklassen_mandanten
		foreign key (Mandant_ID) 
			references Mandanten(Mandant_ID)
);

-- Assoziationstabelle zwischen Mitarbeiter und Steuerklasse
create table in_Steuerklasse (
    Mitarbeiter_ID integer not null,
    Steuerklasse_ID integer not null,
    Mandant_ID integer not null,
    Datum_Von date not null,
    Datum_Bis date not null,
    primary key (Mitarbeiter_ID, Datum_Bis),
    constraint fk_insteuerklasse_mitarbeiter
    	foreign key (Mitarbeiter_ID) 
    		references Mitarbeiter(Mitarbeiter_ID),
    constraint fk_insteuerklasse_steuerklassen
    	foreign key (Steuerklasse_ID) 
    		references Steuerklassen(Steuerklasse_ID),
    constraint fk_insteuerklasse_mandanten
		foreign key (Mandant_ID) 
			references Mandanten(Mandant_ID)
);

-- Tabellen, die den Bereich "Jobtitel" behandeln, erstellen
create table Erfahrungsstufen (
	Erfahrungsstufe_ID serial primary key,
	Mandant_ID integer not null,
	Bezeichnung varchar(32) not null,
    constraint fk_erfahrungsstufen_mandanten
		foreign key (Mandant_ID) 
			references Mandanten(Mandant_ID)
);

create table Jobtitel (
	Jobtitel_ID serial primary key,
	Mandant_ID integer not null,
	Bezeichnung varchar(64) not null,
    constraint fk_jobtitel_mandanten
		foreign key (Mandant_ID) 
			references Mandanten(Mandant_ID)
);

-- Assoziationstabelle zwischen Mitarbeiter und Jobtitel + Erfahrungsstufen
create table hat_Jobtitel (
	Mitarbeiter_ID integer not null,
	Jobtitel_ID integer not null,
	Erfahrungsstufe_ID integer not null,
	Mandant_ID integer not null,
	Datum_Von date not null,
    Datum_Bis date not null,
    primary key (Mitarbeiter_ID, Datum_Bis),
    constraint fk_hatjobtitel_mitarbeiter
    	foreign key (Mitarbeiter_ID) 
    		references Mitarbeiter(Mitarbeiter_ID),
    constraint fk_hatjobtitel_jobtitel
    	foreign key (Jobtitel_ID) 
    		references Jobtitel(Jobtitel_ID),
    constraint fk_hatjobtitel_erfahrungsstufen
		foreign key (Erfahrungsstufe_ID)
			references Erfahrungsstufen(Erfahrungsstufe_ID),
	constraint fk_hatjobtitel_mandanten
		foreign key (Mandant_ID) 
			references Mandanten(Mandant_ID)
);

-- Tabellen, die den Bereich "Adresse" behandeln, erstellen
create table Laender (
	Land_ID serial primary key,
	Mandant_ID integer not null,
	Landesname varchar(128) not null,
    constraint fk_laender_mandanten
		foreign key (Mandant_ID) 
			references Mandanten(Mandant_ID)
);

create table Regionen (
	Region_ID serial primary key,
	Mandant_ID integer not null,
	Regionname varchar(128) not null,
	Land_ID integer not null,
    constraint fk_regionen_mandanten
		foreign key (Mandant_ID) 
			references Mandanten(Mandant_ID),
	constraint fk_regionen_laender
		foreign key (Land_ID)
			references Laender(Land_ID)
);

create table Staedte (
	Stadt_ID serial primary key,
	Mandant_ID integer not null,
	stadtname varchar(128) not null,
	Region_ID integer not null,
	constraint fk_staedte_mandanten
		foreign key (Mandant_ID) 
			references Mandanten(Mandant_ID),
	constraint fk_staedte_regionen
		foreign key (Region_ID)
			references Regionen(Region_ID)
);

create table Postleitzahlen (
	Postleitzahl_ID serial primary key,
	Mandant_ID integer not null,
	Postleitzahl varchar(16) not null,
	Stadt_ID integer not null,
	constraint fk_postleitzahlen_mandanten
		foreign key (Mandant_ID) 
			references Mandanten(Mandant_ID),
	constraint fk_postleitzahlen_staedte
		foreign key (Stadt_ID)
			references Staedte(Stadt_ID)
);

create table Erstwohnsitze (
	Erstwohnsitz_ID serial primary key,
	Mandant_ID integer not null,
	Strasse varchar(64) not null,
	Hausnummer varchar(8) not null,
	Postleitzahl_ID integer not null,
	constraint fk_erstwohnsitze_mandanten
		foreign key (Mandant_ID) 
			references Mandanten(Mandant_ID),
	constraint fk_erstwohnsitze_postleitzahlen
		foreign key (Postleitzahl_ID)
			references Postleitzahlen(Postleitzahl_ID)
);

-- Assoziationstabelle zwischen Mitarbeiter und Adressenbereich
create table wohnt_in (
	Mitarbeiter_ID integer not null,
	Erstwohnsitz_ID integer not null,
	Mandant_ID integer not null,
	Datum_Von date not null,
    Datum_Bis date not null,
    primary key (Mitarbeiter_ID, Datum_Bis),
    constraint fk_wohntin_mitarbeiter
    	foreign key (Mitarbeiter_ID) 
    		references Mitarbeiter(Mitarbeiter_ID),
    constraint fk_wohntin_erstwohnsitze
    	foreign key (Erstwohnsitz_ID) 
    		references Erstwohnsitze(Erstwohnsitz_ID),
	constraint fk_wohntin_mandanten
		foreign key (Mandant_ID) 
			references Mandanten(Mandant_ID)
);

-- Tabellen, die den Bereich "Abteilung" behandeln, erstellen
create table Abteilungen (
	Abteilung_ID serial primary key,
	Mandant_ID integer not null,
	Bezeichnung varchar(128) not null,
	Abkuerzung varchar(32) not null,
	untersteht_Abteilung integer,
	constraint fk_abteilungen_mandanten
		foreign key (Mandant_ID) 
			references Mandanten(Mandant_ID),
	constraint fk_abteilungen_abteilungen
		foreign key (untersteht_Abteilung)
			references Abteilungen(Abteilung_ID)
);

-- Assoziationstabelle zwischen Mitarbeiter und Geschäftsbereich
create table eingesetzt_in (
	Mitarbeiter_ID integer not null,
	Abteilung_ID integer not null,
	Mandant_ID integer not null,
	Datum_Von date not null,
    Datum_Bis date not null,
    fuehrungskraft boolean not null,
    primary key (Mitarbeiter_ID, Abteilung_ID, Datum_Bis),
    constraint fk_eingesetztin_mitarbeiter
    	foreign key (Mitarbeiter_ID) 
    		references Mitarbeiter(Mitarbeiter_ID),
    constraint fk_eingesetztin_abteilungen
    	foreign key (Abteilung_ID) 
    		references Abteilungen(Abteilung_ID),
	constraint fk_eingesetztin_mandanten
		foreign key (Mandant_ID) 
			references Mandanten(Mandant_ID)
);

-- Tabellen, die den Bereich "Mitarbeitertyp" (Angestellter, Arbeiter, Praktikant, Werkstudent etc.) behandeln, erstellen
create table Mitarbeitertypen (
	Mitarbeitertyp_ID serial primary key,
	Mandant_ID integer not null,
	Bezeichnung varchar(32),
	constraint fk_mitarbeitertypen_mandanten
		foreign key (Mandant_ID) 
			references Mandanten(Mandant_ID)
);

-- Assoziationstabelle zwischen Mitarbeiter und Mitarbeitertyp
create table ist_Mitarbeitertyp (
	Mitarbeiter_ID integer not null,
	Mitarbeitertyp_ID integer not null,
	Mandant_ID integer not null,
	Datum_Von date not null,
    Datum_Bis date not null,
    primary key (Mitarbeiter_ID, Datum_Bis),
    constraint fk_istmitarbeitertyp_mitarbeiter
    	foreign key (Mitarbeiter_ID) 
    		references Mitarbeiter(Mitarbeiter_ID),
    constraint fk_istmitarbeitertyp_mitarbeitertypen
    	foreign key (Mitarbeitertyp_ID) 
    		references Mitarbeitertypen(Mitarbeitertyp_ID),
	constraint fk_istmitarbeitertyp_mandanten
		foreign key (Mandant_ID) 
			references Mandanten(Mandant_ID)
);

-- Tabellen, die den Bereich "Gesellschaft" behandeln, erstellen
create table Gesellschaften (
	Gesellschaft_ID serial primary key,
	Mandant_ID integer not null,
	Bezeichnung varchar(128) not null,
	Abkuerzung varchar (32) not null,
	untersteht_Gesellschaft integer not null,
	constraint fk_gesellschaften_mandanten
		foreign key (Mandant_ID) 
			references Mandanten(Mandant_ID),
	constraint fk_gesellschaften_gesellschaften
		foreign key (untersteht_Gesellschaft)
			references Gesellschaften(Gesellschaft_ID)
);

-- Assoziationstabelle zwischen Mitarbeiter und Gesellschaft
create table in_Gesellschaft (
	Mitarbeiter_ID integer not null,
	Gesellschaft_ID integer not null,
	Mandant_ID integer not null,
	Datum_Von date not null,
    Datum_Bis date not null,
    primary key (Mitarbeiter_ID, Gesellschaft_ID, Datum_Bis),
    constraint fk_ingesellschaft_mitarbeiter
    	foreign key (Mitarbeiter_ID) 
    		references Mitarbeiter(Mitarbeiter_ID),
    constraint fk_ingesellschaft_gesellschaften
    	foreign key (Gesellschaft_ID) 
    		references Gesellschaften(Gesellschaft_ID),
	constraint fk_ingesellschaft_mandanten
		foreign key (Mandant_ID) 
			references Mandanten(Mandant_ID)
);

-- Assoziationstabelle zwischen Erstwohnsitze und Gesellschaft
create table sitzt_in (
	Gesellschaft_ID integer not null,
	Erstwohnsitz_ID integer not null,
	Mandant_ID integer not null,
	Datum_Von date not null,
    Datum_Bis date not null,
    primary key (Gesellschaft_ID, Datum_Bis),
    constraint fk_sitztin_gesellschaften
    	foreign key (Gesellschaft_ID) 
    		references Gesellschaften(Gesellschaft_ID),
    constraint fk_sitztin_erstwohnsitze
    	foreign key (Erstwohnsitz_ID) 
    		references Erstwohnsitze(Erstwohnsitz_ID),
	constraint fk_sitztin_mandanten
		foreign key (Mandant_ID) 
			references Mandanten(Mandant_ID)
);

-- Tabellen, die den Bereich "Entgelt/Tarif" behandeln, erstellen
create table Gewerkschaften (
	Gewerkschaft_ID serial primary key,
	Mandant_ID integer not null,
	Bezeichnung varchar(255) not null,
	constraint fk_gewerkschaften_mandanten
		foreign key (Mandant_ID) 
			references Mandanten(Mandant_ID)
);

create table Tarife (
	Tarif_ID serial primary key,
	Mandant_ID integer not null,
	Tarifbezeichnung varchar(16) not null,
	Gewerkschaft_ID integer not null,
	constraint fk_tarife_mandanten
		foreign key (Mandant_ID) 
			references Mandanten(Mandant_ID),
	constraint fk_tarife_gewerkschaften
		foreign key (Gewerkschaft_ID)
			references Gewerkschaften(Gewerkschaft_ID)
);

create table Verguetungen (
	Verguetung_ID serial primary key,
	Mandant_ID integer not null,
	Grundgehalt_monat decimal(10, 2) not null,
	Weihnachtsgeld decimal(10,2),
	Urlaubsgeld decimal (10, 2),
	Sonderzahlung decimal (10,2),
	constraint fk_verguetungen_mandanten
		foreign key (Mandant_ID) 
			references Mandanten(Mandant_ID)
);

create table hat_Verguetung(
	Tarif_ID integer not null,
	Verguetung_ID integer not null,
	Mandant_ID integer not null,
	Datum_Von date not null,
	Datum_Bis date not null,
	primary key (Tarif_ID, Datum_Bis),
	constraint fk_hatverguetung_tarife
		foreign key (Tarif_ID)
			references Tarife(Tarif_ID),
	constraint fk_hatverguetung_verguetungen
		foreign key (Verguetung_ID)
			references Verguetungen(Verguetung_ID),
	constraint fk_hatverguetung_mandanten
		foreign key (Mandant_ID) 
			references Mandanten(Mandant_ID)
);

create table hat_Tarif (
    Mitarbeiter_ID integer not null,
    Tarif_ID integer not null,
    Mandant_ID integer not null,
    Datum_Von date not null,
    Datum_Bis date not null,
	primary key (Mitarbeiter_ID, Datum_Bis),
	constraint fk_hattarif_mitarbeiter
    	foreign key (Mitarbeiter_ID) 
    		references Mitarbeiter(Mitarbeiter_ID),
    constraint fk_hattarif_tarif
		foreign key (Tarif_ID) 
			references Tarife(Tarif_ID),
	constraint fk_hattarif_mandanten
		foreign key (Mandant_ID) 
			references Mandanten(Mandant_ID)
);

create table Aussertarifliche (
	Mitarbeiter_ID integer not null,
	Mandant_ID integer not null,
	Datum_Von date not null,
	Datum_Bis date not null,
	Grundgehalt_monat decimal(10, 2) not null,
	Weihnachtsgeld decimal(10,2),
	Urlaubsgeld decimal (10, 2),
	Sonderzahlung decimal (10,2),
	primary key (Mitarbeiter_ID, Datum_Bis),
	constraint fk_aussertarifliche_mitarbeiter
		foreign key (Mitarbeiter_ID)
			references Mitarbeiter(Mitarbeiter_ID),
	constraint fk_aussertarifliche_mandanten
		foreign key (Mandant_ID) 
			references Mandanten(Mandant_ID)		
);

-- Tabellen für den Bereich "Beamte" erzeugen
create table Beamte (
	Mitarbeiter_ID integer not null,
	Mandant_ID integer not null,
	Datum_Von date not null,
	Datum_Bis date not null,
	primary key (Mitarbeiter_ID, Datum_Bis),
	constraint fk_beamte_mitarbeiter
		foreign key (Mitarbeiter_ID)
			references Mitarbeiter(Mitarbeiter_ID),
	constraint fk_beamte_mandanten
		foreign key (Mandant_ID) 
			references Mandanten(Mandant_ID)		
);

create table Beamtenzuschuesse (
	AG_Beamtenzuschuesse_ID serial primary key,
	Mandant_ID integer not null,
	AG_Zuschuss_Krankenversicherung decimal (7, 2) not null,
	AG_Zuschuss_KVZusatzbeitrag decimal (7, 2),
	AG_Zuschuss_Pflegeversicherung decimal (7, 2),
	constraint fk_beamtenzuschuesse_mandanten
		foreign key (Mandant_ID)
			references Mandanten(Mandant_ID)
);

create table bekommt_Beamtenzuschuesse(
	Mitarbeiter_ID integer not null,
	AG_Beamtenzuschuesse_ID integer not null,
	Mandant_ID integer not null,
	Datum_Von date not null,
	Datum_Bis date not null,
	constraint fk_bekommtbeamtenzuschuesse_mandanten
		foreign key (Mandant_ID)
			references Mandanten(Mandant_ID)
);

-- Tabellen, die den Bereich "SV-Angestellte" behandeln, erzeugen
create table SVpflichtige_Angestellte (
	Mitarbeiter_ID integer not null,
	Mandant_ID integer not null,
	primary key (Mitarbeiter_ID),
	constraint fk_svpflichtigeangestellte_mitarbeiter
		foreign key (Mitarbeiter_ID)
			references Mitarbeiter(Mitarbeiter_ID),
	constraint fk_svpflichtigeangestellte_mandanten
		foreign key (Mandant_ID) 
			references Mandanten(Mandant_ID)		
);

-- 1) Tabellen für die Unfall-, Renten- und Arbeitslosenversicherung erstellen, da Diese alle SV-pflichtige Angestellte betrifft (egal ob gesetzlich oder privat krankenversichert)
-- Tabellen für die Unfallversicherung erstellen
create table Risikoklassen(
	Risikoklasse_ID serial primary key,
	Mandant_ID integer not null,
	Bezeichnung varchar(16) not null,
	constraint fk_risikoklassen_mandanten
		foreign key (Mandant_ID) 
			references Mandanten(Mandant_ID)
);

create table Unfallversicherungen(
	AG_Unfallversicherungs_ID serial primary key,
	Mandant_ID integer not null,
	Risikoklasse_ID integer not null,
	AG_Unfallversicherungsbeitrag_in_Prozent decimal(5,3),
	Beitrag_Gueltig_Von date not null,
	Beitrag_Gueltig_Bis date not null,
	constraint fk_unfallversicherungen_mandanten
		foreign key (Mandant_ID) 
			references Mandanten(Mandant_ID),
	constraint fk_unfallversicherungen_risikoklassen
		foreign key (Risikoklasse_ID) 
			references Risikoklassen(Risikoklasse_ID)
);

create table ist_in_Unfallversicherung(
	Mitarbeiter_ID integer not null,
	AG_Unfallversicherungs_ID integer not null,
	Mandant_ID integer not null,
	Datum_Von date not null,
	Datum_Bis date not null,
	primary key (Mitarbeiter_ID, Datum_Bis),
	constraint fk_istinUnfallversicherung_svpflichtigeangestellte
		foreign key (Mitarbeiter_ID)
			references SVpflichtige_Angestellte(Mitarbeiter_ID),
	constraint fk_istinUnfallversicherung_unfallversicherungen
		foreign key (AG_Unfallversicherungs_ID)
			references Unfallversicherungen(AG_Unfallversicherungs_ID),
	constraint fk_istinUnfallversicherung_mandanten
		foreign key (Mandant_ID) 
			references Mandanten(Mandant_ID)
);

-- Tabellen für die Rentenversicherung erstellen
create table Rentenversicherungsbeitraege(
	Rentenversicherungsbeitrag_ID serial primary key,
	Mandant_ID integer not null,
	AG_Rentenversicherungsbeitrag_in_Prozent decimal(5,3) not null,
	AN_Rentenversicherungsbeitrag_in_Prozent decimal(5,3) not null,
	Beitragsbemessungsgrenze_RV_Ost decimal(8,2) not null,
	Beitragsbemessungsgrenze_RV_West decimal(8,2) not null,
	constraint fk_rentenversicherungsbeitraege_mandanten
		foreign key (Mandant_ID) 
			references Mandanten(Mandant_ID)
);

create table hat_RVBeitraege(
	Mitarbeiter_ID integer not null,
	Rentenversicherungsbeitrag_ID integer not null,
	Mandant_ID integer not null,
	Datum_Von date not null,
	Datum_Bis date not null,
	primary key (Mitarbeiter_ID, Datum_Bis),
	constraint fk_hatrvbeitraege_svpflichtigeangestellte
		foreign key (Mitarbeiter_ID)
			references SVpflichtige_Angestellte(Mitarbeiter_ID),
	constraint fk_hatrvbeitraege_rentenversicherungsbeitraege
		foreign key (Rentenversicherungsbeitrag_ID)
			references Rentenversicherungsbeitraege(Rentenversicherungsbeitrag_ID),
	constraint fk_hatrvbeitraege_mandanten
		foreign key (Mandant_ID) 
			references Mandanten(Mandant_ID)
);

-- Tabellen für die Arbeitslosenversicherung erstellen
create table Arbeitslosenversicherungsbeitraege(
	Arbeitslosenversicherungsbeitrag_ID serial primary key,
	Mandant_ID integer not null,
	AG_Arbeitslosenversicherungsbeitrag_in_Prozent decimal(5,3) not null,
	AN_Arbeitslosenversicherungsbeitrag_in_Prozent decimal(5,3) not null,
	Beitragsbemessungsgrenze_AV_Ost decimal(8,2) not null,
	Beitragsbemessungsgrenze_AV_West decimal(8,2) not null,
	constraint fk_arbeitslosenversicherungsbeitraege_mandanten
		foreign key (Mandant_ID) 
			references Mandanten(Mandant_ID)
);

create table hat_AVBeitraege(
	Mitarbeiter_ID integer not null,
	Arbeitslosenversicherungsbeitrag_ID integer not null,
	Mandant_ID integer not null,
	Datum_Von date not null,
	Datum_Bis date not null,
	primary key (Mitarbeiter_ID, Datum_Bis),
	constraint fk_hatavbeitraege_svpflichtigeangestellte
		foreign key (Mitarbeiter_ID)
			references SVpflichtige_Angestellte(Mitarbeiter_ID),
	constraint fk_hatavbeitraege_arbeitslosenversicherungsbeitraege
		foreign key (Arbeitslosenversicherungsbeitrag_ID)
			references Arbeitslosenversicherungsbeitraege(Arbeitslosenversicherungsbeitrag_ID),
	constraint fk_hatavbeitraege_mandanten
		foreign key (Mandant_ID) 
			references Mandanten(Mandant_ID)
);

-- Spezialisierung eines SV-pflichtigen Angestellten: privat kranken- und pflegeversichert
create table KV_PV_Privat (
	Mitarbeiter_ID integer not null,
	Mandant_ID integer not null,
	AG_Zuschuss_Krankenversicherung decimal(8,2) not null,
	AG_Zuschuss_Zusatzbeitrag decimal(8,2) not null,
	AG_Zuschuss_Pflegeversicherung decimal(8,2) not null,
	Datum_Von date not null,
	Datum_Bis date not null,
	primary key (Mitarbeiter_ID),
	constraint fk_kvpvprivat_svpflichtigeangestellte
		foreign key (Mitarbeiter_ID)
			references SVpflichtige_Angestellte(Mitarbeiter_ID),
	constraint fk_kvpvprivat_mandanten
		foreign key (Mandant_ID) 
			references Mandanten(Mandant_ID)		
);

-- Spezialisierung eines SV-pflichtigen Angestellten: gesetzlich kranken- und pflegeversichert
create table KV_PV_Gesetzlich (
	Mitarbeiter_ID integer not null,
	Mandant_ID integer not null,
	Datum_Von date not null,
	Datum_Bis date not null,
	primary key (Mitarbeiter_ID),
	constraint fk_kvpvgesetzlich_svpflichtigeangestellte
		foreign key (Mitarbeiter_ID)
			references SVpflichtige_Angestellte(Mitarbeiter_ID),
	constraint fk_kvpvgesetzlich_mandanten
		foreign key (Mandant_ID) 
			references Mandanten(Mandant_ID)		
);

-- Tabellen für das Thema Zusatzbeiträge Krankenversicherung
create table KV_Zusatzbeitraege(
	Zusatzbeitrag_ID serial primary key,
	Mandant_ID integer not null,
	Zusatzbeitrag_Krankenversicherung_in_Prozent decimal(5,3) not null,
	constraint fk_kvzusatzbeitraege_mandanten
		foreign key (Mandant_ID) 
			references Mandanten(Mandant_ID)
);

create table Krankenkassen(
	Krankenkasse_ID serial primary key,
	Mandant_ID integer not null,
	Bezeichnung varchar(128) not null,
	Abkuerzung varchar(16),
	constraint fk_krankenkassen_mandanten
		foreign key (Mandant_ID) 
			references Mandanten(Mandant_ID)
);

create table hat_KV_Zusatzbeitrag(
	Krankenkasse_ID integer not null,
	Zusatzbeitrag_ID integer not null,
	Mandant_ID integer not null,
	Gueltig_Von date not null,
	Gueltig_Bis date not null,
	primary key (Krankenkasse_ID, Gueltig_Bis),
	constraint fk_hatkVzusatzbeitrag_krankenkassen
		foreign key (Krankenkasse_ID)
			references Krankenkassen(Krankenkasse_ID),
	constraint fk_hatkVzusatzbeitrag_kvzusatzbeitraege
		foreign key (Zusatzbeitrag_ID)
			references KV_Zusatzbeitraege(Zusatzbeitrag_ID),
	constraint fk_hatkVzusatzbeitrag_mandanten
		foreign key (Mandant_ID) 
			references Mandanten(Mandant_ID)
);

create table ist_in_GKV(
	Mitarbeiter_ID integer not null,
	Krankenkasse_ID integer not null,
	Mandant_ID integer not null,
	Datum_Von date not null,
	Datum_Bis date not null,
	primary key (Mitarbeiter_ID, Datum_Bis),
	constraint fk_istingkv_kvpvgesetzlich
		foreign key (Mitarbeiter_ID)
			references KV_PV_Gesetzlich(Mitarbeiter_ID),
	constraint fk_istingkv_krankenkassen
		foreign key (Krankenkasse_ID)
			references Krankenkassen(Krankenkasse_ID),
	constraint fk_istingkv_mandanten
		foreign key (Mandant_ID) 
			references Mandanten(Mandant_ID)
);

-- Tabellen für das Thema Arbeitgeberbeiträge Pflegeversicherung
create table AG_Pflegeversicherungsbeitraege_gesetzlich(
	AG_PV_Beitrag_ID serial primary key,
	Mandant_ID integer not null,
	AG_Anteil_Pflegeversicherungsbeitrag_in_Prozent decimal(5,3) not null,
	constraint fk_agpflegeversicherungsbeitraegegesetzlich_mandanten
		foreign key (Mandant_ID) 
			references Mandanten(Mandant_ID)
);

create table wohnhaft_Sachsen(
	wohnhaft_Sachsen_ID serial primary key,
	Mandant_ID integer not null,
	in_Sachsen boolean not null,
	constraint fk_wohnhaftsachsen_mandanten
		foreign key (Mandant_ID) 
			references Mandanten(Mandant_ID)
);

create table hat_gesetzlichen_AG_PV_Beitragssatz(
	wohnhaft_Sachsen_ID integer not null,
	AG_PV_Beitrag_ID integer not null,
	Mandant_ID integer not null,
	Gueltig_Von date not null,
	Gueltig_Bis date not null,
	primary key (wohnhaft_Sachsen_ID, Gueltig_Bis),
	constraint fk_hatgesetzlichenagpvbeitragssatz_wohnhaftsachsen
		foreign key (wohnhaft_Sachsen_ID)
			references wohnhaft_Sachsen(wohnhaft_Sachsen_ID),
	constraint fk_hatgesetzlichenagpvbeitragssatz_agpvbeitraegegesetzlich
		foreign key (AG_PV_Beitrag_ID)
			references AG_Pflegeversicherungsbeitraege_gesetzlich(AG_PV_Beitrag_ID),
	constraint fk_hatgesetzlichenagpvbeitragssatz_mandanten
		foreign key (Mandant_ID) 
			references Mandanten(Mandant_ID)
);

create table wohnt_in_Sachsen(
	Mitarbeiter_ID integer not null,
	wohnhaft_Sachsen_ID integer not null,
	Mandant_ID integer not null,
	Datum_Von date not null,
	Datum_Bis date not null,
	primary key (Mitarbeiter_ID, Datum_Bis),
	constraint fk_wohntinsachsen_kvpvgesetzlich
		foreign key (Mitarbeiter_ID)
			references KV_PV_Gesetzlich(Mitarbeiter_ID),
	constraint fk_wohntinsachsen_wohnhaftsachsen
		foreign key (wohnhaft_Sachsen_ID)
			references wohnhaft_Sachsen(wohnhaft_Sachsen_ID),
	constraint fk_wohntinsachsen_mandanten
		foreign key (Mandant_ID) 
			references Mandanten(Mandant_ID)
);

-- Tabellen für das Thema Arbeitnehmerbeiträge Pflegeversicherung
create table AN_Pflegeversicherungsbeitraege_gesetzlich(
	AN_PV_Beitrag_ID serial primary key,
	Mandant_ID integer not null,
	AN_Anteil_Pflegeversicherungsbeitrag_in_Prozent decimal(5,3) not null,
	Beitragsbemessungsgrenze_PV_Ost decimal(8,2) not null,
	Beitragsbemessungsgrenze_PV_West decimal(8,2) not null,
	constraint fk_anpflegeversicherungsbeitraegegesetzlich_mandanten
		foreign key (Mandant_ID) 
			references Mandanten(Mandant_ID)
);

create table Anzahl_Kinder_unter_25(
	Anzahl_Kinder_unter_25_ID serial primary key,
	Mandant_ID integer not null,
	Anzahl_Kinder integer not null,
	constraint fk_anzahlkinderunter25_mandanten
		foreign key (Mandant_ID) 
			references Mandanten(Mandant_ID)
);

create table hat_gesetzlichen_AN_PV_Beitragssatz(
	Anzahl_Kinder_unter_25_ID integer not null,
	AN_PV_Beitrag_ID integer not null,
	Mandant_ID integer not null,
	Gueltig_Von date not null,
	Gueltig_Bis date not null,
	primary key (Anzahl_Kinder_unter_25_ID, Gueltig_Bis),
	constraint fk_hatgesetzlichenanpvbeitragssatz_anzahlkinderunter25
		foreign key (Anzahl_Kinder_unter_25_ID)
			references Anzahl_Kinder_unter_25(Anzahl_Kinder_unter_25_ID),
	constraint fk_hatgesetzlichenanpvbeitragssatz_anpvbeitraegegesetzlich
		foreign key (AN_PV_Beitrag_ID)
			references AN_Pflegeversicherungsbeitraege_gesetzlich(AN_PV_Beitrag_ID),
	constraint fk_hatgesetzlichenanpvbeitragssatz_mandanten
		foreign key (Mandant_ID) 
			references Mandanten(Mandant_ID)
);

create table hat_x_Kinder_unter25(
	Mitarbeiter_ID integer not null,
	Anzahl_Kinder_unter_25_ID integer not null,
	Mandant_ID integer not null,
	Datum_Von date not null,
	Datum_Bis date not null,
	primary key (Mitarbeiter_ID, Datum_Bis),
	constraint fk_hatxkinderunter25_kvpvgesetzlich
		foreign key (Mitarbeiter_ID)
			references KV_PV_Gesetzlich(Mitarbeiter_ID),
	constraint fk_hatxkinderunter25_anzahlkinderunter25
		foreign key (Anzahl_Kinder_unter_25_ID)
			references Anzahl_Kinder_unter_25(Anzahl_Kinder_unter_25_ID),
	constraint fk_hatxkinderunter25_mandanten
		foreign key (Mandant_ID) 
			references Mandanten(Mandant_ID)
);

-- Tabellen für das Thema Krankenversicherungsbeiträge
create table Krankenversicherungsbeitraege(
	Krankenversicherungsbeitraege_ID serial primary key,
	Mandant_ID integer not null,
	AG_Krankenversicherungsbeitrag_in_Prozent decimal(5,3) not null,
	Beitragsbemessungsgrenze_KV_Ost decimal(5,3) not null,
	Beitragsbemessungsgrenze_KV_West decimal(8,2) not null,
	constraint fk_krankenversicherungsbeitraege_mandanten
		foreign key (Mandant_ID) 
			references Mandanten(Mandant_ID)
);

create table hat_KVBeitraege(
	Mitarbeiter_ID integer not null,
	Krankenversicherungsbeitraege_ID integer not null,
	Mandant_ID integer not null,
	Datum_Von date not null,
	Datum_Bis date not null,
	primary key (Mitarbeiter_ID, Datum_Bis),
	constraint fk_hatkvbeitraege_kvpvgesetzlich
		foreign key (Mitarbeiter_ID)
			references KV_PV_Gesetzlich(Mitarbeiter_ID),
	constraint fk_hatkvbeitraege_krankenversicherungsbeitraege
		foreign key (Krankenversicherungsbeitraege_ID)
			references Krankenversicherungsbeitraege(Krankenversicherungsbeitraege_ID),
	constraint fk_hatkvbeitraege_mandanten
		foreign key (Mandant_ID) 
			references Mandanten(Mandant_ID)
);


