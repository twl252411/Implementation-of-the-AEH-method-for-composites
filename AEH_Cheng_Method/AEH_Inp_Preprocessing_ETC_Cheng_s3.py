#
#
import numpy as np
from itertools import product
#
#--------------------------------------------------------------------
#
satin_num = 3 # 2 for plain and 3 for twill
job_name = f'Job_woven{satin_num}_FEH_etc'
new_job_name = f'Job_woven{satin_num}_AEH3_etc'
if satin_num == 2:
    tmp_num, t_num, s_num = satin_num, 1, 4
else:
    tmp_num = satin_num + 1
    t_num, s_num = 1, 8
yarn_w, yarn_h, yarn_sec1, yarn_sec2, extra_t = 2.0, 0.6, 1.8, 0.4, 0.04   # 2.2 for twill, 2.29 for plain
rve_t = yarn_h + yarn_sec2 + extra_t/s_num
rve_size = np.array([tmp_num*yarn_w + extra_t, rve_t, tmp_num*yarn_w + extra_t])
pbc_temp = np.array([0.0, 0.0, 0.0])
xlenp, ylenp, zlenp = rve_size / 2.
xlenm, ylenm, zlenm = - rve_size / 2.

#----------------------------- Open the inp file ------------------------------
#
with open(f'{job_name}.inp', 'r') as f1:
	lines = f1.readlines()

#----------------------------- Modify Job name ------------------------------
#
lines[1] = '** Job name: Job-p4 Model name: Model-1\n'

#----------------------------- Node number and coordinates ------------------------------
#
line_str1, line_str2 = '*Node\n', '*Element, type=DC3D4\n'
staid, endid = lines.index(line_str1), lines.index(line_str2)
ndnum = endid - staid - 1
#
ndcoords = np.array([list(map(float, lines[i].replace('\n', '').split(',')))
	for i in range(staid + 1, endid)])
#-Creating node sets ---
addedlines1 = [f'*Nset, nset=Set-{i + 1}, instance=Part-1-1\n {i + 1},\n'
	for i in range(ndnum)]
#
staid1 = lines.index('*End Instance\n') + 2
lines = lines[0:staid1]+addedlines1+lines[staid1:]

#--------------------------------------------------------------
#
input_t = np.loadtxt(f'{new_job_name}_sec_nd_t.txt', delimiter=',')
#
addedlines2 = []
addedlines2.append('** ----------------------------------------------------------------\n')
addedlines2.append('** \n')
addedlines2.append('** STEP: Step-1\n')
addedlines2.append('** \n')
addedlines2.append('*Step, name=Step-1, nlgeom=NO\n')
addedlines2.append('*Heat Transfer, steady state, deltmx=0.\n')
addedlines2.append('1., 1., 1e-05, 1.,\n')
addedlines2.append('** \n')
addedlines2.append('** BOUNDARY CONDITIONS\n')
addedlines2.append('** \n')
#
for inum in range(ndnum):
	addedlines2.append('** Name: BC-'+str(inum+1)+' Type: Temperature\n')
	addedlines2.append('*Boundary\n')
	addedlines2.append('Set-'+str(inum+1)+', 11, 11, '+str(input_t[inum,1])+'\n')
#
addedlines3 = []
addedlines3.append('** ----------------------------------------------------------------\n')
addedlines3.append('** \n')
addedlines3.append('** STEP: Step-2\n')
addedlines3.append('** \n')
addedlines3.append('*Step, name=Step-2, nlgeom=NO\n')
addedlines3.append('*Heat Transfer, steady state, deltmx=0.\n')
addedlines3.append('1., 1., 1e-05, 1.,\n')
addedlines3.append('** \n')
addedlines3.append('** BOUNDARY CONDITIONS\n')
addedlines3.append('** \n')
#
for inum in range(ndnum):
	addedlines3.append('** Name: BC-'+str(inum+1)+' Type: Temperature\n')
	addedlines3.append('*Boundary\n')
	addedlines3.append('Set-'+str(inum+1)+', 11, 11, '+str(input_t[inum,2])+'\n')
#
addedlines4 = []
addedlines4.append('** ----------------------------------------------------------------\n')
addedlines4.append('** \n')
addedlines4.append('** STEP: Step-3\n')
addedlines4.append('** \n')
addedlines4.append('*Step, name=Step-3, nlgeom=NO\n')
addedlines4.append('*Heat Transfer, steady state, deltmx=0.\n')
addedlines4.append('1., 1., 1e-05, 1.,\n')
addedlines4.append('** \n')
addedlines4.append('** BOUNDARY CONDITIONS\n')
addedlines4.append('** \n')
#
for inum in range(ndnum):
	addedlines4.append('** Name: BC-'+str(inum+1)+' Type: Temperature\n')
	addedlines4.append('*Boundary\n')
	addedlines4.append('Set-'+str(inum+1)+', 11, 11, '+str(input_t[inum,3])+'\n')
#
addedlines5 = []
addedlines5.append('** \n')
addedlines5.append('** OUTPUT REQUESTS\n')
addedlines5.append('** \n')
addedlines5.append('*Restart, write, frequency=0\n')
addedlines5.append('** \n')
addedlines5.append('** FIELD OUTPUT: F-Output-1\n')
addedlines5.append('** \n')
addedlines5.append('*Output, field\n')
addedlines5.append('*Node Output\n')
addedlines5.append('COORD, NT, RFL\n')
addedlines5.append('*Element Output, directions=YES\n')
addedlines5.append('COORD\n')
addedlines5.append('*Output, history\n')
addedlines5.append('*End Step\n')
#
#-----------------------------Job-1------------------------------
#
staid1 = lines.index('** STEP: Step-1\n') - 2
lines_1 = lines[0:staid1] + addedlines2 + addedlines5
lines_2 = lines[0:staid1] + addedlines3 + addedlines5
lines_3 = lines[0:staid1] + addedlines4 + addedlines5
#
with open(f'{new_job_name}_31.inp', mode='w') as f:
	f.writelines(lines_1)
with open(f'{new_job_name}_32.inp', mode='w') as f:
	f.writelines(lines_2)
with open(f'{new_job_name}_33.inp', mode='w') as f:
	f.writelines(lines_3)
#