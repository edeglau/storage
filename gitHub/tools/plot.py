import os, subprocess, sys, platform, logging, signal, webbrowser, urllib, re, getpass, datetime, glob, random, numpy
import maya.cmds as cmds
import maya.mel
import pymel.core as pm
from numpy import arange
from functools import partial
from os  import popen
from sys import stdin
from random import randint
from sys import argv

class plotter_UI(object):

    def plotter_mayaUI(self):
        winName = "Plotter Window 1.0"
        winTitle = winName
        if cmds.window(winName, exists=True):
                cmds.deleteUI(winName)
        window = cmds.window(winName, title=winTitle, tbm=1, w=600, h=220 )
        cmds.menuBarLayout(h=30)
        stringField='''"Plot vertex" - (launches window)if you're familiar with rivets, it's similar except that
    there is no dependency set up. it bakes a locator in space for the animation duration
    to the face or vertex of your choice
        "PLOT VERT"
            * Step 1: Select a vertex
            * Step 2: press "plot" - locator will follow vertex anim
        "PLOT AVERAGES"
            * Step 1: Select multiple vertex
            * Step 2: press "plot each" - locator will follow the center of the selected verts          
        "PLOT OBJECT"
            * Step 1: Select Object
            * Step 2: press "plot each" - locator will follow the object
        "PLOT EACH"
            * Step 1: Select Objects
            * Step 2: press "plot each" - locator will follow multiple objects          
        "ONION"
            * Step 1: Select a vertex
            * Step 2: press "onion" - locators will be created at each frame
        "LOCATE"
            * Step 1: Select a vertex or a group of vertices
            * Step 2: press "locate" - a locator will place in center of selection         
        "OFFSET CACHE"
            * Step 1: Select the follower mesh 
            * Step 2: Select the lead mesh
            * Step 3: press "offset cache" - the cache will follow the new cache position
        "TRANSFORM CACHE"
            * Step 1: Select the mesh meant to move 
            * Step 2: Select the mesh in the preferred location
            * Step 3: press "transform cache" - the cache will move to the new cache position
        "MATCH MATRIX"
            * Step 1: Select the object to move 
            * Step 2: Select the object in the preferred location
            * Step 3: press "match matrix" - the object will move to the new position               
        "RESHAPE TO EDGE"
            * Step 1: Select an uninterrupted edge line of one object
            * Step 2: Select an uninterrupted edge line of another object
            * Step 3: press "reshape to edge" - the second object will be shaped and follow the edge of the first object     
         "RESHAPE TO SHAPE"
            * Step 1: Select an uninterrupted edge line of one object
            * Step 2: Select an uninterrupted edge line of another object
            * Step 3: press "reshape to shape" - the object edges of second object will be aligned and follow the edge of the first object 
        "ALIGN"
            * Step 1: Select a line of verts on one object and exact same number of
                verts on second object
            * Step 2: Set amount that you will want to offset. Leave at "0.0" to snap
                to.
            * Step 3: Set direction of normal to offset: X, Y, Z              
            * Step 4: press "aligne" - this will align the second selection to the first'''
        getDir=["X", "Y", "Z", "XY", "XZ", "YZ"]
        self.fileMenu = cmds.menu( label='Help', pmc=lambda *args:self.helpWin(stringField))         
        cmds.rowColumnLayout  (' selectArrayRow ', nr=1, w=300)
        cmds.frameLayout('LrRow', label='', lv=0, nch=1, borderStyle='out', bv=1, p='selectArrayRow')
        cmds.rowLayout  (' rMainRow ', w=300, numberOfColumns=6, p='LrRow')
        cmds.columnLayout ('selectArrayColumn', parent = 'rMainRow')
        cmds.setParent ('selectArrayColumn')
        cmds.gridLayout('txvaluemeter', p='selectArrayColumn', numberOfColumns=2, cellWidthHeight=(150, 18))            
        cmds.button (label='Plot vert', p='txvaluemeter', command = lambda *args:self._plotter())
        cmds.button (label='Plot averages', p='txvaluemeter', command = lambda *args:self._plotter_avrg())
        cmds.button (label='Plot object', p='txvaluemeter', command = lambda *args:self._plotmattrix())
        cmds.button (label='Plot each', p='txvaluemeter', command = lambda *args:self._plot_each_vert())
        cmds.button (label='Onion', p='txvaluemeter', command = lambda *args:self._onion_skin())
        cmds.button (label='Locate', p='txvaluemeter', command = lambda *args:self.locator_select_verts())
        cmds.button (label='Offset Cache', p='txvaluemeter', command = lambda *args:self.offset_cache())
        cmds.button (label='Transform Cache', p='txvaluemeter', command = lambda *args:self.offset_cache_static())
        cmds.button (label='Match Matrix', p='txvaluemeter', command = lambda *args:self.xformmove())
        cmds.button (label='Reshape to Edge', p='txvaluemeter', command = lambda *args:self.matchCurveShapes())
        cmds.button (label='Reshape to Shape', p='txvaluemeter', command = lambda *args:self.matchFullShape())
        cmds.frameLayout('BRow', label='', lv=0, nch=1, borderStyle='out', bv=1, p='selectArrayRow') 
        cmds.rowColumnLayout( 'vertex_align', p = 'BRow', numberOfColumns=1 ) 
        cmds.text ('Vertice Align', p='vertex_align', bgc=[0.55, 0.6, 0.6])
        # self.zip = cmds.checkBox("Meet")
        cmds.text ('Strength', p='vertex_align')
        self.strength = cmds.textField( w=40, h=25, p='vertex_align', text="1.0")        
        cmds.text ('Bias', p='vertex_align')
        self.bias = cmds.textField( w=40, h=25, p='vertex_align', text="0.5")  
        cmds.gridLayout('txvaluemeter', p='vertex_align', numberOfColumns=2, cellWidthHeight=(150, 18))          
        cmds.text ('Drift', p='txvaluemeter')
        self.direction = cmds.optionMenu( label='Axis', p='txvaluemeter')
        for each in getDir:
            cmds.menuItem( label=each)
        self.amount = cmds.textField( w=40, h=25, p='vertex_align', text="0.0")        
        cmds.button (label='Align', p='vertex_align', command = lambda *args:self._offset_verts(strength=cmds.textField(self.strength, q=1, text=1), amount=cmds.textField(self.amount, q=1, text=1), direction=cmds.optionMenu(self.direction, q=1, v=1), biases=cmds.textField(self.bias, q=1, text=1)))
        cmds.showWindow(window)

    def selection_grab(self):
        '''--------------------------------------------------------------------------------------------------------------------------------------
        Common selection query
        --------------------------------------------------------------------------------------------------------------------------------------'''        
        getSel=cmds.ls(sl=1, fl=1)
        if getSel:
            pass
        else:
            print "You need to make a selection for this tool to operate on."
            return
        return getSel

    def _plotter_avrg(self):
        self.plotter_avrg()
        
    def _plotter(self):
        self.plot_vert()

    def _plotmattrix(self):
        self.plot_matrix()

    def _offset_verts(self, strength, amount, direction, biases):
        self.space_vert(strength, amount, direction, biases)
        
    def _plot_each_vert(self):
        self.plot_each_vert()

    def _onion_skin(self):
        self.onionSkin()      

    def matchCurveShapes(self):
        self.CurveShapes()

    def matchFullShape(self):
        getFirstGrp, getSecondGrp=self.CurveShapes()
        self.matchCurveShapes_andShrinkWrap(getFirstGrp, getSecondGrp)

    def onionSkin(self):
        selObj=cmds.ls(sl=1, fl=1)       
        if len(selObj)==1:
            pass
        else:
            print "Select 1 object" 
        getRange=cmds.playbackOptions(q=1, max=1)#get framerange of scene to set keys in iteration 
        getRange=int(getRange)#change framerange to an integer. May have to change this to a float iterator on a half key blur(butterfly wings)
        for each in range(getRange):
            for item in selObj:
                getloc=cmds.spaceLocator(n=item+"cnstr_lctr")
                cmds.normalConstraint(item, getloc[0])
                getNum="%04d" % (each,)
                placeloc=cmds.spaceLocator(n=item+'FR'+str(getNum)+"_lctr")
                transform=cmds.xform(item, q=True, ws=1, t=True)
                cmds.xform(getloc[0], ws=1, t=transform)  
                cmds.SetKeyTranslate(getloc[0])
                cmds.xform(placeloc[0], ws=1, t=transform)
                cmds.SetKeyTranslate(placeloc[0])               
                rotate=cmds.xform(getloc[0], q=True, ws=1, ro=True)
                cmds.xform(placeloc[0], ws=1, ro=rotate)  
                cmds.SetKeyRotate(placeloc[0])
                maya.mel.eval( "playButtonStepForward;" )
                cmds.delete(getloc[0])

    def plot_each_vert(self):
        '''plots a locator to a vertice or face per keyframe in a timeline'''
        selObj=cmds.ls(sl=1, fl=1)
        for item in selObj:
            cmds.select(item, r=1)
            self.plot_vert()

    def plotter_avrg(self):
        '''plots a locator to a vertice or face per keyframe in a timeline'''
        selObj=cmds.ls(sl=1, fl=1)      
        if len(selObj)>0:
            pass
        else:
            print "Select 1 object" 
            return     
        getTopRange=cmds.playbackOptions(q=1, max=1)+1#get framerange of scene to set keys in iteration 
        getLowRange=cmds.playbackOptions(q=1, min=1)-1#get framerange of scene to set keys in iteration 
        edgeBucket=[]
        getRange=arange(getLowRange,getTopRange, 1 )
        getloc=cmds.spaceLocator(n=selObj[0]+"cnstr_lctr")
        cmds.normalConstraint(selObj[0], getloc[0])
        placeloc=cmds.spaceLocator(n=selObj[0]+"lctr")
        for each in getRange:
            cmds.currentTime(each)            
            transform=cmds.xform(selObj, q=1, ws=1, t=1)
            posBucketx=self.array_median_find(transform[0::3])
            posBuckety=self.array_median_find(transform[1::3])
            posBucketz=self.array_median_find(transform[2::3])
            cmds.xform(getloc[0], ws=1, t=(posBucketx, posBuckety, posBucketz))  
            cmds.SetKeyTranslate(getloc[0])
            cmds.xform(placeloc[0], ws=1, t=(posBucketx, posBuckety, posBucketz))
            cmds.SetKeyTranslate(placeloc[0])               
            rotate=cmds.xform(getloc[0], q=True, ws=1, ro=True)
            cmds.xform(placeloc[0], ws=1, ro=rotate)  
            cmds.SetKeyRotate(placeloc[0])
            cmds.currentTime(each)
        cmds.delete(getloc[0])
        return placeloc[0]

    def plot_vert(self):
        '''plots a locator to a vertice or face per keyframe in a timeline'''
        selObj=cmds.ls(sl=1, fl=1)      
        if len(selObj)>0:
            pass
        else:
            print "Select 1 object" 
            return     
        getTopRange=cmds.playbackOptions(q=1, max=1)+1#get framerange of scene to set keys in iteration 
        getLowRange=cmds.playbackOptions(q=1, min=1)-1#get framerange of scene to set keys in iteration 
        edgeBucket=[]
        getRange=arange(getLowRange,getTopRange, 1 )
        getloc=cmds.spaceLocator(n=selObj[0]+"cnstr_lctr")
        cmds.normalConstraint(selObj[0], getloc[0])
        placeloc=cmds.spaceLocator(n=selObj[0]+"lctr")
        for each in getRange:
            cmds.currentTime(each)            
            transform=cmds.xform(selObj[0], q=True, ws=1, t=True)
            if len(transform)<4:
                pass
            else:
                posBucket=[]
                posBucket.append(self.median_find(transform[0::3]))
                posBucket.append(self.median_find(transform[1::3]))
                posBucket.append(self.median_find(transform[2::3]))
                transform=posBucket
            cmds.xform(getloc[0], ws=1, t=transform)  
            cmds.SetKeyTranslate(getloc[0])
            cmds.xform(placeloc[0], ws=1, t=transform)
            cmds.SetKeyTranslate(placeloc[0])               
            rotate=cmds.xform(getloc[0], q=True, ws=1, ro=True)
            cmds.xform(placeloc[0], ws=1, ro=rotate)  
            cmds.SetKeyRotate(placeloc[0])
            cmds.currentTime(each)
        cmds.delete(getloc[0])


    def _plotter_avrg(self):
        '''plots a locator to a vertice or face per keyframe in a timeline'''
        selObj=cmds.ls(sl=1, fl=1)      
        if len(selObj)>0:
            pass
        else:
            print "Select 1 object" 
            return     
        getTopRange=cmds.playbackOptions(q=1, max=1)+1#get framerange of scene to set keys in iteration 
        getLowRange=cmds.playbackOptions(q=1, min=1)-1#get framerange of scene to set keys in iteration 
        edgeBucket=[]
        getRange=arange(getLowRange,getTopRange, 1 )
        getloc=cmds.spaceLocator(n=selObj[0]+"cnstr_lctr")
        cmds.normalConstraint(selObj[0], getloc[0])
        placeloc=cmds.spaceLocator(n=selObj[0]+"lctr")
        for each in getRange:
            cmds.currentTime(each)            
            transform=cmds.xform(selObj, q=1, ws=1, t=1)
            posBucketx=self.array_median_find(transform[0::3])
            posBuckety=self.array_median_find(transform[1::3])
            posBucketz=self.array_median_find(transform[2::3])
            cmds.xform(getloc[0], ws=1, t=(posBucketx, posBuckety, posBucketz))  
            cmds.SetKeyTranslate(getloc[0])
            cmds.xform(placeloc[0], ws=1, t=(posBucketx, posBuckety, posBucketz))
            cmds.SetKeyTranslate(placeloc[0])               
            rotate=cmds.xform(getloc[0], q=True, ws=1, ro=True)
            cmds.xform(placeloc[0], ws=1, ro=rotate)  
            cmds.SetKeyRotate(placeloc[0])
            cmds.currentTime(each)            

    def median_find(self, lst):
        even = (0 if len(lst) % 2 else 1) + 1
        half = (len(lst) - 1) / 2
        mysum= sum(sorted(lst)[half:half + even]) / float(even)
        return mysum

    def array_median_find(self, lst):
        mysum=numpy.median(numpy.array(lst))
        return mysum            

    def space_vert(self, strength, amount, direction, bias):
        '''offsets a vert from another'''
        strength=float(strength)
        amount=float(amount)
        bias=float(bias)
        selObj=cmds.ls(sl=1, fl=1)   
        firstpart, secondpart = selObj[:len(selObj)/2], selObj[len(selObj)/2:]
        if len(firstpart)==len(secondpart):
            pass
        else:
            print "Odd number in length. Please pick exactly same amount of verts between two rows"
            return
        for leadingVert, followVert in map(None, firstpart, secondpart):
            transform=cmds.xform(leadingVert, q=True, ws=1, t=True)
            transform_follvert=cmds.xform(followVert, q=True, ws=1, t=True)
            #calc x
            xsum = transform[0]-transform_follvert[0]
            startxsum = xsum*bias
            differencesum = 1.0 - bias
            addedsum=xsum*differencesum
            move_xfollow = transform_follvert[0] + startxsum * strength
            move_xlead = transform[0] - addedsum * strength
            ysum = transform[1]-transform_follvert[1]
            startysum = ysum*bias
            differenceysum = 1.0 - bias
            addedysum=ysum*differenceysum 
            move_yfollow = transform_follvert[1] + startysum * strength
            move_ylead = transform[1] - addedysum * strength            
            zsum = transform[2]-transform_follvert[2]
            startzsum = zsum*bias
            differencezsum = 1.0 - bias
            addedzsum=zsum*differencezsum
            move_zfollow = transform_follvert[2] + startzsum * strength
            move_zlead = transform[2] - addedzsum * strength    
            cmds.move(move_xfollow, move_yfollow, move_zfollow, followVert, ws=1)
            cmds.move(move_xlead, move_ylead, move_zlead, leadingVert, ws=1)
            if direction=="X":
                cmds.move(amount, 0.0, 0.0, followVert, r=1, ls=1)
            if direction=="Y":
                cmds.move(0.0, amount, 0.0, followVert, r=1, ls=1)
            if direction=="Z":
                cmds.move(0.0, amount, 0.0, followVert, r=1, ls=1)
            if direction=="XY":
                cmds.move(amount,amount, 0.0, followVert, r=1, ls=1)
            if direction=="XZ":
                cmds.move(amount, 0.0, amount, followVert, r=1, ls=1)
            if direction=="YZ":
                cmds.move(0.0, amount, amount, followVert, r=1, ls=1)
         

    def plot_matrix(self):
        selObj=cmds.ls(sl=1, fl=1)      
        if len(selObj)>0:
            pass
        else:
            print "Select 1 object" 
        getTopRange=cmds.playbackOptions(q=1, max=1)+1#get framerange of scene to set keys in iteration 
        getLowRange=cmds.playbackOptions(q=1, min=1)-1#get framerange of scene to set keys in iteration 
        edgeBucket=[]
        getRange=arange(getLowRange,getTopRange, 1 )
        getloc=cmds.spaceLocator(n=selObj[0]+"cnstr_lctr")
        for each in getRange:
            cmds.currentTime(each)            
            matrix=cmds.xform(selObj[0], q=1, ws=1, m=1)
            cmds.xform(getloc[0], ws=1, m=matrix)       
            cmds.SetKeyTranslate(getloc[0])          
            cmds.SetKeyRotate(getloc[0])
            cmds.currentTime(each)


    def locator_select_verts(self, arg=None):
        selObj=cmds.ls(sl=1, fl=1)
        transform=cmds.xform(selObj, q=1, ws=1, t=1)
        posBucketx=self.median_find(transform[0::3])
        posBuckety=self.median_find(transform[1::3])
        posBucketz=self.median_find(transform[2::3])
        getLoc=cmds.spaceLocator()
        cmds.xform(getLoc[0], t=(posBucketx, posBuckety, posBucketz))
        return getLoc[0]


    def helpWin(self, stringField):
        '''--------------------------------------------------------------------------------------------------------------------------------------
        Interface Layout
        --------------------------------------------------------------------------------------------------------------------------------------'''
        # def helpPage(self, arg=None):
        winName = "Description"
        winTitle = winName
        if cmds.window(winName, exists=True):
                deleteUI(winName)
        window = cmds.window(winName, title=winTitle, tbm=1, w=700, h=400 )
        cmds.menuBarLayout(h=30)
        cmds.rowColumnLayout  (' selectArrayRow ', nr=1, w=700)
        cmds.frameLayout('LrRow', label='', lv=0, nch=1, borderStyle='out', bv=1, p='selectArrayRow')
        cmds.rowLayout  (' rMainRow ', w=700, numberOfColumns=6, p='selectArrayRow')
        cmds.columnLayout ('selectArrayColumn', parent = 'rMainRow')
        cmds.setParent ('selectArrayColumn')
        cmds.gridLayout('txvaluemeter', p='selectArrayColumn', numberOfColumns=2, cellWidthHeight=(700, 400))
        self.list=cmds.scrollField( editable=False, wordWrap=True, ebg=1,bgc=[0.11, 0.15, 0.15], w=700, text=str(stringField))
        cmds.showWindow(window)

    def offset_cache(self):
        checkSel = cmds.ls(sl=1)
        if len(checkSel)<2:
            print "you need to select two objects"
        leader = checkSel[1]
        cmds.select(leader, r=1)
        cmds.ConvertSelectionToVertices(leader)
        ld_lctr = self.plotter_avrg()
        follower = checkSel[0]
        cmds.select(follower, r=1)
        cmds.ConvertSelectionToVertices(follower)
        flw_lctr = self.plotter_avrg()
        # set the offset node for translate
        plsMns = cmds.shadingNode("plusMinusAverage", asUtility = 1)
        cmds.setAttr(plsMns+".operation", 2)
        cmds.connectAttr(ld_lctr+".translate", plsMns+".input3D[0]", f=1)
        cmds.connectAttr(flw_lctr+".translate", plsMns+".input3D[1]", f=1)
        # set cluster
        cmds.select(checkSel[0])
        getpar=cmds.listRelatives(checkSel[0], p=1)
        getchildren=[(nodes) for nodes in cmds.listRelatives(getpar[0], ad=1, type="mesh") if "Orig" not in str(nodes) ]
        cmds.select(getchildren, add =1 )
        create_cstr = cmds.cluster()
        # connect result to cluster
        cmds.connectAttr( plsMns+".output3D", create_cstr[0]+"Handle.translate", f = 1)

    def offset_cache_static(self):
        checkSel = cmds.ls(sl=1)
        if len(checkSel)<2:
            print "you need to select two objects"
        leader = checkSel[1]
        cmds.select(leader, r=1)
        cmds.ConvertSelectionToVertices(leader)
        ld_lctr = self.locator_select_verts()
        follower = checkSel[0]
        cmds.select(follower, r=1)
        cmds.ConvertSelectionToVertices(follower)
        flw_lctr = self.locator_select_verts()
        # set the offset node for translate
        plsMns = cmds.shadingNode("plusMinusAverage", asUtility = 1)
        cmds.setAttr(plsMns+".operation", 2)
        cmds.connectAttr(ld_lctr+".translate", plsMns+".input3D[0]", f=1)
        cmds.connectAttr(flw_lctr+".translate", plsMns+".input3D[1]", f=1)
        # set cluster
        cmds.select(checkSel[0])
        getpar=cmds.listRelatives(checkSel[0], p=1)
        getchildren=[(nodes) for nodes in cmds.listRelatives(getpar[0], ad=1, type="mesh") if "Orig" not in str(nodes) ]
        cmds.select(getchildren, add =1 )
        create_cstr = cmds.cluster()
        # connect result to cluster
        cmds.connectAttr( plsMns+".output3D", create_cstr[0]+"Handle.translate", f = 1)

    def CurveShapes(self):
        getSel=self.selection_grab()
        if getSel:
            pass
        else:
            return
        getNames=cmds.ls(sl=1, fl=1)
        if ".e[" not in str(getNames[0]):
            print "selection needs to be continuous edges of two seperate polygon objects: first select one, then continuous edge and then the continuous edge on a seperate poly object that you want to deform it along"
            return
        else:
            pass
        getFirstGrp = getNames[0].split(".")[0]
        getSecondGrp = getNames[-1:][0].split(".")[0]
        if getFirstGrp == getSecondGrp:
            print "Only one poly object has been detected. Select one object and it's continuous edge and then select another object and select it's continuous edge for the first object to align to."
            return
        else:
            pass
        firstList=[(each) for each in getNames if each.split(".")[0]==getFirstGrp]
        secondList=[(each) for each in getNames if each.split(".")[0]==getSecondGrp]
        '''create childfirst curve'''
        cmds.select(firstList)
        cmds.CreateCurveFromPoly()
        getFirstCurve=cmds.ls(sl=1, fl=1)
        '''get cv total of curve'''
        getFirstCurveInfo=cmds.ls(sl=1, fl=1)
        numberCV=str(pm.PyNode(getFirstCurveInfo[0]).numCVs())
        cmds.delete(getFirstCurve[0], ch=1)
        '''wrap child mesh to curve'''
        cmds.select(cmds.ls(getFirstGrp)[0], r=1)
        cmds.wire(w=getFirstCurve[0], gw=0, en=1.000000, ce=0.000000, li=0.000000, dds=[(0, 500)] )
        '''create parent curve'''
        cmds.select(secondList)
        cmds.CreateCurveFromPoly()
        getSecondCurve=cmds.ls(sl=1, fl=1)
        getSecondCurveInfo=cmds.ls(sl=1, fl=1)
        '''rebuilt curve to match first curve built'''
        cmds.rebuildCurve(getSecondCurve[0], getFirstCurve[0], rt=2 )
        getSecondCurve=cmds.ls(sl=1, fl=1)
        getSecondCurveInfo=cmds.ls(sl=1, fl=1)
        cmds.delete(getSecondCurve[0], ch=1)
        '''wrap parent curve to parent mesh'''
        cmds.select(getSecondCurve[0], r=1)
        cmds.select(cmds.ls(getSecondGrp)[0], add=1)
        cmds.CreateWrap()
        '''blend child curve to parent curve'''
        cmds.blendShape(getSecondCurve[0], getFirstCurve[0],w=(0, 1.0))
        return getFirstGrp, getSecondGrp


    def matchCurveShapes_andShrinkWrap(self, getFirstGrp, getSecondGrp):
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
        cmds.delete(getFirstGrp, ch=1)
        getShrink=cmds.deformer(getFirstGrp, type="shrinkWrap")
        cmds.connectAttr(getSecondGrp+".worldMesh[0]", getShrink[0]+".targetGeom", f=1)
        for key, value in myDict.items():
            cmds.setAttr(getShrink[0]+key, value)

    def xformmove(self):
        '''move to matrix'''
        objSel=cmds.ls(sl=1)
        matrix=cmds.xform(objSel[1], q=1, ws=1, m=1)
        cmds.xform(objSel[0], ws=1, m=matrix)   
        cmds.select(objSel[0])
