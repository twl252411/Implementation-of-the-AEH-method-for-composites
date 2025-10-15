# -*- coding: mbcs -*-
#
# Abaqus/CAE Release 2018 replay file
# Internal Version: 2017_11_08-01.21.41 127140
# Run by DELL
#
from abaqus import *
from abaqusConstants import *
from driverUtils import executeOnCaeStartup
import numpy as np

executeOnCaeStartup()
Mdb()


#----------------------------------------------------------------------------------------------
#
mdb_1 = mdb.models['Model-1']
alpha = 45.0
sb, r = 1.0, 2.0
extra_t = 0.06
#
width = (4 + 2 * r) * sb / np.cos(alpha / 180 * np.pi)
thickness = (4 + 2 * r) * sb / np.sin(alpha / 180 * np.pi)
height = thickness
rve_size = np.array([width+extra_t, thickness+extra_t, height+extra_t])
gamma = np.arctan(4 * (2 + r) * sb / (height * np.sin(2.0 * alpha / 180 * np.pi))) * 180 / np.pi
#
sa = sb * np.cos(gamma / 180 * np.pi) * np.sqrt(r**2 + 4 * r + 3)
l1 = (4 + 2 * r) * sb * np.cos(gamma / 180 * np.pi)
l2 = (2 + 2 * r) * sb * np.cos(gamma / 180 * np.pi)


#----------------------------------------------------------------------------------------------
# Section of the braiding yarns
#
s = mdb_1.ConstrainedSketch(name='__profile__', sheetSize=200.0)
g, v, d, c = s.geometry, s.vertices, s.dimensions, s.constraints
s.setPrimaryObject(option=STANDALONE)
s.Line(point1=(l2/2, -sb), point2=(l1/2, 0))
s.Line(point1=(l1/2, 0), point2=(l2/2, sb))
s.Line(point1=(l2/2, sb), point2=(-l2/2, sb))
s.Line(point1=(-l2/2, sb), point2=(-l1/2, 0))
s.Line(point1=(-l1/2, 0), point2=(-l2/2, -sb))
s.Line(point1=(-l2/2, -sb), point2=(l2/2, -sb))
p = mdb_1.Part(name='Part-1', dimensionality=THREE_D, type=DEFORMABLE_BODY)
p.BaseSolidExtrude(sketch=s, depth=height*5.0)
s.unsetPrimaryObject()
p = mdb_1.parts['Part-1']
del mdb_1.sketches['__profile__']


#----------------------------------------------------------------------------------------------
# the axial (motionless) yarns
s = mdb_1.ConstrainedSketch(name='__profile__', sheetSize=200.0)
g, v, d, c = s.geometry, s.vertices, s.dimensions, s.constraints
s.setPrimaryObject(option=STANDALONE)
s.rectangle(point1=(0.0, 0.0), point2=(r, r))
p = mdb_1.Part(name='Part-2', dimensionality=THREE_D, type=DEFORMABLE_BODY)
p.BaseSolidExtrude(sketch=s, depth=1.5 * height)
s.unsetPrimaryObject()
p = mdb_1.parts['Part-2']
del mdb_1.sketches['__profile__']


#----------------------------------------------------------------------------------------------
# the matrix
s = mdb_1.ConstrainedSketch(name='__profile__', sheetSize=200.0)
g, v, d, c = s.geometry, s.vertices, s.dimensions, s.constraints
s.setPrimaryObject(option=STANDALONE)
s.rectangle(point1=(0.0, 0.0), point2=(width, thickness))
p = mdb_1.Part(name='Part-3', dimensionality=THREE_D, type=DEFORMABLE_BODY)
p.BaseSolidExtrude(sketch=s, depth=height)
s.unsetPrimaryObject()
p = mdb_1.parts['Part-3']
del mdb_1.sketches['__profile__']


#----------------------------------------------------------------------------------------------
#---pink ones---
a = mdb_1.rootAssembly
p = mdb_1.parts['Part-1']
a.Instance(name='Part-1-1', part=p, dependent=OFF)
a.Instance(name='Part-1-2', part=p, dependent=OFF)
a.Instance(name='Part-1-3', part=p, dependent=OFF)
a.Instance(name='Part-1-4', part=p, dependent=OFF)
a.translate(instanceList=('Part-1-1', 'Part-1-2', 'Part-1-3', 'Part-1-4', ), vector=(thickness/8.0, width*3.0/8.0, -height*2.0))
a.rotate(instanceList=('Part-1-1', 'Part-1-2', 'Part-1-3', 'Part-1-4', ), axisPoint=(thickness/8.0, width*3.0/8.0, 0.0),
    axisDirection=(0.0, 0.0, 1.0), angle=alpha)
