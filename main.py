import glob
import pandas as pd
import numpy as np
from read_files_DTS import read_files_dts
from read_files_datalog import read_datalogger
from read_files_DSTS import read_files_dsts
import matplotlib.pyplot as plt
from graph import moy_pos,mean_pos,temp_at_time,temp_at_pos,surface_plot,traces

from csv_utils import *

folder='csv/13_08_2021/DTS/'
a = read_csv(folder, 'labo')

plt.plot(a.date, np.nanmean(a.temp,axis=1))

# # # FIGURE 1 : PROFIL DE TEMPÉRATURE EN FONCTION DU TEMPS, MOYENNE SUR LA LONGUEUR DE LA FIBRE
f = mean_pos(a)
f.show()
# #
# # # FIGURE 2 : PROFIL DE TEMPÉRATURE EN FONCTION DE LA POSITION, SLIDER SUR LA DATE
f = temp_at_time(a)
f.show()
# #
# # # FIGURE 3: PROFIL DE TEMPÉRATURE EN FONCTION DE LA DATE, SLIDER SUR LA POSITION
# f = temp_at_pos(a)
# f.show()
#
# # FIGURE 4 : SUPERPOSITION DES PROFILS DE TEMPÉRATURE LE LONG DE LA FIBRE, POUR TOUTES LES ACQUISITIONS
# f = traces(a)
# f.show()
#
# # # FIGURE 5: SURFACE PLOT
# f = surface_plot(a)
# f.show()
