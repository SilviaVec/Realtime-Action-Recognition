import sys
import os
import simplejson
import numpy as np
import functools
import pickle
if True:  # Include project path
    import sys
    import os
    ROOT = os.path.dirname(os.path.abspath(__file__))+"/../"
    CURR_PATH = os.path.dirname(os.path.abspath(__file__))+"/"
    sys.path.append(ROOT)

    from utils.lib_classifier import ClassifierOnlineTest
    from utils.lib_skeletons_io import load_skeleton_data


def getXYZandName(ll, person_id = ' 0'):                                            
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
    return coordsNew, univocName



WINDOW_SIZE = 0.5
ROOT = os.path.dirname(os.path.abspath(__file__))+"/../"
sys.path.append(ROOT)

ROOTOutput = ROOT + "output/"
if not os.path.exists(ROOTOutput):
    os.makedirs(ROOTOutput)

SRC_MODEL_PATH = ROOT + "/model/trained_classifier.pickle"
classes = ['sit', 'stand', 'walk']
filepath = ROOT+"data_test/"


iniziale = 809
finale = 814
contaFrame = 0

finale_contenuto = ""

while (iniziale < finale+1):
    name=str(iniziale)
    nomeDaScrivere = str(contaFrame)
    contaFrame = contaFrame+1           
    while(len(name)<8):
        name = "0" + name  #SERVE PERCHE LE FOTO SI CHIAMANO 00076
    fileDaAprire = filepath + "body3DScene_" + name +".json"
    with open(fileDaAprire, 'r') as f3:   
        ll = simplejson.load(f3)
        coordsxyz, univocName = getXYZandName(ll)
    f3.close()  
    if (coordsxyz== None):
        coordsxyz = ', 0'* (54) 

    create_classifier = ClassifierOnlineTest(SRC_MODEL_PATH, classes, WINDOW_SIZE, 0)
    create_classifier.reset()
    create_classifier.predict(coordsxyz)

    stringaOut =''
    finale_contenuto=''
    for element in coordsxyz:
        stringaOut = stringaOut + ", " + (str(element))
        
    contenuto = "[[["+ "0" + ", " + "\"" + " " + "\""  + str(stringaOut) + "]]]"
    
    if (finale_contenuto == ""):
        finale_contenuto = contenuto
    else:
        finale_contenuto = finale_contenuto + ", " + contenuto 

    nomeDaScrivere = ROOTOutput + "skeleton_for_test" + name + ".txt"

    daScrivere = open(nomeDaScrivere,"w")
    daScrivere.write(finale_contenuto)
    daScrivere.close()

    iniziale=iniziale+1







    
    

    