import numpy as np
import glob
import pandas as pd

from appareil import Appareil


def save_to_csv(dateArr, tempMat, posArr, tdeltaArr, folder):

    if folder[-1]=='/':
        folder = folder[:-1]
    pd.DataFrame(dateArr).to_csv("{}/date.csv".format(folder), header=False, index=False)
    pd.DataFrame(tdeltaArr).to_csv("{}/tdelta.csv".format(folder), header=False,index=False)
    pd.DataFrame(posArr).to_csv("{}/position.csv".format(folder), header=False,index=False)
    pd.DataFrame(tempMat).to_csv("{}/temperature.csv".format(folder), header=False,index=False)


def save_datalog_csv(dateArr, tdeltaArr, tempMat,folder,tlog):
    if folder[-1]=='/':
        folder = folder[:-1]
    pd.DataFrame(data=dateArr).to_csv("{}/{}_date.csv".format(folder,tlog), header=False, index=False)
    pd.DataFrame(data=tdeltaArr).to_csv("{}/{}_tdelta.csv".format(folder,tlog), header=False,index=False)
    pd.DataFrame(data=tempMat).to_csv("{}/{}_temperature.csv".format(folder,tlog), header=False,index=False)

def read_csv(folder, name=''):

    n = len(glob.glob(folder+'*.csv'))
    assert n>0, 'aucun fichiers csv dans ce répertoire : {}'.format(folder)

    dateArr = pd.read_csv(folder + 'date.csv', delimiter=';', header=None).values.flatten().astype(np.datetime64)

    tdeltaArr = pd.to_timedelta ( pd.read_csv(folder + 'tdelta.csv', delimiter=';', header=None).values.flatten() ).values

    tempMat = pd.read_csv(folder + 'temperature.csv', header=None).values


    if n == 3:

        return Appareil(date=dateArr, tdelta=tdeltaArr, temp=tempMat, isDatalogger=True, name=name)

    else:

        posArr = pd.read_csv(folder + 'position.csv', header=None).values.flatten()

        return Appareil(date=dateArr, tdelta=tdeltaArr, temp=tempMat, pos=posArr, isDatalogger=False, name=name)


# folder = 'csv/13_08_2021/DTS/'
# files = np.sort(glob.glob('data/13_08_2021/4061_Ch.01_ Fibre 01/2021_08/**/**/*.txt'))
# from read_files_charon3 import read_files_charon3
# dateArr, tempMat, posArr, tdeltaArr = read_files_charon3(files)
# save_to_csv(dateArr, tempMat, posArr, tdeltaArr, folder)
