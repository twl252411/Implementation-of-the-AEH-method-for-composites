
from odbAccess import *
from itertools import product
import numpy as np

#----------------------------- Parameters ------------------------------
#
satin_num = 3 # 2 for plain and 3 for twill
new_job_name = f'Job_woven{satin_num}_AEH3_cte'

odb = openOdb(f'{new_job_name}_1.odb')
Instance = odb.rootAssembly.instances['PART-1-1']
dtm = odb.rootAssembly.DatumCsysByThreePoints(name='CSYS-1', coordSysType=CARTESIAN, origin=(0.0, 0.0, 0.0),
    point1=(1.0, 0.0, 0.0), point2=(0.0, 1.0, 0.0))

file_name = f"{new_job_name}_ini_nd_for.txt"
F1V = (odb.steps["Step-1"].frames[-1].fieldOutputs['RF'].getTransformedField(datumCsys=dtm)
       .getSubset(region=Instance, position=NODAL).values)
with open(file_name, 'w') as f:
    for value in F1V:
        line = ",".join([str(value.nodeLabel), format(value.data[0], ".12f"), format(value.data[1], ".12f"),
                         format(value.data[2], ".12f")])
        f.write(line + "\n")
odb.close()


