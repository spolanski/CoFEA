<<<<<<< HEAD
=======
#!/usr/bin/env python
# coding: utf-8

# In[1]:


>>>>>>> 8cbd91b276c79c45f606b00b49b9d2047080b491
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np

<<<<<<< HEAD
# location of csv_file
csv_file = pd.read_csv('benchmarks/007-raasch-challenge/raasch.csv')
# name of the plot
plot_title = 'Triangle mesh comparison'
# element topology - Tri / Tet / Quad / Hex
el_topology = 'Tri'
# Y axis title
y_axis_title = "Displacement [m]"
target_value = 0.125
layout = go.Layout(
    title=dict(
        text=plot_title,
        font=dict(size=20,),
=======

plot_title = 'Triangle mesh comparison'
results = pd.read_csv('benchmarks/007-raasch-challenge/raasch.csv')

lin_type = results['Mesh type'] == 'Lin-Tri'
quad_type = results['Mesh type'] == 'Quad-Tri'
mesh_type = results[lin_type | quad_type]
zipped = zip(mesh_type['Mesh type'],mesh_type['Size'])
labels = ["{} {}".format(i[0], i[1]) for i in zipped]
code_aster_values = mesh_type['Code_Aster'].tolist()
elmer_values = mesh_type['Elmer'].tolist()
x = np.arange(len(labels))  # the label locations

layout = go.Layout(
    title=dict(
        text=plot_title,
        font=dict(
            size=20,
        ),
>>>>>>> 8cbd91b276c79c45f606b00b49b9d2047080b491
        y=0.95,
        x=0.5),
    xaxis=dict(
        linecolor="#BCCCDC",  # Sets color of X-axis line
        showgrid=True  # Removes X-axis grid lines
    ),
    yaxis=dict(
<<<<<<< HEAD
        title=y_axis_title,  
=======
        title="Displacement [m]",  
>>>>>>> 8cbd91b276c79c45f606b00b49b9d2047080b491
        linecolor="#BCCCDC",  # Sets color of Y-axis line
        showgrid=True,  # Removes Y-axis grid lines    
    )
)

<<<<<<< HEAD
colours = px.colors.qualitative.T10
=======

colours = px.colors.qualitative.Vivid
>>>>>>> 8cbd91b276c79c45f606b00b49b9d2047080b491
fig = go.Figure(layout=layout)

fig.update_layout( # customize font and legend orientation & position
    font_family="Rockwell",
    legend=dict(
        title=None, orientation="h", y=1, yanchor="bottom", x=0.5, xanchor="center"
    )
)

<<<<<<< HEAD
if target_value:
    fig.add_shape( # add a horizontal "target" line
        type="line", line_color="black", line_width=3, opacity=1, line_dash="dot",
        x0=0, x1=1, xref="paper", y0=target_value, y1=target_value, yref="y"
    )

lin_type = csv_file['Mesh type'] == ('Lin-' + el_topology)
quad_type = csv_file['Mesh type'] == ('Quad-' + el_topology)
mesh_type = csv_file[lin_type | quad_type]
zipped = zip(mesh_type['Mesh type'],mesh_type['Size'])
labels = ["{} {}".format(i[0], i[1]) for i in zipped]
x = np.arange(len(labels))  # the label locations

columns = list(mesh_type.columns)
start_index = columns.index('Size') + 1

for n, label in enumerate(columns[start_index:]):
    app_values = mesh_type[label].tolist()

    fig.add_trace(go.Bar(
        x=labels,
        y=app_values,
        name=label,
        marker_color=colours[n]
    ))

# modify the tickangle of the xaxis, resulting in rotated labels.
fig.update_layout(barmode='group', xaxis_tickangle=-45)
fig.show()
=======
fig.add_shape( # add a horizontal "target" line
    type="line", line_color="black", line_width=3, opacity=1, line_dash="dot",
    x0=0, x1=1, xref="paper", y0=0.125, y1=0.125, yref="y"
)


fig.add_trace(go.Bar(
    x=labels,
    y=code_aster_values,
    name='Code_Aster',
    marker_color=colours[0]
))
fig.add_trace(go.Bar(
    x=labels,
    y=elmer_values,
    name='Elmer',
    marker_color=colours[1]
))

# Here we modify the tickangle of the xaxis, resulting in rotated labels.
fig.update_layout(barmode='group', xaxis_tickangle=-45)
fig.show()


# In[2]:

>>>>>>> 8cbd91b276c79c45f606b00b49b9d2047080b491

import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np

<<<<<<< HEAD
# location of csv_file
csv_file = pd.read_csv('benchmarks/007-raasch-challenge/raasch.csv')
# name of the plot
plot_title = 'Quadrilateral mesh comparison'
# element topology - Tri / Tet / Quad / Hex
el_topology = 'Quad'
# Y axis title
y_axis_title = "Displacement [m]"
target_value = 0.125
layout = go.Layout(
    title=dict(
        text=plot_title,
        font=dict(size=20,),
=======

plot_title = 'Quadrilateral mesh comparison'
results = pd.read_csv('benchmarks/007-raasch-challenge/raasch.csv')

lin_type = results['Mesh type'] == 'Lin-Quad'
quad_type = results['Mesh type'] == 'Quad-Quad'
mesh_type = results[lin_type | quad_type]
zipped = zip(mesh_type['Mesh type'],mesh_type['Size'])
labels = ["{} {}".format(i[0], i[1]) for i in zipped]
code_aster_values = mesh_type['Code_Aster'].tolist()
elmer_values = mesh_type['Elmer'].tolist()
x = np.arange(len(labels))  # the label locations

layout = go.Layout(
    title=dict(
        text=plot_title,
        font=dict(
            size=20,
        ),
>>>>>>> 8cbd91b276c79c45f606b00b49b9d2047080b491
        y=0.95,
        x=0.5),
    xaxis=dict(
        linecolor="#BCCCDC",  # Sets color of X-axis line
        showgrid=True  # Removes X-axis grid lines
    ),
    yaxis=dict(
<<<<<<< HEAD
        title=y_axis_title,  
=======
        title="Displacement [m]",  
>>>>>>> 8cbd91b276c79c45f606b00b49b9d2047080b491
        linecolor="#BCCCDC",  # Sets color of Y-axis line
        showgrid=True,  # Removes Y-axis grid lines    
    )
)

<<<<<<< HEAD
colours = px.colors.qualitative.T10
=======

colours = px.colors.qualitative.Vivid
>>>>>>> 8cbd91b276c79c45f606b00b49b9d2047080b491
fig = go.Figure(layout=layout)

fig.update_layout( # customize font and legend orientation & position
    font_family="Rockwell",
    legend=dict(
        title=None, orientation="h", y=1, yanchor="bottom", x=0.5, xanchor="center"
    )
)

<<<<<<< HEAD
if target_value:
    fig.add_shape( # add a horizontal "target" line
        type="line", line_color="black", line_width=3, opacity=1, line_dash="dot",
        x0=0, x1=1, xref="paper", y0=target_value, y1=target_value, yref="y"
    )

lin_type = csv_file['Mesh type'] == ('Lin-' + el_topology)
quad_type = csv_file['Mesh type'] == ('Quad-' + el_topology)
mesh_type = csv_file[lin_type | quad_type]
zipped = zip(mesh_type['Mesh type'],mesh_type['Size'])
labels = ["{} {}".format(i[0], i[1]) for i in zipped]
x = np.arange(len(labels))  # the label locations

columns = list(mesh_type.columns)
start_index = columns.index('Size') + 1

for n, label in enumerate(columns[start_index:]):
    app_values = mesh_type[label].tolist()

    fig.add_trace(go.Bar(
        x=labels,
        y=app_values,
        name=label,
        marker_color=colours[n]
    ))

# modify the tickangle of the xaxis, resulting in rotated labels.
fig.update_layout(barmode='group', xaxis_tickangle=-45)
fig.show()
=======
fig.add_shape( # add a horizontal "target" line
    type="line", line_color="black", line_width=3, opacity=1, line_dash="dot",
    x0=0, x1=1, xref="paper", y0=0.125, y1=0.125, yref="y"
)

fig.add_trace(go.Bar(
    x=labels,
    y=code_aster_values,
    name='Code_Aster',
    marker_color=colours[0]
))
fig.add_trace(go.Bar(
    x=labels,
    y=elmer_values,
    name='Elmer',
    marker_color=colours[1]
))

# Here we modify the tickangle of the xaxis, resulting in rotated labels.
fig.update_layout(barmode='group', xaxis_tickangle=-45)
fig.show()

>>>>>>> 8cbd91b276c79c45f606b00b49b9d2047080b491
