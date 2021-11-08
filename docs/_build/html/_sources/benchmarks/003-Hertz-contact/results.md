# Results

## Conclusions
### Calculix

### Code_Aster

### Elmer

## Mesh convergence study
### Linear Quadrangle mesh

| Solver    |   Coarse Mesh |   Medium Mesh |   Fine Mesh |   Very Fine Mesh |
|:----------|--------------:|--------------:|------------:|-----------------:|
| ccx       |       670.364 |       862.742 |     918.957 |          883.751 |
| elmer     |      5237.54  |      2269.57  |     999.03  |          897.251 |
| codeaster |       949.099 |      1179.4   |    1247.91  |         1171.19  |

### Quadratic Quadrangle mesh

| Solver    |   Coarse Mesh |   Medium Mesh |   Fine Mesh |   Very Fine Mesh |
|:----------|--------------:|--------------:|------------:|-----------------:|
| ccx       |       865.217 |       811.372 |     865.891 |          882.475 |
| elmer     |      1206.86  |       773.639 |     876.11  |          884.852 |
| codeaster |       739.617 |       810.872 |     961.746 |          913.968 |


<!-- ```{jupyter-execute}
:hide-code:
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np

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
``` -->
