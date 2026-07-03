#!/usr/bin/env python3
import os
import re
import json
import random

# Costanti per i colori ANSI nel terminale
RESET = "\033[0m"
BOLD = "\033[1m"
RED = "\033[91m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
CYAN = "\033[96m"

DATA_FOLDER = "data"
ERROR_FILE = "errori.json"
DEFAULT_QUIZ_SIZE = 30

def parse_quiz_files():
    """Legge tutti i file nella cartella 'data' e fa il parsing delle domande."""
    questions_pool = []
    
    if not os.path.exists(DATA_FOLDER):
        print(f"{RED}{BOLD}⚠️ Errore: La cartella '{DATA_FOLDER}' non esiste. Creala e inserisci i file di testo.{RESET}")
        return questions_pool

    pattern = re.compile(
        r"\d+\.\s*(.*?)\n"                     
        r"((?:[A-E]\.\s*.*?\n?)+)"             
        r"\*\*Answer:\*\*\s*([A-E])\s*\n+"     
        r"AI Analyzing:\s*(.*?)(?=\n\d+\.|\n*$)", 
        re.DOTALL | re.IGNORECASE
    )

    for filename in os.listdir(DATA_FOLDER):
        if filename.endswith(".txt"):
            file_path = os.path.join(DATA_FOLDER, filename)
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
                
                matches = pattern.findall(content)
                for match in matches:
                    q_text = match[0].strip()
                    options_raw = match[1].strip().split('\n')
                    options = [opt.strip() for opt in options_raw if opt.strip()]
                    answer = match[2].strip().upper()
                    analysis = match[3].strip()
                    
                    questions_pool.append({
                        "question": q_text,
                        "options": options,
                        "answer": answer,
                        "analysis": analysis,
                        "source": filename
                    })
    return questions_pool

