# Trip Planner
Progetto per il corso di Ingegneria della Conoscenza (ICON) AA. 2023-24

# Installazione
1. Installare il programma SWI-Prolog eseguendo il file ```swipl-9.2.0-1.x64.exe``` nella cartella ```requirements``` del progetto.
    * Durante l'installazione assicurarsi di spuntare la scelta di inserire la variabile d'ambiente di SWI-Prolog in PATH
2. Installare la libreria pyswip con il comando ```pip install git+https://github.com/yuce/pyswip@master#egg=pyswip```
3. Se necessario modificare il file ```C:\Python\Python36\Lib\site-packages\pyswip\core.py``` alla riga 180:<br>
    * ```r'pl\bin'``` -> ```r'swipl\bin'```
4. Tutte le altre librerie richieste dal software possono essere installate in modo classico

N.B. Il programma è stato testato con Python 3.11.4 e con le versioni sopracitate di SWI-Prolog e pyswip, non si assicura il corretto funzionamento con versione diverse di python o di tali librerie.