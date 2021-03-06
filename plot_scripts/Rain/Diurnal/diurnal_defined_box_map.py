import os, sys

import matplotlib

matplotlib.use('Agg') # Must be before importing matplotlib.pyplot or pylab!

from matplotlib import rc
from matplotlib.font_manager import FontProperties
from matplotlib import rcParams
from matplotlib import cm

rc('font', family = 'serif', serif = 'cmr10')
rc('text', usetex=True)

rcParams['text.usetex']=True
rcParams['text.latex.unicode']=True
rcParams['font.family']='serif'
rcParams['font.serif']='cmr10'

from mpl_toolkits.basemap import Basemap
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon

def draw_screen_poly( lats, lons, m):
    x, y = m( lons, lats )
    xy = zip(x,y)
    poly = Polygon( xy, edgecolor=colour, facecolor='none', alpha=0.4, linewidth=2 )
    if (plot_coords[2]=='Southern Indian Ocean'):
       poly = Polygon( xy, edgecolor=colour, facecolor='none', alpha=0.4, linewidth=5 ) 
    plt.gca().add_patch(poly)

    legendEntries.append(poly)
    legendtext.append(plot_coords[2])

def label(lats, lons,  text):
    #y = xy[1] - 0.15 # shift y-value for label so that it's below the artist   
    lons_label = (np.max(lons)+np.min(lons)) / 2
    lats_label = (np.max(lats) + np.min(lats)) / 2
    x, y = m( lons_label, lats_label ) 
    plt.text(x, y, text, ha="center", size=14, color=colour)


# Bit above Western Ghats
lats_1 = [20, 28, 28, 20]
lons_1 = [67, 67, 71, 71]
label_1 = 'Bit above Western Ghats'

# Western Ghats
#lats_2 = [8, 21, 21, 8]
#lons_2 = [72, 72, 77, 77]
#label_2 = 'Western Ghats'

# Western Ghats
lats_2 = [8.75, 22., 22., 8.75]
lons_2 = [73.75, 70., 73.75, 77.75]
label_2 = 'Western Ghats'

# Bay of Bengal
lats_3 = [10, 25, 25, 10]
lons_3 = [80, 80, 100, 100]
label_3 = 'Bay of Bengal'

# Southern , western Indian Ocean
lats_4 = [-10, 5, 5, -10]
lons_4 = [64.12, 64.12, 80, 80]
label_4 = 'Southern, western Indian Ocean'

# Southern , western Indian Ocean
lats_5 = [-10, 5, 5, -10]
lons_5 = [80, 80, 101.87, 101.87]
label_5 = 'Southern, eastern Indian Ocean'

# Southern Indian Ocean
lats_6 = [-10, 5, 5, -10]
lons_6 = [64.12, 64.12, 101.87, 101.87]
label_6 = 'Southern Indian Ocean'

# Monsoon Trough
lats_7 = [21., 16., 22., 27]
lons_7 = [73., 83., 87., 75]
label_7 = 'Monsoon Trough'

# Himalayas
lats_8 = [25.8, 26.3, 30., 30., 28.5, 27.8, 27.8, 25.8]
lons_8 = [90., 83., 76.3, 82.7, 86.3, 90., 95., 95.]
label_8 = 'Himalayas'

#Ganga Basin
lats_9 = [22, 27., 30., 26.2, 25.8, 22]
lons_9 = [87, 75, 76.3, 83, 90., 90.]
label_9 = 'Ganga Basin'

lats = lats_1, lats_2, lats_3, lats_4, lats_5, lats_6, lats_7, lats_8, lats_9
lons = lons_1, lons_2, lons_3, lons_4, lons_5, lons_6, lons_7, lons_8, lons_9
labels = label_1, label_2, label_3, label_4, label_5, label_6, label_7, label_8, label_9


#for l, in enumerate (lats

print len(lats)
print lons                    

lon_high = 110.5
lon_low = 59.5
lat_high= 33.
lat_low=-10.5

NUM_COLOURS = len(lats)
cmap=cm.get_cmap(cm.Set1, NUM_COLOURS*2)

legendEntries=[]
legendtext=[]

fig = plt.figure(figsize=(20,8))
ax = fig.add_subplot(111)

m =\
Basemap(llcrnrlon=lon_low,llcrnrlat=lat_low,urcrnrlon=lon_high,urcrnrlat=lat_high,projection='mill', rsphere=6371229, resolution='h')
m.drawcoastlines(color='#262626')
#m.drawcountries(color='#262626')
m.drawmapboundary(color='#262626')

for l,plot_coords in enumerate(zip(lats,lons, labels)):
    colour = cmap(1.*(l*2)/(NUM_COLOURS*2))
    draw_screen_poly( plot_coords[0], plot_coords[1], m)
    label(plot_coords[0], plot_coords[1], l+1)
    
leg = plt.legend(legendEntries, legendtext, bbox_to_anchor=(1.05, 1), frameon=False, loc=2, borderaxespad=0.)

 # Change the legend label colors to almost black
texts = leg.texts
for t in texts:
    t.set_color('#262626')

plt.savefig('/nfs/a90/eepdw/Figures/EMBRACE/Diurnal/Diurnal_defined_area_boxes_map_notitle.png', format='png', bbox_inches='tight')
#plt.show()
#plt.title('\n'.join(wrap('%s' % (t.title()), 1000,replace_whitespace=False)), fontsize=16)
plt.title('Defined areas for calculating average diurnal rainfall variation for EMBRACE period', fontsize=16, color='#262626')

plt.savefig('/nfs/a90/eepdw/Figures/EMBRACE/Diurnal/Diurnal_defined_area_boxes_map.png', format='png', bbox_inches='tight')
