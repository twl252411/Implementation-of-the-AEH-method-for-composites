#
from abaqus import *
from abaqusConstants import *
from driverUtils import executeOnCaeStartup
import numpy as np
from itertools import product
#
executeOnCaeStartup()
Mdb()

#----------------------------------------------------------------------------------------------
#

cae_name = f'4D_braided_rve.cae'
width, thickness, extra_t = 4.0, 4.0, 0.04
height = width
gamma = np.arctan(np.sqrt(2.0))*180/np.pi
hgt = height/np.cos(gamma/180*np.pi)
rve_size = np.array([width+extra_t, thickness+extra_t, height+extra_t])
#
b = width/(4.0*np.sqrt(2.0))
a = np.sqrt(3.0)*b*np.cos(gamma/180*np.pi)
l1, l2 = 2.0*b*np.cos(gamma/180*np.pi), (4.0-2.0*np.sqrt(3.0))*b


#----------------------------------------------------------------------------------------------
#
s = mdb.models['Model-1'].ConstrainedSketch(name='__profile__', sheetSize=200.0)
g, v, d, c = s.geometry, s.vertices, s.dimensions, s.constraints
s.setPrimaryObject(option=STANDALONE)
s.Line(point1=(l2/2.0, a),   point2=(b, l1/2.0))
s.Line(point1=(b, l1/2.0),   point2=(b, -l1/2.0))
s.Line(point1=(b, -l1/2.0),  point2=(l2/2.0, -a))
s.Line(point1=(l2/2.0, -a),  point2=(-l2/2.0, -a))
s.Line(point1=(-l2/2.0, -a), point2=(-b, -l1/2.0))
s.Line(point1=(-b, -l1/2.0), point2=(-b, l1/2.0))
s.Line(point1=(-b, l1/2.0),  point2=(-l2/2.0, a))
s.Line(point1=(-l2/2.0, a),  point2=(l2/2.0, a))
p = mdb.models['Model-1'].Part(name='Part-1', dimensionality=THREE_D, type=DEFORMABLE_BODY)
p.BaseSolidExtrude(sketch=s, depth=hgt*2.0)
s.unsetPrimaryObject()
del mdb.models['Model-1'].sketches['__profile__']

#----------------------------------------------------------------------------------------------
#
s = mdb.models['Model-1'].ConstrainedSketch(name='__profile__', sheetSize=200.0)
g, v, d, c = s.geometry, s.vertices, s.dimensions, s.constraints
s.setPrimaryObject(option=STANDALONE)
s.rectangle(point1=(0.0, 0.0), point2=(width, thickness))
p = mdb.models['Model-1'].Part(name='Part-2', dimensionality=THREE_D, type=DEFORMABLE_BODY)
p.BaseSolidExtrude(sketch=s, depth=height)
s.unsetPrimaryObject()
del mdb.models['Model-1'].sketches['__profile__']
#
a = mdb.models['Model-1'].rootAssembly
p = mdb.models['Model-1'].parts['Part-2']
a.Instance(name='Part-2-1', part=p, dependent=OFF)

#----------------------------------------------------------------------------------------------
#
#---Pink ones---
a = mdb.models['Model-1'].rootAssembly
p = mdb.models['Model-1'].parts['Part-1']
a.Instance(name='Part-1-1', part=p, dependent=OFF)
a.Instance(name='Part-1-2', part=p, dependent=OFF)
a.Instance(name='Part-1-3', part=p, dependent=OFF)
a.Instance(name='Part-1-4', part=p, dependent=OFF)
#
a.translate(instanceList=('Part-1-1', 'Part-1-2', 'Part-1-3', 'Part-1-4', ), vector=(width, 0.0, -0.5*hgt))
a.rotate(instanceList=('Part-1-1', 'Part-1-2', 'Part-1-3', 'Part-1-4', ), axisPoint=(width, 0.0, 0.0), axisDirection=(0.0, 0.0, 1.0), angle=45)
a.rotate(instanceList=('Part-1-1', 'Part-1-2', 'Part-1-3', 'Part-1-4', ), axisPoint=(width, 0.0, 0.0), axisDirection=(1.0, 1.0, 0.0), angle=-gamma)
a.translate(instanceList=('Part-1-1', 'Part-1-4', ), vector=(width*3/8, -thickness/8, 0.0))
a.translate(instanceList=('Part-1-2', 'Part-1-3', ), vector=(-width*5/8, thickness*7/8, 0.0))
a.translate(instanceList=('Part-1-3', ), vector=(0.0, -thickness, 0.0))
a.translate(instanceList=('Part-1-4', ), vector=(0.0, -thickness, 0.0))
#
a.InstanceFromBooleanMerge(name='Part-11', instances=(a.instances['Part-1-1'], a.instances['Part-1-2'], a.instances['Part-1-3'],
    a.instances['Part-1-4'], ), originalInstances=DELETE, domain=GEOMETRY)
