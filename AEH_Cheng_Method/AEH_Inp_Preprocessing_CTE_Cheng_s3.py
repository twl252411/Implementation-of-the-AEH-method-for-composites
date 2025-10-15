#
from itertools import product
import numpy as np

# ------------------------------------------------------------------------------------
#
satin_num = 2 # 2 for plain and 3 for twill
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

# ----------------------------- Open the inp file ------------------------------
#
with open(f'{job_name}.inp', 'r') as f1:
	lines = f1.readlines()

#----------------------------- Modify Job name ------------------------------
#
lines[1] = f'** Job name: {new_job_name} Model name: Model-1\n'


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

#-----------------------------Boundary conditions------------------------------
#
InputU = np.loadtxt(f'{new_job_name}_sec_nd_disp.txt', delimiter=',')
#
addedlines = []
addedlines.append('** ----------------------------------------------------------------\n')
addedlines.append('** \n')
addedlines.append('** STEP: Step-1\n')
addedlines.append('** \n')
addedlines.append('*Step, name=Step-1\n')
addedlines.append('*Static\n')
addedlines.append('** \n')
addedlines.append('** BOUNDARY CONDITIONS\n')
addedlines.append('** \n')
#
for inum in range(ndnum):
	addedlines.append('** Name: BC-'+str(inum+1)+' Type: Displacement/Rotation\n')
	addedlines.append('*Boundary\n')
	addedlines.append('Set-'+str(inum+1)+', 1, 1, '+str(InputU[inum,1])+'\n')
	addedlines.append('Set-'+str(inum+1)+', 2, 2, '+str(InputU[inum,2])+'\n')
	addedlines.append('Set-'+str(inum+1)+', 3, 3, '+str(InputU[inum,3])+'\n')
	addedlines.append('Set-'+str(inum+1)+', 4, 4\n')
	addedlines.append('Set-'+str(inum+1)+', 5, 5\n')
	addedlines.append('Set-'+str(inum+1)+', 6, 6\n')
#
addedlines.append('** \n')
addedlines.append('** OUTPUT REQUESTS\n')
addedlines.append('** \n')
addedlines.append('** FIELD OUTPUT: F-Output-1\n')
addedlines.append('** \n')
addedlines.append('*Output, field\n')
addedlines.append('*Node Output\n')
addedlines.append('RF, U\n')
addedlines.append('*Element Output, directions=YES\n')
addedlines.append('E, EVOL, IVOL, S\n')
addedlines.append('** \n')
addedlines.append('** HISTORY OUTPUT: H-Output-1\n')
addedlines.append('** \n')
addedlines.append('*Output, history, variable=PRESELECT\n')
addedlines.append('*End Step\n')

#----------------------------- Combine the file ------------------------------
#
staid1 = lines.index('** STEP: Step-1\n') - 2
lines = lines[0:staid1] + addedlines

#----------------------------- Save the file ------------------------------
#
with open(f'{new_job_name}_3.inp', mode='w') as f:
	f.writelines(lines)