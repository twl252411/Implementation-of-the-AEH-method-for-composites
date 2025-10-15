from abaqus import *
from abaqusConstants import *
from caeModules import *
from driverUtils import executeOnCaeStartup
from itertools import product
import numpy as np
import os
import mesh
import periodic_meshes as pm
import regionToolset

#
executeOnCaeStartup()
Mdb()

#--------------------------------------------------------------------------------------
#
composite_type, analysis_type = "woven", "elastic"
#
satin_num = 3 # 2 for plain and 3 for twill
job_name = f'Job_woven{satin_num}_AEH2_{analysis_type}'
cae_name = f'woven{satin_num}_composites_fem_rve.cae'
if satin_num == 2:
    tmp_num, t_num, s_num = satin_num, 1, 4
else:
    tmp_num = satin_num + 1
    t_num, s_num = 1, 8
yarn_w, yarn_h, yarn_sec1, yarn_sec2, extra_t = 2.0, 0.6, 1.8, 0.4, 0.04   # 2.2 for twill, 2.29 for plain
rve_t = yarn_h + yarn_sec2 + extra_t/s_num
rve_size = np.array([tmp_num*yarn_w + extra_t, t_num*rve_t, tmp_num*yarn_w + extra_t])
mesh_size = rve_size[0] / 75.0
phase_num = 3
#
xlenp, ylenp, zlenp = rve_size / 2.
xlenm, ylenm, zlenm = - rve_size / 2.


#--------------------------------------------------------------------------------------
#
base_name, ext = os.path.splitext(cae_name)
path_name = f'{base_name}_FEH.cae'
openMdb(pathName=cae_name)
#
if composite_type == "sphere":
    mdb.models['Model-1'].Material(name='Material-1')
    mdb.models['Model-1'].materials['Material-1'].Elastic(table=((0.074, 0.33),))
    mdb.models['Model-1'].materials['Material-1'].Expansion(table=((2.5E-5,),))
    mdb.models['Model-1'].materials['Material-1'].Conductivity(table=((173.,),))
    mdb.models['Model-1'].HomogeneousSolidSection(name='Section-1', material='Material-1', thickness=None)
    #
    mdb.models['Model-1'].Material(name='Material-2')
    mdb.models['Model-1'].materials['Material-2'].Elastic(table=((0.410, 0.19),))
    mdb.models['Model-1'].materials['Material-2'].Expansion(table=((4.3E-6,),))
    mdb.models['Model-1'].materials['Material-2'].Conductivity(table=((393.,),))
    mdb.models['Model-1'].HomogeneousSolidSection(name='Section-2', material='Material-2', thickness=None)
#
elif composite_type == "fiber":
    mdb.models['Model-1'].Material(name='Material-1')
    mdb.models['Model-1'].materials['Material-1'].Elastic(table=((0.00342, 0.4), ))
    mdb.models['Model-1'].materials['Material-1'].Expansion(table=((8.0E-5, ), ))
    mdb.models['Model-1'].materials['Material-1'].Conductivity(table=((0.363, ), ))
    mdb.models['Model-1'].HomogeneousSolidSection(name='Section-1', material='Material-1', thickness=None)
    #
    mdb.models['Model-1'].Material(name='Material-2')
    mdb.models['Model-1'].materials['Material-2'].Elastic(table=((0.073, 0.2), ))
    mdb.models['Model-1'].materials['Material-2'].Expansion(table=((5.4E-5, ), ))
    mdb.models['Model-1'].materials['Material-2'].Conductivity(table=((1.3, ), ))
    mdb.models['Model-1'].HomogeneousSolidSection(name='Section-2', material='Material-2', thickness=None)
#
elif composite_type == "braided":
    for im in range(phase_num):
        elastic = tuple(np.loadtxt(f'braided{phase_num-1}_abaqus_elastic_stiff_{im}.txt', delimiter=','))
        alpha = tuple(np.loadtxt(f'braided{phase_num-1}_abaqus_alpha_{im}.txt', delimiter=','))
        kappa = tuple(np.loadtxt(f'braided{phase_num-1}_abaqus_kappa_{im}.txt', delimiter=','))
        mdb.models['Model-1'].Material(name=f'Material-{im+1}')
        mdb.models['Model-1'].materials[f'Material-{im+1}'].Elastic(type=ANISOTROPIC, table=(elastic, ))
        mdb.models['Model-1'].materials[f'Material-{im+1}'].Expansion(type=ANISOTROPIC, table=(alpha, ))
        # mdb.models['Model-1'].materials[f'Material-{im+1}'].Expansion(type=ANISOTROPIC, userSubroutine=ON)
        mdb.models['Model-1'].materials[f'Material-{im+1}'].Conductivity(type=ANISOTROPIC, table=(kappa, ))
else:
    for im in range(phase_num):
        elastic = tuple(np.loadtxt(f'woven_abaqus_elastic_stiff_{im}.txt', delimiter=','))
        alpha = tuple(np.loadtxt(f'woven_abaqus_alpha_{im}.txt', delimiter=','))
        kappa = tuple(np.loadtxt(f'woven_abaqus_kappa_{im}.txt', delimiter=','))
        mdb.models['Model-1'].Material(name=f'Material-{im+1}')
        mdb.models['Model-1'].materials[f'Material-{im+1}'].Elastic(type=ANISOTROPIC, table=(elastic, ))
        mdb.models['Model-1'].materials[f'Material-{im+1}'].Expansion(type=ANISOTROPIC, table=(alpha, ))
        # mdb.models['Model-1'].materials[f'Material-{im+1}'].Expansion(type=ANISOTROPIC, userSubroutine=ON)
        mdb.models['Model-1'].materials[f'Material-{im+1}'].Conductivity(type=ANISOTROPIC, table=(kappa, ))

