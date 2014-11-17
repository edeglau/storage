import os, sys
import re
#import win32clipboard
import operator

result = cmds.promptDialog( 
            title='Confirm', 
            message='filename', 
            button=['Continue','Cancel'],
            defaultButton='Continue', 
            cancelButton='Cancel', 
            dismissString='Cancel' )
if result == 'Continue':
    filename=cmds.promptDialog(q=1)
    
printFolder="C:\\temp\\"+filename+".txt"

getGuides=cmds.ls("*guide")
inp=open(printFolder, 'w+')
for each in getGuides:
    transform=cmds.xform(each , q=True, ws=1, t=True)
    if transform==[0, 0, 0]:
        transformWorldMatrix = cmds.xform(each, q=True, wd=1, sp=True)  
        rotateWorldMatrix = cmds.xform(each, q=True, wd=1, ra=True) 
    else:
        transformWorldMatrix = cmds.xform(each, q=True, wd=1, t=True)  
        rotateWorldMatrix = cmds.xform(each, q=True, wd=1, ro=True) 
        print str(each)+":"+str(transformWorldMatrix)+":"+str(rotateWorldMatrix)
    inp=open(printFolder, 'a+')
    inp.write(str(each)+":"+str(transformWorldMatrix)+":"+str(rotateWorldMatrix)+'\r\n')
inp.close()  


if '\\\\' in printFolder:
    newpath=re.sub(r'\\\\',r'\\', printFolder)
    os.startfile(r'\\'+newpath[1:])    
else:
    os.startfile(printFolder)
    
    
    
    
    




    
    
    
    
    
    
    
import os, sys
import re
#import win32clipboard
import operator
guideDict={}
result = cmds.promptDialog( 
            title='Confirm', 
            message='Keep Bone', 
            button=['Continue','Cancel'],
            defaultButton='Continue', 
            cancelButton='Cancel', 
            dismissString='Cancel' )
if result == 'Continue':
    filename=cmds.promptDialog(q=1)
    
printFolder="C:\\temp\\"+filename+".txt"

Ggrp=cmds.CreateEmptyGroup()
cmds.rename(Ggrp, "Guides_"+filename+"_grp")

inp=open(printFolder, 'r')

List = open(printFolder).readlines()

for each in List:
    newlocbucket=[]
    newrotbucket=[]    
    getDictParts=each.split(':')
    getlocpart=getDictParts[1].strip('[]')
    getlocpart=getlocpart.split(', ')
    for item in getlocpart:
        newlocbucket.append(item)
    getrotpart=getDictParts[2].strip('[]]\r\n')
    getrotpart=getrotpart.split(', ')
    for item in getrotpart:
        getit=item.split('.')
        getint=int(getit[0])
        newrotbucket.append(getint)
    newlocbucket.append(newrotbucket)
    makeDict={getDictParts[0]:newlocbucket}
    guideDict.update(makeDict)
                   
for key, value in guideDict.items():
    print key
    newBucket=[]
    xCircmake=cmds.circle(n=key, r=1.5, nrx=1, nry=0, nrz=0)
    yCircmake=cmds.circle(n="yCirc", r=1.5, nrx=0, nry=1, nrz=0)
    zCircmake=cmds.circle(n="zCirc", r=1.5, nrx=0, nry=0, nrz=1)
    groupingShapes=[str(zCircmake[0]+"Shape"), str(yCircmake[0]+"Shape"), str(xCircmake[0])]
    newBucket.append(xCircmake[0])
    cmds.parent(groupingShapes,r=1, s=1)
    cmds.delete(yCircmake[0])
    cmds.delete(zCircmake[0])
    guidez=cmds.rename(zCircmake[0]+"Shape", xCircmake[0]+"Guidez")
    newBucket.append(guidez)
    guidey=cmds.rename(yCircmake[0]+"Shape", xCircmake[0]+"Guidey")
    newBucket.append(guidey) 
    for each in newBucket:  
        cmds.setAttr(each+".overrideEnabled", 1)
        cmds.setAttr(each+".overrideColor", 17)
    cmds.xform(xCircmake[0], ws=1, t=(value[0], value[1], value[2]) )  
    guidey=cmds.rename(xCircmake[0], key)  
    #cmds.makeIdentity(key, a=True, t=1, s=1, r=1, n=0)
    cmds.parent(xCircmake[0],"Guides_"+filename+"_grp")

