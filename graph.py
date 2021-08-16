import plotly.express as px
import plotly.graph_objects as go
import numpy as np
from plotly.subplots import make_subplots
from scipy.signal import correlate

from appareil import Appareil


def moy_pos(*appareils):
    POS_AXIS=1
    fig=go.Figure()

    v = []
    for a in appareils:
        if a.isDatalogger == True:
            line=go.Line(x=a.date, y=a.temp, visible=True, name = a.name)
        else:
            # if moy == True:
            line=go.Line(x=a.date, y=np.nanmean(a.temp,axis=POS_AXIS), visible=True, name = a.name)
            # else :
                # line=go.Line(x=a.date, y=a.temp, visible=True, name = a.name)
        fig.add_traces([line])
        v.append(False)

    fig.show()

    i = 0
    boutons = []
    for a in appareils:
        v_i = v.copy()
        v_i[i]=True
        boutons.append(
            dict(
                label=a.name,
                method="update",
                args=[  {"visible": v_i},
                    {"title": a.name}
                ])
                )
        i+=1

    boutons.append(
        dict(
            label='all',
            method="update",
            args=[  {"visible": [True]*len(v)},
                {"title": 'all'}
            ])
            )

    fig.update_layout(
             title='Température moyenne (dans la fibre) en fonction du temps',
             width=1000,
             height=600,
             xaxis_title='Date',
             yaxis_title='Température (°C)',
    )



    fig.update_layout(
        updatemenus=[
            dict(
                active=0,
                buttons=list(boutons ),
            )
        ])

    # Add range slider
    fig.update_layout(
        xaxis=
        dict(
            rangeslider=dict(
                visible=True
            ),
            type="date"
        )
    )
    return fig


# def temp_at_pos_signal(appareil, signal):

        # pos, temp, time, date = appareil.pos, appareil.temp, appareil.tdelta, appareil.date
#     # formatage
#     nb_time=len(date)
#     nb_pos=len(pos)
#     # température maximale
#     Tmax = np.nanmax(temp)
#     Tmin =  np.nanmin(temp)
#
#     fig=go.Figure()
#     lines=[go.Line(x=date, y=temp[:,k],visible=False) for k in range(nb_pos)]
#     fig.add_traces(lines)
#     lines=[go.Line(x=date, y=correlate(temp[:,k],signal), visible=False) for k in range(nb_pos)]
#     fig.add_traces(lines)
#
#     N = int(len(fig.data)/2)-1
#     fig.data[0]['visible']=True
#     fig.data[N+0]['visible']=True
#
#     steps = []
#     for i in range(0,len(fig.data)):
#         step = dict(
#             method = 'restyle',
#             args = ['visible', [False] * len(fig.data)],
#             label='{:.1f}'.format(pos[i]),
#         )
#         step['args'][1][i] = True # Toggle i'th trace to "visible"
#         step['args'][1][i+N] = True # Toggle i'th trace to "visible"
#         steps.append(step)
#
#     sliders = [dict(
#         active = 0,
#         currentvalue = {"prefix": "Position: "},
#         steps = steps,
#         pad={"t": 100}
#     )]
#
#     fig.update_layout(
#              title='Température à la position X en fonction du temps',
#              width=600,
#              height=600,
#              xaxis_title='Temps écoulé (h)',
#              yaxis_title='Température (°C)',
#              xaxis=dict(range=[date.item(0), date.item(-1)], autorange=True),
#              yaxis=dict(range=[Tmin, Tmax], autorange=False),
#              sliders=sliders
#     )
#
#     return fig

def traces(appareil):

    pos, temp, time, date = appareil.pos, appareil.temp, appareil.tdelta, appareil.date

    fig=go.Figure()
    POS_AXIS=1
    # data :
    for k in range(len(date)):
        line=go.Line(x=pos, y=temp[k], visible=True, name=str(appareil.date[k]))
        fig.add_traces([line])
    fig.update_layout(
             title='Température le long de la fibre (chaque trace=une acquision)',
             width=1000,
             height=600,
             xaxis_title='Position dans la fibre(m)',
             yaxis_title='Température (°C)',
    )
    return fig

def mean_pos(appareil):

    pos, temp, time, date = appareil.pos, appareil.temp, appareil.tdelta, appareil.date

    fig=go.Figure()
    POS_AXIS=1
    # data :
    line=go.Line(x=date, y=np.nanmean(temp,axis=POS_AXIS), visible=True, name = 'dts')
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


def temp_at_time(appareil):

    pos, temp, time, date = appareil.pos, appareil.temp, appareil.tdelta, appareil.date

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
            label=str(date[i]),
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

def temp_at_pos(appareil):

    pos, temp, time, date = appareil.pos, appareil.temp, appareil.tdelta, appareil.date

    # formatage
    nb_time=len(date)
    nb_pos=len(pos)
    # température maximale
    Tmax = np.nanmax(temp)
    Tmin =  np.nanmin(temp)


    fig=go.Figure()
    lines=[go.Line(x=date, y=temp[:,k],visible=False) for k in range(nb_pos)]
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
             xaxis=dict(range=[date.item(0), date.item(-1)], autorange=True),
             yaxis=dict(range=[Tmin, Tmax], autorange=False),
             sliders=sliders
    )

    return fig

def surface_plot(appareil):

    pos, temp, time, date = appareil.pos, appareil.temp, appareil.tdelta, appareil.date

    nb_time=len(date)
    nb_pos=len(pos)

    fig=go.Figure()
    # surface
    surf=go.Surface(x=pos,y=date, z=temp, visible=True,opacity=0.5,colorscale="Viridis")
    fig.add_trace(surf)
    # lignes sur le temps
    lines=[go.Scatter3d( x=pos, y=np.repeat(date[k], nb_pos), z=temp[k],  mode="lines",visible=False) for k in range(nb_time)]
    fig.add_traces(lines)
    # Visible au temps 0
    fig.data[0]['visible']=True
    fig.data[1]['visible']=True

    steps = []
    for i in range(1,len(fig.data)):
        step = dict(
            method = 'restyle',
            args = ['visible', [False] * len(fig.data)],
            label=str(date[i-1]),
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
             width=1500,
             height=1500,
             scene=dict(
             xaxis_title='Position (m)',
             zaxis_title='Température (°C)',
             yaxis_title='Date',
             aspectratio=dict(x=1, y=1, z=1),
                        ),
             sliders=sliders
    )
    return fig
