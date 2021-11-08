import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np

# location of csv_file
csv_file = pd.read_csv('benchmarks/001-thick-plate/elipse_results.csv')
# name of the plot
plot_title = 'Tetrahedral mesh comparison'
# element topology - Tri / Tet / Quad / Hex
el_topology = 'Tet'
# Y axis title
y_axis_title = "Absolute stress in Y direction [MPa]"
target_value = 5.38
layout = go.Layout(
    title=dict(
        text=plot_title,
        font=dict(size=20,),
        y=0.95,
        x=0.5),
    xaxis=dict(
        linecolor="#BCCCDC",  # Sets color of X-axis line
        showgrid=True  # Removes X-axis grid lines
    ),
    yaxis=dict(
        title=y_axis_title,  
        linecolor="#BCCCDC",  # Sets color of Y-axis line
        showgrid=True,  # Removes Y-axis grid lines    
    )
)

colours = px.colors.qualitative.T10
fig = go.Figure(layout=layout)

fig.update_layout( # customize font and legend orientation & position
    font_family="Rockwell",
    legend=dict(
        title=None, orientation="h", y=1, yanchor="bottom", x=0.5, xanchor="center"
    )
)

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

import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np

# location of csv_file
csv_file = pd.read_csv('benchmarks/001-thick-plate/elipse_results.csv')
# name of the plot
plot_title = 'Hexahedral mesh comparison'
# element topology - Tri / Tet / Quad / Hex
el_topology = 'Hex'
# Y axis title
y_axis_title = "Absolute stress in Y direction [MPa]"
target_value = 5.38
layout = go.Layout(
    title=dict(
        text=plot_title,
        font=dict(size=20,),
        y=0.95,
        x=0.5),
    xaxis=dict(
        linecolor="#BCCCDC",  # Sets color of X-axis line
        showgrid=True  # Removes X-axis grid lines
    ),
    yaxis=dict(
        title=y_axis_title,  
        linecolor="#BCCCDC",  # Sets color of Y-axis line
        showgrid=True,  # Removes Y-axis grid lines    
    )
)

colours = px.colors.qualitative.T10
fig = go.Figure(layout=layout)

fig.update_layout( # customize font and legend orientation & position
    font_family="Rockwell",
    legend=dict(
        title=None, orientation="h", y=1, yanchor="bottom", x=0.5, xanchor="center"
    )
)

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