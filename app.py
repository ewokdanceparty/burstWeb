'''
This is a web-based interactive visualization of burst spiking, as sensed intra- and extracellularly. 
It uses Plotly Dash, and this code was initially based off of the "Drug Discovery Demo" from Plotly
Dash.

Paper citation: Allen, B.D., Moore-Kochlacs, C., Bernstein, J.G., Kinney, J.P., Scholvin, J., Seoane, L.F., Chronopoulos, 
C., Lamantia, C., Kodandaramaiah, S.B., Tegmark, M., and Boyden, E.S. (2018).
Automated in vivo patch clamp evaluation of extracellular multielectrode array spike recording
capability. J Neurophysiol.

'''

import dash
from dash.dependencies import Input, Output
import dash_html_components as html
import dash_core_components as dcc
import pandas as pd
import flask
from flask_cors import CORS
import os
import numpy

app = dash.Dash('burst-firing')
app.title = 'Ground truth neurotechnology'
server = app.server
df = pd.read_csv('bursts.csv')

BACKGROUND = 'rgb(230, 230, 230)'
COLORSCALE = [[0, "rgb(128,128,128)"], [0.10, "rgb(255,0,0)"],
              [0.25, "rgb(0,255,0)"], [0.45, "rgb(255,0,255)"],
              [0.65, "rgb(255,255,0)"], [0.85, "rgb(0,0,255)"],
              [1, "rgb(255,128,0)"]]


def scatter_plot_3d(
        #hoverinfo = 'skip',
        x=df['isi'] * 1000,  #numpy.log10(df['isi']),
        y=df['amp'],
        z=df['sample'],
        size=df['SIZE'],
        color=df['COLOR'],
        pic=df['PIC'],
        xlabel='isi',
        ylabel='amp',
        zlabel='sample',
        plot_type='scatter',
        markers=[]):
    def axis_template_3d(title):  #, type='linear' ):
        return dict(showbackground=True,
                    backgroundcolor=BACKGROUND,
                    gridcolor='rgb(255, 255, 255)',
                    title=title,
                    type=type,
                    zerolinecolor='rgb(0, 0, 0)')

    def axis_template_2d(title):
        return dict(xgap=10,
                    ygap=10,
                    backgroundcolor=BACKGROUND,
                    gridcolor='rgb(0, 0, 0)',
                    title=title,
                    zerolinecolor='rgb(255, 255, 255)',
                    color='#444')

    data = [
        dict(x=x,
             y=y,
             z=z,
             mode='markers',
             marker=dict(
                 colorscale=COLORSCALE,
                 line=dict(color='#444'),
                 reversescale=False,
                 sizeref=45,
                 sizemode='diameter',
                 opacity=0.7,
                 size=size,
                 color=color,
             ),
             text=pic,
             type=plot_type,
             ur=pic)
    ]

    layout = dict(font=dict(family='Raleway'),
                  hovermode='closest',
                  showlegend=False,
                  xaxis={
                      'type': 'log',
                      'title': 'inter-spike interval (ms)'
                  },
                  yaxis={
                      'type': 'linear',
                      'title': 'extracellular spike amplitude (&mu;V)'
                  },
                  scene=dict(
                      xaxis=axis_template_2d(xlabel),
                      yaxis=axis_template_2d(ylabel),
                  ))

    if len(markers) > 0:
        data = data + add_markers(data, markers, plot_type=plot_type)

    return dict(data=data, layout=layout)


FIGURE = scatter_plot_3d()

STARTING_IMG = 4591
SPIKE_IMG = df.loc[df['sample'] == STARTING_IMG]['PIC'].iloc[0]

