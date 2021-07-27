import numpy as np
import pandas as pd
import glob


def read_datalogger(file):
    header=11
    dateArr = np.genfromtxt(file, skip_header=header, dtype=str, delimiter=',', usecols=1)
    dateArr = np.array(pd.to_datetime(dateArr))
    tempArr = np.genfromtxt(file, skip_header=header, dtype=np.float, delimiter=',', usecols=2)
    tdeltaArr = np.array(list(map(lambda x: x - dateArr.min() , dateArr.copy())))
    return dateArr, tempArr, tdeltaArr


# file='datalogger.csv'
# dateArr, tempArr, tdeltaArr = read_datalogger(file)
