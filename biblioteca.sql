
create table libro(
	isbn int(7) primary key,
	titolo varchar(255) not null,
	lingua varchar(255),
	editore varchar(255),
	anno int(4),
	copie int(2) not null
);

create table categoria(
	id int(5) primary key,
	nome varchar(255) not null unique
);

create table bridge_categoria(
	isbn_libro int (7) not null references libro(isbn),
	id_categoria int(5) not null references categoria(id)
);

create table autore(
	id int(5) primary key,
	nome varchar(255) not null,
	cognome varchar(255) not null,
	data_nascita date,
	luogo_nascita varchar(255)	
);

create table bridge_autore(
	isbn_libro int (7) not null references libro(isbn),
	id_autore int(5) not null references autore(id)
);

create table utente(
	id_tessera int(5) primary key,
	data_registrazione date not null,
	nome varchar(255) not null,
	cognome varchar(255) not null,
	telefono char(10),
	indirizzo varchar(255),
	email varchar(255) not null
);

create table prestito(
	isbn_libro int(7) not null references libro(isbn),
	tessera_id int(5) not null references utente(id_tessera),
	data_prestito date not null,
	data_restituzione date
);

