# -*- coding: mbcs -*-
#
import subprocess
from abaqus import *
from abaqusConstants import *
from caeModules import *
from driverUtils import executeOnCaeStartup
import numpy as np
#
executeOnCaeStartup()
Mdb()
mdb_1 = mdb.models['Model-1']

#--------------------------------------------------------------------------------
#
satin_num = 2 # 2 for plain and 3 for twill
path_name = f'woven{satin_num}_composites_fem_rve.cae'
if satin_num == 2:
    tmp_num, t_num, s_num = satin_num, 1, 4
else:
    tmp_num = satin_num + 1
    t_num, s_num = 1, 8
yarn_w, yarn_h, yarn_sec1, yarn_sec2, extra_t = 2.0, 0.6, 1.8, 0.4, 0.04   # 2.2 for twill, 2.29 for plain
rve_t = yarn_h + yarn_sec2 + extra_t/s_num
rve_size = np.array([tmp_num*yarn_w + extra_t, rve_t, tmp_num*yarn_w + extra_t])

#--------------------------------------------------------------------------------
#
list_axis1 = []
x = 0
while (x <= (satin_num - 1) * yarn_w):
    if x < 0.5 * yarn_w:
        y = yarn_h / 2.0 * np.sin(np.pi * x / yarn_w)
        list_axis1.append((x, y))
        x = x + 0.01 * yarn_w
    elif x < (satin_num - 1.5) * yarn_w:
        y = yarn_h / 2.0
        list_axis1.append((x, y))
        x = x + 1.0 * yarn_w
    else:
        y = yarn_h / 2.0 * np.sin(np.pi * (x - (satin_num - 2.0) * yarn_w) / yarn_w)
        list_axis1.append((x, y))
        x = x + 0.01 * yarn_w
#
len_list_axis1 = len(list_axis1)
for i in range(len_list_axis1):
    list_axis1.append((list_axis1[i][0] + (satin_num - 1) * yarn_w, - list_axis1[i][1]))
#
len_list_axis1 = satin_num * len(list_axis1)
for i in range(len_list_axis1):
    list_axis1.append((list_axis1[i][0] + 2.0 * (satin_num - 1) * yarn_w, list_axis1[i][1]))
#
s1 = mdb_1.ConstrainedSketch(name='__sweep1__', sheetSize=10.0)
g, v, d, c = s1.geometry, s1.vertices, s1.dimensions, s1.constraints
s1.setPrimaryObject(option=STANDALONE)
s1.Spline(points = list_axis1)

#--------------------------------------------------------------------------------
#
t = np.arange(0, 1.001, 0.001)
x_values = (yarn_sec1 / 2.0) * np.cos(2 * np.pi * t)
y_values = (yarn_sec2 / 2.0) * np.sin(2 * np.pi * t)
list_sec = list(zip(y_values, x_values))
#
eta = 1.2
x_values = (yarn_sec1 / 2.0) * np.cos(2 * np.pi * t)
y_values = np.zeros(len(x_values))
for i in range(len(x_values)):
    if t[i] <= 0.5:
        y_values[i] = (yarn_sec2 / 2.0) * (np.sin(2 * np.pi * t[i]))**eta
    else:
        y_values[i] = -(yarn_sec2 / 2.0) * (-np.sin(2 * np.pi * t[i]))**eta

list_sec = list(zip(y_values, x_values))

#--------------------------------------------------------------------------------
#
s = mdb_1.ConstrainedSketch(name='__profile__', sheetSize=10.0,
    transform=(0.6, -0.8, 0.0, -0.0, 0.0, 1.0, -0.8, -0.6, -0.0, 0.0, 0.0, 0.0))
g, v, d, c = s.geometry, s.vertices, s.dimensions, s.constraints
s.setPrimaryObject(option=SUPERIMPOSE)
s.ConstructionLine(point1=(-5.0, 0.0), point2=(5.0, 0.0))
s.ConstructionLine(point1=(0.0, -5.0), point2=(0.0, 5.0))
s.setPrimaryObject(option=STANDALONE)
s.Spline(points=list_sec)
#
p = mdb_1.Part(name='Part-1', dimensionality=THREE_D, type=DEFORMABLE_BODY)
p.BaseSolidSweep(sketch=s, path=s1)
s.unsetPrimaryObject()
s1.unsetPrimaryObject()
del mdb_1.sketches['__profile__']
del mdb_1.sketches['__sweep1__']

#--------------------------------------------------------------------------------
#
a = mdb_1.rootAssembly
p = mdb_1.parts['Part-1']
ins_list_1 = ()
for i in range(tmp_num * 3):
    ins_name = f'Part-1-{i+1}'
    a.Instance(name=ins_name, part=p, dependent=OFF)
    a.translate(instanceList=(ins_name, ), vector=(yarn_w * (i % tmp_num), 0.0, yarn_w * i))
    ins_list_1 = ins_list_1 + ((a.instances[ins_name], ))
