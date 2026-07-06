#!/usr/bin/env python3
import os
import json
import random
import re

# Costanti per i colori ANSI nel terminale
RESET = "\033[0m"
BOLD = "\033[1m"
RED = "\033[91m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
CYAN = "\033[96m"

DATA_FOLDER = "exams"
ERROR_FILE = "errori_exams.json"
DEFAULT_QUIZ_SIZE = 30

def parse_quiz_files():
    """Legge tutti i file JSON nella cartella 'data' e carica le domande."""
    questions_pool = []
    
    if not os.path.exists(DATA_FOLDER):
        print(f"{RED}{BOLD}⚠️ Errore: La cartella '{DATA_FOLDER}' non esiste. Creala e inserisci i file JSON.{RESET}")
        return questions_pool

    for filename in os.listdir(DATA_FOLDER):
        # Ignoriamo i file JSON di sistema del quiz, leggiamo solo le banche dati
        if filename.endswith(".json") and filename not in [ERROR_FILE, "congrat.json"]:
            file_path = os.path.join(DATA_FOLDER, filename)
            with open(file_path, "r", encoding="utf-8") as f:
                try:
                    data = json.load(f)
                    for item in data:
                        questions_pool.append({
                            "id": item.get("id"),
                            "question": item.get("question"),
                            "options": item.get("options", {}),
                            "correct_answers": item.get("correct_answers", []),
                            "analysis": item.get("ai_analyzing", "Nessuna analisi disponibile."),
                            "source": filename
                        })
                except json.JSONDecodeError:
                    print(f"{RED}⚠️ Errore nel parsing del file: {filename}{RESET}")
                    
    return questions_pool

def load_wrong_questions():
    """Carica le domande sbagliate salvate nel file JSON."""
    if os.path.exists(ERROR_FILE):
        with open(ERROR_FILE, "r", encoding="utf-8") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return []
    return []

def load_congr_json():
    """Carica le frasi di congratulazioni dal file JSON."""
    congr_file = "congrat.json"
    if os.path.exists(congr_file):
        with open(congr_file, "r", encoding="utf-8") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return None
    return None

def congratulations():
    """Stampa una frase di congratulazioni casuale."""
    congrats_data = load_congr_json()
    if congrats_data and "congratulations" in congrats_data:
        print(f"\n{GREEN}{BOLD}{random.choice(congrats_data['congratulations'])}{RESET}")
    else:
        print(f"\n{GREEN}{BOLD}🎉 Ottimo lavoro! Continua così! 🎉{RESET}")
            
def save_wrong_questions(wrong_list):
    """Salva la lista aggiornata delle domande sbagliate."""
    with open(ERROR_FILE, "w", encoding="utf-8") as f:
        json.dump(wrong_list, f, indent=4, ensure_ascii=False)

def normalize_answers(ans_string):
    """Estrae solo le lettere dall'input utente e le ordina alfabeticamente."""
    # Rimuove tutto ciò che non è una lettera A-Z
    cleaned = re.sub(r'[^A-Z]', '', ans_string.upper())
    # Restituisce una lista di lettere ordinate
    return sorted(list(set(cleaned)))