a.rotate(instanceList=('Part-1-1', 'Part-1-2', 'Part-1-3', 'Part-1-4', ), axisPoint=(thickness/8.0, width*3.0/8.0, 0.0),
    axisDirection=(thickness, -width, 0.0), angle=gamma)
a.translate(instanceList=('Part-1-2', 'Part-1-4', ), vector=(0.0, 0.0, height))
a.translate(instanceList=('Part-1-3', ), vector=(thickness, 0.0, 0.0))
a.translate(instanceList=('Part-1-4', ), vector=(thickness, 0.0, 0.0))
#
a.InstanceFromBooleanMerge(name='Part-11', instances=(a.instances['Part-1-1'], a.instances['Part-1-2'], a.instances['Part-1-3'],
    a.instances['Part-1-4'], ), originalInstances=DELETE, domain=GEOMETRY)
del a.features['Part-11-1']
#
a = mdb_1.rootAssembly
p1 = mdb_1.parts['Part-11']
a.Instance(name='Part-11-1', part=p1, dependent=OFF)
a.Instance(name='Part-11-2', part=p1, dependent=OFF)
p1 = mdb_1.parts['Part-3']
a.Instance(name='Part-3-1', part=p1, dependent=OFF)
a.InstanceFromBooleanCut(name='Part-4', instanceToBeCut=mdb_1.rootAssembly.instances['Part-11-2'],
    cuttingInstances=(a.instances['Part-3-1'], ), originalInstances=DELETE)
a.InstanceFromBooleanCut(name='Part-5', instanceToBeCut=mdb_1.rootAssembly.instances['Part-11-1'],
    cuttingInstances=(a.instances['Part-4-1'], ), originalInstances=DELETE)
#
del mdb_1.parts['Part-11']
del mdb_1.parts['Part-4']
a.deleteFeatures(('Part-5-1',))
mdb_1.parts.changeKey(fromName='Part-5', toName='Part-11')


#----------------------------------------------------------------------------------------------
#---red ones---
a = mdb_1.rootAssembly
p = mdb_1.parts['Part-1']
a.Instance(name='Part-1-1', part=p, dependent=OFF)
a.Instance(name='Part-1-2', part=p, dependent=OFF)
a.Instance(name='Part-1-3', part=p, dependent=OFF)
a.Instance(name='Part-1-4', part=p, dependent=OFF)
a.translate(instanceList=('Part-1-1', 'Part-1-2', 'Part-1-3', 'Part-1-4', ), vector=(thickness*5.0/8.0, width/8.0, -height*2.0))
a.rotate(instanceList=('Part-1-1', 'Part-1-2', 'Part-1-3', 'Part-1-4', ), axisPoint=(thickness*5.0/8.0, width/8.0, 0.0),
    axisDirection=(0.0, 0.0, 1.0), angle=-alpha)
a.rotate(instanceList=('Part-1-1', 'Part-1-2', 'Part-1-3', 'Part-1-4', ), axisPoint=(thickness*5.0/8.0, width/8.0, 0.0),
    axisDirection=(thickness, width, 0.0), angle=-gamma)
a.translate(instanceList=('Part-1-2', ), vector=(0.0, 0.0, height))
a.translate(instanceList=('Part-1-3', ), vector=(thickness, 0.0, 0.0))
a.translate(instanceList=('Part-1-4', ), vector=(0.0, width, 0.0))
#
a.InstanceFromBooleanMerge(name='Part-12', instances=(a.instances['Part-1-1'], a.instances['Part-1-2'], a.instances['Part-1-3'],
    a.instances['Part-1-4'], ), originalInstances=DELETE, domain=GEOMETRY)
