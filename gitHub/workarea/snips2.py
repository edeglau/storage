import maya.cmds as mc

for each in cmds.ls(sl=1, fl=1):
    getNames=[(item) for item in cmds.attributeQuery(get_attribute) if '______' in item]
    # getNames=[(item) for item in cmds.attributeQuery(get_attribute, node = each, ln=1)
    print getNames
    cmds.setAttr('{}.{}'.format(each, getNames), l=0)
    cmds.deleteAttr(each, at = getNames)

import maya.cmds as mc

getNames = [(each+"."+item) for each in cmds.ls (sl=1) for item in cmds.listAttr(each, w=1,hd=1, s=1, m=0) if '_______' in item]
for each in getNames:
    cmds.setAttr('visibilityControl_GRP.{}'.format(each), l=0)
    cmds.deleteAttr('visibilityControl_GRP', at = each)



import maya.cmds as mc

getNames = [(each+"."+item) for each in cmds.ls (sl=1) for item in cmds.listAttr(each, w=1,hd=1, s=1, m=0) if '_______' in item]
for each in getNames:
    cmds.setAttr(each, l=0)
    cmds.deleteAttr(each.split('.')[0], at = each.split('.')[-1])




from maya import cmds
fstjnt = cmds.ls(sl=1)[0]
endjnt = [(each)for each in cmds.listRelatives(fstjnt, ad=1) if cmds.nodeType(each) == "joint" ][0]
iknm = 'whynot'
hndl = cmds.ikHandle(n = iknm, sj = fstjnt, ee = endjnt,sol = 'ikSplineSolver', scv=0, ns=2, rtm=1, tws = 'easIn')[0]
getcrv = [(cmds.listRelatives(each, p=1, type = 'transform')[0])for each in cmds.listHistory(hndl) if cmds.nodeType(each) == "nurbsCurve" ][0]
cmds.delete(hndl)
hndl = cmds.ikHandle(n = iknm, sj = fstjnt, ee = endjnt,sol = 'ikSplineSolver', c = crvnm, ccv=0, roc=0, snc = 0, pcv =0,  rtm=1, cra = 1, tws = 'easIn')[0]
gettrnsfm = [(each)for each in cmds.listRelatives(fstjnt, ap=1) if cmds.nodeType(each) == "transform" ][0]
cmds.select([gettrnsfm, getcrv], r=1)
motionPath=cmds.pathAnimation(n='setupmp' , fractionMode=1, follow=1, followAxis="x", upAxis="y", worldUpType="1", worldUpVector=[0, 1, 0], inverseUp=0, inverseFront=0, bank=0)        
cmds.disconnectAttr(motionPath+"_uValue.output", motionPath+".uValue")
cmds.setAttr(motionPath+".fractionMode", True)
cmds.setAttr(motionPath+".uValue", 0) 

from maya import cmds
fstjnt = cmds.ls(sl=1)[0]
tnslt = cmds.xform(fstjnt, q=1, ws=1, t=1)
rtt = cmds.xform(fstjnt, q=1, ws=1, ro=1)
endjnt = [(each)for each in cmds.listRelatives(fstjnt, ad=1) if cmds.nodeType(each) == "joint" ][0]
iknm = 'whynot'
hndl = cmds.ikHandle(n = iknm, sj = fstjnt, ee = endjnt,sol = 'ikSplineSolver', scv=0, ns=2, rtm=1, tws = 'easIn')[0]
getcrv = [(cmds.listRelatives(each, p=1, type = 'transform')[0])for each in cmds.listHistory(hndl) if cmds.nodeType(each) == "nurbsCurve" ][0]
cmds.delete(hndl)
hndl = cmds.ikHandle(n = iknm, sj = fstjnt, ee = endjnt,sol = 'ikSplineSolver', c = crvnm, ccv=0, roc=0, snc = 0, pcv =0,  rtm=1, cra = 1, tws = 'easIn')[0]
gettrnsfm = [(each)for each in cmds.listRelatives(fstjnt, ap=1) if cmds.nodeType(each) == "transform" ][0]
cmds.xform(gettrnsfm, ws=1, t=tnslt)
cmds.xform(gettrnsfm, ws=1, ro=rtt)
cmds.select([gettrnsfm, getcrv], r=1)
motionPath=cmds.pathAnimation(n='setupmp' , fractionMode=1, follow=1, followAxis="x", upAxis="y", worldUpType="objectrotation", worldUpVector=[0, 1, 0], iu=0, inverseFront=1, bank=0)        
cmds.disconnectAttr(motionPath+"_uValue.output", motionPath+".uValue")
cmds.setAttr(motionPath+".fractionMode", True)
cmds.setAttr(motionPath+".uValue", 0) 



makeIdentity -apply true -t 1 -r 1 -s 1 -n 0 -pn 1;



cmds.makeIdentity(endjntik+'_GRP', apply=1, t=1, r=1, s=0, n=0, pn=0)


hotkeySet -e -import "/net/homes/edeglau/maya/2022/prefs/hotkeys/userHotkeys_elises.mhk";


#####adds driven key slot
import maya.cmds as mc
getconnection =  cmds.listConnections(cmds.ls(sl=1)[0], scn=1, d=1, p=1) [0]
getinconnection =  cmds.listConnections(cmds.ls(sl=1)[0], p=1) [-1]
cmds.setDrivenKeyframe(getconnection,  i=2, dv = 2, cd =  getinconnection) 



#####adds driven key slot
import maya.cmds as cmds
dict = {0:1, 1:0, 2:0}
for key, value in dict.items():
    for side in 'LR':
        for alpha in 'ABCDEFG':
            getgrop = cmds.ls('{}_{}_SPC_GRP_parentConstraint1_C_headWorld_JNT_worldTransform_GRP_offset_orig_locW0'.format(side, alpha))
            getconnection =  cmds.listConnections(getgrop, scn=1, d=1, p=1) [0]
            getinconnection =  cmds.listConnections(getgrop, p=1) [-1]
            cmds.setDrivenKeyframe(getconnection,  i=2, dv = key, v=value, cd =  getinconnection) 
    


#####adds driven key slot
import maya.cmds as cmds
dict = {0:0, 1:1, 2:0}
for key, value in dict.items():
    for side in 'LR':
        for alpha in 'ABCDEFG':
            getgrop = cmds.ls('{}_{}_SPC_GRP_parentConstraint1_C_headWorld_JNT_layoutTransform_GRP_offset_orig_locW1'.format(side, alpha))
            getconnection =  cmds.listConnections(getgrop, scn=1, d=1, p=1) [0]
            getinconnection =  cmds.listConnections(getgrop, p=1) [-1]
            cmds.setDrivenKeyframe(getconnection,  i=2, dv = key, v=value, cd =  getinconnection) 

#####adds driven key slot
import maya.cmds as cmds
dict = {0:1, 1:0, 2:0}
for key, value in dict.items():
    for side in 'LR':
        for alpha in 'ABCDEFG':
            getgrop = cmds.ls('{}_{}_SPC_GRP_parentConstraint1_C_headWorld_JNT_worldTransform_GRP_offset_orig_locW0'.format(side, alpha))[0]
            getconnection =  cmds.listConnections(getgrop, scn=1, d=1, p=1) [0]
            getinconnection =  cmds.listConnections(getgrop, p=1) [-1]
            cmds.setDrivenKeyframe(getconnection,  i=key, v=value, cd =  getinconnection) 
            cmds.keyframe(getgrop, index= (key,key), absolute=1, valueChange = value)
dict = {0:0, 1:1, 2:0}
for key, value in dict.items():
    for side in 'LR':
        for alpha in 'ABCDEFG':
            getgrop = cmds.ls('{}_{}_SPC_GRP_parentConstraint1_C_headWorld_JNT_layoutTransform_GRP_offset_orig_locW1'.format(side, alpha))[0]
            getconnection =  cmds.listConnections(getgrop, scn=1, d=1, p=1) [0]
            getinconnection =  cmds.listConnections(getgrop, p=1) [-1]
            cmds.setDrivenKeyframe(getconnection,  i=key,  v=value, cd =  getinconnection) 
            cmds.keyframe(getgrop, index= (key,key), absolute=1, valueChange = value)



#####adds driven key slot
import maya.cmds as cmds

dict = {0:0, 1:0, 2:1}#####set for local
for key, value in dict.items():
    getgrop = cmds.ls(sl=1)[0]
    getconnection =  cmds.listConnections(getgrop, scn=1, d=1, p=1) [0]
    getinconnection =  cmds.listConnections(getgrop, p=1) [-1]
    cmds.setDrivenKeyframe(getconnection,  i=key,  v=value, dv = key, cd =  getinconnection) 
    cmds.keyframe(getgrop, index= (key,key), absolute=1, valueChange = value)


####constrain many to one (first selected)
import maya.cmds as cmds

for each in cmds.ls(sl=1)[1:]:
    cmds.parentConstraint(cmds.ls(sl=1)[0], each, mo=1)

###curent next in numbers



bones = cmds.select('L_noseFingies_A_1_JNT1', hi=1)
getsel = cmds.ls(sl=1)
getchildObj=cmds.ls(sl=1, fl=1)
getbns = [(each) for each in getchildObj if cmds.nodeType(each) == "joint"]
print getbns
getlen= len(getbns)
for eachPoint in enumerate(xrange(1,getlen)):
    each, next_item = eachPoint[1], int(eachPoint[1])+1
    cmds.aimConstraint('L_noseFingies_A_{}_JNT1'.format(next_item), 'L_noseFingies_A_{}_JNT1'.format(each), mo=1)
    




