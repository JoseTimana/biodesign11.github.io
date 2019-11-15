#Starter code demonstrating how to read in the data
from mpl_toolkits.mplot3d import Axes3D
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt # plotting
import numpy as np # linear algebra
import os # accessing directory structure
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
print(os.listdir("C:\Laptop\Biodesign\Database python\input"))
print(os.listdir("C:\Laptop\Biodesign\Database python\input\mitbih_database"))

# Distribution graphs (histogram/bar graph) of column data
def plotPerColumnDistribution(df, nGraphShown, nGraphPerRow):
    nunique = df.nunique()
    df = df[[col for col in df if nunique[col] > 1 and nunique[col] < 50]] # For displaying purposes, pick columns that have between 1 and 50 unique values
    nRow, nCol = df.shape
    columnNames = list(df)
    nGraphRow = (nCol + nGraphPerRow - 1) / nGraphPerRow
    plt.figure(num = None, figsize = (6 * nGraphPerRow, 8 * nGraphRow), dpi = 80, facecolor = 'w', edgecolor = 'k')
    for i in range(min(nCol, nGraphShown)):
        plt.subplot(nGraphRow, nGraphPerRow, i + 1)
        columnDf = df.iloc[:, i]
        if (not np.issubdtype(type(columnDf.iloc[0]), np.number)):
            valueCounts = columnDf.value_counts()
            valueCounts.plot.bar()
        else:
            columnDf.hist()
        plt.ylabel('counts')
        plt.xticks(rotation = 90)
        plt.title(f'{columnNames[i]} (column {i})')
    plt.tight_layout(pad = 1.0, w_pad = 1.0, h_pad = 1.0)
    plt.show()

# Correlation matrix
def plotCorrelationMatrix(df, graphWidth):
    filename = df.dataframeName
    df = df.dropna('columns') # drop columns with NaN
    df = df[[col for col in df if df[col].nunique() > 1]] # keep columns where there are more than 1 unique values
    if df.shape[1] < 2:
        print(f'No correlation plots shown: The number of non-NaN or constant columns ({df.shape[1]}) is less than 2')
        return
    corr = df.corr()
    plt.figure(num=None, figsize=(graphWidth, graphWidth), dpi=80, facecolor='w', edgecolor='k')
    corrMat = plt.matshow(corr, fignum = 1)
    plt.xticks(range(len(corr.columns)), corr.columns, rotation=90)
    plt.yticks(range(len(corr.columns)), corr.columns)
    plt.gca().xaxis.tick_bottom()
    plt.colorbar(corrMat)
    plt.title(f'Correlation Matrix for {filename}', fontsize=15)
    plt.show()

# Scatter and density plots
def plotScatterMatrix(df, plotSize, textSize):
    df = df.select_dtypes(include =[np.number]) # keep only numerical columns
    # Remove rows and columns that would lead to df being singular
    df = df.dropna('columns')
    df = df[[col for col in df if df[col].nunique() > 1]] # keep columns where there are more than 1 unique values
    columnNames = list(df)
    if len(columnNames) > 10: # reduce the number of columns for matrix inversion of kernel density plots
        columnNames = columnNames[:10]
    df = df[columnNames]
    ax = pd.plotting.scatter_matrix(df, alpha=0.75, figsize=[plotSize, plotSize], diagonal='kde')
    corrs = df.corr().values
    for i, j in zip(*plt.np.triu_indices_from(ax, k = 1)):
        ax[i, j].annotate('Corr. coef = %.3f' % corrs[i, j], (0.8, 0.2), xycoords='axes fraction', ha='center', va='center', size=textSize)
    plt.suptitle('Scatter and Density Plot')
    plt.show()

#Let's check n file: ../input/mitbih_database/n.csv
n = 2
nRowsRead = 360*n # specify 'None' if want to read whole file
# 100.csv may have more rows in reality, but we are only loading/previewing the first 1000 rows
df1 = pd.read_csv('C:\Laptop\Biodesign\Database python\input\mitbih_database/112.csv', delimiter=',', nrows = nRowsRead)
df1.dataframeName = '112.csv'
nRow, nCol = df1.shape
print(f'There are {nRow} rows and {nCol} columns')
print(df1.head(1000))
#print(df1.iloc[[0],[1]])
#Convert to numpy array
npdf1 = df1.to_numpy()
print(npdf1)
sample = npdf1[:,0]
xsample = np.divide(sample,360)
MLII = npdf1[:,1]
yMLII = np.divide(np.subtract(MLII,850),204.8)
V5 = npdf1[:,2]
ecg = plt.figure('Ventricular Tachycardia Ambulatory Monitoring', figsize = (12,5))
ax = ecg.add_subplot(1,1,1)
ax.set(xlim = [0,2], ylim = [-1,1])
ax.plot(xsample,yMLII, color = 'black', linewidth = 1.5)

xmajor_ticks = np.arange(0, n + 0.2, 0.2)
xminor_ticks = np.arange(0, n + 0.04, 0.04)
ymajor_ticks = np.arange(-1, 1.5, 0.5)
yminor_ticks = np.arange(-1, 1.1, 0.1)

ax.set_xticks(xmajor_ticks)
ax.set_xticks(xminor_ticks, minor=True)
ax.set_yticks(ymajor_ticks)
ax.set_yticks(yminor_ticks, minor=True)

# And a corresponding grid
ax.grid(which='both')

# Or if you want different settings for the grids:
ax.set(title ='ECG Lead II', ylabel ='Voltage (mV)', xlabel = 'Time (s)')
plt.grid(b = True, which = 'major', color = 'red', linestyle = '-', linewidth = 1)
#plt.minorticks_on()
plt.grid(b = True, which = 'minor', color = 'red', linestyle = '-', alpha = 0.2)
plt.show()