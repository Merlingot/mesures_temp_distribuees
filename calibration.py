import glob
import pandas as pd
import numpy as np
from read_files_DTS import read_files_dts
from read_files_datalog import read_datalogger
from read_files_DSTS import read_files_dsts
import matplotlib.pyplot as plt
from graph import moy_pos,mean_pos,temp_at_time,temp_at_pos,surface_plot,traces, fig_pos

file='data/28_07_2021/datalogger/tlog1.csv'
dateArr, tempArr, tdeltaArr = read_datalogger(file)
a1 = ['datalog1', dateArr, tempArr, tdeltaArr]

file='data/backscattering/0706.txt'
pos = np.genfromtxt(file, skip_header=2, usecols=(0), delimiter=';')
level = np.genfromtxt(file, skip_header=2, usecols=(1),delimiter=';')

from scipy.signal import find_peaks
from scipy.signal import savgol_filter
xf = savgol_filter(level, 5, 2, deriv=2)
peaks1, _ = find_peaks(xf, prominence=0.1)
peaks2, _ = find_peaks(-1*xf, prominence=0.1)
plt.plot(pos, level)
plt.plot(pos[peaks1], level[peaks1], "x")
plt.plot(pos[peaks2], level[peaks2], "x")
plt.show()

t0706 = 300
t1 = tempMat1[t0706]
t2 = tempMat2[t0706]

plt.plot(pos, level)
plt.plot(posArr1, t1)
plt.plot(posArr2, t2)
plt.legend(['backscattering', 'dts - extrémité 1', 'dts - extrémité 2'])
plt.xlabel('position (m)')

files_dts1 = np.sort(glob.glob('data/28_07_2021/DTS/Fibre 01 /2021/*.txt'))
dateArr1, tempMat1, posArr1, tdeltaArr1 = read_files_dts(files_dts1)

files_dts2 = np.sort(glob.glob('data/28_07_2021/DTS/Fibre 02/2021/*.txt'))
dateArr2, tempMat2, posArr2, tdeltaArr2 = read_files_dts(files_dts2)
posArr2 = posArr2.max() - posArr2
