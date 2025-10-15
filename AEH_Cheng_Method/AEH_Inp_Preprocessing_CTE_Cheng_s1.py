
from itertools import product
import numpy as np

#----------------------------- Parameters ------------------------------
#
satin_num = 3 # 2 for plain and 3 for twill
job_name = f'Job_woven{satin_num}_FEH_cte'
new_job_name = f'Job_woven{satin_num}_AEH3_cte'
if satin_num == 2:
    tmp_num, t_num, s_num = satin_num, 1, 4
else:
    tmp_num = satin_num + 1
    t_num, s_num = 1, 8
yarn_w, yarn_h, yarn_sec1, yarn_sec2, extra_t = 2.0, 0.6, 1.8, 0.4, 0.04   # 2.2 for twill, 2.29 for plain
rve_t = yarn_h + yarn_sec2 + extra_t/s_num
rve_size = np.array([tmp_num*yarn_w + extra_t, rve_t, tmp_num*yarn_w + extra_t])
xlenp, ylenp, zlenp = rve_size / 2.
xlenm, ylenm, zlenm = - rve_size / 2.

#----------------------------- Open the inp file ------------------------------
#
with open(f'{job_name}.inp', 'r') as f1:
	lines = f1.readlines()

#----------------------------- Modify Job name ------------------------------
#
lines[1] = '** Job name: Job-p2 Model name: Model-1\n'

#----------------------------- Node number and coordinates ------------------------------
#
line_str1, line_str2 = '*Node\n', '*Element, type=C3D4\n'
staid, endid = lines.index(line_str1), lines.index(line_str2)
ndnum = endid - staid - 1
#
ndcoords = np.zeros([ndnum,4])
for il in range(staid+1,endid):
	newline1 = lines[il].replace('\n', '').split(',')
	for inl in range(4):
		ndcoords[il-staid-1,inl] = float(newline1[inl])

#----------------------------- Creating node sets ------------------------------
#
addedlines1 = []
for inum in range(ndnum):
	addedlines1.append(f'*Nset, nset=Set-{inum+1}, instance=Part-1-1\n')
	addedlines1.append(f' {inum+1},\n')
#
staid1 = lines.index('*End Instance\n') + 2
lines = lines[0:staid1]+addedlines1+lines[staid1:]

#-----------------------------  ------------------------------
#
addedlines2 = []
addedlines2.append('** \n')
addedlines2.append('** PREDEFINED FIELDS\n')
addedlines2.append('** \n')
addedlines2.append('** Name: Predefined Field-1 Type: Temperature\n')
addedlines2.append('*Initial Conditions, type=TEMPERATURE \n')
addedlines2.append('Set-T, 0. \n')
addedlines2.append('** ----------------------------------------------------------------\n')
addedlines2.append('** \n')
addedlines2.append('** STEP: Step-1\n')
addedlines2.append('** \n')
addedlines2.append('*Step, name=Step-1\n')
addedlines2.append('*Static\n')
addedlines2.append('** \n')
addedlines2.append('** BOUNDARY CONDITIONS\n')
addedlines2.append('** \n')
#
for inum in range(ndnum):
	addedlines2.append(f'** Name: BC-{inum+1} Type: Displacement/Rotation\n')
	addedlines2.append('*Boundary\n')
	addedlines2.append(f'Set-{inum+1}, 1, 1\n')
	addedlines2.append(f'Set-{inum+1}, 2, 2\n')
	addedlines2.append(f'Set-{inum+1}, 3, 3\n')
	addedlines2.append(f'Set-{inum+1}, 4, 4\n')
	addedlines2.append(f'Set-{inum+1}, 5, 5\n')
	addedlines2.append(f'Set-{inum+1}, 6, 6\n')
#
np.savetxt(f'{new_job_name}_ini_nd_disp.txt', ndcoords, delimiter=',')
#
addedlines2.append('** \n')
addedlines2.append('** PREDEFINED FIELDS\n')
addedlines2.append('** \n')
addedlines2.append('** Name: Predefined Field-2 Type: Temperature\n')
addedlines2.append('*TEMPERATURE\n')
addedlines2.append('Set-T, -1.\n')
#
addedlines2.append('** \n')
addedlines2.append('** OUTPUT REQUESTS\n')
addedlines2.append('** \n')
addedlines2.append('** FIELD OUTPUT: F-Output-1\n')
addedlines2.append('** \n')
addedlines2.append('*Output, field\n')
addedlines2.append('*Node Output\n')
addedlines2.append('RF, U\n')
addedlines2.append('*Element Output, directions=YES\n')
addedlines2.append('E, EVOL, IVOL, S\n')
addedlines2.append('** \n')
addedlines2.append('** HISTORY OUTPUT: H-Output-1\n')
addedlines2.append('** \n')
addedlines2.append('*Output, history, variable=PRESELECT\n')
addedlines2.append('*End Step\n')

#----------------------------- Combine the file ------------------------------
#
staid1 = lines.index('** STEP: Step-1\n') - 2
lines = lines[0:staid1] + addedlines2

#----------------------------- Save the file ------------------------------
#
with open(f'{new_job_name}_1.inp', mode='w') as f:
	f.writelines(lines)