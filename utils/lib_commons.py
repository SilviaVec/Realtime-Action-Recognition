''' This script defines some common functions '''

'''
Esempio:
data = [7, 67, 7041, "stand", "stand_03-08-20-24-55-587/00055.jpg", 0.5670731707317073, 0.11005434782608697, 0.5670731707317073, 0.18342391304347827, 0.5182926829268293, 0.1875, 0.5030487804878049, 0.27309782608695654, 0.5030487804878049, 0.34239130434782605, 0.6189024390243902, 0.18342391304347827, 0.6310975609756098, 
            0.2649456521739131, 0.6310975609756098, 0.3342391304347826, 0.5365853658536586, 0.34646739130434784, 0.5335365853658537, 0.46467391304347827, 0.5335365853658537, 0.5747282608695652, 0.600609756097561, 0.34646739130434784,
            0.600609756097561, 0.4565217391304348, 0.5945121951219512, 0.5665760869565217, 0.5579268292682927, 0.10190217391304347, 0.5762195121951219, 0.09782608695652173, 0.5426829268292683, 0.11005434782608697, 0.5884146341463414, 0.11005434782608697, 0.5335365853658537, 0.46467391304347827, 0.5335365853658537, 
            0.5747282608695652, 0.600609756097561, 0.34646739130434784, 0.600609756097561, 0.4565217391304348, 0.5945121951219512, 0.5665760869565217, 0.5579268292682927, 0.10190217391304347,  0.5762195121951219, 0.09782608695652173, 0.5426829268292683, 0.11005434782608697, 0.5884146341463414, 0.11005434782608697] 

7041 = numero dei frame analizzati
67 = section analizzate 
7 = lable 

'''


import numpy as np
import cv2
import math
import time
import os
import glob
import yaml
import datetime
from os import listdir
from os.path import isfile, join
import functools
import simplejson


def getXYZandName(ll)                                               #ADDED
    mylist=ll.get("bodies")
    listToStr = ' '.join([str(elem) for elem in mylist]) 

    x = listToStr.split("[")
    x = x[1].split("]")
    coords=x[0].split(",")

    zerotolen = range(0,len(coords))
    for i in zerotolen:
        coords[i]= float(coords[i])

    anticounter = range(18,-1,-1)
    for i in anticounter: 
        numero=coords[(4*i)-1]
        coords.remove(numero)

    coordsNew=[]
    ordine=[1,16,15,18,17,3,9,4,10,5,11,6,12,7,13,8,14]

    indici= range(0,16)
    for i in indici:
        coordsNew.append(coords[ordine[i]*3])
        coordsNew.append(coords[ordine[i]*3+1])
        coordsNew.append(coords[ordine[i]*3+2])

    univocName=ll.get("univTime")
    return coordsNew, univocName


def int2str(num, idx_len):
    return ("{:0"+str(idx_len)+"d}").format(num)


def save_listlist(filepath, ll):
    ''' Save a list of lists to file '''
    folder_path = os.path.dirname(filepath)
    os.makedirs(folder_path, exist_ok=True)
    with open(filepath, 'w') as f:
        simplejson.dump(ll, f)


def read_listlist(filepath):
    ''' Read a list of lists from file '''
    with open(filepath, 'r') as f:   
        ll = simplejson.load(f)
        coordsxyz, univocName = getXYZandName(ll)                         #TODO mettere anche i rimanenti 3 numeri davanti (vedi esempio in alto)
        return ll


def read_yaml(filepath):
    ''' Input a string filepath, 
        output a `dict` containing the contents of the yaml file.
    '''
    with open(filepath, 'r') as stream:
        data_loaded = yaml.safe_load(stream)
    return data_loaded


def get_filenames(path, use_sort=True, with_folder_path=False):
    ''' Get all filenames under certain path '''
    fnames = [f for f in listdir(path) if isfile(join(path, f))]
    if use_sort:
        fnames.sort()
    if with_folder_path:
        fnames = [path + "/" + f for f in fnames]
    return fnames


def get_time_string():
    ''' Get a formatted string time: `month-day-hour-minute-seconds-miliseconds`,
        such as: `02-26-15-51-12-106`.
    '''
    s = str(datetime.datetime.now())[5:].replace(
        ' ', '-').replace(":", '-').replace('.', '-')[:-3]
    return s
