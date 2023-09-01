-- Tabellen, die den Bereich "Austrittsgruende" behandeln, erstellen
create table Kategorien_Austrittsgruende (
	Kategorie_Austrittsgruende_ID serial primary key,
	Bezeichnung varchar(20) check (Bezeichnung in ('personenbedingt', 'verhaltensbedingt', 'betriebsbedingt', 'ausserordentlich'))
);

create table Austrittsgruende (
	Austrittsgrund_ID serial primary key,
	Beschreibung text not null,
	Kategorie_Austrittsgruende_ID integer not null,
	constraint fk_austrittsgrundkategorien 
		foreign key (Kategorie_Austrittsgruende_ID) 
			references Kategorien_Austrittsgruende(Kategorie_Austrittsgruende_ID)
);

-- Tabellen, die den Bereich "Geschlecht" behandeln, erstellen
create table Geschlechter (
    Geschlecht_ID serial primary key,
    Bezeichnung varchar(10) check (Bezeichnung in ('weiblich', 'maennlich', 'divers'))
);

-- Zentrale Tabelle "Mitarbeiter"
create table Mitarbeiter (
    Mitarbeiter_ID serial primary key,
    Vorname varchar(100) not null,
    Nachname varchar(100) not null,
    Geburtsdatum date not null,
    Eintrittsdatum date not null,
    Austrittsdatum date,
    Wochenarbeitszeit integer not null,
    Steuernummer varchar(25) not null,
    Sozialversicherungsnummer varchar(25) not null,
    ISBN varchar(25) not null,
    Telefonnummer varchar(25) not null,
    Private_Emailadresse varchar(100) not null,
    Austrittsgrund_ID integer,
    Geschlecht_ID integer not null,
    constraint fk_austrittsgruende 
    	foreign key (Austrittsgrund_ID) 
    		references Austrittsgruende(Austrittsgrund_ID),
    constraint fk_geschlechter 
    	foreign key (Geschlecht_ID) 
    		references Geschlechter(Geschlecht_ID)
);

-- Tabellen, die den Bereich "Steuerklasse" behandeln, erstellen
create table Steuerklassen (
    Steuerklasse_ID serial primary key,
    Steuerklasse varchar(10) not null,
    Beschreibung varchar(255) not null
);

-- Assoziationstabelle zwischen Mitarbeiter und Steuerklasse
create table in_Steuerklasse (
    Mitarbeiter_ID integer not null,
    Steuerklasse_ID integer not null,
    Datum_Von date not null,
    Datum_Bis date,
    constraint fk_mitarbeiter
    	foreign key (Mitarbeiter_ID) 
    		references Mitarbeiter(Mitarbeiter_ID),
    constraint fk_steuerklassen
    	foreign key (Steuerklasse_ID) 
    		references Steuerklassen(Steuerklasse_ID),
    primary key (Mitarbeiter_ID, Steuerklasse_ID, Datum_Von)
);

-- Tabellen, die den Bereich "Jobtitel" behandeln, erstellen
create table Erfahrungsstufen (
	Erfahrungsstufe_ID serial primary key,
	Bezeichnung varchar(50) not null,
	Bedingungen varchar(255)
);

create table Jobtitel (
	Jobtitel_ID serial primary key,
	Bezeichnung varchar(50) not null,
	Erfahrungsstufe_ID integer not null,
	constraint fk_erfahrungsstufen
		foreign key (Erfahrungsstufe_ID)
			references Erfahrungsstufen(Erfahrungsstufe_ID)
);

-- Assoziationstabelle zwischen Mitarbeiter und Jobtitel
create table hat_Jobtitel (
	Mitarbeiter_ID integer not null,
	Jobtitel_ID integer not null,
	Datum_Von date not null,
    Datum_Bis date,
    constraint fk_mitarbeiter
    	foreign key (Mitarbeiter_ID) 
    		references Mitarbeiter(Mitarbeiter_ID),
    constraint fk_jobtitel
    	foreign key (Jobtitel_ID) 
    		references Jobtitel(Jobtitel_ID),
    primary key (Mitarbeiter_ID, Jobtitel_ID, Datum_Von)
);