#####adds driven key slot
import maya.cmds as cmds
dict = {0:1, 1:0}
for key, value in dict.items():
    for side in 'LR':
        for alpha in 'ABCDEFG':
            getgrop = cmds.ls('{}_{}_MTX_GRP_parentConstraint1_C_nose_LCL_JNTW0'.format(side, alpha))[0]
            getconnection =  cmds.listConnections(getgrop, scn=1, d=1, p=1) [0]
            getinconnection =  cmds.listConnections(getgrop, p=1) [-1]
            cmds.setDrivenKeyframe(getconnection,  i=key, v=value, cd =  getinconnection) 
            cmds.keyframe(getgrop, index= (key,key), absolute=1, valueChange = value)



dict = {0:0, 1:1}
for key, value in dict.items():
    for side in 'LR':
        for alpha in 'ABCG':
            getgrop = cmds.ls('{}_{}_MTX_GRP_parentConstraint1_C_headLocal_JNTW1'.format(side, alpha))[0]
            print getgrop
            getconnection =  cmds.listConnections(getgrop, scn=1, d=1, p=1) [0]
            getinconnection =  cmds.listConnections(getgrop, p=1) [-1]
            cmds.setDrivenKeyframe(getconnection,  i=key,  v=value, dv = key, cd =  getinconnection) 
            cmds.keyframe(getgrop, index= (key,key), absolute=1, valueChange = value)

#unparents a heirarchy, lines it up and reheiararchies
from maya import cmds
gettrn = cmds.xform(cmds.ls(sl=1)[0], q=1, ws=1, t=1)
getrot = cmds.xform(cmds.ls(sl=1)[0], q=1, ws=1, ro=1)
gettrn2 = cmds.xform(cmds.ls(sl=1)[-1], q=1, ws=1, t=1)
getrot2 = cmds.xform(cmds.ls(sl=1)[-1], q=1, ws=1, ro=1)
cmds.xform(cmds.ls(sl=1)[0], ws=1, t=gettrn2)
cmds.xform(cmds.ls(sl=1)[0], ws=1, ro=getrot2)
cmds.xform(cmds.ls(sl=1)[-1], ws=1, t=gettrn)
cmds.xform(cmds.ls(sl=1)[-1],ws=1, ro=getrot)


#reorderlist:

import maya.cmds as cmds
import ridemaya.lib.attr as ltra
get = cmds.listAttr("visibilityControl_GRP", ud=1)

newget = [u'_', u'joint',
u'__', u'membrane_fk1',
u'___', u'C_jaw1',
 u'C_jaw2', u'____', u'C_tongueFk1',
 u'C_tongueIk1', u'C_tongueSubs', u'L_mouthCornerpreset1', u'C_face1', u'C_face2', u'C_face3', u'_____',
 u'C_fingieMaskTop1', u'C_fingieMaskBot1',u'noseFingiesVis', u'noseFingiesIK2',  u'______', u'C_nose1', u'C_fingieTopHitch1',
  u'C_lowerFingies1', u'C_fingieBotHitch1',]

ltra.reorder("visibilityControl_GRP", newget)



cmds.offsetCurve(ch on -rn false -cb 2 -st true -cl true -cr 0 -d 1 -tol 0.01 -sd 5 -ugn false  "curve1" ;#reparent
#lines up starters to the joints it controls
from maya import cmds
a_dict = []
for side in 'RL':
    for alpha in 'ABCDEFG':
        grp = "{}_noseFingies{}1_CTL_SLOC".format(side, alpha, x)
        getpartransform = cmds.listRelatives(grp, ad=1, typ="transform")
        #for each_item in getpartransform[::-1]:
        initial_order = getpartransform[::-1]
        for i in xrange(len(initial_order)-1):
            current_item, next_item = initial_order[i], initial_order[i+1]
            newdict = (current_item, next_item)
            print newdict



#lines up starters to the joints it controls
#injects starters with subs
from maya import cmds
a_dict = []
for side in 'RL':
    for alpha in 'ABCDEFG':
        grp = "{}_noseFingies{}Starter_GRP".format(side, alpha)
        getpartransform = cmds.listRelatives(grp, ad=1, typ="transform")
        #for each_item in getpartransform[::-1]:
        initial_order = getpartransform[::-1]
        for i in xrange(len(initial_order)-1):
            current_item, next_item = initial_order[i], initial_order[i+1]
            ea = current_item.split('_CTL_SLOC')[0]+'sub_CTL_SLOC'
            try:
                get = cmds.parentConstraint(current_item, ea, mo=0)[0]
                cmds.delete(get)
                cmds.parent(ea, current_item)
                cmds.parent(next_item, ea)
            except:
                pass
        try:
            get = cmds.parentConstraint('{}_noseFingies{}6_CTL_SLOC'.format(side, alpha), '{}_noseFingies{}6sub_CTL_SLOC'.format(side, alpha), mo=0)[0]
            cmds.delete(get)
            cmds.parent('{}_noseFingies{}6sub_CTL_SLOC'.format(side, alpha), '{}_noseFingies{}6_CTL_SLOC'.format(side, alpha))
        except:
            pass
defname = '_wrp'.format())
cmds.select([], r=1)
wrapDef = cmds.deformer(type="wrap", n=wrapDef)[0]
getWrapBase = [(connected) for connected in cmds.listConnections(wrapDef, d=1, sh=1, type = "nurbsCurve") if "geoBase" in connected and "wrp" not in connected][0]
shortname = getWrapBase.split("|")[1]
newname = "{}wrp_geoBaseShape".format()
cmds.rename(getWrapBase, newname)
cmds.parent(newname, )

from maya import cmds
for side in 'LR':
    for alpha in 'ABCDEFG':
        fstjnt_dup = '{}_noseFingies_{}_1_JNT1'.format(side, alpha)
        cmds.select(fstjnt, hi=1)
        getchildObj=cmds.ls(sl=1, fl=1)
        complist = complista[:-1]
        getlngth = len(getchildlist)
        getdist = getlngth/14
        if len(getchildlist[::getdist])==6:
            for item in getchildlist[::getdist]:
                orderlist.append(item)
        elif len(getchildlist[::getdist])==7:
            for item in  getchildlist[::getdist][1:]:
                orderlist.append(item)
        for index, each in enumerate(orderlist[::-1]):
            gtnum= index
from maya import cmds

for side in 'LR':
    for
alpha in 'ABCDEFG':
fstjnt_dup = '{}_noseFingies_{}_1_JNT1'.format(side, alpha)
cmds.select(fstjnt_dup, hi=1)
getchildObj = cmds.ls(sl=1, fl=1)
print
getchildObj
getUVmap = cmds.polyListComponentConversion(sel_obj, fe=1, tv=1)
cmds.select('{}_{}_poly.e[0]'.format(side, alpha))
cmds.polySelectSp(loop=1)
getVert = cmds.polyListComponentConversion(sel_obj, fe=1, tv=1)
getvertlistend = len(getVert]
complist = complista[:-1]
getlngth = len(getchildlist)
getdist = getlngth / 14
if len(getchildlist[::getdist]) == 6:
    for
item in getchildlist[::getdist]:
orderlist.append(item)
elif len(getchildlist[::getdist]) == 7:
for item in getchildlist[::getdist][1:]:
    orderlist.append(item)
for index, each in enumerate(orderlist[::-1]):
    gtnum = index

getUVmap = cmds.polyListComponentConversion(sel_obj, fv=1, tuv=1)

cmds.nurbsToPoly('L_A_extd', n="thing", pt=1, pc=100, ch=0, f=1, chr=0.9, ft=0.01, d=0.1, mel=0.001, ut=1, un=3, vt=1, mnd=1,
                                    uch=0, ucr=0, cht=0.2, es=0, ntr=0, mrt=0, uss=1)[0]



#injects starters with subs
from maya import cmds
cmds.nurbsToPoly('L_A_extd', n="thing", pt=1, pc=100, ch=0, f=1, chr=0.9, ft=0.01, d=0.1, mel=0.001, ut=1, un=3, vt=1, mnd=1,
                                    uch=0, ucr=0, cht=0.2, es=0, ntr=0, mrt=0, uss=1)[0]
CurveWarp


getpartransform = cmds.listConnections('{}Shape', t="curveWarp")[0]
print getpartransform

cmds.polySelectSp(loop=1)

CreateWrap;
performCreateWrap false;
cmds.deformer(type='wrap', geometry = '')

cmds.deformer("wrap")
cmds.select('L_A_poly.e[8]', 'L_A_poly.e[13]', 'L_A_poly.e[27]', 'L_A_poly.e[56:57]', 'L_A_poly.e[67]', 'L_A_poly.e[76]', r=1]

crcl = cmds.circle(c=(.5, .5, .5), nr=(0, 1, 0), n='circle_ext_cv', sw=360, r=0.0015, d=3, ut=0, tol=0.01, s=8, ch=1)[0]

from maya import cmds

for side in 'LR':
    for
