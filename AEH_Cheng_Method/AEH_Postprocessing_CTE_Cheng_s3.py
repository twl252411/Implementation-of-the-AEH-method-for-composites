
from odbAccess import *
from itertools import product
import numpy as np

#----------------------------- Parameters ------------------------------
#
satin_num = 2 # 2 for plain and 3 for twill
new_job_name = f'Job_woven{satin_num}_AEH3_cte'
new_job_name1 = f'Job_woven{satin_num}_AEH3_elastic'
if satin_num == 2:
    tmp_num, t_num, s_num = satin_num, 1, 4
else:
    tmp_num = satin_num + 1
    t_num, s_num = 1, 8
yarn_w, yarn_h, yarn_sec1, yarn_sec2, extra_t = 2.0, 0.6, 1.8, 0.4, 0.04   # 2.2 for twill, 2.29 for plain
rve_t = yarn_h + yarn_sec2 + extra_t/s_num
rve_size = np.array([tmp_num*yarn_w + extra_t, rve_t, tmp_num*yarn_w + extra_t])
savefile1 = f'Woven{satin_num}_Homogenized_Stiffness_AEH3.txt'
savefile2 = f'Woven{satin_num}_Homogenized_CTE1_AEH3.txt'

homo_stiff = np.loadtxt(savefile1, delimiter=",")
rve_volume = rve_size[0]*rve_size[1]*rve_size[2]
#
# ------------------------------ SAVE THE RESULTS -----------------------------
#
odb = openOdb(f'{new_job_name}_3.odb')
dtm = odb.rootAssembly.DatumCsysByThreePoints(name='CSYS-1', coordSysType=CARTESIAN, origin=(0.0, 0.0, 0.0),
    point1=(1.0, 0.0, 0.0), point2=(0.0, 1.0, 0.0))
Instance = odb.rootAssembly.instances['PART-1-1']
#
file_name = f'{new_job_name}_sec_nd_for.txt'
F1V = (odb.steps["Step-1"].frames[-1].fieldOutputs['RF'].getTransformedField(datumCsys=dtm)
       .getSubset(region=Instance, position=NODAL).values)
with open(file_name, 'w') as f:
    for value in F1V:
        line = ",".join([str(value.nodeLabel), format(value.data[0], ".12f"), format(value.data[1], ".12f"),
                         format(value.data[2], ".12f")])
        f.write(line + "\n")
odb.close()
#
#---------------------------------------------------------------------------------
#
IniU1   = np.loadtxt(f'{new_job_name1}_ini_nd_disp_1.txt', delimiter=',')
IniU2   = np.loadtxt(f'{new_job_name1}_ini_nd_disp_2.txt', delimiter=',')
IniU3   = np.loadtxt(f'{new_job_name1}_ini_nd_disp_3.txt', delimiter=',')
IniU4   = np.loadtxt(f'{new_job_name1}_ini_nd_disp_4.txt', delimiter=',')
IniU5   = np.loadtxt(f'{new_job_name1}_ini_nd_disp_5.txt', delimiter=',')
IniU6   = np.loadtxt(f'{new_job_name1}_ini_nd_disp_6.txt', delimiter=',')
IniRF   = np.loadtxt(f'{new_job_name}_ini_nd_for.txt', delimiter=',')
SecRF   = np.loadtxt(f'{new_job_name}_sec_nd_for.txt', delimiter=',')
#
homo_beta = np.zeros([6,1])
for i,k in product(range(3), range(len(SecRF))):
    homo_beta[0, 0] += IniU1[k, i + 1] * (IniRF[k, i + 1] - SecRF[k, i + 1]) / rve_volume
    homo_beta[1, 0] += IniU2[k, i + 1] * (IniRF[k, i + 1] - SecRF[k, i + 1]) / rve_volume
    homo_beta[2, 0] += IniU3[k, i + 1] * (IniRF[k, i + 1] - SecRF[k, i + 1]) / rve_volume
    homo_beta[3, 0] += IniU4[k, i + 1] * (IniRF[k, i + 1] - SecRF[k, i + 1]) / rve_volume
    homo_beta[4, 0] += IniU5[k, i + 1] * (IniRF[k, i + 1] - SecRF[k, i + 1]) / rve_volume
    homo_beta[5, 0] += IniU6[k, i + 1] * (IniRF[k, i + 1] - SecRF[k, i + 1]) / rve_volume
#
inv_stiff = np.linalg.inv(homo_stiff)
temp_alpha = np.dot(inv_stiff, homo_beta)
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
