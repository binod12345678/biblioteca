
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
    


def add_categoria(categoria): #implementare controllo degli errori: CONTROLLO DELLE CATEGORIE SE CI SONO
    estrai = '''SELECT MAX(id) FROM categoria;'''
    x = esegui(conn, estrai) # tupla contenente id max
    codice = x[0][0] + 1 #estraggo il numero dalla tupla e sommo per creare la chiave
    print('ultimo codice id è: ',codice)
    inserisci = '''INSERT INTO categoria (id, nome)
    values (?, ?)'''
    esegui(conn, inserisci,(codice,categoria))
    conn.commit()
    return  codice

def delete_categoria(): #IMPLEMENTARE LA CANCELLAZIONE A CASCATA e CANCELAZIONE IN BRIDGE_CATEGORIA
    print('cancella una delle seguenti categorie:\n')
    print(estrazione(conn, 'categoria', 'nome'))
    canc = input('...') #CONTROLLARE CHE L'INPUT SIA GIUSTO SE NO NON CANCELLA NULLA
    cancella = '''DELETE FROM categoria WHERE nome = :category ''' 
    id_canc = esegui(conn, 'SELECT id FROM categoria WHERE nome = :category', {"category" :canc})
    esegui(conn, cancella, {"category" :canc})
    conn.commit()
    return id_canc #[(11,)] cancellare in brifge_categoria

def add_utente(): #IMPLEMENTARE LA GESTIONE ERRORI
    print('inserisci un nuovo utente')
    nome = input('nome: ')
    cognome = input('cognome: ')
    data = input('data registrazione: ')
    tel = input('telefono: ')
    email = input('email: ')
    indirizzo = input('indirizzo: ')
    estrai = '''SELECT MAX(id_tessera) FROM utente;'''
    u = esegui(conn, estrai) # tupla contenente id max
    codice = u[0][0] + 1 #estraggo il numero dalla tupla e sommo
    print('ultimo codice id è: ',codice) # IL CODICE ID SI CHIEDE IN INPUT , DA FARE
    inserisci = '''INSERT INTO utente (id_tessera, data_registrazione, nome, cognome, telefono, indirizzo, email)
    values (?, ?, ?, ?, ?, ?, ?)'''
    esegui(conn, inserisci,(codice, data, nome, cognome, tel, indirizzo, email))
    conn.commit()
    return 

def delete_utente():
    print('cancella uno dei seguenti utenti, inserisci ID associato:\n')
    print(estrazione(conn, 'utente', 'id_tessera'))
    canc = input('...') #CONTROLLARE CHE L'INPUT SIA GIUSTO SE NO NON CANCELLA NULLA
    cancella = '''DELETE FROM utente WHERE id_tessera = :userid ''' 
    esegui(conn, cancella, {"userid" :canc})
    conn.commit()
    return 

def add_libro(): #CONTROLLO DEL isbn SE CI SONO gia
    print('inserisci un nuovo libro:')
    isbn = int(input('isbn:'))
    titolo = input('titolo:')
    lingua = input('lingua:') 
    editore = input('editore')
    anno = input('anno:')
    copie = int(input('numero copie:'))
    query = '''INSERT INTO libro (isbn, titolo, lingua, editore, anno, copie)
    values (?, ?, ?, ?, ?, ?)'''
    esegui(conn, query,(isbn, titolo, lingua, editore, anno, copie))
    cat_libro = []
    while True:
        cat_libro.append(input('inserisci categoria: '))
        x = input('desideri inserire altre categorie? s/n')
        if x == 's':
            continue
        else: break
    cat_id = []
    for c in cat_libro:
        if c not in estrazione(conn, 'categoria', 'nome'):
            print(f'la categoria {c} non è presente nel db, creazione della nuova categoria in corso...')
            nuova_categoria = c
            key_id = add_categoria(nuova_categoria) 
            cat_id.append(key_id)
        else:
            fetch = esegui(conn,'SELECT id FROM categoria WHERE nome = :cat ', {'cat' : c}) # restituisce una tupla con solo gli id
            cat_id.append(fetch[0][0]) #estraggo il valore id dalla tupla
    #BRIDGE_CATEGORIA collegamento tra libro e la categoria/e associate
    link = '''INSERT INTO bridge_categoria (isbn_libro, id_categoria) 
    VALUES (?, ?)''' 
    for cod in cat_id:
        esegui(conn, link, (isbn,cod))
    conn.commit()
    return
   # categoria = input('categoria') # IMPLEMENTARE CATEGORIE MULTIPLE
   
def delete_libro():
    print('cancella uno dei seguenti libri, inserisci ID associato:\n')
    print(estrazione(conn, 'libro', 'titolo'))
    print(estrazione(conn, 'libro', 'isbn'))
    canc = input('...') #CONTROLLARE CHE L'INPUT SIA GIUSTO SE NO NON CANCELLA NULLA
    cancella = '''DELETE FROM libro WHERE isbn = :id ''' 
    esegui(conn, cancella, {"id" :canc})
    conn.commit()
    return  #IMPLEMENTARE LA CANCELLLAZIONE A CASCATA IN BRIDGE_CATEGORIA
   
   
    
'''ERA IN DELETE_CATEGORIA() DOPO LA PRINT
    estrai = SELECT nome FROM categoria;
    y = esegui(conn, estrai) # tupla contenente le categorie
    for categoria in y:         #stampo a video le categorie
        print(categoria[0])     #SOSTITUIRE CON LA FUNZIONE ESTRAZIONE()  
'''
 

#cancellare la categoria solo se non ha associato un libro 
#ricerca prestiti cliente e visualizzazione cliente 
    
print("Inserisci il numero corrispondente la funzione che vuoi svolgere: {}" .format(__name__))
'''
def estrazione(conn, tabella, colonna):
   print("è in esecuzione la funzione 1")

def add_categoria(categoria):
   print("è in esecuzione la funzione 2")  

def delete_categoria(categora):
   print("è in esecuzione la funzione 3")

def add_utente():
   print("è in esecuzione la funzione 4")
   
def delete_utente():
   print("è in esecuzione la funzione 5")
   
def add_libro():
   print("è in esecuzione la funzione 6")

def delete_libro():
   print("è in esecuzione la funzione 7")
'''
if __name__ == "__main__":
    num = input("metti un numero:\n")
    schema= 'biblioteca.sql'
    dml = 'dml_biblioteca.sql'
    schema_filename = os.path.abspath(schema)
    dml_filename = os.path.abspath(dml)
    print(schema_filename)
    conn = sqlite3.connect("./test1.db")
    tabella = "categoria"
    colonna = "id"
    if num == "1":
        estrazione(conn, tabella, colonna)
        pass

    if num == "2":
        categoria = "drama"
        add_categoria(categoria)
        pass

    if num == "3":
        delete_categoria()
        pass

    if num == "4":
        add_utente()
        pass

    if num == "5":
        delete_utente()
        pass

    if num == "6":
        add_libro()
        pass

    if num == "7":
        delete_libro()
        pass

else:
   print("******* IL COMANDO INSERITO NON E' VALIDO*******") 