alpha in 'ABCDEFG':
fstjnt_dup = '{}_noseFingies_{}_1_JNT1'.format(side, alpha)
cmds.select(fstjnt_dup, hi=1)
getchildObj = cmds.ls(sl=1, fl=1)
print
getchildObj
cmds.select('{}_{}_poly.e[0]'.format(side, alpha))
cmds.polySelectSp(loop=1)
getVert = cmds.polyListComponentConversion(sel_obj, fe=1, tv=1)
getvertlistend = len(getVert]
complist = complista[:-1]
getlngth = len(getchildlist)
getdist = getlngth / 14
if len(getchildlist[::getdist]) == 6:
    for
item in getchildlist[::getdist]:
orderlist.append(item)
elif len(getchildlist[::getdist]) == 7:
for item in getchildlist[::getdist][1:]:
    orderlist.append(item)
for index, each in enumerate(orderlist[::-1]):
    gtnum = index

getUVmap = cmds.polyListComponentConversion(sel_obj, fv=1, tuv=1)

from maya import cmds

for side in 'LR':
    for
alpha in 'ABCDEFG':
fstjnt_dup = '{}_noseFingies_{}_1_JNT1'.format(side, alpha)
cmds.select(fstjnt_dup, hi=1)
getchildlist = cmds.ls(sl=1, fl=1)
print
getchildObj

cmds.select('{}_{}_poly.e[0]'.format(side, alpha))
cmds.polySelectSp(loop=1)
getVert = cmds.ConvertSelectionToVertices()
# cmds.polyListComponentConversion(cmds.ls(sl=1)[0], fe=1, tv=1)
getvertlistend = len(getVert]
print
getvertlistend
complist = getchildlist[:-1]
print
complist
getlngth = len(getchildlist)
getdist = getlngth / 14print
getdist
orderlist = []
if len(getchildlist[::getdist]) == 14:
    for
item in getchildlist[::getdist]:
orderlist.append(item)
elif len(getchildlist[::getdist]) == 7:
for item in getchildlist[::getdist][1:]:
    orderlist.append(item)
for index, each in enumerate(orderlist[::-1]):
    gtnum = index

getUVmap = cmds.polyListComponentConversion(sel_obj, fv=1, tuv=1)

from maya import cmds

for side in 'LR':
    for
alpha in 'ABCDEFG':
fstjnt_dup = '{}_noseFingies_{}_1_JNT1'.format(side, alpha)
cmds.select(fstjnt_dup, hi=1)
getchildlist = cmds.ls(sl=1, fl=1)
print
getchildlist
getjointlistend = len(getchildlist)
print
getjointlistend

from maya import cmds

for side in 'LR':
    for
alpha in 'ABCDEFG':
fstjnt_dup = '{}_noseFingies_{}_1_JNT1'.format(side, alpha)
findjntlist = [(eajnt) for eajnt in cmds.listRelatives(fstjnt_dup, ad=1, type="transform") if
               cmds.nodeType(eajnt) == "joint"]
getchildlist = findjntlist + [fstjnt_dup]
getchildlist = getchildlist[::-1]
getjointlistend = len(getchildlist)
print
str(getjointlistend) + ' jnts'
cmds.select('{}_{}_poly.e[0]'.format(side, alpha))
cmds.polySelectSp(loop=1)
cmds.ConvertSelectionToVertices()
getVert = cmds.ls(sl=1)
# cmds.polyListComponentConversion(cmds.ls(sl=1)[0], fe=1, tv=1)
getvertlistend = len(getVert)
print
str(getvertlistend) + ' verts'
complist = getchildlist[:-1]
getlngth = len(getchildlist)
getdist = getlngth / 14
orderlist = []
print
getchildlist[::getdist]
if len(getchildlist[::getdist]) == 14:
    for
item in getchildlist[::getdist]:
orderlist.append(item)
elif len(getchildlist[::getdist]) == 7:
for item in getchildlist[::getdist][1:]:
    orderlist.append(item)
for index, each in enumerate(orderlist[::-1]):
    gtnum = index

getUVmap = cmds.polyListComponentConversion(sel_obj, fv=1, tuv=1)



from maya import cmds
for side in 'LR':
    for alpha in 'ABCDEFG':
        fstjnt_dup = '{}_noseFingies_{}_1_JNT1'.format(side, alpha)
        findjntlist = [(eajnt) for eajnt in cmds.listRelatives(fstjnt_dup, ad=1, type="transform") if cmds.nodeType(eajnt) == "joint"]
        getchildlist = findjntlist+[fstjnt_dup]
        getchildlist =  getchildlist[::-1]
        getjointlistend = len(getchildlist)
        print str(getjointlistend)+ ' jnts'
        cmds.select('{}_{}_poly.e[0]'.format(side, alpha))
        cmds.polySelectSp(loop=1)
        cmds.ConvertSelectionToVertices()
        getVert = cmds.ls(sl=1)
        for each_v in getVert:
            getTranslation = cmds.xform(each, q=True, ws=1, t=True)
            loc = cmds.spaceLocator(n=each_v+'_loc')
            cmds.xform(loc, ws=1, t = getTranslation)
from maya import cmds

for side in 'LR':
    for
alpha in 'ABCDEFG':
fstjnt_dup = '{}_noseFingies_{}_1_JNT1'.format(side, alpha)
findjntlist = [(eajnt) for eajnt in cmds.listRelatives(fstjnt_dup, ad=1, type="transform") if
               cmds.nodeType(eajnt) == "joint"]
getchildlist = findjntlist + [fstjnt_dup]
getchildlist = getchildlist[::-1]
getjointlistend = len(getchildlist)
cmds.select('{}_{}_poly.e[0]'.format(side, alpha))
cmds.polySelectSp(loop=1)
# cmds.polyListComponentConversion(cmds.ls(sl=1)[0], fe=1, tv=1)
getverts = cmds.polyInfo(cmds.ls(sl=1), ev=1)
cmds.ConvertSelectionToVertices()
getVert = cmds.ls(sl=1)
# cmds.polyListComponentConversion(cmds.ls(sl=1)[0], fe=1, tv=1)
getvertlistend = len(getVert)
print
str(getvertlistend) + ' verts'
complist = getchildlist[:-1]
getlngth = len(getchildlist)
getdist = getlngth / 14
orderlist = []
print
getchildlist[::getdist]
if len(getchildlist[::getdist]) == 14:
    for
item in getchildlist[::getdist]:
orderlist.append(item)
elif len(getchildlist[::getdist]) == 7:
for item in getchildlist[::getdist][1:]:
    orderlist.append(item)
for index, each in enumerate(orderlist[::-1]):
    gtnum = index

getUVmap = cmds.polyListComponentConversion(sel_obj, fv=1, tuv=1)from maya import cmds

cmds.selectPref(tso=True)
for side in 'LR':
    for
alpha in 'ABCDEFG':
fstjnt_dup = '{}_noseFingies_{}_1_JNT1'.format(side, alpha)
findjntlist = [(eajnt) for eajnt in cmds.listRelatives(fstjnt_dup, ad=1, type="transform") if
               cmds.nodeType(eajnt) == "joint"]
getchildlist = findjntlist + [fstjnt_dup]
getchildlist = getchildlist[::-1]
getjointlistend = len(getchildlist)
cmds.select('{}_{}_poly.e[0]'.format(side, alpha))
cmds.polySelectSp(loop=1)
cmds.polyListComponentConversion(cmds.ls(sl=1)[0], fe=1, tv=1)
# getverts = cmds.polyInfo(cmds.ls(sl=1), ev=1)
for index, ea_edge in cmds.ls(os=1):
    print
ea_edge
getTranslation = cmds.xform(ea_edge, q=True, ws=1, t=True)
loc = cmds.spaceLocator(n='{}_{}_loc'.format(index))
cmds.xform(loc, ws=1, t=getTranslation)

getverts = cmds.polyInfo(ea_edge, ev=1)
print
getverts
print
cmds.polyEvaluate(ea_edge, vc=1)
cmds.ConvertSelectionToVertices()
getVert = cmds.ls(sl=1)
# cmds.polyListComponentConversion(cmds.ls(sl=1)[0], fe=1, tv=1)
getvertlistend = len(getVert)
print
str(getvertlistend) + ' verts'
complist = getchildlist[:-1]
getlngth = len(getchildlist)
getdist = getlngth / 14
orderlist = []
print
getchildlist[::getdist]
if len(getchildlist[::getdist]) == 14:
    for
item in getchildlist[::getdist]:
orderlist.append(item)
elif len(getchildlist[::getdist]) == 7:
for item in getchildlist[::getdist][1:]:
    orderlist.append(item)
for index, each in enumerate(orderlist[::-1]):
    gtnum = index

getUVmap = cmds.polyListComponentConversion(sel_obj, fv=1, tuv=1)




from maya import cmds

for side in 'LR':
    for alpha in 'ABCDEFG':
        locl_ofst_crv = '{}_noseFingies_{}_mn_crv_ofst'.format(side, alpha)
        ext = '{}_{}_poly'.format(side, alpha)
        cmds.select(locl_ofst_crv)
        cmds.select(ext, add=1)
        cmds.deformer(type="wrap")