a.InstanceFromBooleanMerge(name='Part-T', instances=ins_list_1, originalInstances=DELETE, domain=GEOMETRY)
a.deleteFeatures(('Part-T-1', ))
mdb_1.parts.changeKey(fromName='Part-T', toName='Part-2')
#
ins_list_2 = ()
for i in range(tmp_num * 3):
    ins_name = f'Part-1-{i+1}'
    a.Instance(name=ins_name, part=p, dependent=OFF)
    a.rotate(instanceList=(ins_name, ), axisPoint=(0.0, 0.0, 0.0), axisDirection=(0.0, -1.0, 0.0), angle=90.0)
    a.translate(instanceList=(ins_name, ), vector=(yarn_w * (satin_num - 0.5), 0.0, - yarn_w * (satin_num - 1.5)))
    a.translate(instanceList=(ins_name, ), vector=(yarn_w * i, 0.0, yarn_w * (i % tmp_num)))
    ins_list_2 = ins_list_2 + ((a.instances[ins_name], ))

a.InstanceFromBooleanMerge(name='Part-T', instances=ins_list_2, originalInstances=DELETE, domain=GEOMETRY)
a.deleteFeatures(('Part-T-1', ))
mdb_1.parts.changeKey(fromName='Part-T', toName='Part-3')
#
a = mdb_1.rootAssembly
p = mdb_1.parts['Part-2']
a.Instance(name='Part-2-1', part=p, dependent=ON)
p = mdb_1.parts['Part-3']
a.Instance(name='Part-3-1', part=p, dependent=ON)
a.translate(instanceList=('Part-2-1', 'Part-3-1', ), vector=(-yarn_w * (satin_num) * 2.0 + 0.5 * yarn_w,
    0.0, -yarn_w * (satin_num) * 2.0))

#--------------------------------------------------------------------------------
#
s = mdb_1.ConstrainedSketch(name='__profile__', sheetSize=200.0)
g, v, d, c = s.geometry, s.vertices, s.dimensions, s.constraints
s.setPrimaryObject(option=STANDALONE)
s.rectangle(point1=(0.0, 0.0), point2=(tmp_num*yarn_w, rve_t))
p = mdb_1.Part(name='Part-4', dimensionality=THREE_D, type=DEFORMABLE_BODY)
p.BaseSolidExtrude(sketch=s, depth=tmp_num*yarn_w)
s.unsetPrimaryObject()
a.Instance(name='Part-4-1', part=p, dependent=OFF)
a.translate(instanceList=('Part-4-1', ), vector=(-tmp_num*yarn_w/2.0, -rve_t/2.0, -tmp_num*yarn_w/2.0))
#
a.InstanceFromBooleanCut(name='Part-5', instanceToBeCut=a.instances['Part-4-1'],
    cuttingInstances=(a.instances['Part-2-1'], a.instances['Part-3-1'], ), originalInstances=SUPPRESS)
a.resumeFeatures(('Part-2-1', 'Part-3-1', 'Part-4-1', ))
a.InstanceFromBooleanCut(name='Part-6', instanceToBeCut=a.instances['Part-2-1'],
    cuttingInstances=(a.instances['Part-4-1'], ), originalInstances=SUPPRESS)
a.resumeFeatures(('Part-2-1', 'Part-4-1', ))
a.InstanceFromBooleanCut(name='Part-7', instanceToBeCut=a.instances['Part-2-1'],
    cuttingInstances=(a.instances['Part-6-1'], ), originalInstances=DELETE)
a.InstanceFromBooleanCut(name='Part-8', instanceToBeCut=a.instances['Part-3-1'],
    cuttingInstances=(a.instances['Part-4-1'], ), originalInstances=SUPPRESS)
a.resumeFeatures(('Part-3-1', 'Part-4-1', ))
a.InstanceFromBooleanCut(name='Part-9', instanceToBeCut=a.instances['Part-3-1'],
    cuttingInstances=(a.instances['Part-8-1'], ), originalInstances=DELETE)
#
a.deleteFeatures(('Part-4-1', 'Part-5-1', 'Part-7-1', 'Part-9-1', ))
del mdb_1.parts['Part-1']
del mdb_1.parts['Part-2']
del mdb_1.parts['Part-3']
del mdb_1.parts['Part-4']
del mdb_1.parts['Part-5']
del mdb_1.parts['Part-6']
del mdb_1.parts['Part-8']
mdb_1.parts.changeKey(fromName='Part-7', toName='Part-2')
mdb_1.parts.changeKey(fromName='Part-9', toName='Part-3')

