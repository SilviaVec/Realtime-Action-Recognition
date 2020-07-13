import sys
import os
import csv

ROOT = os.path.dirname(os.path.abspath(__file__))+"/../"
sys.path.append(ROOT)
ROOTOutput = ROOT + "output/"
actionPath_stabilizzato = ROOTOutput + 'action_stabilizzato.csv'

b=[]
for a in range(0, 3*30):
    b.append("not visible")
for a in range(3*30+1, 17*30):
    b.append("walk")
for a in range(17*30+1, 23*30):
    b.append("stand")
for a in range(23*30+1, 26*30):
    b.append("walk")
for a in range(26*30+1, 40*30):
    b.append("sit")
for a in range(40*30+1, 69*30):
    # b.append("meal")
    b.append("sit")
for a in range(69*30+1, 73*30):
    b.append("walk")
for a in range(73*30+1, 77*30):
    b.append("stand")
for a in range(77*30+1, 92*30):
    b.append("walk")

giusta_previsione = 0
sbagliata_previsione= 0
with open(actionPath_stabilizzato) as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    for row in csv_reader:       
        # print(f'\t{row[0]} {row[1]} ')
        if (line_count > 150):            #150 perchè nei primi 150 frame del video1 non c'è nessuna persona
            if (row[1].strip() == b[line_count]):
                giusta_previsione = giusta_previsione +1
            else:
                sbagliata_previsione = sbagliata_previsione +1
        line_count += 1

print(((giusta_previsione/(giusta_previsione+sbagliata_previsione)*100)))
print(((sbagliata_previsione/(giusta_previsione+sbagliata_previsione)*100)))



