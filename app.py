'''
This is a web-based interactive visualization of burst spiking, as sensed intra- and extracellularly. 
It uses Plotly Dash, and this code was initially based off of the "Drug Discovery Demo" from Plotly
Dash.

Use app.run_server(8001), at the bottom of this script, to run the server locally (otherwise app.run_server(8001) for running on Heroku)

Paper citation: Allen, B.D., Moore-Kochlacs, C., Bernstein, J.G., Kinney, J.P., Scholvin, J., Seoane, L.F., Chronopoulos, 
C., Lamantia, C., Kodandaramaiah, S.B., Tegmark, M., and Boyden, E.S. (2018).
Automated in vivo patch clamp evaluation of extracellular multielectrode array spike recording
capability. J Neurophysiol.

'''

import dash
from dash.dependencies import Input, Output
from dash import html
from dash import dcc
import pandas as pd
from flask_cors import CORS

app = dash.Dash(__name__)
app.title = 'Ground truth neurotechnology'
server = app.server
df = pd.read_csv('bursts.csv')

BACKGROUND = 'rgb(230, 230, 230)'
COLORSCALE = [[0, "rgb(128,128,128)"], [0.10, "rgb(255,0,0)"],
              [0.25, "rgb(0,255,0)"], [0.45, "rgb(255,0,255)"],
              [0.65, "rgb(255,255,0)"], [0.85, "rgb(0,0,255)"],
              [1, "rgb(255,128,0)"]]


def scatter_plot_3d(
        x=df['isi'] * 1000,
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
    def axis_template_3d(title):
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

    layout = dict(font=dict(family='Helvetica'),
                  hovermode='closest',
                  showlegend=False,
                  xaxis={
                      'type': 'log',
                      'title': 'inter-spike interval (ms)',
                      'fixedrange': True
                  },
                  yaxis={
                      'type': 'linear',
                      'title': 'extracellular spike amplitude (&mu;V)',
                      'fixedrange': True
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
                        'left': '50px',
                        'font-family': 'Helvetica',
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
                          config={
                              'displayModeBar': False,
                              'scrollZoom': False,
                          },
                          clickData=dict(points=[dict(pointNumber=0)]),
                          figure=FIGURE),
            ],
                     className='nine columns',
                     style=dict(textAlign='center')),
        ],
                 className='row'),
        html.Div([
            html.
            P("Many neurons fire a sequence of spikes, known as a burst, in response to stimuli. Waveforms of later spikes within a burst may be significantly less pronounced, making them harder to detect (or perhaps impossible to detect) with an electrode placed near the neuron. Bursting is presumed to play a role in neural coding, so understanding when we can and cannot detect burst spikes with a given technology could prove to be important."
              ),
            html.
            P("This is an exploration of burst spikes as electrically sensed inside (intracellularly) and outside (extracellularly) of a single cortical neuron, in an awake animal. The relatively high-fidelity intracellular signal acts as ground truth, telling us when to look for a spike from the particular neuron in the extracellular signal. The lower-fidelity extracellular signal will often contain spikes from other neurons in the vicinity, in addition to spikes from the neuron of interest, making it difficult to tell which spikes originated from which neurons. This problem can be approached with the technique known as spike sorting."
              ),
            html.
            P("Recordings like these are typically difficult to achieve and are rare, affording a unique opportunity to assess the limits of spike detectability with a given electrode configuration and spike sorting algorithm. The recordings here were enabled by the technology developed as described in the paper linked to at the bottom of the page."
              ),
            html.
            P("Tap the data points in the figure (right) to explore spikes (left) that occur at various positions within a burst."
              ),
            html.
            P("Left: Spikes as sensed intracellularly (top; the derivative of the signal with respect to time is in the middle), and extracellularly (bottom; bandpass filtered for spikes). Scalebar: 20ms (horiz.), 10mV/100\u03BCV (vert., top/bottom)"
              ),
            html.
            P("Right: Extracellular spike amplitude, colored by spike number within a burst, with respect to time since the previous spike (inter-spike interval). Key: Non-burst spike (grey), 1st spike in burst (red), 2nd (green), 3rd (magenta), 4th (yellow), 5th (blue), 6th (orange). Tapping a data point will show its corresponding spike (left; the particular spike will be centered in the x-axis)"
              ),
        ], style={'position': 'relative', 'margin-left': '40px', 'margin-right': '40px'}),
        dcc.Markdown(children=markdown_text, style={'position': 'relative', 'margin-left': '40px', 'margin-right': '40px'})
    ],
    className='container')

def dfRowFromHover(clickData):
    ''' Returns row for hover point as a Pandas Series '''
    if clickData is not None:
        if 'points' in clickData:
            firstPoint = clickData['points'][0]
            if 'pointNumber' in firstPoint:
                point_number = firstPoint['pointNumber']
                spike_name = str(
                    FIGURE['data'][0]['text'][point_number]).strip()
                return spike_name
    return pd.Series()

@app.callback(Output('spike_img', 'src'),
              [Input('clickable-graph', 'clickData')])
def display_image(clickData):
    row = dfRowFromHover(clickData)
    img_src = row
    return img_src

if __name__ == '__main__':
    # app.run_server(debug=False) # Run locally
    app.run_server(8001) # Run on Heroku