del a.features['Part-11-1']
#
#----------------------------------------------------
#
a = mdb.models['Model-1'].rootAssembly
p = mdb.models['Model-1'].parts['Part-11']
a.Instance(name='Part-11-1', part=p, dependent=OFF)
a.Instance(name='Part-11-2', part=p, dependent=OFF)
p = mdb.models['Model-1'].parts['Part-2']
a.Instance(name='Part-2-1', part=p, dependent=OFF)
#
a.InstanceFromBooleanCut(name='Part-3', instanceToBeCut=mdb.models['Model-1'].rootAssembly.instances['Part-11-2'],
    cuttingInstances=(a.instances['Part-2-1'], ), originalInstances=DELETE)
a.InstanceFromBooleanCut(name='Part-4', instanceToBeCut=mdb.models['Model-1'].rootAssembly.instances['Part-11-1'],
    cuttingInstances=(a.instances['Part-3-1'], ), originalInstances=DELETE)
del mdb.models['Model-1'].parts['Part-11']
del mdb.models['Model-1'].parts['Part-3']
a.deleteFeatures(('Part-4-1',))
mdb.models['Model-1'].parts.changeKey(fromName='Part-4', toName='Part-11')

#----------------------------------------------------------------------------------------------
#
#---Red ones---
a = mdb.models['Model-1'].rootAssembly
p = mdb.models['Model-1'].parts['Part-1']
a.Instance(name='Part-1-5', part=p, dependent=OFF)
a.Instance(name='Part-1-6', part=p, dependent=OFF)
a.Instance(name='Part-1-7', part=p, dependent=OFF)
a.Instance(name='Part-1-8', part=p, dependent=OFF)
#
a.translate(instanceList=('Part-1-5', 'Part-1-6', 'Part-1-7', 'Part-1-8' ), vector=(width, thickness, -0.5*hgt))
a.rotate(instanceList=('Part-1-5', 'Part-1-6', 'Part-1-7', 'Part-1-8' ), axisPoint=(width, thickness, 0.0), axisDirection=(0.0, 0.0, -1.0), angle=45)
a.rotate(instanceList=('Part-1-5', 'Part-1-6', 'Part-1-7', 'Part-1-8' ), axisPoint=(width, thickness, 0.0), axisDirection=(-1.0, 1.0, 0.0), angle=-gamma)
a.translate(instanceList=('Part-1-5', 'Part-1-8', ), vector=(-width/8, -thickness*3/8, 0.0))
a.translate(instanceList=('Part-1-6', 'Part-1-7', ), vector=(width*7/8, thickness*5/8, 0.0))
a.translate(instanceList=('Part-1-7', ), vector=(-width, 0.0, 0.0))
a.translate(instanceList=('Part-1-8', ), vector=(-width, 0.0, 0.0))
#
a.InstanceFromBooleanMerge(name='Part-12', instances=(a.instances['Part-1-5'], a.instances['Part-1-6'], a.instances['Part-1-7'],
    a.instances['Part-1-8'], ), originalInstances=DELETE, domain=GEOMETRY)
del a.features['Part-12-1']

