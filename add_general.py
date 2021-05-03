# -*- coding: utf-8 -*-
"""
Created on Thu Apr 29 09:16:21 2021

@author: JalexFollosco
"""
import oggetti as o
import os
import sqlite3

#CREAZIONE DB INIZIALE

db_filename = 'test1.db' # creo un secondo db solo per l'esempio poichè esiste giò chinook.sqlite

schema= 'biblioteca.sql'
dml = 'dml_biblioteca.sql'
schema_filename = os.path.abspath(schema)
dml_filename = os.path.abspath(dml)

db_is_new = not os.path.exists(db_filename)

with sqlite3.connect(db_filename) as conn:
    if db_is_new:
        print('Creazione dello schema')
        with open(schema_filename, 'rt') as f:
            schema = f.read()
        conn.executescript(schema)
        f.close()

        print('Inserimento dei dati di partenza')
        with open(dml_filename, 'rt') as g:
            schema_dml = g.read()
        conn.executescript(schema_dml)
        g.close()
                
    else:
        print('Il database esiste, si suppone che esista anche lo schema.')

     
# biblioteca funzione con sqlite

def esegui(conn, query, params=()):
    with conn:
        cur = conn.cursor()
        cur.execute(query, params)
        return cur.fetchall()
    
"""
Esegue una query usando la connessione conn, e ritorna la lista di risultati 
ottenuti. In params, possiamo mettere una lista di parametri per la query. 
"""

# estrae la colonna di una tabella e la mette in una lista
def estrazione(conn, tabella, colonna):
    zz = []
    estrai = f'SELECT {colonna} FROM {tabella}'
    tupla = esegui(conn, estrai)
    for estrai in tupla:         
        zz.append(estrai[0])
    return zz 

    
def add_general(oggetto):
    codice = id_generator(oggetto)
    
    query_utente = '''INSERT INTO utente (id_tessera, data_registrazione, nome, cognome, telefono, indirizzo, email) 
    values (?, ?, ?, ?, ?, ?, ?)'''
    query_categoria = '''INSERT INTO categoria (id, nome) values (?, ?)'''
    query_libro = '''INSERT INTO libro (isbn, titolo, lingua, editore, anno, copie)
    values (?, ?, ?, ?, ?, ?)'''
    query_autore = '''INSERT INTO autore (id, nome, cognome, data_nascita, luogo_nascita) 
    values (?, ?, ?, ?, ?)'''  # modificare schema sql.. aggiungere campo note.. , note
    
    if oggetto.__class__.__name__ == 'utente':
        esegui(conn, query_utente,(codice,oggetto.registrazione, oggetto.nome, oggetto.cognome, oggetto.telefono, oggetto.indirizzo, oggetto.email))
        
    elif oggetto.__class__.__name__ == 'str': 
        esegui(conn, query_categoria,(codice,oggetto))
        
    elif oggetto.__class__.__name__ == 'Libro':
        esegui(conn, query_libro,(oggetto.ISBN, oggetto.titolo, oggetto.lingua, oggetto.editore, oggetto.anno, oggetto.copie))
        link = '''INSERT INTO bridge_categoria (isbn_libro, id_categoria) 
        values (?, ?)''' 
        cat_id = []
        for c in oggetto.categoria:
            if c not in estrazione(conn, 'categoria', 'nome'):
                print(f'la categoria {c} non è presente nel db, creazione della nuova categoria in corso...')
                nuova_categoria = c
                key_id = id_generator(nuova_categoria) # crea nuova categor
                esegui(conn, query_categoria, (key_id, nuova_categoria))
                cat_id.append(key_id)
            else:
                fetch = esegui(conn,'SELECT id FROM categoria WHERE nome = :cat ', {'cat' : c}) # restituisce una tupla con solo gli id
                cat_id.append(fetch[0][0]) #estraggo il valore id dalla tupla
        for cod in cat_id:
            esegui(conn, link, (oggetto.ISBN,cod))
        link_autore = '''INSERT INTO bridge_autore (isbn_libro, id_autore) 
        values (?, ?)''' 
        aut_id = []
        for c in oggetto.autore:
            if (tuple(c.split())) not in esegui(conn, 'SELECT nome,cognome FROM autore'):
                 print(f'autore {c} non presente nel db, creazione del nuovo autore:\n')
                 new_autore = crea_autore()
                 autore_id = id_generator(new_autore)
                 esegui(conn, query_autore, (autore_id, new_autore.nome, new_autore.cognome, new_autore.data_nascita, new_autore.luogo_nascita)) # , oggetto.note
                 aut_id.append(autore_id)
            else:
                fetch1 = esegui(conn,'SELECT id FROM autore WHERE nome = :n and cognome = :cn ', {'n' : c.split()[0], 'cn' : c.split()[1]})
                aut_id.append(fetch1[0][0])
        for cod_autore in aut_id:
                esegui(conn, link_autore, (oggetto.ISBN,cod_autore))
            
    #MODIFICARE SCHEMA AUTORE aggiungere NOte 
    elif oggetto.__class__.__name__ == 'autore':
        esegui(conn, query_autore,(codice, oggetto.nome, oggetto.cognome, oggetto.data_nascita, oggetto.luogo_nascita)) # , oggetto.note
    conn.commit()
    return