def run_quiz(questions, max_size=None):
    """Avvia la sessione di quiz interattiva con colori."""
    if not questions:
        print(f"\n{RED}📭 Nessuna domanda disponibile per questa modalità.{RESET}")
        return

    if max_size and len(questions) > max_size:
        session_questions = random.sample(questions, max_size)
    else:
        session_questions = list(questions)
        random.shuffle(session_questions)
        
    sample_size = len(session_questions)
    score = 0
    currently_wrong = []
    previously_wrong = load_wrong_questions()

    print(f"\n{GREEN}{BOLD}🚀 Il quiz sta per iniziare! Rispondi a {sample_size} domande.{RESET}")
    print(f"{YELLOW}" + "="*60 + f"{RESET}")
    
    for idx, q in enumerate(session_questions, 1):
        print(f"\n{BOLD}[Domanda {idx}/{sample_size}]{RESET} ({BLUE}File: {q['source']} - ID: {q.get('id', 'N/A')}{RESET})")
        print(f"{YELLOW}📌 {q['question']}{RESET}\n")
        
        # Stampa le opzioni dal dizionario
        for key, value in q['options'].items():
            print(f"  {BOLD}{key}{RESET}: {value}")
        
        # Gestione input per risposte multiple
        correct_sorted = sorted(q['correct_answers'])
        is_multiple = len(correct_sorted) > 1
        
        prompt_msg = f"\n✍️  La tua risposta (es. {BOLD}A,B{RESET}) | {YELLOW}{BOLD}S{RESET} to SKIP o '{RED}{BOLD}Q{RESET}' per uscire: " if is_multiple else f"\n✍️  La tua risposta ({BOLD}A-E{RESET}) | {YELLOW}{BOLD}S{RESET} to SKIP o '{RED}{BOLD}Q{RESET}' per uscire: "
        
        user_input = ""
        user_parsed = []
        
        while True:
            user_input = input(prompt_msg).strip().upper()
            if user_input in ['Q', 'S']:
                break
            
            user_parsed = normalize_answers(user_input)
            if user_parsed: # Se ha inserito almeno una lettera valida
                break
        
        if user_input == 'Q':
            print(f"\n{RED}👋 Quiz interrotto. Alla prossima!{RESET}")
            break
        
        if user_input == 'S':
            print(f"\n{CYAN}🔍 SKIP - Solution: {', '.join(correct_sorted)}{RESET}")
            continue
        
        # Verifica della risposta (confronta le liste ordinate)
        if user_parsed == correct_sorted:
            congratulations()
            score += 1
            # Rimuove dai precedentemente sbagliati confrontando l'ID o la domanda
            previously_wrong = [x for x in previously_wrong if x.get('id') != q.get('id') and x['question'] != q['question']]
        else:
            print(f"\n{RED}{BOLD}❌ SBAGLIATO! La risposta corretta era: {', '.join(correct_sorted)}{RESET}")
            currently_wrong.append(q)
            # Aggiunge agli errori se non è già presente
            if q['question'] not in [x['question'] for x in previously_wrong]:
                previously_wrong.append(q)
        
        # Stampa l'analisi dell'AI
        print(f"\n{CYAN}{BOLD}🧠 AI Analyzing:{RESET} {CYAN}{q['analysis']}{RESET}")
        print(f"{YELLOW}" + "-" * 60 + f"{RESET}")

    # Report finale
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
    os.system('cls' if os.name == 'nt' else 'clear')
    
    print(f"{BLUE}{BOLD}🤖 DEEP LEARNING QUIZ BOT v3.0 (JSON Edition) 🤖{RESET}")
    print(f"{BLUE}="*46 + f"{RESET}")
    
    all_questions = parse_quiz_files()
    wrong_questions = load_wrong_questions()
    
    print(f"📚 Totale domande caricate: {GREEN}{BOLD}{len(all_questions)}{RESET}")
    print(f"⚠️  Domande nel pool errori: {RED}{BOLD}{len(wrong_questions)}{RESET}")
    
    print(f"\n{BOLD}Scegli la modalità di studio:{RESET}")
    print(f"{GREEN}1. Quiz Standard{RESET} (30 domande casuali)")
    print(f"{CYAN}2. Quiz per Argomento / File{RESET} (Tutte le domande di un singolo file JSON)")
    print(f"{RED}3. Quiz di Recupero{RESET} (Allena solo le risposte sbagliate)")
    print(f"{YELLOW}4. Resetta archivio errori{RESET}")
    
    choice = input(f"\nInserisci il numero ({BOLD}1-4{RESET}): ").strip()
    
    if choice == "1":
        run_quiz(all_questions, max_size=DEFAULT_QUIZ_SIZE)
        
    elif choice == "2":
        files = sorted(list(set([q['source'] for q in all_questions])))
        if not files:
            print(f"\n{RED}📭 Nessun file rilevato. Verifica la cartella '{DATA_FOLDER}'.{RESET}")
            return
            
        print(f"\n{BOLD}📚 Seleziona un file JSON:{RESET}")
        for idx, filename in enumerate(files, 1):
            count = sum(1 for q in all_questions if q['source'] == filename)
            print(f"  {CYAN}{idx}.{RESET} {filename} ({YELLOW}{count} domande{RESET})")
            
        try:
            file_choice = int(input(f"\nScegli il numero del file (1-{len(files)}): ").strip())
            if 1 <= file_choice <= len(files):
                selected_file = files[file_choice - 1]
                topic_questions = [q for q in all_questions if q['source'] == selected_file]
                run_quiz(topic_questions, max_size=None)
            else:
                print(f"{RED}Scelta non valida.{RESET}")
        except ValueError:
            print(f"{RED}Inserisci un numero valido.{RESET}")
            
    elif choice == "3":
        run_quiz(wrong_questions, max_size=None)
        
    elif choice == "4":
        confirm = input(f"{RED}Sei sicuro di voler azzerare tutti gli errori salvati? (s/n): {RESET}").strip().lower()
        if confirm == 's' and os.path.exists(ERROR_FILE):
            os.remove(ERROR_FILE)
            print(f"🗑️  {GREEN}Archivio errori svuotato con successo!{RESET}")
        else:
            print("❌ Operazione annullata.")
    else:
        print(f"{RED}Scelta non valida. Uscita.{RESET}")

if __name__ == "__main__":
    main()