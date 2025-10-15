from abaqus import *
from abaqusConstants import *
from driverUtils import executeOnCaeStartup
import numpy as np
import os
#
executeOnCaeStartup()
Mdb()

#---------------------------------------------------------------------------
#
filename = f'points3d_particle.txt'
base_name, ext = os.path.splitext(filename)
cae_name = f'sphere_particle.cae'
pts = np.loadtxt(filename, delimiter=' ')
rve_size, layer_t, inc_rad = 100.0, 0.2, 10.0

#---------------------------------------------------------------------------
#
s = mdb.models['Model-1'].ConstrainedSketch(name='__profile__', sheetSize=200.0)
g, v, d, c = s.geometry, s.vertices, s.dimensions, s.constraints
s.setPrimaryObject(option=STANDALONE)
s.ConstructionLine(point1=(0.0, -100.0), point2=(0.0, 100.0))
s.ArcByCenterEnds(center=(0.0, 0.0), point1=(0.0, inc_rad), point2=(0.0, -inc_rad), direction=CLOCKWISE)
s.Line(point1=(0.0, -inc_rad), point2=(0.0, inc_rad))
p = mdb.models['Model-1'].Part(name='Part-1', dimensionality=THREE_D, type=DEFORMABLE_BODY)
p.BaseSolidRevolve(sketch=s, angle=360.0, flipRevolveDirection=OFF)
s.unsetPrimaryObject()
del mdb.models['Model-1'].sketches['__profile__']

#---------------------------------------------------------------------------
#
a = mdb.models['Model-1'].rootAssembly
p = mdb.models['Model-1'].parts['Part-1']
ins_lists = ()
for i in range(len(pts)):
    a.Instance(name=f'Part-1-{i+1}', part=p, dependent=OFF)
    a.translate(instanceList=(f'Part-1-{i+1}', ), vector=(pts[i][0], pts[i][1], pts[i][2]))
    ins_lists += (a.instances[f'Part-1-{i+1}'], )
a.InstanceFromBooleanMerge(name='Part-New', instances=ins_lists, keepIntersections=ON, originalInstances=DELETE, domain=GEOMETRY)
a.deleteFeatures(('Part-New-1',))
mdb.models['Model-1'].parts.changeKey(fromName='Part-New', toName='Part-2')
del mdb.models['Model-1'].parts['Part-1']
#
p = mdb.models['Model-1'].parts['Part-2']
a.Instance(name='Part-2-1', part=p, dependent=OFF)
a.Instance(name='Part-2-2', part=p, dependent=OFF)

#---------------------------------------------------------------------------
#
s = mdb.models['Model-1'].ConstrainedSketch(name='__profile__', sheetSize=200.0)
g, v, d, c = s.geometry, s.vertices, s.dimensions, s.constraints
s.setPrimaryObject(option=STANDALONE)
s.rectangle(point1=(0.0, 0.0), point2=(rve_size, rve_size))
p = mdb.models['Model-1'].Part(name='Part-1', dimensionality=THREE_D, type=DEFORMABLE_BODY)
p.BaseSolidExtrude(sketch=s, depth=rve_size)
s.unsetPrimaryObject()
del mdb.models['Model-1'].sketches['__profile__']
#
a = mdb.models['Model-1'].rootAssembly
p = mdb.models['Model-1'].parts['Part-1']
a.Instance(name='Part-1-1', part=p, dependent=OFF)

#---------------------------------------------------------------------------
#
a = mdb.models['Model-1'].rootAssembly
a.InstanceFromBooleanCut(name='Part-3',instanceToBeCut=mdb.models['Model-1'].rootAssembly.instances['Part-2-1'],
    cuttingInstances=(a.instances['Part-1-1'], ), originalInstances=DELETE)
a.InstanceFromBooleanCut(name='Part-4', instanceToBeCut=mdb.models['Model-1'].rootAssembly.instances['Part-2-2'],
    cuttingInstances=(a.instances['Part-3-1'], ), originalInstances=DELETE)