#----------------------------------------------------
#
a = mdb.models['Model-1'].rootAssembly
p1 = mdb.models['Model-1'].parts['Part-12']
a.Instance(name='Part-12-1', part=p1, dependent=OFF)
a.Instance(name='Part-12-2', part=p1, dependent=OFF)
p1 = mdb.models['Model-1'].parts['Part-2']
a.Instance(name='Part-2-1', part=p1, dependent=OFF)
#
a.InstanceFromBooleanCut(name='Part-3',instanceToBeCut=mdb.models['Model-1'].rootAssembly.instances['Part-12-2'],
    cuttingInstances=(a.instances['Part-2-1'], ), originalInstances=DELETE)
a.InstanceFromBooleanCut(name='Part-4', instanceToBeCut=mdb.models['Model-1'].rootAssembly.instances['Part-12-1'],
    cuttingInstances=(a.instances['Part-3-1'], ), originalInstances=DELETE)
del mdb.models['Model-1'].parts['Part-12']
del mdb.models['Model-1'].parts['Part-3']
a.deleteFeatures(('Part-4-1',))
mdb.models['Model-1'].parts.changeKey(fromName='Part-4', toName='Part-12')

#----------------------------------------------------------------------------------------------
#
#---Blue ones---
a = mdb.models['Model-1'].rootAssembly
p = mdb.models['Model-1'].parts['Part-1']
a.Instance(name='Part-1-9', part=p, dependent=OFF)
a.Instance(name='Part-1-10', part=p, dependent=OFF)
a.Instance(name='Part-1-11', part=p, dependent=OFF)
a.Instance(name='Part-1-12', part=p, dependent=OFF)
#
a.translate(instanceList=('Part-1-9', 'Part-1-10', 'Part-1-11', 'Part-1-12', ), vector=(0.0, 0.0, -0.5*hgt))
a.rotate(instanceList=('Part-1-9', 'Part-1-10', 'Part-1-11', 'Part-1-12', ), axisPoint=(0.0, 0.0, 0.0), axisDirection=(0.0, 0.0, -1.0), angle=45)
a.rotate(instanceList=('Part-1-9', 'Part-1-10', 'Part-1-11', 'Part-1-12', ), axisPoint=(0.0, 0.0, 0.0), axisDirection=(1.0, -1.0, 0.0), angle=-gamma)
a.translate(instanceList=('Part-1-9', 'Part-1-12',), vector=(width/8, thickness*3/8, 0.0))
a.translate(instanceList=('Part-1-10', 'Part-1-11', ), vector=(-width*7/8, -thickness*5/8, 0.0))
a.translate(instanceList=('Part-1-11', ), vector=(width, 0.0, 0.0))
a.translate(instanceList=('Part-1-12', ), vector=(width, 0.0, 0.0))
#
a.InstanceFromBooleanMerge(name='Part-13', instances=(a.instances['Part-1-9'], a.instances['Part-1-10'], a.instances['Part-1-11'],
    a.instances['Part-1-12'], ), originalInstances=DELETE, domain=GEOMETRY)
del a.features['Part-13-1']

#----------------------------------------------------
#
a = mdb.models['Model-1'].rootAssembly
p1 = mdb.models['Model-1'].parts['Part-13']
a.Instance(name='Part-13-1', part=p1, dependent=OFF)
a.Instance(name='Part-13-2', part=p1, dependent=OFF)
p1 = mdb.models['Model-1'].parts['Part-2']
a.Instance(name='Part-2-1', part=p1, dependent=OFF)
#
a.InstanceFromBooleanCut(name='Part-3',instanceToBeCut=mdb.models['Model-1'].rootAssembly.instances['Part-13-2'],
    cuttingInstances=(a.instances['Part-2-1'], ), originalInstances=DELETE)
a = mdb.models['Model-1'].rootAssembly
a.InstanceFromBooleanCut(name='Part-4', instanceToBeCut=mdb.models['Model-1'].rootAssembly.instances['Part-13-1'],
    cuttingInstances=(a.instances['Part-3-1'], ), originalInstances=DELETE)
