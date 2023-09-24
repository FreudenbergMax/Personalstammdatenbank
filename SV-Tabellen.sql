-- Tabellen, die den Bereich "Sozialversicherung" behandeln, erstellen
create table Versicherungsformen(
	Versicherungsform_ID serial primary key,
	Bezeichnung varchar(10) not null
);

create table Sozialversicherte(
	Versicherungsform_ID integer not null,
	Mitarbeiter_ID integer not null,
	Datum_Von date not null,
	Datum_Bis date not null,
	primary key (Mitarbeiter_ID, Datum_Bis),
	constraint fk_versicherungsformen
		foreign key (Versicherungsform_ID)
			references Versicherungsformen(Versicherungsform_ID),
	constraint fk_mitarbeiter
		foreign key (Mitarbeiter_ID)
			references Mitarbeiter(Mitarbeiter_ID)
);

create table Risikoklassen(
	Risikoklasse_ID serial primary key,
	Bezeichnung varchar(50) not null
);

create table Unfallversicherungen(
	AG_Unfallversicherungs_ID serial primary key,
	Risikoklasse_ID integer not null,
	AG_Unfallversicherungsbeitrag_in_prozent decimal(7,6) not null,
	Beitrag_gueltig_von date not null,
	Beitrag_gueltig_bis date not null,
	constraint fk_risikoklassen
		foreign key (Risikoklasse_ID)
			references Risikoklassen(Risikoklasse_ID)
);
/*
create table Ist_in_Unfallversicherung(
	Mitarbeiter_ID integer not null,
	AG_Unfallversicherungs_ID integer not null,
	Beitrag_gueltig_von date not null,
	Beitrag_gueltig_bis date not null,
	primary key(Mitarbeiter_ID, AG_Unfallversicherungs_ID, Beitrag_gueltig_bis),
	constraint fk_unfallversicherungen
		foreign key (AG_Unfallversicherungs_ID)
			references Unfallversicherungen(AG_Unfallversicherungs_ID),
	constraint fk_Sozialversicherte
		foreign key (Mitarbeiter_ID)
			references Sozialversicherte(Mitarbeiter_ID)
);

-- Spezialisierung "privat versichert" 
create table Privat_versicherte (
	Versicherungsform_ID integer not null,
	Mitarbeiter_ID integer not null,
	Datum_Bis date not null,
	primary key (Versicherungsform_ID, Mitarbeiter_ID, Datum_Bis),
	constraint fk_Sozialversicherte_privatVersicherte
		foreign key (Mitarbeiter_ID, Tarifform_ID, Datum_Bis)
			references Entgelt(Mitarbeiter_ID, Tarifform_ID, Datum_Bis)
);
*/

-- entferne Tabellen, die den Bereich "Sozialversicherung" behandeln
--drop table Ist_in_Unfallversicherung;
drop table Unfallversicherungen;
drop table Risikoklassen;
drop table Sozialversicherte;
drop table versicherungsformen;