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


folder='csv/13_08_2021/DTS/'
a = read_csv(folder, 'labo')
date,pos,temp,time = a.date,a.pos,a.temp,a.tdelta


# MOVING AVERAGE:
def moving_average(x, w):
    x_padded = np.pad(x, (w//2, w-1-w//2), mode='edge')
    return np.convolve(x_padded, np.ones(w), 'valid') / w

def moving_average_2d(x, w_time, w_spatial):
    x_padded = np.pad(x, [(w_time//2, w_time-1-w_time//2), (w_spatial//2, w_spatial-1-w_spatial//2)], mode='edge')
    return convolve2d(x_padded, np.ones((w_time, w_spatial)), 'valid')/(w_time*w_spatial)

# Mesures à chaque 2 minutes:
w_time = int(60/2) #average sur 60 minutes
# Mesures à chaque 1 mètres:
w_spatial = int(2/1) #average sur 2 mètres
new_temp = moving_average_2d(temp, w_time,w_spatial)


plt.figure()
plt.title('Application Moving Average sur les mesures DTS')
plt.plot(temp[:,490])
plt.plot(new_temp[:,490])
plt.ylabel('Température (C)')
plt.xlabel('# Sample')
plt.legend(['signal brut', 'signal filtré'])

# choisir un sample dans les données du DTS
sample = temp[:,480]
# FILTRE PASSE BAS POUR ENLEVER LE BRUIT : LE FOUR CHANGE DE TMEPÉRATURE À CHAQUE HEURE: ON FILTRE LES DONNÉES QUI ONT DES FRÉQUENCES PLUS RAPIDES
sos = butter(2, 1/(60*60), 'lp', fs=1/(120), output='sos')
samplef = sosfilt(sos, sample)

plt.figure()
plt.title('Application filtre passe bas sur les mesures DTS')
plt.plot(sample)
plt.plot(samplef )
plt.plot(new_temp[:,490])
plt.ylabel('Température (C)')
plt.xlabel('# Sample')
plt.legend(['signal brut', 'signal filtré LP', 'signal filtré MA'])


# CORRELATION MESURES FOUR
# Lire data du four
dtoven = pd.to_timedelta ( pd.read_csv('csv/13_08_2021/four/dt_four24h.csv',header=None).values.flatten() ).values
oven = pd.read_csv('csv/13_08_2021/four/temp_four24h.csv',header=None).values.flatten()
doven  = date[0] + dtoven
signal_date = np.concatenate( [ doven, doven + np.timedelta64(1, 'D'), doven + np.timedelta64(2, 'D') ] )
signal = np.concatenate( [oven,oven,oven])


# Up sample les données du four
from scipy import interpolate
dt = (signal_date - signal_date[0]).astype(np.float)/1e9 #secondes
f = interpolate.interp1d(dt, signal)
dt_upsample = (date - date[0])
signal_upsample = f(dt_upsample)

# CORRÉLATION
signal_noise = new_temp[:,490]
corr = correlate(signal_noise,signal_upsample)
lags = correlation_lags(len(signal_upsample), len(signal_noise))*2 #minutes
corr /= np.max(corr)
n = int(len(lags)/2)


fig, (ax_noise, ax_corr) = plt.subplots(2, 1, figsize=(10, 5))
ax_noise.plot(date, signal_noise,label='mesure DTS')
ax_noise.plot(date,signal_upsample,label='Four')
ax_noise.legend()
ax_noise.set_title('Signaux')
ax_noise.set_xlabel('Date (mois-jour heure)')
ax_corr.plot(lags[n-100:n+100], corr[n-100:n+100])
ax_corr.axvline(lags[np.argmax(corr)], color='k', linestyle='--')
ax_corr.set_title('Corrélation croisée')
ax_corr.set_xlabel('Lag (minutes)')
ax_noise.margins(0, 0.1)
ax_corr.margins(0, 0.1)
fig.tight_layout()
plt.show()

def crosscorr(d1, d2, lag):
    return stats.pearsonr(d1, np.roll(d2, lag))[0]

d1 = signal_noise
d2 = signal_upsample
n = int(len(lags)/2)
lags_n = lags[n-100:n+100]
rs = [ crosscorr(d1, d2, lag) for lag in lags_n ]
offset = np.floor(len(rs)/2)-np.argmax(rs)


fig, (ax_noise, ax_corr) = plt.subplots(2, 1, figsize=(10, 5))
ax_noise.plot(date, signal_noise,label='Mesures DTS')
ax_noise.plot(date,signal_upsample,label='Four')
ax_noise.legend()
ax_noise.set_title('Signaux')
ax_noise.set_xlabel('Date (mois-jour heure)')
ax_noise.set_ylabel('Température (C)')
ax_corr.plot(lags_n, rs)
ax_corr.axvline(0,color='k',linestyle='--',label='Centre')
ax_corr.axvline(lags_n[np.argmax(rs)],color='tab:orange',linestyle='--',label='Max de synchronicité \nDécalage de {} minutes'.format(np.absolute(lags_n[np.argmax(rs)])))
plt.legend()
ax_corr.set_title('Corrélation croisée')
ax_corr.set_xlabel('Lag')
ax_corr.set_ylabel('Corrélation')
ax_noise.margins(0, 0.1)
ax_corr.margins(0, 0.1)
fig.tight_layout()
plt.show()

plt.figure(figsize=(5,5))
plt.title('Données applaties')
plt.plot(signal_upsample,signal_noise,'.')
plt.xlabel('Température du four')
plt.ylabel('Mesure du DTS')
plt.axis('equal')
