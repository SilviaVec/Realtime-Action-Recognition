import sys
import os
import simplejson
import numpy as np
import functools
import pickle
import csv
import cv2


if True:  # Include project path
    import sys
    import os
    ROOT = os.path.dirname(os.path.abspath(__file__))+"/../"
    CURR_PATH = os.path.dirname(os.path.abspath(__file__))+"/"
    sys.path.append(ROOT)

    from utils.lib_classifier import ClassifierOnlineTest
    from utils.lib_skeletons_io import load_skeleton_data
    import utils.lib_commons as lib_commons

    
def remove_skeletons_with_few_joints(skeletons):                              
    ''' Remove bad skeletons before sending to the tracker '''
    good_skeletons = []
    px = skeletons[3:(3+13*3):3]
    py = skeletons[4:(3+13*3):3]
    num_valid_joints = len([x for x in px if x != 0])
    num_leg_joints = len([x for x in px[-6:] if x != 0])
    total_size = max(py) - min(py)
    # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    # IF JOINTS ARE MISSING, TRY CHANGING THESE VALUES:
    # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    if num_valid_joints >= 5 and total_size >= 0.1 and num_leg_joints >= 0:
        # add this skeleton only when all requirements are satisfied
        good_skeletons.append(skeletons)
    return good_skeletons


def getXYZandName_lifting(f1):                                            
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

    ordine=[1,0,9,10,11,3,4,5,12,13,14,6,7,8,16,15,18,17]

    coordsNew= []

    indici= range(0,18)
    for i in indici:
        coordsNew.append(coords[ordine[i]*3])
        coordsNew.append(coords[ordine[i]*3+1])
        coordsNew.append(coords[ordine[i]*3+2])
    for element in coordsNew:
        stringaOut = stringaOut + ", " + (str(element))
    
    univocName=ll.get("univTime")
    return coordsNew, univocName

cfg_all = lib_commons.read_yaml(ROOT + "config/config.yaml")

WINDOW_SIZE = int(cfg_all["features"]["window_size"])
ROOT = os.path.dirname(os.path.abspath(__file__))+"/../"
sys.path.append(ROOT)

ROOTOutput = ROOT + "output/"
if not os.path.exists(ROOTOutput):
    os.makedirs(ROOTOutput)

SRC_MODEL_PATH = ROOT + "/model/trained_classifier.pickle"
# classes = ['sit', 'stand', 'walk', 'meal']
classes = ['sit', 'stand', 'walk']
filepath = ROOT+"data_test/"

path, dirs, files = next(os.walk(filepath+"TestVideo1"))
file_count = len(files)
test_file=[]
for i in range(1, file_count-1):
    test_file.append((str(i) + '.txt'))


'''# r=root, d=directories, f = files
for r, d, f in os.walk(filepath):
    for file in f:
        if file.endswith(".txt"):
            test_file.append(os.path.join(r, file))'''


contaFrame = 0
dict_id2skeleton = {}
id2label = {}
finale_contenuto = ""

create_classifier = ClassifierOnlineTest(SRC_MODEL_PATH, classes, WINDOW_SIZE, 0)

while (contaFrame < len(test_file)):
    fileDaAprire=str(test_file[contaFrame])
    nomeDaScrivere = str(contaFrame) 
    contaFrame = contaFrame+1     
    try:    
        with open(filepath+"TestVideo1/"+fileDaAprire, 'r') as f3: 
            # ll = simplejson.load(f3)  
            coordsxyz = getXYZandName_lifting(f3)
        f3.close() 
        
        if (coordsxyz== None):
            coordsxyz = "0"
            for i in range (0, 18):
                coordsxyz = coordsxyz + ", 0" 
        coordsxyz = coordsxyz[1:] 
        

        coordsxyz = coordsxyz.split(",")
        counter=0
        for elem in coordsxyz:
            coordsxyz[counter]=float(elem.strip())
            counter=counter+1

        coordsxyz_np = np.asarray(coordsxyz)
        coordsxyz_np = remove_skeletons_with_few_joints(coordsxyz_np)

        
        dict_id2skeleton = {0: coordsxyz_np}


        for id, skeleton in dict_id2skeleton.items():     
            id2label[contaFrame] = create_classifier.predict(skeleton)

        stringaOut =''
        finale_contenuto=''
        for element in coordsxyz:
            stringaOut = stringaOut + ", " + (str(element))
            
        contenuto = "[[["+ "0" + ", " + "\"" + " " + "\""  + str(stringaOut) + "]]]"
        
        if (finale_contenuto == ""):
            finale_contenuto = contenuto
        else:
            finale_contenuto = finale_contenuto + ", " + contenuto 

        '''nomeDaScrivere = ROOTOutput + "skeleton_for_test" + contaFrame + ".txt"

        daScrivere = open(nomeDaScrivere,"w")
        daScrivere.write(finale_contenuto)
        daScrivere.close()'''

    except IOError:
        id2label[contaFrame] = ""
        print ("Could not open file!")


