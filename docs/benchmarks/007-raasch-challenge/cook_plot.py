# import matplotlib.pyplot as plt
# from matplotlib.ticker import FormatStrFormatter
import pandas as pd
import numpy as np
# plt.close('all')

# def mesh_study():
#     plot_title = 'Triangle mesh comparison'
#     file_name = 'triangle_raasch.png'
#     results = pd.read_csv('raasch.csv')

#     lin_type = results['Mesh type'] == 'Lin-Tri'
#     quad_type = results['Mesh type'] == 'Quad-Tri'
#     mesh_type = results[lin_type | quad_type]
#     zipped = zip(mesh_type['Mesh type'],mesh_type['Size'])
#     labels = ["{} {}".format(i[0], i[1]) for i in zipped]
#     # ccx_values = mesh_type['Calculix'].tolist()
#     code_aster_values = mesh_type['Code_Aster'].tolist()
#     elmer_values = mesh_type['Elmer'].tolist()
#     x = np.arange(len(labels))  # the label locations

#     width = 0.2  # the width of the bars
#     # plt.style.use('seaborn-white') 
#     fig, ax = plt.subplots(figsize=(10,6))
#     # ax.bar(x - 0.2, ccx_values, width, label='Calculix')
#     ax.bar(x, code_aster_values, width, label='Code_Aster')
#     ax.bar(x + 0.2, elmer_values, width, label='Elmer')

#     target_value_x = [-1.5 * width, len(mesh_type) - 1 + 1.5 * width]
#     ax.plot(target_value_x, 0.125 * np.ones_like(target_value_x), c='black',
#             ls=('dashed'), label='Target')

#     ax.set_ylabel('Maximum Z displacement')
#     ax.set_title(plot_title)
#     ax.set_xticks(x)
#     ax.set_xticklabels(labels)
#     ax.yaxis.set_major_formatter(FormatStrFormatter('%.3f'))
#     ax.legend(facecolor='white', framealpha=1)
#     props = {"rotation" : 30}
#     plt.setp(ax.get_xticklabels(), **props)
#     fig.tight_layout()
#     plt.grid(color='gray', linestyle='-.', linewidth=0.5)
#     fig.savefig(file_name)
#     plt.show()

def plotly_test():
    import plotly.graph_objects as go
    import plotly.express as px


    plot_title = 'Triangle mesh comparison'
    file_name = 'triangle_raasch.png'
    results = pd.read_csv('raasch.csv')

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
                size=18,
            ),
            y=0.95,
            x=0.5),
        plot_bgcolor="#FFF",  # Sets background color to white
        xaxis=dict(
            linecolor="#BCCCDC",  # Sets color of X-axis line
            showgrid=True  # Removes X-axis grid lines
        ),
        yaxis=dict(
            title="Displacement [m]",  
            linecolor="#BCCCDC",  # Sets color of Y-axis line
            showgrid=True,  # Removes Y-axis grid lines    
        ),
        legend=dict(
            x=0.415,
            y=1.1,
            orientation="h",
        )
    )

    colours = px.colors.qualitative.Vivid
    fig = go.Figure(layout=layout)

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
   
if __name__ == "__main__":
    plotly_test()
    
