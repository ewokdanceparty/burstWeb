# burstWeb

This is a web-based interactive visualization of burst spiking, as sensed intra- and extracellularly. 
It uses Plotly Dash, and this code was initially based off of the "Drug Discovery Demo" from Plotly
Dash.

Paper citation: Allen, B.D., Moore-Kochlacs, C., Bernstein, J.G., Kinney, J.P., Scholvin, J., Seoane, L.F., Chronopoulos, C., Lamantia, C., Kodandaramaiah, S.B., Tegmark, M., and Boyden, E.S. (2018).
Automated in vivo patch clamp evaluation of extracellular multielectrode array spike recording
capability. J Neurophysiol. https://doi.org/10.1152/jn.00650.2017

This code has been tested on Mac and Linux. For it to work on Windows, some dependencies may need to be updated.

Run `python3 install -r requirements.txt` to install requirements. To cordon these requirements off from the rest of your system, first create and activate a virtual environment with `python3 -m venv venv` and `source venv/bin/activate`.

Run `python3 app.py` to start the server to visualize the data, explained below. If you want to run the server locally, change the second-to-last line, app.run_server(debug=False), to app.run_server(8001), and go to 127.0.0.1:8001 in a web browser.


