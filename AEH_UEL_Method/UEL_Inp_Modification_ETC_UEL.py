#
#
import numpy as np
from itertools import product

#----------------------------- Parameters ------------------------------
#
satin_num = 3 # 2 for plain and 3 for twill
job_name = f'Job_woven{satin_num}_AEH1_etc'
if satin_num == 2:
    tmp_num, t_num, s_num = satin_num, 1, 4
else:
    tmp_num = satin_num + 1
    t_num, s_num = 1, 8
yarn_w, yarn_h, yarn_sec1, yarn_sec2, extra_t = 2.0, 0.6, 1.8, 0.4, 0.04   # 2.2 for twill, 2.29 for plain
rve_t = yarn_h + yarn_sec2 + extra_t/s_num
rve_size = np.array([tmp_num*yarn_w + extra_t, rve_t, tmp_num*yarn_w + extra_t])
vrve = rve_size[0] * rve_size[1] * rve_size[2]
#
with open(f'{job_name}_1.inp', 'r') as f1:
	lines = f1.readlines()
#
#-----------------------Delete Materials---------------------------------------
#
for il in range(len(lines)):
	if lines[il] == '** \n' and lines[il+1] == '** MATERIALS\n':
		staid = il
		break
line_str = '** STEP: Step-1\n'
endid = lines.index(line_str)
del lines[staid+1:endid-2]
#
#-----------------------Modify element type -----------------------------------
#
for il in range(len(lines)):
	if lines[il] == '*Element, type=DC3D4\n' and '1,' in lines[il+1]:
		staid = il
		break
del lines[staid:staid+1]
#
lines.insert(staid, '*User element, nodes=4, type=U5, properties=4, coordinates=3, variables=11\n')
lines.insert(staid+1, '11\n')
lines.insert(staid+2, '*Element, type=U5\n')
#
#--------------------Modified sections and materials------------------------
#
for il in range(len(lines)):
	if lines[il] == '** Section: Section-1\n':
		staid = il
		break
line_str = '*End Instance\n'
endid = lines.index(line_str)
del lines[staid:endid]
#
for im in range(1, 4):
	kappa = np.loadtxt(f'woven_abaqus_kappa_{im-1}.txt', delimiter=',')
	section_lines = [
		f'** Section: Section-{im}\n',
		f'*Uel property, elset=Set-M-{im}\n',
		', '.join(map(str, kappa[0:6])) + f', {vrve}\n',
		'**E,nu,Volume\n']
	lines[staid + (im - 1) * 4:staid + (im - 1) * 4] = section_lines

for il in range(len(lines)):
	if lines[il] == '*Orientation, name=Ori-1\n':
		staid = il
		break
line_str = '** Section: Section-1\n'
endid = lines.index(line_str)
del lines[staid:endid]
#-------------------- ------------------------
#
with open(f'{job_name}_2.inp', mode='w') as f:
	f.writelines(lines)
