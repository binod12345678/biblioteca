# -*- coding: utf-8 -*-
"""
Created on Fri May  7 13:45:29 2021

@author: JalexFollosco
"""

#MAIN

import oggetti as o
import query_sql as sql
import sqlite3
import os

 
db_filename = 'bibliotecatest01.db' # creo un secondo db solo per l'esempio poichè esiste giò chinook.sqlite

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
  

#controllo cancella categoria, non cancella se la categoria è attribuita ad un libro
'''
canc_categ = input('inserisci la categoria da cancellare')
if canc_categ in estrazione(conn, 'categoria', 'nome'):
    delete_general(canc_categ, 0)
else:
    print('questa categoria non esiste')
'''
#CONTROLLO ADD_AUTORE 
'''
canc_utente = int(input('inserisci il numero di tessera dell utente da cancellare'))
if canc_utente in estrazione(conn, 'utente', 'id_tessera'):
    delete_general(canc_utente, 1)
else:
    print('questo utente non è presente nel db, oppure hai inserito un id errato')
'''

#CONTROLLO ADD_LIBRO CANCELLA IL LIBRO SOLO SE NON è PRESENTE NELLA TABELLA PRESTITO
'''
canc_libro = int(input('inserisci l ISBN del libro da cancellare'))
if canc_libro in estrazione(conn, 'libro', 'isbn'):
    delete_general(canc_libro, 2)
else:
    print('questo libro non è presente nel db, oppure hai inserito un isbn errato')
 '''  
  #cancella autore
'''
canc_autore = input('inserisci l autore da cancellare')
canc_autore = canc_autore.split()
if tuple(canc_autore) in sql.esegui(conn, 'select nome, cognome from autore'):
    print('cancella')
else:
    print('questo autore non è presente nel db')
    '''
 
#RICERCA 
'''
ricerca = int(input('inserisci l ISBN del libro che stai cercando'))
if ricerca in estrazione(conn, 'libro', 'isbn'):
   view = ricerca_libro(ricerca)
   print(view.__dict__)
else:
    print('questo libro non è presente nel db, oppure hai inserito un isbn errato')
'''

def crea_autore():
    print('inserisci un nuovo autore:')
    nome = (input('nome:'))
    cognome = input('cognome:')
    data_nascita = input('data di nascita:') 
    luogo_nascita = input('luogo di nascita')
    note = (input('note (descrizione):'))
    autore = o.autore(nome, cognome, data_nascita, luogo_nascita, note)
    return autore

def crea_utente():
    print('inserisci un nuovo utente:')
    nome = (input('nome:'))
    cognome = input('cognome:')
    registrazione = input('data registrazione') #now = datetime.date.today()
    telefono = input('telefono:') 
    email = (input('email:'))
    indirizzo = (input('indirizzo:'))
    utente = o.utente(nome, cognome, registrazione, telefono, email, indirizzo, numero_tessera = '')
    return utente

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

#------------TEST---------------
x = sql.estrazione(conn, 'libro','titolo')
c = create_libro()
sql.add_general(conn, c)

#GESTIONE DEGLI ERRORI CATEGORIA
'''
while True:
    try:
        nuova_cat = input('inserisci nuova categoria')
        sql.add_general(conn,nuova_cat)
        break
    except sqlite3.IntegrityError:
        print('hai inserito una categoria già esistente')
'''