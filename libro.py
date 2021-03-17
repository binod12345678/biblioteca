

class Libro:
    
    def __init__ (self,ISBN = "", titolo = "", lingua = "", autore = "", editore = "", anno = "",  pagine = "", categoria = ""):
        
        self.ISBN = ISBN
        self.titolo = titolo
        self.lingua = lingua
        self.autore = autore
        self.editore = editore
        self.anno = anno
        self.pagine = pagine
        self.categoria = categoria
        
        
    def titolook (self, titolo):
        if(type (titolo) is str):
            self.titolo = titolo
        else:
            print("non è una stringa")
        
    def autoreok (self, autore):
        if(type (autore) is str):
            self.autore = autore
        else:
            print("non è una stringa")
        
    def editoreok (self, editore):
        if(type (editore) is str):
            self.editore = editore
        else:
            print("non è una stringa")
        
    def n_pagine (self):
        return (self.pagine > 10)
        
    def info(self):
        print(self.titolo)
        print(self.autore)
        print(self.editore)
        print(self.pagine)
        print(self.categoria)