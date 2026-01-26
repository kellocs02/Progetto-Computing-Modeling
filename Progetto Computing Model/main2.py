import random  #random restituisce un numero casuale tra 0 e 1
import math
import variabili2
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
def Calcolo_Metriche(arrivi1, arrivi2, tempoSimulazione):
    # Tassi di arrivo
    lambda1 = arrivi1 / tempoSimulazione
    lambda2 = arrivi2 / tempoSimulazione

    # Tassi di servizio
    mu1 = 0.5   # tipo 1
    mu2 = 1.5   # tipo 2

    # Capacità massime code
    K1 = 5
    K2 = 12

    def mm1k(lambda_, mu, K):
        """Calcolo metriche per coda M/M/1/K"""
        rho = lambda_ / mu
        # Probabilità che la coda sia vuota
        if rho != 1:
            P0 = (1 - rho) / (1 - rho**(K + 1))
        else:
            P0 = 1 / (K + 1)

        # Probabilità di avere n richieste nel sistema
        Pn = [P0 * rho**n for n in range(K + 1)]

        # Probabilità di scarto (loss rate)
        P_block = Pn[-1]

        # Throughput effettivo
        throughput = lambda_ * (1 - P_block)

        # Numero medio di richieste nel sistema
        L = sum(n * Pn[n] for n in range(K + 1))

        # Tempo medio di risposta
        W = L / throughput if throughput > 0 else 0

        # Utilizzo server
        U = 1 - P0

        return {
            "rho": rho,
            "P_block": P_block,
            "throughput": throughput,
            "L": L,
            "W": W,
            "U": U,
            "Pn": Pn
        }

    # Calcolo metriche per le due code
    metrics1 = mm1k(lambda1, mu1, K1)
    metrics2 = mm1k(lambda2, mu2, K2)

    # Throughput totale del sistema
    throughput_totale = metrics1["throughput"] + metrics2["throughput"]

    # Numero medio totale di richieste nel sistema
    L_totale = metrics1["L"] + metrics2["L"]

    # Tempo medio di risposta totale
    W_totale = L_totale / throughput_totale if throughput_totale > 0 else 0

    return {
        "Coda1": metrics1,
        "Coda2": metrics2,
        "Throughput_totale": throughput_totale,
        "L_totale": L_totale,
        "W_totale": W_totale
    }


