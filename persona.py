class persona: 

     

  def __init__(self, nome = "", cognome = "", eta =""): 

        self.nome = nome 

        self.cognome = cognome 

        self.eta = eta 

           



class utente(persona): 

    profilo = "utente" 

  

    def __init__(self, nome, cognome, eta, residenza, numero_tessera, registrazione, telefono, email, indirizzo): 

        super().__init__(nome, cognome, eta) 

        self.residenza = residenza 

        self.numero_tessera = numero_tessera 

        self.registrazione = registrazione 

        self.telefono = telefono 

        self.email = email 

        self.indirizzo = indirizzo 



class bibliotecario(persona): 

    profilo = "bibliotecario" 

     

    def __init__(self, nome, cognome, eta, numero_tessera, telefono, email, indirizzo): 

        super().__init__(nome, cognome, eta) 

        self.numero_tessera = numero_tessera 

        self.numero_tessera = numero_tessera 

        self.email = email 

        self.indirizzo = indirizzo 

         

class autore(persona): 

    profilo = "autore"     

     

    def __init__(self, nome, cognome, eta, data_nascita, luogo_nascita): 

        super().__init__(nome, cognome, eta) 

        self.data_nascita = data_nascita 

        self.luogo_nascita = luogo_nascita 
        
    def info (self): 
        print(self.nome)
        print(self.cognome)
        print(self.eta)
        print(self.data_nascita)
        print(self.luogo_nascita)
        
        
        
        
        
        
        
        
        
        
        
      