cmds.connectAttr('{}.outputX'.format(revnode),  '{}_noseFingies_{}_mn_crv_ofst_ik_bsp.envelope'.format(side, alpha))
#injects starters with subs
from maya import cmds
a_dict = []
for side in 'RL':
    for alpha in 'ABCDEFG':
        grp = "{}_noseFingies{}Starter_GRP".format(side, alpha)
        getpartransform = cmds.listRelatives(grp, ad=1, typ="transform")
        #for each_item in getpartransform[::-1]:
        initial_order = getpartransform[::-1]
        for i in xrange(len(initial_order)-1):
            current_item, next_item = initial_order[i], initial_order[i+1]
            ea = current_item.split('_CTL_SLOC')[0]+'sub_CTL_SLOC'
            try:
                get = cmds.parentConstraint(current_item, ea, mo=0)[0]
                cmds.delete(get)
                cmds.parent(ea, current_item)
                cmds.parent(next_item, ea)
            except:
                pass
        try:
            get = cmds.parentConstraint('{}_noseFingies{}6_CTL_SLOC'.format(side, alpha), '{}_noseFingies{}6sub_CTL_SLOC'.format(side, alpha), mo=0)[0]
            cmds.delete(get)
            cmds.parent('{}_noseFingies{}6sub_CTL_SLOC'.format(side, alpha), '{}_noseFingies{}6_CTL_SLOC'.format(side, alpha))
        except:
            pass

#injects starters with subs


#reshuffle starters with subs
#injects starters with subs
from maya import cmds
a_dict = []
for side in 'RL':
    for alpha in 'ABCDEFG':
        grp = "{}_noseFingies{}Starter_GRP".format(side, alpha)
        getpartransform = [(each) for each in cmds.listRelatives(grp, ad=1, typ="transform") if "sub" not in each]
        getpartransformsub = [(each) for each in cmds.listRelatives(grp, ad=1, typ="transform") if "sub" in each]
        #for each_item in getpartransform[::-1]:
        initial_order = getpartransform[::-1]
        for i in xrange(len(initial_order)-1):
            current_item, next_item = initial_order[i], initial_order[i+1]
            print next_item, current_item
            try:
                cmds.parent(next_item, current_item)
            except:
                pass
        for i in xrange(len(getpartransformsub)-1):
            current_item, next_item = getpartransformsub[i], getpartransformsub[i+1]
            print current_item, next_item
            try:
                cmds.parent(current_item, next_item)
            except:
                pass
        cmds.parent("{}_noseFingies{}1sub_CTL_SLOC".format(side, alpha), "{}_noseFingies{}Starter_GRP".format(side, alpha))#injects starters with subs
from maya import cmds
a_dict = []
for side in 'RL':
    for alpha in 'ABCDEFG':
        grp = "{}_noseFingies{}Starter_GRP".format(side, alpha)
        getpartransform = [(each) for each in cmds.listRelatives(grp, ad=1, typ="transform") if "sub" not in each]
        getpartransformsub = [(each) for each in cmds.listRelatives(grp, ad=1, typ="transform") if "sub" in each]
        #for each_item in getpartransform[::-1]:
        initial_order = getpartransform[::-1]
        for i in xrange(len(initial_order)-1):
            current_item, next_item = initial_order[i], initial_order[i+1]
            print next_item, current_item
            try:
                cmds.parent(next_item, current_item)
            except:
                pass
        for i in xrange(len(getpartransformsub)-1):
            current_item, next_item = getpartransformsub[i], getpartransformsub[i+1]
            print current_item, next_item
            try:
                cmds.parent(current_item, next_item)
            except:
                pass
        cmds.parent("{}_noseFingies{}1sub_CTL_SLOC".format(side, alpha), "{}_noseFingies{}Starter_GRP".format(side, alpha))



import maya.cmds as cmds
grp ='render_scalesLayout_default_default_:scales_GRP'
getpartransform = [(each) for each in cmds.listRelatives(grp, ad=1, typ="transform") if "_GE" in each]
cmds.select(getpartransform)
cmds.polyUnite(cmds.ls(sl=1), ch=1, mergeUVSets=1,centerPivot =1, name="scales_GED")
cmds.delete(cmds.ls(sl=1)[0], ch=1)
cmds.parent("scales_GED", "setup_GRP")

snakeOil = cmds.deformer('scales_GED', type = "snakeOil")[0]
cmds.connectAttr ("render_primary_default_default_:skinPurple_C_head_PLY.worldMesh", snakeOil + ".driverMesh")
#cmds.connectAttr ("render_primary_default_default_:skinPurple_C_head_PLYRef.worldMesh", snakeOil + ".driverMeshBind")
cmds.setAttr (snakeOil+'.bindMode',2)
cmds.setAttr ("snakeOil1.rebind", 1)
cmds.setAttr ("snakeOil1.rebind", 0)

import maya.cmds as cmds

grp ='render_scalesLayout_default_default_:scales_GRP'
getpartransform = [(each) for each in cmds.listRelatives(grp, ad=1, typ="transform") if "_GE" in each]
cmds.select(getpartransform)
cmds.polyUnite(cmds.ls(sl=1), ch=1, mergeUVSets=1,centerPivot =1, name="scales_GED")
cmds.delete(cmds.ls(sl=1)[0], ch=1)
cmds.parent("scales_GED", "setup_GRP")

snakeOil = cmds.deformer('scales_GED', type = "snakeOil")[0]
cmds.connectAttr ("render_primary_default_default_:skinPurple_C_head_PLY.worldMesh", snakeOil + ".driverMesh")
#cmds.connectAttr ("render_primary_default_default_:skinPurple_C_head_PLYRef.worldMesh", snakeOil + ".driverMeshBind")
cmds.setAttr (snakeOil+'.bindMode',2)
cmds.setAttr ("snakeOil1.rebind", 1)
cmds.setAttr ("snakeOil1.rebind", 0)import maya.cmds as cmds

grp ='render_scalesLayout_default_default_:scales_GRP'
getpartransform = [(each) for each in cmds.listRelatives(grp, ad=1, typ="transform") if "_GE" in each]
cmds.select(getpartransform)
cmds.polyUnite(cmds.ls(sl=1), ch=1, mergeUVSets=1,centerPivot =1, name="scales_GED")
cmds.delete(cmds.ls(sl=1)[0], ch=1)
cmds.parent("scales_GED", "setup_GRP")

snakeOil = cmds.deformer('scales_GED', type = "snakeOil")[0]
cmds.connectAttr ("render_primary_default_default_:skinPurple_C_head_PLY.worldMesh", snakeOil + ".driverMesh")
#cmds.connectAttr ("render_primary_default_default_:skinPurple_C_head_PLYRef.worldMesh", snakeOil + ".driverMeshBind")
cmds.setAttr (snakeOil+'.bindMode',2)
cmds.setAttr ("snakeOil1.rebind", 1)
cmds.setAttr ("snakeOil1.rebind", 0)

import maya.cmds as cmds

grp ='render_scalesLayout_default_default_:scales_GRP'
getpartransform = [(each) for each in cmds.listRelatives(grp, ad=1, typ="transform") if "_GE" in each]
cmds.select(getpartransform)
cmds.polyUnite(cmds.ls(sl=1), ch=1, mergeUVSets=1,centerPivot =1, name="scales_GED")
cmds.delete(cmds.ls(sl=1)[0], ch=1)
cmds.parent("scales_GED", "setup_GRP")

snakeOil = cmds.deformer('scales_GED', type = "snakeOil")[0]
cmds.connectAttr ("render_primary_default_default_:skinPurple_C_head_PLY.worldMesh", snakeOil + ".driverMesh")
#cmds.connectAttr ("render_primary_default_default_:skinPurple_C_head_PLYRef.worldMesh", snakeOil + ".driverMeshBind")
cmds.setAttr (snakeOil+'.bindMode',2)
cmds.setAttr ("snakeOil1.rebind", 1)
cmds.setAttr ("snakeOil1.rebind", 0)
import maya.cmds as cmds

grp ='render_scalesLayout_default_default_:scales_GRP'
getpartransform = [(each) for each in cmds.listRelatives(grp, ad=1, typ="transform") if "_GE" in each]
cmds.select(getpartransform)
cmds.polyUnite(cmds.ls(sl=1), ch=1, mergeUVSets=1,centerPivot =1, name="scales_GED")
cmds.delete(cmds.ls(sl=1)[0], ch=1)
cmds.parent("scales_GED", "setup_GRP")

snakeOil = cmds.deformer('scales_GED', type = "snakeOil")[0]
cmds.connectAttr ("render_primary_default_default_:skinPurple_C_head_PLY.worldMesh", snakeOil + ".driverMesh")
#cmds.connectAttr ("render_primary_default_default_:skinPurple_C_head_PLYRef.worldMesh", snakeOil + ".driverMeshBind")
cmds.setAttr (snakeOil+'.bindMode',2)
cmds.setAttr ("snakeOil1.rebind", 1)
cmds.setAttr ("snakeOil1.rebind", 0)

import maya.cmds as cmds

grp ='render_scalesLayout_default_default_:scales_GRP'
getpartransform = [(each) for each in cmds.listRelatives(grp, ad=1, typ="transform") if "_GE" in each]
cmds.select(getpartransform)
cmds.polyUnite(cmds.ls(sl=1), ch=1, mergeUVSets=1,centerPivot =1, name="scales_GED")
cmds.delete(cmds.ls(sl=1)[0], ch=1)
cmds.parent("scales_GED", "setup_GRP")

