import matplotlib.pyplot as plt
import numpy as np
import glob as gb
import pandas as pd
from collections import defaultdict, OrderedDict
result_file_names = gb.glob("CSV/Mises/*.csv")

max_y_value = []
limit = 2.5
values = OrderedDict()
ccx = OrderedDict()

nested_dict = lambda: defaultdict(nested_dict)
to_mdwn = nested_dict()
lin_results = pd.DataFrame(columns = ['Soft', 'Shape', 'Coarse Mesh', 'Medium Mesh', 'Fine Mesh', 'Very Fine Mesh'])
for result in result_file_names:
    # print(result)
    key = result.split('/')[-1].replace('_mises.csv','')
    df = pd.read_csv(result)
    if 'ccx' in key:
        x, y = df['Points:1'].to_list(), df['S_Mises'].to_list()
    elif 'elmer' in key:
        x, y = df['Points:1'].to_list(), df['vonmises'].to_list()
    else:
        raise ValueError
    x, y = np.abs(np.array(x)), np.array(y)
    x = x[x <= limit]
    y = y[:len(x)]
    values[key] = [x,y]

    f = np.interp(0.214204, x, y)
    temp = defaultdict(OrderedDict)
    mesh, soft = key.split('_')
    # print(mesh)

    if mesh.count('-') == 2:
        size, shape, topo = mesh.split('-')
        to_mdwn[soft][shape][size] = f
        # to_mdwn['212']['asda'] = 3
        # print(to_mdwn)
    else:
        size1, size2, shape, topo = mesh.split('-')
        size = '{}-{}'.format(size1, size2)
        to_mdwn[soft][shape][size] = f
        # lin_results[]

for soft, vals_1 in to_mdwn.items():
    temp = {'Soft': soft}
    for shape, vals_2 in vals_1.items():
        temp['Shape'] = shape
        for mesh, mises in vals_2.items():
            if mesh == 'coarse':
                temp['Coarse Mesh'] = mises
            elif mesh == 'med':
                temp['Medium Mesh'] = mises
            elif mesh == 'fine':
                temp['Fine Mesh'] = mises
            elif mesh == 'very-fine':
                temp['Very Fine Mesh'] = mises
        lin_results = lin_results.append(temp, ignore_index=True)

# linear = lin_results[lin_results['Shape'] == 'lin']
lin_results = lin_results.set_index('Soft')
lin_results = lin_results.sort_values(by='Shape')
# linear = linear.drop(['Shape'], axis=1)
print(lin_results.to_markdown())
# mark = pd.DataFrame.from_dict(mark)
# print(mark.to_markdown())

fig, ax = plt.subplots()
for key, vals in values.items():
    x, y = vals
    ax.plot(x, y, label=key)

plt.grid()
plt.legend()
plt.show()

