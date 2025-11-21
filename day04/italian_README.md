
# 1 chiedere a chap gpt tutorial per installare conda con il miniforge prompt e seguire i comandi
# 2 chiedere a chat gpt comandi per verificare che python sia installato e spiegarti esattamente dove mettere questi comandi
# 3 scaricare vs code studio, e chiedi a chat gpt di aiutarti nell'installazione per verificare che sia tutto fatto correttamente e che il tuo interprete di python sia attivabile su vsc
# 4 una volta fatti gli step base per installare python e il programma, scaricare la cartella dell'applicazione come file zip e metterla in un posto comodo nel pc
# 5 torna su vsc e apri la cartella scaricata
# 6 apri il file environment (quello con il punto esclamativo), fai uno screen, e mettilo su chatgpt chiedendo di aiutarti nel creare un ambiente in vsc tramite conda. spiegandogli che hai una cartella con un file environment

---
Mappa del progetto (con ruoli)
Radice del progetto

environment.yml
Ricetta Conda: crea l’ambiente chem-reporter con Python, RDKit, requests, PySimpleGUI, pytest. È il “DNA” dell’ambiente di sviluppo ed esecuzione.
Comandi tipici:

conda env create -f environment.yml
conda activate chem-reporter


.gitignore
Tiene fuori dal repo ciò che non va versionato: cache Python, build, results/, .env, ecc. (così non committi dati locali né segreti).

.env.example → .env
Modello di variabili d’ambiente. Copiandolo in .env hai i parametri runtime (timeout, user-agent, eventuali chiavi future). Il codice li legge all’avvio.

copy .env.example .env


README.md
Appunti d’uso e struttura del progetto. È la tua home page per chi apre il repo.

bootstrap_chem_reporter*.bat
Script che ha generato questa impalcatura. Non serve a runtime; resta utile se vuoi ricreare un progetto da zero.

Automazione & asset

.github/workflows/ci.yml
Pipeline GitHub Actions: su ogni push crea un ambiente con environment.yml e lancia pytest -q. È la “sirena antincendio” che ti avvisa se rompi qualcosa con una modifica.

assets/icon.png
Icona (per GUI o eventuali report). È solo un asset statico.

scripts/run_app.bat
Avvio rapido su Windows. In un setup completo dovrebbe: attivare l’ambiente e lanciare la GUI con

call conda activate chem-reporter
python -m src.app_gui


(vedi nota su app_gui.py più sotto).

Codice applicativo (src/)

__init__.py
Rende src un package Python. Utile se poi importi moduli come from src.pubchem import resolve.

config.py
Carica .env (con python-dotenv) e fornisce costanti tipo HTTP_TIMEOUT, USER_AGENT. È lo strato di configurazione a cui il resto del codice si appoggia, così non hard-codi nulla.

models.py
Dataclasses che descrivono i dati “puliti” dentro l’app. Al minimo:

MeltingPoint(value, unit, source, notes)

Result(input_smiles, cid, iupac_name, melting_points, sources, created_at)
Sono il contratto interno delle funzioni: tutto passa attraverso queste strutture, come indicato nella roadmap 

roadmap_project

.

rdkit_utils.py
Roba RDKit di basso livello:

validazione SMILES

conversione in Molecola RDKit

scrittura SDF con proprietà (IUPAC ecc.).
È lo strato “chimico”: normalizza e serializza la struttura verso file structure.sdf (flusso MVP esplicitato nella roadmap) 

roadmap_project

.

pubchem.py
Parla con PubChem PUG-REST/PUG-View:

da SMILES → CID

recupera IUPAC name

estrae Melting Point dalle “Experimental Properties” quando c’è
Ritorna un Result completo + URL sorgenti (così tracci la provenienza, come consigliato) 

roadmap_project

.

io_utils.py
I/O di alto livello:

safe_name() per nomi di cartelle file-system-safe

write_outputs(result, base_dir="results") che crea results/<NomeComposto>/ e scrive:

metadata.json (riassunto, link, timestamp)

structure.sdf (da RDKit)

IUPAC.txt

melting_point.csv (può essere vuoto ma con header se il dato non c’è)
Questo è esattamente l’output pack definito nella roadmap (MVP) 

roadmap_project

.

Nota GUI: nella tua src/ non vedo ancora app_gui.py. Nella roadmap è previsto (PySimpleGUI: input SMILES → bottone “Search” → log/risultati) e lo script scripts/run_app.bat è pronto a lanciarlo. Quindi questo file è il pezzo mancante da implementare per avere la UI minimale descritta (Step “MVP GUI”) 

roadmap_project

. Finché non c’è, puoi comunque usare le funzioni via riga di comando o scrivere un main.py temporaneo.

Test

tests/test_pubchem.py
Smoke test: interroga PubChem con l’aspirina, controlla che iupac_name non sia vuoto e che l’output venga creato. È il canarino in miniera: se questo passa, l’MVP regge le basi definite in roadmap 

roadmap_project

.

Output runtime

results/
Qui finiscono i risultati per composto, es.:

results/Aspirin/
  metadata.json
  structure.sdf
  IUPAC.txt
  melting_point.csv


Il nome cartella viene da safe_name() (preferibilmente IUPAC). La roadmap dettaglia proprio questo layout e i file richiesti 

roadmap_project

.

Come “scorre” l’app (schema mentale)

Input (da GUI o CLI): SMILES

Validazione + parsing con RDKit (rdkit_utils)

Fetch su PubChem (pubchem) → Result

Scrittura ordinata su disco (io_utils)

Verifica automatica con pytest e in CI
Questo è il flusso MVP che la roadmap raccomanda, con estensioni future per NIST/NMRShiftDB/MassBank pianificabili senza rifattorizzare il cuore (adapter per nuove sorgenti) 
---