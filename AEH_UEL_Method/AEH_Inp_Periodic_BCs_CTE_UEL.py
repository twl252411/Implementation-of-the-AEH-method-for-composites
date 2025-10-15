#
import numpy as np
from itertools import product

#----------------------------- Parameters ------------------------------
#
satin_num = 3 # 2 for plain and 3 for twill
job_name = f'Job_woven{satin_num}_AEH1_cte'
new_job_name = f'Job_woven{satin_num}_AEH1_cte'
if satin_num == 2:
    tmp_num, t_num, s_num = satin_num, 1, 4
else:
    tmp_num = satin_num + 1
    t_num, s_num = 1, 8
yarn_w, yarn_h, yarn_sec1, yarn_sec2, extra_t = 2.0, 0.6, 1.8, 0.4, 0.04   # 2.2 for twill, 2.29 for plain
rve_t = yarn_h + yarn_sec2 + extra_t/s_num
rve_size = np.array([tmp_num*yarn_w + extra_t, rve_t, tmp_num*yarn_w + extra_t])
xlenp, ylenp, zlenp = rve_size / 2.
xlenm, ylenm, zlenm = - rve_size / 2.

#----------------------------- Open the inp file ------------------------------
#
with open(f'{job_name}.inp', 'r') as f1:
	lines = f1.readlines()

#----------------------------- Modify Job name ------------------------------
#
lines[1] = f'** Job name: {new_job_name} Model name: Model-1\n'
#
#----------------------------- Node number and coordinates -----------------------------
#
line_str1, line_str2 = '*Node\n', '*Element, type=C3D4\n'
staid, endid = lines.index(line_str1), lines.index(line_str2)
ndnum = endid-staid-1
#
ndcord = np.zeros([ndnum,4])
for il in range(staid+1,endid):
	newline1 = lines[il].replace('\n', '').split(',')
	for inl in range(4):
		ndcord[il-staid-1,inl] = float(newline1[inl])
