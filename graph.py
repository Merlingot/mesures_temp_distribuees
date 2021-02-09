import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import pandas as pd
from plotly.subplots import make_subplots


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
             title='Température moyenne (dans la fibre) en fonction du temps',
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
                               {"title": "all"}]),
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

def vis_3d(dts, dsts):

    pos0,temp0,time0,dates0 = dts
    pos1,temp1,time1,dates1 = dsts
    mean_pos0=np.mean(pos0, axis=1)
    mean_pos1=np.mean(pos1, axis=1)


    fig=go.Figure()

    # surface
    surf0=go.Surface(x=time0, y=mean_pos0, z=temp0, visible=True,opacity=0.5,colorscale='Viridis')
    fig.add_trace(surf0)
    surf1=go.Surface(x=time1, y=mean_pos1, z=temp1, visible=False,opacity=0.5, colorscale='Cividis')
    fig.add_trace(surf1)

    # Update 3D scene options
    fig.update_scenes(
        aspectmode="manual"
    )
    fig.update_layout(
        # title='Profil de température',
        width=800,
        height=800,
        scene=dict(
        yaxis_title='Position (m)',
        zaxis_title='Température (°C)',
        xaxis_title='Temps écoulé (h)',
        aspectratio=dict(x=1, y=1, z=1),
        ),
    )
    button_layer_1_height = 1.25
    button_layer_2_height = 1.15
    # Add dropdown
    fig.update_layout(
        updatemenus=[
            dict(
                buttons=list([
                    dict(
                        args=["type", "surface"],
                        label="3D Surface",
                        method="restyle"
                    ),
                    dict(
                        args=["type", "heatmap"],
                        label="Heatmap",
                        method="restyle"
                    ),
                    dict(
                        args=["type", "contour"],
                        label="Contour",
                        method="restyle"
                    )
                ]),

                type = "buttons",
                direction="right",
                pad={"r": 10, "t": 10},
                showactive=True,
                x=0.13,
                xanchor="left",
                y=button_layer_2_height,
                yanchor="top"
            ),
            dict(
                active=0,
                buttons=list([
                    dict(label="DTS",
                         method="update",
                         args=[{"visible": [True, False]},
                               {"title": "dts"}]),
                    dict(label="DSTS",
                         method="update",
                         args=[{"visible": [False, True]},
                               {"title": "dsts"}]),
                ]),
                type = "buttons",
                direction="right",
                pad={"r": 10, "t": 10},
                showactive=True,
                x=0.13,
                xanchor="left",
                y=button_layer_1_height,
                yanchor="top"
            )
        ]
    )

    fig.update_layout(
        annotations=[
            dict(text="Data", x=-0.05, xref="paper", y=button_layer_1_height*0.975, yref="paper",
                                 align="left", showarrow=False),
            dict(text="Affichage", x=-0.05, xref="paper", y=button_layer_2_height*0.975,
                                 yref="paper", showarrow=False),

        ])

    return fig

def surface_plot(data, name):

    pos,temp,time,dates = data
    nb_time=time.shape[0]
    nb_pos=pos.shape[0]
    timemat=np.outer(np.ones([nb_pos]),time)
    fig=go.Figure()
    # surface
    surf=go.Surface(x=pos,y=timemat, z=temp, visible=True,opacity=0.5,colorscale="Viridis")
    fig.add_trace(surf)
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
             title='{}'.format(name),
             width=600,
             height=600,
             scene=dict(
             xaxis_title='Position (m)',
             zaxis_title='Température (°C)',
             yaxis_title='Temps écoulé (h)',
             aspectratio=dict(x=1, y=1, z=1),
                        ),
             sliders=sliders
    )

    return fig



def temp_at_time(data):

    pos,temp,time,dates = data

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


def temp_at_pos(data, name):

    pos,temp,time,dates = data
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
             title='{}'.format(name),
             width=600,
             height=600,
             xaxis_title='Temps écoulé (h)',
             yaxis_title='Température (°C)',
             xaxis=dict(range=[time.item(0), time.item(-1)], autorange=True),
             yaxis=dict(range=[Tmin, Tmax], autorange=False),
             sliders=sliders
    )

    return fig