snakeOil = cmds.deformer('scales_GED', type = "snakeOil")[0]
cmds.connectAttr ("render_primary_default_default_:skinPurple_C_head_PLY.worldMesh", snakeOil + ".driverMesh")
#cmds.connectAttr ("render_primary_default_default_:skinPurple_C_head_PLYRef.worldMesh", snakeOil + ".driverMeshBind")
cmds.setAttr (snakeOil+'.bindMode',2)
cmds.setAttr ("snakeOil1.rebind", 1)
cmds.setAttr ("snakeOil1.rebind", 0)
import maya.cmds as cmds

grp ='render_scalesLayout_default_default_:scales_GRP'
getpartransform = [(each) for each in cmds.listRelatives(grp, ad=1, typ="transform") if "_GE" in each]
cmds.select(getpartransform)
cmds.polyUnite(cmds.ls(sl=1), ch=1, mergeUVSets=1,centerPivot =1, name="scales_GED")
cmds.delete(cmds.ls(sl=1)[0], ch=1)
cmds.parent("scales_GED", "setup_GRP")

snakeOil = cmds.deformer('scales_GED', type = "snakeOil")[0]
cmds.connectAttr ("render_primary_default_default_:skinPurple_C_head_PLY.worldMesh", snakeOil + ".driverMesh")
#cmds.connectAttr ("render_primary_default_default_:skinPurple_C_head_PLYRef.worldMesh", snakeOil + ".driverMeshBind")
cmds.setAttr (snakeOil+'.bindMode',2)
cmds.setAttr ("snakeOil1.rebind", 1)
cmds.setAttr ("snakeOil1.rebind", 0)

import maya.cmds as cmds

grp ='render_scalesLayout_default_default_:scales_GRP'
getpartransform = [(each) for each in cmds.listRelatives(grp, ad=1, typ="transform") if "_GE" in each]
cmds.select(getpartransform)
cmds.polyUnite(cmds.ls(sl=1), ch=1, mergeUVSets=1,centerPivot =1, name="scales_GED")
cmds.delete(cmds.ls(sl=1)[0], ch=1)
cmds.parent("scales_GED", "setup_GRP")

snakeOil = cmds.deformer('scales_GED', type = "snakeOil")[0]
cmds.connectAttr ("render_primary_default_default_:skinPurple_C_head_PLY.worldMesh", snakeOil + ".driverMesh")
#cmds.connectAttr ("render_primary_default_default_:skinPurple_C_head_PLYRef.worldMesh", snakeOil + ".driverMeshBind")
cmds.setAttr (snakeOil+'.bindMode',2)
cmds.setAttr ("snakeOil1.rebind", 1)
cmds.setAttr ("snakeOil1.rebind", 0)
import maya.cmds as cmds
import maya.mel
import numpy
setjnts = []
getjnts = []

for mainjoint in cmds.ls(sl=1):
    try:
        parent_jnt = cmds.listRelatives(mainjoint, p=1, typ="joint")[0]
    except:
        pass
    getjnts.append(mainjoint)
    get_jnts_list=cmds.listRelatives(mainjoint, ad=1, typ="joint")
    for eajnt in get_jnts_list:
        setjnts.append(eajnt)
    for jt in reversed(setjnts):
        getjnts.append(jt)
    point_value_set = []
    for c in mainjoint:
        if c.isdigit():
            onum = c
    suffix = mainjoint.split(onum)[-1]
    pref = mainjoint.split(onum)[0]
    newnum = str(int(onum) +1)
    jnt_crv_name = pref+str(onum)+suffix+'_crv'
    for indexNumber, eachPoint in enumerate(xrange(len(getjnts))):
        try:
            each, next_item = getjnts[eachPoint], getjnts[eachPoint + 1]
            #print each, next_item
            current_item = each
            curTran =cmds.xform(current_item, q=True, ws=1, t=True)
            point_value_set.append(curTran)
            #print curTran
            nextTran = cmds.xform(next_item, q=True, ws=1, t=True)
            xpos_sum = nextTran[0]  - curTran[0]
            xpos2 = xpos_sum/2
            xpos = curTran[0] + xpos2
            ypos_sum = nextTran[1]  - curTran[1]
            ypos2 = ypos_sum/2
            ypos = curTran[1] + ypos2
            zpos_sum = nextTran[2]  - curTran[2]
            zpos2 = zpos_sum/2
            zpos = curTran[2] + zpos2
            point_val = (xpos, ypos, zpos)
            point_value_set.append(point_val)
        except:
            pass    cur_last_Tran =cmds.xform(getjnts[-1], q=True, ws=1, t=True)
    point_value_set.append(cur_last_Tran)
    more = int(len(point_value_set) *1)
    CurveMake = cmds.curve(n=jnt_crv_name, d=1, p=point_value_set)
    cmds.rebuildCurve(jnt_crv_name, ch=1, rpo=1, rt=0, end=1, kr=0, kcp=0, kep=1, kt=0, s=int(more), d=3, tol=0.01)
    get_cv = cmds.ls('{}.cv[*]'.format(jnt_crv_name), fl=1)
    get_new_chain  =  jnt_crv_name.split('_crv')[0]
    last_num = len(get_cv) + int(onum )
    keep_orients = []
    keep_orient_list = numpy.repeat(getjnts, 2)
    for each_jnt_orient in keep_orient_list:
        getornt = cmds.joint(each_jnt_orient, q=1, o=1)
        keep_orients.append(getornt)
    stlist = [keep_orients[0]]
    endlst = [keep_orients[-1]]
    setlist = stlist + keep_orients + endlst
    cmds.delete (getjnts)
    newjoint_bucket = []
    for c_jnts, ornt in map(None, enumerate(get_cv), setlist):
        index = c_jnts[0]
        item = c_jnts[-1]
        getTranslation=cmds.xform(item, q=1, t=1, ws=1)
        get_each = item.split('_crv')[0]
        pref = get_each.split(onum)[0]
        suffix =  get_each.split(onum)[-1]
        new_num_add = int(onum)+index
        jointnames = pref+str(new_num_add)+suffix
        njnt = cmds.joint(n=jointnames, p=getTranslation, o = ornt)
        newjoint_bucket.append(njnt)
    if cmds.objExists(parent_jnt) == True:
        cmds.parent(get_new_chain, parent_jnt)
    # cmds.joint(get_new_chain , e=1, ch = 1, sao = 'yup', oj = 'xyz', zso = 1, spa=1)
    cmds.delete(jnt_crv_name)
    cmds.select(cl=1)
getSecondGrp='techmesh_:lip_msh'
getFirstGrp='lip_ctrl_msh'
myDict={
        ".shapePreservationEnable":1,
        ".shapePreservationSteps":72,
        ".shapePreservationReprojection":1,
        ".shapePreservationIterations":1,
        ".shapePreservationMethod":0,
        ".envelope":1,
        ".targetSmoothLevel":1,
        ".continuity":1,
        ".keepBorder":0,
        ".boundaryRule":1,
        ".keepHardEdge":0,
        ".propagateEdgeHardness":0,
        ".keepMapBorders":1,
        ".projection":4,
        ".closestIfNoIntersection":0,
        ".closestIfNoIntersection":0 ,
        ".reverse":0,
        ".bidirectional":0,
        ".boundingBoxCenter":1,
        ".axisReference":0 ,
        ".alongX":1,
        ".alongY":1,
        ".alongZ":1,
        ".offset":0,
        ".targetInflation":0,
        ".falloff":0.3021390379,
        ".falloffIterations": 1
        }
#cmds.delete(getFirstGrp, ch=1)
getShrink=cmds.deformer(getFirstGrp, type="shrinkWrap")
cmds.connectAttr(getSecondGrp+".worldMesh[0]", getShrink[0]+".targetGeom", f=1)
for key, value in myDict.items():
    cmds.setAttr(getShrink[0]+key, value)


import maya.cmds as mc
selObj=cmds.ls(sl=1, fl=1)
drivenmesh = selObj[1]
parentObj=selObj[0]
getparentObj=cmds.listRelatives(parentObj, ad=1, type="mesh")
cmds.select(getparentObj, r=1)
cmds.deformer(type="rigWrap")
for each in getparentObj:
    cmds.select([each, drivenmesh], r=1)
    cmds.connectAttr("{}.worldMesh[0]".format(each), "rigWrapNode.driverPoints[0]")
cmds.setAttr("rigWrapNode.bind", 1)



#onion
import maya.cmds as cmds
selObj=cmds.ls(sl=1, fl=1)
getmin = cmds.playbackOptions(q=1, min=1)  # get framerange of scene to set keys in iteration
getRangemax=cmds.playbackOptions(q=1, max=1)#get framerange of scene to set keys in iteration
# getRange=int(getRange)#change framerange to an integer. May have to change this to a float iterator on a half key blur(butterfly wings)
getmin=int(getmin)
getRangemax=int(getRangemax)
for item in selObj:
    getloc = cmds.spaceLocator(n=item + "cnstr_lctr")
    cmds.normalConstraint(item, getloc[0])
    for each in xrange(getmin, getRangemax):
        getNum="%04d" % (each,)
        placeloc=cmds.spaceLocator(n=item+'FR'+str(getNum)+"_lctr")
        print each, placeloc
        transform=cmds.xform(item, q=True, ws=1, t=True)
        cmds.xform(placeloc[0], ws=1, t=transform)
        cmds.SetKeyTranslate(placeloc[0])
        rotate=cmds.xform(getloc[0], q=True, ws=1, ro=True)
        cmds.xform(placeloc[0], ws=1, ro=rotate)
        cmds.SetKeyRotate(placeloc[0])
        maya.mel.eval( "playButtonStepForward;" )