def load_wrong_questions():
    """Carica le domande sbagliate salvate nel file JSON."""
    if os.path.exists(ERROR_FILE):
        with open(ERROR_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def load_congr_json():
    """Carica le frasi di congratulazioni dal file JSON."""
    congr_file = "congrat.json"
    
    if os.path.exists(congr_file):
        with open(congr_file, "r", encoding="utf-8") as f:
            return json.load(f)

def congratulations():
    """Stampa una frase di congratulazioni casuale."""
    congrats = load_congr_json()
    if congrats:
        print(f"\n{GREEN}{BOLD}{random.choice(congrats["congratulations"])}{RESET}")
    else:
        print(f"\n{GREEN}{BOLD}🎉 Ottimo lavoro! Continua così! 🎉{RESET}")
            
def save_wrong_questions(wrong_list):
    """Salva la lista aggiornata delle domande sbagliate."""
    with open(ERROR_FILE, "w", encoding="utf-8") as f:
        json.dump(wrong_list, f, indent=4, ensure_ascii=False)

def run_quiz(questions, max_size=None):
    """Avvia la sessione di quiz interattiva con colori."""
    if not questions:
        print(f"\n{RED}📭 Nessuna domanda disponibile per questa modalità.{RESET}")
        return

    # Se max_size è definito (es. 30), estrae un campione casuale, altrimenti fa l'intero blocco (es. 50 domande)
    if max_size and len(questions) > max_size:
        session_questions = random.sample(questions, max_size)
    else:
        session_questions = list(questions)
        random.shuffle(session_questions) # Mescola comunque l'ordine delle domande
        
    sample_size = len(session_questions)
    
    score = 0
    currently_wrong = []
    previously_wrong = load_wrong_questions()

    print(f"\n{GREEN}{BOLD}🚀 Il quiz sta per iniziare! Rispondi a {sample_size} domande.{RESET}")
    print(f"{YELLOW}" + "="*60 + f"{RESET}")
    
    for idx, q in enumerate(session_questions, 1):
        print(f"\n{BOLD}[Domanda {idx}/{sample_size}]{RESET} ({BLUE}File: {q['source']}{RESET})")
        print(f"{YELLOW}📌 {q['question']}{RESET}\n")
        
        for opt in q['options']:
            print(f"  {opt}")
        
        user_ans = ""
        while user_ans not in ['A', 'B', 'C', 'D', 'E', 'Q', 'S']:
            user_ans = input(f"\n✍️  La tua risposta ({BOLD}A-E{RESET}) | {YELLOW}{BOLD}S{RESET} to SKIP o '{RED}{BOLD}Q{RESET}' per uscire: ").strip().upper()
        
        if user_ans == 'Q':
            print(f"\n{RED}👋 Quiz interrotto. Alla prossima!{RESET}")
            break
        
        if user_ans == 'S':
            # SKIP
            print(f"\n{CYAN}🔍 SKIP - Solution: {q['answer']}{RESET}")
            continue
        
        # Verifica della risposta
        if user_ans == q['answer']:
            congratulations()
            score += 1
            # Se indovinata, toglila dal database degli errori precedenti
            previously_wrong = [x for x in previously_wrong if x['question'] != q['question']]
        else:
            print(f"\n{RED}{BOLD}❌ SBAGLIATO! La risposta corretta era: {q['answer']}{RESET}")
            currently_wrong.append(q)
            if q['question'] not in [x['question'] for x in previously_wrong]:
                previously_wrong.append(q)
        
        # Stampa l'analisi dell'AI
        print(f"\n{CYAN}{BOLD}🧠 AI Analyzing:{RESET} {CYAN}{q['analysis']}{RESET}")
        print(f"{YELLOW}" + "-" * 60 + f"{RESET}")

    # Report finale colorato
    print("\n" + f"{YELLOW}="*20 + f" {BOLD}RISULTATI FINALI{RESET} {YELLOW}" + "="*20 + f"{RESET}")
    percentage = int(score/sample_size*100) if sample_size > 0 else 0
    
    if percentage >= 70:
        score_color = GREEN
    elif percentage >= 50:
        score_color = YELLOW
    else:
        score_color = RED
        
    print(f"🎯 Punteggio: {score_color}{BOLD}{score}/{sample_size}{RESET} ({score_color}{percentage}%{RESET})")
    
    save_wrong_questions(previously_wrong)
    print(f"💾 File degli errori aggiornato. Domande rimaste da ripassare: {RED}{BOLD}{len(previously_wrong)}{RESET}")
    print(f"{YELLOW}" + "="*58 + f"{RESET}")

def main():
    # Pulisce lo schermo per un look ottimale all'avvio
    os.system('cls' if os.name == 'nt' else 'clear')
    
    print(f"{BLUE}{BOLD}🤖 DEEP LEARNING QUIZ BOT v2.5 🤖{RESET}")
    print(f"{BLUE}="*32 + f"{RESET}")
    
    all_questions = parse_quiz_files()
    wrong_questions = load_wrong_questions()
    
    print(f"📚 Totale domande caricate dal materiale: {GREEN}{BOLD}{len(all_questions)}{RESET}")
    print(f"⚠️  Domande nel pool errori: {RED}{BOLD}{len(wrong_questions)}{RESET}")
    
    print(f"\n{BOLD}Scegli la modalità di studio:{RESET}")
    print(f"{GREEN}1. Quiz Standard{RESET} (30 domande casuali da tutto il programma)")
    print(f"{CYAN}2. Quiz per Argomento / File{RESET} (Tutte le 50 domande di un singolo file)")
    print(f"{RED}3. Quiz di Recupero{RESET} (Allena solo le risposte sbagliate)")
    print(f"{YELLOW}4. Resetta archivio errori{RESET}")
    
    choice = input(f"\nInserisci il numero ({BOLD}1-4{RESET}): ").strip()
    
    if choice == "1":
        run_quiz(all_questions, max_size=DEFAULT_QUIZ_SIZE)
        
    elif choice == "2":
        # Trova la lista unica dei file disponibili
        files = sorted(list(set([q['source'] for q in all_questions])))
        if not files:
            print(f"\n{RED}📭 Nessun argomento rilevato. Verifica la cartella 'data'.{RESET}")
            return
            
        print(f"\n{BOLD}📚 Seleziona un argomento:{RESET}")
        for idx, filename in enumerate(files, 1):
            # Conta quante domande ci sono per questo file specifico
            count = sum(1 for q in all_questions if q['source'] == filename)
            print(f"  {CYAN}{idx}.{RESET} {filename} ({YELLOW}{count} domande{RESET})")
            
        try:
            file_choice = int(input(f"\nScegli il numero dell'argomento (1-{len(files)}): ").strip())
            if 1 <= file_choice <= len(files):
                selected_file = files[file_choice - 1]
                # Filtra le domande tenendo solo quelle del file scelto
                topic_questions = [q for q in all_questions if q['source'] == selected_file]
                # Avvia senza max_size per farle tutte e 50
                run_quiz(topic_questions, max_size=None)
            else:
                print(f"{RED}Scelta non valida.{RESET}")
        except ValueError:
            print(f"{RED}Inserisci un numero valido.{RESET}")
            
    elif choice == "3":
        run_quiz(wrong_questions, max_size=None)
        
    elif choice == "4":
        confirm = input(f"{RED}Sei sicura di voler azzerare tutti gli errori salvati? (s/n): {RESET}").strip().lower()
        if confirm == 's' and os.path.exists(ERROR_FILE):
            os.remove(ERROR_FILE)
            print(f"🗑️  {GREEN}Archivio errori svuotato con successo!{RESET}")
        else:
            print("❌ Operazione annullata.")
    else:
        print(f"{RED}Scelta non valida. Uscita.{RESET}")

if __name__ == "__main__":
    main()