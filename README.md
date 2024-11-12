# Trattamento di ambliopia e strabismo attraverso gamification e eye tracking con MediaPipe

Questo repository contiene il codice sorgente e la documentazione relativi al progetto di tesi triennale intitolato "Trattamento di ambliopia e strabismo attraverso gamification e eye tracking con MediaPipe". Il lavoro presentato mira a esplorare soluzioni innovative per il trattamento di ambliopia e strabismo nei bambini, utilizzando una combinazione di gamification e tecnologie avanzate di tracciamento oculare. Sono stati sviluppati due giochi interattivi, **Brick Breaker** e **Memory**, progettati per migliorare l'aderenza al trattamento visivo rispetto ai metodi tradizionali, attraverso un'esperienza terapeutica coinvolgente e dinamica.

## Abstract

L’ambliopia e lo strabismo sono disturbi visivi che in età pediatrica possono essere causa di deficit visivi significativi irreversibili. Spesso trattati con metodi tradizionali come l’uso di occlusori ed esercizi visivi ripetitivi, tali approcci sorono di una bassa aderenza da parte dei pazienti, specialmente a causa della monotonia e del disagio sociale. Le tecnologie di tracciamento oculare e la gamification rappresentano un’alternativa promettente, ma non sono ancora ampiamente utilizzate nella terapia visiva.

Due giochi, nello specifico Brick Breaker e Memory, sono stati sviluppati utilizzando MediaPipe, una piattaforma per la rapida prototipazione di applicazioni basate su Machine Learning che include soluzioni per il rilevamento degli occhi e il tracciamento oculare. I giochi proposti in questo studio orono una terapia più interattiva e meno invasiva, coinvolgendo i bambini attraverso un’esperienza ludica. La ricerca ha valutato l’ecacia del sistema tramite due sondaggi, uno sull’accessibilità e l’usabilità dei giochi, e l’altro sull’atteggiamento dei genitori verso la gamification.

I risultati mostrano che il sistema è stato giudicato intuitivo e semplice da utilizzare, e i giochi sono stati apprezzati per la loro capacità di mantenere alto l’interesse durante le sessioni di trattamento. Inoltre, i genitori hanno espresso un giudizio positivo sull’integrazione della gamification nel trattamento, ritenendola utile per migliorare la motivazione dei bambini. Tuttavia, sono emerse alcune perplessità sulla durata dell’ecacia a lungo termine.

In conclusione, il sistema proposto ha arontato con successo i limiti dei metodi tradizionali migliorando l’aderenza al trattamento attraverso un approccio più dinamico e interattivo, aprendo nuove possibilità per la riabilitazione visiva.

## Contenuti del Repository

Questo repository include:

- **Codice sorgente**: i giochi **Brick Breaker** e **Memory**, sviluppati in Python con MediaPipe per il tracciamento oculare e Pygame per la grafica e l'interazione;
- **Tesi**: versione PDF della tesi;
- **Presentazione**: le slide PowerPoint utilizzate per la discussione.

## Requisiti

Per eseguire i giochi, è necessario installare le seguenti librerie Python:

- **MediaPipe**: una libreria per il machine learning e il tracciamento oculare;
- **Pygame**: una libreria per lo sviluppo di giochi in Python;
- **OpenCV**: una libreria per la computer vision;
- **PyAutoGUI**: una libreria per il controllo del mouse e della tastiera.

Per installare queste librerie, puoi utilizzare `pip`:

```bash
pip install mediapipe pygame opencv-python pyautogui