getparentObj = [cmds.ls(sl=1)[0]]
drivenmesh = cmds.ls(sl=1)[-1]
defnm = "{}_rwrp".format(drivenmesh)
rigmsh = cmds.deformer(type="rigWrap", n=defnm)[0]
for each in getparentObj:
    cmds.connectAttr("{}.worldMesh[0]".format(each), "{}.driverPoints[0]".format(defnm))
cmds.setAttr("{}.bind".format(rigmsh), 1)
cmds.setAttr("{}.searchMethod".format(rigmsh), 3)#sets to vertex



#####select the driven multiple and then the driver last
getparentObj = cmds.ls(sl=1)[-1]
drivenmesh = cmds.ls(sl=1)[:-1]#multidriven
for eachdrvn in drivenmesh:
    defnm = "{}_rwrp".format(eachdrvn)
    rigmsh = cmds.deformer(eachdrvn, type="rigWrap", n=defnm)[0]
    cmds.connectAttr("{}.worldMesh[0]".format(getparentObj), "{}.driverPoints[0]".format(defnm))
    cmds.setAttr("{}.bind".format(rigmsh), 1)
    cmds.setAttr("{}.searchMethod".format(rigmsh), 3)




getparentObj = cmds.ls(sl=1)[0]
drivenmesh = cmds.ls(sl=1)[-1]

defnm = "{}_rwrp".format(drivenmesh)
rigmsh = cmds.deformer(drivenmesh, type="rigWrap", n=defnm)[0]
cmds.connectAttr("{}.worldMesh[0]".format(getparentObj), "{}.driverPoints[0]".format(defnm))
cmds.setAttr("{}.bind".format(rigmsh), 1)
cmds.setAttr("{}.searchMethod".format(rigmsh), 3)#sets to vertex


iknm = 'cThreadStitch_IK'
fstjnt = 'skeleton_:C_threadStitch1_JNT'
getall = cmds.ls('skeleton_:C_threadStitch*_JNT')
crvnm = 'techmesh_:threadStitch_CRV'
gettop = len(getall)
endjnt = 'skeleton_:C_threadStitch{}_JNT'.format(gettop)
hndl = cmds.ikHandle(n = iknm, fj=1, sj = fstjnt, ee = endjnt,sol = 'ikSplineSolver', c=crvnm,rtm=1, tws = 'easIn')[0]
import maya.cmds as cmds
import maya.mel
defname = 'tube_wrp'
cmds.select('techmesh_:tube_length_CRV')
cmds.select('techmesh_:threadCage_PLY', add=1)
maya.mel.eval( "CreateWrap;" )
#cmds.deformer('techmesh_:tube_length_CRV', type="wrap", n=defname)[0]

cmds.duplicate('techmesh_:thread_CRV', n='C_threadMain_CRV')

cmds.deformer('techmesh_:threadCage_PLY', type='curveWarp', n = "thread_crvwrp")
cmds.connectAttr('C_threadMain_CRVShape.worldSpace[0]','thread_crvwrp.inputCurve')import maya.cmds as cmds

'''create a spline ik to drive the joints of the threadPull chain'''

iknm = 'cThreadPull_IK'
fstjnt = 'skeleton_:C_threadPull1_JNT'
getall = cmds.ls('skeleton_:C_threadPull*_JNT')
crvnm = 'techmesh_:threadPull_CRV'
gettop = len(getall)
endjnt = 'skeleton_:C_threadPull{}_JNT'.format(gettop)
hndl = cmds.ikHandle(n = iknm, fj=1, sj = fstjnt, ee = endjnt,sol = 'ikSplineSolver', c=crvnm,rtm=1, tws = 'easIn')[0]

iknm = 'cThreadStitch_IK'
fstjnt = 'skeleton_:C_threadStitch1_JNT'
getall = cmds.ls('skeleton_:C_threadStitch*_JNT')
crvnm = 'techmesh_:threadStitch_CRV'
gettop = len(getall)
endjnt = 'skeleton_:C_threadStitch{}_JNT'.format(gettop)
hndl = cmds.ikHandle(n = iknm, fj=1, sj = fstjnt, ee = endjnt,sol = 'ikSplineSolver', c=crvnm,rtm=1, tws = 'easIn')[0]


'''create a wire wrap to control the main curve driving the deform'''

#cmds.wire('C_threadMain_CRV', gw=0, en= 1.000000, ce=0.000000, li= 0.000000, w= 'techmesh_:thread_CRV')
cmds.wire('techmesh_:threadStitch_CRV', gw=0, en= 1.000000, ce=0.000000, li= 0.000000, w= 'cThreadPull_CRV')




import maya.cmds as cmds
import maya.mel
'''create a spline ik to drive the joints of the threadPull chain'''

leadWire = 'anim_primary_default_default_:defaultBlack_C_threadCurve_CRV'

iknm = 'cThreadPull_IK'
fstjnt = 'skeleton_:C_threadPull1_JNT'
getall = cmds.ls('skeleton_:C_threadPull*_JNT')
crvnm = 'cThreadPull_CRV'
gettop = len(getall)
endjnt = 'skeleton_:C_threadPull{}_JNT'.format(gettop)
hndl = cmds.ikHandle(n = iknm, fj=1, sj = fstjnt, ee = endjnt,sol = 'ikSplineSolver', c=crvnm,rtm=1, tws = 'easIn')[0]
cmds.parent(hndl, 'setup_GRP')

'''create a wire wrap to control the main curve driving the deform'''

cmds.rebuildCurve( leadWire, ch=0, rpo=1, rt=0, end=1, kr=0, kcp=0, kep=0, kt=0, s=150, sm=2, d=2, tol=0.001)
cmds.wire('anim_primary_default_default_:defaultBlack_C_thread_GES', gw=0, en= 1.000000, ce=0.000000, li= 0.000000, w= leadWire)
#cmds.wire('techmesh_:thread_CRV', gw=0, en= 1.000000, ce=0.000000, li= 0.000000, w= 'cThreadPull_CRV')


cmds.addAttr('C_threadBody_CTL', ln='pullThread', min=0, max=700, at="double", k=1, nn='pullThread')
cmds.connectAttr('C_threadBody_CTL.pullThread', "thread_crvwrp.offset", f=1) 

#cmds.select(['techmesh_:threadCage_PLY','techmesh_:threadLength_CRV'], r=1) 
cmds.select('techmesh_:threadLength_CRV')
cmds.select('techmesh_:threadCage_PLY', add=1)
maya.mel.eval( "CreateWrap;" )
#cmds.deformer('techmesh_:threadLength_CRV', type='wire', frontOfChain=True, n='threadLength_wr')[0]

import maya.cmds as cmds
import maya.mel


'''create a spline ik to drive the joints of the threadPull chain'''

leadWire = 'anim_primary_default_default_:defaultBlack_C_threadCurve_CRV'

# iknm = 'cThreadPull_IK'
# fstjnt = 'skeleton_:C_threadPull1_JNT'
# getall = cmds.ls('skeleton_:C_threadPull*_JNT')
# crvnm = 'cThreadPull_CRV'
# gettop = len(getall)
# endjnt = 'skeleton_:C_threadPull{}_JNT'.format(gettop)
# hndl = cmds.ikHandle(n = iknm, fj=1, sj = fstjnt, ee = endjnt,sol = 'ikSplineSolver', c=crvnm,rtm=1, tws = 'easIn')[0]
# cmds.parent(hndl, 'setup_GRP')

'''create a wire wrap to control the main curve driving the deform'''

cmds.rebuildCurve( leadWire, ch=0, rpo=1, rt=0, end=1, kr=0, kcp=0, kep=0, kt=0, s=150, sm=2, d=2, tol=0.001)
cmds.wire('anim_primary_default_default_:defaultBlack_C_thread_GES', n='rope_mesh_wr', gw=0, en= 1.000000, ce=0.000000, li= 0.000000, w= leadWire)
cmds.duplicate('techmesh_:thread_CRV', n="C_threadMainPull_CRV")
cmds.blendShape('techmesh_:thread_CRV', 'C_threadMainPull_CRV', n = "crvblend_bsp", w=(0, 1.0))
cmds.wire('C_threadMainPull_CRV', gw=0, n='ikHandle_wr', en= 1.000000, ce=0.000000, li= 0.000000, w= 'cThreadPull_CRV')


