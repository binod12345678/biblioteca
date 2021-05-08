insert into categoria (id, nome)
values(0, 'horror');

insert into categoria (id, nome)
values(1, 'fantasy');

insert into categoria (id, nome)
values(2, 'finanza');

insert into categoria (id, nome)
values(3, 'romanzo');

insert into categoria (id, nome)
values(4, 'giallo');

insert into categoria (id, nome)
values(5, 'rosa');

insert into categoria (id, nome)
values(6, 'narrativa classica');

insert into categoria (id, nome)
values(7, 'fantascienza');

insert into categoria (id, nome)
values(8, 'psicologia');

insert into categoria (id, nome)
values(9, 'ragazzi');

insert into categoria (id, nome)
values(10, 'economia');

insert into categoria (id, nome)
values(11, 'management');

insert into libro (isbn, titolo, lingua, editore, anno, copie)
values(4165472289563,'La coscienza di Zeno', 'italiano', 'Newton Compton Editori', 2014, 30); 
insert into autore (id, nome, cognome, data_nascita, luogo_nascita) 
values (0, 'Italo', 'Svevo', '1861-12-19', 'Italia');
insert into bridge_categoria (isbn_libro, id_categoria) 
values (4165472289563, 6);
insert into bridge_autore (isbn_libro, id_autore) 
values (4165472289563, 0);

insert into libro (isbn, titolo, lingua, editore, anno, copie)
values(8322066111124,'1984', 'italiano', 'HarperCollins Publishers', 1949, 16); 
insert into autore (id, nome, cognome, data_nascita, luogo_nascita) 
values (1, 'George', 'Orwell', '1903-06-25', 'India');
insert into bridge_categoria (isbn_libro, id_categoria) 
values (8322066111124, 7);
insert into bridge_categoria (isbn_libro, id_categoria) 
values (8322066111124, 3);
insert into bridge_autore (isbn_libro, id_autore) 
values (8322066111124, 1);

insert into libro (isbn, titolo, lingua, editore, anno, copie)
values(9788854171633,'L interpretazione dei sogni', 'italiano', 'Newton Compton Editori', 1899, 10); 
insert into autore (id, nome, cognome, data_nascita, luogo_nascita) 
values (2, 'Sigmund', 'Freud', '1856-05-06', 'Repubblica Ceca');
insert into bridge_categoria (isbn_libro, id_categoria) 
values (9788854171633, 8);
insert into bridge_autore (isbn_libro, id_autore) 
values (9788854171633, 2);

insert into libro (isbn, titolo, lingua, editore, anno, copie)
values(9788831003445,'Harry Potter e i doni della morte', 'italiano', 'Salani', 2015, 48); 
insert into autore (id, nome, cognome, data_nascita, luogo_nascita) 
values (3, 'J.K.', 'Rowling', '1965-07-31', 'Regno Unito');
insert into bridge_categoria (isbn_libro, id_categoria) 
values (9788831003445, 1);
insert into bridge_categoria (isbn_libro, id_categoria) 
values (9788831003445, 9);
insert into bridge_autore (isbn_libro, id_autore) 
values (9788831003445, 3);


insert into libro (isbn, titolo, lingua, editore, anno, copie)
values(9788820396244,'L investitore intelligente', 'italiano', 'Hoepli', 2005, 30); 
insert into autore (id, nome, cognome, data_nascita, luogo_nascita) 
values (4, 'Benjamin', 'Graham', '1894-05-09', 'Regno Unito');
insert into bridge_categoria (isbn_libro, id_categoria) 
values (9788820396244, 2);
insert into bridge_categoria (isbn_libro, id_categoria) 
values (9788820396244, 10);
insert into bridge_categoria (isbn_libro, id_categoria) 
values (9788820396244, 11);
insert into bridge_autore (isbn_libro, id_autore) 
values (9788820396244, 4);

insert into libro (isbn, titolo, lingua, editore, anno, copie)
values(12345678910123,'test', 'italiano', 'test-editore', 2020, 61); 
insert into bridge_categoria (isbn_libro, id_categoria) 
values (12345678910123, 0);
insert into bridge_categoria (isbn_libro, id_categoria) 
values (12345678910123, 3);
insert into bridge_categoria (isbn_libro, id_categoria) 
values (12345678910123, 6);
insert into bridge_autore (isbn_libro, id_autore) 
values (12345678910123, 4);
insert into bridge_autore (isbn_libro, id_autore) 
values (12345678910123, 1);

insert into utente (id_tessera, data_registrazione, nome, cognome, telefono, indirizzo, email) 
values (0, '2021-01-01', 'Jalex', 'Follosco', '3896276542', 'via xyz', 'follosco.j@itsrizzoli.it');

insert into utente (id_tessera, data_registrazione, nome, cognome, telefono, indirizzo, email) 
values (1, '2021-01-02', 'Binod', 'Comini', '3884835678', 'via abc', 'comini.b@itsrizzoli.it');

insert into utente (id_tessera, data_registrazione, nome, cognome, telefono, indirizzo, email) 
values (2, '2021-01-02', 'Mario', 'Rossi', '3814825408', 'via def', 'rossi.m@itsrizzoli.it');

insert into utente (id_tessera, data_registrazione, nome, cognome, telefono, indirizzo, email) 
values (3, '2021-01-05', 'Luca', 'Verdi', '3214325400', 'via ghi', 'verdi.l@itsrizzoli.it');

insert into utente (id_tessera, data_registrazione, nome, cognome, telefono, indirizzo, email) 
values (4, '2021-01-15', 'Luigi', 'Bianchi', '3294325007', 'via jkl', 'bianchi.l@itsrizzoli.it');


insert into prestito(isbn_libro, tessera_id, data_prestito, data_restituzione)
values (9788820396244, 0, '2021-01-05', '2021-01-25');
insert into prestito(isbn_libro, tessera_id, data_prestito, data_restituzione)
values (9788854171633, 0, '2021-01-25', '2021-02-07');
insert into prestito(isbn_libro, tessera_id, data_prestito, data_restituzione)
values (4165472289563, 0, '2021-05-01', null);
insert into prestito(isbn_libro, tessera_id, data_prestito, data_restituzione)
values (9788820396244, 1, '2021-01-15', '2021-01-30');
insert into prestito(isbn_libro, tessera_id, data_prestito, data_restituzione)
values (9788854171633, 1, '2021-02-03', null);
insert into prestito(isbn_libro, tessera_id, data_prestito, data_restituzione)
values (4165472289563, 0, '2021-05-03', null);



