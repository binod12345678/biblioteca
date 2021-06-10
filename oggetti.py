# -*- coding: utf-8 -*-
"""
Created on Thu Apr 29 09:19:42 2021

@author: JalexFollosco
"""

class persona: #classe padre
    
  def __init__(self, nome = "", cognome = "", eta =""):
        self.nome = nome
        self.cognome = cognome
        
          
            

        
class utente(persona): #classe figlie
    profilo = "utente"

    def __init__(self, nome, cognome, registrazione, telefono, email, indirizzo, numero_tessera = ''):
        super().__init__(nome, cognome)
        self.numero_tessera = numero_tessera
        self.registrazione = registrazione
        self.telefono = telefono
        self.email = email
        self.indirizzo = indirizzo
        
class autore(persona): #classe figlie
    profilo = "autore"     

    def __init__(self, nome, cognome, data_nascita, luogo_nascita, note= ''): 
        super().__init__(nome, cognome)
        self.data_nascita = data_nascita 
        self.luogo_nascita = luogo_nascita 
        self.note = note
        
        
class Libro:
    
    def __init__ (self,ISBN = "", titolo = "", lingua = "", autore = "", editore = "", anno = "",  copie = "", categoria = ""):
        
        self.ISBN = ISBN
        self.titolo = titolo
        self.lingua = lingua
        self.editore = editore
        self.anno = anno
        self.categoria = categoria
        self.copie = copie
        self.autore = autore
        
    def view(self):
        print('\n\nISBN: ', self.ISBN)
        print('Titolo: ', self.titolo)
        print('Lingua: ', self.lingua)
        print('Editore: ', self.editore)
        print('Anno: ', self.anno)
        print('Categoria: ', self.categoria)
        print('Copie: ', self.copie)
        print('Autore: ',self.autore)
        
     
