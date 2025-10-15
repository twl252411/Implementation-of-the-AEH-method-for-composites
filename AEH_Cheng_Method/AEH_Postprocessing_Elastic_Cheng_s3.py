
from odbAccess import *
import numpy as np
from itertools import product
#


#----------------------------- Parameters ------------------------------
#
satin_num = 3 # 2 for plain and 3 for twill
new_job_name = f'Job_woven{satin_num}_AEH3_elastic'
if satin_num == 2:
    tmp_num, t_num, s_num = satin_num, 1, 4
else:
    tmp_num = satin_num + 1
    t_num, s_num = 1, 8
yarn_w, yarn_h, yarn_sec1, yarn_sec2, extra_t = 2.0, 0.6, 1.8, 0.4, 0.04   # 2.2 for twill, 2.29 for plain
rve_t = yarn_h + yarn_sec2 + extra_t/s_num
rve_size = np.array([tmp_num*yarn_w + extra_t, rve_t, tmp_num*yarn_w + extra_t])
savefile = f'Woven{satin_num}_Homogenized_Stiffness_AEH3.txt'

# ------------------------------ SAVE THE RESULTS -----------------------------
#
homo_stiff, VRVE = np.zeros([6,6]), rve_size[0]*rve_size[1]*rve_size[2]

#---------------------------------------------------------------------------------
#
odb = openOdb(f'{new_job_name}_3.odb')
dtm = odb.rootAssembly.DatumCsysByThreePoints(name='CSYS-1', coordSysType=CARTESIAN, origin=(0.0, 0.0, 0.0),
    point1=(1.0, 0.0, 0.0), point2=(0.0, 1.0, 0.0))
Instance = odb.rootAssembly.instances['PART-1-1']
#
for iStep in range(6):
    file_name = f'{new_job_name}_sec_nd_for_{iStep+1}.txt'
    F1V = (odb.steps[f"Step-{iStep + 1}"].frames[-1].fieldOutputs['RF'].getTransformedField(datumCsys=dtm).
           getSubset(region=Instance, position=NODAL).values)
    with open(file_name, 'w') as f:
        for value in F1V:
            line = ",".join([str(value.nodeLabel), format(value.data[0], ".12f"), format(value.data[1], ".12f"),
                             format(value.data[2], ".12f")])
            f.write(line + "\n")
odb.close()

#---------------------------------------------------------------------------------
#
data = {}
for i in range(1, 7):  # Steps 1 to 6
    try:
        data[f'InputU{i}'] = np.loadtxt(f'{new_job_name}_ini_nd_disp_{i}.txt', delimiter=',')
        data[f'RF{i}'] = np.loadtxt(f'{new_job_name}_ini_nd_for_{i}.txt', delimiter=',')
        data[f'U{i}'] = np.loadtxt(f'{new_job_name}_sec_nd_disp_{i}.txt', delimiter=',')
        data[f'SeRF{i}'] = np.loadtxt(f'{new_job_name}_sec_nd_for_{i}.txt', delimiter=',')
    except Exception as e:
        print(f"Error loading data for step {i}: {e}")

for i in range(len(data["InputU1"])):
    for row in range(6):
        for col in range(6):
            input_disp = data[f"InputU{row+1}"][i, 1:4] - data[f"U{row+1}"][i, 1:4]
            force_diff = data[f"RF{col+1}"][i, 1:4] - data[f"SeRF{col+1}"][i, 1:4]
            homo_stiff[row, col] += np.dot(input_disp, force_diff) / VRVE

#---------------------------------------------------------------------------------
#
np.savetxt(savefile, homo_stiff, delimiter=",")
#

