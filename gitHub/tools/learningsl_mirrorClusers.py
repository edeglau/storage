#Author: ShaoLei
#email: woshishaolei@qq.com
#QQ:364925474

from maya.cmds import *

#the main func
def sl_mirroClusterPitch(meshObj,clusterHandle,deriction):
    meshs = listRelatives(meshObj,s = 1,c = 1)
    oldList = sl_mirroClusterFilter(meshObj,clusterHandle)

    for pair in oldList:
        
        pointPos = pointPosition(pair[0],l = 1)

        node = createNode('closestPointOnMesh')

        if deriction == 1:
            
            setAttr((node + ".inPosition"),-pointPos[0],pointPos[1],pointPos[2])
        elif deriction == 2:
            setAttr((node + ".inPosition"),pointPos[0],-pointPos[1],pointPos[2])
        else:
            setAttr((node + ".inPosition"),pointPos[0],pointPos[1],-pointPos[2])

        try:
            connectAttr((meshs[0] + ".outMesh"),(node + ".inMesh"),f = 1)
            select(cl = 1)
        except:
            pass
        num = getAttr((node + ".closestVertexIndex"))
        newPoint = (meshObj + ".vtx[" + str(num) + "]")
        pair[0] = newPoint
        delete(node)
    amount = len(oldList)
    newPoints = [oldList[x][0] for x in range(amount)]

    clusDeformer = listConnections((clusterHandle + ".worldMatrix[0]"),type ="cluster",d = 1)
    rela = getAttr((clusDeformer[0] + ".relative"))
    newClus = cluster(newPoints, n = ("mirro" + clusDeformer[0]),rel = rela )

    #deal with the cluster weight

    for x in range (amount):
        percent(newClus[0],oldList[x][0],v = oldList[x][1])

    print("done")

#this func is in order to getting all vertex and its value of a cluster
#require one preferences
    
def sl_mirroClusterDefine(clusterHandle):
    
    clusDeformer = listConnections((clusterHandle + ".worldMatrix[0]"),type ="cluster",d = 1)

    clusSets = listConnections(clusDeformer[0], type = "objectSet" );

    components = sets(clusSets[0],q = 1)

    components = filterExpand(components,sm = (28,31,36,46))
    backTo = []
    for vertex in components:
        pair = [vertex]       
        valueW = percent(clusDeformer[0],vertex,q = 1,v = 1)
        pair.append(valueW[0])
        backTo.append(pair)

    return backTo

#sometime, a cluster may effect several object
#in order to removing the unwanted vertexs,I create this func

def sl_mirroClusterFilter(meshObj,clusterHandle):
    CODEC = 'utf-8'
    backTo = sl_mirroClusterDefine(clusterHandle)
    returnTo = []

    for pair in backTo:
        name = pair[0].encode(CODEC)

        if name.startswith(meshObj):
            returnTo.append(pair)
    return returnTo

# this is UI

def sl_mirroClusterUI():
    winname = "sl_mirroClusterUI"
    if window(winname,q= 1,exists = 1):
        deleteUI(winname)
    window(winname,wh = [300,188],t = winname)

    columnLayout(adj = 1)

    textF1 = textFieldButtonGrp(l = "object",bl = "sel",columnAlign3 = ["right","right","right"],cw3 = [50,200,100])

    textFieldButtonGrp(textF1, e = 1 ,bc = ("sl_addSelToTextField('" + textF1 + "')"))

    #===================================
    text(" ")
    separator(bgc = (0.5,0.5,0.5),h = 5 , style = "none")

    textF2 = textFieldButtonGrp(l = "cluster",bl = "sel",columnAlign3 = ["right","right","right"],cw3 = [50,200,100])

    textFieldButtonGrp(textF2, e = 1 ,bc = ("sl_addSelToTextField('" + textF2 + "')"))

    #===================================
    text(" ")
    separator(bgc = (0.5,0.5,0.5),h = 5 , style = "none")

    radios = radioButtonGrp(nrb = 3,sl = 1, l = "mirroDirection", labelArray3 = ["x","y","z"],columnAlign4 = ["right","left","left","left"],cw4 = [100,50,50,50])

    #===================================
    text(" ")
    separator(bgc = (0.5,0.5,0.5),h = 5 , style = "none")
    rowColumnLayout(nc = 2,cw = [(1,140),(2,140)])

    bt1 = button(l = "Mirro",c = (("sl_mirroClusterPre('" + textF1 + "','" + textF2 + "','" + radios + "')")))

    bt2 = button(l = "Cancel",c = (("deleteUI('" + winname + "')")))

    showWindow(winname)


#ready to go
    
def sl_mirroClusterPre(textF1,textF2,radios):

    meshObj = textFieldButtonGrp(textF1,q = 1,text = 1)

    clusterHandle = textFieldButtonGrp(textF2,q = 1,text = 1)

    deriction = radioButtonGrp(radios,q = 1,sl = 1)

    sl_mirroClusterPitch(meshObj,clusterHandle,deriction)
    
#<_>==============================

def sl_addSelToTextField(textFieldss):

    obj = ls(sl = 1)

    textFieldButtonGrp(textFieldss,e = 1,text = obj[0])
    
sl_mirroClusterUI()
