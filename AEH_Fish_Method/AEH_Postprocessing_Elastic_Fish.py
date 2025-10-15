#
from odbAccess import *
import numpy as np
from itertools import product

#---------------------------------------------------------------------------------
#
satin_num = 2 # 2 for plain and 3 for twill
job_name = f'Job_woven{satin_num}_AEH2_elastic'
if satin_num == 2:
    tmp_num, t_num, s_num = satin_num, 1, 4
else:
    tmp_num = satin_num + 1
    t_num, s_num = 1, 8
yarn_w, yarn_h, yarn_sec1, yarn_sec2, extra_t = 2.0, 0.6, 1.8, 0.4, 0.04   # 2.2 for twill, 2.29 for plain
rve_t = yarn_h + yarn_sec2 + extra_t/s_num
rve_size = np.array([tmp_num*yarn_w + extra_t, rve_t, tmp_num*yarn_w + extra_t])
savefile = f'Woven{satin_num}_Homogenized_Stiffness_AEH2.txt'
#
odb = openOdb(f'{job_name}_1.odb')
dtm = odb.rootAssembly.DatumCsysByThreePoints(name='CSYS-1', coordSysType=CARTESIAN, origin=(0.0, 0.0, 0.0),
    point1=(1.0, 0.0, 0.0), point2=(0.0, 1.0, 0.0))
Instance = odb.rootAssembly.instances['PART-1-1']
homoStiff, VRVE = np.zeros([6, 6]), rve_size[0]*rve_size[1]*rve_size[2]
#
for iStep in range(6):
    F1V = (odb.steps[f'Step-{iStep+1}'].frames[-1].fieldOutputs['S'].getTransformedField(datumCsys=dtm)
           .getSubset(region=Instance, position=INTEGRATION_POINT).values)
    F2V = odb.steps[f'Step-{iStep+1}'].frames[-1].fieldOutputs['IVOL'].getSubset(region=Instance, position=INTEGRATION_POINT).values
    for iv in range(len(F1V)):
        homoStiff[iStep,:] -= np.divide(np.multiply(F1V[iv].data, F2V[iv].data), VRVE)
odb.close()
#
np.savetxt(savefile, homoStiff, delimiter=",")



