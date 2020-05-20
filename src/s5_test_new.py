import sys
import os
import simplejson
import numpy as np
import functools
import pickle
import csv


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
    px = skeletons[3:3+13*3:3]
    py = skeletons[4:3+13*3:3]
    pz = skeletons[5:3+13*3:3]
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
classes = ['sit', 'stand', 'walk']
filepath = ROOT+"data_test/"

test_file = []


# r=root, d=directories, f = files
for r, d, f in os.walk(filepath):
    for file in f:
        if file.endswith(".json"):
            # print(os.path.join(r, file))
            test_file.append(os.path.join(r, file))


contaFrame = 0
dict_id2skeleton = {}
id2label = {}
finale_contenuto = ""

create_classifier = ClassifierOnlineTest(SRC_MODEL_PATH, classes, WINDOW_SIZE, 0)

while (contaFrame < len(test_file)):
    fileDaAprire=str(test_file[contaFrame])
    nomeDaScrivere = str(contaFrame) 
    contaFrame = contaFrame+1         
    with open(fileDaAprire, 'r') as f3:   
        ll = simplejson.load(f3)
        coordsxyz, univocName = getXYZandName(ll)
    f3.close()  
    if (coordsxyz== None):
        coordsxyz = ', 0'* (54) 

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


 
actionPath = ROOTOutput + '/action.csv'


with open(actionPath, 'w') as f:
    for key in id2label.keys(): 
        f.write("%s, %s\n" % (key, id2label[key]))

print((id2label))



    
    

    