#------------------------------------------------------------------------------------
#
p = mdb.models['Model-1'].parts['Part-1']
print(composite_type)
for inum in range(phase_num):
    region, section_name = p.sets[f'Set-M-{inum + 1}'], f'Section-{inum + 1}'
    mdb.models['Model-1'].HomogeneousSolidSection(name=section_name, material=f'Material-{inum + 1}', thickness=None)
    p.SectionAssignment(region=region, sectionName=section_name, offset=0.0, offsetType=MIDDLE_SURFACE, offsetField='',
        thicknessAssignment=FROM_SECTION)
#
region = regionToolset.Region(cells=p.cells)
p.MaterialOrientation(region=region, orientationType=GLOBAL, axis=AXIS_1, additionalRotationType=ROTATION_NONE,
    localCsys=None, fieldName='', stackDirection=STACK_3)

#--------------------------------------------------------------------------------------
#
if analysis_type == "elastic":
    mdb.models['Model-1'].StaticLinearPerturbationStep(name='Step-1', previous='Initial')
    mdb.models['Model-1'].StaticLinearPerturbationStep(name='Step-2', previous='Step-1')
    mdb.models['Model-1'].StaticLinearPerturbationStep(name='Step-3', previous='Step-2')
    mdb.models['Model-1'].StaticLinearPerturbationStep(name='Step-4', previous='Step-3')
    mdb.models['Model-1'].StaticLinearPerturbationStep(name='Step-5', previous='Step-4')
    mdb.models['Model-1'].StaticLinearPerturbationStep(name='Step-6', previous='Step-5')
    mdb.models['Model-1'].FieldOutputRequest(name='F-Output-1', createStepName='Step-1', variables=('S', 'E', 'U',
        'RF', 'EVOL', 'IVOL',), frequency=LAST_INCREMENT, position=INTEGRATION_POINTS)
    a = mdb.models['Model-1'].rootAssembly
    cell = a.instances['Part-1-1'].cells
    a.Set(cells=cell, name='Set-T')
elif analysis_type == "cte":
    mdb.models['Model-1'].StaticStep(name='Step-1', previous='Initial')
    mdb.models['Model-1'].FieldOutputRequest(name='F-Output-1', createStepName='Step-1', variables=('S', 'E', 'U',
        'RF', 'EVOL', 'IVOL', ), frequency=LAST_INCREMENT, position=INTEGRATION_POINTS)
    a = mdb.models['Model-1'].rootAssembly
    cell = a.instances['Part-1-1'].cells
    a.Set(cells=cell, name='Set-T')
else:
    mdb.models['Model-1'].HeatTransferStep(name='Step-1', previous='Initial', response=STEADY_STATE, amplitude=RAMP)
    mdb.models['Model-1'].FieldOutputRequest(name='F-Output-1', createStepName='Step-1', variables=('NT', 'HFL',
        'EVOL', 'IVOL', 'RFL',), frequency=LAST_INCREMENT, position=INTEGRATION_POINTS)

#--------------------------------------------------------------------------------------
#
a = mdb.models['Model-1'].rootAssembly
a.seedPartInstance(regions=(a.instances['Part-1-1'], ), size=mesh_size, deviationFactor=0.1, minSizeFactor=0.1)
a.setMeshControls(regions=a.instances['Part-1-1'].cells, elemShape=TET, technique=FREE)
if analysis_type == "etc":
    elemType1 = mesh.ElemType(elemCode=DC3D8, elemLibrary=STANDARD)
    elemType2 = mesh.ElemType(elemCode=DC3D6, elemLibrary=STANDARD)
    elemType3 = mesh.ElemType(elemCode=DC3D4, elemLibrary=STANDARD, secondOrderAccuracy=OFF, distortionControl=DEFAULT)
else:
    elemType1 = mesh.ElemType(elemCode=C3D8, elemLibrary=STANDARD)
    elemType2 = mesh.ElemType(elemCode=C3D6, elemLibrary=STANDARD)
    elemType3 = mesh.ElemType(elemCode=C3D4, elemLibrary=STANDARD, secondOrderAccuracy=OFF, distortionControl=DEFAULT)
a.setElementType(regions=(a.instances['Part-1-1'].cells, ), elemTypes=(elemType1, elemType2, elemType3))
a.generateMesh(regions=(a.instances['Part-1-1'], ))

#---------------------------------------------------------------------------------
#
mdb.Job(name=job_name, model='Model-1', description='', type=ANALYSIS, atTime=None, waitMinutes=0, waitHours=0,
    queue=None, memory=90, memoryUnits=PERCENTAGE, getMemoryFromAnalysis=True, explicitPrecision=SINGLE,
    nodalOutputPrecision=SINGLE, echoPrint=OFF, modelPrint=OFF, contactPrint=OFF, historyPrint=OFF,
    userSubroutine='', scratch='', resultsFormat=ODB, multiprocessingMode=DEFAULT, numCpus=1, numGPUs=0)
mdb.jobs[job_name].writeInput(consistencyChecking=OFF)
#
mdb.saveAs(pathName=path_name)