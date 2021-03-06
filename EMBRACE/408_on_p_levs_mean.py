"""
Load multiple pp diagnostic files, aggregate by year, day etc, calcualte mean, sum etc and save
"""

import os, sys
import datetime

import iris
import iris.unit as unit
from iris.coord_categorisation import add_categorised_coord

import pdb

diag = '_408_on_p_levs'

pp_file_path='/nfs/a90/eepdw/Data/EMBRACE/'

experiment_ids = ['djznw', 'djzny', 'djznq', 'djzns', 'dkjxq', 'dklyu', 'dkmbq', 'dklwu', 'dklzq'] # All minus large 3
#experiment_ids = ['djznw', 'djzny', 'djznq', 'dkjxq', 'dkmbq', 'dklzq']
experiment_ids = ['dkmgw']


#pdb.set_trace()

dtmindt = datetime.datetime(2011,8,19,0,0,0)
dtmaxdt = datetime.datetime(2011,9,7,23,0,0)
dtmin = unit.date2num(dtmindt, 'hours since 1970-01-01 00:00:00', unit.CALENDAR_STANDARD)
dtmax = unit.date2num(dtmaxdt, 'hours since 1970-01-01 00:00:00', unit.CALENDAR_STANDARD)
time_constraint = iris.Constraint(time= lambda t: dtmin <= t.point <= dtmax)

fg = '%sdjzn/djznw/djznw%s.pp' % (pp_file_path, diag)
glob_load = iris.load_cube(fg,  time_constraint)

## Get time points from global LAM to use as time constraint when loading other runs
time_list = glob_load.coord('time').points
glob_tc = iris.Constraint(time=time_list)



del glob_load

for experiment_id in experiment_ids:

 expmin1 = experiment_id[:-1]

 fu = '%s%s/%s/%s%s.pp' % (pp_file_path, expmin1, experiment_id, experiment_id, diag)
 print experiment_id
 sys.stdout.flush()

 try:
        #cube_names = ['%s' % cube_name_param, '%s' % cube_name_explicit]
        cube = iris.load_cube(fu)
       
        #time_coords = cube.coord('time')       

        try:
            os.remove('%s%s/%s/%s%s_mean.pp' % (pp_file_path, expmin1, experiment_id, experiment_id, diag))
        except OSError,e:
            print '%s%s/%s/%s%s_mean.pp NOT REMOVED' % (pp_file_path, expmin1, experiment_id, experiment_id, diag)
            print e
            pass 
        for height_slice in cube.slices(['time', 'grid_latitude', 'grid_longitude']):
            #pdb.set_trace()
            mean = height_slice.collapsed('time', iris.analysis.MEAN)
            iris.save((mean),'%s%s/%s/%s%s_mean.pp' % (pp_file_path, expmin1, experiment_id, experiment_id, diag), append=True)

 except iris.exceptions.ConstraintMismatchError:        
        pass

