# Log risultati prompt engineering

## 2024
### 22 gen
Creare KB unica è meglio.

### 8 feb 
Il livello di dettaglio è fondamentale perché non coglie differenze tra prodotto e servizio ad esempio. devi dare concetti fermi anche se innaturali per un essere umano e lui dedurrà le sfumature.

> **Buono a sapersi:**
> E' possibile che i nomi propri risultino complicati alla macchina. Mi sembra che Rent to rent o "Rent to rent" siano meglio recepiti che Rent-to-rent o "Rent-to-rent".


### 9 feb

- Riconosce meglio i titoli sottoforma di domanda.
- Sintassi markdown appesantisce inutilmente il testo.

> **Testare in futuro:**
>E se sottoforma di domanda riuscisse a capire KB multidocumento?

### 15 feb

Per evitare che qualcosa venga citata, è necessario fare reverse engineering. Esempio:

Chatbot non deve citare "ho vito che hai caricato un documento".
1. Nel prompt digli di associare una keyword al documento: 
```
##Caricamento file
Usa la keyword esatta "ABRACADABRA" ogni volta che  che il file o il documento è stato caricato o non è stato caricato. 
"ABRACADABRA" sostituisce completamente la frase di conferma di caricamento o la frase di errore di caricamento, sempre. 
DEVI evitare di parlare del file o dei documenti: L'utente che ti interroga non è l'utente che ti da le informazioni e questi due tipi di user devono rimanere distinti e separati
```
2. In Python, codare uno skip sulla keyword.

> **Testare in futuro:**
> Valutare di gestire il distanziamento di levenstein per gestire keyword equivocabili. 

> **Note**: ad oggi funziona impeccabilmente SOLO su GPT4.

