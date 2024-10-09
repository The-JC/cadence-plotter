from scipy.signal import find_peaks
import matplotlib.patches as patches
import numpy as np

def plotDF(ax, x, y, label, xscale=1):
    ax.plot(x*xscale ,y, label=label)

def getData(df, base, str, ind):
    return df[r"%s %s %s" % (base, str, ind)].values

def minSFDR(ax, df, name_base, data_names, xlim, xscale):
    (x_min, x_max) = (xlim)
    max_branchA = None
    max_branchB = None

    glb_pkfa = 0
    glb_pkYa = 0
    glb_pkfb = 0
    glb_pkYb = 0

    for strF in data_names:
        x = getData(df,name_base, strF, 'X')
        y = getData(df,name_base, strF, 'Y')
        peakind = find_peaks(y, height=-50)[0]
        pksf    = x[peakind]
        pksY    = y[peakind]
        isorted = np.argsort(pksY)
        sfdrval = pksY[isorted[-1]] - pksY[isorted[-2]]
        pkfa = pksf[isorted[-1]]*xscale
        pkYa = pksY[isorted[-1]]
        pkfb = pksf[isorted[-2]]*xscale
        pkYb = pksY[isorted[-2]]

        if max_branchA == None or pkYa > glb_pkYa:
            max_branchA = strF
            glb_pkfa = pkfa
            glb_pkYa = pkYa
        if max_branchB == None or pkYb > glb_pkYb:
            max_branchB = strF
            glb_pkfb = pkfb
            glb_pkYb = pkYb

    ax.plot([glb_pkfa, x_max], [glb_pkYa, glb_pkYa], c='black')
    ax.plot([glb_pkfb, x_max], [glb_pkYb, glb_pkYb], c='black')
    ax.annotate('', xy=((glb_pkfb*2+x_max)/3, glb_pkYa), xycoords='data',
                xytext=((glb_pkfb*2+x_max)/3, glb_pkYb), textcoords='data',
                arrowprops=dict(arrowstyle="<->",
                                connectionstyle=patches.ConnectionStyle.Bar(armA=0.0, armB=0.0, fraction=0.0, angle=None),
                                #ec="k",
                                shrinkA=1, shrinkB=1)) 
    ax.annotate("SFDR %ddB" % (glb_pkYa-glb_pkYb), ((glb_pkfb*2+x_max)/3+1, (glb_pkYa+glb_pkYb)/2), va='center', ha='left')