#
#----------------------------- Node on the surfaces -----------------------------
#
NdRS, NdLS, NdTS, NdDS, NdFS, NdBS = [], [], [], [], [], []
NdEdAB, NdEdBC, NdEdCD, NdEdDA, NdEdA1B1, NdEdB1C1,  = [], [], [], [], [], []
NdEdC1D1, NdEdD1A1, NdEdAA1, NdEdBB1, NdEdCC1, NdEdDD1 = [], [], [], [], [], []
NdVrt1, NdVrt2, NdVrt3, NdVrt4, NdVrt5, NdVrt6, NdVrt7, NdVrt8 = [], [], [], [], [], [], [], []
#
for ind in ndcord:
	if abs(ind[1]-xlenp)<1.0E-4 and abs(ind[2]-ylenm)>1.0E-4 and abs(ind[2]-ylenp)>1.0E-4 and abs(ind[3]-zlenm)>1.0E-4 and abs(ind[3]-zlenp)>1.0E-4:
		NdRS.append(int(ind[0]))
	if abs(ind[1]-xlenm)<1.0E-4 and abs(ind[2]-ylenm)>1.0E-4 and abs(ind[2]-ylenp)>1.0E-4 and abs(ind[3]-zlenm)>1.0E-4 and abs(ind[3]-zlenp)>1.0E-4:
		NdLS.append(int(ind[0]))
	if abs(ind[2]-ylenp)<1.0E-4 and abs(ind[1]-xlenm)>1.0E-4 and abs(ind[1]-xlenp)>1.0E-4 and abs(ind[3]-zlenm)>1.0E-4 and abs(ind[3]-zlenp)>1.0E-4:
		NdTS.append(int(ind[0]))
	if abs(ind[2]-ylenm)<1.0E-4 and abs(ind[1]-xlenm)>1.0E-4 and abs(ind[1]-xlenp)>1.0E-4 and abs(ind[3]-zlenm)>1.0E-4 and abs(ind[3]-zlenp)>1.0E-4:
		NdDS.append(int(ind[0]))
	if abs(ind[3]-zlenp)<1.0E-4 and abs(ind[2]-ylenm)>1.0E-4 and abs(ind[2]-ylenp)>1.0E-4 and abs(ind[1]-xlenm)>1.0E-4 and abs(ind[1]-xlenp)>1.0E-4:
		NdFS.append(int(ind[0]))
	if abs(ind[3]-zlenm)<1.0E-4 and abs(ind[2]-ylenm)>1.0E-4 and abs(ind[2]-ylenp)>1.0E-4 and abs(ind[1]-xlenm)>1.0E-4 and abs(ind[1]-xlenp)>1.0E-4:
		NdBS.append(int(ind[0]))
	#
	if abs(ind[2]-ylenp)<1.0E-4 and abs(ind[3]-zlenp)<1.0E-4 and abs(ind[1]-xlenp)>1.0E-4 and abs(ind[1]-xlenm)>1.0E-4:
		NdEdAB.append(int(ind[0]))
	if abs(ind[2]-ylenp)<1.0E-4 and abs(ind[1]-xlenp)<1.0E-4 and abs(ind[3]-zlenp)>1.0E-4 and abs(ind[3]-zlenm)>1.0E-4:
		NdEdBC.append(int(ind[0]))
	if abs(ind[2]-ylenp)<1.0E-4 and abs(ind[3]-zlenm)<1.0E-4 and abs(ind[1]-xlenp)>1.0E-4 and abs(ind[1]-xlenm)>1.0E-4:
		NdEdCD.append(int(ind[0]))
	if abs(ind[2]-ylenp)<1.0E-4 and abs(ind[1]-xlenm)<1.0E-4 and abs(ind[3]-zlenp)>1.0E-4 and abs(ind[3]-zlenm)>1.0E-4:
		NdEdDA.append(int(ind[0]))
	#
	if abs(ind[2]-ylenm)<1.0E-4 and abs(ind[3]-zlenp)<1.0E-4 and abs(ind[1]-xlenp)>1.0E-4 and abs(ind[1]-xlenm)>1.0E-4:
		NdEdA1B1.append(int(ind[0]))
	if abs(ind[2]-ylenm)<1.0E-4 and abs(ind[1]-xlenp)<1.0E-4 and abs(ind[3]-zlenp)>1.0E-4 and abs(ind[3]-zlenm)>1.0E-4:
		NdEdB1C1.append(int(ind[0]))
	if abs(ind[2]-ylenm)<1.0E-4 and abs(ind[3]-zlenm)<1.0E-4 and abs(ind[1]-xlenp)>1.0E-4 and abs(ind[1]-xlenm)>1.0E-4:
		NdEdC1D1.append(int(ind[0]))
	if abs(ind[2]-ylenm)<1.0E-4 and abs(ind[1]-xlenm)<1.0E-4 and abs(ind[3]-xlenp)>1.0E-4 and abs(ind[3]-zlenm)>1.0E-4:
		NdEdD1A1.append(int(ind[0]))
	#
	if abs(ind[3]-zlenp)<1.0E-4 and abs(ind[1]-xlenm)<1.0E-4 and abs(ind[2]-ylenp)>1.0E-4 and abs(ind[2]-ylenm)>1.0E-4:
		NdEdAA1.append(int(ind[0]))
	if abs(ind[3]-zlenp)<1.0E-4 and abs(ind[1]-xlenp)<1.0E-4 and abs(ind[2]-ylenp)>1.0E-4 and abs(ind[2]-ylenm)>1.0E-4:
		NdEdBB1.append(int(ind[0]))
	if abs(ind[3]-zlenm)<1.0E-4 and abs(ind[1]-xlenp)<1.0E-4 and abs(ind[2]-ylenp)>1.0E-4 and abs(ind[2]-ylenm)>1.0E-4:
		NdEdCC1.append(int(ind[0]))
	if abs(ind[3]-zlenm)<1.0E-4 and abs(ind[1]-xlenm)<1.0E-4 and abs(ind[2]-ylenp)>1.0E-4 and abs(ind[2]-ylenm)>1.0E-4:
		NdEdDD1.append(int(ind[0]))
	#
	if abs(ind[1]-xlenm)<1.0E-4 and abs(ind[2]-ylenp)<1.0E-4 and abs(ind[3]-zlenp)<1.0E-4:
		NdVrt1.append(int(ind[0]))
	if abs(ind[1]-xlenp)<1.0E-4 and abs(ind[2]-ylenp)<1.0E-4 and abs(ind[3]-zlenp)<1.0E-4:
		NdVrt2.append(int(ind[0]))
	if abs(ind[1]-xlenp)<1.0E-4 and abs(ind[2]-ylenp)<1.0E-4 and abs(ind[3]-zlenm)<1.0E-4:
		NdVrt3.append(int(ind[0]))
	if abs(ind[1]-xlenm)<1.0E-4 and abs(ind[2]-ylenp)<1.0E-4 and abs(ind[3]-zlenm)<1.0E-4:
		NdVrt4.append(int(ind[0]))
	if abs(ind[1]-xlenm)<1.0E-4 and abs(ind[2]-ylenm)<1.0E-4 and abs(ind[3]-zlenp)<1.0E-4:
		NdVrt5.append(int(ind[0]))
	if abs(ind[1]-xlenp)<1.0E-4 and abs(ind[2]-ylenm)<1.0E-4 and abs(ind[3]-zlenp)<1.0E-4:
		NdVrt6.append(int(ind[0]))
	if abs(ind[1]-xlenp)<1.0E-4 and abs(ind[2]-ylenm)<1.0E-4 and abs(ind[3]-zlenm)<1.0E-4:
		NdVrt7.append(int(ind[0]))
	if abs(ind[1]-xlenm)<1.0E-4 and abs(ind[2]-ylenm)<1.0E-4 and abs(ind[3]-zlenm)<1.0E-4:
		NdVrt8.append(int(ind[0]))
