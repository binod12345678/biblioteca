# -*- coding: utf-8 -*-
"""
Created on Sat May 15 15:03:52 2021

@author: JalexFollosco
"""

import main as m
import query_sql as sql


def MenuRicerca(conn):
    
    simboli = [0, 1, 2, 3]
    
    print('\n\n\n|--------**{   MENU\' RICERCA   }**--------|')
    print('|                            |          |')
    print('|-Torna al Menù principale   |-> press 0|')
    print('|-Ricerca Libro              |-> press 1|')
    print('|-Ricerca prestiti           |-> press 2|')
    print('|-Ricerca prestiti in ritardo|-> press 3|')
    print('|                            |          |')
    print('|---------------------------------------|\n')
    
    while True:
        try:
            scelta = int(input('Premi per scegliere: '))
            if scelta in simboli:
                break
        except ValueError:
            continue
        
    if scelta == 1:
        RicercaLibro(conn)
        MenuRicerca(conn)
    elif scelta == 2:
        RicercaPrestiti(conn)
        MenuRicerca(conn)
    elif scelta == 3 :
        RicercaRitardi(conn)
        MenuRicerca(conn)
    elif scelta == 0:
        m.Menu(conn)
        
        

def RicercaLibro(conn):
    while True:
        
        try:
            ricerca = int(input('inserisci l\' ISBN del libro che stai cercando: '))
            if ricerca in sql.estrazione(conn, 'libro', 'isbn'):
               libro = sql.ricerca_libro(conn, ricerca)
               libro.view()
               break
            else:
                print('questo libro non è presente nel db')
                
        except ValueError:
            continue
        
        return
        

def RicercaPrestiti(conn):
    while True:
        
        try:
            utente = int(input('inserisci il numero di tessera dell utente'))
            if utente in sql.estrazione(conn, 'utente', 'id_tessera'):
                prestiti = sql.ricerca_prestito(conn, utente)
                isbn = []
                libri = []
                for i in prestiti:
                    isbn.append(i[1])
                for j in isbn:
                    libro = sql.ricerca_libro(conn, j)
                    libri.append(libro)
                for k in libri:
                    k.view()
                if len(isbn) == 0:
                    print('L\'utente non ha libri in prestito')
                break
        except ValueError:
            continue
    
    return
        
def RicercaRitardi(conn):
    while True:
        
        try:
            utente = int(input('inserisci il numero di tessera dell utente'))
            if utente in sql.estrazione(conn, 'utente', 'id_tessera'):
                ritardi = sql.ritardi(conn, utente)
                if len(ritardi) > 0:
                    libri = []
                    for j in ritardi:
                        libro = sql.ricerca_libro(conn, j)
                        libri.append(libro)
                    for k in libri:
                        k.view()
                else:
                    print('L\'utente non ha prestiti in ritardo')
                break
        except ValueError:
            continue
    
    return
            
        
        
#--------TEST-----
if __name__ == '__main__':
    conn = sql.createDb()
    MenuRicerca(conn)