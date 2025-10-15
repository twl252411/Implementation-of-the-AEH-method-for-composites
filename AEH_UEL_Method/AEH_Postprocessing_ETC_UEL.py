
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
rve_volume = rve_size[0] * rve_size[1] * rve_size[2]
#

# ------------------------------ SAVE THE RESULTS -----------------------------
#
savefile = f'Woven{satin_num}_Homogenized_ETC_AEH1.txt'
homo_lambda = np.zeros([3, 3])
#
with open(f'{job_name}_3.dat','r') as f:
    lines = f.readlines()
#
# ----------------------------------------------------------------------------
#
line_str = '   STEP-2\n'
endid = lines.index(line_str)
tmplines = lines[0:endid]

elenum = 1
for iline in tmplines:
    data = iline.split()
    if len(data) == 3 and float(data[0]) > elenum:
        elenum = float(data[0])
#
heat_flux = np.zeros((int(elenum), 3))
for i in range(int(elenum)):
    data = lines[i*2].split()
    irow = int(data[0]) - 1
    heat_flux[irow,0:2] = [float(data[1]), float(data[2])]
    data = lines[i*2+1].split()
    heat_flux[irow,2] = float(data[0])
#
# ------------------------------ STEP-1 -----------------------------
#
line_str = '   STEP-2\n'
staid1 = lines.index(line_str)
heat_flux1 = heat_flux
#
for i in range(2*int(elenum), staid1, 2):
    data = lines[i].split()
    irow = int(data[0]) - 1
    heat_flux1[irow,0:2] = [float(data[1]), float(data[2])]
    data = lines[i+1].split()
    heat_flux1[irow, 2] = float(data[0])
#
homo_lambda[:,0] = np.divide(np.sum(heat_flux1, axis=0), rve_volume)
#
# ------------------------------ STEP-2 -----------------------------
#
line_str = '   STEP-3\n'
staid2 = lines.index(line_str)
heat_flux2 = heat_flux
#
for i in range(staid1+1,staid2,2):
    data = lines[i].split()
    irow = int(data[0]) - 1
    heat_flux2[irow,0:2] = [float(data[1]), float(data[2])]
    data = lines[i+1].split()
    heat_flux2[irow, 2] = float(data[0])
#
homo_lambda[:,1] = np.divide(np.sum(heat_flux2, axis=0), rve_volume)
#
# ------------------------------ STEP-3 -----------------------------
#
heat_flux3 = heat_flux
#
for i in range(staid2+1,len(lines),2):
    data = lines[i].split()
    irow = int(data[0]) - 1
    heat_flux3[irow,0:2] = [float(data[1]), float(data[2])]
    data = lines[i+1].split()
    heat_flux3[irow, 2] = float(data[0])
#
homo_lambda[:, 2] = np.divide(np.sum(heat_flux3, axis=0), rve_volume)
#
# ------------------------------ ------------------------------------------------

np.savetxt(savefile, homo_lambda, delimiter=",")