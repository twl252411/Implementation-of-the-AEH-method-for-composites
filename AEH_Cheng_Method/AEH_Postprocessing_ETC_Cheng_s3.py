

from odbAccess import *
import numpy as np
from itertools import product

#----------------------------- Open the inp file ------------------------------
#
satin_num = 3 # 2 for plain and 3 for twill
new_job_name = f'Job_woven{satin_num}_AEH3_etc'
if satin_num == 2:
    tmp_num, t_num, s_num = satin_num, 1, 4
else:
    tmp_num = satin_num + 1
    t_num, s_num = 1, 8
yarn_w, yarn_h, yarn_sec1, yarn_sec2, extra_t = 2.0, 0.6, 1.8, 0.4, 0.04   # 2.2 for twill, 2.29 for plain
rve_t = yarn_h + yarn_sec2 + extra_t/s_num
rve_size = np.array([tmp_num*yarn_w + extra_t, rve_t, tmp_num*yarn_w + extra_t])
savefile = f'Woven{satin_num}_Homogenized_ETC_AEH3.txt'

# ------------------------------ SAVE THE RESULTS -----------------------------
#
T1 = np.loadtxt(f'{new_job_name}_ini_nd_t.txt', delimiter=',')
T2 = np.loadtxt(f'{new_job_name}_sec_nd_t.txt', delimiter=',')
RFL1 = np.loadtxt(f'{new_job_name}_ini_nd_rfl.txt', delimiter=',')
RFL2 = np.zeros_like(RFL1)
rve_volume = rve_size[0] * rve_size[1] * rve_size[2]
#
for iob in range(3): #
    odb = openOdb(f'{new_job_name}_3{iob+1}.odb')
    Instance = odb.rootAssembly.instances['PART-1-1']
    #
    F1V = odb.steps[f'Step-{iob+1}'].frames[-1].fieldOutputs['RFL11'].getSubset(region=Instance, position=NODAL).values
    for iv in range(len(F1V)):
        RFL2[F1V[iv].nodeLabel-1, 0] = F1V[iv].nodeLabel
        RFL2[F1V[iv].nodeLabel-1, iob+1] = F1V[iv].data
    odb.close()

#---------------------------------------------------------------------------------
#
diff_RFL = RFL1[:, 1:4] - RFL2[:, 1:4]  # Shape: (n, 3)
diff_T   = T1[:, 1:4]
homo_lambda = (diff_T.T @ diff_RFL) / rve_volume  # Matrix multiplication and normalization
np.savetxt(savefile, homo_lambda, delimiter=",")