-- Tabellen, die den Bereich "Austrittsgruende" behandeln, erstellen
create table Kategorien_Austrittsgruende (
	Kategorie_Austrittsgruende_ID serial primary key,
	Bezeichnung varchar(20) not null
);

create table Austrittsgruende (
	Austrittsgrund_ID serial primary key,
	Bezeichnung varchar(50) not null,
	Kategorie_Austrittsgruende_ID integer not null,
	constraint fk_austrittsgrundkategorien 
		foreign key (Kategorie_Austrittsgruende_ID) 
			references Kategorien_Austrittsgruende(Kategorie_Austrittsgruende_ID)
);

-- Zentrale Tabelle "Mitarbeiter"
create table Mitarbeiter (
    Mitarbeiter_ID serial primary key,
    Vorname varchar(100) not null,
    Nachname varchar(100) not null,
    Geschlecht varchar(10) check (Geschlecht in ('weiblich', 'maennlich', 'divers')),
    Geburtsdatum date not null,
    Eintrittsdatum date not null, 
    Steuernummer varchar(50) not null,
    Sozialversicherungsnummer varchar(50) not null,
    IBAN varchar(50) not null,
    Telefonnummer varchar(50) not null,
    Private_Emailadresse varchar(100) not null,
    Austrittsdatum date,
    Austrittsgrund_ID integer,
    constraint fk_austrittsgruende 
    	foreign key (Austrittsgrund_ID) 
    		references Austrittsgruende(Austrittsgrund_ID)
);

-- Tabellen, die den Bereich "Wochenarbeitsstunden" behandeln, erstellen
create table Wochenarbeitsstunden(
	Wochenarbeitsstunden_ID serial primary key,
	in_Stunden decimal(4, 2) not null
);

create table arbeitet_x_Wochenstunden (
    Mitarbeiter_ID integer not null,
    Wochenarbeitsstunden_ID integer not null,
    Datum_Von date not null,
    Datum_Bis date not null,
    primary key (Mitarbeiter_ID, Datum_Bis),
    constraint fk_mitarbeiter
    	foreign key (Mitarbeiter_ID) 
    		references Mitarbeiter(Mitarbeiter_ID),
    constraint fk_wochenarbeitsstunden
    	foreign key (Wochenarbeitsstunden_ID) 
    		references Wochenarbeitsstunden(Wochenarbeitsstunden_ID)
);

-- Tabellen, die den Bereich "Steuerklasse" behandeln, erstellen
create table Steuerklassen (
    Steuerklasse_ID serial primary key,
    Beschreibung varchar(255) not null
);

-- Assoziationstabelle zwischen Mitarbeiter und Steuerklasse
create table in_Steuerklasse (
    Mitarbeiter_ID integer not null,
    Steuerklasse_ID integer not null,
    Datum_Von date not null,
    Datum_Bis date not null,
    primary key (Mitarbeiter_ID, Datum_Bis),
    constraint fk_mitarbeiter
    	foreign key (Mitarbeiter_ID) 
    		references Mitarbeiter(Mitarbeiter_ID),
    constraint fk_steuerklassen
    	foreign key (Steuerklasse_ID) 
    		references Steuerklassen(Steuerklasse_ID)
);

-- Tabellen, die den Bereich "Jobtitel" behandeln, erstellen
create table Erfahrungsstufen (
	Erfahrungsstufe_ID serial primary key,
	Bezeichnung varchar(50) not null
);

create table Jobtitel (
	Jobtitel_ID serial primary key,
	Bezeichnung varchar(50) not null
);

-- Assoziationstabelle zwischen Mitarbeiter und Jobtitel + Erfahrungsstufen
create table hat_Jobtitel (
	Mitarbeiter_ID integer not null,
	Jobtitel_ID integer not null,
	Erfahrungsstufe_ID integer not null,
	Datum_Von date not null,
    Datum_Bis date not null,
    primary key (Mitarbeiter_ID, Datum_Bis),
    constraint fk_mitarbeiter
    	foreign key (Mitarbeiter_ID) 
    		references Mitarbeiter(Mitarbeiter_ID),
    constraint fk_jobtitel
    	foreign key (Jobtitel_ID) 
    		references Jobtitel(Jobtitel_ID),
    constraint fk_erfahrungsstufen
		foreign key (Erfahrungsstufe_ID)
			references Erfahrungsstufen(Erfahrungsstufe_ID)
);

-- Tabellen, die den Bereich "Adresse" behandeln, erstellen
create table Laender (
	Land_ID serial primary key,
	Landesname varchar(100) not null
);

create table Staedte (
	Stadt_ID serial primary key,
	stadtname varchar(100) not null,
	Land_ID integer not null,
	constraint fk_laender
		foreign key (Land_ID)
			references Laender(Land_ID)
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
    Datum_Bis date not null,
    primary key (Mitarbeiter_ID, Erstwohnsitz_ID, Datum_Bis),
    constraint fk_mitarbeiter
    	foreign key (Mitarbeiter_ID) 
    		references Mitarbeiter(Mitarbeiter_ID),
    constraint fk_erstwohnsitze
    	foreign key (Erstwohnsitz_ID) 
    		references Erstwohnsitze(Erstwohnsitz_ID)
);

