import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import pandas as pd
import os

#Use to manually load latex path on IAS machines if not loaded earlier 
os.environ["PATH"] += os.pathsep + "/software/texlive/2023/bin/x86_64-linux"

#Import using pandas
# df = pd.read_csv("./data/final/Interactive.548_OUT_tran.csv")
df = pd.read_csv("./data/Interactive.375_OUT.csv")

#Activate style
plt.style.use("./styles/BA.mplstyle")

#Create axis (default is 1x1)
fig, ax = plt.subplots()

xmin = min(df["OUTp (Design_Point=1) X"].values)
xscale = 10**12
xscale_suffix = 'p'

#plot on axis (column names are generated by pandas)
ax.plot((df["OUTp (Design_Point=1) X"].values-xmin)*xscale ,df["OUTp (Design_Point=1) Y"].values, label="OUTp")
ax.plot((df["OUTn (Design_Point=1) X"].values-xmin)*xscale ,df["OUTn (Design_Point=1) Y"].values, label="OUTn")

# ax.xaxis.set_major_formatter(ticker.FuncFormatter(lambda x, pos: '{:,.2f}'.format(x*10**9) + 'n'))

#Set axis labels
ax.set_xlabel(r"Time [\si{%s\second}]" % (xscale_suffix))
ax.set_ylabel(r"OUT [\si{\volt}]")

ax.set_xlim(0, 160)

#Show legend
# plt.legend(loc='upper center', ncol=2, bbox_to_anchor=(0.5, 1.15))
plt.legend(loc='upper right')

# plt.savefig("./plots/transient.pdf")
plt.show()
