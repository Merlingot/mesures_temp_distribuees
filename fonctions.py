import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import pandas as pd




# Fonctions DSTS ---------------------------------------------------------------
def read_files_dsts(files, L, ntime, npos):

    def read_date(file):
        nb=55
        with open(file) as f:
            f.seek(nb)
            d = f.readline()[:-1]
        date=pd.to_datetime(d)
        return date

    def find_footer(L,posFrame):
        indexes=posFrame.index.values[(posFrame>L).values.flatten()]
        start = indexes[0]
        end = indexes[-1]
        footer = end-start+1
        return start, end, footer

    first_file=files[0]
    #  header:
    nb_header_lines = 32
    # Lire une première fois :
    posFrame0=pd.read_table(first_file, header=None, skiprows=nb_header_lines, delimiter='  ', na_filter=True, engine='python', usecols=[0], comment='#')
    start, end, footer = find_footer(L,posFrame0)
    # skiprows
    skip = lambda x: (x % npos != 0 or x < nb_header_lines or x > start)
    # position:
    posFrame=pd.read_table(first_file, header=None, skiprows=skip, delimiter='  ', na_filter=True, engine='python', usecols=[0], comment='#')
    # temperature
    tempFrame=pd.read_table(first_file, header=None, skiprows=skip, delimiter='  ', na_filter=True, engine='python',usecols=[1],comment='#')
    tempFrame=tempFrame.rename(columns={1:0})
    # time series:
    range_ntime = [x for x in range(0, len(files)) if x%ntime == 0 ]
    timeSerie=pd.Series(np.zeros( (len(range_ntime)) ), dtype=float)
    dateSerie=pd.Series(np.zeros( (len(range_ntime)) ), dtype=str)
    date0 = read_date(first_file)
    timeSerie.at[0,0] = (date0-date0).total_seconds()/3600
    dateSerie.at[0,0] = str(date0)

    for i,j in zip(range_ntime[1:], range(1,len(range_ntime))): # index sur le temps
        # position
        posFrame[i]=pd.read_table(files[i], header=None, skiprows=skip,  delimiter='  ', na_filter=True,engine='python',usecols=[0],comment='#')
        # température
        tempFrame[i]=pd.read_table(files[i], header=None, skiprows=skip,  delimiter='  ', na_filter=True,engine='python',usecols=[1],comment='#')
        # date
        date=read_date(files[i])
        timeSerie.at[j,0] = (date-date0).total_seconds()/3600
        dateSerie.at[j,0] = str(date)

    # Valeurs sous forme de np.array()
    time=timeSerie.values.flatten()
    time-=time.min(); a=np.argsort(time); time=time[a]
    temp = tempFrame.values[:,a] #row=pos, col=time
    pos = posFrame.values[:,a] #row=pos, col=time
    dates = dateSerie.values[a]

    return pos, temp, time, dates
# ------------------------------------------------------------------------------


# Fonctions DTS ---------------------------------------------------------------
def read_files_dts(files, ntime, npos):


    def read_date(file):
        d = pd.read_table(file, header=None, sep='\t', na_filter=False, skiprows=9, nrows=1, usecols=[1], dtype=str)
        return pd.to_datetime(d.values.flatten()[0])


    # usecols :
    use = lambda x : (x%npos == 0 and x!=-1)

    # Lire le premier fichier ------------------------------------------------
    first_file=files[0]
    # lire une fois pour connaitre la longueur du fichier
    posFrame0=pd.read_table(first_file, header=None, sep='\t', na_filter=False, skiprows=8, nrows=1)
    names=np.arange(-1, posFrame0.shape[1]-1)
    # Position
    posFrame=pd.read_table(first_file, header=None, sep='\t', na_filter=False, skiprows=8, nrows=1, names = names, usecols=use).T
    # Température
    tempFrame=pd.read_table(first_file, header=None, sep='\t', na_filter=False, skiprows=10, nrows=1, names = names, usecols=use).T

    # time series:
    range_ntime = [x for x in range(0, len(files)) if x%ntime == 0 ]
    timeSerie=pd.Series(np.zeros( (len(range_ntime)) ), dtype=float)
    dateSerie=pd.Series(np.zeros( (len(range_ntime)) ), dtype=str)
    date0 = read_date(first_file)
    timeSerie.at[0] = (date0-date0).total_seconds()/3600
    dateSerie.at[0] = str(date0)[:-6]



    # Lire le reste des fichiers --------------------------------------------
    for i,j in zip(range_ntime[1:], range(1,len(range_ntime))): # index sur le temps
        # Position
        posFrame[i]=pd.read_table(files[i], header=None, sep='\t', na_filter=False, skiprows=8, nrows=1, names = names, usecols=use).T
        # Température
        tempFrame[i]=pd.read_table(files[i], header=None, sep='\t', na_filter=False, skiprows=10, nrows=1, names = names, usecols=use).T
        # date
        date = read_date(files[i])
        timeSerie.at[j] = (date-date0).total_seconds()/3600
        dateSerie.at[j] = str(date)[:-6]


    # Valeurs sous forme de np.array()
    time=timeSerie.values.flatten()
    time-=time.min();a=np.argsort(time);time=time[a]
    temp = tempFrame.values[:,a] #row=pos, col=time
    pos = posFrame.values[:,a] #row=pos, col=time
    dates=dateSerie.values[a]

    return pos, temp, time, dates