actionPath = ROOTOutput + '/action.csv'


with open(actionPath, 'w') as f:
    for key in id2label.keys(): 
        f.write("%s, %s\n" % (key, id2label[key]))
counter=0


# resmeal = 0
resit = 0
resstand = 0
reswalk = 0
for key in id2label: 
    '''if id2label[key] == 'meal': 
        resmeal = resmeal + 1'''
    if id2label[key] == 'sit': 
        resit = resit + 1
    if id2label[key] == 'stand': 
        resstand = resstand + 1
    if id2label[key] == 'walk': 
        reswalk = reswalk + 1

# print("frame of meal = ",resmeal)
print("frame of sit = ",resit)
print("frame of stand = ",resstand)
print("frame of walk = ",reswalk)

newarray=[]
lenLable = len(id2label)

for i in range(1, lenLable-90, 90):
    for num in range (i-1, i+89):
        newarray.append(id2label[num+1])
    n_sit = 0
    n_stand = 0
    n_walk = 0
    # n_meal =0
    for y in range(i-1, i+89):
        if newarray[y] == 'sit': 
            n_sit = n_sit + 1
        if newarray[y] == 'stand': 
            n_stand = n_stand + 1
        if newarray[y] == 'walk': 
            n_walk = n_walk + 1 
        ''' if newarray[y] == 'meal': 
            n_meal = n_meal + 1''' 
    # massimo = max(n_sit, n_stand, n_walk, n_meal)
    massimo = max(n_sit, n_stand, n_walk)
    if massimo == n_sit: 
        for rg in range(i, i+90):
            id2label[rg] = 'sit'
    if massimo == n_stand:
        for rg in range(i, i+90):
            id2label[rg] = 'stand'
    if massimo == n_walk: 
        for rg in range(i, i+90):
            id2label[rg] = 'walk' 
    ''' if massimo == n_meal: 
        for rg in range(i, i+90):
            id2label[rg] = 'meal'
            '''
            

actionPath_stabilizzato = ROOTOutput + '/action_stabilizzato.csv'


with open(actionPath_stabilizzato, 'w') as f:
    for key in id2label.keys(): 
        f.write("%s, %s\n" % (key, id2label[key]))

# resmeal = 0
resit = 0
resstand = 0
reswalk = 0
for key in id2label: 
    ''' if id2label[key] == 'meal': 
        resmeal = resmeal + 1''' 
    if id2label[key] == 'sit': 
        resit = resit + 1
    if id2label[key] == 'stand': 
        resstand = resstand + 1
    if id2label[key] == 'walk': 
        reswalk = reswalk + 1

# print("frame of meal = ",resmeal)
print("frame of sit = ",resit)
print("frame of stand = ",resstand)
print("frame of walk = ",reswalk)

            
        
cap = cv2.VideoCapture(ROOT + '/data_test/Video1.mp4')
fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter('outputwithaction_stabilizzato.avi',cv2.VideoWriter_fourcc(*'DIVX'), 30, (848,478))
actioncount = 1


contatore_frame = 0
while (cap.isOpened()):
    ret, frame = cap.read()
    if (contatore_frame > 150):                                     #150 perchè nei primi 150 frame del video1 non c'è nessuna persona
        if(actioncount < lenLable - 1):
            azione = id2label[actioncount]
            cv2.putText(frame, azione, (50, 50), cv2.FONT_HERSHEY_SIMPLEX , 1, (0, 255, 0), 2, cv2.LINE_AA)
            # cv2.imshow('frame',frame)
            out.write(frame)
            actioncount = actioncount+1
        else:
            break
    else:
        contatore_frame = contatore_frame +1

out.release()
cap.release()
cv2.destroyAllWindows()  

    