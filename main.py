import glob
import pandas as pd
import numpy as np
from read_files_DTS import read_files_dts
from read_files_datalog import read_datalogger
from read_files_DSTS import read_files_dsts

from graph import moy_pos

file='data/28_07_2021/datalog.csv'
dateArr, tempArr, tdeltaArr = read_datalogger(file)
a1 = ['datalog1', dateArr, tempArr, tdeltaArr]
pd.DataFrame(data = dateArr , columns=['%date']).to_csv("csv/datalog/date.csv", index=False, header=True, sep=';')
pd.DataFrame(data = tdeltaArr , columns=['%time']).to_csv("csv/datalog/time.csv", index=False, header=True, sep=';')
pd.DataFrame(data = tempArr , columns=['%temperature(m)']).to_csv("csv/datalog/temperature.csv", index=False, header=True, sep=';')

files_dts = np.sort(glob.glob('data/28_07_2021/data_juin_juil/Fibre 01 /2021/*.txt'))
dateArr, tempMat, posArr, tdeltaArr = read_files_dts(files_dts)
a2 = ['dts01', dateArr, tempMat, posArr, tdeltaArr ]

pd.DataFrame(data = dateArr , columns=['%date']).to_csv("csv/fibre01/date.csv", index=False, header=True, sep=';')
pd.DataFrame(data = tdeltaArr , columns=['%time']).to_csv("csv/fibre01/time.csv", index=False, header=True, sep=';')
pd.DataFrame(data = posArr , columns=['%position(m)']).to_csv("csv/fibre01/position.csv", index=False, header=True, sep=';')
# pd.DataFrame(data = tempMat, index=dateArr, columns=posArr).to_csv("csv/fibre01/temperature.csv", index=True, header=True, sep=';')
pd.DataFrame(data = tempMat).to_csv("csv/fibre01/temperature.csv", index=False, header=False, sep=';')


files_dts = np.sort(glob.glob('data/28_07_2021/data_juin_juil/Fibre 02/2021/*.txt'))
dateArr, tempMat, posArr, tdeltaArr = read_files_dts(files_dts)
a3 = ['dts02', dateArr, tempMat, posArr, tdeltaArr ]

pd.DataFrame(data = dateArr , columns=['%date']).to_csv("csv/fibre02/date.csv", index=False, header=True, sep=';')
pd.DataFrame(data = tdeltaArr , columns=['%time']).to_csv("csv/fibre02/time.csv", index=False, header=True, sep=';')
pd.DataFrame(data = posArr , columns=['%position(m)']).to_csv("csv/fibre02/position.csv", index=False, header=True, sep=';')
# pd.DataFrame(data = tempMat, index=dateArr, columns=posArr).to_csv("csv/fibre02/temperature.csv", index=True, header=True, sep=';')
pd.DataFrame(data = tempMat).to_csv("csv/fibre02/temperature.csv", index=False, header=False, sep=';')

df = pd.DataFrame(data = dateArr , columns=['date'])
df.date.dt.dayofweek.value_counts()

period = 24*60*60 # samples
f = 1/period
samples = np.arange(len(dateArr))*15*60 # 15 minutes
signal = np.sin(f * samples)

import matplotlib.pyplot as plt
plt.plot(dateArr, signal)
from scipy.signal import correlate
correlate(tem)
plt.show()
# FIGURE 0 : TOUS LES PROFILS DE TEMPÉRATURE
moy_pos(a1, a2, a3)

# # FIGURE 1 : PROFIL DE TEMPÉRATURE EN FONCTION DU TEMPS, MOYENNE SUR LA LONGUEUR DE LA FIBRE
# f = mean_pos(dateArr, tempMat)
# f.show()
#
# # FIGURE 2 : PROFIL DE TEMPÉRATURE EN FONCTION DE LA POSITION, SLIDER SUR LA DATE
# f = temp_at_time(posArr,tempMat,tdeltaArr,dateArr)
# f.show()
#
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
