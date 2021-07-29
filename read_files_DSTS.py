import numpy as np
import pandas as pd
import glob
from graph import temp_at_time, temp_at_pos, mean_pos, traces, surface_plot

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
    headerDTS=32
    dateArr, tempMat, posArr = init_arrays(files, headerDTS)
    read_1by1(files, dateArr, tempMat, headerDTS)
    tdeltaArr = np.array(list(map(lambda x: x - dateArr.min() , dateArr.copy())))
    return dateArr, tempMat, posArr, tdeltaArr

# # dsts (OZ Optics) -------------------------------------------------------------
# files_dsts = np.sort(glob.glob('/Volumes/MARINOUILLE/dsts/*.tep'))[::100]
# dateArr, tempMat, posArr, tdeltaArr = read_files_dsts(files_dsts)
#
#
# # FIGURE 1 : PROFIL DE TEMPÉRATURE EN FONCTION DU TEMPS, MOYENNE SUR LA LONGUEUR DE LA FIBRE
# f = mean_pos(dateArr, tempMat)
# f.show()
#
# # FIGURE 2 : PROFIL DE TEMPÉRATURE EN FONCTION DE LA POSITION, SLIDER SUR LA DATE
# f = temp_at_time(posArr,tempMat,tdeltaArr,dateArr)
# f.show()
# # FIGURE 3: PROFIL DE TEMPÉRATURE EN FONCTION DE LA DATE, SLIDER SUR LA POSITION
# f = temp_at_pos(posArr,tempMat,tdeltaArr,dateArr)
# f.show()
#
# # FIGURE 4 : SUPERPOSITION DES PROFILS DE TEMPÉRATURE LE LONG DE LA FIBRE, POUR TOUTES LES ACQUISITIONS
# f = traces(posArr,tempMat,tdeltaArr,dateArr)
# f.show()
#
# # FIGURE 5: SURFACE PLOT
# f = surface_plot(posArr,tempMat,tdeltaArr,dateArr)
# f.show()