del mdb.models['Model-1'].parts['Part-13']
del mdb.models['Model-1'].parts['Part-3']
a.deleteFeatures(('Part-4-1',))
mdb.models['Model-1'].parts.changeKey(fromName='Part-4', toName='Part-13')

#----------------------------------------------------------------------------------------------
#
#---Green ones---
a = mdb.models['Model-1'].rootAssembly
p = mdb.models['Model-1'].parts['Part-1']
a.Instance(name='Part-1-13', part=p, dependent=OFF)
a.Instance(name='Part-1-14', part=p, dependent=OFF)
a.Instance(name='Part-1-15', part=p, dependent=OFF)
a.Instance(name='Part-1-16', part=p, dependent=OFF)
#
a.translate(instanceList=('Part-1-13', 'Part-1-14', 'Part-1-15', 'Part-1-16', ), vector=(0.0, thickness, -0.5*hgt))
a.rotate(instanceList=('Part-1-13', 'Part-1-14', 'Part-1-15', 'Part-1-16', ), axisPoint=(0.0, thickness, 0.0), axisDirection=(0.0, 0.0, 1.0), angle=45)
a.rotate(instanceList=('Part-1-13', 'Part-1-14', 'Part-1-15', 'Part-1-16', ), axisPoint=(0.0, thickness, 0.0), axisDirection=(-1.0, -1.0, 0.0), angle=-gamma)
a.translate(instanceList=('Part-1-13', 'Part-1-16', ), vector=(-width*3/8, thickness/8, 0.0))
a.translate(instanceList=('Part-1-14', 'Part-1-15', ), vector=(width*5/8, -thickness*7/8, 0.0))
a.translate(instanceList=('Part-1-15', ), vector=(0.0, thickness, 0.0))
a.translate(instanceList=('Part-1-16', ), vector=(0.0, thickness, 0.0))
#
a.InstanceFromBooleanMerge(name='Part-14', instances=(a.instances['Part-1-13'], a.instances['Part-1-14'], a.instances['Part-1-15'],
    a.instances['Part-1-16'], ), originalInstances=DELETE, domain=GEOMETRY)
del a.features['Part-14-1']

#----------------------------------------------------
#
a = mdb.models['Model-1'].rootAssembly
p1 = mdb.models['Model-1'].parts['Part-14']
a.Instance(name='Part-14-1', part=p1, dependent=OFF)
a.Instance(name='Part-14-2', part=p1, dependent=OFF)
p1 = mdb.models['Model-1'].parts['Part-2']
a.Instance(name='Part-2-1', part=p1, dependent=OFF)
#
a.InstanceFromBooleanCut(name='Part-3', instanceToBeCut=mdb.models['Model-1'].rootAssembly.instances['Part-14-2'],
    cuttingInstances=(a.instances['Part-2-1'], ), originalInstances=DELETE)
a.InstanceFromBooleanCut(name='Part-4', instanceToBeCut=mdb.models['Model-1'].rootAssembly.instances['Part-14-1'],
    cuttingInstances=(a.instances['Part-3-1'], ), originalInstances=DELETE)
del mdb.models['Model-1'].parts['Part-14']
del mdb.models['Model-1'].parts['Part-3']
a.deleteFeatures(('Part-4-1',))
mdb.models['Model-1'].parts.changeKey(fromName='Part-4', toName='Part-14')

#----------------------------------------------------------------------------------------------
#
a = mdb.models['Model-1'].rootAssembly
p = mdb.models['Model-1'].parts['Part-11']
a.Instance(name='Part-11-1', part=p, dependent=OFF)
p = mdb.models['Model-1'].parts['Part-12']
a.Instance(name='Part-12-1', part=p, dependent=OFF)
p = mdb.models['Model-1'].parts['Part-13']
a.Instance(name='Part-13-1', part=p, dependent=OFF)
p = mdb.models['Model-1'].parts['Part-14']
a.Instance(name='Part-14-1', part=p, dependent=OFF)
a.translate(instanceList=('Part-11-1', 'Part-12-1', 'Part-13-1', 'Part-14-1', ), vector=(-width/2.0, -thickness/2.0, -height/2.0))
del mdb.models['Model-1'].parts['Part-2']