# --------------------------------------------------------------------------------
#
a = mdb_1.rootAssembly
s = mdb_1.ConstrainedSketch(name='__profile__', sheetSize=200.0)
g, v, d, c = s.geometry, s.vertices, s.dimensions, s.constraints
s.setPrimaryObject(option=STANDALONE)
s.rectangle(point1=(0.0, 0.0), point2=(rve_size[0], rve_size[1]))
p = mdb_1.Part(name='Part-4', dimensionality=THREE_D, type=DEFORMABLE_BODY)
p.BaseSolidExtrude(sketch=s, depth=rve_size[2])
s.unsetPrimaryObject()
a.Instance(name='Part-4-1', part=p, dependent=OFF)
a.translate(instanceList=('Part-4-1', ), vector=(-rve_size[0]/2.0, -rve_size[1]/2.0, -rve_size[2]/2.0))
#
insts = ()
p = mdb_1.parts['Part-2']
a.Instance(name='Part-2-1', part=p, dependent=OFF)
p = mdb_1.parts['Part-3']
a.Instance(name='Part-3-1', part=p, dependent=OFF)
insts = insts + ((a.instances['Part-2-1'], a.instances['Part-3-1'], a.instances['Part-4-1'], ))
a.InstanceFromBooleanMerge(name='Part-5', instances=insts, keepIntersections=ON, originalInstances=DELETE, domain=GEOMETRY)
a.deleteFeatures(('Part-5-1', ))
del mdb_1.parts['Part-2']
del mdb_1.parts['Part-3']
del mdb_1.parts['Part-4']
mdb_1.parts.changeKey(fromName='Part-5', toName='Part-1')
p = mdb_1.parts['Part-1']
a.Instance(name='Part-1-1', part=p, dependent=OFF)
#
if t_num != 1:
    insts = ()
    p = mdb_1.parts['Part-1']
    for i in range(t_num):
        a.Instance(name=f'Part-1-{i+1}', part=p, dependent=OFF)
        a.translate(instanceList=(f'Part-1-{i+1}', ), vector=(0.0, -rve_size[1]*(t_num/2-0.5-i), 0.0))
        a.rotate(instanceList=(f'Part-1-{i+1}', ), axisPoint=(0.0, 0.0, 0.0), axisDirection=(0.0, 1.0, 0.0), angle=90.0*(i%2))
        insts = insts + ((a.instances[f'Part-1-{i+1}'], ))
    a.InstanceFromBooleanMerge(name='Part-2', instances=insts, keepIntersections=ON, originalInstances=DELETE, domain=GEOMETRY)
    a.deleteFeatures(('Part-2-1', ))
    del mdb_1.parts['Part-1']
    mdb_1.parts.changeKey(fromName='Part-2', toName='Part-1')
    p = mdb_1.parts['Part-1']
    a.Instance(name='Part-1-1', part=p, dependent=OFF)

#--------------------------------------------------------------------------------------------------
#
p = mdb.models['Model-1'].parts['Part-1']
selcellx, selcelly = p.cells[0:0], p.cells[0:0]
for icell in p.cells:
    num1, num2 = 0, 0
    faceid = icell.getFaces()
    cenpts = np.zeros([len(faceid), 3])
    for fid in range(len(faceid)):
        cenpts[fid,:] = p.faces[faceid[fid]-1].getCentroid()[0]
    coord = tmp_num*yarn_w / 2.0
    num1 += np.sum(cenpts[:,0] ==  coord)
    num1 += np.sum(cenpts[:,0] == -coord)
    num2 += np.sum(cenpts[:,2] ==  coord)
    num2 += np.sum(cenpts[:,2] == -coord)
    if num1 == 2:
        selcellx += p.cells[icell.index:icell.index+1]
    if num2 == 2:
        selcelly += p.cells[icell.index:icell.index+1]
p.Set(cells=selcellx, name='Set-M-2')
p.Set(cells=selcelly, name='Set-M-3')
volume2 = p.getMassProperties(regions=p.sets['Set-M-2'].cells)['volume']
volume3 = p.getMassProperties(regions=p.sets['Set-M-3'].cells)['volume']

p = mdb.models['Model-1'].parts['Part-1']
selcellz = p.cells[0:0]
for icell in p.cells:
    if icell not in p.sets['Set-M-2'].cells and icell not in p.sets['Set-M-3'].cells:
        selcellz += p.cells[icell.index:icell.index + 1]
p.Set(cells=selcellz, name='Set-M-1')
volume1 = p.getMassProperties(regions=p.sets['Set-M-1'].cells)['volume']

print (f'Volume fraction of yarns is: {1 - volume1/(volume1+volume2+volume3)}')

#--------------------------------------------------------------------------------
#
mdb.saveAs(pathName=path_name)

