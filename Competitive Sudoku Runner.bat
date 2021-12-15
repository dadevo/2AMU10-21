set pythonLoc=C:\Users\Dadevo\AppData\Local\Programs\Python\Python38\python.exe
set appLoc=C:\Users\Dadevo\Documents\GitHub\2AMU10-21\simulate_game.py

set P1=team21_A2
set P2=greedy_player
set board=boards/random-3x3.txt
set time=5

%pythonLoc% %appLoc% --first=%P1% --second=%P2% --board=%board% --time=%time%
pause