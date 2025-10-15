
from odbAccess import *
import numpy as np
from itertools import product
#
#
#----------------------------- Open the inp file ------------------------------
#
satin_num = 3 # 2 for plain and 3 for twill
new_job_name = f'Job_woven{satin_num}_AEH3_etc'

ini_nd_t = np.loadtxt(f'{new_job_name}_ini_nd_t.txt', delimiter=',')
sec_nd_t = np.zeros_like(ini_nd_t)
#
for iob in range(3):
    #
    odb = openOdb(f'{new_job_name}_2{iob+1}.odb')
    Instance = odb.rootAssembly.instances['PART-1-1']
    #
    F1V = odb.steps[f'Step-{iob+1}'].frames[-1].fieldOutputs['NT11'].getSubset(region=Instance, position=NODAL).values
    for iv in range(len(F1V)):
        sec_nd_t[F1V[iv].nodeLabel-1, 0] = F1V[iv].nodeLabel
        sec_nd_t[F1V[iv].nodeLabel-1, iob+1] = F1V[iv].data
    odb.close()
#
np.savetxt(f'{new_job_name}_sec_nd_t.txt', sec_nd_t, delimiter=',')


