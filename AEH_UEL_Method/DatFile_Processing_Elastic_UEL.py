import numpy as np
from itertools import product

#----------------------------- Parameters ------------------------------
#
satin_num = 2 # 2 for plain and 3 for twill
job_name = f'Job_woven{satin_num}_AEH1_elastic'

#----------------------------- Open the dat file ------------------------------
#
with open(f'{job_name}_2.dat','r') as f1:
	lines = f1.readlines()
#
staid, endid = [], [len(lines)]
for il in range(len(lines)-1, -1, -1):
	if lines[il] == '\n' and lines[il+1] == '\n' and lines[il+2] == '          THE ANALYSIS HAS BEEN COMPLETED\n':
		staid.append(il)
		break
#
for il in range(len(lines)-1, -1, -1):
	if lines[il] == '1\n' and lines[il+1] == '\n':
		staid.append(il)
	if lines[il] == '      (6) USING "*RESTART, WRITE" CAN GENERATE A LARGE AMOUNT OF DATA WRITTEN IN THE WORK DIRECTORY.\n':
		endid.append(il+1)
#
staid = staid[0:6] + staid[7:]
#
for i in range(len(staid)):
	del lines[staid[i]:endid[i]]

#----------------------------- Save the file ------------------------------
#
with open(f'{job_name}_3.dat', mode='w') as f:
	f.writelines(lines)