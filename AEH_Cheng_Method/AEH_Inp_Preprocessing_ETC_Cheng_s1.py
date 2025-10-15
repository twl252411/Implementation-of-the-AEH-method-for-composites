#
import numpy as np
from itertools import product
#
#----------------------------- Open the inp file ------------------------------
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
xlenp, ylenp, zlenp = rve_size / 2.
xlenm, ylenm, zlenm = - rve_size / 2.
pbc_temp = rve_size

#
with open(f'{job_name}.inp', 'r') as f1:
	lines = f1.readlines()
#
#----------------------------- Modify Job name ------------------------------
#
lines[1] = f'** Job name: {job_name}_2 Model name: Model-1\n'
#
#----------------------------- Node number and coordinates ------------------------------
#
line_str1, line_str2 = '*Node\n', '*Element, type=DC3D4\n'
staid, endid = lines.index(line_str1), lines.index(line_str2)
ndnum = endid - staid - 1
#
ndcoords = np.array([list(map(float, lines[i].replace('\n', '').split(',')))
	for i in range(staid + 1, endid)])

#-Creating node sets ---
addlns1 = [f'*Nset, nset=Set-{i+1}, instance=Part-1-1\n {i+1},\n'
	for i in range(ndnum)]
#
staid1 = lines.index('*End Instance\n') + 2
lines = lines[0:staid1] + addlns1 + lines[staid1: ]

#--------------------------------------------------------------
#
addlns2, addlns3, addlns4, addlns5 = [], [], [], []
addlns2.append('** ----------------------------------------------------------------\n')
addlns2.append('** \n')
addlns2.append('** STEP: Step-1\n')
addlns2.append('** \n')
addlns2.append('*Step, name=Step-1, nlgeom=NO\n')
addlns2.append('*Heat Transfer, steady state, deltmx=0.\n')
addlns2.append('1., 1., 1e-05, 1.,\n')
addlns2.append('** \n')
addlns2.append('** BOUNDARY CONDITIONS\n')
addlns2.append('** \n')
#
for inum in range(ndnum):
	addlns3.append('** Name: BC-'+str(inum+1)+' Type: Temperature\n')
	addlns3.append('*Boundary\n')
	addlns3.append('Set-'+str(inum+1)+', 11, 11, '+str(ndcoords[inum,1])+'\n')
#
	addlns4.append('** Name: BC-'+str(inum+1)+' Type: Temperature\n')
	addlns4.append('*Boundary\n')
	addlns4.append('Set-'+str(inum+1)+', 11, 11, '+str(ndcoords[inum,2])+'\n')
#
	addlns5.append('** Name: BC-'+str(inum+1)+' Type: Temperature\n')
	addlns5.append('*Boundary\n')
	addlns5.append('Set-'+str(inum+1)+', 11, 11, '+str(ndcoords[inum,3])+'\n')
#
addlns6 = []
addlns6.append('** \n')
addlns6.append('** OUTPUT REQUESTS\n')
addlns6.append('** \n')
addlns6.append('*Restart, write, frequency=0\n')
addlns6.append('** \n')
addlns6.append('** FIELD OUTPUT: F-Output-1\n')
addlns6.append('** \n')
addlns6.append('*Output, field\n')
addlns6.append('*Node Output\n')
addlns6.append('COORD, NT, RFL\n')
addlns6.append('*Element Output, directions=YES\n')
addlns6.append('COORD\n')
addlns6.append('*Output, history\n')
addlns6.append('*End Step\n')
#
#-----------------------------Job-1------------------------------
#
staid1 = lines.index('** STEP: Step-1\n') - 2
lines_1 = lines[0:staid1] + addlns2 + addlns3 +addlns6
lines_2 = lines[0:staid1] + addlns2 + addlns4 +addlns6
lines_3 = lines[0:staid1] + addlns2 + addlns5 +addlns6
#
with open(f'{new_job_name}_11.inp', mode='w') as f:
	f.writelines(lines_1)
with open(f'{new_job_name}_12.inp', mode='w') as f:
	f.writelines(lines_2)
with open(f'{new_job_name}_13.inp', mode='w') as f:
	f.writelines(lines_3)
#
np.savetxt(f'{new_job_name}_ini_nd_t.txt', ndcoords, delimiter=',')