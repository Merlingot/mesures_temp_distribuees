import numpy as np
import pandas as pd
import glob


def read_date(file):
    nb=55
    with open(file) as f:
        f.seek(nb)
        d = f.readline()[4:-1]
    return np.datetime64( pd.to_datetime(d) )


def read_fileN(file, header):
    temp =  np.genfromtxt(file, skip_header=header,dtype=np.float,usecols=1)
    date = read_date(file)
    return date, temp

def read_file0(file, header):
    pos = np.genfromtxt(file, skip_header=header, dtype=np.float,usecols=0)
    temp =  np.genfromtxt(file, skip_header=header,dtype=np.float,usecols=1)
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


def read_files_dsts(files):
    header=32
    dateArr, tempMat, posArr = init_arrays(files, header)
    read_1by1(files, dateArr, tempMat, header)
    tdeltaArr = np.array(list(map(lambda x: x - dateArr.min() , dateArr.copy())))
    return dateArr, tempMat, posArr, tdeltaArr
