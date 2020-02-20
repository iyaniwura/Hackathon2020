"""
Bokeh App for solving ODE model - quarantine version
B Chan | Feb 18th 2020
"""
#-----------------------------------------------------------
# Boilerplate:
#-----------------------------------------------------------
import pandas as pd
import numpy as np

import model_q # Separate file with ODE model code

# Bokeh libraries
from bokeh.io import output_file, output_notebook, curdoc
from bokeh.plotting import figure, show
from bokeh.models import ColumnDataSource, Slider, Button, TextInput
from bokeh.layouts import row, column, gridplot
from bokeh.models.widgets import Tabs, Panel
from bokeh.events import ButtonClick
#-----------------------------------------------------------
# End boilerplate
#-----------------------------------------------------------

# Initialize the figures
fig_init = figure(title='Wuhan: ', plot_height = 300, plot_width = 300)
fig_init2 = figure(title='Country 2: ', plot_height = 150, plot_width = 150)
fig_init3 = figure(title='Country 3: ', plot_height = 150, plot_width = 150)
fig_init4 = figure(title='Country 4: ', plot_height = 150, plot_width = 150)
fig_init5 = figure(title='Country 4: ', plot_height = 150, plot_width = 150)

def solve_ode():
    '''
    Function that takes values from interface inputs and uses them to run the specified model
    Inputs: None
    Outputs: t | 1D vector representing the number of time steps
             I | [t, n] array representing infected over time t for n countries
             E | [t, n] array representing exposed over time t for n countries
             R | [t, n] array representing recovered over time t for n countries
    '''
    M = 5 # Number of countries - currently fixed. Change if desired
    g_params = {'R0': spinner1.value, 'De': spinner2.value, 'Di': spinner3.value, 'alpha': np.zeros(M)} # global model parameters
    g_params['alpha'][0] = float(spinner4.value)
    g_params['psi'] = np.array([float(spinner5.value), ]*M)
    g_params['phi'] = np.array([float(spinner6.value), ]*M)
    g_params['h'] = np.array([float(spinner7.value), ]*M)
    g_params['gamma'] = np.array([float(spinner8.value), ]*M)
    g_params['Gamma'] = np.array([float(spinner9.value), ]*M)
    g_params['beta'] = np.array([float(spinner10.value), ]*M)
    g_params['tau'] = np.array([float(spinner11.value), ]*M)

    bats = int(spinner12.value)

    # Commented out dynamic travel matrix adjustments 
    # TODO:// Fix bug with typing issues, might be a model things
    #l1 = list(g1.value)
    #l2 = list(g2.value)
    #l3 = list(g3.value)
    #l4 = list(g4.value)
    #l5 = list(g5.value)
    #L_data = np.array(np.column_stack([l1,l2,l3,l4,l5]))
    #L_data  = L_data.astype(int)

    # Hard coded array
    L_data = np.array([[     0,  13056,   5930,    563,    355],
       [  6849,      0,  99640, 197190,  49887],
       [    20,  29300,      0, 261774,  66226],
       [   214,  86535, 419844,      0, 237225],
       [   153,  21950, 106494, 237846,      0]])

    t, I, E, R = model_q.run_model(g_params, L_data, bats)

    return t, I, E, R

def update(event):
    '''
    Callback function for the "Solve" button. Calls solve_ode() to obtain the model results and then
    plots the results to the defined figures
    Inputs: None
    Outputs: None
    '''
    # Get data
    t, I, E, R = solve_ode()

    #source.data.update(dict(x=list[x1],y=list[y1]))   
    fig1_new = figure(title='Wuhan: ', plot_height = 300, plot_width = 300)
    fig2_new = figure(title='Country 2: ', plot_height = 300, plot_width = 300)
    fig3_new = figure(title='Country 3: ', plot_height = 300, plot_width = 300)
    fig4_new = figure(title='Country 4: ', plot_height = 300, plot_width = 300)
    fig5_new = figure(title='Country 4: ', plot_height = 300, plot_width = 300)
    
    fig1_new.line(y=I[:,0], x=t, color='red', line_width=1, legend='Infected')
    fig1_new.line(y=E[:,0], x=t, color='blue', line_width=1, legend='Exposed')
    fig1_new.line(y=R[:,0], x=t, color='green', line_width=1, legend='Recovered')

    fig2_new.line(y=I[:,1], x=t, color='red', line_width=1, legend='Infected')
    fig2_new.line(y=E[:,1], x=t, color='blue', line_width=1, legend='Exposed')
    fig2_new.line(y=R[:,1], x=t, color='green', line_width=1, legend='Recovered')

    fig3_new.line(y=I[:,2], x=t, color='red', line_width=1, legend='Infected')
    fig3_new.line(y=E[:,2], x=t, color='blue', line_width=1, legend='Exposed')
    fig3_new.line(y=R[:,2], x=t, color='green', line_width=1, legend='Recovered')

    fig4_new.line(y=I[:,3], x=t, color='red', line_width=1, legend='Infected')
    fig4_new.line(y=E[:,3], x=t, color='blue', line_width=1, legend='Exposed')
    fig4_new.line(y=R[:,3], x=t, color='green', line_width=1, legend='Recovered')

    fig5_new.line(y=I[:,4], x=t, color='red', line_width=1, legend='Infected')
    fig5_new.line(y=E[:,4], x=t, color='blue', line_width=1, legend='Exposed')
    fig5_new.line(y=R[:,4], x=t, color='green', line_width=1, legend='Recovered')

    new_figs = gridplot([fig1_new, fig2_new, fig3_new, fig4_new, fig5_new], ncols=3, plot_width=400, plot_height=300)

    layout.children[0] = new_figs 

    # For future implenetation :: Saving data as a file
    #df = fold_geo_information(t, S, I, E)
    #df.to_csv('./temp_csv.csv')
    