def surface_pos_plot(data, name):

    pos,temp,time,dates = data
    nb_time=time.shape[0]
    nb_pos=pos.shape[0]
    timemat=np.outer(np.ones([nb_pos]),time)

    fig = make_subplots( rows=1, cols=2,
        specs=[[{"type": "scene"}, {"type": "xy"}]],
        subplot_titles=("Température en fonction <br> du temps et de la position", "Température en fonction de la position "),
        column_widths=[0.3, 0.5],
        horizontal_spacing=0.2
    )
    # surface
    surf=go.Surface(x=pos,y=timemat, z=temp, visible=True,opacity=0.5,colorscale="Viridis", hovertemplate = 'Température: %{z:.2f}<br>Position: %{x:.2f}<br>Temps: %{y:.2f}<extra></extra>' )

    fig.add_trace(surf, row=1, col=1)
    # lignes sur le temps
    lines=[go.Scatter3d( z=temp[:,k], x=pos[:,k], y=timemat[:,k], mode="lines",visible=False, hovertemplate = 'Température: %{z:.2f}<br>Position: %{x:.2f}<br>Temps: %{y:.2f}<extra></extra>' ) for k in range(nb_time)]
    fig.add_traces(lines, rows=1, cols=1)
    l = len(lines)
    lines=[go.Line( y=temp[:,k], x=pos[:,k],visible=False, hovertemplate='Température: %{y:.2f}<br>Position: %{x:.2f}<extra></extra>') for k in range(nb_time)]
    fig.add_traces(lines, rows=1, cols=2)

    # Visible au temps 0
    fig.data[0]['visible']=True
    fig.data[1]['visible']=True
    fig.data[l+1]['visible']=True

    steps = []
    for i in range(1,l+1):
        step = dict(
            method = 'restyle',
            args = ['visible', [False] * len(fig.data)],
            label=str(dates[i-1][5:]),
        )
        step['args'][1][0] = True # Toggle surface
        step['args'][1][i] = True # Toggle i'th trace to "visible"
        step['args'][1][l+i] = True # Toggle i'th trace to "visible"
        steps.append(step)

    sliders = [dict(
        active = 0,
        currentvalue = {"prefix": "Date: "},
        steps = steps,
        pad={"t": 100}
    )]

    fig.update_layout(
             title='Appareil : {}'.format(name),
             width=1100,
             height=600,
             scene=dict(
             xaxis_title='Position (m)',
             zaxis_title='Température (°C)',
             yaxis_title='Temps écoulé (h)',
             aspectratio=dict(x=1, y=1, z=1),
                        ),
             font=dict(size=10),
             sliders=sliders,
             showlegend=False
    )

    for i in fig['layout']['annotations']:
        i['font'] = dict(size=10)

    # Update yaxis properties
    fig.update_xaxes(title_text="Position (m)",  row=1, col=2)
    fig.update_yaxes(title_text="Température (°C)", row=1, col=2)

    return fig

def surface_time_plot(data, name):
    pos,temp,time,dates = data
    nb_time=time.shape[0]
    nb_pos=pos.shape[0]
    timemat=np.outer(np.ones([nb_pos]),time)
    mean_pos = np.mean(pos, axis=1)

    fig = make_subplots( rows=1, cols=2,
    specs=[[{"type": "scene"}, {"type": "xy"}]],
    subplot_titles=("Température en fonction <br> du temps et de la position", "Température en fonction du temps"),
    column_widths=[0.3, 0.5],
    horizontal_spacing=0.2
    )
    # surface
    surf=go.Surface(x=pos,y=timemat, z=temp, visible=True,opacity=0.5,colorscale="Viridis", hovertemplate = 'Température: %{z:.2f} °C<br>Position: %{x:.2f} m<br>Temps: %{y:.2f} h<extra></extra>' )
    fig.add_trace(surf, row=1, col=1)
    # lignes sur le temps
    lines=[go.Scatter3d( z=temp[k,:], x=pos[k,:], y=timemat[k,:], mode="lines",visible=False, hovertemplate = 'Température: %{z:.2f} °C<br>Position: %{x:.2f} m<br>Temps: %{y:.2f} h<extra></extra>' ) for k in range(nb_pos)]
    fig.add_traces(lines, rows=1, cols=1)
    l = len(lines)
    lines=[go.Line( y=temp[k,:], x=time,visible=False, hovertemplate='Température: %{y:.2f} °C<br>Position: %{x:.2f} m<extra></extra>') for k in range(nb_pos)]
    fig.add_traces(lines, rows=1, cols=2)

    # Visible au temps 0
    fig.data[0]['visible']=True
    fig.data[1]['visible']=True
    fig.data[l+1]['visible']=True

    steps = []
    for i in range(1,l+1):
        step = dict(
            method = 'restyle',
            args = ['visible', [False] * len(fig.data)],
            label='{:.2f}'.format(mean_pos[i-1]),
        )
        step['args'][1][0] = True # Toggle surface
        step['args'][1][i] = True # Toggle i'th trace to "visible"
        step['args'][1][l+i] = True # Toggle i'th trace to "visible"
        steps.append(step)

    sliders = [dict(
        active = 0,
        currentvalue = {"prefix": "Position (m) :"},
        steps = steps,
        pad={"t": 100}
    )]

    fig.update_layout(
             title='Appareil : {}'.format(name),
             width=1100,
             height=600,
             scene=dict(
             xaxis_title='Position (m)',
             zaxis_title='Température (°C)',
             yaxis_title='Temps écoulé (h)',
             aspectratio=dict(x=1, y=1, z=1),
                        ),
             font=dict(size=10),
             sliders=sliders,
             showlegend=False
    )

    for i in fig['layout']['annotations']:
        i['font'] = dict(size=10)

    # Update yaxis properties
    fig.update_xaxes(title_text="Temps écoulé (h)",  row=1, col=2)
    fig.update_yaxes(title_text="Température (°C)", row=1, col=2)

    return fig
