'''transfer UV'''
batman = cmds.ls(sl=True)
twoface = batman[1:]
for i in range (len(twoface)):
        cmds.select (batman[0])
        cmds.select (twoface[i], add=True)
        cmds.transferAttributes ( uvs=1, spa=4)
        
        
'''write to file'''
#open animator file from GUI. Run script to drop file path and name in .txt
import maya.cmds as cmds
myFileObject=open('/drd/jobs/hf2/wip/depts/rig/users/elise.deglau/docs/writefolder/data1.txt', 'w')
flepath=cmds.file(q=1, l=1)
name = flepath[count]
myFileObject.writelines( name +'\n')
myFileObject.close()

#import file into new or loaded scene from the printed .txt file
import maya.cmds as cmds
import re
path_file = open('/drd/jobs/hf2/wip/depts/rig/users/elise.deglau/docs/writefolder/data1.txt')
text = path_file.read()
path_file.close()
hg=str(text)
shrt=hg.split('/')
wrd=shrt[-1].rstrip('.ma')
cmds.file(text, r=1, op='v=0', typ="mayaAscii", ns=wrd)



'''
Created on Jul 7, 2011

@author: elise.deglau

'''
#<<downstream select

import maya.cmds as cmds
from functools import partial
from string import *
import re

hui=cmds.ls(sl=1)[0]
kil=[]

jiu=cmds.listConnections( hui, s=1, p=1, sh=1, scn=1)
outmeshs=["outputGeometry", "outMesh", "outputMesh", "worldMesh" ]
for r in range(len(jiu)):
    for i in range(len(outmeshs)):
        if outmeshs[i] in jiu[r]:
            kil.append(jiu[r])
print kil
gh=kil[0].split('.')
cmds.select(gh[0], r=1)

#>>upstream select

import maya.cmds as cmds
from functools import partial
from string import *
import re

hui=cmds.ls(sl=1)[0]
kil=[]

jiu=cmds.listConnections( hui, s=1, p=1, sh=1, scn=1)
outmeshs=["inputGeometry", "inMesh", "inputMesh" ]
for r in range(len(jiu)):
    for i in range(len(outmeshs)):
        if outmeshs[i] in jiu[r]:
            kil.append(jiu[r])
print kil
gh=kil[0].split('.')
cmds.select(gh[0], r=1)



#in_cn=cmds.connectionInfo( io, sfd=1)
#gh=in_cn.split('.')
#cmds.select(gh[0], r=1)
#
#ot_cn=cmds.connectionInfo( io, ged=1)
#gh=ot_cn.split('.')
#cmds.select(gh[0], r=1)



###################

transform=cmds.ls(sl=True, l=True)[0]

inmesh=cmds.listConnections((transform+'.inputGeometry'), s=True, d=False, p=True)

print inmesh




hui=cmds.ls(sl=1)[0]
kil=[]
jiu=cmds.listConnections( hui, s=1, p=1, sh=1, scn=1)
outmeshs=["outputGeometry", "outMesh", "outputMesh" ]
for r in range(len(jiu)):
    for i in range(len(outmeshs)):
        if outmeshs[i] in jiu[r]:
            kil.append(jiu[r])

print kil
#####




import re
xsi=Application
pt=LogMessage
eg_Gs=[]
fullNm=xsi.Selection[0]
rd=str(fullNm)#fullname
pNm=rd.split('_')#get pretty name
gh=re.sub(r'\d[0-9]', '',pNm[0] )# sep numbers
eg_Gs.append(gh)
sh=re.sub(r'\D[a-bA-B]*', '',pNm[0] )# sep letters
eg_Gs.append(sh)
delimiter="_"
FnNme=delimiter.join(eg_Gs)#recombine
print FnNme