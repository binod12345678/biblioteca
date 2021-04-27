insert into libro (isbn, titolo, lingua, editore, anno, copie)
values(0000000,'come trattare gli altri', 'italiano', 'bompiani', 1985, 45);

insert into libro (isbn, titolo, lingua, editore, anno, copie)
values(0000001,'48 rules', 'italiano', 'monda', 1945, 35);


insert into categoria (id, nome)
values(00000, 'horror');

insert into categoria (id, nome)
values(00001, 'fantasy');

insert into categoria (id, nome)
values(00002, 'finanza');

insert into categoria (id, nome)
values(00003, 'romanzo');

insert into categoria (id, nome)
values(00004, 'giallo');

insert into categoria (id, nome)
values(00005, 'rosa');



insert into bridge_categoria (isbn_libro, id_categoria)
values(0000000, 00001);

insert into bridge_categoria (isbn_libro, id_categoria)
values(0000000, 00002);

insert into bridge_categoria (isbn_libro, id_categoria)
values(0000000, 00003);

