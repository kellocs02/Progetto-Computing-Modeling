import random  #random restituisce un numero casuale tra 0 e 1
import math
import variabili2
import time
#Fase 1 implementare Poisson
#il tempo medio tra due arrivi è di 1.6 minuti, gli intervalli di tempo
#tra due arrivi consecutivi sono casuali, indipendenti, distribuiti in modo esponenziale
#con media 1.6 minuti.
#Bisogna generare un numero casuale che rappresenti il tempo di attesa fino
#al prossimo arrivo, può esser piccolo o grande, lo chiamiamo Delta_T, in media vale 1.6
# in questo modo la prossima richiesta arriva a (t+Delta_T)
#Con un processo di Poisson non genero arrivi,
#genero tempi di attesa tra un arrivo e il successivo.

#prova progetto 2 bisogna implementare la coda di arrivi
#
def Poisson():
    return  -math.log(1 - random.random()) / variabili2.V_Lambda

def EsecuzioneDelServizio1():
    variabili2.coda1.pop(0)
    variabili2.N1-=1 #decrementiamo il valore della coda
    variabili2.completati_N1+=1
    variabili2.fine_occupato=variabili2.tempo

def EsecuzioneDelServizio2():
    variabili2.coda2.pop(0)
    variabili2.N2-=1
    variabili2.completati_N2+=1
    variabili2.fine_occupato=variabili2.tempo


def GenerazioneTempoServizio1():
    print("Generazione del tempo di servizio per la richiesta nella coda 1\n")
    tempo_servizio_1 = -math.log(1 - random.random()) / variabili2.Durata_Media_Del_Serviziop_N1 #decidiamo quanto durerà l'esecuzione del servizio in base al dato fornito
    variabili2.tempo_fine_servizio=tempo_servizio_1+variabili2.tempo
    variabili2.stato=1
    variabili2.inizio_occupato=variabili2.tempo

def GenerazioneTempoServizio2():
    print("Generazione del tempo di servizio per la richiesta nella coda 2\n")
    tempo_servizio_2 = -math.log(1 - random.random()) / variabili2.Durata_Media_Del_Serviziop_N2
    variabili2.tempo_fine_servizio=tempo_servizio_2+variabili2.tempo
    variabili2.stato=2
    variabili2.inizio_occupato=variabili2.tempo

def EstrazioneCasuale():
    if random.random() <=0.50:
        GenerazioneTempoServizio1()
    else:
        GenerazioneTempoServizio2()

def EsecuzioneCasualeCode():
    if(variabili2.N1!=0 and variabili2.N2!=0): #nel caso in cui in entrambe le code vi siano delle richieste
        EstrazioneCasuale()
    elif(variabili2.N1!=0 and variabili2.N2==0): #caso in cui nella coda 1 vi sono richieste ma non nella coda 2
        GenerazioneTempoServizio1()
    else:
        GenerazioneTempoServizio2()

