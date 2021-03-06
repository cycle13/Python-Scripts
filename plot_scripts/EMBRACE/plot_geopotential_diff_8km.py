"""

Load mean geopotential heights and plot in colour

"""
import os, sys
from matplotlib import rc

import matplotlib
matplotlib.use('Agg')

import matplotlib.pyplot as plt
import matplotlib.cm as mpl_cm
from mpl_toolkits.basemap import Basemap
import iris
import iris.analysis.cartography
import numpy as np
import imp
import h5py

import cartopy.crs as ccrs
#import cartopy.io.img_tiles as cimgt
import matplotlib.ticker as mticker
from cartopy.mpl.gridliner import LONGITUDE_FORMATTER, LATITUDE_FORMATTER

import scipy.interpolate

try:
    import cStringIO as StringIO
except:
    import StringIO

import PIL
import Image

#from matplotlib.font_manager import FontProperties
#from matplotlib import rcParams


font = {'family' : 'normal',
        'weight' : 'bold',
        'size'   : 14}

matplotlib.rc('font', **font)

from textwrap import wrap

import math


model_name_convert_title = imp.load_source('util', '/nfs/see-fs-01_users/eepdw/python_scripts/modules/model_name_convert_title.py')

save_path='/nfs/a90/eepdw/Figures/EMBRACE/'

def main():

# Plot diagnostics, model and pressure levels etc. to plot on for looping through

 plot_type='mean_masked'
 plot_type_h5py_var = 'mean'
 plot_diags=['temp', 'sp_hum']
 plot_levels = [925, 850, 700, 500] 
 #plot_levels = [925]
 experiment_ids = ['dklyu']
 difference_id = 'dkmgw'
 diffidmin1 = difference_id[:-1]
 divisor=10  # for lat/lon rounding

 p_levels = [1000, 950, 925, 850, 700, 500, 400, 300, 250, 200, 150, 100, 70, 50, 30, 20, 10]

 degs_crop_top = 3.7
 degs_crop_bottom = 3.5
 degs_crop_left = 2
 degs_crop_right = 3


   ###############################################################################
####################  Load heights, winds and temp/sp_hum for difference id #####################

 
 f_glob_h = '/nfs/a90/eepdw/Data/EMBRACE/Pressure_level_means/408_pressure_levels_interp_pressure_%s_%s' % (difference_id, plot_type)
 
 with h5py.File(f_glob_h, 'r') as i:
     mh = i['%s' % plot_type_h5py_var]
     mean_heights_global = mh[. . .]

######################################################################################


 fu_g = '/nfs/a90/eepdw/Data/EMBRACE/Mean_State/pp_files/%s/%s/30201_mean.pp' % (diffidmin1, difference_id)
       
 u_wind_g,v_wind_g = iris.load(fu_g)
    
 for  pl in plot_diags:
  plot_diag=pl

  f_glob_d = '/nfs/a90/eepdw/Data/EMBRACE/Pressure_level_means/%s_pressure_levels_interp_%s_%s' % (plot_diag, difference_id, plot_type)
 

  with h5py.File(f_glob_d, 'r') as i:
   mg = i['%s' % plot_type_h5py_var]
   mean_var_global = mg[. . .]

  for experiment_id in experiment_ids:
    expmin1 = experiment_id[:-1]

    

    ###############################################################################
####################  Load  heights and temp/sp_hum #####################

    fname_h = '/nfs/a90/eepdw/Data/EMBRACE/Pressure_level_means/408_pressure_levels_interp_pressure_%s_%s' % (experiment_id, plot_type)
    fname_d = '/nfs/a90/eepdw/Data/EMBRACE/Pressure_level_means/%s_pressure_levels_interp_%s_%s' % (plot_diag, experiment_id, plot_type)
    # print fname_h
    # print fname_d
  