del mdb.models['Model-1'].parts['Part-1']
del mdb.models['Model-1'].parts['Part-2']
del mdb.models['Model-1'].parts['Part-3']
a.deleteFeatures(('Part-4-1',))
mdb.models['Model-1'].parts.changeKey(fromName='Part-4', toName='Part-2')
p = mdb.models['Model-1'].parts['Part-2']
a.Instance(name='Part-2-1', part=p, dependent=OFF)
a.translate(instanceList=('Part-2-1', ), vector=(layer_t/2.0, layer_t/2.0, layer_t/2.0))

#---------------------------------------------------------------------------
#
s = mdb.models['Model-1'].ConstrainedSketch(name='__profile__', sheetSize=200.0)
g, v, d, c = s.geometry, s.vertices, s.dimensions, s.constraints
s.setPrimaryObject(option=STANDALONE)
s.rectangle(point1=(0.0, 0.0), point2=(rve_size+layer_t, rve_size+layer_t))
p = mdb.models['Model-1'].Part(name='Part-1', dimensionality=THREE_D, type=DEFORMABLE_BODY)
p.BaseSolidExtrude(sketch=s, depth=rve_size+layer_t)
s.unsetPrimaryObject()
del mdb.models['Model-1'].sketches['__profile__']
#
a = mdb.models['Model-1'].rootAssembly
p = mdb.models['Model-1'].parts['Part-1']
a.Instance(name='Part-1-1', part=p, dependent=OFF)

#---------------------------------------------------------------------------
#
a = mdb.models['Model-1'].rootAssembly
a.InstanceFromBooleanCut(name='Part-3', instanceToBeCut=mdb.models['Model-1'].rootAssembly.instances['Part-1-1'],
    cuttingInstances=(a.instances['Part-2-1'], ), originalInstances=DELETE)
del mdb.models['Model-1'].parts['Part-1']
a.deleteFeatures(('Part-3-1',))
mdb.models['Model-1'].parts.changeKey(fromName='Part-3', toName='Part-1')

#---------------------------------------------------------------------------
#
a = mdb.models['Model-1'].rootAssembly
p = mdb.models['Model-1'].parts['Part-1']
a.Instance(name='Part-1-1', part=p, dependent=OFF)
a.translate(instanceList=('Part-1-1', ), vector=(-(rve_size+layer_t)/2.0, -(rve_size+layer_t)/2.0, -(rve_size+layer_t)/2.0))
p = mdb.models['Model-1'].parts['Part-2']
a.Instance(name='Part-2-1', part=p, dependent=OFF)
a.translate(instanceList=('Part-2-1', ), vector=(-rve_size/2.0, -rve_size/2.0, -rve_size/2.0))

#---------------------------------------------------------------------------
#
a = mdb.models['Model-1'].rootAssembly
a.InstanceFromBooleanMerge(name='Part-New', instances=(a.instances['Part-1-1'], a.instances['Part-2-1'], ),
    keepIntersections=ON, originalInstances=DELETE, domain=GEOMETRY)
a.deleteFeatures(('Part-New-1',))
del mdb.models['Model-1'].parts['Part-1']
del mdb.models['Model-1'].parts['Part-2']
mdb.models['Model-1'].parts.changeKey(fromName='Part-New', toName='Part-1')
p = mdb.models['Model-1'].parts['Part-1']
a.Instance(name='Part-1-1', part=p, dependent=OFF)

#---------------------------------------------------------------------------
#
p = mdb.models['Model-1'].parts['Part-1']
selcell = p.cells.findAt(((-(rve_size+layer_t)/2.0, -(rve_size+layer_t)/2.0, -(rve_size+layer_t)/2.0), ))
p.Set(cells=selcell, name='Set-M-1')
volume1 = p.getMassProperties(regions=p.sets['Set-M-1'].cells)['volume']
#
incCells = p.cells[0:0]
for icell in p.cells:
    if icell.index != selcell[0].index:
        incCells += p.cells[icell.index:icell.index+1]
p.Set(cells=incCells, name='Set-M-2')
volume2 = p.getMassProperties(regions=p.sets['Set-M-2'].cells)['volume']
print (f'The volume fraction of particles is: {volume2/(volume2+volume1)}')

#---------------------------------------------------------------------------
#
mdb.saveAs(pathName=cae_name)