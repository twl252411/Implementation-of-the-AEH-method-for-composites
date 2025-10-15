#
#
import numpy as np
from itertools import product

#----------------------------- Parameters ------------------------------
#
satin_num = 2 # 2 for plain and 3 for twill
job_name = f'Job_woven{satin_num}_AEH1_etc'

#----------------------------- Open the dat file ------------------------------
#
with open(f'{job_name}_2.dat', 'r') as f1:
	lines = f1.readlines()
#
#----------------------------- Operate the file ------------------------------
#
for il in range(len(lines)):
	if lines[il] == '1\n' and lines[il+1] == '\n':
		staid = il
		break
line_str = '          THE MAXIMUM TIME INCREMENT ALLOWED IS                 1.00    \n'
endid = lines.index(line_str)
del lines[staid:endid+1]
#
line_str = '                   M E M O R Y   E S T I M A T E\n'
staid = lines.index(line_str) - 1
line_str = '      (6) USING "*RESTART, WRITE" CAN GENERATE A LARGE AMOUNT OF DATA WRITTEN IN THE WORK DIRECTORY.\n'
endid = lines.index(line_str)
del lines[staid:endid+1]
#
#----------------------------- STEP-2 ------------------------------
#
line_str = '                                                                                               STEP    2  INCREMENT    1\n'
staid = lines.index(line_str) - 5
line_str = '          THE MAXIMUM TIME INCREMENT ALLOWED IS                 1.00    \n'
endid = lines.index(line_str)
del lines[staid:endid+1]
lines = lines[0:staid] + ['   STEP-2\n'] + lines[staid:]
#
line_str = '                   M E M O R Y   E S T I M A T E\n'
staid = lines.index(line_str) - 1
line_str = '      (6) USING "*RESTART, WRITE" CAN GENERATE A LARGE AMOUNT OF DATA WRITTEN IN THE WORK DIRECTORY.\n'
endid = lines.index(line_str)
del lines[staid:endid+1]
#
#----------------------------- STEP-3 ------------------------------
#
line_str = '                                                                                               STEP    3  INCREMENT    1\n'
staid = lines.index(line_str) - 5
line_str = '          THE MAXIMUM TIME INCREMENT ALLOWED IS                 1.00    \n'
endid = lines.index(line_str)
del lines[staid:endid+1]
lines = lines[0:staid] + ['   STEP-3\n'] + lines[staid:]
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
#
#----------------------------- Save the file ------------------------------
#
with open(f'{job_name}_3.dat', 'w') as f:
	f.writelines(lines)