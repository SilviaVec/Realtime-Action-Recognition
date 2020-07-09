'''
s12 is the union of s1_get_skeletons_from_training_imgs.py and s2_put_skeleton_txt_to_a_single txt.py
Read the joint in a json file, write it in the correct form:
data = [7, 67, 7041, "stand", "stand_03-08-20-24-55-587/00055.jpg", 0.5670731707317073, 0.11005434782608697, 0.5670731707317073, 0.18342391304347827, 0.5182926829268293, 0.1875, 0.5030487804878049, 0.27309782608695654, 0.5030487804878049, 0.34239130434782605, 0.6189024390243902, 0.18342391304347827, 0.6310975609756098, 
            0.2649456521739131, 0.6310975609756098, 0.3342391304347826, 0.5365853658536586, 0.34646739130434784, 0.5335365853658537, 0.46467391304347827, 0.5335365853658537, 0.5747282608695652, 0.600609756097561, 0.34646739130434784,
            0.600609756097561, 0.4565217391304348, 0.5945121951219512, 0.5665760869565217, 0.5579268292682927, 0.10190217391304347, 0.5762195121951219, 0.09782608695652173, 0.5426829268292683, 0.11005434782608697, 0.5884146341463414, 0.11005434782608697, 0.5335365853658537, 0.46467391304347827, 0.5335365853658537, 
            0.5747282608695652, 0.600609756097561, 0.34646739130434784, 0.600609756097561, 0.4565217391304348, 0.5945121951219512, 0.5665760869565217, 0.5579268292682927, 0.10190217391304347,  0.5762195121951219, 0.09782608695652173, 0.5426829268292683, 0.11005434782608697, 0.5884146341463414, 0.11005434782608697] 

7041 = numero dei frame analizzati
67 = section analizzate 
7 = lable 

'''

import sys
import os
import simplejson
import numpy as np

def getXYZandName(ll, person_id):                                            
    mylist=ll.get("bodies")  
    if (len(mylist) < 1):
        return None, None
    listToStr = ' '.join([str(elem) for elem in mylist])                        # aggiunto

    coords = []
    check = 0

    x = listToStr.split("{")
    rng = range(1, len(x))
    for i in rng:
        x_sp = x[i].split(":")
        person_id_orig = x_sp[1].split(",")
        person_id_orig = person_id_orig[0]
        if(person_id_orig == person_id):
            x_coord = x_sp[2].split("[")
            x_coord = x_coord[1].split("]")
            coords=x_coord[0].split(",")
            check = 1
        if(check ==0):
            return None, None

    stringaOut =''

    zerotolen = range(0,len(coords))
    for i in zerotolen:
        coords[i]= float(coords[i])

    anticounter = range(18,-1,-1)
    for i in anticounter: 
        numero=coords[(4*i)-1]
        coords.remove(numero)

    coordsNew=[]
    ordine=[1,0,9,10,11,3,4,5,12,13,14,6,7,8,16,15,18,17]

    indici= range(0,18)
    for i in indici:
        coordsNew.append(coords[ordine[i]*3])
        coordsNew.append(coords[ordine[i]*3+1])
        coordsNew.append(coords[ordine[i]*3+2])
    for element in coordsNew:
        stringaOut = stringaOut + ", " + (str(element))

    univocName=ll.get("univTime")
    # print (stringaOut)
    return stringaOut, univocName

def getXYZandName_lifting(f1, person_id):                                            
    b = ""
    i = 0
    for line in f1:
        b=b+line
    temp = b.split("[")
    x = temp[3]
    x = x.replace(']', '')
    x = x.replace('\n', '')
    x = x.replace('(', '')
    x = x.strip()
    y = temp[4]
    y = y.replace(']', '')
    y = y.replace('\n', '')
    y = y.replace('(', '')
    y = y.strip()
    z = temp[5]
    z = z.replace(']', '')
    z = z.replace('\n', '')
    z = z.replace('(', '')
    z = z.strip()

    xvect = x.split(" ")
    while ('' in xvect):
        xvect.remove('')

    yvect = y.split(" ")
    while ('' in yvect):
        yvect.remove('')

    zvect = z.split(" ")
    while ('' in zvect):
        zvect.remove('')


    coordsNew = []
    ordine = [9 , 8 ,14 , 15 , 16 , 11, 12, 13 , 4 ,5 ,6 , 1 , 2 , 3 , 10, 10 ,10, 10]
    indici = range(0, 18)
    for i in indici:
        coordsNew.append(xvect[ordine[i]])
        coordsNew.append(yvect[ordine[i]])
        coordsNew.append(zvect[ordine[i]])
    stringaOut = ''
    for element in coordsNew:
        stringaOut = stringaOut + ", " + (str(element))
    return stringaOut
    