def main():
    print("Progetto Computing Modeling / Professor. Scarpa / Studente Alberto Paludetti")
    i=0 #Generiamo la prima richiesta in arrivo (Quando arriverà)
    while(i<100000):
        delta_t = Poisson()
        print("delta-T Inizio while : ",delta_t)
        variabili2.prossimo_arrivo=variabili2.tempo+delta_t #calcoliamo quando arriverà la prossima richiesta
        print("prossimo_arrivo : ",variabili2.prossimo_arrivo)
        print("tempo fine servizio : ", variabili2.tempo_fine_servizio)
        if(variabili2.prossimo_arrivo < variabili2.tempo_fine_servizio or variabili2.tempo_fine_servizio==0):#verifichiamo quale evento si svolgerà prima 
            variabili2.tempo_precedente=variabili2.tempo #salviamo il tempo dell'ultimo evento
            variabili2.tempo=variabili2.prossimo_arrivo #aumentiamo il tempo del sistema
            variabili2.area+=(variabili2.N1+variabili2.N2+(1 if variabili2.stato !=0 else 0)) * (variabili2.tempo-variabili2.tempo_precedente) 
            print("N1-> ",variabili2.N1)
            variabili2.area_coda1[variabili2.N1-1]+=variabili2.tempo-variabili2.tempo_precedente
            variabili2.area_coda2[variabili2.N2-1]+=variabili2.tempo-variabili2.tempo_precedente
            print("Arrivo di una nuova richiesta al tempo ", variabili2.tempo)
            tipo_Di_richiesta=random.random() #generiamo un numero casuale che utilizziamo per decidere di che tipo è la richiesta (sotto il 75 sarà di tipo 2, altrimenti di tipo 1)
            if(tipo_Di_richiesta<=0.75):
                print("Richiesta di tipo 2,\nControllo Spazio nella coda\n")
                variabili2.arrivi_N2+=1 #aumentiamo il valore di arrivi che tiene il conto del numero di richieste arrivate nel sistema
                if(variabili2.N2<12):   
                    print("Spazio disponibile, aggiunta della richiesta nella coda N2")
                    variabili2.coda2.append(variabili2.tempo)
                    print(variabili2.coda2[-1])
                    variabili2.N2+=1
                else:
                    print("Spazio esaurito, richiesta scartata")
                    variabili2.scartati_N2+=1
            else:
                print("Richiesta di tipo 1,\nControllo Spazio nella coda\n")
                variabili2.arrivi_N1+=1  #aumentiamo il valore di arrivi che tiene il conto del numero di richieste arrivate nel sistema
                if(variabili2.N1<5):
                    print("Spazio Disponibile, aggiunta della richiesta nella coda N1")
                    variabili2.coda1.append(variabili2.tempo)
                    variabili2.N1+=1
                else:
                    print("Spazio esaurito, richiesta scartata")
                    variabili2.scartati_N1+=1
            if(variabili2.N1+variabili2.N2!=0 and variabili2.stato==0): #Forse implementare ciclo while
                print("entriamo in esecuzione casuale code")
                EsecuzioneCasualeCode()
            else:
                print("Server Occupato\n")
        else:
            #caso in cui dobbiamo gestire l'evento per la fine del servizio
            if(variabili2.stato==1):
                print("siamo in esecuzione servizio 1")
                EsecuzioneDelServizio1()
                variabili2.tempo_precedente=variabili2.tempo #salviamo il tempo dell'ultimo evento
                variabili2.tempo=variabili2.tempo_fine_servizio #il tempo nel sistema va avanti
                variabili2.tempo_fine_servizio=0#variabile della funzione rimessa a 0
                variabili2.stato=0 #server libero
                variabili2.area+=(variabili2.N1+variabili2.N2+(1 if variabili2.stato !=0 else 0)) * (variabili2.tempo-variabili2.tempo_precedente)
                variabili2.area_coda1[variabili2.N1-1]+=variabili2.tempo-variabili2.tempo_precedente
                variabili2.area_coda2[variabili2.N2-1]+=variabili2.tempo-variabili2.tempo_precedente
                variabili2.tempo_server_occupato=variabili2.tempo_server_occupato+(variabili2.fine_occupato-variabili2.inizio_occupato)
            else:
                print("siamo in esecuzione servizio 2")
                EsecuzioneDelServizio2()
                variabili2.tempo_precedente=variabili2.tempo #salviamo il tempo dell'ultimo evento
                variabili2.tempo=variabili2.tempo_fine_servizio #il tempo nel sistema va avanti
                variabili2.tempo_fine_servizio=0
                variabili2.stato=0 #server libero
                variabili2.area+=(variabili2.N1+variabili2.N2+(1 if variabili2.stato !=0 else 0)) * (variabili2.tempo-variabili2.tempo_precedente)
                variabili2.area_coda1[variabili2.N1-1]+=variabili2.tempo-variabili2.tempo_precedente
                variabili2.area_coda2[variabili2.N2-1]+=variabili2.tempo-variabili2.tempo_precedente
                variabili2.tempo_server_occupato=variabili2.tempo_server_occupato+(variabili2.fine_occupato-variabili2.inizio_occupato)
            #dopo aver eseguito il servizio, se vi sono altre richieste in coda, il server avvia un nuovo job
            if(variabili2.N1+variabili2.N2!=0): #dopo aver finito l'ultimo servizio il server verifica se vi siano altre richieste in coda e in caso genera il nuovo job
                EsecuzioneCasualeCode()
        i+=1
        print("i-> ", i)
    print("Elaborazione completata...Dati prodotti:\n")
    print("Throughput: ",(variabili2.completati_N1+variabili2.completati_N2)/variabili2.tempo)
    print("Richieste arrivate di tipo 1: ",variabili2.arrivi_N1)
    print("Richieste arrivate di tipo 2: ",variabili2.arrivi_N2)
    print("Richieste scartate di tipo 1: ",variabili2.scartati_N1)
    print("Richieste scartate di tipo 2: ",variabili2.scartati_N2)
    print("Loss rate tipo 1: ",variabili2.scartati_N1/variabili2.arrivi_N1)
    print("Loss rate tipo 2: ",variabili2.scartati_N2/variabili2.arrivi_N2)
    print("Loss rate totale: ",(variabili2.scartati_N1+variabili2.scartati_N2)/(variabili2.arrivi_N1+variabili2.arrivi_N2))
    print("Tempo server occupato : ", variabili2.tempo_server_occupato)
    print("tempo totale simulazione: ",variabili2.tempo)
    print("numero di richieste medio nel sistema: ",variabili2.area/variabili2.tempo)
    for k in range(len(variabili2.area_coda1)):
        print(f"Coda 1 - k={k}: {variabili2.area_coda1[k] / variabili2.tempo}")

    for k in range(len(variabili2.area_coda2)):
        print(f"Coda 2 - k={k}: {variabili2.area_coda2[k] / variabili2.tempo}")
    print("tempo medio di risposta : ")




if __name__ == "__main__":
    main() 