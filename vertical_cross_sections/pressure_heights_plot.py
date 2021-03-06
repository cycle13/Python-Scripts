"""

Load geopotential heights/pt/sp hum and plot

22/05/14

"""

import os, sys
import numpy as np

import matplotlib

matplotlib.use('Agg') # Must be before importing matplotlib.pyplot or pylab!

import matplotlib.pyplot as plt
import matplotlib.cm as mpl_cm

from matplotlib import rc
from matplotlib.ticker import MultipleLocator, FormatStrFormatter

rc('font', family = 'serif', serif = 'cmr10')
rc('text', usetex=True)

c_section_lon=74.
c_section_lat=0

diags=['temp', 'sp_hum']
#experiment_ids = ['djznw', 'djzny', 'djznq', 'dklyu', 'dkmbq', 'dklwu', 'dklzq', 'djzns', 'dkjxq'  ]
experiment_ids = ['djzny', 'djznq', 'dklyu', 'dkmbq', 'dklwu', 'dklzq', 'djzns'  ]
p_levels = [1000., 950., 925., 850., 700., 500., 400., 300., 250., 200., 150., 100., 70., 50., 30., 20., 10.]



for experiment_id in experiment_ids:
    for diag in diags:
        if diag=='temp':
            clevpt_min=298.
            clevpt_max=350.
        if diag=='sp_hum':
            clevpt_min=0.
            clevpt_max=0.02
        if c_section_lon!=0:
            data=np.load('/nfs/a90/eepdw/Data/EMBRACE/Cross_Sections/%s_%s_height_XC_Longitude_%s.npz' % (experiment_id, diag, c_section_lon))
            xc=data['xc']
            coords=data['coord']
        if c_section_lat!=0:
            data=np.load('/nfs/a90/eepdw/Data/EMBRACE/Cross_Sections/%s_%s_height_XC_Latitude_%s.npz' % (experiment_id, diag, c_section_lat))
            xc=data['xc']
            coords=data['coord']

        X,Y = np.meshgrid(coords,p_levels)

        # grid the data.
        #zi = griddata(x,y,z,xi,yi,interp='linear')
        fig=plt.figure(figsize=(8,10))
        ax = fig.add_axes([0.05,0.05,0.9,0.85])
     
        
        if diag=='temp':
            plt.title('%s - Potential Temperature' % experiment_id)
            CS = ax.contourf(X,Y,np.swapaxes(xc,0,1), np.linspace(clevpt_min, clevpt_max, 8), cmap=plt.cm.jet)
            cbar = plt.colorbar(CS,orientation='horizontal', format='${%d}$')
            cbar.set_label('${K}$')
        if diag=='sp_hum':
            plt.title('%s - Specific Humidity' % experiment_id)
            CS = ax.contourf(X,Y,np.swapaxes(xc,0,1), np.linspace(clevpt_min, clevpt_max, 8), cmap=plt.cm.jet_r)
            cbar = plt.colorbar(CS,orientation='horizontal', format='${%.3f}$')
            cbar.set_label('${kg/kg}$')
        #CS = ax.contour(X,Y,np.swapaxes(xc,0,1), np.linspace(clevpt_min, clevpt_max, 10), colors='k')
        
        plt.ylim([950,300])
        plt.xlim([10,30])

        
        plt.gca().invert_yaxis
        #plt.clabel(CS, fontsize=9, inline=1)

        ax.xaxis.set_major_formatter(FormatStrFormatter('${%d}$'))
        ax.yaxis.set_major_formatter(FormatStrFormatter('${%d}$'))
        
        
        #plt.show()
        if c_section_lon!=0:
            plt.xlabel('Latitude')
        
            plt.savefig('/nfs/a90/eepdw/Figures/EMBRACE/Cross_Sections/%s_%s_height_XC_Longitude_%s.png' % (experiment_id, diag, c_section_lon), bbox_inches='tight')
        if c_section_lat!=0:
            plt.xlabel('Longitude')
            plt.savefig('/nfs/a90/eepdw/Figures/EMBRACE/Cross_Sections/%s_%s_height_XC_Latitude_%s.png' % (experiment_id, diag, c_section_lat), bbox_inches='tight')

        plt.close()

    


            
        

    
        

    

    
    