#
#----------------------------- Reference points -----------------------------
#
addlns1 = []
#
addlns1.append('*Node\n')
addlns1.append('      1,   '+str(xlenp*1.1)+',           0.,           0.\n')
addlns1.append('*Node\n')
addlns1.append('      2,           0.,   '+str(ylenp*1.1)+',           0.\n')
addlns1.append('*Node\n')
addlns1.append('      3,           0.,           0.,   '+str(zlenp*1.1)+'\n')
#
#----------------------------- Sets of Periodic BCs -----------------------------
#
addlnsP17 = []
addlnsP17.append('*Nset, nset=Set-RP-1\n')
addlnsP17.append(' 1,\n')
addlnsP17.append('*Nset, nset=Set-RP-2\n')
addlnsP17.append(' 2,\n')
addlnsP17.append('*Nset, nset=Set-RP-3\n')
addlnsP17.append(' 3,\n')
#
addlnsS1, addlnsS2, addlnsS15, addlnsS16, addlnsS18, addlnsS19 = [], [], [], [], [], []
ssetnum1, ssetnum2, ssetnum3 = 0, 0, 0
for ind in NdRS:
	ssetnum1 += 1
	addlnsS18.append('*Nset, nset=Set-RightSurf-'+str(ssetnum1)+', instance=Part-1-1\n')
	addlnsS18.append(' '+str(ind)+',\n')
	for jnd in NdLS:
		if abs(ndcord[ind-1,2]-ndcord[jnd-1,2])<1.E-4 and abs(ndcord[ind-1,3]-ndcord[jnd-1,3])<1.E-4:
			addlnsS16.append('*Nset, nset=Set-LeftSurf-'+str(ssetnum1)+', instance=Part-1-1\n')
			addlnsS16.append(' '+str(jnd)+',\n')
			break
for ind in NdTS:
	ssetnum2 += 1
	addlnsS19.append('*Nset, nset=Set-TopSurf-'+str(ssetnum2)+', instance=Part-1-1\n')
	addlnsS19.append(' '+str(ind)+',\n')
	for jnd in NdDS:
		if abs(ndcord[ind-1,1]-ndcord[jnd-1,1])<1.E-4 and abs(ndcord[ind-1,3]-ndcord[jnd-1,3])<1.E-4:
			addlnsS2.append('*Nset, nset=Set-DownSurf-'+str(ssetnum2)+', instance=Part-1-1\n')
			addlnsS2.append(' '+str(jnd)+',\n')
			break
for ind in NdFS:
	ssetnum3 += 1
	addlnsS15.append('*Nset, nset=Set-FrontSurf-'+str(ssetnum3)+', instance=Part-1-1\n')
	addlnsS15.append(' '+str(ind)+',\n')
	for jnd in NdBS:
		if abs(ndcord[ind-1,2]-ndcord[jnd-1,2])<1.E-4 and abs(ndcord[ind-1,1]-ndcord[jnd-1,1])<1.E-4:
			addlnsS1.append('*Nset, nset=Set-BackSurf-'+str(ssetnum3)+', instance=Part-1-1\n')
			addlnsS1.append(' '+str(jnd)+',\n')
			break
