import numpy as np
from itertools import product
from odbAccess import *

#----------------------------- Parameters ------------------------------
#
satin_num = 3 # 2 for plain and 3 for twill
job_name = f'Job_woven{satin_num}_FEH_cte'
if satin_num == 2:
    tmp_num, t_num, s_num = satin_num, 1, 4
else:
    tmp_num = satin_num + 1
    t_num, s_num = 1, 8
yarn_w, yarn_h, yarn_sec1, yarn_sec2, extra_t = 2.0, 0.6, 1.8, 0.4, 0.04   # 2.2 for twill, 2.29 for plain
rve_t = yarn_h + yarn_sec2 + extra_t/s_num
rve_size = np.array([tmp_num*yarn_w + extra_t, rve_t, tmp_num*yarn_w + extra_t])
savefile1 = f'Woven{satin_num}_Homogenized_Stiffness_FEH.txt'
savefile2 = f'Woven{satin_num}_Homogenized_CTE2_FEH.txt'
homo_stiff = np.loadtxt(savefile1, delimiter=",")
#
odb = openOdb(f'{job_name}_2.odb')
dtm = odb.rootAssembly.DatumCsysByThreePoints(name='CSYS-1', coordSysType=CARTESIAN, origin=(0.0, 0.0, 0.0),
    point1=(1.0, 0.0, 0.0), point2=(0.0, 1.0, 0.0))
Instance = odb.rootAssembly.instances['PART-1-1']
homo_beta, VRVE = np.zeros([6]), rve_size[0] * rve_size[1] * rve_size[2]
#
F1V = (odb.steps[f'Step-1'].frames[-1].fieldOutputs['S'].getTransformedField(datumCsys=dtm).
    getSubset(region=Instance, position=INTEGRATION_POINT).values)
F2V = odb.steps[f'Step-1'].frames[-1].fieldOutputs['IVOL'].getSubset(region=Instance, position=INTEGRATION_POINT).values
for iv in range(len(F1V)):
    homo_beta += np.divide(np.multiply(F1V[iv].data, F2V[iv].data), VRVE)
odb.close()
#
inv_stiff = np.linalg.inv(homo_stiff)
temp_alpha = - np.dot(inv_stiff, homo_beta)
#
homo_alpha = np.zeros((3,3))
homo_alpha[0,0] = temp_alpha[0]
homo_alpha[1,1] = temp_alpha[1]
homo_alpha[2,2] = temp_alpha[2]
homo_alpha[0,1] = temp_alpha[3]
homo_alpha[0,2] = temp_alpha[4]
homo_alpha[1,2] = temp_alpha[5]
homo_alpha[1,0] = temp_alpha[3]
homo_alpha[2,0] = temp_alpha[4]
homo_alpha[2,1] = temp_alpha[5]

# ------------------------------ ------------------------------------------------
#
np.savetxt(savefile2, homo_alpha, delimiter=",")