#  Height data file
    with h5py.File(fname_h, 'r') as i:
        mh = i['%s' % plot_type_h5py_var]
        mean_heights = mh[. . .]
    # print mean_heights.shape
    with h5py.File(fname_d, 'r') as i:
        mh = i['%s' % plot_type_h5py_var]
        mean_var = mh[. . .]
    # print mean_var.shape

    f_oro =  '/nfs/a90/eepdw/Data/EMBRACE/Mean_State/pp_files/%s/%s/33.pp' % (expmin1, experiment_id)
    oro = iris.load_cube(f_oro)

    fu = '/nfs/a90/eepdw/Data/EMBRACE/Mean_State/pp_files/%s/%s/30201_mean.pp' % (expmin1, experiment_id)
       
    u_wind,v_wind = iris.load(fu)
    lat_w = u_wind.coord('grid_latitude').points
    lon_w = u_wind.coord('grid_longitude').points
 
    p_levs = u_wind.coord('pressure').points

    lat = oro.coord('grid_latitude').points
    lon = oro.coord('grid_longitude').points

    cs = oro.coord_system('CoordSystem')  

    if isinstance(cs, iris.coord_systems.RotatedGeogCS):
        print ' 33.pp  - %s - Unrotate pole %s' % (experiment_id, cs)
        lons, lats = np.meshgrid(lon, lat) 

        lon_low= np.min(lons)
        lon_high = np.max(lons)
        lat_low = np.min(lats)
        lat_high = np.max(lats)

        lon_corners, lat_corners = np.meshgrid((lon_low, lon_high), (lat_low, lat_high))

        lons,lats = iris.analysis.cartography.unrotate_pole(lons,lats, cs.grid_north_pole_longitude, cs.grid_north_pole_latitude)
        lon_corner_u,lat_corner_u = iris.analysis.cartography.unrotate_pole(lon_corners, lat_corners, cs.grid_north_pole_longitude, cs.grid_north_pole_latitude)
        #lon_highu,lat_highu = iris.analysis.cartography.unrotate_pole(lon_high, lat_high, cs.grid_north_pole_longitude, cs.grid_north_pole_latitude)

        lon=lons[0]
        lat=lats[:,0]
        lon_low = lon_corner_u[0,0]
        lon_high = lon_corner_u[0,1]
        lat_low = lat_corner_u[0,0]
        lat_high = lat_corner_u[1,0]
 
        lon_min=np.min(lon)
        lon_max=np.max(lon)
  
        lon_low_tick=lon_min -(lon_min%divisor)
        lon_high_tick=math.ceil(lon_max/divisor)*divisor

        lat_min=np.min(lat)
        lat_max=np.max(lat)
        lat_low_tick=lat_min - (lat_min%divisor)
        lat_high_tick=math.ceil(lat_max/divisor)*divisor
    
    cs_w = u_wind.coord_system('CoordSystem')

    if isinstance(cs_w, iris.coord_systems.RotatedGeogCS):
        print ' Wind - %s - Unrotate pole %s' % (experiment_id, cs_w)
        lons_w, lats_w = np.meshgrid(lon_w, lat_w)
        lons_w,lats_w = iris.analysis.cartography.unrotate_pole(lons_w,lats_w, cs_w.grid_north_pole_longitude, cs_w.grid_north_pole_latitude)
        
        lon_w=lons_w[0]
        lat_w=lats_w[:,0]

    lon_high = 102
    lon_low = 64
    lat_high= 30.
    lat_low=-10


    csur_w=cs_w.ellipsoid
    for p in plot_levels:
  
        ### Search for pressure level match
    
        s = np.searchsorted(p_levels[::-1], p)          

# Difference heights

        plt_h = np.where(np.isnan(mean_heights[:,:,-(s+1)]), np.nan, mean_heights[:,:,-(s+1)] - mean_heights_global[:,:,-(s+1)])