#
addlnsE3, addlnsE4, addlnsE5, addlnsE6, addlnsE7, addlnsE8 = [], [], [], [], [], []
addlnsE9, addlnsE10, addlnsE11, addlnsE12, addlnsE13, addlnsE14 = [], [], [], [], [], []
esetnum1, esetnum2, esetnum3 = 0, 0, 0
for ind in NdEdAB:
	esetnum1 += 1
	addlnsE5.append('*Nset, nset=Set-EdgeAB-'+str(esetnum1)+', instance=Part-1-1\n')
	addlnsE5.append(' '+str(ind)+',\n')
	for jnd in NdEdCD:
		if abs(ndcord[ind-1,1]-ndcord[jnd-1,1])<1.E-4:
			addlnsE11.append('*Nset, nset=Set-EdgeCD-'+str(esetnum1)+', instance=Part-1-1\n')
			addlnsE11.append(' '+str(jnd)+',\n')
			break
	for knd in NdEdC1D1:
		if abs(ndcord[ind-1,1]-ndcord[knd-1,1])<1.E-4:
			addlnsE9.append('*Nset, nset=Set-EdgeC1D1-'+str(esetnum1)+', instance=Part-1-1\n')
			addlnsE9.append(' '+str(knd)+',\n')
			break
	for lnd in NdEdA1B1:
		if abs(ndcord[ind-1,1]-ndcord[lnd-1,1])<1.E-4:
			addlnsE3.append('*Nset, nset=Set-EdgeA1B1-'+str(esetnum1)+', instance=Part-1-1\n')
			addlnsE3.append(' '+str(lnd)+',\n')
			break
#
for ind in NdEdBC:
	esetnum2 += 1
	addlnsE8.append('*Nset, nset=Set-EdgeBC-'+str(esetnum2)+', instance=Part-1-1\n')
	addlnsE8.append(' '+str(ind)+',\n')
	for jnd in NdEdDA:
		if abs(ndcord[ind-1,3]-ndcord[jnd-1,3])<1.E-4:
			addlnsE13.append('*Nset, nset=Set-EdgeDA-'+str(esetnum2)+', instance=Part-1-1\n')
			addlnsE13.append(' '+str(jnd)+',\n')
			break
	for knd in NdEdB1C1:
		if abs(ndcord[ind-1,3]-ndcord[knd-1,3])<1.E-4:
			addlnsE6.append('*Nset, nset=Set-EdgeB1C1-'+str(esetnum2)+', instance=Part-1-1\n')
			addlnsE6.append(' '+str(knd)+',\n')
			break
	for lnd in NdEdD1A1:
		if abs(ndcord[ind-1,3]-ndcord[lnd-1,3])<1.E-4:
			addlnsE12.append('*Nset, nset=Set-EdgeD1A1-'+str(esetnum2)+', instance=Part-1-1\n')
			addlnsE12.append(' '+str(lnd)+',\n')
			break
#
for ind in NdEdBB1:
	esetnum3 += 1
	addlnsE7.append('*Nset, nset=Set-EdgeBB1-'+str(esetnum3)+', instance=Part-1-1\n')
	addlnsE7.append(' '+str(ind)+',\n')
	for jnd in NdEdAA1:
		if abs(ndcord[ind-1,2]-ndcord[jnd-1,2])<1.E-4:
			addlnsE4.append('*Nset, nset=Set-EdgeAA1-'+str(esetnum3)+', instance=Part-1-1\n')
			addlnsE4.append(' '+str(jnd)+',\n')
			break
	for knd in NdEdCC1:
		if abs(ndcord[ind-1,2]-ndcord[knd-1,2])<1.E-4:
			addlnsE10.append('*Nset, nset=Set-EdgeCC1-'+str(esetnum3)+', instance=Part-1-1\n')
			addlnsE10.append(' '+str(knd)+',\n')
			break
	for lnd in NdEdDD1:
		if abs(ndcord[ind-1,2]-ndcord[lnd-1,2])<1.E-4:
			addlnsE14.append('*Nset, nset=Set-EdgeDD1-'+str(esetnum3)+', instance=Part-1-1\n')
			addlnsE14.append(' '+str(lnd)+',\n')
			break
