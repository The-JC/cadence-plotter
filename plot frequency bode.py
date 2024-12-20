import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import pandas as pd
import numpy as np
import os

from plot_utils import *

name_base = "AC_OUTn"
name_suffix = ["(Design_Point=218)", "(Design_Point=2)"]
labels = ["Two LC-Filter", "One LC-Filter"]
file_name = ["./data/filter/2nd_order_25GHz.csv", "./data/filter/1st_order_25GHz.csv"]


y_min = -60
y_max = 30
x_min = 1
x_max = 100

xlim=(x_min, x_max)

xscale = 10**-9#
xscale_suffix = 'G'


#Use to manually load latex path on IAS machines if not loaded earlier 
os.environ["PATH"] += os.pathsep + "/software/texlive/2023/bin/x86_64-linux"

def plotWithSFDR(ax, x, y):
    #plot on axis (column names are generated by pandas)

    peakind = find_peaks(x, height=-30)[0]
    pksf=x[peakind]
    pksY=y[peakind]
    isorted = np.argsort(pksY)
    sfdrval = pksY[isorted[-1]] - pksY[isorted[-2]]

    pkfa = pksf[isorted[-1]]*xscale
    pkYa = pksY[isorted[-1]]
    pkfb = pksf[isorted[-2]]*xscale
    pkYb = pksY[isorted[-2]]
    # ax.fill_between((0,100),(pkYb,pkYb),(pkYa,pkYa), label = 'SFDR',
    #                      color = "lightblue") 

    ax.plot([pkfa, x_max], [pkYa, pkYa], c='black')
    ax.plot([pkfb, x_max], [pkYb, pkYb], c='black')
    ax.annotate('', xy=((pkfb*2+x_max)/3, pkYa), xycoords='data',
                xytext=((pkfb*2+x_max)/3, pkYb), textcoords='data',
                arrowprops=dict(arrowstyle="<->",
                                connectionstyle=patches.ConnectionStyle.Bar(armA=0.0, armB=0.0, fraction=0.0, angle=None),
                                #ec="k",
                                shrinkA=1, shrinkB=1)) 
    ax.annotate("SFDR %ddB" % (pkYa-pkYb), ((pkfb*2+x_max)/3+1, (pkYa+pkYb)/2), va='center', ha='left')

    ax.scatter(
        pksf*xscale,
        pksY,
        marker='x',
        c='r')

def plotDiff(ax, x1, x2, x, y, xscale, x_offset=0):
    index1 = np.where(x*xscale==x1)[0][0]
    index2 = np.where(x*xscale==x2)[0][0]

    y1 = y[index1]
    y2 = y[index2]

    ax.plot([x1, x2+x_offset+1], [y1, y1], c='black')
    if x_offset > 0:
        ax.plot([x2, x2+x_offset], [y2, y2], c='black')
    ax.plot([x1], [y1], marker="x", color='#CC071E')
    ax.plot([x2], [y2], marker="x", color='#CC071E')
    ax.annotate('', xy=(x2+x_offset, y1), xycoords='data',
                xytext=(x2+x_offset, y2), textcoords='data',
                arrowprops=dict(arrowstyle="<->",
                                connectionstyle=patches.ConnectionStyle.Bar(armA=0.0, armB=0.0, fraction=0.0, angle=None),
                                #ec="k",
                                shrinkA=1, shrinkB=1)) 
    ax.annotate("%ddB" % (y1-y2), (x2+x_offset+2, (y1+y2)/2), va='center', ha='left')

# ax.xaxis.set_major_formatter(ticker.FuncFormatter(lambda x, pos: '{:,.2f}'.format(x*10**9) + 'n'))

if __name__ == "__main__":
    #Activate style
    plt.style.use("./styles/presentation.mplstyle")



    #Create axis (default is 1x1)
    fig, ax = plt.subplots(1, 1)

    for i in range(0, len(name_suffix)):

        #Import using pandas
        df = pd.read_csv(file_name[i])

        # x = getData(df,name_base, strF)
        x = getData(df, name_base, name_suffix[i], 'X')
        y = getData(df, name_base, name_suffix[i], 'Y')
        plotDF(ax, x, y, "%s" % (labels[i]), xscale)

        # minSFDR(ax, df, name_base, [name_suffix], xlim, xscale)

        #Set axis labels

        ax.set_ylim(y_min, y_max)
        ax.set_xlim(x_min, x_max)

        plotDiff(ax, 25, 50, x, y, xscale, 3*i)


    ax.set_xlabel(r"Frequency [\si{%s\hertz}]" % (xscale_suffix))
    ax.set_ylabel(r"Attenuation [\si{\decibel}]")
    # ax.legend(loc='upper center', ncol=2, bbox_to_anchor=(0.5, 1.15))
    ax.legend()

    #Show legend
    # plt.legend(loc='upper center', ncol=3, bbox_to_anchor=(0.5, 1.15))

    plt.savefig(r"./plots/filter_bode_%s.svg" % (name_base))
    plt.show()
