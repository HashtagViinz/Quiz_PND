
# Deep Learning & Computer Science Quiz Bot

Un'applicazione interattiva da riga di comando (CLI) progettata per supportare lo studio e la preparazione degli esami universitari attraverso quiz teorici e simulazioni d'esame. Il sistema integra un meccanismo avanzato di tracciamento degli errori e un'interfaccia terminale ottimizzata per una navigazione rapida ed efficiente.

## 🚀 Funzionalità

- **Quiz Standard**: Generazione di una sessione di quiz con un numero prefissato di domande estratte casualmente dall'intero pool (default: 30 domande).
- **Quiz per Argomento / File**: Filtro automatico e mirato delle domande in base al file sorgente selezionato, consentendo di completare interi blocchi d'esame o capitoli specifici.
- **Quiz di Recupero (Sessione Errori)**: Modalità focalizzata esclusivamente sulle domande precedentemente sbagliate, attingendo direttamente dall'archivio storico degli errori per ottimizzare la curva di apprendimento.
- **Supporto Risposte Multiple**: Gestione dinamica di quesiti con una o più risposte corrette simultanee. L'input dell'utente viene automaticamente normalizzato, ordinato e confrontato.
- **Tracciamento Persistente**: Salvataggio automatico e progressivo degli errori in un file JSON dedicato. Quando una domanda viene indovinata in una sessione successiva, viene automaticamente rimossa dal pool di recupero.
- **Interfaccia CLI Colorata**: Sfrutta i codici ANSI per formattare l'output nel terminale, evidenziando in modo chiaro domande, opzioni, feedback immediati e spiegazioni approfondite dell'AI.

## 📂 Struttura del Progetto


```

```text
README.md generato con successo.

```text
.
├── theory.py            # Script per la gestione dei quiz di teoria (v3.0 JSON Edition)
├── exams.py             # Script dedicato alle simulazioni e prove d'esame storiche
├── congrat.json         # File di configurazione contenente stringhe di congratulazioni casuali
├── errori.json          # Archivio storico delle risposte errate (generato e aggiornato in automatico)
└── data/                # Directory contenente i database delle domande in formato JSON
    ├── networking.json  # Esempio di pool di domande (es. reti, IPv6, ARP)
    └── deep_learning.json

```

## 🛠️ Requisiti e Installazione

Il progetto è sviluppato interamente in **Python 3** utilizzando esclusivamente i moduli nativi della libreria standard (`os`, `json`, `random`, `re`). Non è richiesta l'installazione di alcuna dipendenza di terze parti via `pip`.

1. Assicurati che l'ambiente di esecuzione disponga di **Python 3.x**.
2. Rendi gli script eseguibili e avviali all'interno del tuo terminale Linux:

```bash
# Assegnazione dei permessi di esecuzione
chmod +x theory.py exams.py

# Avvio del quiz di teoria
./theory.py

```

## 🎮 Modalità d'Uso e Comandi della CLI

Durante lo svolgimento di una sessione di quiz, il terminale accetterà i seguenti input:

* **Lettere delle opzioni (A-E)**: Inserisci le opzioni che ritieni corrette. Per domande a risposta multipla, puoi digitare le lettere in sequenza (es. `ACD` o `a, c, d`). Il parser interno ripulirà l'input da spazi o caratteri speciali, ordinando le risposte per il confronto con il database.
* **`S` (Skip)**: Salta la domanda corrente senza penalizzazioni nel punteggio. Il sistema mostrerà immediatamente la combinazione corretta e l'analisi dettagliata.
* **`Q` (Quit)**: Interrompe la sessione di quiz corrente, aggiorna in modo sicuro il file `errori.json` con i progressi maturati fino a quel momento e ritorna alla shell.

## 📊 Specifiche del Formato Dati (JSON)

I file delle domande posizionati all'interno della directory `data/` devono rispettare rigidamente la seguente struttura per consentire il corretto parsing del software:

```json
[
  {
    "id": 1,
    "question": "Testo dettagliato del quesito teorico o d'esame...",
    "options": {
      "A": "Testo dell'opzione A",
      "B": "Testo dell'opzione B",
      "C": "Testo dell'opzione C",
      "D": "Testo dell'opzione D"
    },
    "correct_answers": [
      "A",
      "C"
    ],
    "ai_analyzing": "Analisi logica, spiegazione dettagliata del contesto o motivazione della risposta corretta."
  }
]

```

## 🧠 Note di Sviluppo

Il sistema gestisce autonomamente i conflitti di duplicazione delle domande all'interno del pool degli errori verificando sia la corrispondenza dell'identificativo unico (`id`) sia l'uguaglianza del testo della domanda, garantendo l'integrità del database di ripasso anche in presenza di file sorgente multipli.
