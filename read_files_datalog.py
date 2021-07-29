import numpy as np

from read_files_DTS import read_files_dts

def read_datalogger(file):
    header=11
    dateArr = np.genfromtxt(file, skip_header=header, dtype=str, delimiter=',', usecols=1)
    dateArr = np.array(list(map( lambda x: np.datetime64( x.replace('/','-').replace(' ', 'T') ) , dateArr ) ))
    tempArr = np.genfromtxt(file, skip_header=header, dtype=np.float, delimiter=',', usecols=2)
    tdeltaArr = np.array(list(map(lambda x: x - dateArr.min() , dateArr)))
    return dateArr, tempArr, tdeltaArr
