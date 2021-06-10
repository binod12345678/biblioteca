# -*- coding: utf-8 -*-
"""
Created on Thu Apr 29 09:16:21 2021

@author: JalexFollosco
"""
#import oggetti as o
#import datetime

#CREAZIONE DB INIZIALE





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
 
def add_general(conn,oggetto):
    codice = id_generator(conn, oggetto)
    
    query_utente = '''INSERT INTO utente (id_tessera, data_registrazione, nome, cognome, telefono, indirizzo, email) 
    values (?, ?, ?, ?, ?, ?, ?)'''
    query_categoria = '''INSERT INTO categoria (id, nome) values (?, ?)'''
    query_libro = '''INSERT INTO libro (isbn, titolo, lingua, editore, anno, copie)
    values (?, ?, ?, ?, ?, ?)'''
    query_autore = '''INSERT INTO autore (id, nome, cognome, data_nascita, luogo_nascita, note) 
    values (?, ?, ?, ?, ?, ?)'''  
    
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
                key_id = id_generator(conn, nuova_categoria) # crea nuova categor
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
                 autore_id = id_generator(conn, new_autore)
                 esegui(conn, query_autore, (autore_id, new_autore.nome, new_autore.cognome, new_autore.data_nascita, new_autore.luogo_nascita, new_autore.note)) 
                 aut_id.append(autore_id)
            else:
                fetch1 = esegui(conn,'SELECT id FROM autore WHERE nome = :n and cognome = :cn ', {'n' : c.split()[0], 'cn' : c.split()[1]})
                aut_id.append(fetch1[0][0])
        for cod_autore in aut_id:
                esegui(conn, link_autore, (oggetto.ISBN,cod_autore)) 
    elif oggetto.__class__.__name__ == 'autore':
        esegui(conn, query_autore,(codice, oggetto.nome, oggetto.cognome, oggetto.data_nascita, oggetto.luogo_nascita, oggetto.note)) 
    conn.commit()
    return

def id_generator(conn,oggetto): #autore, categoria, tessera(id utente)
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
    
def delete_general(conn,row, table):
    if table == 0:
        lista_categorie= esegui(conn, 'select * from categoria')
        for i in range(len(lista_categorie)):
            if row == lista_categorie[i][1]:
                id_categoria = lista_categorie[i][0]
        if id_categoria not in estrazione(conn, 'bridge_categoria', 'id_categoria'):
            cancella = '''DELETE FROM categoria WHERE nome = :category '''
            esegui(conn, cancella, {"category" :row})
            print('la categoria seguente è stata cancellata')
        else:
            print('la categoria seguente non può essere cancellata, perchè asoociata a uno o più libri')
    elif table == 1:
        check_prestito= 'SELECT tessera_id FROM prestito WHERE data_restituzione is NULL AND tessera_id = :tessera'
        if len(esegui(conn, check_prestito, {'tessera':row})) > 0:
            print('L utente non può essere cancellata, perchè asoociata a uno o più libri in prestito')
        else:
            print('canccellato')
            cancella = '''DELETE FROM utente WHERE id_tessera = :userid '''
            esegui(conn, cancella, {"userid" :row}) ## cancellare solo se non ha libri in prestito non restituite
    elif table == 2:
        check_prestito= 'SELECT isbn_libro FROM prestito WHERE data_restituzione is NULL AND isbn_libro = :isbn'
        if len(esegui(conn, check_prestito, {'isbn':row})) > 0:
            print('Libro non può essere cancellato, perchè asoociata a uno o più utenti che l hanno preso in prestito')
        else:
            print('canccellato')
            cancella = '''DELETE FROM libro WHERE isbn = :isbn ''' #cancellare libro solo se non è in prestito da un utente
            esegui(conn, cancella, {"isbn" :row})
            cascade_categoria= '''DELETE FROM bridge_categoria WHERE isbn_libro = :isbn '''
            esegui(conn, cascade_categoria, {"isbn" :row})
            cascade_autore = '''DELETE FROM bridge_autore WHERE isbn_libro = :isbn '''
            esegui(conn, cascade_autore, {"isbn" :row})
            cascade_prestito = '''DELETE FROM prestito WHERE isbn_libro = :isbn '''
            esegui(conn, cascade_prestito, {"isbn" :row})
    conn.commit()
    return


    

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
#test = create_libro()
#add_general(test)





#FUNZIONE RICERCA METTERLO IN UN OGGETTO PER LA VISUALIZZAZIONE

