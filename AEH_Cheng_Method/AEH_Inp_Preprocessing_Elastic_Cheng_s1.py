#
import numpy as np
from itertools import product

#----------------------------- Parameters ------------------------------
#
satin_num = 3 # 2 for plain and 3 for twill
job_name = f'Job_woven{satin_num}_FEH_elastic'
new_job_name = f'Job_woven{satin_num}_AEH3_elastic'
if satin_num == 2:
    tmp_num, t_num, s_num = satin_num, 1, 4
else:
    tmp_num = satin_num + 1
    t_num, s_num = 1, 8
yarn_w, yarn_h, yarn_sec1, yarn_sec2, extra_t = 2.0, 0.6, 1.8, 0.4, 0.04  
rve_t = yarn_h + yarn_sec2 + extra_t/s_num
rve_size = np.array([tmp_num*yarn_w + extra_t, rve_t, tmp_num*yarn_w + extra_t])
pbc_disp = np.array([0.0, 0.0, 0.0])
xlenp, ylenp, zlenp = rve_size / 2.
xlenm, ylenm, zlenm = - rve_size / 2.

#----------------------------- Open the inp file ------------------------------
#
with open(f'{job_name}.inp', 'r') as f1:
	lines = f1.readlines()

#----------------------------- Modify Job name ------------------------------
#
lines[1] = '** Job name: Job Model name: Model-1\n'

#----------------------------- Node number and coordinates ------------------------------
#
staid = lines.index('*Node\n')
endid = lines.index('*Element, type=C3D4\n')
ndnum = endid - staid - 1
#
# ndcoords = np.zeros([ndnum,4])
# for il in range(staid+1,endid):
# 	newline1 = lines[il].replace('\n', '').split(',')
# 	for inl in range(4):
# 		ndcoords[il-staid-1,inl] = float(newline1[inl])
ndcoords = np.array([list(map(float, lines[i].replace('\n', '').split(',')))
	for i in range(staid + 1, endid)])

#----------------------------- Creating node sets ------------------------------
#
addedlines1 = [f'*Nset, nset=Set-{i + 1}, instance=Part-1-1\n {i + 1},\n'
	for i in range(ndnum)]
#
staid1 = lines.index('*End Instance\n') + 2
lines = lines[0:staid1]+addedlines1+lines[staid1:]

#------------------ Define step displacement patterns ------------
#
def get_displacement(step, coords):
	x, y, z = coords[1:]
	if step == 0:
		return x, 0., 0.
	elif step == 1:
		return 0., y, 0.
	elif step == 2:
		return 0., 0., z
	elif step == 3:
		return y / 2., x / 2., 0.
	elif step == 4:
		return z / 2., 0., x / 2.
	else:  # step == 5
		return 0., z / 2., y / 2.
addedlines2 = []

for istep in range(6):
	#
	addedlines2.extend([
		'** ----------------------------------------------------------------\n',
		'** \n',
		f'** STEP: Step-{istep + 1}\n',
		'** \n',
		f'*Step, name=Step-{istep + 1}, nlgeom=NO, perturbation\n',
		'*Static\n',
		'** \n',
		'** BOUNDARY CONDITIONS\n'
		'** \n'])

	#
	ini_nd_disp = np.zeros([ndnum,4])
	#
	for inum in range(ndnum):
		#
		xx, yy, zz = get_displacement(istep, ndcoords[inum])
		addedlines2.extend([
			f'** Name: BC-{istep + 1}-{inum + 1} Type: Displacement/Rotation\n',
			'*Boundary\n',
			f'Set-{inum + 1}, 1, 1, {xx}\n',
			f'Set-{inum + 1}, 2, 2, {yy}\n',
			f'Set-{inum + 1}, 3, 3, {zz}\n',
			f'Set-{inum + 1}, 4, 4\n',
			f'Set-{inum + 1}, 5, 5\n',
			f'Set-{inum + 1}, 6, 6\n'
		])
		ini_nd_disp[inum] = [inum + 1, xx, yy, zz]
	#
	np.savetxt(f'{new_job_name}_ini_nd_disp_{istep+1}.txt', ini_nd_disp, delimiter=',')
	#
	addedlines2.extend([
		'** \n',
		'** OUTPUT REQUESTS\n',
		'** \n',
		'** \n',
		'** FIELD OUTPUT: F-Output-1\n',
		'** \n',
		'*Output, field\n',
		'*Node Output\n',
		'RF, U\n',
		'*Element Output, directions=YES\n',
		'E, EVOL, IVOL, S\n',
		'** \n',
		'** HISTORY OUTPUT: H-Output-1\n',
		'** \n',
		'*Output, history, variable=PRESELECT\n',
		'*End Step\n'
	])

#----------------------------- Combine the file ------------------------------
#
staid1 = lines.index('** STEP: Step-1\n') - 2
lines = lines[0:staid1] + addedlines2

#----------------------------- Save the file ------------------------------
#
with open(f'{new_job_name}_1.inp', mode='w') as f:
	f.writelines(lines)