#----------------------------------------------------------------------------------------------
#
s = mdb.models['Model-1'].ConstrainedSketch(name='__profile__', sheetSize=200.0)
g, v, d, c = s.geometry, s.vertices, s.dimensions, s.constraints
s.setPrimaryObject(option=STANDALONE)
s.rectangle(point1=(0.0, 0.0), point2=(width+extra_t, thickness+extra_t))
p = mdb.models['Model-1'].Part(name='Part-2', dimensionality=THREE_D, type=DEFORMABLE_BODY)
p.BaseSolidExtrude(sketch=s, depth=height+extra_t)
s.unsetPrimaryObject()
del mdb.models['Model-1'].sketches['__profile__']
#
a = mdb.models['Model-1'].rootAssembly
p = mdb.models['Model-1'].parts['Part-2']
a.Instance(name='Part-2-1', part=p, dependent=OFF)
a.translate(instanceList=('Part-2-1', ), vector=(-width/2.0-extra_t/2.0, -thickness/2.0-extra_t/2.0, -height/2.0-extra_t/2.0))
a.InstanceFromBooleanCut(name='Part-3', instanceToBeCut=a.instances['Part-2-1'], cuttingInstances=(a.instances['Part-11-1'],
    a.instances['Part-12-1'], a.instances['Part-13-1'], a.instances['Part-14-1'], ), originalInstances=DELETE)
a.deleteFeatures(('Part-3-1',))
del mdb.models['Model-1'].parts['Part-1']
del mdb.models['Model-1'].parts['Part-2']
mdb.models['Model-1'].parts.changeKey(fromName='Part-3', toName='Part-1')

#----------------------------------------------------------------------------------------------
#
mdb.models['Model-1'].parts.changeKey(fromName='Part-11', toName='Part-2')
mdb.models['Model-1'].parts.changeKey(fromName='Part-12', toName='Part-3')
mdb.models['Model-1'].parts.changeKey(fromName='Part-13', toName='Part-4')
mdb.models['Model-1'].parts.changeKey(fromName='Part-14', toName='Part-5')
#
a = mdb.models['Model-1'].rootAssembly
p = mdb.models['Model-1'].parts['Part-2']
a.Instance(name='Part-2-1', part=p, dependent=OFF)
p = mdb.models['Model-1'].parts['Part-3']
a.Instance(name='Part-3-1', part=p, dependent=OFF)
p = mdb.models['Model-1'].parts['Part-4']
a.Instance(name='Part-4-1', part=p, dependent=OFF)
p = mdb.models['Model-1'].parts['Part-5']
a.Instance(name='Part-5-1', part=p, dependent=OFF)
p = mdb.models['Model-1'].parts['Part-1']
a.Instance(name='Part-1-1', part=p, dependent=OFF)
a.translate(instanceList=('Part-2-1', 'Part-3-1', 'Part-4-1', 'Part-5-1', ), vector=(-width/2.0, -thickness/2.0, -height/2.0))
#
keypoints = np.zeros((16, 3))
for ins in range(4):
    p = mdb.models['Model-1'].parts[f'Part-{ins+2}']
    for icount, icell in enumerate(p.cells):
        keypoints[ins*4 + icount, :] = p.getCentroid(cells=p.cells[icell.index:icell.index+1])
#
a = mdb.models['Model-1'].rootAssembly
a.InstanceFromBooleanMerge(name='Part-11', instances=(a.instances['Part-1-1'], a.instances['Part-2-1'], a.instances['Part-3-1'],
    a.instances['Part-4-1'], a.instances['Part-5-1'], ), keepIntersections=ON, originalInstances=DELETE, domain=GEOMETRY)
del a.features['Part-11-1']
#
del mdb.models['Model-1'].parts['Part-1']
del mdb.models['Model-1'].parts['Part-2']
del mdb.models['Model-1'].parts['Part-3']
del mdb.models['Model-1'].parts['Part-4']
del mdb.models['Model-1'].parts['Part-5']
mdb.models['Model-1'].parts.changeKey(fromName='Part-11', toName='Part-1')