def CheckType(stringa):
    '''if 'jump' in stringa:
        return(1)

    if 'kick' in stringa: 
        return(2)
        
    if 'punch' in stringa: 
        return(3)
        
    if 'run' in stringa: 
        return(4)
        
    if 'sit' in stringa: 
        return(5)
        
    if 'squat' in stringa: 
        return(6)
        
    if 'stand' in stringa: 
        return(7)
        
    if 'walk' in stringa: 
        return(8)
        
    if 'wave' in stringa: 
        return(9)'''
    if 'sit' in stringa: 
        return(1)
        
    if 'stand' in stringa: 
        return(2)
        
    if 'walk' in stringa: 
        return(3)
    if 'meal' in stringa: 
        return(4)
    return 0


def getParametri(riga):
    if(len(riga)<10):
        riga=riga.split(" ")
        a = riga[0]
        b = riga[1]
        return int(a),int(b)

def getFolderName(riga):
    riga=riga.split(",")
    b = riga[1]
    c = riga[2]
    b = b.replace(' ', '')
    return b, c


ROOT = os.path.dirname(os.path.abspath(__file__))+"/../"
CURR_PATH = os.path.dirname(os.path.abspath(__file__))+"/githubs/Lable_video.txt"
sys.path.append(ROOT)

ROOTOutput = ROOT + "data_proc/raw_skeletons/skeleton_res/"
if not os.path.exists(ROOTOutput):
    os.makedirs(ROOTOutput)

filepath = ROOT+"dataset"

f= open(CURR_PATH,"r")


f1 = f.read().splitlines()

contaSection=0
contaFrame =0
FPS = 30
error = 0

lableList = ['sit', 'stand', 'walk', 'meal']

for line in f1:
    action = CheckType(line)
    if action != 0:
        azione=action
        nomeCart, person_id = getFolderName(line)
        filepathtemp = filepath + "/" + nomeCart
        nameAction = lableList[action-1]
    else:
        iniziale,finale=getParametri(line)
        if (nomeCart == '160422_haggling1' or nomeCart == '160906_band4' or nomeCart == '161029_sports1' or nomeCart == '170915_office1' or nomeCart == '171204_pose1'):
            iniziale = iniziale *FPS
            finale = finale *FPS
        contaSection=contaSection+1

        # count = INIZIALE    #QUI LO FACCIO ANDARE BENE PER I MIEI DATI
        while (iniziale < finale+1):
            name=str(iniziale)
            nomeDaScrivere = str(contaFrame - error)
            contaFrame = contaFrame+1   
            if (nomeCart == '160422_haggling1' or nomeCart == '160906_band4' or nomeCart == '161029_sports1' or nomeCart == '170915_office1' or nomeCart == '171204_pose1'):      
                while(len(name)<8):
                    name = "0" + name  #SERVE PERCHE LE FOTO SI CHIAMANO 00076
                fileDaAprire = filepathtemp + "/hdPose3d_stage1_coco19/body3DScene_" + name +".json"
            else:
                fileDaAprire = filepathtemp + "/" + name +".txt"
            try:
                with open(fileDaAprire, 'r') as f3:   
                    if (nomeCart == '160422_haggling1' or nomeCart == '160906_band4' or nomeCart == '161029_sports1' or nomeCart == '170915_office1' or nomeCart == '171204_pose1'):
                        ll = simplejson.load(f3)
                        coordsxyz, univocName = getXYZandName(ll, person_id)
                    else:
                        ll = f3
                        univocName = str(filepathtemp) + '_' + name
                        coordsxyz = getXYZandName_lifting(ll, person_id)
                f3.close()   
                if (coordsxyz== None):
                    coordsxyz = ', 0'* (54) 
                    
                contenuto = "[["+ str(azione) + ", " + str(contaSection) + ", " + str(contaFrame) + ", " + "\"" + str(nameAction) + "\"" + ", \"" + str(univocName) + "\"" + str(coordsxyz) + "]]"
                
                while(len(nomeDaScrivere)<8):
                    nomeDaScrivere = "0" + nomeDaScrivere  #SERVE PERCHE LE FOTO SI CHIAMANO 00076
                nomeDaScrivere = ROOTOutput + str(nomeDaScrivere) + ".json"
                daScrivere = open(nomeDaScrivere,"w")
                daScrivere.write(contenuto)
                daScrivere.close()
            
            except IOError:
                print ("Could not open file!")
                print (name, error)
                error = error +1

            iniziale=iniziale+1
    print(filepathtemp)

    
f.close() 