-- Tabellen, die den Bereich "Abteilung" behandeln, erstellen
create table Abteilungen (
	Abteilung_ID serial primary key,
	Bezeichnung varchar(50) not null,
	untersteht_Abteilung integer,
	constraint fk_Abteilung
		foreign key (untersteht_Abteilung)
			references Abteilungen(Abteilung_ID)
);

-- Assoziationstabelle zwischen Mitarbeiter und Geschäftsbereich
create table eingesetzt_in (
	Mitarbeiter_ID integer not null,
	Abteilung_ID integer not null,
	Datum_Von date not null,
    Datum_Bis date not null,
    fuehrungskraft boolean not null,
    primary key (Mitarbeiter_ID, Abteilung_ID, Datum_Bis),
    constraint fk_mitarbeiter
    	foreign key (Mitarbeiter_ID) 
    		references Mitarbeiter(Mitarbeiter_ID),
    constraint fk_abteilungen
    	foreign key (Abteilung_ID) 
    		references Abteilungen(Abteilung_ID)
);

-- Tabellen, die den Bereich "Mitarbeitertyp" (Angestellter, Arbeiter, Praktikant, Werkstudent etc.) behandeln, erstellen
create table Mitarbeitertypen (
	Mitarbeitertyp_ID serial primary key,
	Bezeichnung varchar(20)
);

-- Assoziationstabelle zwischen Mitarbeiter und Mitarbeitertyp
create table ist_Mitarbeitertyp (
	Mitarbeiter_ID integer not null,
	Mitarbeitertyp_ID integer not null,
	Datum_Von date not null,
    Datum_Bis date not null,
    primary key (Mitarbeiter_ID, Datum_Bis),
    constraint fk_mitarbeiter
    	foreign key (Mitarbeiter_ID) 
    		references Mitarbeiter(Mitarbeiter_ID),
    constraint fk_mitarbeitertypen
    	foreign key (Mitarbeitertyp_ID) 
    		references Mitarbeitertypen(Mitarbeitertyp_ID)
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
    Datum_Bis date not null,
    primary key (Mitarbeiter_ID, Gesellschaft_ID, Datum_Bis),
    constraint fk_mitarbeiter
    	foreign key (Mitarbeiter_ID) 
    		references Mitarbeiter(Mitarbeiter_ID),
    constraint fk_gesellschaften
    	foreign key (Gesellschaft_ID) 
    		references Gesellschaften(Gesellschaft_ID)
);

-- Tabellen, die den Bereich "Entgelt/Tarif" behandeln, erstellen
create table Tarifformen (
	Tarifform_ID serial primary key,
	Bezeichnung varchar(20)
);

create table Entgelt (
	Mitarbeiter_ID integer not null,
	Tarifform_ID integer not null,
	Datum_Von date not null,
	Datum_Bis date not null,
	primary key (Mitarbeiter_ID, Datum_Bis),
    constraint fk_mitarbeiter
    	foreign key (Mitarbeiter_ID) 
    		references Mitarbeiter(Mitarbeiter_ID),
    constraint fk_tarifformen
    	foreign key (Tarifform_ID) 
    		references Tarifformen(Tarifform_ID)
);

create table Aussertarifliche (
	Mitarbeiter_ID integer not null,
	Datum_Bis date not null,
	Grundgehalt_monat decimal(10, 2) not null,
	Weihnachtsgeld decimal(10,2),
	Urlaubsgeld decimal (10, 2),
	Sonderzahlung decimal (10,2),
	primary key (Mitarbeiter_ID, Datum_Bis),
	constraint fk_Entgelt_Aussertarifliche
		foreign key (Mitarbeiter_ID, Datum_Bis)
			references Entgelt(Mitarbeiter_ID, Datum_Bis)
);

create table Gewerkschaften (
	Gewerkschaft_ID serial primary key,
	Bezeichnung varchar(255) not null
);

create table Verguetungen (
	Verguetung_ID serial primary key,
	Grundgehalt_monat decimal(10, 2) not null,
	Weihnachtsgeld decimal(10,2),
	Urlaubsgeld decimal (10, 2),
	Sonderzahlung decimal (10,2)
);

create table Tarife (
	Tarif_ID serial primary key,
	Tarifbezeichnung varchar(20) not null,
	Gewerkschaft_ID integer not null,
	constraint fk_gewerkschaft
		foreign key (Gewerkschaft_ID)
			references Gewerkschaften(Gewerkschaft_ID)
);

create table Tarife_Verguetungen(
	Tarif_ID integer not null,
	Verguetung_ID integer not null,
	Datum_Von date not null,
	Datum_Bis date not null,
	primary key (Tarif_ID, Datum_Bis),
	constraint fk_tarife
		foreign key (Tarif_ID)
			references Tarife(Tarif_ID),
	constraint fk_verguetungen
		foreign key (Verguetung_ID)
			references Verguetungen(Verguetung_ID)
);

create table Tarifbeschaeftigte(
	Mitarbeiter_ID integer not null,
	Datum_Bis date not null,
	Tarif_ID integer not null,
	primary key (Mitarbeiter_ID, Datum_Bis),
	constraint fk_Entgelt2
		foreign key (Mitarbeiter_ID, Datum_Bis)
			references Entgelt(Mitarbeiter_ID, Datum_Bis),
	constraint fk_tarife
		foreign key (Tarif_ID)
			references Tarife(Tarif_ID)
);

