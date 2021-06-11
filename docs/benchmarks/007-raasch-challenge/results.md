# Results

## Conclusions
### Calculix

Some initial tests with the S4R elements revealed that Calculix is not able to capture the behaviour correctly (even for the fine mesh). However, it turns out that for the presented loadcase, the wrong displacement value was caused by the reduced integration scheme. Calculix is able to predict the correct response once the fully integrated elements are used.

This study also revealed that it is not possible within the Calculix solver to directly impose a load distributed over an edge. However, one can use a third party software called [PrePoMax](http://lace.fs.uni-mb.si/wordpress/borovinsek/) that allows to define the surface traction load on an edge, which is converted into *CLOAD keyword afterwards.

```{figure} ./calculix.png
---
width: 600px
name: S4R vs S4 elements in Calculix
---
Difference between the results with S4R (left) and S4 (right) shell elements in Calculix
```

### Code_Aster
Code_Aster allows to run this particular benchmark almost in a frictionless manner. A solution close to the expected value has been achieved even for the linear type of elements. Additionally, the code has a built-in keyword called FORCE_ARETE that allows to specify a load distributed over an edge.

While setting up the solver is straightforward, the post-processing of results with the second-order shell elements might be confusing. Code_Aster solver uses TRIA6_7 or QUAD8_9 element formulation which have an additional node in the middle of element. At the current moment, it is not possible to directly visualise the displacement field in this place. A possible workaround is to run the simulation with the mesh that includes the additional nodes and then project the results onto mesh without them. The section [Tested Finite Element codes](./tested-codes) presents an example of input deck that take advantage of the mentioned workaround.

```{figure} .   /code_aster_results.png
---
width: 600px
name: QUAD8_9 vs Projected results
---
Inappropriate display of results with the QUAD8_9 elements (left) and the projected results (right)
```

### Elmer
Although the Elmer solver does not support second-order shell elements, it was still possible to achieve a displacement value close to the expected one. The distributed loading conditions have also been easily defined using Resultant Force keyword.

It is worth mentioning that the current shell implementation in Elmer requires a manual definition of shell normals. The definition consists of a file called mesh.director containng node numbers and the normal vectors at the position of a particular node. One can quickly realise that it is rather non-trivial operation to obtain the vectors value for complex shapes. For the case of this particular study, a Python script that aims to be executed in the FreeCAD environment has been prepared. This script loads a BREP representation of the geometry and the Elmer mesh.nodes file, so the precise vector could be computed at any node position. The mentioned script can be found on the [CoFEA Github](https://github.com/spolanski/CoFEA) repo. 

## Mesh convergence study
### Linear and Quadratic Triangle mesh

|   Solver   | Coarse Mesh <br> linear / quadratic | Fine Mesh <br> linear / quadratic | Very Fine Mesh <br> linear / quadratic |
|:----------:|:------------------------------:|:----------------------------:|:------------------------:|
|  Calculix  |          0.017 / 0.127   |         0.036 / 0.131    |           0.067 / 0.131      |
| Code_Aster |          0.116 / 0.129         |         0.118 / 0.128        |           0.116 / 0.128          |
|    Elmer   |          0.040 / -             |         0.055 / -            |           0.084 / -              |


```{jupyter-execute}
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
```

### Linear and Quadratic Quadrilateral mesh

|   Solver   | Coarse Mesh <br> linear / quadratic | Fine Mesh <br> linear / quadratic | Very Fine Mesh <br> linear / quadratic |
|:----------:|:--------------------------------:|:------------------------------:|:--------------------------:|
| Calculix   |           0.126 / 0.129      |          0.127 / 0.130     |            0.129 / 0.130       |
| Code_Aster |           0.112 / 0.130          |          0.118 / 0.128         |            0.116 / 0.127           |
|    Elmer   |           0.0304 / -             |          0.052 / -             |            0.125 / -               |

```{jupyter-execute}
:hide-code:
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np

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
