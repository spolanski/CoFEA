# Results

Number of simulations with different element types and mesh size have been performed for the hemisphere shell model.

## Conclusions

A few conclusions can be derived from the presented study:

1. It is hard to perform a shell analysis with force loading condition using open-source software and achieve a correct solution. In the current study, only code_aster benchmark mesh was able to obtain a displacement value close to the target of $u_{x}=0.185 m$.
2. To obtain precise results with Elmer it is needed to use finer meshes and calculate normal vectors before starting the calculations (mesh.director). For now (27.03.2021) Elmer doesn't support quadratic shell elements. Please remember that shell solver is under development.
3. CalculiX was unable to produce correct results with shell elements and symmetry boundary conditions. For more detailed information please read chapter below.
4. Code_Aster support QUAD_9 instead QUAD_8 elements. Fortunately the solver itself contains a mesh converter to this type of elements.


```{figure} ./shell.png
---
width: 600px
alt: Hemispherical shell membrane results
name: Hemispherical shell membrane results
---
Results obtained with Code_Aster software and linear hexahedral mesh
```
## Linear quadrilateral mesh

| Solver                |Coarse Mesh              |Fine Mesh                |
|-----------------------|-------------------------|-------------------------|
| CalculiX              | 0.000306 m              |  0.0000325 m            |    
| Code_Aster            | 0.163 m                 |  0.192 m                |
| Elmer                 | 0.009578 m              |  0.033597 m             |

## Quadratic quadrilateral mesh

| Solver                |Coarse Mesh              |Fine Mesh                |
|-----------------------|-------------------------|-------------------------|
| CalculiX              | 0.0000431 m             |  0.0000792 m            |    
| Code_Aster            | 0.147 m                 |  0.184 m                |
| Elmer                 | no data                 | no data                 |

```{jupyter-execute}
:hide-code:
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np

# location of csv_file
csv_file = pd.read_csv('benchmarks/005-hemispherical-shell-point-load/results.csv')
# name of the plot
plot_title = 'Quadrilateral mesh comparison'
# element topology - Tri / Tet / Quad / Hex
el_topology = 'Quad'
# Y axis title
y_axis_title = "Displacement in X direction [m]"
target_value = 0.185
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

## Numerous models in CalculiX
In order to obtain correct results with CalculiX 3 models were prepared:
- quarter hemisphere model with use of shell S8 elements as described in NAFEMS benchmark,
- quarter hemisphere model with use of solid C3D20R elements as described in NAFEMS benchmark,
- half sphere model with use of shell S8 elements modeled without symmetry boundary conditions,

Shell element types in CalculiX did not allow to achieve results close to the target value with symmetry boundary conditions. For the hemisphere shell model, the contour of displacement field seems to be similar to the expected one, although the values are still not correct. On the contrary, the solid model with 3 elements per thickness allows to obtain a satisfying result, but it required some time to estimate the response. These comparison proves that the CalculiX model was set up correctly, but it is the shell element type which is the source of non-satisfactory results.

```{figure} ./ccx_comparison.png
---
width: 700px
alt: CalculiX results comparison
name: CalculiX results comparison
---
Graph representing results of different models results in CalculiX from left: S8 shell elements quarter hemisphere model, S8 shell half sphere model, solid C3D20R elements quarter hemisphere model.

```
```{figure} ./solver_comparison.png
---
width: 700px
alt: Solver results comparison
name: Solver results comparison
---
Results from fine shell mesh in Code_Aster, very fine shell mesh in Elmer and very fine hexahedral mesh in Calculix'
```
