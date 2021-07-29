import glob
import pandas as pd
import numpy as np
from read_files_DTS import read_files_dts
from read_files_datalog import read_datalogger
from read_files_DSTS import read_files_dsts

from graph import moy_pos,mean_pos,temp_at_time,temp_at_pos,surface_plot,traces, fig_pos

file='data/28_07_2021/datalog.csv'
dateArr, tempArr, tdeltaArr = read_datalogger(file)
a1 = ['datalog1', dateArr, tempArr, tdeltaArr]


files_dts = np.sort(glob.glob('data/28_07_2021/data_juin_juil/Fibre 01 /2021/*.txt'))
dateArr, tempMat, posArr, tdeltaArr = read_files_dts(files_dts)
a2 = ['dts01', dateArr, tempMat, posArr, tdeltaArr ]
a2_ = ['dts01', dateArr, tempMat[:,0], posArr, tdeltaArr ]

files_dts = np.sort(glob.glob('data/28_07_2021/data_juin_juil/Fibre 02/2021/*.txt'))
dateArr, tempMat, posArr, tdeltaArr = read_files_dts(files_dts)
posArr = posArr.max() - posArr
a3 = ['dts02', dateArr, tempMat, posArr, tdeltaArr ]
a3_ = ['dts02', dateArr, tempMat[:,0], posArr, tdeltaArr ]

# FIGURE 0 : TOUS LES PROFILS DE TEMPÉRATURE
f = moy_pos(a1, a2, a3)
f.show()

# FIGURE 0 : TOUS LES PROFILS DE TEMPÉRATURE
f = fig_pos(a1, a2_, a3_)
f.show()
# FIGURE 1 : PROFIL DE TEMPÉRATURE EN FONCTION DU TEMPS, MOYENNE SUR LA LONGUEUR DE LA FIBRE
f = mean_pos(dateArr, tempMat)
f.show()

# FIGURE 2 : PROFIL DE TEMPÉRATURE EN FONCTION DE LA POSITION, SLIDER SUR LA DATE
f = temp_at_time(posArr,tempMat,tdeltaArr,dateArr)
f.show()

# FIGURE 3: PROFIL DE TEMPÉRATURE EN FONCTION DE LA DATE, SLIDER SUR LA POSITION
f = temp_at_pos(posArr,tempMat,tdeltaArr,dateArr)
f.show()

# FIGURE 4 : SUPERPOSITION DES PROFILS DE TEMPÉRATURE LE LONG DE LA FIBRE, POUR TOUTES LES ACQUISITIONS
f = traces(posArr,tempMat,tdeltaArr,dateArr)
f.show()

# # FIGURE 5: SURFACE PLOT
f = surface_plot(posArr,tempMat,tdeltaArr,dateArr)
f.show()
