from timetable import *

horario, horario_reab = timetableClean("C:/Users/Bruno/Coding/JupyterNotebooks/Outros/enfjun'23.csv", "JanEnf'23")

for key in horario.keys():
    print(f'{key}: {horario[key]},')

for key in horario_reab.keys():
    print(f'{key}: {horario_reab[key]},')
