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
    query_autore = '''INSERT INTO autore (id, nome, cognome, , data_nascita, luogo_nascita, note)
    values (?, ?, ?, ?, ?, ?)'''  # modificare schema sql.. aggiungere campo note..
    
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
            
    #MODIFICARE SCHEMA AUTORE    
    elif oggetto.__class__.__name__ == 'autore':
        esegui(conn, query_autore,(oggetto.nome, oggetto.cognome, oggetto.data_nascita, oggetto.luogo_nascita, oggetto.note))
        link = '''INSERT INTO bridge_autore (isbn_libro, id_autore) 
        values (?, ?)''' 
        aut_id = []
        for c in oggetto.autore:
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
        pass
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
    
        
        

    






   
   
#script per inserirlo dento l'oggetto libro..  

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
autore = input('autore:')
libro = o.Libro(isbn,titolo, lingua,autore, editore, anno, copie, cat_libro)
add_general(libro)