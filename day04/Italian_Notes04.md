
# alcune note:
- inlcudi OS del pc e versione di aggiornamento del pc, importante per bug resolution, se sono dipendenti dal codice o dal pc per se
- includi anche la lingua del OS
- versione di py
- folder __pycache__ va rimosso da git, e si aggiunge un .gitignore

```bash
git status
git add .gitignore
git commit -m "remove __pycache__" # o qualcosa del genere
```
- posso fargli evitare al git commit anche tutti i csv per esempio. o qualsiasi cosa voglio aggiungere nel suo file gitignore 
- in pytest (guarda bene che puoi fare)
- come fare con conda a creare tutti i documenti come su uv? che crea automaticamente readme.md; file toml, .python-version
- librerie scientifiche
- web scraping (bot che download roba da siti internet)-> API
- librerie di py che interagiscono con API
- differenza tra FASTA e json files (soprattutto nelle librerie genetiche), per manipolazioni poi su i dati estratti quale è meglio
- cosa è IDE? mypy?
- diff tra
```py
try....
except
# da cosa differisce con il loop IF
```
- dictionaries come creare (hanno kew value pairs), e in cosa sono differenti rispetto alle liste

## assignment
- prendi un database (es chembl) e scrivi un programma (con main separato, uno per l'interazione con l'user e uno per il database) 
- importante fai in modo che l'email e la chiave API sia in un file separato che non viene portato su github