#Difference temperature/specific humidity
   
        plt_v = np.where(np.isnan(mean_var[:,:,-(s+1)]), np.nan, mean_var[:,:,-(s+1)] - mean_var_global[:,:,-(s+1)])
    
    # Set u,v for winds, linear interpolate to approx. 2 degree grid
        sc =  np.searchsorted(p_levs, p)

        lat_wind_1deg = np.arange(lat_low,lat_high, 2)
        lon_wind_1deg = np.arange(lon_low,lon_high, 2)

    ### Regrid winds to 2 degree spacing
       
        lons_wi, lats_wi = np.meshgrid(lon_wind_1deg, lat_wind_1deg)

        fl_la_lo = (lats_w.flatten(),lons_w.flatten())

        u_wind_diff = u_wind[sc,:,:] - u_wind_g[sc,:,:]
        v_wind_diff = v_wind[sc,:,:] - v_wind_g[sc,:,:]

        u = scipy.interpolate.griddata(fl_la_lo, u_wind_diff.data.flatten(), (lats_wi, lons_wi), method='linear')
        v = scipy.interpolate.griddata(fl_la_lo, v_wind_diff.data.flatten(), (lats_wi, lons_wi), method='linear')
       
#######################################################################################

### Plotting #########################################################################

        rc('font', family = 'serif', serif = 'cmr10')
        rc('text', usetex=True)

        #m_title = 'Height of %s-hPa level (m)' % (p)

# Set pressure height contour min/max
        if p == 925:
            clev_min = -24.
            clev_max = 24.
        elif p == 850:
            clev_min = -24.
            clev_max = 24.
        elif p == 700:
            clev_min = -24.
            clev_max = 24.
        elif p == 500:
            clev_min = -24.
            clev_max = 24.
        else:
            print 'Contour min/max not set for this pressure level'

# Set potential temperature min/max       
        if p == 925:
            clevpt_min = -3.
            clevpt_max = 3.
        elif p == 850:
            clevpt_min = -3.
            clevpt_max = 3.
        elif p == 700:
            clevpt_min = -3.
            clevpt_max = 3.
        elif p == 500:
            clevpt_min = -3.
            clevpt_max = 3.
        else:
            print 'Potential temperature min/max not set for this pressure level'

 # Set specific humidity min/max       
        if p == 925:
            clevsh_min = -0.0025
            clevsh_max = 0.0025
        elif p == 850:
            clevsh_min = -0.0025
            clevsh_max = 0.0025
        elif p == 700:
            clevsh_min = -0.0025
            clevsh_max = 0.0025
        elif p == 500:
            clevsh_min = -0.0025
            clevsh_max = 0.0025
        else:
            print 'Specific humidity min/max not set for this pressure level'

        clevs_lin = np.linspace(clev_min, clev_max, num=24)

        m =\
