

import persona


print('sei il bibliotecario?')

n ='0'
while n =='0':
    print("Digita un numero per eseguire una funzione:")
    print("1 --> Per la funzione che stampa a video i numeri pari e dispari di una lista")
    print("2 --> Per la funzione che stampa a video i numeri max, min e media di una lista")
    print("3 --> Per la funzione che stampa a video i la potenza tra due numeri")
    print("4 per interrompere il programma")
    
    n = input ("Digita il numero corrispondente all'operazione che vuoi fare : ")
    
    if n == "1":
        funzione1() 
    elif n == "2":
        funzione2()
    elif n == "3":
        funzione3()
    elif n == "4":
        exit()
    else:
     print("il numero inserito per eseguire una delle funzioni non è valido!")