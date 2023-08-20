drop table Mitarbeiter;
drop table Austrittsgruende;
drop table Geschlecht;
drop table Austrittsgrund_Kategorien;


create table Austrittsgrund_Kategorien (
	AustrittsgrundKategorie_ID serial primary key,
	Bezeichnung varchar(20) CHECK (Bezeichnung IN ('personenbedingt', 'verhaltensbedingt', 'betriebsbedingt', 'ausserordentlich'))
);

create table Austrittsgruende (
	Austrittsgrund_ID serial primary key,
	Beschreibung text not null,
	AustrittsgrundKategorie_ID integer not null,
	constraint fk_austrittsgrundkategorien 
		foreign key (AustrittsgrundKategorie_ID) 
			references Austrittsgrund_Kategorien(AustrittsgrundKategorie_ID)
);

CREATE TABLE Geschlecht (
    Geschlecht_ID serial PRIMARY KEY,
    Bezeichnung varchar(10) CHECK (Bezeichnung IN ('weiblich', 'männlich', 'divers'))
);

CREATE TABLE Mitarbeiter (
    Mitarbeiter_ID serial PRIMARY KEY,
    Vorname varchar(100) NOT NULL,
    Nachname varchar(100) NOT NULL,
    Geburtsdatum DATE NOT NULL,
    Eintrittsdatum DATE NOT NULL,
    Austrittsdatum DATE,
    Wochenarbeitszeit integer NOT NULL,
    Steuernummer varchar(25) NOT NULL,
    Sozialversicherungsnummer varchar(25) NOT NULL,
    ISBN varchar(25) NOT NULL,
    Telefonnummer varchar(25) NOT NULL,
    Private_Emailadresse varchar(100) NOT NULL,
    Austrittsgrund_ID integer,
    Geschlecht_ID integer NOT NULL,
    constraint fk_austrittsgruende 
    	foreign key (Austrittsgrund_ID) 
    		references Austrittsgruende(Austrittsgrund_ID),
    constraint fk_geschlecht 
    	foreign key (Geschlecht_ID) 
    		references Geschlecht(Geschlecht_ID)
);