# ------------------------------------------------------------------------------


# Fonction datalogger ----------------------------------------------------------
def read_datalogger(file):

    datedl = pd.read_table(file, header=None, skiprows=11, delimiter=',', usecols=[1], na_filter=True, parse_dates=True, infer_datetime_format=False)
    dateSerie = pd.Series( pd.to_datetime(datedl[1]) )
    timeSerie = (dateSerie - dateSerie[0])
    timeSerie = timeSerie.apply(lambda x : x.total_seconds()/3600)
    tempFramedl = pd.read_table('datalogger.csv', header=None, skiprows=11, delimiter=',', usecols=[2], na_filter=True)
    # Valeurs
    temp = tempFramedl.values.flatten() #row=pos, col=time
    time = timeSerie.values.flatten()
    dateSerie = dateSerie.apply(lambda x : str(x))
    dates = dateSerie.values
    return temp, time, dates
# ------------------------------------------------------------------------------








def moyenne_pos_3(dates0,temp0,dates1,temp1,dates2,temp2):

    fig=go.Figure()

    # data :
    mean_dts_0 = np.mean(temp0[:,0])
    line0=go.Line(x=dates0, y=np.mean(temp0,axis=0), visible=True, name = 'dts')
    line1=go.Line(x=dates1, y=np.mean(temp1,axis=0), visible=False,  name = 'dsts')
    line2=go.Line(x=dates2, y=temp2, visible=False, name = 'datalogger')
    line3=go.Line(x=dates1, y=(np.mean(temp1,axis=0)+mean_dts_0), visible=False,  name ='dsts offset')

    fig.add_traces([line0,line1,line2,line3])


    fig.update_layout(
             title='Température moyenne en fonction du temps',
             width=1000,
             height=600,
             xaxis_title='Date',
             yaxis_title='Température (°C)',
    )

    v = [False, False, False, False]

    fig.update_layout(
        updatemenus=[
            dict(
                active=0,
                buttons=list([
                    dict(label="DTS",
                         method="update",
                         args=[{"visible": [True, False, False, False]},
                               {"title": "dts"}]),
                    dict(label="DSTS",
                         method="update",
                         args=[{"visible": [False, True, False, False]},
                               {"title": "dsts"}]),
                    dict(label="DataLogger",
                         method="update",
                         args=[{"visible": [False, False, True, False]},
                               {"title": "datalogger"}]),
                    dict(label="All",
                         method="update",
                         args=[{"visible": [True, False, True, True]},
                               {"title": "datalogger"}]),
                ]),
            )
        ])

    # Add range slider
    fig.update_layout(
        xaxis=dict(
            rangeslider=dict(
                visible=True
            ),
            type="date"
        )
    )
    return fig