#
addlnsV20 = []
addlnsV20.append('*Nset, nset=Set-V-1, instance=Part-1-1\n')
addlnsV20.append(' '+str(NdVrt1[0])+',\n')
addlnsV20.append('*Nset, nset=Set-V-2, instance=Part-1-1\n')
addlnsV20.append(' '+str(NdVrt2[0])+',\n')
addlnsV20.append('*Nset, nset=Set-V-3, instance=Part-1-1\n')
addlnsV20.append(' '+str(NdVrt3[0])+',\n')
addlnsV20.append('*Nset, nset=Set-V-4, instance=Part-1-1\n')
addlnsV20.append(' '+str(NdVrt4[0])+',\n')
addlnsV20.append('*Nset, nset=Set-V-5, instance=Part-1-1\n')
addlnsV20.append(' '+str(NdVrt5[0])+',\n')
addlnsV20.append('*Nset, nset=Set-V-6, instance=Part-1-1\n')
addlnsV20.append(' '+str(NdVrt6[0])+',\n')
addlnsV20.append('*Nset, nset=Set-V-7, instance=Part-1-1\n')
addlnsV20.append(' '+str(NdVrt7[0])+',\n')
addlnsV20.append('*Nset, nset=Set-V-8, instance=Part-1-1\n')
addlnsV20.append(' '+str(NdVrt8[0])+',\n')
#
#-----------------------------  ------------------------------
#
addlns1 = addlns1 + addlnsS1 + addlnsS2 + addlnsE3 + addlnsE4 + addlnsE5 + addlnsE6 + addlnsE7 + addlnsE8
addlns1 = addlns1 + addlnsE9 + addlnsE10 + addlnsE11 + addlnsE12 + addlnsE13 + addlnsE14
addlns1 = addlns1 + addlnsS15 + addlnsS16 + addlnsP17 + addlnsS18 + addlnsS19 + addlnsV20
#
#-----------------------------  ------------------------------
#
addlns2 = []
#
for icrd in range(3):
	if icrd == 0:
		di = 'X'
	elif icrd == 1:
		di = 'Y'
	else:
		di = 'Z'
	for inum in range(len(NdEdA1B1)):
		addlns2.append('** Constraint: Constraint-Edge-A1B1-C1D1-'+di+'-'+str(inum+1)+'\n')
		addlns2.append('*Equation\n')
		addlns2.append('3\n')
		addlns2.append('Set-EdgeA1B1-'+str(inum+1)+', '+str(icrd+1)+', 1.\n')
		addlns2.append('Set-EdgeC1D1-'+str(inum+1)+', '+str(icrd+1)+', -1.\n')
		addlns2.append('Set-RP-3, '+str(icrd+1)+', -1.\n')
#
for icrd in range(3):
	if icrd == 0:
		di = 'X'
	elif icrd == 1:
		di = 'Y'
	else:
		di = 'Z'
	for inum in range(len(NdEdAA1)):
		addlns2.append('** Constraint: Constraint-Edge-AA1-DD1-'+di+'-'+str(inum+1)+'\n')
		addlns2.append('*Equation\n')
		addlns2.append('3\n')
		addlns2.append('Set-EdgeAA1-'+str(inum+1)+', '+str(icrd+1)+', 1.\n')
		addlns2.append('Set-EdgeDD1-'+str(inum+1)+', '+str(icrd+1)+', -1.\n')
		addlns2.append('Set-RP-3, '+str(icrd+1)+', -1.\n')
#
for icrd in range(3):
	if icrd == 0:
		di = 'X'
	elif icrd == 1:
		di = 'Y'
	else:
		di = 'Z'
	for inum in range(len(NdEdAB)):
		addlns2.append('** Constraint: Constraint-Edge-AB-CD-'+di+'-'+str(inum+1)+'\n')
		addlns2.append('*Equation\n')
		addlns2.append('3\n')
		addlns2.append('Set-EdgeAB-'+str(inum+1)+', '+str(icrd+1)+', 1.\n')
		addlns2.append('Set-EdgeCD-'+str(inum+1)+', '+str(icrd+1)+', -1.\n')
		addlns2.append('Set-RP-3, '+str(icrd+1)+', -1.\n')
