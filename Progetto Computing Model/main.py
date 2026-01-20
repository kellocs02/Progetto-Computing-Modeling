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

def EstrazioneCasuale():
    if(random.random<0.50):
        print("Esecuzione richiesta in coda 1\n")
        tempo_servizio_1 = -math.log(1 - random.random()) / variabili.Durata_Media_Del_Serviziop_N1
        variabili.N1-=1
    else:
        print("Esecuzione richiesta in coda 2\n")
        tempo_servizio_2 = -math.log(1 - random.random()) / variabili.Durata_Media_Del_Serviziop_N2


def EsecuzioneCasualeCode():
    if(variabili.N1!=0 and variabili.N2!=0):
        EstrazioneCasuale()


def main():
    print("Progetto Computing Modeling / Professor. Scarpa / Studente Alberto Paludetti")
    delta_t = -math.log(1 - random.random()) / variabili.V_Lambda #genera il numero casuale di arrivo della richiesta seguendo la distribuzione di poisson 
    variabili.tempo+=delta_t #aumentiamo il tempo nel sistema
    print("Arrivo di una nuova richiesta al tempo ", variabili.tempo)
    tipo_Di_richiesta=random.random() #generiamo un numero casuale che utilizziamo per decidere di che tipo è la richiesta (sotto il 75 sarà di tipo 2, altrimenti di tipo 1)
    if(tipo_Di_richiesta<=0.75):
        print("Richiesta di tipo 2,\nControllo Spazio nella coda\n")
        variabili.arrivi_N2+=1
        if(variabili.N2<12):
            print("Spazio disponibile, aggiunta della richiesta nella coda N2")
            variabili.coda2.append(variabili.tempo)
            variabili.N2+=1
        else:
            print("Spazio esaurito, richiesta scartata")
            variabili.scartati_N2+=1
    else:
        print("Richiesta di tipo 1,\nControllo Spazio nella coda\n")
        variabili.arrivi_N1+=1
        if(variabili.N1<6):
            print("Spazio Disponibile, aggiunta della richiesta nella coda N1")
            variabili.coda1.append(variabili.tempo)
            variabili.N1+=1
        else:
            print("Spazio esaurito, richiesta scartata")
            variabili.scartati_N1+=1
    if(variabili.N1+variabili.N2!=0): #fase di esecuzione delle richieste in coda
        EsecuzioneCasualeCode()





if __name__ == "__main__":
    main() 