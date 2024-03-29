import numpy as np
import glob
from graph import temp_at_time, temp_at_pos, mean_pos, traces, surface_plot


def read_fileN(file,header):
    temp =  np.genfromtxt(file, skip_header=header+2, max_rows=1,dtype=np.float)[2:]
    date = np.genfromtxt(file, skip_header=header+1, max_rows=1,usecols=0,dtype=str).astype(np.datetime64).item()
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
    header=8
    dateArr, tempMat, posArr = init_arrays(files, header)
    read_1by1(files, dateArr, tempMat, header)
    tdeltaArr = np.array(list(map(lambda x: x - dateArr.min() , dateArr.copy())))
    return dateArr, tempMat, posArr, tdeltaArr