del a.features['Part-12-1']
#
a = mdb_1.rootAssembly
p1 = mdb_1.parts['Part-12']
a.Instance(name='Part-12-1', part=p1, dependent=OFF)
a.Instance(name='Part-12-2', part=p1, dependent=OFF)
p1 = mdb_1.parts['Part-3']
a.Instance(name='Part-3-1', part=p1, dependent=OFF)
a.InstanceFromBooleanCut(name='Part-4', instanceToBeCut=mdb_1.rootAssembly.instances['Part-12-2'],
    cuttingInstances=(a.instances['Part-3-1'], ), originalInstances=DELETE)
a.InstanceFromBooleanCut(name='Part-5', instanceToBeCut=mdb_1.rootAssembly.instances['Part-12-1'],
    cuttingInstances=(a.instances['Part-4-1'], ), originalInstances=DELETE)
#
del mdb_1.parts['Part-12']
del mdb_1.parts['Part-4']
a.deleteFeatures(('Part-5-1',))
mdb_1.parts.changeKey(fromName='Part-5', toName='Part-12')


#----------------------------------------------------------------------------------------------
#---Blue ones---
a = mdb_1.rootAssembly
p = mdb_1.parts['Part-1']
a.Instance(name='Part-1-1', part=p, dependent=OFF)
a.Instance(name='Part-1-2', part=p, dependent=OFF)
a.Instance(name='Part-1-3', part=p, dependent=OFF)
a.Instance(name='Part-1-4', part=p, dependent=OFF)
a.translate(instanceList=('Part-1-1', 'Part-1-2', 'Part-1-3', 'Part-1-4', ), vector=(thickness*3.0/8.0, width*7.0/8.0, -height*2.0))
a.rotate(instanceList=('Part-1-1', 'Part-1-2', 'Part-1-3', 'Part-1-4', ), axisPoint=(thickness*3.0/8.0, width*7.0/8.0, 0.0),
    axisDirection=(0.0, 0.0, 1.0), angle=-alpha)
a.rotate(instanceList=('Part-1-1', 'Part-1-2', 'Part-1-3', 'Part-1-4', ), axisPoint=(thickness*3.0/8.0, width*7.0/8.0, 0.0),
    axisDirection=(thickness, width, 0.0), angle=gamma)
a.translate(instanceList=('Part-1-2', ), vector=(0.0, 0.0, height))
a.translate(instanceList=('Part-1-3', ), vector=(-thickness, 0.0, 0.0))
a.translate(instanceList=('Part-1-4', ), vector=(0.0, -width, 0.0))
#
a.InstanceFromBooleanMerge(name='Part-13', instances=(a.instances['Part-1-1'], a.instances['Part-1-2'], a.instances['Part-1-3'],
    a.instances['Part-1-4'], ), originalInstances=DELETE, domain=GEOMETRY)
del a.features['Part-13-1']
#
a = mdb_1.rootAssembly
p1 = mdb_1.parts['Part-13']
a.Instance(name='Part-13-1', part=p1, dependent=OFF)
a.Instance(name='Part-13-2', part=p1, dependent=OFF)
p1 = mdb_1.parts['Part-3']
a.Instance(name='Part-3-1', part=p1, dependent=OFF)
a.InstanceFromBooleanCut(name='Part-4', instanceToBeCut=mdb_1.rootAssembly.instances['Part-13-2'],
    cuttingInstances=(a.instances['Part-3-1'], ), originalInstances=DELETE)
a.InstanceFromBooleanCut(name='Part-5', instanceToBeCut=mdb_1.rootAssembly.instances['Part-13-1'],
    cuttingInstances=(a.instances['Part-4-1'], ), originalInstances=DELETE)
#
del mdb_1.parts['Part-13']
del mdb_1.parts['Part-4']
a.deleteFeatures(('Part-5-1',))
mdb_1.parts.changeKey(fromName='Part-5', toName='Part-13')


#----------------------------------------------------------------------------------------------
#---Green ones---
a = mdb_1.rootAssembly
p = mdb_1.parts['Part-1']
a.Instance(name='Part-1-1', part=p, dependent=OFF)
a.Instance(name='Part-1-2', part=p, dependent=OFF)
a.Instance(name='Part-1-3', part=p, dependent=OFF)
a.Instance(name='Part-1-4', part=p, dependent=OFF)
a.translate(instanceList=('Part-1-1', 'Part-1-2', 'Part-1-3', 'Part-1-4', ), vector=(thickness*7.0/8.0, width*5.0/8.0, -height*2.0))
a.rotate(instanceList=('Part-1-1', 'Part-1-2', 'Part-1-3', 'Part-1-4', ), axisPoint=(thickness*7.0/8.0, width*5.0/8.0, 0.0),
    axisDirection=(0.0, 0.0, 1.0), angle=alpha)
