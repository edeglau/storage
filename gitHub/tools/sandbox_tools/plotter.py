class PlotterWindow(self):

    def vertex_UI(self, arg=None):
        winName = "vertex"
        winTitle = winName
        if cmds.window(winName, exists=True):
                deleteUI(winName)
        window = cmds.window(winName, title=winTitle, tbm=1, w=300, h=100 )
        menuBarLayout(h=30)
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
            * Step 3: press "reshape to edge" - the second object will be shaped and follow 
                the edge of the first object     
         "RESHAPE TO SHAPE"
            * Step 1: Select an uninterrupted edge line of one object
            * Step 2: Select an uninterrupted edge line of another object
            * Step 3: press "reshape to shape" - the object edges of second object will be 
                aligned and follow the edge of the first object 
        "ALIGN"
            * Step 1: Select a line of verts on one object and exact same number of
                verts on second object
            * Step 2: Set amount that you will want to offset. Leave at "0.0" to snap
                to.
            * Step 3: Set direction of normal to offset: X, Y, Z              
            * Step 4: press "aligne" - this will align the second selection to the first
        "INTERSECTION FIX"
            * Step 1: Select two objects as you would performing any shrinkwrap             
            * Step 2: press "Intersection fix" - this will set a shrink wrap that will
                only affect the area
            '''
        getDir=["X", "Y", "Z"]
        self.fileMenu = cmds.menu( label='Help', pmc=lambda *args:self.helpWin(stringField))         
        rowColumnLayout  (' selectArrayRow ', nr=1, w=300)
        frameLayout('LrRow', label='', lv=0, nch=1, borderStyle='out', bv=1, p='selectArrayRow')
        rowLayout  (' rMainRow ', w=300, numberOfColumns=6, p='selectArrayRow')
        columnLayout ('selectArrayColumn', parent = 'rMainRow')
        setParent ('selectArrayColumn')
        cmds.gridLayout('txvaluemeter', p='selectArrayColumn', numberOfColumns=2, cellWidthHeight=(150, 18))            
        cmds.button (label='Plot averages', p='txvaluemeter', command = lambda *args:self.plotter_avrg())
        cmds.button (label='Plot object', p='txvaluemeter', command = lambda *args:self.plot_matrix())
        cmds.button (label='Plot each', p='txvaluemeter', command = lambda *args:self.plot_each_vert())
        cmds.button (label='Onion', p='txvaluemeter', command = lambda *args:self._onion_skin())
        cmds.button (label='Locate', p='txvaluemeter', command = lambda *args:self.locator_select_verts())
        cmds.button (label='Offset Cache', p='txvaluemeter', command = lambda *args:self.offset_cache())
        cmds.button (label='Transform Cache', p='txvaluemeter', command = lambda *args:self.offset_cache_static())
        cmds.button (label='Match Matrix', p='txvaluemeter', command = lambda *args:self.xformmove())
        cmds.button (label='Reshape to Edge', p='txvaluemeter', command = lambda *args:self.matchCurveShapes())
        cmds.button (label='Reshape to Shape', p='txvaluemeter', command = lambda *args:self.matchFullShape())
        cmds.button (label='Intersection Fix', p='txvaluemeter', command = lambda *args:self.shrink_intersections())
        self.amount=cmds.textField( w=40, h=25, p='txvaluemeter', text="0.0")        
        self.direction=cmds.optionMenu( label='Attributes')
        for each in getDir:
            cmds.menuItem( label=each)       
        button (label='offset', p='txvaluemeter', command = lambda *args:self._offset_verts(amount=cmds.textField(self.amount, q=1, text=1), direction=cmds.optionMenu(self.direction, q=1, v=1)))        
        showWindow(window)
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

    
    def matchCurveShapes(self):
        self.CurveShapes()

    def matchFullShape(self):
        getFirstGrp, getSecondGrp=self.CurveShapes()
        self.matchCurveShapes_andShrinkWrap(getFirstGrp, getSecondGrp)
        
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
        
    def xformmove(self):
        '''move to matrix'''
        objSel=cmds.ls(sl=1)
        matrix=cmds.xform(objSel[1], q=1, ws=1, m=1)
        cmds.xform(objSel[0], ws=1, m=matrix)   
        cmds.select(objSel[0])
        
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
    def _plotter(self, arg=None):
        getBaseClass.plot_vert()


    def _offset_verts(self, amount, direction):
        getBaseClass.space_vert(amount, direction)
        
    def _plot_each_vert(self, arg=None):
        getBaseClass.plot_each_vert()

    def _onion_skin(self, arg=None):
        getBaseClass.onionSkin()
    
    def locator_select_verts(self, arg=None):
        selObj=cmds.ls(sl=1, fl=1)
        transform=cmds.xform(selObj, q=1, ws=1, t=1)
        posBucketx=self.median_find(transform[0::3])
        posBuckety=self.median_find(transform[1::3])
        posBucketz=self.median_find(transform[2::3])
        getLoc=cmds.spaceLocator()
        cmds.xform(getLoc[0], t=(posBucketx, posBuckety, posBucketz))
        return getLoc[0]
    
    def store_obj_matrix_pt(self, objectSel, fileName):
        '''plots transforms off of an object with constraint to a text file'''
        objectSel=cmds.ls(sl=1)
        if len(objectSel)>0:
            pass
        else:
            print "Select 1 object" 
            return     
        fileName=fileName+'.txt'
        print fileName
        if "Windows" in OSplatform:
            if not os.path.exists(fileName): os.makedirs(fileName)
        if "Linux" in OSplatform:
            inp=open(fileName, 'w+')
        getTopRange=cmds.playbackOptions(q=1, max=1)+1#get framerange of scene to set keys in iteration 
        getLowRange=cmds.playbackOptions(q=1, min=1)-1#get framerange of scene to set keys in iteration 
        getRange=arange(getLowRange,getTopRange, 1 )
        collection_of_valueTX={}
        collection_of_valueTY={}
        collection_of_valueTZ={}
        collection_of_valueRX={}
        collection_of_valueRY={}
        collection_of_valueRZ={}
        for each_obj in objectSel:            
            inp.write('\n'+str(each_obj)+">>")        
            for each_frame in getRange:
                cmds.currentTime(each_frame)            
                transform=cmds.xform(each_obj, q=True, ws=1, t=True)
                rotation=cmds.xform(each_obj, q=True, ws=1, ro=True)
                if len(transform)<4:
                    pass
                else:
                    posBucket=[]
                    posBucket.append(self.median_find(transform[0::3]))
                    posBucket.append(self.median_find(transform[1::3]))
                    posBucket.append(self.median_find(transform[2::3]))
                    transform=posBucket
                # print str(each_frame)+":"+str(transform[0])
                makeDictTX = {each_frame:transform[0]}
                collection_of_valueTX.update(makeDictTX)
                makeDictTY = {each_frame:transform[1]}
                collection_of_valueTY.update(makeDictTY)
                makeDictTZ = {each_frame:transform[2]}
                collection_of_valueTZ.update(makeDictTZ)
                makeDictRX = {each_frame:rotation[0]}
                collection_of_valueRX.update(makeDictRX)
                makeDictRY = {each_frame:rotation[1]}
                collection_of_valueRY.update(makeDictRY)
                makeDictRZ = {each_frame:rotation[2]}
                collection_of_valueRZ.update(makeDictRZ)
                cmds.currentTime(each_frame)
            inp.write("<translateX;")
            inp.write(str(collection_of_valueTX))
            inp.write("<translateY;")
            inp.write(str(collection_of_valueTY))
            inp.write("<translateZ;")
            inp.write(str(collection_of_valueTZ))
            inp.write("<rotateX;")
            inp.write(str(collection_of_valueRX))
            inp.write("<rotateY;")
            inp.write(str(collection_of_valueRY))
            inp.write("<rotateZ;")
            inp.write(str(collection_of_valueRZ))
        inp.close()


    def plot_matrix(self):
        from numpy import arange
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
        # getRange=cmds.playbackOptions(q=1, max=1)#get framerange of scene to set keys in iteration 
        # getRange=int(getRange)#change framerange to an integer. May have to change this to a float iterator on a half key blur(butterfly wings)
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
            # maya.mel.eval( "playButtonStepForward;" )
        cmds.delete(getloc[0])

    def shrink_intersections(self):
        myDict={
        ".alongX":0,
        ".alongY":0,
        ".alongZ":0,
        ".axisReference":0,
        ".bidirectional":0,
        ".boundaryRule":1,
        ".boundingBoxCenter":1,
        ".caching":0,
        ".closestIfNoIntersection":0,
        ".continuity":1.0,
        ".envelope":1.0,
        ".falloff":0.4185185189,
        ".falloffIterations":54,
        ".fchild1":0,
        ".fchild2":0,
        ".fchild3":0,
        ".frozen":0,
        ".innerGeom":0,
        ".innerGroupId":0,
        ".inputEnvelope":[()],
        ".isHistoricallyInteresting":2,
        ".keepBorder":0,
        ".keepHardEdge":0,
        ".keepMapBorders":1,
        ".nodeState":0,
        ".offset":0.03237410082,
        ".projection":1,
        ".propagateEdgeHardness":0,
        ".reverse":1,
        ".shapePreservationEnable":0,
        ".shapePreservationIterations":1,
        ".shapePreservationMethod":0,
        ".shapePreservationReprojection":0,
        ".shapePreservationSteps":1,
        ".smoothUVs":1,
        ".targetGeom":0,
        ".targetInflation":0.06115107902,
        ".targetSmoothLevel":1,
        }
        getSel=self.selection_grab()
        if getSel:
            pass
        else:
            return
        getShrink=cmds.deformer(getSel[0], type="shrinkWrap")
        cmds.connectAttr(getSel[1]+".worldMesh[0]", getShrink[0]+".targetGeom", f=1)
        for key, value in myDict.items():
            try:
                cmds.setAttr(getShrink[0]+key, value)        
            except:
                pass
    def plot_each_vert(self):
        '''plots a locator to a vertice or face per keyframe in a timeline'''
        selObj=cmds.ls(sl=1, fl=1)
        for item in selObj:
            cmds.select(item, r=1)
            self.plot_vert()


    def space_vert(self, amount, direction):
        '''offsets a vert from another'''
        amount=float(amount)
        selObj=cmds.ls(sl=1, fl=1)   
        firstpart, secondpart = selObj[:len(selObj)/2], selObj[len(selObj)/2:]
        if len(firstpart)==len(secondpart):
            pass
        else:
            print "Odd number in length. Please pick exactly same amount of verts between two rows"
            return
        for leadingVert, followVert in map(None, firstpart, secondpart):
            # getloc=cmds.spaceLocator(n=leadingVert+"cnstr_lctr")
            transform=cmds.xform(leadingVert, q=True, ws=1, t=True)
            # cmds.xform(getloc[0], ws=1, t=transform)  
            # cmds.normalConstraint(leadingVert, getloc[0])
            # cmds.duplicate(getloc[0], rr=1, n="temp_cnstr_lctr")
            if direction=="X":
                cmds.move(transform[0], transform[1], transform[2], followVert, ws=1)
                cmds.move(amount, 0.0, 0.0, followVert, r=1, ls=1)
            if direction=="Y":
                cmds.move(transform[0], transform[1]+amount, transform[2], followVert, os=1, ls=1)
            if direction=="Z":       
                cmds.xform(followVert, ws=1, t=transform)        
                # cmds.move(transform[0], transform[1], transform[2], followVert, ws=1)
                cmds.move(0.0, 0.0, amount, followVert, r=1, ls=1)                
                    # cmds.move(transform[0], transform[1], transform[2]+amount, followVert, os=1, ls=1)
            # offsetTransform=cmds.xform("temp_cnstr_lctr", q=True, ws=1, t=True)
            # cmds.xform(followVert, ws=1, t=offsetTransform)
            # cmds.delete("temp_cnstr_lctr")
            # cmds.delete(getloc[0])


    def space_vertV1(self):
        '''offsets a vert from another'''
        amount=float(amount)
        if direction=="X":
            moveVert=[amount, 0.0, 0.0]
        if direction=="Y":
            moveVert=0.0, amount, 0.0
        if direction=="Z":
            moveVert=0.0, 0.0, amount
        selObj=cmds.ls(sl=1, fl=1)   
        firstpart, secondpart = selObj[:len(selObj)/2], selObj[len(selObj)/2:]
        if len(firstpart)==len(secondpart):
            pass
        else:
            print "Odd number in length. Please pick exactly same amount of verts between two rows"
            return
        for leadingVert, followVert in map(None, firstpart, secondpart):
            getloc=cmds.spaceLocator(n=leadingVert+"cnstr_lctr")
            transform=cmds.xform(leadingVert, q=True, ws=1, t=True)
            cmds.xform(getloc[0], ws=1, t=transform)  
            cmds.normalConstraint(leadingVert, getloc[0])
            cmds.duplicate(getloc[0], rr=1, n="temp_cnstr_lctr")
            cmds.move(moveVert[0], moveVert[1], moveVert[2], "temp_cnstr_lctr", r=1, ls=1)
            offsetTransform=cmds.xform("temp_cnstr_lctr", q=True, ws=1, t=True)
            cmds.xform(followVert, ws=1, t=offsetTransform)
            cmds.delete("temp_cnstr_lctr")
            cmds.delete(getloc[0])



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



    def Percentages(self, getSel, minValue, maxValue):
        collectNewNumbers=[]  
        '''add first value to bucket'''
        collectNewNumbers.append(minValue)  
        '''find incremental percentile to add to bucket'''
        getSeln=getSel[1:-1]#isolate midrange selection
        RangeSel=getSel[:-1]#isolate all but the last (full 100%) list item
        findRangeSpace=maxValue-minValue#find difference of range            
        percentTop=findRangeSpace*100#find the 100% value that could be added to the minimum range to reach the maximum cap amount
        getPercentile=percentTop/len(RangeSel)#divide the cap by the ranged list length to find the incremented value
        BucketValue=[(key+1)*getPercentile*.01 for key in range(len(getSeln))]#reference the mid list length to append the incremented value to bucket
        for each in BucketValue:#Add each value to the minimum number to get true value to add to bucket
            getNum=minValue+each
            collectNewNumbers.append(getNum)
        '''add last value to bucket'''
        collectNewNumbers.append(maxValue)
        return collectNewNumbers
