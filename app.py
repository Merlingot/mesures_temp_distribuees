import pandas as pd
import glob
import numpy as np
import matplotlib.pyplot as plt
from fonctions import *
from graph import *
import time
from plotly.subplots import make_subplots
import plotly.graph_objects as go


# dts --------------------------------------------------------------------------
files = np.sort(glob.glob('/Volumes/MARINOUILLE/dts/s/Controller/4061/Fibre 02/2021/*.txt'))
len(files)
ntime=100; npos=100
pos0, temp0, time0, dates0 = read_files_dts(files, ntime, npos)
dts = (pos0,temp0,time0,dates0)
# dsts  ------------------------------------------------------------------------
L=4359
files = np.sort(glob.glob('/Volumes/MARINOUILLE/*.tep'))
ntime=100; npos=50
pos1, temp1, time1, dates1 = read_files_dsts(files, L, ntime, npos)
dsts = (pos1,temp1,time1,dates1)
# datalogger  ----------------------------------------------------------------
file='datalogger.csv'
temp2, time2, dates2 = read_datalogger(file)
dl = (temp2, time2, dates2)
# Figures ----------------------------------------------------------------------


fig = surface_time_plot(dsts, name='DSTS')
fig.show()
