"""
Bokeh App for solving ODE model - Basic version
B Chan | Feb 18th 2020
"""
#-----------------------------------------------------------
# Boilerplate:
#-----------------------------------------------------------
import pandas as pd
import numpy as np

import model # Separate file with ODE model code

# Bokeh libraries
from bokeh.io import output_file, output_notebook, curdoc
from bokeh.plotting import figure, show
from bokeh.models import ColumnDataSource, Slider, Button
from bokeh.layouts import row, column, gridplot
from bokeh.models.widgets import Tabs, Panel
from bokeh.events import ButtonClick
#-----------------------------------------------------------
# End boilerplate
#-----------------------------------------------------------

# Initialize the figures
fig_init = figure(title='Wuhan: ', plot_height = 300, plot_width = 300)
fig_init2 = figure(title='Country 2: ', plot_height = 300, plot_width = 300)
fig_init3 = figure(title='Country 3: ', plot_height = 300, plot_width = 300)

def solve_ode():
    '''
    Function that takes values from interface inputs and uses them to run the specified model
    Inputs: None
    Outputs: t | 1D vector representing the number of time steps
             S | [t, n] array representing susceptible over time t for n countries
             I | [t, n] array representing infected over time t for n countries
             E | [t, n] array representing exposed over time t for n countries
    '''
    i = spinner1.value
    j = spinner2.value
    k = spinner3.value

    t, S, I, E = model.ode_model(i, j, k)

    return t, S, I, E

def update(event):
    '''
    Callback function for the "Solve" button. Calls solve_ode() to obtain the model results and then
    plots the results to the defined figures
    Inputs: None
    Outputs: None
    '''
    # Get data
    t, S, I, E = solve_ode()

    #source.data.update(dict(x=list[x1],y=list[y1]))   
    fig1_new = figure(title='Wuhan: ', plot_height = 300, plot_width = 300)
    fig2_new = figure(title='Country 2: ', plot_height = 300, plot_width = 300)
    fig3_new = figure(title='Country 3: ', plot_height = 300, plot_width = 300)
    
    fig1_new.line(y=S[:,0], x=t, color='red', line_width=1, legend='Susceptible')
    fig1_new.line(y=I[:,0], x=t, color='blue', line_width=1, legend='Infected')
    fig1_new.line(y=E[:,0], x=t, color='green', line_width=1, legend='Exposed')

    fig2_new.line(y=S[:,1], x=t, color='red', line_width=1, legend='Susceptible')
    fig2_new.line(y=I[:,1], x=t, color='blue', line_width=1, legend='Infected')
    fig2_new.line(y=E[:,1], x=t, color='green', line_width=1, legend='Exposed')

    fig3_new.line(y=S[:,2], x=t, color='red', line_width=1, legend='Susceptible')
    fig3_new.line(y=I[:,2], x=t, color='blue', line_width=1, legend='Infected')
    fig3_new.line(y=E[:,2], x=t, color='green', line_width=1, legend='Exposed')

    new_figs = row(fig1_new, fig2_new, fig3_new)
    layout.children[0] = new_figs 

    df = fold_geo_information(t, S, I, E)
    df.to_csv('./temp_csv.csv')
    
def clear(event):
    '''
    Function to clear/reset the plots rendered
    Inputs: None
    Outputs: None
    '''
    fig_init = figure(title='Wuhan: ', plot_height = 300, plot_width = 300)
    fig_init2 = figure(title='Country 2: ', plot_height = 300, plot_width = 300)
    fig_init3 = figure(title='Country 3: ', plot_height = 300, plot_width = 300)
    new_figs = row(fig_init, fig_init2, fig_init3)
    layout.children[0] = new_figs

def fold_geo_information(t,S,I,E):
    df = pd.DataFrame(columns=['day','s','i','e','region'])

    region_names = ['North America','Asia','Europe']
    r = 0
    for region in region_names:
        df_temp = pd.DataFrame(np.column_stack([t, S[:,r], I[:,r], E[:,r]]))
        df_temp['region'] = region
        df_temp = df_temp.rename(columns={0: "day", 1: "s", 2: "i", 3: "e", 4: "s",})
        r += 1
        df = df.append(df_temp)

    return df

# Initialize controls and inputs
spinner1 = Slider(start=0, end=10, value=1, step=.1,title='R0')
spinner2 = Slider(start=0, end=10, value=1, step=.1,title='De')
spinner3 = Slider(start=0, end=10, value=1, step=.1,title='Di')

button_solve = Button(label="Solve", button_type="success")
button_solve.on_event(ButtonClick, update) #('value', lambda attr, old, new: update())

button_reset = Button(label="Reset", button_type="success")
button_reset.on_event(ButtonClick, clear)

# Organize layout 
figs = row(fig_init, fig_init2, fig_init3)
controls = column(spinner1, spinner2, spinner3, button_solve, button_reset)
layout = column(figs, controls)

fig_temp = figure(title='Wuhan: ', plot_height = 300, plot_width = 300)

# Create two panels
plot_panel = Panel(child=layout, title='Model')
#map_panel = Panel(child=fig_temp, title='Map')

# Assign the panels to Tabs
tabs = Tabs(tabs=[plot_panel])

curdoc().add_root(tabs)
curdoc().title = "Plot"