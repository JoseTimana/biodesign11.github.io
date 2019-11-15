#!/usr/bin/python3
#Starter code demonstrating how to read in the data
from mpl_toolkits.mplot3d import Axes3D
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt # plotting
import numpy as np # linear algebra
import os # accessing directory structure
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
#Let's check x file: ../input/mitbih_database/x.csv
for i in range(9,10):
    df1 = 0
    npdf1 = 0
    sample = 0
    xsample = 0

    tf = 60*0+10
    ti = 60*0+0
    df1 = pd.read_csv('C:\Laptop\Biodesign\Database python\input\mitbih_database/10'+ str(i)+'.csv', delimiter=',', nrows = 360*(tf-ti), skiprows = 360*ti)

    #Convert to numpy array
    npdf1 = df1.to_numpy()
    #Define axis for plotting
    sample = npdf1[:,0]
    xsample = np.divide(sample,360)
    MLII = npdf1[:,1]
    zero = np.mean(MLII) #Define zero voltage
    yMLII = np.divide(np.subtract(MLII,zero),204.8)

    #from scipy.signal import savgol_filter
    #fyMLII = savgol_filter(yMLII, 51, 11) # window size 51, polynomial order 3

    #Start plotting Time vs Voltage
    ecg = plt.figure('Ventricular Tachycardia Ambulatory Monitoring', figsize = (12,5))
    ax = ecg.add_subplot(1,1,1)
    ax.plot(xsample,yMLII, color = 'black', linewidth = 1.5)
    ax.set(title ='ECG Lead II', ylabel ='Voltage (mV)', xlabel = 'Time (s)')

    #ECG ticks
    xmajor_ticks = np.arange(ti, tf+0.2, 0.2)
    xminor_ticks = np.arange(ti, tf+0.04, 0.04)
    ymajor_ticks = np.arange(-2, 2, 0.5)
    yminor_ticks = np.arange(-2, 2, 0.1)

    ax.set_xticks(xmajor_ticks)
    ax.set_xticks(xminor_ticks, minor=True)
    ax.set_yticks(ymajor_ticks)
    ax.set_yticks(yminor_ticks, minor=True)

    #Limit data to show
    ax.set(xlim = [ti,tf], ylim = [-2, 2])

    # ECG grids
    plt.grid(b = True, which = 'major', color = 'red', linestyle = '-', linewidth = 1)
    plt.grid(b = True, which = 'minor', color = 'red', linestyle = '-', alpha = 0.2)

    #Find peaks
    from scipy.signal import find_peaks
    peaks, _ = find_peaks(yMLII, distance = 60*6*0.6)
    plt.plot(peaks/360 + ti, yMLII[peaks], "o", color = 'purple', markersize = 5)
    #Plot heart rate
    print(60/(peaks[2]/360 - peaks[1]/360))
    necg = i
    plt.savefig('C:\Laptop\Biodesign\Database python\ECG/ecg'+str(necg)+'.png', bbox_inches='tight')
    ecg = 0
