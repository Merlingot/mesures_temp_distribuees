import numpy as np
import matplotlib.pyplot as plt
import glob


def read_fileN(file,header):
    temp =  np.genfromtxt(file, skip_header=header+2, max_rows=1,dtype=np.float)[2:]
    date = np.genfromtxt(file, skip_header=header+1, max_rows=1,usecols=0,dtype=np.datetime64).astype(np.datetime64)
    return date, temp

def read_file0(file,header):
    pos = np.genfromtxt(file, skip_header=header, max_rows=1,dtype=np.float)
    temp =  np.genfromtxt(file, skip_header=header+2, max_rows=1, dtype=np.float)[2:]
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


def read_files_dts(files):
    headerDTS=8
    dateArr, tempMat, posArr = init_arrays(files, headerDTS)
    read_1by1(files, dateArr, tempMat, headerDTS)
    tdeltaArr = np.array(list(map(lambda x: x - dateArr.min() , dateArr.copy())))
    return dateArr, tempMat, posArr, tdeltaArr

# dts (LIOS) -------------------------------------------------------------------
# files_dts = np.sort(glob.glob('/Volumes/MARINOUILLE/dts/s/Controller/4061/Fibre 02/2021/*.txt'))[::100]
# dateArr, tempMat, posArr, tdeltaArr = read_files_dts(files_dts)
