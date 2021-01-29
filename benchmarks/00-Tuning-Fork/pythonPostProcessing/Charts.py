import matplotlib.pyplot as plt
import matplotlib.lines as mlines
import numpy as np
import glob as gb
from matplotlib.font_manager import FontProperties

#Matrix of ideal frequencies values
ideal_frequency = np.full((9,1), 440)


def read_files(name_file, name_chart):
    
    #Read from results file			
    software_names = np.genfromtxt(name_file, dtype="str",skip_header = 1, usecols = (1))
    grid_size = np.genfromtxt(name_file, dtype="str",skip_header = 1, usecols = (2))
    all_frequencies = np.genfromtxt(name_file, skip_header = 1, usecols = (3))
    all_numbering = np.genfromtxt(name_file, skip_header = 1, usecols = (0))
    mesh_type = np.genfromtxt(name_file, dtype="str", max_rows=1)


    #Create plot
    fig, ax1 = plt.subplots()
    axes = plt.axes()

    #PLot data
    plt.plot (all_numbering[0:3], ideal_frequency[0:3],'--', color = 'orange', linewidth = '3')
    plt.xticks(all_numbering[0:3], grid_size[0:3])
    plt.plot(all_numbering[0:3], all_frequencies[0:3],'r+',markersize = 15)
    plt.plot(all_numbering[0:3], all_frequencies[3:6],'gx',markersize = 15)
    plt.plot(all_numbering[0:3], all_frequencies[6:9],'b.',markersize = 15)
    
    #Create axis names
    plt.yscale('Linear')
    plt.ylabel('Frequency [Hz]')
    plt.xlabel('Grid size [mm]')

    #Create label
    blue_dot = mlines.Line2D([], [], color='blue', marker='.', markersize=15, label=software_names[8])
    red_dot = mlines.Line2D([], [], color='red', marker='+', markersize=15, label=software_names[2])
    green_dot = mlines.Line2D([], [], color='green', marker='x', markersize=15, label=software_names[5])


    #Adjusts plot size	
    plt.subplots_adjust(right=0.75)
    plt.legend(handles=[red_dot,green_dot, blue_dot], title='Solver', bbox_to_anchor=(1.04, 0.5), loc='center left')

    #Scale labels
    ymin = round (min (all_frequencies)) - 1

    if name_file in ["QUAD-WEDGE.dat","QUAD-TET.dat","QUAD-HEX.dat"]:

        ymin = round (min (all_frequencies)) - 0.5
        ymax = round (max(all_frequencies)) + 0.5
        axes.set_ylim([ymin,ymax])
        plt.title(mesh_type)
        plt.grid(b=True)


        plt.savefig(str(mesh_type))

    elif ymin > 440:

        ymin = 438
        ymax = round (max(all_frequencies)) + 2.5
        axes.set_ylim([ymin,ymax])
        plt.title(mesh_type)
        plt.grid(b=True)
        plt.savefig(str(mesh_type))

    else :

        ymin = round (min(all_frequencies)) - 2.5
        ymax = round (max(all_frequencies)) + 2.5
        axes.set_ylim([ymin,ymax])
        plt.title(mesh_type)
        plt.grid(b=True)
        plt.savefig(str(mesh_type))


#Searcg data files
data_files = gb.glob("*.dat")


for data_file in data_files:


    name_chart_file = data_file.replace(".dat",".png")
    read_files(data_file,name_chart_file)