markdown_text = "Credit: Automated in vivo patch clamp evaluation of extracellular multielectrode array spike recording capability, by BD Allen, C Moore-Kochlacs, JG Bernstein, et al., 2018. J Neurophys: [Paper](https://doi.org/10.1152/jn.00650.2017). [Python source code](https://github.com/ewokdanceparty/burstWeb). [Matlab source code for other paper analyses](https://github.com/ewokdanceparty/spikeval/tree/devel)."
app.layout = html.Div(
    [
        # Row 1: Header and Intro text
        html.Div([
            html.H2('Burst firing: intra- and extracellular properties',
                    style={
                        'position': 'relative',
                        'top': '0px',
                        'left': '10px',
                        'font-family': 'Dosis',
                        'display': 'inline',
                        'font-size': '6.0rem',
                        'color': '#4D637F'
                    }),
        ],
                 className='row twelve columns',
                 style={
                     'position': 'relative',
                     'right': '15px'
                 }),
        html.Div([html.Div([], className='twelve columns')], className='row'),

        # Row 2: Hover Panel and Graph
        html.Div([
            html.Div([
                html.Img(id='spike_img',
                         src=SPIKE_IMG,
                         width='300px',
                         height='400px'),
            ],
                     className='three columns',
                     style=dict(marginTop='100px')),
            html.Div([
                dcc.Graph(id='clickable-graph',
                          style=dict(width='600px', height='600px'),
                          hoverData=dict(points=[dict(pointNumber=0)]),
                          config={
                              'displayModeBar': False,
                              'scrollZoom': False
                          },
                          figure=FIGURE),
            ],
                     className='nine columns',
                     style=dict(textAlign='center')),
        ],
                 className='row'),
        html.Div([
            html.
            P("Many neurons fire a sequence of spikes, known as a burst, in response to stimuli. Waveforms of later spikes within a burst may be significantly less pronounced, making them harder to detect with an electrode placed near the neuron. This is an exploration of burst spikes as electrically sensed inside (intracellularly) and outside (extracellularly) of a single neuron, in vivo. Such recordings are rare, affording a unique opportunity to assess the limits of spike detectability with a given electrode. Mouse over the data points in the figure (right) to explore spikes (left) that occur at various positions within a burst."
              ),
            html.
            P("Left: Spikes as sensed intracellularly (top, with derivative of signal in middle), and extracellularly (bottom; filtered for spikes). Scalebar: 20ms (horiz.), 10mV/100\u03BCV (vert., top/bottom)"
              ),
            html.
            P("Right: Extracellular spike amplitude, colored by spike number within a burst, with respect to time since the previous spike (interspike interval). Key: non-burst spike (grey), 1st spike in burst (red), 2nd (green), 3rd (magenta), 4th (yellow), 5th (blue), 6th (orange). Hovering over a datapoint will show its corresponding spike (left; the particular spike will be centered in the x-axis)"
              ),
        ]),
        dcc.Markdown(children=markdown_text)
    ],
    className='container')

#


def dfRowFromHover(hoverData):
    ''' Returns row for hover point as a Pandas Series '''
    if hoverData is not None:
        if 'points' in hoverData:
            firstPoint = hoverData['points'][0]
            if 'pointNumber' in firstPoint:
                point_number = firstPoint['pointNumber']
                spike_name = str(
                    FIGURE['data'][0]['text'][point_number]).strip()
                return spike_name
    return pd.Series()


@app.callback(Output('spike_img', 'src'),
              [Input('clickable-graph', 'hoverData')])
def display_image(hoverData):
    row = dfRowFromHover(hoverData)
    img_src = row
    return img_src


external_css = [
    "https://cdnjs.cloudflare.com/ajax/libs/skeleton/2.0.4/skeleton.min.css",
    "//fonts.googleapis.com/css?family=Dosis:400,300,600",
    "//fonts.googleapis.com/css?family=Dosis:Medium",
    "https://cdn.rawgit.com/plotly/dash-app-stylesheets/0e463810ed36927caf20372b6411690692f94819/dash-drug-discovery-demo-stylesheet.css"
]

for css in external_css:
    app.css.append_css({"external_url": css})

if __name__ == '__main__':
    #app.run_server(debug=False)
    app.run_server(8001)