#
for icrd in range(3):
	if icrd == 0:
		di = 'X'
	elif icrd == 1:
		di = 'Y'
	else:
		di = 'Z'
	for inum in range(len(NdEdB1C1)):
		addlns2.append('** Constraint: Constraint-Edge-B1C1-D1A1-'+di+'-'+str(inum+1)+'\n')
		addlns2.append('*Equation\n')
		addlns2.append('3\n')
		addlns2.append('Set-EdgeB1C1-'+str(inum+1)+', '+str(icrd+1)+', 1.\n')
		addlns2.append('Set-EdgeD1A1-'+str(inum+1)+', '+str(icrd+1)+', -1.\n')
		addlns2.append('Set-RP-1, '+str(icrd+1)+', -1.\n')
#
for icrd in range(3):
	if icrd == 0:
		di = 'X'
	elif icrd == 1:
		di = 'Y'
	else:
		di = 'Z'
	for inum in range(len(NdEdBB1)):
		addlns2.append('** Constraint: Constraint-Edge-BB1-AA1-'+di+'-'+str(inum+1)+'\n')
		addlns2.append('*Equation\n')
		addlns2.append('3\n')
		addlns2.append('Set-EdgeBB1-'+str(inum+1)+', '+str(icrd+1)+', 1.\n')
		addlns2.append('Set-EdgeAA1-'+str(inum+1)+', '+str(icrd+1)+', -1.\n')
		addlns2.append('Set-RP-1, '+str(icrd+1)+', -1.\n')
#
for icrd in range(3):
	if icrd == 0:
		di = 'X'
	elif icrd == 1:
		di = 'Y'
	else:
		di = 'Z'
	for inum in range(len(NdEdBC)):
		addlns2.append('** Constraint: Constraint-Edge-BC-DA-'+di+'-'+str(inum+1)+'\n')
		addlns2.append('*Equation\n')
		addlns2.append('3\n')
		addlns2.append('Set-EdgeBC-'+str(inum+1)+', '+str(icrd+1)+', 1.\n')
		addlns2.append('Set-EdgeDA-'+str(inum+1)+', '+str(icrd+1)+', -1.\n')
		addlns2.append('Set-RP-1, '+str(icrd+1)+', -1.\n')
#
for icrd in range(3):
	if icrd == 0:
		di = 'X'
	elif icrd == 1:
		di = 'Y'
	else:
		di = 'Z'
	for inum in range(len(NdEdCC1)):
		addlns2.append('** Constraint: Constraint-Edge-CC1-DD1-'+di+'-'+str(inum+1)+'\n')
		addlns2.append('*Equation\n')
		addlns2.append('3\n')
		addlns2.append('Set-EdgeCC1-'+str(inum+1)+', '+str(icrd+1)+', 1.\n')
		addlns2.append('Set-EdgeDD1-'+str(inum+1)+', '+str(icrd+1)+', -1.\n')
		addlns2.append('Set-RP-1, '+str(icrd+1)+', -1.\n')
#
for icrd in range(3):
	if icrd == 0:
		di = 'X'
	elif icrd == 1:
		di = 'Y'
	else:
		di = 'Z'
	for inum in range(len(NdEdCD)):
		addlns2.append('** Constraint: Constraint-Edge-CD-C1D1-'+di+'-'+str(inum+1)+'\n')
		addlns2.append('*Equation\n')
		addlns2.append('3\n')
		addlns2.append('Set-EdgeCD-'+str(inum+1)+', '+str(icrd+1)+', 1.\n')
		addlns2.append('Set-EdgeC1D1-'+str(inum+1)+', '+str(icrd+1)+', -1.\n')
		addlns2.append('Set-RP-2, '+str(icrd+1)+', -1.\n')
#
for icrd in range(3):
	if icrd == 0:
		di = 'X'
	elif icrd == 1:
		di = 'Y'
	else:
		di = 'Z'
	for inum in range(len(NdEdDA)):
		addlns2.append('** Constraint: Constraint-Edge-DA-D1A1-'+di+'-'+str(inum+1)+'\n')
		addlns2.append('*Equation\n')
		addlns2.append('3\n')
		addlns2.append('Set-EdgeDA-'+str(inum+1)+', '+str(icrd+1)+', 1.\n')
		addlns2.append('Set-EdgeD1A1-'+str(inum+1)+', '+str(icrd+1)+', -1.\n')
		addlns2.append('Set-RP-2, '+str(icrd+1)+', -1.\n')
