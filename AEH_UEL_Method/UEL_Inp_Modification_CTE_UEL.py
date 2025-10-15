import numpy as np
from itertools import product

# ----------------------------- Parameters ------------------------------
#
satin_num = 3 # 2 for plain and 3 for twill
job_name = f'Job_woven{satin_num}_AEH1_cte'
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
pbc_temp = np.array([0.0, 0.0, 0.0])
vrve = rve_size[0] * rve_size[1] * rve_size[2]

#----------------------------- Open the inp file ------------------------------
#
with open(f'{job_name}_1.inp', 'r') as f1:
	lines = f1.readlines()

#-----------------------Delete Materials---------------------------------------
#
for il in range(len(lines)):
	if lines[il] == '** \n' and lines[il+1] == '** MATERIALS\n':
		staid = il
		break
line_str = '** BOUNDARY CONDITIONS\n'
endid = lines.index(line_str)
del lines[staid:endid-1]
#
#-----------------------Modify element type -----------------------------------
#
for il in range(len(lines)):
	if lines[il] == '*Element, type=C3D4\n' and '1,' in lines[il+1]:
		staid = il
		break
del lines[staid:staid+1]
#
lines.insert(staid, '*User element, nodes=4, type=U5, properties=4, coordinates=3, variables=14\n')
lines.insert(staid+1, '1, 2, 3\n')
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
for im in range(1,4):
	elastic = np.loadtxt(f'woven_abaqus_elastic_stiff_{im-1}.txt', delimiter=',')
	alpha = np.loadtxt(f'woven_abaqus_alpha_{im-1}.txt', delimiter=',')
	#
	lines.insert(staid+0+(im-1)*7, f'** Section: Section-{im}\n')
	lines.insert(staid+1+(im-1)*7, f'*Uel property, elset=Set-M-{im}\n')
	lines.insert(staid+2+(im-1)*7, f'{elastic[0]}, {elastic[1]}, {elastic[2]}, {elastic[3]}, {elastic[4]}, {elastic[5]}, {elastic[6]}, {elastic[7]} \n')
	lines.insert(staid+3+(im-1)*7, f'{elastic[8]}, {elastic[9]}, {elastic[10]}, {elastic[11]}, {elastic[12]}, {elastic[13]}, {elastic[14]}, {elastic[15]} \n')
	lines.insert(staid+4+(im-1)*7, f'{elastic[16]}, {elastic[17]}, {elastic[18]}, {elastic[19]}, {elastic[20]}, {alpha[0]}, {alpha[1]}, {alpha[2]} \n')
	lines.insert(staid+5+(im-1)*7, f'{alpha[3]}, {alpha[4]}, {alpha[5]}, {vrve}\n')
	lines.insert(staid+6+(im-1)*7, '**27 parameters,Volume\n')

for il in range(len(lines)):
	if lines[il] == '*Orientation, name=Ori-1\n':
		staid = il
		break
line_str = '** Section: Section-1\n'
endid = lines.index(line_str)
del lines[staid:endid]
#
#-------------------- ------------------------
#
with open(f'{job_name}_2.inp', mode='w') as f:
	f.writelines(lines)