def clear(event):
    '''
    Function to clear/reset the plots rendered
    Inputs: None
    Outputs: None
    '''
    fig1_new = figure(title='Wuhan: ', plot_height = 300, plot_width = 300)
    fig2_new = figure(title='Country 2: ', plot_height = 150, plot_width = 150)
    fig3_new = figure(title='Country 3: ', plot_height = 150, plot_width = 150)
    fig4_new = figure(title='Country 4: ', plot_height = 150, plot_width = 150)
    fig5_new = figure(title='Country 4: ', plot_height = 150, plot_width = 150)
    
    new_figs = gridplot([fig1_new, fig2_new, fig3_new, fig4_new, fig5_new], ncols=3, plot_width=400, plot_height=300)

    layout.children[0] = new_figs 

# CURRENTLY NOT USED.
def fold_geo_information(t, I, E, R):
    '''
    Function that "wraps" the data from all countries into a single dataframe - could be used to do other analysis
    Inputs: t | np linspace(?) that represents timesteps
            I | [t, n] array representing infected over time t for n countries
            E | [t, n] array representing exposed over time t for n countries
            R | [t, n] array representing recovered over time t for n countries
    Outputs: df | pandas dataframe with the "folded data tagged by metric
    '''
    df = pd.DataFrame(columns=['day','s','i','e','region'])

    region_names = ['North America','Asia','Europe'] #NOT IN CORRECT ORDER RIGHT NOW
    r = 0
    for region in region_names:
        df_temp = pd.DataFrame(np.column_stack([t, S[:,r], I[:,r], E[:,r]]))
        df_temp['region'] = region
        df_temp = df_temp.rename(columns={0: "day", 1: "s", 2: "i", 3: "e", 4: "s",})
        r += 1
        df = df.append(df_temp)

    #df = df.merge(geo_data, on='region') # Could merge with geographic data to do coloropleth plots

    return df

# Initialize controls and inputs
# 'Standard' inputs:
spinner1 = Slider(start=0, end=10, value=3, step=.1,title='R0')
spinner2 = Slider(start=0, end=10, value=6.5, step=.1,title='De')
spinner3 = Slider(start=0, end=10, value=7, step=.1,title='Di')

# Model special inputs:
spinner4 = TextInput(value='1', title='alpha')
spinner5 = TextInput(value='0.2', title='psi (fear level)')
spinner6 = TextInput(value='0.3', title='phi (prob of infected being able to travel)')
spinner7 = TextInput(value='0.1', title='h (infection rate in hospital)')
spinner8 = TextInput(value='0.5', title='gamma (prob of E to quarantine)')
spinner9 = TextInput(value='0.5', title='Gamma (prob of I to quarantine)')
spinner10 = TextInput(value='0.1', title='beta (prob of E to quarantine at arrival)')
spinner11 = TextInput(value='0.8', title='tau (prob of I to quarantine at arrival)')
spinner12 = Slider(start=0, end=500, value=20, step=1,title='Bats?')

# Matrix inputs: (Not used yet - just for show)
g1 = TextInput(value='[0, 13056, 5930, 563, 355]', title='Matrix')
g2 = TextInput(value='[6849, 0, 99640, 197190, 49887]') 
g3 = TextInput(value='[20,29300, 0, 261774,  66226]')
g4 = TextInput(value='[214, 86535, 419844, 0, 237225]')
g5 = TextInput(value='[153, 21950, 106494, 237846, 0]')
matrix = column(g1,g2,g3,g4,g5)

# Buttons to control updates/resets
button_solve = Button(label="Solve", button_type="success")
button_solve.on_event(ButtonClick, update) #('value', lambda attr, old, new: update())
button_reset = Button(label="Reset", button_type="warning")
button_reset.on_event(ButtonClick, clear)

# Organize layout 
figs = gridplot([fig_init, fig_init2, fig_init3, fig_init4, fig_init5], ncols=3, plot_width=400, plot_height=300)

model_controls = column(spinner1, spinner2, spinner3, button_solve, button_reset)
quarantine_controls = column(spinner4, spinner5, spinner6, spinner7, spinner8)
quarantine_controls2 = column(spinner9, spinner10, spinner11, spinner12)
controls = row(model_controls, quarantine_controls,quarantine_controls2, matrix)

layout = column(figs, controls)

# Create panels (Could add more if wanted)
plot_panel = Panel(child=layout, title='Model')

# Assign the panels to Tabs
tabs = Tabs(tabs=[plot_panel])

curdoc().add_root(tabs)
curdoc().title = "Plot"