-- Tabellen, die den Bereich "Adresse" behandeln, erstellen
create table Laender (
	Land_ID serial primary key,
	Landesname varchar(100) not null
);

create table Regionen (
	Region_ID serial primary key,
	Regionname varchar(100) not null,
	Land_ID integer not null,
	constraint fk_laender
		foreign key (Land_ID)
			references Laender(Land_ID)
);

create table Staedte (
	Stadt_ID serial primary key,
	stadtname varchar(100) not null,
	Region_ID integer not null,
	constraint fk_regionen
		foreign key (Region_ID)
			references Regionen(Region_ID)
);

create table Postleitzahlen (
	Postleitzahl_ID serial primary key,
	Postleitzahl varchar(50) not null,
	Stadt_ID integer not null,
	constraint fk_staedte
		foreign key (Stadt_ID)
			references Staedte(Stadt_ID)
);

create table Erstwohnsitze (
	Erstwohnsitz_ID serial primary key,
	Strasse varchar(100) not null,
	Hausnummer varchar(5) not null,
	Postleitzahl_ID integer not null,
	constraint fk_postleitzahlen
		foreign key (Postleitzahl_ID)
			references Postleitzahlen(Postleitzahl_ID)
);

-- Assoziationstabelle zwischen Mitarbeiter und Adressenbereich
create table wohnt_in (
	Mitarbeiter_ID integer not null,
	Erstwohnsitz_ID integer not null,
	Datum_Von date not null,
    Datum_Bis date,
    constraint fk_mitarbeiter
    	foreign key (Mitarbeiter_ID) 
    		references Mitarbeiter(Mitarbeiter_ID),
    constraint fk_erstwohnsitze
    	foreign key (Erstwohnsitz_ID) 
    		references Erstwohnsitze(Erstwohnsitz_ID),
    primary key (Mitarbeiter_ID, Erstwohnsitz_ID, Datum_Von)
);

-- Tabellen, die den Bereich "Geschaeftseinheit" behandeln, erstellen
create table Geschaeftseinheiten (
	Geschaeftseinheit_ID serial primary key,
	Bezeichnung varchar(50) not null,
	untersteht_geschaeftseinheit integer,
	constraint fk_geschaeftseinheiten
		foreign key (untersteht_geschaeftseinheit)
			references Geschaeftseinheiten(Geschaeftseinheit_ID)
);

-- Assoziationstabelle zwischen Mitarbeiter und Adressenbereich
create table eingesetzt_in (
	Mitarbeiter_ID integer not null,
	Geschaeftseinheit_ID integer not null,
	Datum_Von date not null,
    Datum_Bis date,
    fuehrungskraft boolean not null,
    constraint fk_mitarbeiter
    	foreign key (Mitarbeiter_ID) 
    		references Mitarbeiter(Mitarbeiter_ID),
    constraint fk_geschaeftseinheiten
    	foreign key (Geschaeftseinheit_ID) 
    		references Geschaeftseinheiten(Geschaeftseinheit_ID),
    primary key (Mitarbeiter_ID, Geschaeftseinheit_ID)
);

-- Tabellen, die den Bereich "Mitarbeitertyp" (Angestellter, Arbeiter, Praktikant, Werkstudent etc.) behandeln, erstellen
create table Mitarbeitertypen (
	Mitarbeitertyp_ID serial primary key,
	Bezeichnung varchar (20)
);

-- Assoziationstabelle zwischen Mitarbeiter und Mitarbeitertyp
create table ist_Mitarbeitertyp (
	Mitarbeiter_ID integer not null,
	Mitarbeitertyp_ID integer not null,
	Datum_Von date not null,
    Datum_Bis date,
    constraint fk_mitarbeiter
    	foreign key (Mitarbeiter_ID) 
    		references Mitarbeiter(Mitarbeiter_ID),
    constraint fk_mitarbeitertypen
    	foreign key (Mitarbeitertyp_ID) 
    		references Mitarbeitertypen(Mitarbeitertyp_ID),
    primary key (Mitarbeiter_ID, Mitarbeitertyp_ID)
);