#cmds.select(['techmesh_:threadCage_PLY','techmesh_:threadLength_CRV'], r=1) 
cmds.select('techmesh_:threadLength_CRV')
cmds.select('techmesh_:threadCage_PLY', add=1)
maya.mel.eval( "CreateWrap;" )
#cmds.deformer('techmesh_:threadLength_CRV', type='wire', frontOfChain=True, n='threadLength_wr')[0]
import maya.cmds as cmds
basename = 'cThreadPull'
for each in xrange(1, 5):
    child = '{}{}_CTL'.format(basename, each)
    parentgrp = cmds.listRelatives(child, ap = 1)
    localnosename = '{}{}Ctl_SWCH_GRP'.format(basename, each)
    cmds.CreateEmptyGroup()
    cmds.rename(cmds.ls(sl=1)[0], localnosename)
    getTranslation_nose = cmds.xform(parentgrp, ws=1, q=1, t=1)
    getEndRot_nose = cmds.xform(parentgrp, ws=1, q=1, ro=1)
    cmds.xform(localnosename, ws=1, t=getTranslation_nose)
    cmds.xform(localnosename, ws=1, ro=getEndRot_nose)
    cmds.parent(child, localnosename)
    cmds.parent(localnosename, parentgrp)



'''create a spline ik to drive the joints of the threadPull chain'''

leadWire = 'anim_primary_default_default_:defaultBlack_C_threadCurve_CRV'

iknm = 'cThreadPull_IK'
fstjnt = 'skeleton_:C_threadPull1_JNT'
getall = cmds.ls('skeleton_:C_threadPull*_JNT')
crvnm = 'cThreadPull_CRV'
gettop = len(getall)
endjnt = 'skeleton_:C_threadPull{}_JNT'.format(gettop)
hndl = cmds.ikHandle(n = iknm, fj=1, sj = fstjnt, ee = endjnt,sol = 'ikSplineSolver', c=crvnm,rtm=1, tws = 'easIn')[0]
cmds.parent(hndl, 'setup_GRP')
import maya.cmds as cmds
import maya.mel

leadWire = 'anim_primary_default_default_:defaultBlack_C_threadCurve_CRV'

'''create a wire wrap to control the main curve driving the deform'''

cmds.rebuildCurve( leadWire, ch=0, rpo=1, rt=0, end=1, kr=0, kcp=0, kep=0, kt=0, s=150, sm=2, d=2, tol=0.001)
cmds.wire('anim_primary_default_default_:defaultBlack_C_thread_GES', n='rope_mesh_wr', gw=0, en= 1.000000,  ce=0.000000, li= 0.000000, w= leadWire)
cmds.setAttr('rope_mesh_wr.dropoffDistance[0]', 50)
cmds.duplicate('techmesh_:thread_CRV', n="C_threadMainPull_CRV")
cmds.wire('C_threadMainPull_CRV', gw=0, n='pull_wr', en= 1.000000, ce=0.000000, li= 0.000000, w= 'cThreadPull_CRV')
cmds.wire('C_threadMainPull_CRV', gw=0, n='stitch_wr', en= 1.000000, ce=0.000000, li= 0.000000, w= 'techmesh_:thread_CRV')

'''Set the stitch part of the thread to not take the influence of the ik handle that uses the pull controls'''
cmds.select('C_threadMainPull_CRV.cv[0:80]', r=1)
cmds.percent('pull_wr', v=0 )
cmds.select('C_threadMainPull_CRV.cv[81:122]', r=1)
cmds.percent('stitch_wr', v=0 )
cmds.setAttr('pull_wr.dropoffDistance[0]', 50)
cmds.setAttr('stitch_wr.dropoffDistance[0]', 50)

'''wrap the unravelled sourcing curve with the mesh that will drive it (for the curvewarp) - this is important to have it come from straight to stitched for cleaner wrap'''
cmds.select('techmesh_:threadLength_CRV')
cmds.select('techmesh_:threadCage_PLY', add=1)
maya.mel.eval( "CreateWrap;" )
import maya.cmds as cmds
import maya.mel

'''Create and connect the curve warp deformer to produce unravel effect'''

cmds.deformer('techmesh_:threadCage_PLY', type='curveWarp', n = "thread_crvwrp")
cmds.connectAttr('C_threadMainPull_CRVShape.worldSpace[0]','thread_crvwrp.inputCurve')
cmds.setAttr('thread_crvwrp.maxScale',1)
cmds.setAttr('thread_crvwrp.lengthScale', 1)

'''Creating wire deformer on the thread curve to follow the main effect curve '''
cmds.wire('anim_primary_default_default_:defaultBlack_C_threadCurve_CRV', n='guide_curve_wr', gw=0, en= 1.000000, ce=0.000000, li= 0.000000, w= 'techmesh_:threadLength_CRV')
cmds.setAttr('guide_curve_wr.rotation', 0)
cmds.setAttr('guide_curve_wr.dropoffDistance[0]', 50)

'''Adding and connecting the offset attribute of the curvewarp deformer to the body control'''
cmds.addAttr('C_threadBody_CTL', ln='pullThread', min=0, max=700, at="double", k=1, nn='pullThread')
cmds.connectAttr('C_threadBody_CTL.pullThread', "thread_crvwrp.offset", f=1)
cmds.addAttr('C_threadBody_CTL', ln='lengthThread', min=0, max=700, at="double", k=1, nn='lengthThread')
cmds.connectAttr('C_threadBody_CTL.lengthThread', "thread_crvwrp.lengthScale", f=1)

'''Set visibility state of the main curve to help show visual reference when animating'''
cmds.setAttr('C_threadMainPull_CRV.v', 1)
cmds.select('C_threadMainPull_CRV', r=1)
maya.mel.eval( "TemplateObject;" )
import maya.cmds as cmds


basename = 'cThreadPull'
for each in xrange(1, 5):
    child = '{}{}_CTL'.format(basename, each)
    parentgrp = cmds.listRelatives(child, ap = 1)
    localnosename = '{}{}Ctl_SWCH_GRP'.format(basename, each)
    cmds.CreateEmptyGroup()
    cmds.rename(cmds.ls(sl=1)[0], localnosename)
    getTranslation_nose = cmds.xform(parentgrp, ws=1, q=1, t=1)
    getEndRot_nose = cmds.xform(parentgrp, ws=1, q=1, ro=1)
    cmds.xform(localnosename, ws=1, t=getTranslation_nose)
    cmds.xform(localnosename, ws=1, ro=getEndRot_nose)
    cmds.parent(child, localnosename)
    cmds.parent(localnosename, parentgrp)


class corrective_bs():
    def __init__(self):
##clean maya scene for dispatcher
from maya import cmds
#lists for later:
exempt_list = ['geoShape', 'primary_defaultShape', 'locator_defaultShape']
to_remove = []
#Setup the cleanup group
dup_shape_grp = cmds.ls("*CLEAN_UP*")
if len(dup_shape_grp)<1:
    dup_shape_grp = cmds.CreateEmptyGroup()
    cmds.rename(dup_shape_grp, "CLEAN_UP")
    dup_shape_grp = cmds.ls("*CLEAN_UP*")
else:
    dup_shape_grp = cmds.ls("*CLEAN_UP*")  
###find errant shapes in the sets
etAllSets=[(each) for each in cmds.ls(typ="objectSet")]
for each in getAllSets:
    if cmds.objExists('{}.dispatcher_grouping_settings'.format(each)) == True:
        chld =cmds.sets(each, q=1)
        for ea_chld in chld:
            geo_chld = [(achld) for achld in cmds.sets(ea_chld, q=1) if achld.endswith('_geometry')][0]
            dependnts = [(itm_rm) for itm_rm in cmds.sets(geo_chld, q=1) if itm_rm.endswith('BaseShape') or itm_rm.endswith('Base') or ':' not in itm_rm and 'Orig' not in itm_rm]
            if len(dependnts)>0:
                for itm_to_rm in dependnts:
                    cmds.sets(itm_to_rm, rm=geo_chld)
                    print ("removing {} from dispatcher set {}".format(itm_to_rm, geo_chld)) 
###find errant shapes in the heirarchy and remove
if cmds.objExists(cmds.ls('geo')[0]) == True:
    exempt_ptlist = [(each)for each in cmds.listRelatives(cmds.ls('geo')[0], c=1)]
    for each_shp in exempt_ptlist:
        exempt_list.append(each_shp)
        try:
            exempt_ptlist = cmds.listRelatives(each_shp, s=1, c=1)[0]
            exempt_list.append(exempt_ptlist)
        except:
            pass        
    dependnts = [(each)for each in cmds.listRelatives(cmds.ls('geo')[0], ad=1) if each.endswith('BaseShape') or each.endswith('Base') or ':' not in each and 'Orig' not in each]
    for item in dependnts:        
        if item not in exempt_list:
            to_remove.append(item)
    for item_rem in to_remove:
        if cmds.nodeType(item_rem) == 'shape':
            pass
        else:
            try:
                cmds.parent(item_rem, 'CLEAN_UP')
                print ("moving {} out of the publishing heirarchy. Please find them in the created 'CLEAN_UP' group".format(item_rem))
            except:
                pass

print "┈╭━━━━━━━━━━━─╮♪♫♪♪"
print "┈┃▔▔▔┊┏━┳━┓╭─╮┃♪♫"
print "┈┃╱╱╱┊┃╱┃╱┃┃▏│┃♪♫"
print "╭┻━━┳╯┃╱┃╱┃┃▏│┃♫"
print "┃┛▂┗┊┈┗━┻━┛╰╥╯┃♪"
print "┃╰┻╯┊┈┈┈┈┈┈┈║┈┃"
print "┗▃▃▃▃╭╮▃▃▃▃▃╭╮┘"
print "┈╰╯┈┈╰╯┈┈┈┈┈╰╯"   
         

