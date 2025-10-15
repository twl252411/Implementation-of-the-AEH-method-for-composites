import numpy as np
from itertools import product

#----------------------------- Parameters ------------------------------
#
satin_num = 3 # 2 for plain and 3 for twill
job_name = f'Job_woven{satin_num}_AEH1_cte'

#----------------------------- Open the inp file ------------------------------
#
with open(f'{job_name}_2.dat', 'r') as f1:
	lines = f1.readlines()

#----------------------------- Operate the file ------------------------------
#
line_str = '     LINEAR EQUATION SOLVER TYPE         DIRECT SPARSE\n'
endid = lines.index(line_str)
del lines[0:endid+1]
#
line_str = '                   M E M O R Y   E S T I M A T E\n'
staid = lines.index(line_str) - 1
line_str = '      (6) USING "*RESTART, WRITE" CAN GENERATE A LARGE AMOUNT OF DATA WRITTEN IN THE WORK DIRECTORY.\n'
endid = lines.index(line_str)
del lines[staid:endid+1]
#
line_str = '          THE ANALYSIS HAS BEEN COMPLETED\n'
staid = lines.index(line_str) - 2
del lines[staid: ]

#----------------------------- Save the file ------------------------------
#
with open(f'{job_name}_3.dat', mode='w') as f:
	f.writelines(lines)