def ricerca_libro (conn,ricerca):

    concat = '''SELECT libro.isbn, libro.titolo, libro.lingua, libro.editore, libro.anno, libro.copie, group_concat(distinct categoria.nome), group_concat(distinct autore.cognome)
                FROM libro
                join bridge_categoria ON libro.isbn = bridge_categoria.isbn_libro
                join categoria ON categoria.id = bridge_categoria.id_categoria
                join bridge_autore ON libro.isbn = bridge_autore.isbn_libro
                join autore ON autore.id = bridge_autore.id_autore
                WHERE libro.isbn = :filtro
                group by libro.isbn '''
    cursor = conn.cursor()
    cursor.execute(concat, {'filtro': ricerca})
    isbn, titolo, lingua, editore, anno, copie, categorie, autori = cursor.fetchone()
    libro = o.Libro(isbn,titolo, lingua,autori, editore, anno, copie, categorie)
    return libro 

'''
ricerca = int(input('inserisci l ISBN del libro che stai cercando'))
if ricerca in estrazione(conn, 'libro', 'isbn'):
   view = ricerca_libro(ricerca)
   print(view.__dict__)
else:
    print('questo libro non è presente nel db, oppure hai inserito un isbn errato')
'''
#DATETIME 
#import datetime
#now = datetime.date.today()
#scadenza = now + datetime.timedelta(days = 30)
# cc= '2000-05-26'
#date_format= datetime.datetime.strptime(cc, "%Y-%m-%d").date()



        
        
#PRESTITO
'''

 

V2

while True:
    try:
        libro_isbn = int(input('inserisci isbn libro'))
        if libro_isbn in sql.estrazione(conn, 'libro', 'isbn'):
            libro = sql.ricerca_libro(conn,libro_isbn)
            if libro.copie > 0:
                break
            else:
                print('questo libro non è disponibile al prestito, scegliere un altro libro')
                continue
        else:
            print('questo isbn non è presente nel db o hai digitato male.')
            continue
    except ValueError:
        continue
    
while True:
    try:
        utente = int(input('inserisci il numero di tessera dell utente'))
        if utente in estrazione(conn, 'utente', 'id_tessera'):
            break
    except ValueError:
        continue
  


isbn_utente = tuple((utente, libro.ISBN))
if isbn_utente in ricerca_prestito(conn, utente):
    print('l\' utente ha già in prestito questo libro')
else:
    prestito(conn, libro, utente)



'''





#check_ritardi_pandas = pd.read_sql_query
#('SELECT data_prestito FROM prestito WHERE data_restituzione is NULL AND 
#tessera_id = :tessera',conn, params= {'tessera' :0})
# check_ritardi_pandas.values.tolist()

'''
#visualizzazione di una lista di libri  
lista_libri = [9788854171633, 9788831003445, 4165472289563]

for i in lista_libri:
    oggetti_libri.append(sql.ricerca_libro(conn, i))
    
oggetti_libri = []
for x in oggetti_libri:
    print(x.__dict__)
    
#Utilizzare pandas
'''

'''
#UPDATE COPIE
isbn = 12345678910123
libro = ricerca_libro(conn,isbn)
update_copie = 'UPDATE libro SET copie = :n_copie WHERE isbn = :filtro'
esegui(conn, update_copie, {'n_copie': libro.copie, 'filtro': isbn})
'''

import datetime

def restituzione(conn, libro, utente):
    update_copie = '''UPDATE libro SET copie = :n_copie WHERE isbn = :filtro'''
    esegui(conn, update_copie, {'n_copie': libro.copie+1, 'filtro': libro.ISBN})
    riconsegna = datetime.date.today()
    query = '''UPDATE prestito SET data_restituzione = :data 
    WHERE isbn_libro = :filtro AND tessera_id = :filtro2 '''
    esegui(conn, query, {'data': riconsegna, 'filtro': libro.ISBN, 'filtro2': utente})
    conn.commit()
    return

#RESTITUZIONE

def ricerca_prestito(conn, utente):
    query='SELECT tessera_id, isbn_libro FROM prestito WHERE data_restituzione is NULL AND tessera_id = :tessera'
    x = sql.esegui(conn, query, {'tessera':utente})
    return x


'''
while True:
    
    try:
        libro_isbn = int(input('inserisci l isbn del libro da riconsegnare'))
        if libro_isbn in sql.estrazione(conn, 'prestito', 'isbn_libro'):
            libro = ricerca_libro(conn,libro_isbn)
            break
        else:
            print('questo libro non risulta nei prestiti')
            continue
    except ValueError:
        continue

while True:
    try:
        utente = int(input('inserisci il numero di tessera dell utente'))
        if utente in sql.estrazione(conn, 'prestito', 'tessera_id'):
            break
        else:
            print('numero di tessera inesistente')
            continue
    except ValueError:
        continue
    
isbn_utente = tuple((utente, libro_isbn))
if isbn_utente in ricerca_prestito(conn, utente):
    print('esiste la coppia')
    restituzione(conn,libro, utente)
else:
    print('non esiste questa coppia')

'''

def update_libroDB(conn, libro, campo, valore):
    query= '''UPDATE libro SET {campo} = :valore WHERE isbn = :filtro '''
    sql.esegui(conn, query, {'valore': valore, 'filtro': libro})
    conn.commit()
    return