#----------------------------------------------------------------------------------------------
#
a = mdb.models['Model-1'].rootAssembly
p = mdb.models['Model-1'].parts['Part-1']
a.Instance(name='Part-1-1', part=p, dependent=OFF)

#----------------------------------------------------------------------------------------------
#
# p = mdb.models['Model-1'].parts['Part-1']
# p.DatumCsysByThreePoints(name='Datum csys-0', coordSysType=CARTESIAN, origin=(0, 0, 0), point1=(1, 0, 0), point2=(0, 1, 0))
# #
# p = mdb.models['Model-1'].parts['Part-1']
# p.DatumCsysByThreePoints(name='Datum csys-1', coordSysType=CARTESIAN, origin=(-1.0/8*width, 3.0/8*thickness, 0.5*height),
#    point1=(7.0/8*width, -5.0/8*thickness, -0.5*height), point2=(7.0/8*width, thickness+3.0/8*thickness, 0.5*height))
# #
# p = mdb.models['Model-1'].parts['Part-1']
# p.DatumCsysByThreePoints(name='Datum csys-2', coordSysType=CARTESIAN, origin=(3.0/8*width, 1.0/8*thickness, -0.5*height),
#    point1=(-5.0/8*width, -7.0/8*thickness, 0.5*height), point2=(11.0/8*width, -7.0/8*thickness, -0.5*height))
# #
# p = mdb.models['Model-1'].parts['Part-1']
# p.DatumCsysByThreePoints(name='Datum csys-3', coordSysType=CARTESIAN, origin=(-3.0/8*width, -1.0/8*thickness, -0.5*height),
#    point1=(5.0/8*width, 7.0/8*thickness, 0.5*height), point2=(5.0/8*width, -9.0/8*thickness, -0.5*height))
# #
# p = mdb.models['Model-1'].parts['Part-1']
# p.DatumCsysByThreePoints(name='Datum csys-4', coordSysType=CARTESIAN, origin=(1.0/8*width, -3.0/8*thickness, 0.5*height),
#    point1=(-7.0/8*width, 5.0/8*thickness, -0.5*height), point2=(9.0/8*width, 5.0/8*thickness, 0.5*height))

#----------------------------------------------------------------------------------------------
#
p = mdb.models['Model-1'].parts['Part-1']
cell1, cell2, cell3, cell4 = p.cells[0:0], p.cells[0:0], p.cells[0:0], p.cells[0:0]
for inum in range(16):
    tpt = (keypoints[inum][0]-width/2.0, keypoints[inum][1]-thickness/2.0, keypoints[inum][2]-height/2.0)
    if inum//4 == 0:
        cell1 += p.cells.findAt(((tpt), ))
    elif inum//4 == 1:
        cell2 += p.cells.findAt(((tpt), ))
    elif inum // 4 == 2:
        cell3 += p.cells.findAt(((tpt), ))
    else:
        cell4 += p.cells.findAt(((tpt), ))
p.Set(cells=cell1, name='Set-M-2')
p.Set(cells=cell2, name='Set-M-3')
p.Set(cells=cell3, name='Set-M-4')
p.Set(cells=cell4, name='Set-M-5')
#
p = mdb.models['Model-1'].parts['Part-1']
cell1 = p.cells[0:0]
for icell in p.cells:
    if (icell not in p.sets['Set-M-2'].cells and icell not in p.sets['Set-M-3'].cells and
        icell not in p.sets['Set-M-4'].cells and icell not in p.sets['Set-M-5'].cells):
        cell1 += p.cells[icell.index:icell.index+1]
p.Set(cells=cell1, name='Set-M-1')
volume1 = p.getMassProperties(regions=p.sets['Set-M-1'].cells)['volume']
#
p = mdb.models['Model-1'].parts['Part-1']
dic = p.getMassProperties( )
volume = dic['volume']
#
print (f'The volume fraction of yarns is: {1.0 - volume1/volume}')

#----------------------------------------------------------------------------------------------
#
mdb.saveAs(pathName=cae_name)