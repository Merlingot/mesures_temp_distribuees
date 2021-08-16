import numpy as np
import glob
import pandas as pd

def read_fileN(file, header):
    with open(file,encoding='ISO-8859-1') as f:
        date = f.readline()[2:-1]
    datetime = np.datetime64(date[:10] + 'T' + date[11:11+2] + ':' + date[14:14+2] + ':' + date[17:17+2])
    temp = np.genfromtxt(file, skip_header=header, usecols=(1), encoding='ISO-8859-1')
    return datetime, temp

def read_file0(file, header):
    pos = np.genfromtxt(file, skip_header=header, usecols=(0), encoding='ISO-8859-1')
    temp = np.genfromtxt(file, skip_header=header, usecols=(1), encoding='ISO-8859-1')
    assert len(temp)==len(pos), 'len(temp):{} != len(pos):{}'.format(len(temp),len(pos))
    return pos

def init_arrays(files, header):
    posArr = read_file0(files[0],header) #file[0] is a random file
    Ntime = len(files)
    Npos = len(posArr)
    tempMat = np.zeros([Ntime, Npos]) #indexation time, pos
    dateArr = np.zeros([Ntime], dtype='O')
    return dateArr, tempMat, posArr

def read_1by1(files, dateArr, tempMat, header):
    for N in range(len(files)):
        date, temp = read_fileN(files[N],header)
        dateArr[N] = date
        tempMat[N,:] = temp

def read_files_charon3(files):
    header=3
    dateArr, tempMat, posArr = init_arrays(files, header)
    read_1by1(files, dateArr, tempMat, header)
    tdeltaArr = np.array(list(map(lambda x: x - dateArr.min() , dateArr.copy())))
    return dateArr, tempMat, posArr, tdeltaArr