a.rotate(instanceList=('Part-1-1', 'Part-1-2', 'Part-1-3', 'Part-1-4', ), axisPoint=(thickness*7.0/8.0, width*5.0/8.0, 0.0),
    axisDirection=(thickness, -width, 0.0), angle=-gamma)
a.translate(instanceList=('Part-1-2', 'Part-1-4', ), vector=(0.0, 0.0, height))
a.translate(instanceList=('Part-1-3', ), vector=(-thickness, 0.0, 0.0))
a.translate(instanceList=('Part-1-4', ), vector=(-thickness, 0.0, 0.0))
#
a.InstanceFromBooleanMerge(name='Part-14', instances=(a.instances['Part-1-1'], a.instances['Part-1-2'], a.instances['Part-1-3'],
    a.instances['Part-1-4'], ), originalInstances=DELETE, domain=GEOMETRY)
del a.features['Part-14-1']
#
a = mdb_1.rootAssembly
p1 = mdb_1.parts['Part-14']
a.Instance(name='Part-14-1', part=p1, dependent=OFF)
a.Instance(name='Part-14-2', part=p1, dependent=OFF)
p1 = mdb_1.parts['Part-3']
a.Instance(name='Part-3-1', part=p1, dependent=OFF)
a.InstanceFromBooleanCut(name='Part-4', instanceToBeCut=mdb_1.rootAssembly.instances['Part-14-2'],
    cuttingInstances=(a.instances['Part-3-1'], ), originalInstances=DELETE)
a.InstanceFromBooleanCut(name='Part-5', instanceToBeCut=mdb_1.rootAssembly.instances['Part-14-1'],
    cuttingInstances=(a.instances['Part-4-1'], ), originalInstances=DELETE)
#
del mdb_1.parts['Part-14']
del mdb_1.parts['Part-4']
a.deleteFeatures(('Part-5-1',))
mdb_1.parts.changeKey(fromName='Part-5', toName='Part-14')


#----------------------------------------------------------------------------------------------
#---the axial yarns---
a = mdb_1.rootAssembly
p = mdb_1.parts['Part-2']
a.Instance(name='Part-2-1', part=p, dependent=OFF)
a.Instance(name='Part-2-2', part=p, dependent=OFF)
a.Instance(name='Part-2-3', part=p, dependent=OFF)
a.Instance(name='Part-2-4', part=p, dependent=OFF)
a.translate(instanceList=('Part-2-1', 'Part-2-2', 'Part-2-3', 'Part-2-4', ), vector=(-r/2, -r/2, -0.25*height))
a.rotate(instanceList=('Part-2-1', 'Part-2-3', ), axisPoint=(0.0, 0.0, 0.0), axisDirection=(0.0, 0.0, 1.0), angle=alpha)
a.rotate(instanceList=('Part-2-2', 'Part-2-4', ), axisPoint=(0.0, 0.0, 0.0), axisDirection=(0.0, 0.0, 1.0), angle=-alpha)
a.translate(instanceList=('Part-2-1', ), vector=(thickness/4.0, width/4.0, 0.0))
a.translate(instanceList=('Part-2-2', ), vector=(thickness/4.0, width*3.0/4.0, 0.0))
a.translate(instanceList=('Part-2-3', ), vector=(thickness*3.0/4.0, width*3.0/4.0, 0.0))
a.translate(instanceList=('Part-2-4', ), vector=(thickness*3.0/4.0, width/4.0, 0.0))
#
a.InstanceFromBooleanMerge(name='Part-15', instances=(a.instances['Part-2-1'], a.instances['Part-2-2'],
    a.instances['Part-2-3'], a.instances['Part-2-4'], ), originalInstances=DELETE, domain=GEOMETRY)
