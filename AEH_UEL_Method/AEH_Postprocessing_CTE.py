import numpy as np
from itertools import product

#----------------------------- Parameters ------------------------------
#
satin_num = 3 # 2 for plain and 3 for twill
job_name = f'Job_woven{satin_num}_AEH1_cte'
savefile1 = f'Woven{satin_num}_Homogenized_Stiffness_AEH1.txt'
savefile2 = f'Woven{satin_num}_Homogenized_CTE_AEH1.txt'
homo_stiff = np.loadtxt(savefile1, delimiter=",")
#
with open(f'{job_name}_3.dat', 'r') as f1:
    lines = f1.readlines()
#
elenum = 1
for iline in lines:
    data = iline.split()
    if len(data) == 3 and float(data[0]) > elenum:
        elenum = float(data[0])
elenum = int(elenum)
#
strain = np.zeros((elenum, 6))
for i in range(0, len(lines), 3):
    data = lines[i+0].split()
    irow = int(data[0]) - 1
    strain[irow,0:2] = [float(data[1]), float(data[2])]
    data = lines[i+1].split()
    strain[irow,2:5] = [float(data[0]), float(data[1]), float(data[2])]
    data = lines[i+2].split()
    strain[irow,5] = float(data[0])
#
homo_beta = np.sum(strain, axis=0)
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
#
# ------------------------------ ------------------------------------------------
#
np.savetxt(savefile2, homo_alpha, delimiter=",")