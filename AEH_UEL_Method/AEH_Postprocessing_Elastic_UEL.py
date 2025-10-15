
import numpy as np
from itertools import product

#----------------------------- Parameters ------------------------------
#
satin_num = 2  # 2 for plain and 3 for twill
job_name = f'Job_woven{satin_num}_AEH1_elastic'
savefile = f'Woven{satin_num}_Homogenized_Stiffness_AEH1.txt'
#
data = np.loadtxt(f'{job_name}_3.dat')
[row, col] = data.shape
estran, homo_stiff = np.zeros([int(row/2), 6]), np.zeros([6, 6])
#
for i in range(int(row/2)):
    estran[i,0:3], estran[i,3:6] = data[i*2+0,0:3], data[i*2+1,0:3]
#
[row1, col1] = estran.shape
for i, j, k in product(range(6), range(6), range(int(row1/6))):
    homo_stiff[j, i] += estran[i*int(row1/6)+k, j]
np.savetxt(savefile, homo_stiff, delimiter=",")