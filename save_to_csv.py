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
