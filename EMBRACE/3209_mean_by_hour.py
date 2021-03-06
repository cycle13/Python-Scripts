"""
Load multiple pp diagnostic files, aggregate by year, day etc, calcualte mean, sum etc and save
"""

import os, sys
import datetime

import iris
import iris.unit as unit
from iris.coord_categorisation import add_categorised_coord
from iris.analysis.cartography import unrotate_pole
from iris.coords import DimCoord

import numpy as np

import pdb

diag = '3209'

cube_names=['','']

#pp_file_path='/projects/cascade/pwille/moose_retrievals/'
pp_file_path='/nfs/a90/eepdw/Data/EMBRACE/'

experiment_ids = ['djznw', 'djzny', 'djznq', 'djzns', 'dkjxq', 'dklyu', 'dkmbq', 'dklwu', 'dklzq'] # All minus large 3
#experiment_ids = ['djzns', 'dkjxq', 'dklyu', 'dkmbq', 'dklwu', 'dklzq'] # All minus large 3

#experiment_ids = ['djznw', 'djzny', 'djznq', 'dkjxq', 'dkmbq', 'dklzq']

regrid_model='djznw'
regrid_model_min1=regrid_model[:-1]

def add_hour_of_day(cube, coord, name='hour'):
    add_categorised_coord(cube, name, coord,
          lambda coord, x: coord.units.num2date(x).hour)

dtmindt = datetime.datetime(2011,8,19,0,0,0)
dtmaxdt = datetime.datetime(2011,9,7,23,0,0)
dtmin = unit.date2num(dtmindt, 'hours since 1970-01-01 00:00:00', unit.CALENDAR_STANDARD)
dtmax = unit.date2num(dtmaxdt, 'hours since 1970-01-01 00:00:00', unit.CALENDAR_STANDARD)
time_constraint = iris.Constraint(time= lambda t: dtmin <= t.point <= dtmax)

fr = '%s%s/%s/%s.pp' % (pp_file_path, regrid_model_min1, regrid_model, diag)
fg = '%sdjzn/djznw/%s.pp' % (pp_file_path, diag)

glob_load = iris.load(fg, time_constraint)[0]



## Get time points from global LAM to use as time constraint when loading other runs
time_list = glob_load.coord('time').points
# Some models have radiation diagnostics that are 10s offset from others so checking int values of time 
glob_tc = iris.Constraint(time= lambda t: int(t.point) in time_list.astype(int))
#glob_tc = iris.Constraint(time=time_list)

del glob_load

for experiment_id in experiment_ids:

 expmin1 = experiment_id[:-1]

 fu = '%s%s/%s/%s.pp' % (pp_file_path, expmin1, experiment_id, diag)

 print experiment_id
 sys.stdout.flush()

 try:
     os.remove('%s%s/%s/%s_mean_by_hour.pp' % (pp_file_path, expmin1, experiment_id, diag))
 except OSError:
     print '%s%s/%s/%s_mean_by_hour.pp NOT REMOVED' % (pp_file_path, expmin1, experiment_id, diag)
     pass 



 
 
for c, cube_name in enumerate(cube_names):
     
         cube = iris.load(fu,  glob_tc)[c]

         #pdb.set_trace()

         mean_list=[]
         for pressure_cube in (cube.slices(['time', 'grid_latitude', 'grid_longitude'])):

             time_coords = pressure_cube.coord('time')
             add_hour_of_day(pressure_cube, time_coords)

             pc_time_merge = pressure_cube.aggregated_by('hour', iris.analysis.MEAN)
             pc_time_merge.add_dim_coord(DimCoord(points=pc_time_merge.coords('time')[0].bounds[:,0].flatten(),\
                                        long_name='time', standard_name='time',units=pc_time_merge.coords('time')[0].units),0)

             mean_list.extend(iris.cube.CubeList([pc_time_merge]))

         mean = iris.cube.CubeList(mean_list).merge_cube()  
         iris.save((mean),'%s%s/%s/%s_%s_mean_by_hour_regrid.pp' % (pp_file_path, expmin1, experiment_id, diag, c), append=True)