def id_generator(oggetto): #autore, categoria, tessera(id utente)
    if oggetto.__class__.__name__ == 'utente':
        estrai = '''SELECT MAX(id_tessera) FROM utente;'''
    if oggetto.__class__.__name__ == 'str':
        estrai = '''SELECT MAX(id) FROM categoria;'''
    if oggetto.__class__.__name__ == 'Libro':
        estrai = '''SELECT MAX(id) FROM categoria;'''
    if oggetto.__class__.__name__ == 'autore':
        estrai = '''SELECT MAX(id) FROM autore;'''
    x = esegui(conn, estrai)
    idd = x[0][0] + 1
    print('codice id è: ',idd)
    return idd 
    
def delete_general(row, table):
    if table == 0:
        cancella = '''DELETE FROM categoria WHERE nome = :category '''
        esegui(conn, cancella, {"category" :row})
    elif table == 1:
        cancella = '''DELETE FROM utente WHERE id_tessera = :userid '''
        esegui(conn, cancella, {"userid" :row})
    elif table == 2:
        cancella = '''DELETE FROM libro WHERE isbn = :id ''' 
        esegui(conn, cancella, {"id" :row})
    conn.commit()
    pass

def delete_categoria(categoria): #IMPLEMENTARE LA CANCELLAZIONE A CASCATA e CANCELAZIONE IN BRIDGE_CATEGORIA
    print('cancella una delle seguenti categorie:\n')
    print(estrazione(conn, 'categoria', 'nome'))
    canc = input('...') #CONTROLLARE CHE L'INPUT SIA GIUSTO SE NO NON CANCELLA NULLA
    cancella = '''DELETE FROM categoria WHERE nome = :category ''' 
    id_canc = esegui(conn, 'SELECT id FROM categoria WHERE nome = :category', {"category" :canc})
    esegui(conn, cancella, {"category" :canc})
    conn.commit()
    return id_canc #[(11,)] cancellare in brifge_categoria

def delete_utente(id_tessera, data_registrazione, nome, cognome, data, tel, indirizzo, email):
    print('cancella uno dei seguenti utenti, inserisci ID associato:\n')
    print(estrazione(conn, 'utente', 'id_tessera'))
    canc = input('...') #CONTROLLARE CHE L'INPUT SIA GIUSTO SE NO NON CANCELLA NULLA
    cancella = '''DELETE FROM utente WHERE id_tessera = :userid ''' 
    esegui(conn, cancella, {"userid" :canc})
    conn.commit()
    return 

def delete_libro(isbn, titolo, lingua, editore, anno, copie):
    print('cancella uno dei seguenti libri, inserisci ID associato:\n')
    print(estrazione(conn, 'libro', 'titolo'))
    print(estrazione(conn, 'libro', 'isbn'))
    canc = input('...') #CONTROLLARE CHE L'INPUT SIA GIUSTO SE NO NON CANCELLA NULLA
    cancella = '''DELETE FROM libro WHERE isbn = :id ''' 
    esegui(conn, cancella, {"id" :canc})
    conn.commit()
    return  
        
#cancellare la categoria e utente solo se non ha associato un libro
    

#controllo cancella categoria, non cancella se la categoria è attribuita ad un libro
canc_categ = input('inserisci la categoria da cancellare')
if canc_categ in estrazione(conn, 'categoria', 'nome'):
    #if
    pass





   
   
#script per inserirlo dento l'oggetto libro..  
def crea_autore():
    print('inserisci un nuovo autore:')
    nome = (input('nome:'))
    cognome = input('cognome:')
    data_nascita = input('data di nascita:') 
    luogo_nascita = input('luogo di nascita')
    note = (input('note (descrizione):'))
    autore = o.autore(nome, cognome, data_nascita, luogo_nascita, note)
    return autore

def create_libro():
    print('inserisci un nuovo libro:')
    isbn = int(input('isbn:'))
    titolo = input('titolo:')
    lingua = input('lingua:') 
    editore = input('editore')
    anno = int(input('anno:'))
    copie = int(input('numero copie:'))
    cat_libro = []
    while True:
        cat_libro.append(input('inserisci categoria: '))
        x = input('desideri inserire altre categorie? s/n')
        if x == 's':
            continue
        else: break
    aut_libro = []
    while True:
        aut_libro.append(input('inserisci autore/i: '))
        y = input('questo libro ha più di un autore? s/n')
        if y == 's':
            continue
        else: break
    libro = o.Libro(isbn,titolo, lingua,aut_libro, editore, anno, copie, cat_libro)
    return libro 
#test = create_libro()
#add_general(test)





'''
while True:
        autore = (input('inserisci autore/i: '))
        if tuple(autore.split()) in esegui(conn, 'SELECT nome,cognome FROM autore'):
            print('questo autore risulta già nel db.. OK')
            #collegamento autore-libro
        else:
            print('autore non presente nel db')
            new_autore = crea_autore()
            add_general(new_autore)
        aut_libro.append(autore)
        y = input('questo libro ha più di un autore? s/n')
        if y == 's':
            continue
        else: break
'''


#FUNZIONE RICERCA METTERLO IN UN OGGETTO PER LA VISUALIZZAZIONE
ricerca=input('seleziona isbn')
concat = '''SELECT libro.isbn, libro.titolo, libro.anno, libro.copie, libro.editore, libro.lingua,group_concat(categoria.nome)
FROM libro
join bridge_categoria ON libro.isbn = bridge_categoria.isbn_libro
join categoria ON categoria.id = bridge_categoria.id_categoria
WHERE libro.isbn = :filtro
group by libro.isbn '''

print(esegui(conn, concat, {'filtro': ricerca}))


        