import maya.cmds as mc
drvnjnt = cmds.ls('skeleton_:C_threadPull*JNT')[1:-1]
print drvnjnt


from blhrig.template import skeletonquad_thread
reload(skeletonquad_thread)

from blhrig.puppet import multicurve_edit
reload(multicurve_edit)

from hourglassrig.puppet import multicurve_edit
reload(multicurve_edit)

from hourglassrig.lib import wavepatterns, skin

skinClusterA_model_anim_primary_default_cBody0001_SKC


cmds.deformer(type="rigWrap")
cmds.connectAttr("polySurface2Shape.worldMesh[0]", "rigWrapNode.driverPoints[0]")
cmds.setAttr("rigWrapNode.bind", 1)

a=['jo', 'ji', 'ja', 'jh']
for nextControl, each in enumerate(a):
    current_item = each
    newitem = each+'_op'
    next_item = a[(newitem + 1) % len(a)]
    print next_item, each
# Build gun bullets if present in scene
from rigtool.bullet import core

core.evaluate_build_all_bullets()

# Set preroll parameters - for creatures only
from rigtool import preroll
from rigtool.preroll import core

preroll.core.pre_roll_enable()
preroll.core.flesh_enable()

# Bake rigSpeedReader nodes
from rigtool.pipeline import speedreader

speedreader.speedreader_bake()

# try to run any show specific hook : myshowrig.rigtool.pipeline.hook.py
try:
    import os
    import importlib

    show_hook_module = importlib.import_module("{}rig.rigtool.pipeline.hook".format(
        os.environ['PL_SHOW']))
    show_hook_module.root_locator_euler_filter()
except:
    pass


import sys
path = '/job/hourglass/common/maya/2022.4/python/hourglassrig/callback'
if path not in sys.path:
    sys.path.append(path)
 
import shapeNetworkQcConnector
widget = shapeNetworkQcConnector.ConnectEyesTeethToShapeNetwork()
widget.connect()


import maya.cmds as cmdsgrp ='render_scalesLayout_default_default_:scales_GRP'
getpartransform = [(each) for each in cmds.listRelatives(grp, ad=1, typ="transform") if "_GE" in each]
cmds.select(getpartransform)
cmds.polyUnite(cmds.ls(sl=1), ch=1, mergeUVSets=1,centerPivot =1, name="scales_GED")
cmds.delete(cmds.ls(sl=1)[0], ch=1)
cmds.parent("scales_GED", "setup_GRP")

snakeOil = cmds.deformer('scales_GED', type = "snakeOil")[0]
cmds.connectAttr ("render_primary_default_default_:skinPurple_C_head_PLY.worldMesh", snakeOil + ".driverMesh")
#cmds.connectAttr ("render_primary_default_default_:skinPurple_C_head_PLYRef.worldMesh", snakeOil + ".driverMeshBind")
cmds.setAttr (snakeOil+'.bindMode',2)
cmds.setAttr ("snakeOil1.rebind", 1)
cmds.setAttr ("snakeOil1.rebind", 0)



getwraps = cmds.ls(type = 'wrap')
for each in getwraps:
    wrapBase = cmds.listConnections('{}.basePoints'.format(each), sh=1,p=0)
    print wrapBase


##bulk change uvset
import maya.cmds as cmds
for each in cmds.ls(sl=1):
    cmds.polyUVSet(uvs="groomUV", cuv=1)
## select parent and then group of individual children to pass on the position based on UV
import maya.cmds as cmds
par = cmds.ls(sl=1)[0]
for each in cmds.ls(sl=1)[1:]:
    cmds.transferAttributes(par, each, transferPositions=1,
    transferNormals=0,
    transferUVs=0,
    transferColors=0,
    sampleSpace=3,
    sourceUvSpace ="groomUV",
    targetUvSpace ="groomUV",
    searchMethod=0,
    flipUVs=0,
    colorBorders=1)


##nuc initiate
import maya.cmds as cmds

getNode=cmds.ls(type="nucleus")
getStartValue=cmds.getAttr(getNode[0]+".startFrame")
getStateValue=cmds.getAttr(getNode[0]+".enable")
getLowRange=cmds.playbackOptions(q=1,min=1)
if getStartValue != getLowRange:
    cmds.setAttr(getNode[0]+".startFrame", getLowRange)
if getStateValue != 1:
    cmds.setAttr(getNode[0]+".enable", 1)
setinit = int(getLowRange)+1
cmds.currentTime(getLowRange)
cmds.currentTime(setinit)
cmds.currentTime(getLowRange)
cmds.select(getNode[0])


##setview muscles
import maya.cmds as cmds
cmds.setAttr("hardwareRenderingGlobals.transparencyAlgorithm", 3)
###intersections
import maya.cmds as cmds
get_sel = cmds.ls(sl=1)
cmds.duplicate()
new_sel = cmds.ls(sl=1)
cmds.polyCBoolOp(new_sel[0], new_sel[1], op=3, ch=0,name=new_sel[0])
new_intersection = cmds.ls(sl=1)[0]
cmds.parent(w=1)

name_shdr_nde = "intersection_colors"
create_shade_node = cmds.shadingNode('lambert', asShader=True, n=name_shdr_nde)
cmds.hyperShade(assign=str(create_shade_node))
lst_sg_node = [create_shade_node]
set_name = 'techanim_textures' 
if cmds.objExists(set_name):
    pass
else:
    cmds.sets(n=set_name, co=3)
cmds.sets(lst_sg_node, add=set_name)
cmds.setAttr('{}.color'.format(name_shdr_nde), 0,1,1, type='double3')
cmds.setAttr('{}.incandescence'.format(name_shdr_nde), 0,1,1, type='double3')




import maya.cmds as cmds
maya_sets=[(each) for each in cmds.ls(typ="objectSet") if 'out_SEL' in each and each.endswith('_initialise')]
for each in maya_sets:
    cmds.sets('nucleus1', add=each)
###intersections
import maya.cmds as cmds
get_sel = cmds.ls(sl=1)
cmds.duplicate()
new_sel = cmds.ls(sl=1)
cmds.polyCBoolOp(new_sel[0], new_sel[1], op=3, ch=0,name=new_sel[0])
new_intersection = cmds.ls(sl=1)[0]

name_shdr_nde = "intersection_colors"
if cmds.objExists(name_shdr_nde) == False:
    create_shade_node = cmds.shadingNode('lambert', asShader=True, n=name_shdr_nde)
    cmds.setAttr('{}.color'.format(name_shdr_nde), 0,1,1, type='double3')
    cmds.setAttr('{}.incandescence'.format(name_shdr_nde), 0,1,1, type='double3')
else:
    cmds.sets(n=set_name, co=3)
cmds.select(new_intersection, r=1)
cmds.hyperShade(assign=str(name_shdr_nde))

lst_sg_node = ['intersection_colors']
set_name = 'techanim_textures' 
if cmds.objExists(set_name):
    pass
else:
    cmds.sets(n=set_name, co=3)
cmds.sets(lst_sg_node, add=set_name)cmds.select(new_intersection, r=1)
try:
    cmds.parent(w=1)
except:
    pass





from maya import cmds, mel

wtsFolder = "/job/gen/dev/character/Krypto/work/edeglau/maya/data/weightmps/shape_attr.xml"
attributes = ['inputAttractPerVertex']
cmds.deformerWeights (wtsFolder,ex=True, sh='simOut_skinGrey_C_bodyskinSlide_PLY:simOut_skinGrey_C_bodyskinSlide_PLYShape', vc=True, at=attributes)

    def bsp_map_apply(self, bds, type_wts):
        # Load smoothSimple
        self._thisDir = os.path.dirname(__file__)
        print self._thisDir
        print os.path.join(self._thisDir,
                                       type_wts,
                                       '%s.wts' % bds)
        wts.load(bds,
                 filePath=os.path.join(self._thisDir,
                                       type_wts,
                                       '%s.wts' % bds))



from maya import cmds, mel
cmds.loadPlugin("rigWeightIO")

wtsFolder = "//job/gen/dev/character/Krypto/work/edeglau/maya/data/wmps/simOut_skinGrey_C_bodyskinSlide_PLY.wts"
cmds.rigWeightImportCmd(f=wtsFolder, m='vertex', a=["skinGrey_C_bodyskinSlide_PLY_CTHShape.inputAttractPerVertex",])


import maya.cmds as cmds
import maya.mel as mm
loadfile = '/job/gen/dev/character/Krypto/work/edeglau/maya/data/wmps/settest2export.wgt'
mm.eval ( 'NClothPaintCallback "Input Attract";' )
cmds.artAttrCtx(cmds.currentCtx(), e=1, ifl=loadfile)



import maya.cmds as cmds
cmds.select(["techMesh_group_:midres_skinPink_C_body_GES", "in_defaultGrey_C_bodyCollideShapeLocal_PLY"], r=1)
cmds.transferAttributes(pos= 1, nml= 0, uvs = 0, col= 0, spa= 3, sus= "map1", tus = "map1", sm= 3,fuv= 0,clb= 1)
cmds.select("in_defaultGrey_C_bodyCollideShapeLocal_PLY", r=1)
cmds.delete(ch=1)