del a.features['Part-15-1']
#
a = mdb_1.rootAssembly
p1 = mdb_1.parts['Part-15']
a.Instance(name='Part-15-1', part=p1, dependent=OFF)
a.Instance(name='Part-21-2', part=p1, dependent=OFF)
p1 = mdb_1.parts['Part-3']
a.Instance(name='Part-3-1', part=p1, dependent=OFF)
a.InstanceFromBooleanCut(name='Part-4', instanceToBeCut=mdb_1.rootAssembly.instances['Part-21-2'],
    cuttingInstances=(a.instances['Part-3-1'], ), originalInstances=DELETE)
a.InstanceFromBooleanCut(name='Part-5', instanceToBeCut=mdb_1.rootAssembly.instances['Part-15-1'],
    cuttingInstances=(a.instances['Part-4-1'], ), originalInstances=DELETE)
#
del mdb_1.parts['Part-15']
del mdb_1.parts['Part-4']
a.deleteFeatures(('Part-5-1',))
mdb_1.parts.changeKey(fromName='Part-5', toName='Part-15')


#----------------------------------------------------------------------------------------------
#---the axial motionless yarns---
a = mdb_1.rootAssembly
p = mdb_1.parts['Part-2']
for irow in range(3):
    for jcol in range(3):
        ins_name = f'Part-2-{irow*3+jcol+1}'
        a.Instance(name=ins_name, part=p, dependent=OFF)
        a.translate(instanceList=(ins_name,), vector=(-r/2, -r/2, -0.25*height))
        a.rotate(instanceList=(ins_name, ), axisPoint=(0.0, 0.0, 0.0), axisDirection=(0.0, 0.0, 1.0), angle=-alpha)
        a.translate(instanceList=(ins_name, ), vector=(width/2.0*irow, thickness/2.0*jcol, 0.0))
#
a.InstanceFromBooleanMerge(name='Part-16', instances=(a.instances['Part-2-1'], a.instances['Part-2-2'],
    a.instances['Part-2-3'], a.instances['Part-2-4'], a.instances['Part-2-5'], a.instances['Part-2-6'],
    a.instances['Part-2-7'], a.instances['Part-2-8'], a.instances['Part-2-9'], ), originalInstances=DELETE, domain=GEOMETRY)
del a.features['Part-16-1']
#
a = mdb_1.rootAssembly
p1 = mdb_1.parts['Part-16']
a.Instance(name='Part-16-1', part=p1, dependent=OFF)
a.Instance(name='Part-22-2', part=p1, dependent=OFF)
p1 = mdb_1.parts['Part-3']
a.Instance(name='Part-3-1', part=p1, dependent=OFF)
a.InstanceFromBooleanCut(name='Part-4', instanceToBeCut=mdb_1.rootAssembly.instances['Part-22-2'],
    cuttingInstances=(a.instances['Part-3-1'], ), originalInstances=DELETE)
a.InstanceFromBooleanCut(name='Part-5', instanceToBeCut=mdb_1.rootAssembly.instances['Part-16-1'],
    cuttingInstances=(a.instances['Part-4-1'], ), originalInstances=DELETE)
#
del mdb_1.parts['Part-16']
del mdb_1.parts['Part-4']
a.deleteFeatures(('Part-5-1',))
mdb_1.parts.changeKey(fromName='Part-5', toName='Part-16')


#----------------------------------------------------------------------------------------------
#
a = mdb_1.rootAssembly
p1 = mdb_1.parts['Part-11']
a.Instance(name='Part-11-1', part=p1, dependent=OFF)
p1 = mdb_1.parts['Part-12']
a.Instance(name='Part-12-1', part=p1, dependent=OFF)
p1 = mdb_1.parts['Part-13']
a.Instance(name='Part-13-1', part=p1, dependent=OFF)
p1 = mdb_1.parts['Part-14']
a.Instance(name='Part-14-1', part=p1, dependent=OFF)
p1 = mdb_1.parts['Part-15']
a.Instance(name='Part-15-1', part=p1, dependent=OFF)
p1 = mdb_1.parts['Part-16']
a.Instance(name='Part-16-1', part=p1, dependent=OFF)
a.translate(instanceList=('Part-11-1', 'Part-12-1', 'Part-13-1', 'Part-14-1', 'Part-15-1', 'Part-16-1', ),
    vector=(-width/2., -thickness/2., -height/2.))
