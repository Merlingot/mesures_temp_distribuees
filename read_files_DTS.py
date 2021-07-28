import numpy as np
import glob
import plotly.graph_objects as go
from graph import temp_at_time, temp_at_pos, mean_pos, traces


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
    headerDTS=8
    dateArr, tempMat, posArr = init_arrays(files, headerDTS)
    read_1by1(files, dateArr, tempMat, headerDTS)
    tdeltaArr = np.array(list(map(lambda x: x - dateArr.min() , dateArr.copy())))
    return dateArr, tempMat, posArr, tdeltaArr



# dts (LIOS) -------------------------------------------------------------------
files_dts = np.sort(glob.glob('/Volumes/MARINOUILLE/dts_28_07_2021/data/Controller/4061/Fibre 02/2021/*.txt'))
dateArr, tempMat, posArr, tdeltaArr = read_files_dts(files_dts)


# FIGURE 1 : PROFIL DE TEMPÉRATURE EN FONCTION DU TEMPS, MOYENNE SUR LA LONGUEUR DE LA FIBRE
f = mean_pos(dateArr, tempMat)
f

# FIGURE 2 : PROFIL DE TEMPÉRATURE EN FONCTION DE LA POSITION, SLIDER SUR LA DATE
f = temp_at_time(posArr,tempMat,tdeltaArr,dateArr)
f
# FIGURE 3: PROFIL DE TEMPÉRATURE EN FONCTION DE LA DATE, SLIDER SUR LA POSITION
f = temp_at_pos(posArr,tempMat,tdeltaArr,dateArr)
f

# FIGURE 4 : SUPERPOSITION DES PROFILS DE TEMPÉRATURE LE LONG DE LA FIBRE, POUR TOUTES LES ACQUISITIONS
f = traces(posArr,tempMat,tdeltaArr,dateArr)
f

# FIGURE 5: SURFACE PLOT
f = surface_plot(posArr,tempMat,tdeltaArr,dateArr)
f