#
for icrd in range(3):
	if icrd == 0:
		di = 'X'
	elif icrd == 1:
		di = 'Y'
	else:
		di = 'Z'
	for inum in range(len(NdFS)):
		addlns2.append('** Constraint: Constraint-Surf-Front-Back-'+di+'-'+str(inum+1)+'\n')
		addlns2.append('*Equation\n')
		addlns2.append('3\n')
		addlns2.append('Set-FrontSurf-'+str(inum+1)+', '+str(icrd+1)+', 1.\n')
		addlns2.append('Set-BackSurf-'+str(inum+1)+', '+str(icrd+1)+', -1.\n')
		addlns2.append('Set-RP-3, '+str(icrd+1)+', -1.\n')
#
for icrd in range(3):
	if icrd == 0:
		di = 'X'
	elif icrd == 1:
		di = 'Y'
	else:
		di = 'Z'
	for inum in range(len(NdRS)):
		addlns2.append('** Constraint: Constraint-Surf-Right-Left-'+di+'-'+str(inum+1)+'\n')
		addlns2.append('*Equation\n')
		addlns2.append('3\n')
		addlns2.append('Set-RightSurf-'+str(inum+1)+', '+str(icrd+1)+', 1.\n')
		addlns2.append('Set-LeftSurf-'+str(inum+1)+', '+str(icrd+1)+', -1.\n')
		addlns2.append('Set-RP-1, '+str(icrd+1)+', -1.\n')
#
for icrd in range(3):
	if icrd == 0:
		di = 'X'
	elif icrd == 1:
		di = 'Y'
	else:
		di = 'Z'
	for inum in range(len(NdTS)):
		addlns2.append('** Constraint: Constraint-Surf-Top-Down-'+di+'-'+str(inum+1)+'\n')
		addlns2.append('*Equation\n')
		addlns2.append('3\n')
		addlns2.append('Set-TopSurf-'+str(inum+1)+', '+str(icrd+1)+', 1.\n')
		addlns2.append('Set-DownSurf-'+str(inum+1)+', '+str(icrd+1)+', -1.\n')
		addlns2.append('Set-RP-2, '+str(icrd+1)+', -1.\n')
#
for icrd in range(3):
	if icrd == 0:
		di = 'X'
	elif icrd == 1:
		di = 'Y'
	else:
		di = 'Z'
	#
	addlns2.append('** Constraint: Constraint-Vert-'+di+'-1\n')
	addlns2.append('*Equation\n')
	addlns2.append('3\n')
	addlns2.append('Set-V-1, '+str(icrd+1)+', 1.\n')
	addlns2.append('Set-V-4, '+str(icrd+1)+', -1.\n')
	addlns2.append('Set-RP-3, '+str(icrd+1)+', -1.\n')
	#
	addlns2.append('** Constraint: Constraint-Vert-'+di+'-2\n')
	addlns2.append('*Equation\n')
	addlns2.append('3\n')
	addlns2.append('Set-V-3, '+str(icrd+1)+', 1.\n')
	addlns2.append('Set-V-4, '+str(icrd+1)+', -1.\n')
	addlns2.append('Set-RP-1, '+str(icrd+1)+', -1.\n')
	#
	addlns2.append('** Constraint: Constraint-Vert-'+di+'-3\n')
	addlns2.append('*Equation\n')
	addlns2.append('3\n')
	addlns2.append('Set-V-2, '+str(icrd+1)+', 1.\n')
	addlns2.append('Set-V-3, '+str(icrd+1)+', -1.\n')
	addlns2.append('Set-RP-3, '+str(icrd+1)+', -1.\n')
	#
	addlns2.append('** Constraint: Constraint-Vert-'+di+'-4\n')
	addlns2.append('*Equation\n')
	addlns2.append('3\n')
	addlns2.append('Set-V-6, '+str(icrd+1)+', 1.\n')
	addlns2.append('Set-V-5, '+str(icrd+1)+', -1.\n')
	addlns2.append('Set-RP-1, '+str(icrd+1)+', -1.\n')
	#
	addlns2.append('** Constraint: Constraint-Vert-'+di+'-5\n')
	addlns2.append('*Equation\n')
	addlns2.append('3\n')
	addlns2.append('Set-V-5, '+str(icrd+1)+', 1.\n')
	addlns2.append('Set-V-8, '+str(icrd+1)+', -1.\n')
	addlns2.append('Set-RP-3, '+str(icrd+1)+', -1.\n')
	#
	addlns2.append('** Constraint: Constraint-Vert-'+di+'-6\n')
	addlns2.append('*Equation\n')
	addlns2.append('3\n')
	addlns2.append('Set-V-7, '+str(icrd+1)+', 1.\n')
	addlns2.append('Set-V-8, '+str(icrd+1)+', -1.\n')
	addlns2.append('Set-RP-1, '+str(icrd+1)+', -1.\n')
	#
	addlns2.append('** Constraint: Constraint-Vert-'+di+'-7\n')
	addlns2.append('*Equation\n')
	addlns2.append('3\n')
	addlns2.append('Set-V-4, '+str(icrd+1)+', 1.\n')
	addlns2.append('Set-V-8, '+str(icrd+1)+', -1.\n')
	addlns2.append('Set-RP-2, '+str(icrd+1)+', -1.\n')
