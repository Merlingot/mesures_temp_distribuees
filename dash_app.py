
import pandas as pd
import glob
import numpy as np
import matplotlib.pyplot as plt
from fonctions import *
from graph import *
import time
import dash
import dash_core_components as dcc
import dash_html_components as html
from jupyter_dash import JupyterDash


def generator_dts(list_, left, right):
    for char in list_:
        new_char = char[left:right]
        yield pd.to_datetime(new_char, format='%Y-%m-%d-%H-%M', errors='ignore')

def generator_dsts(list_, left, right):
    for char in list_:
        new_char = '2021'+char[left:right]
        yield pd.to_datetime(new_char, format='%Y%b%d%H%M', errors='ignore')

def read_dates_from_filename(folder, name):

    if name == 'dsts':
        left, right = -18,-9
        files=np.sort(glob.glob(folder + '*.tep'))
        dates = list(generator_dsts(files, left, right))
    elif name == 'dts':
        left, right = -23,-7
        files=np.sort(glob.glob(folder + '*.txt'))
        dates =  list(generator_dts(files, left, right))
    return dates

# files = read_dates_from_filename(folder_dsts, 'dsts')


# #### Importer les fichiers
# dts (LIOS) -------------------------------------------------------------------
files_dts = np.sort(glob.glob('/Volumes/MARINOUILLE/dts/s/Controller/4061/Fibre 02/2021/*.txt'))[:100]
pos0, temp0, time0, dates0 = read_files_dts(files_dts)
# dsts (OZ OPTICS)  ------------------------------------------------------------
L=4359
files_dsts = np.sort(glob.glob('/Volumes/MARINOUILLE/dsts/*.tep'))[:100]
pos1, temp1, time1, dates1 = read_files_dsts(files_dsts, L)
# datalogger  ----------------------------------------------------------------
file='data/datalogger.csv'
temp2, time2, dates2 = read_datalogger(file)

# Format
dts = (pos0 ,temp0 ,time0 ,dates0 )
dsts = (pos1 ,temp1 ,time1 ,dates1 )
dl = (temp2 , time2 , dates2 )

# #### Graphiques
fig1  = moyenne_pos_3(dates0 ,temp0 ,dates1 ,temp1 ,dates2 ,temp2 )
fig2  = surface_plot(dts, name='DTS')
fig3  = vis_3d(dts, dsts)
fig4  = temp_at_pos(dsts, name='DSTS')


app = JupyterDash(__name__)
app.layout = html.Div([
    # dcc.Upload(html.Button('Upload File')),

    # html.Hr(),
            html.Div([
            dcc.Graph(figure=fig1)
        ]),
            html.Div([
            dcc.Graph(figure=fig2)
        ]),
            html.Div([
            dcc.Graph(figure=fig3)
        ]),
            html.Div([
            dcc.Graph(figure=fig4)
        ])

])

if __name__ == '__main__':
    app.run_server(debug=True)

app.run_server(mode='external')