Basemap(llcrnrlon=lon_low,llcrnrlat=lat_low,urcrnrlon=lon_high,urcrnrlat=lat_high, rsphere = 6371229)

        x,y = m(lons,lats)
        x_w,y_w = m(lons_wi, lats_wi)
        fig=plt.figure(figsize=(8,10))
        ax = fig.add_axes([0.05,0.05,0.9,0.85], axisbg='#262626')
   
        m.drawcoastlines(color='#262626')  
        m.drawcountries(color='#262626')  
        m.drawcoastlines(linewidth=0.5)
         #m.fillcontinents(color='#CCFF99')
        m.drawparallels(np.arange(int(lat_low_tick),int(lat_high_tick)+divisor,divisor),labels=[1,0,0,0], color='#262626')
        m.drawmeridians(np.arange(int(lon_low_tick),int(lon_high_tick)+divisor,divisor),labels=[0,0,0,1], color='#262626' )
    
        cs_lin = m.contour(x,y, plt_h, clevs_lin,colors='#262626',linewidths=0.5)
       
        cmap=plt.cm.RdBu_r
      
        if plot_diag=='temp':
            
             plt_v = np.ma.masked_outside(plt_v, clevpt_max+20,  clevpt_min-20)

             cs_col = m.contourf(x,y, plt_v,  np.linspace(clevpt_min, clevpt_max, 256), cmap=cmap, extend='both')
             
             cbar = m.colorbar(cs_col,location='bottom',pad="5%", format = '%d')  
             #cbar = plt.colorbar(cs_col, orientation='horizontal', pad=0.05, extend='both', format = '%d')
             tick_gap=1.
             cbar.set_ticks(np.arange(clevpt_min,clevpt_max+tick_gap,tick_gap))
             cbar.set_ticklabels(np.arange(clevpt_min,clevpt_max+tick_gap,tick_gap))
             cbar.set_label('K')  
             pn='8km  Explicit model (dklyu) minus 8km parametrised model geopotential height (grey contours), potential temperature (colours), and wind (vectors)'

        elif plot_diag=='sp_hum':
             plt_v = np.ma.masked_outside(plt_v, clevsh_max+20,  clevsh_min-20)

             cs_col = m.contourf(x,y, plt_v,  np.linspace(clevsh_min, clevsh_max, 256), cmap=cmap, extend='both')
             cbar = m.colorbar(cs_col,location='bottom',pad="5%", format = '%.3f') 
             #cbar = plt.colorbar(cs_col, orientation='horizontal', pad=0.05, extend='both', format = '%d')
             cbar.set_label('kg/kg')
             pn='8km  Explicit model (dklyu) minus 8km parametrised model geopotential height (grey contours), specific humidity (colours), and wind (vectors)'
        wind = m.quiver(x_w,y_w, u, v,scale=75, color='#262626' )
        qk = plt.quiverkey(wind, 0.1, 0.1, 1, '5 m/s', labelpos='W')
                
        plt.clabel(cs_lin, fontsize=14, fmt='%d', color='black')
   
        #pn='%s' % (model_name_convert_title.main(experiment_id))
        # pn in sphum and temp loops

        if not os.path.exists('%s%s/%s' % (save_path, experiment_id, plot_diag)): os.makedirs('%s%s/%s' % (save_path, experiment_id, plot_diag))

        # Save no title # #  
        ram = StringIO.StringIO()

        plt.savefig(ram, format='png', bbox_inches='tight', rasterized=True)
        #plt.savefig('%s%s/%s/geop_height_difference_8km_%shPa_%s_%s_notitle.png' % (save_path, experiment_id, plot_diag, p, experiment_id, plot_diag), format='png', bbox_inches='tight', rasterized=True)
        
        ram.seek(0)
        im = Image.open(ram)
        im2 = im.convert('RGB').convert('P', palette=Image.ADAPTIVE)
        im2.save('%s%s/%s/geop_height_difference_%shPa_%s_minus_%s_%s_notitle_large_font.png' \
                 % (save_path, experiment_id, plot_diag, p, experiment_id, diff_id, plot_diag) , format='PNG', optimize=True)

        plt.title('\n'.join(wrap('%s-hPa\n%s' % (p, pn) , 75, replace_whitespace=False)), fontsize=16, color='#262626')
        #plt.show()  
        
         # Save with title # #  

        ram = StringIO.StringIO()

        plt.savefig(ram, format='png', bbox_inches='tight', rasterized=True)
        #plt.savefig('%s%s/%s/geop_height_difference_8km_%shPa_%s_%s.png' % (save_path, experiment_id, plot_diag, p, experiment_id, plot_diag), format='png', bbox_inches='tight', rasterized=True)

        ram.seek(0)
        im = Image.open(ram)
        im2 = im.convert('RGB').convert('P', palette=Image.ADAPTIVE)
        im2.save('%s%s/%s/geop_height_difference_8km_%shPa_%s_minus_%s_%s_large_font.png' \
                 % (save_path, experiment_id, plot_diag, p, experiment_id, diff_id, plot_diag) , format='PNG', optimize=True)
       
    
        plt.cla()
        plt.clf()

        #  Save fig - update dpi if need for printing
if __name__ == '__main__':
    main()
