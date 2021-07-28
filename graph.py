import plotly.express as px
import plotly.graph_objects as go
import numpy as np
# import pandas as pd
from plotly.subplots import make_subplots


def traces(posArr, tempArr, tdeltaArr, dateArr):

    fig=go.Figure()
    POS_AXIS=1
    # data :
    for k in range(len(dateArr)):
        line=go.Line(x=posArr, y=tempMat[k], visible=True, name=str(dateArr[k]))
        fig.add_traces([line])
    fig.update_layout(
             title='Température le long de la fibre (chaque trace=une acquision)',
             width=1000,
             height=600,
             xaxis_title='Position dans la fibre(m)',
             yaxis_title='Température (°C)',
    )
    return fig

def mean_pos(dateArr, tempMat):
    fig=go.Figure()
    POS_AXIS=1
    # data :
    line=go.Line(x=dateArr, y=np.nanmean(tempMat,axis=POS_AXIS), visible=True, name = 'dts')
    fig.add_traces([line])
    fig.update_layout(
             title='Température moyenne (dans la fibre) en fonction du temps',
             width=1000,
             height=600,
             xaxis_title='Date',
             yaxis_title='Température (°C)',
    )

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

def temp_at_time(pos, temp, time, dates):

    # formatage
    nb_time=len(time)
    nb_pos=len(pos)

    # température maximale
    Tmax = np.nanmax(temp)
    Tmin =  np.nanmin(temp)

    fig=go.Figure()
    lines=[go.Line(x=pos, y=temp[k],visible=False) for k in range(nb_time)]
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


def temp_at_pos(pos,temp,time,dates):
    # formatage
    nb_time=len(dates)
    nb_pos=len(pos)
    # température maximale
    Tmax = np.nanmax(temp)
    Tmin =  np.nanmin(temp)


    fig=go.Figure()
    lines=[go.Line(x=dates, y=temp[:,k],visible=False) for k in range(nb_pos)]
    fig.add_traces(lines)
    fig.data[0]['visible']=True

    steps = []
    for i in range(0,len(fig.data)):
        step = dict(
            method = 'restyle',
            args = ['visible', [False] * len(fig.data)],
            label='{:.1f}'.format(pos[i]),
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
             title='Température à la position X en fonction du temps',
             width=600,
             height=600,
             xaxis_title='Temps écoulé (h)',
             yaxis_title='Température (°C)',
             xaxis=dict(range=[dates.item(0), dates.item(-1)], autorange=True),
             yaxis=dict(range=[Tmin, Tmax], autorange=False),
             sliders=sliders
    )

    return fig

def surface_plot(posArr,tempMat,timeArr,dateArr):

    nb_time=len(dateArr)
    nb_pos=len(posArr)

    fig=go.Figure()
    # surface
    surf=go.Surface(x=posArr,y=dateArr, z=tempMat, visible=True,opacity=0.5,colorscale="Viridis")
    fig.add_trace(surf)
    # lignes sur le temps
    lines=[go.Scatter3d( x=posArr, y=np.repeat(dateArr[k], nb_pos), z=tempMat[k],  mode="lines",visible=False) for k in range(nb_time)]
    fig.add_traces(lines)
    # Visible au temps 0
    fig.data[0]['visible']=True
    fig.data[1]['visible']=True

    steps = []
    for i in range(1,len(fig.data)):
        step = dict(
            method = 'restyle',
            args = ['visible', [False] * len(fig.data)],
            label=str(dateArr[i-1]),
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
             title='Surface température en fonction de la date (y) et de la position (x)',
             width=600,
             height=600,
             scene=dict(
             xaxis_title='Position (m)',
             zaxis_title='Température (°C)',
             yaxis_title='Date',
             aspectratio=dict(x=1, y=1, z=1),
                        ),
             sliders=sliders
    )
    return fig
