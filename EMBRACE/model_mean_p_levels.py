"""
Average mean sea level pressure and save
"""

import os, sys

import itertools

import numpy as np

import h5py
import datetime
        
#experiment_ids = ['djzny','djznq', 'djznw']
experiment_ids = ['dklyu', 'dkmbq', 'dklwu', 'dklzq']
#experiment_ids = ['djznq', 'djzny', 'djznw', 'djzns', 'dkbhu','dkjxq', 'dklyu', 'dkmbq', 'dklwu', 'dklzq' ]
data_to_mean = ['temp', 'sp_hum']
dset = ['t_on_p', 'sh_on_p']


import iris.unit as unit

# There is some data missing from some of the runs, so cutting out first and last days.  Might need more for some, like 8km explicit.

u = unit.Unit('hours since 1970-01-01 00:00:00', calendar=unit.CALENDAR_STANDARD)
date_min = u.date2num(datetime.datetime(2011, 8, 19))
date_max = u.date2num(datetime.datetime(2011, 9, 7))

for experiment_id in experiment_ids:
    print experiment_id
    expmin1 = experiment_id[:-1]

    time_file_g = '/nfs/a90/eepdw/Model_Run_Time_Lists/djznw_time_list'
    with h5py.File(time_file_g, 'r') as i:
        dates_global= i['tstamps'][:]
        
    time_file = '/nfs/a90/eepdw/Model_Run_Time_Lists/%s_time_list' % experiment_id
    with h5py.File(time_file, 'r') as i:
        dates= i['tstamps'][:]
    #date_mask = np.ma.masked_outside(dates.flatten(), date_min,date_max)
    date_mask = np.in1d(dates.flatten(), dates_global.flatten())

# Calculate mean of variable like temperature and specific humidity
  
    for a, dm in enumerate(data_to_mean):
    
        fname = '/nfs/a90/eepdw/On_Heights_Interpolation_Data/%s_pressure_levels_interp_%s' % (dm,experiment_id)
        
        ds = dset[a]
        with h5py.File(fname, 'r') as i:
            #d = i['%s' % ds]
            #print d.shape

            with h5py.File('%s_mean_masked' % fname, 'w') as i2:
             mean = i2.create_dataset('mean' ,i['%s' % ds][0].shape, dtype='float32')
             print mean.shape
             print i['%s' % ds][0,0,0,:].shape
             sys.stdout.flush()
             for p in  range(len(i['%s' % ds][0,0,0,:])):
                 print '%s - %s' % (ds,p)
                 npmean =  i['%s' %ds][date_mask,:,:,p].mean(axis=0)
                 #npmean =  np.ma.array(i['interps'][:,:,:,p], mask=[date_mask.mask,:,:]).mean(axis=0)
                 mean[:,:,p]=npmean
                 sys.stdout.flush()                 
   
#Calculate mean of heights

    fname = '/nfs/a90/eepdw/On_Heights_Interpolation_Data/408_pressure_levels_interp_pressure_%s' % (experiment_id)

        
    with h5py.File(fname, 'r') as i:
                    #d = i['interps']
                    #print d
            with h5py.File('%s_mean_masked' % fname, 'w') as i2:
                mean = i2.create_dataset('mean' ,i['interps'][0].shape, dtype='float32')
                print i['interps'][0,0,0,: ].shape
                sys.stdout.flush()
                for p in  range(len(i['interps'][0,0,0,:])):
                    print p
                    sys.stdout.flush()
                    npmean =  i['interps'][date_mask,:,:,p].mean(axis=0)
                    # npmean =  np.ma.array(i['interps'][:,:,:,p], mask=date_mask.mask).mean(axis=0)
                    mean[:,:,p] =npmean                   
