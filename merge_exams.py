import json
import os
import glob

def unisci_domande(cartella_input, file_output):
    domande_viste = set()
    domande_unificate = []
    contatore_id = 1

    # Trova tutti i file .json nella cartella indicata
    pattern_ricerca = os.path.join(cartella_input, "*.json")
    file_json = glob.glob(pattern_ricerca)

    if not file_json:
        print(f"Nessun file JSON trovato nella cartella '{cartella_input}'")
        return

    print(f"Trovati {len(file_json)} file da elaborare...")

    for percorso_file in file_json:
        # Salta il file di output se si trova nella stessa cartella
        if os.path.abspath(percorso_file) == os.path.abspath(file_output):
            continue

        try:
            with open(percorso_file, 'r', encoding='utf-8') as f:
                dati = json.load(f)
                
                # Se il file contiene un singolo oggetto anziché una lista, lo standardizza
                if isinstance(dati, dict):
                    dati = [dati]
                
                for item in dati:
                    # Estrae il testo della domanda per verificare i duplicati
                    testo_domanda = item.get("question", "").strip()
                    
                    if testo_domanda and testo_domanda not in domande_viste:
                        domande_viste.add(testo_domanda)
                        
                        # Crea una copia della domanda per non sovrascrivere l'originale
                        nuova_domanda = item.copy()
                        # Aggiorna l'ID in modo che sia sequenziale nel nuovo file
                        nuova_domanda["id"] = contatore_id
                        
                        domande_unificate.append(nuova_domanda)
                        contatore_id += 1
                        
        except json.JSONDecodeError:
            print(f"Errore nel leggere il file (JSON non valido): {percorso_file}")
        except Exception as e:
            print(f"Errore imprevisto sul file {percorso_file}: {e}")

    # Scrive il file finale unificato
    with open(file_output, 'w', encoding='utf-8') as f_out:
        json.dump(domande_unificate, f_out, ensure_ascii=False, indent=2)

    print(f"\nElaborazione completata!")
    print(f"Domande totali (senza duplicati): {len(domande_unificate)}")
    print(f"File salvato con successo in: {file_output}")

# --- CONFIGURAZIONE ---
# Specifica la cartella dove si trovano i tuoi file correnti (usa '.' per la cartella corrente dello script)
CARTELLA_DATI = "exams" 
# Nome del file in cui salvare l'output
FILE_FINALE = "exams/all_questions.json"

# Avvia lo script
unisci_domande(CARTELLA_DATI, FILE_FINALE)