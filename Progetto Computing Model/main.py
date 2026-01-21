import random  #random restituisce un numero casuale tra 0 e 1
import math
import variabili
#Fase 1 implementare Poisson
#il tempo medio tra due arrivi è di 1.6 minuti, gli intervalli di tempo
#tra due arrivi consecutivi sono casuali, indipendenti, distribuiti in modo esponenziale
#con media 1.6 minuti.
#Bisogna generare un numero casuale che rappresenti il tempo di attesa fino
#al prossimo arrivo, può esser piccolo o grande, lo chiamiamo Delta_T, in media vale 1.6
# in questo modo la prossima richiesta arriva a (t+Delta_T)
#Con un processo di Poisson non genero arrivi,
#genero tempi di attesa tra un arrivo e il successivo.
#Fase 2 
def Poisson():
    return  -math.log(1 - random.random()) / variabili.V_Lambda

def EsecuzioneDelServizio1():
    variabili.coda1.pop(0)
    variabili.N1-=1 #decrementiamo il valore della coda

def EsecuzioneDelServizio2():
    variabili.coda2.pop(0)
    variabili.N2-=1

def GenerazioneTempoServizio1():
    print("Generazione del tempo di servizio per la richiesta nella coda 1\n")
    tempo_servizio_1 = -math.log(1 - random.random()) / variabili.Durata_Media_Del_Serviziop_N1 #decidiamo quanto durerà l'esecuzione del servizio in base al dato fornito
    variabili.tempo_fine_servizio=tempo_servizio_1+variabili.tempo
    variabili.stato=1

def GenerazioneTempoServizio2():
    print("Generazione del tempo di servizio per la richiesta nella coda 2\n")
    tempo_servizio_2 = -math.log(1 - random.random()) / variabili.Durata_Media_Del_Serviziop_N2
    variabili.tempo_fine_servizio=tempo_servizio_2+variabili.tempo
    variabili.stato=2

def EstrazioneCasuale():
    if random.random() <=0.50:
        GenerazioneTempoServizio1()
    else:
        GenerazioneTempoServizio2()

def EsecuzioneCasualeCode():
    if(variabili.N1!=0 and variabili.N2!=0): #nel caso in cui in entrambe le code vi siano delle richieste
        EstrazioneCasuale()
    elif(variabili.N1!=0 and variabili.N2==0): #caso in cui nella coda 1 vi sono richieste ma non nella coda 2
        GenerazioneTempoServizio1()
    else:
        GenerazioneTempoServizio2()

def main():
    print("Progetto Computing Modeling / Professor. Scarpa / Studente Alberto Paludetti")
    i=0
    delta_t = Poisson() #Generiamo la prima richiesta in arrivo (Quando arriverà)
    while(i<10): 
        variabili.prossimo_arrivo=variabili.tempo+delta_t #calcoliamo quando arriverà la prossima richiesta

        if(variabili.prossimo_arrivo < variabili.tempo_fine_servizio or variabili.tempo_fine_servizio==0):#verifichiamo quale evento si svolgerà prima 
            variabili.tempo=variabili.prossimo_arrivo #aumentiamo il tempo del sistema
            print("Arrivo di una nuova richiesta al tempo ", variabili.tempo)
            tipo_Di_richiesta=random.random() #generiamo un numero casuale che utilizziamo per decidere di che tipo è la richiesta (sotto il 75 sarà di tipo 2, altrimenti di tipo 1)
            if(tipo_Di_richiesta<=0.75):
                print("Richiesta di tipo 2,\nControllo Spazio nella coda\n")
                variabili.arrivi_N2+=1 #aumentiamo il valore di arrivi che tiene il conto del numero di richieste arrivate nel sistema
                if(variabili.N2<12):
                    print("Spazio disponibile, aggiunta della richiesta nella coda N2")
                    variabili.coda2.append(variabili.tempo)
                    variabili.N2+=1
                else:
                    print("Spazio esaurito, richiesta scartata")
                    variabili.scartati_N2+=1
            else:
                print("Richiesta di tipo 1,\nControllo Spazio nella coda\n")
                variabili.arrivi_N1+=1  #aumentiamo il valore di arrivi che tiene il conto del numero di richieste arrivate nel sistema
                if(variabili.N1<6):
                    print("Spazio Disponibile, aggiunta della richiesta nella coda N1")
                    variabili.coda1.append(variabili.tempo)
                    variabili.N1+=1
                else:
                    print("Spazio esaurito, richiesta scartata")
                    variabili.scartati_N1+=1
            if(variabili.N1+variabili.N2!=0 and variabili.stato==0): #fase di esecuzione delle richieste in coda
                print("entriamo in esecuzione casuale code")
                EsecuzioneCasualeCode()
                print(variabili.coda2[0])
            else:
                print("Server Occupato\n")
            i+=1
            delta_t=Poisson() #generiamo il tempo dell'arrivo della prossima richiesta
            print("siamo dopo il secondo delta\n")
        else:
            #caso in cui dobbiamo gestire l'evento per la fine del servizio
            if(variabili.stato==1):
                EsecuzioneDelServizio1()
                variabili.tempo=variabili.tempo_fine_servizio #il tempo nel sistema va avanti
                variabili.stato=0 #server libero
            else:
                EsecuzioneDelServizio2()
                variabili.tempo=variabili.tempo_fine_servizio #il tempo nel sistema va avanti
                variabili.stato=0 #server libero
            #Dopo aver eseguito il servizio, se vi sono altre richieste in coda, il server avvia un nuovo job
            if(variabili.N1+variabili.N2!=0): #dopo aver finito l'ultimo servizio il server verifica se vi siano altre richieste in coda e in caso genera il nuovo job
                EsecuzioneCasualeCode()



if __name__ == "__main__":
    main() 