del mdb_1.parts['Part-1']
del mdb_1.parts['Part-2']
del mdb_1.parts['Part-3']
#
keypoints = np.zeros([29, 3])
for ins in range(6):
    p = mdb_1.parts['Part-' + str(ins + 11)]
    icount = 0
    for icell in p.cells:
        keypoints[icount + ins * 4, :] = p.getCentroid(cells=p.cells[icell.index:icell.index + 1])
        icount = icount + 1


#----------------------------------------------------------------------------------------------
#
s = mdb_1.ConstrainedSketch(name='__profile__', sheetSize=200.0)
g, v, d, c = s.geometry, s.vertices, s.dimensions, s.constraints
s.setPrimaryObject(option=STANDALONE)
s.rectangle(point1=(0.0, 0.0), point2=(rve_size[0], rve_size[1]))
p = mdb_1.Part(name='Part-2', dimensionality=THREE_D, type=DEFORMABLE_BODY)
p.BaseSolidExtrude(sketch=s, depth=rve_size[2])
s.unsetPrimaryObject()
del mdb_1.sketches['__profile__']
a = mdb_1.rootAssembly
a.Instance(name='Part-2-1', part=p, dependent=OFF)
a.translate(instanceList=('Part-2-1', ), vector=(-rve_size[0]/2., -rve_size[1]/2., -rve_size[2]/2.))
#
insts = ((a.instances['Part-11-1'], a.instances['Part-12-1'], a.instances['Part-13-1'], a.instances['Part-14-1'],
    a.instances['Part-15-1'], a.instances['Part-16-1'], a.instances['Part-2-1'], ))
a.InstanceFromBooleanMerge(name='Part-T', instances=insts, keepIntersections=ON, originalInstances=DELETE, domain=GEOMETRY)
a.deleteFeatures(('Part-T-1', ))
del mdb_1.parts['Part-11']
del mdb_1.parts['Part-12']
del mdb_1.parts['Part-13']
del mdb_1.parts['Part-14']
del mdb_1.parts['Part-15']
del mdb_1.parts['Part-16']
del mdb_1.parts['Part-2']
mdb_1.parts.changeKey(fromName='Part-T', toName='Part-1')
p = mdb_1.parts['Part-1']
a.Instance(name='Part-1-1', part=p, dependent=OFF)


#--------------------------------------------------------------------------------------------------
#
p = mdb.models['Model-1'].parts['Part-1']
cell2, cell3, cell4, cell5, cell6 = p.cells[0:0], p.cells[0:0], p.cells[0:0], p.cells[0:0], p.cells[0:0]
for inum in range(29):
    tpt = (keypoints[inum][0]-thickness/2.0, keypoints[inum][1]-width/2.0, keypoints[inum][2]-height/2.0)
    if inum//4 == 0:
        cell2 += p.cells.findAt(((tpt), ))
    elif inum//4 == 1:
        cell3 += p.cells.findAt(((tpt), ))
    elif inum // 4 == 2:
        cell4 += p.cells.findAt(((tpt), ))
    elif inum // 4 == 3:
        cell5 += p.cells.findAt(((tpt), ))
    else:
        cell6 += p.cells.findAt(((tpt), ))
p.Set(cells=cell2, name='Set-M-2')
p.Set(cells=cell3, name='Set-M-3')
p.Set(cells=cell4, name='Set-M-4')
p.Set(cells=cell5, name='Set-M-5')
p.Set(cells=cell6, name='Set-M-6')
#
p = mdb.models['Model-1'].parts['Part-1']
cell1 = p.cells[0:0]
for icell in p.cells:
    if (icell not in p.sets['Set-M-2'].cells and icell not in p.sets['Set-M-3'].cells and
        icell not in p.sets['Set-M-4'].cells and icell not in p.sets['Set-M-5'].cells and
        icell not in p.sets['Set-M-6'].cells):
        cell1 += p.cells[icell.index:icell.index+1]
p.Set(cells=cell1, name='Set-M-1')
volume1 = p.getMassProperties(regions=p.sets['Set-M-1'].cells)['volume']
#
p = mdb.models['Model-1'].parts['Part-1']
volume = p.getMassProperties( )['volume']
print (f'The volume fraction of yarns is: {1.0 - volume1/volume}')

#----------------------------------------------------------------------------------------------
#
cae_name = '5D_braided_RVE.cae'
mdb.saveAs(pathName=cae_name)