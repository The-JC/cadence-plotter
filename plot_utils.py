from scipy.signal import find_peaks
import matplotlib.patches as patches
import numpy as np

def plotDF(ax, x, y, label, xscale=1):
    ax.plot(x*xscale ,y, label=label)

def getData(df, base, str, ind):
    return df[r"%s %s %s" % (base, str, ind)].values

def intersection(y1, y2, tol=5e-2):
    close = np.isclose(y1, y2, atol=tol)
    return np.where(close == True)[0]

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

def minSFDR_XY(ax, x, y, x_lim_sfdr, atol, xscale, shrink=1):
    ind_x_min = np.where(abs(x*xscale-x_lim_sfdr[0]) <= atol)[0][0]
    ind_x_max = np.where(abs(x*xscale-x_lim_sfdr[1]) <= atol)[0][0]
    peakind = find_peaks(np.power(10, y[ind_x_min:ind_x_max]))[0]
    pksf=x[ind_x_min+peakind]
    pksY=y[ind_x_min+peakind]
    isorted = np.argsort(pksY)
    sfdrval = pksY[isorted[-1]] - pksY[isorted[-2]]

    pkfa = pksf[isorted[-1]]*xscale
    pkYa = pksY[isorted[-1]]
    pkfb = pksf[isorted[-2]]*xscale
    pkYb = pksY[isorted[-2]]
    print(f"First peak at {pkfa}, second at {pkfb}")
    # ax.fill_between((0,100),(pkYb,pkYb),(pkYa,pkYa), label = 'SFDR',
    #                      color = "lightblue") 

    x_max = ax.get_xlim()[1]
    y_range = ax.get_ylim()[1]-ax.get_ylim()[0]
    ax.plot([pkfa, x_max], [pkYa, pkYa], c='black')
    ax.plot([pkfb, x_max], [pkYb, pkYb], c='black')
    if sfdrval < y_range*0.1:
        ax.annotate('', xy=(pkfb+1, pkYa), xycoords='data',
                xytext=(pkfb+1, pkYa+y_range*0.1), textcoords='data',
                arrowprops=dict(arrowstyle="->",
                                connectionstyle=patches.ConnectionStyle.Bar(armA=0.0, armB=0.0, fraction=0.0, angle=None),
                                #ec="k",
                                shrinkA=shrink, shrinkB=shrink))
        ax.annotate('', xy=(pkfb+1, pkYb), xycoords='data',
                xytext=(pkfb+1, pkYb-y_range*0.1), textcoords='data',
                arrowprops=dict(arrowstyle="->",
                                connectionstyle=patches.ConnectionStyle.Bar(armA=0.0, armB=0.0, fraction=0.0, angle=None),
                                #ec="k",
                                shrinkA=shrink, shrinkB=shrink))
        ax.annotate(r"%d\si{\decibel}" % (pkYa-pkYb), (pkfb+2, pkYb-y_range*0.05), va='center', ha='left') 
    else:
        ax.annotate('', xy=(pkfb+1, pkYa), xycoords='data',
                xytext=(pkfb+1, pkYb), textcoords='data',
                arrowprops=dict(arrowstyle="<->",
                                connectionstyle=patches.ConnectionStyle.Bar(armA=0.0, armB=0.0, fraction=0.0, angle=None),
                                #ec="k",
                                shrinkA=shrink, shrinkB=shrink)) 
        ax.annotate(r"%d\si{\decibel}" % (pkYa-pkYb), (pkfb+2, (pkYa+pkYb)/2), va='center', ha='left')
    # ax.annotate('', xy=((pkfb*2+x_max)/3, pkYa), xycoords='data',
    #             xytext=((pkfb*2+x_max)/3, pkYb), textcoords='data',
    #             arrowprops=dict(arrowstyle="<->",
    #                             connectionstyle=patches.ConnectionStyle.Bar(armA=0.0, armB=0.0, fraction=0.0, angle=None),
    #                             #ec="k",
    #                             shrinkA=1, shrinkB=1)) 
    # ax.annotate("SFDR %ddB" % (pkYa-pkYb), ((pkfb*2+x_max)/3+1, (pkYa+pkYb)/2), va='center', ha='left')

    pksf = np.array([pkfa, pkfb])
    pksY = np.array([pkYa, pkYb])
    ax.scatter(
        pksf,
        pksY,
        marker='x',
        c='r')