def reset_variabili():
    variabili2.tempo = 0
    variabili2.N1 = 0
    variabili2.N2 = 0
    variabili2.arrivi_N1 = 0
    variabili2.arrivi_N2 = 0
    variabili2.scartati_N1 = 0
    variabili2.scartati_N2 = 0
    variabili2.completati_N1 = 0
    variabili2.completati_N2 = 0
    variabili2.area = 0
    variabili2.tempo_fine_servizio = 0
    variabili2.stato = 0
    variabili2.coda1 = []
    variabili2.coda2 = []
    variabili2.area_coda1 = [0]*5
    variabili2.area_coda2 = [0]*12
    variabili2.tempo_server_occupato = 0

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
    if variabili2.priorità==0:  #0 indica casuale, valore diverso da 0 priorità alla coda di tipo 1
        if random.random() <=0.50:
            GenerazioneTempoServizio1()
        else:
            GenerazioneTempoServizio2()
    else:
        if variabili2.N1!=0:
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
    tempo_massimo=100000
    tempo_inziale_non_conteggiato=10000
    while(variabili2.tempo<tempo_massimo):
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
    print("Elaborazione completata...Dati prodotti:\n")
    tempo_effettivo=variabili2.tempo-tempo_inziale_non_conteggiato
    throughput= (variabili2.completati_N1+variabili2.completati_N2)/tempo_effettivo
    print("Throughput: ",throughput)
    print("Richieste arrivate di tipo 1: ",variabili2.arrivi_N1)
    print("Richieste arrivate di tipo 2: ",variabili2.arrivi_N2)
    print("Richieste scartate di tipo 1: ",variabili2.scartati_N1)
    print("Richieste scartate di tipo 2: ",variabili2.scartati_N2)
    loss_rate_tipo_1=variabili2.scartati_N1/variabili2.arrivi_N1
    loss_rate_tipo_2=variabili2.scartati_N2/variabili2.arrivi_N2
    loss_rate_totale=(variabili2.scartati_N1+variabili2.scartati_N2)/(variabili2.arrivi_N1+variabili2.arrivi_N2)
    print("Loss rate tipo 1: ",loss_rate_tipo_1)
    print("Loss rate tipo 2: ",loss_rate_tipo_2)
    print("Loss rate totale: ",loss_rate_totale)
    print("Tempo server occupato : ", variabili2.tempo_server_occupato)
    print("tempo totale simulazione: ",variabili2.tempo)
    print("tempo effettivo conteggiato: ", tempo_effettivo)
    numero_di_richieste_medio_nel_sistema=variabili2.area/tempo_effettivo
    print("numero di richieste medio nel sistema: ",numero_di_richieste_medio_nel_sistema)
    for k in range(len(variabili2.area_coda1)):
        print(f"Coda 1 - k={k}: {variabili2.area_coda1[k] / tempo_effettivo}")

    for k in range(len(variabili2.area_coda2)):
        print(f"Coda 2 - k={k}: {variabili2.area_coda2[k] / tempo_effettivo}")
    L = variabili2.area / variabili2.tempo
    throughput = (variabili2.completati_N1 + variabili2.completati_N2) / tempo_effettivo
    tempo_medio_risposta = L / throughput

    print("tempo medio di risposta : ", tempo_medio_risposta)
    if(variabili2.priorità==0):
        variabili2.dizionario_valori_1={
            "throughput": throughput,
            "arrivi_tipo_1": variabili2.arrivi_N1,
            "arrivi_tipo_2": variabili2.arrivi_N2,
            "scarti_tipo_1": variabili2.scartati_N1,
            "scarti_tipo_2": variabili2.scartati_N2,
            "loss_rate_tipo_1": loss_rate_tipo_1,
            "loss_rate_tipo_2": loss_rate_tipo_2,
            "loss_rate_totale": loss_rate_totale,
            "tempo_server_occupato": variabili2.tempo_server_occupato,
            "tempo_totale": variabili2.tempo,
            "L_medio_sistema": numero_di_richieste_medio_nel_sistema,
            "tempo_medio_risposta": tempo_medio_risposta
        }
    else:
        variabili2.dizionario_valori_2={
            "throughput": throughput,
            "arrivi_tipo_1": variabili2.arrivi_N1,
            "arrivi_tipo_2": variabili2.arrivi_N2,
            "scarti_tipo_1": variabili2.scartati_N1,
            "scarti_tipo_2": variabili2.scartati_N2,
            "loss_rate_tipo_1": loss_rate_tipo_1,
            "loss_rate_tipo_2": loss_rate_tipo_2,
            "loss_rate_totale": loss_rate_totale,
            "tempo_server_occupato": variabili2.tempo_server_occupato,
            "tempo_totale": variabili2.tempo,
            "L_medio_sistema": numero_di_richieste_medio_nel_sistema,
            "tempo_medio_risposta": tempo_medio_risposta
        }




if __name__ == "__main__":
    variabili2.priorità = 0
    reset_variabili()
    main()

    variabili2.priorità = 1
    reset_variabili()
    main()
    input("premi per vedere i risultati dell'esercizio con priorità casuale:\n")
    for i,k in variabili2.dizionario_valori_1.items():
        print(i,":",k)
    input("premi per vedere risultati dell'esercizio con priorità sulla coda 1\n")
    for i,k in variabili2.dizionario_valori_2.items():
        print(i,":",k)
    input("premi per passare al secondo esercizio...\n")
    input("Il calcolo delle metriche viene eseguito sui valori dell'esercizio in cui la priorità è casuale:\n")
    risultati = Calcolo_Metriche(variabili2.dizionario_valori_1["arrivi_tipo_1"], variabili2.dizionario_valori_1["arrivi_tipo_2"], 100000)
    print("Coda 1")
    for k, v in risultati["Coda1"].items():
        if k != "Pn":
            print(f"{k}: {v:.5f}")
    print("\nCdoa2")
    for k, v in risultati["Coda2"].items():
        if k != "Pn":
            print(f"{k}: {v:.5f}")
    print("\nThroughput totale:", risultati["Throughput_totale"])
    print("Numero medio richieste totale:", risultati["L_totale"])
    print("Tempo medio di risposta totale:", risultati["W_totale"])

