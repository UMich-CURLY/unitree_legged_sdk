# create a python script that reads the .log file and plots the data
#
# the script should be able to plot any data in the .log file

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import os
import argparse
import logging
import sys
import datetime
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import style
from matplotlib.animation import FuncAnimation
from matplotlib.colors import ListedColormap, LinearSegmentedColormap
from matplotlib import rc
from matplotlib import rcParams
from matplotlib import cm



def main():
    # create a parser to read the arguments from the command line
    parser = argparse.ArgumentParser(description='Analyze the log file')
    parser.add_argument('--log', type=str, default='log.log', help='log file to be analyzed')
    parser.add_argument('--plot', type=str, default='none', help='plot the data')
    parser.add_argument('--save', type=str, default='no', help='save the plot')
    parser.add_argument('--show', type=str, default='yes', help='show the plot')
    parser.add_argument('--save_path', type=str, default='.', help='path to save the plot')
    parser.add_argument('--save_name', type=str, default='plot', help='name of the plot')
    parser.add_argument('--save_format', type=str, default='png', help='format of the plot')

    # parse the arguments
    args = parser.parse_args()

    # set the log file
    log_file = args.log
    
    # set the plot
    plot = args.plot

    # set the save
    save = args.save

    # set the show
    show = args.show

    # set the save path
    save_path = args.save_path

    # set the save name
    save_name = args.save_name

    # set the save format
    save_format = args.save_format
    
    with open(log_file, 'r') as f:
        header = f.readline().split(' ')
        header = [x for x in header if x != '']
    
    feet_order = ['time','FR', 'FL', 'RR', 'RL','\n']


    # Read the data from the log file where the values are separated by a || and do not read the last column
    data = pd.read_csv(log_file, sep=' ', header=None, skiprows=1, engine='python', names=feet_order)


    # data.to_csv('file.csv')
    # get the indices where the contact is true for each leg
    del data['\n']
    del header[-1]
    print(data)
    plt.figure()
    for i in range(4):
        plt.subplot(2, 2, i+1)
        plt.plot(data['time'][5000:6000]*0.002, data[feet_order[i+1]][5000:6000])
        plt.ylabel('Force (N)')
        plt.xlabel('time')
        plt.title('Force on foot ' + feet_order[i+1])
    if save == 'yes':
        plt.savefig(save_path + '/' + save_name + '_' + feet_order[i+1] + '.' + save_format)
    if show == 'yes':
        plt.show()


if __name__ == '__main__':
    main()

    