def surface_plot(pos,time,temp,dates):
    Tmax = temp.max()
    Tmin =  temp.min()
    nb_time=time.shape[0]
    nb_pos=pos.shape[0]
    timemat=np.outer(np.ones([nb_pos]),time)
    fig=go.Figure()
    # surface
    surf=go.Surface(x=pos,y=timemat, z=temp, visible=True,opacity=0.5,colorscale="Aggrnyl")
    fig.add_trace(surf)
    fig.show()
    # lignes sur le temps
    lines=[go.Scatter3d( z=temp[:,k], x=pos[:,k], y=timemat[:,k], mode="lines",visible=False) for k in range(nb_time)]
    fig.add_traces(lines)
    # Visible au temps 0
    fig.data[0]['visible']=True
    fig.data[1]['visible']=True

    steps = []
    for i in range(1,len(fig.data)):
        step = dict(
            method = 'restyle',
            args = ['visible', [False] * len(fig.data)],
            label=str(dates[i-1]),
        )
        step['args'][1][0] = True # Toggle surface
        step['args'][1][i] = True # Toggle i'th trace to "visible"
        steps.append(step)

    sliders = [dict(
        active = 0,
        currentvalue = {"prefix": "Date: "},
        steps = steps,
        pad={"t": 100}
    )]

    fig.update_layout(
             title='Profil de température',
             width=600,
             height=600,
             scene=dict(
             xaxis_title='Position (m)',
             zaxis_title='Température (°C)',
             yaxis_title='Temps écoulé (h)',
             yaxis=dict(range=[0, time.item(-1)], autorange=True),
             zaxis=dict(range=[Tmin, Tmax], autorange=False),
             aspectratio=dict(x=1, y=1, z=1),
                        ),
             sliders=sliders
    )

    return fig



def temp_at_time(pos,time,temp,dates):

    # formatage
    nb_time=time.shape[0]
    nb_pos=pos.shape[0]
    # température maximale
    Tmax = temp.max()
    Tmin =  temp.min()

    fig=go.Figure()
    lines=[go.Line(x=pos[:,k], y=temp[:,k],visible=False) for k in range(nb_time)]
    fig.add_traces(lines)
    fig.data[0]['visible']=True

    steps = []
    for i in range(0,len(fig.data)):
        step = dict(
            method = 'restyle',
            args = ['visible', [False] * len(fig.data)],
            label=str(dates[i]),
        )
        step['args'][1][i] = True # Toggle i'th trace to "visible"
        steps.append(step)

    sliders = [dict(
        active = 0,
        currentvalue = {"prefix": "Date: "},
        steps = steps,
        pad={"t": 100}
    )]

    fig.update_layout(
             title='Profil de température en fonction de la position',
             width=600,
             height=600,
             xaxis_title='Position (m)',
             yaxis_title='Température (°C)',
             xaxis=dict(range=[pos.item(0), pos.item(-1)], autorange=False),
             yaxis=dict(range=[Tmin, Tmax], autorange=False),
             sliders=sliders
    )

    return fig


def temp_at_pos(pos,time,temp):

    # formatage
    nb_time=time.shape[0]
    nb_pos=pos.shape[0]
    # température maximale
    Tmax = temp.max()
    Tmin =  temp.min()
    # position moyenne
    mean_pos=np.mean(pos,axis=1)

    fig=go.Figure()
    lines=[go.Line(x=time, y=temp[k,:],visible=False) for k in range(nb_pos)]
    fig.add_traces(lines)
    fig.data[0]['visible']=True

    steps = []
    for i in range(0,len(fig.data)):
        step = dict(
            method = 'restyle',
            args = ['visible', [False] * len(fig.data)],
            label='{:.1f}'.format(mean_pos[i]),
        )
        step['args'][1][i] = True # Toggle i'th trace to "visible"
        steps.append(step)

    sliders = [dict(
        active = 0,
        currentvalue = {"prefix": "Position: "},
        steps = steps,
        pad={"t": 100}
    )]

    fig.update_layout(
             title='Profil de température en fonction du temps',
             width=600,
             height=600,
             xaxis_title='Temps écoulé (h)',
             yaxis_title='Température (°C)',
             xaxis=dict(range=[time.item(0), time.item(-1)], autorange=True),
             yaxis=dict(range=[Tmin, Tmax], autorange=False),
             sliders=sliders
    )

    return fig