-- Tabellen, die den Bereich "Gesellschaft" behandeln, erstellen
create table Gesellschaften (
	Gesellschaft_ID serial primary key,
	Bezeichnung varchar (50)
);

-- Assoziationstabelle zwischen Mitarbeiter und Gesellschaft
create table in_Gesellschaft (
	Mitarbeiter_ID integer not null,
	Gesellschaft_ID integer not null,
	Datum_Von date not null,
    Datum_Bis date,
    constraint fk_mitarbeiter
    	foreign key (Mitarbeiter_ID) 
    		references Mitarbeiter(Mitarbeiter_ID),
    constraint fk_gesellschaften
    	foreign key (Gesellschaft_ID) 
    		references Gesellschaften(Gesellschaft_ID),
    primary key (Mitarbeiter_ID, Gesellschaft_ID)
);

-- Tabellen, die den Bereich "Entgelt/Tarif" behandeln, erstellen
--create table Tarifformen (
--	Tarifform_ID serial primary key,
--	Bezeichnung varchar(20)
--);

create table Entgelt (
	Entgelt_ID serial primary key,
	Mitarbeiter_ID integer not null,
	--Tarifform_ID integer not null,
	Tarifform varchar(20) check (Tarifform in ('tarifbeschaeftigt', 'aussertariflich')),
	Datum_Von date not null,
	Datum_Bis date,
	--primary key (Mitarbeiter_ID, Tarifform_ID, Datum_Von),
    constraint fk_mitarbeiter
    	foreign key (Mitarbeiter_ID) 
    		references Mitarbeiter(Mitarbeiter_ID)
    --constraint fk_tarifformen
    --	foreign key (Tarifform_ID) 
    --		references Tarifformen(Tarifform_ID)
);

create table Aussertarif (
	Aussertarif_ID serial primary key,
	Datum_Von date not null,
	Datum_Bis date,
	Grundgehalt_monat decimal(10, 2) not null,
	Weihnachtsgeld decimal(10,2),
	Urlaubsgeld decimal (10, 2),
	Sonderzahlung decimal (10,2),
	Entgelt_ID integer not null,
	constraint fk_Entgelt1
		foreign key (Entgelt_ID)
			references Entgelt(Entgelt_ID)
);

create table Gewerkschaften (
	Gewerkschaft_ID serial primary key,
	Bezeichnung varchar(255) not null
);

create table Tarifbezeichnungen (
	Tarifbezeichnung_ID serial primary key,
	Bezeichnung varchar (20) not null,
	Gewerkschaft_ID integer not null,
	constraint fk_Gewerkschaften
		foreign key (Gewerkschaft_ID)
			references Gewerkschaften(Gewerkschaft_ID)
);

create table Tarife (
	Tarif_ID serial primary key,
	Tarifbezeichnung_ID integer not null,
	Datum_Von date not null,
	Datum_Bis date not null,
	Bedingungen varchar(255) not null,
	Grundgehalt_monat decimal(10, 2) not null,
	Weihnachtsgeld decimal(10,2),
	Urlaubsgeld decimal (10, 2),
	Sonderzahlung decimal (10,2),
	constraint fk_tarifbezeichnungen
		foreign key (Tarifbezeichnung_ID)
			references Tarifbezeichnungen(Tarifbezeichnung_ID)
);

create table Tarifbeschaeftigung(
	Entgelt_ID integer not null,
	Tarif_ID integer not null,
	primary key (Entgelt_ID, Tarif_ID),
	constraint fk_Entgelt2
		foreign key (Entgelt_ID)
			references Entgelt(Entgelt_ID),
	constraint fk_tarife
		foreign key (Tarif_ID)
			references Tarife(Tarif_ID)
);



