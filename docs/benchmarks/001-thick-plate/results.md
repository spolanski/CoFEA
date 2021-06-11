# Results

Number of simulations with different element types and mesh size have been performed for the thick plate under pressure model.

## Conclusions

A few conclusions can be derived from the presented study:

1. It is possible to perform a structural analysis with pressure loading condition using open-source software and achieve a correct solution. In the current study, fairly coarse meshes have been tested and they allow to obtain a stress value close to the target of $\sigma_{yy}=5.38 MPa$. An additional test with a very fine mesh has been run and all tested FE codes converged to the target value.
2. It can be seen that Calculix and Code_Aster generally provided similar output apart for the case of linear hex mesh. It may indicate that a slightly different element formulation for linear hexahedral meshes was used.
3. The results from Elmer show a different convergence behaviour comparing to other FE codes. While this behaviour can be a result of different numerical scheme implementation, it should also be highlighted that FE meshes used in Elmer runs were slightly different compared to the runs in other codes. This difference was caused by the fact that the meshes used in Calculix and Code_Aster came as an output from meshpresso converter and those seem not to be compatible with Elmer. It looks like the 3D geometry requires all type of elements to be provided (3D hex/tet, 2D tri/quad and 1D wires) while at the current stage, the meshpresso provides only 3D or 2D elements. However, it was also noted that ElmerGUI struggles to import some type of .UNV meshes created in the Salome environment. Especially, the quadratic hexahedral mesh type seems to be problematic.

```{figure} ./ccx_output.png
---
width: 600px
alt: Calculix results
name: Calculix results
---
Results obtained with Calculix software and quadratic hexahedral mesh
```

## Linear tetrahedral mesh

| Solver                |Coarse Mesh              |Fine Mesh                |
|-----------------------|-------------------------|-------------------------|
| CalculiX              | -1.51 MPa               | -4.38 MPa               |    
| Code_Aster            | -1.51 MPa               | -4.38 MPa               |
| Elmer                 | -2.64 MPa               | -5.49 MPa               |

## Quadratic tetrahedral mesh

| Solver                |Coarse Mesh              |Fine Mesh                |
|-----------------------|-------------------------|-------------------------|
| CalculiX              | -5.45 MPa               |  -5.77 MPa              |    
| Code_Aster            | -5.51 MPa               |  -5.85 MPa              |
| Elmer                 | -4.58 MPa               |  -5.50 MPa              |

```{jupyter-execute}
:hide-code:
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
```

## Linear hexahedral mesh

| Solver                |Coarse Mesh              |Fine Mesh                |
|-----------------------|-------------------------|-------------------------|
| CalculiX              | -2.75 MPa               |  -3.08 MPa              |    
| Code_Aster            | -4.05 MPa               |  -5.42 MPa              |
| Elmer                 | -4.52 MPa               |  -5.02 MPa              |

## Quadratic hexahedral mesh

| Solver                |Coarse Mesh              |Fine Mesh                |
|-----------------------|-------------------------|-------------------------|
| CalculiX              | -7.34 MPa               |  -5.65 MPa              |    
| Code_Aster            | -7.39 MPa               |  -5.66 MPa              |
| Elmer                 | -5.56 MPa               |  -5.65 MPa              |

```{jupyter-execute}
:hide-code:
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
```