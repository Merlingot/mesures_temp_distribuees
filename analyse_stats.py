import glob
import pandas as pd
import numpy as np
from read_files_DTS import read_files_dts
from read_files_datalog import read_datalogger
from read_files_DSTS import read_files_dsts
import matplotlib.pyplot as plt
from graph import moy_pos,mean_pos,temp_at_time,temp_at_pos,surface_plot,traces
from scipy.signal import convolve2d,correlate,correlation_lags,butter,sosfilt
from csv_utils import *
import scipy.stats as stats
import seaborn as sns


folder='csv/13_08_2021/DTS/'
a = read_csv(folder, 'labo')
date,pos,temp,time = a.date,a.pos,a.temp,a.tdelta


# MOVING AVERAGE ###############################################################
def moving_average(x, w):
    x_padded = np.pad(x, (w//2, w-1-w//2), mode='edge')
    return np.convolve(x_padded, np.ones(w), 'valid') / w

def moving_average_2d(x, w_time, w_spatial):
    x_padded = np.pad(x, [(w_time//2, w_time-1-w_time//2), (w_spatial//2, w_spatial-1-w_spatial//2)], mode='edge')
    return convolve2d(x_padded, np.ones((w_time, w_spatial)), 'valid')/(w_time*w_spatial)

# Temporel : Mesures à chaque 2 minutes:
w_time = int(60/2) #average sur 60 minutes
# Spatial : Mesures à chaque 1 mètres:
w_spatial = int(2/1) #average sur 2 mètres
dts = moving_average_2d(temp, w_time,w_spatial)


# Plot la différence
# %matplotlib
df1 = pd.DataFrame(data=temp, columns=pos, index=date)
df2 = pd.DataFrame(data=dts, columns=pos, index=date)

fig,axs = plt.subplots(nrows=1, ncols=2, sharey=True, figsize=(17,12))
axs[0].set_title('Données brutes')
axs[0].set_ylabel('Date')
axs[0].set_xlabel('Position')
im=sns.heatmap(df1, ax=axs[0],center=0, cbar=False)
axs[1].set_title('Après filtre passe bas')
axs[1].set_xlabel('Position')
sns.heatmap(df2, ax=axs[1],center=0, cbar=False)
mappable = im.get_children()[0]
plt.colorbar(mappable, ax = [axs[0],axs[1]],orientation = 'horizontal')
plt.savefig('figures/filtre.png')

# SECTIONS ###############################################################
sections=['ch1', 'ch2', 'eau1', 'eau2', 'spool', 'four' ]

# On regarde les 40 premiers mètres
N=100
df = pd.DataFrame(data=dts[:,:N], columns=pos[:N], index=date)
sns.heatmap(df,center=20, cbar=True)




# n=10
# import matplotlib.pylab as pl
# colors = pl.cm.jet(np.linspace(0,1,n))
# plt.figure(figsize=(15,7))
# for i in range(n):
#     plt.plot(date,dts[:,i],color=colors[i], label=pos[i])
# plt.legend(title='Position')



















#