#
#----------------------------- Combine the file ------------------------------
#
staid1 = lines.index('*End Instance\n') + 2
lines = lines[:staid1] + addlns1 + addlns2 + lines[staid1:]
#
#----------------------------- Initial BCs ------------------------------
#
addlns3 = []
addlns3.append('** \n')
addlns3.append('** BOUNDARY CONDITIONS\n')
addlns3.append('** \n')
addlns3.append('** Name: BC-4 Type: Displacement/Rotation\n')
addlns3.append('*Boundary\n')
addlns3.append('Set-V-8, 1, 1\n')
addlns3.append('Set-V-8, 2, 2\n')
addlns3.append('Set-V-8, 3, 3\n')
#
#----------------------------- PBCs -----------------------------
#
addlns4 = []
addlns4.append('** ----------------------------------------------------------------\n')
addlns4.append('** \n')
addlns4.append('** STEP: Step-1\n')
addlns4.append('** \n')
addlns4.append('*Step, name=Step-1\n')
addlns4.append('*Static\n')
addlns4.append('** \n')
addlns4.append('** BOUNDARY CONDITIONS\n')
addlns4.append('** \n')
#
addlns4.append('** Name: BC-1 Type: Displacement/Rotation\n')
addlns4.append('*Boundary\n')
addlns4.append('Set-RP-1, 1, 1\n')
addlns4.append('Set-RP-1, 2, 2\n')
addlns4.append('Set-RP-1, 3, 3\n')
addlns4.append('** Name: BC-2 Type: Displacement/Rotation\n')
addlns4.append('*Boundary\n')
addlns4.append('Set-RP-2, 1, 1\n')
addlns4.append('Set-RP-2, 2, 2\n')
addlns4.append('Set-RP-2, 3, 3\n')
addlns4.append('** Name: BC-3 Type: Displacement/Rotation\n')
addlns4.append('*Boundary\n')
addlns4.append('Set-RP-3, 1, 1\n')
addlns4.append('Set-RP-3, 2, 2\n')
addlns4.append('Set-RP-3, 3, 3\n')
#
addlns4.append('** \n')
addlns4.append('** OUTPUT REQUESTS\n')
addlns4.append('** \n')
addlns4.append('** \n')
addlns4.append('** FIELD OUTPUT: F-Output-1\n')
addlns4.append('** \n')
addlns4.append('*Output, field\n')
addlns4.append('*Node Output\n')
addlns4.append('RF, U\n')
addlns4.append('*Element Output, directions=YES\n')
addlns4.append('E, EVOL, IVOL, S\n')
addlns4.append('** \n')
addlns4.append('** HISTORY OUTPUT: H-Output-1\n')
addlns4.append('** \n')
addlns4.append('*Output, history, variable=PRESELECT\n')
addlns4.append('*End Step\n')
#
#----------------------------- Combine the file ------------------------------
#
staid2 = lines.index('** STEP: Step-1\n') - 2
lines = lines[0:staid2] + addlns3 + addlns4
#
#----------------------------- Save the file ------------------------------
#
with open(f'{new_job_name}_1.inp', mode='w') as f:
	f.writelines(lines)