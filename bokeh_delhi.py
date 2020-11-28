import pandas as pd
from bokeh.plotting import figure, curdoc
from bokeh.layouts import column, row, layout
from bokeh.models import ColumnDataSource, Panel, Tabs, HoverTool, PreText, Div

# Read in dataset and extract Delhi data
whole_dataset = pd.read_csv("city_day.csv", parse_dates=['Date'])
delhi_dataset = whole_dataset[whole_dataset['City'] == 'Delhi']

# Create CDS object
delhi_df = delhi_dataset # Panda dataframe
delhi_dataset = ColumnDataSource(delhi_dataset)


TOOLS = ["pan,wheel_zoom,xbox_select,box_zoom,reset"]

particle_list = ["PM2.5", "PM10", "NO", "NO2", "NOx", "NH3", "CO"]

# Create figures and tabs for data visualization of particle amount over time
tabs = []
figure_list = []
for i in range(7):
    figure_list.append(figure(plot_width=800, plot_height=600, x_axis_type='datetime', x_axis_label="Date (YYYY/MM/DD)", 
        y_axis_label="Particle Amount in Air (ug/m\u00b3)", tools = TOOLS, active_drag="xbox_select"))
    
    figure_list[i].add_tools(HoverTool(tooltips=[('Amount', '$y ug/m\u00b3'), ('Date', '@Date{%F}')], formatters={'@Date': 'datetime'}))
    _color = 'blue'
    figure_list[i].circle("Date", particle_list[i], source=delhi_dataset, color=_color, alpha=0.5)
    tabs.append(Panel(child=figure_list[i], title=particle_list[i]))

# Header
div = Div(text='<h1>Delhi Air Quality Data Visualization</h1>')


# Stats Widget
stats = PreText(text=str(delhi_df[particle_list[:4]].describe()), width=300)
stats2 = PreText(text=str(delhi_df[particle_list[4:]].describe()), width=300)

# Method to update stats widget
def update_stats(data):
    stats.text = str(data[particle_list[:4]].describe())
    stats2.text = str(data[particle_list[4:]].describe())

# Callback method to update stats and date range
def update(attr, old, new):
    data = delhi_df
    selected = delhi_dataset.selected.indices

    if selected:
        data = data.iloc[selected, :]
    update_stats(data)

    # Update Date range
    first_val = data['Date'].values[0]
    first_date = pd.to_datetime(first_val).date()
    last_val = data['Date'].values[-1]
    last_date = pd.to_datetime(last_val).date()
    
    indice.text = 'Date Range: ' + str(first_date) + ' : ' + str(last_date)
    

delhi_dataset.selected.on_change('indices', update)
    
# Date range
indice = PreText(text="Date Range: 2015-01-01 : 2020-07-01")

layout = layout([div], [Tabs(tabs=tabs), column(stats, stats2, indice)])

curdoc().add_root(layout)
curdoc().title = 'Delhi Air Quality Data Visualization'