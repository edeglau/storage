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
        "PLOT"
            * Step 1: Select a vertex
            * Step 2: press "plot" - locator will follow vertex anim
        "PLOT EACH"
            * Step 1: Select multiple vertex
            * Step 2: press "plot each" - locator will follow each vertex anim
        "ONION"
            * Step 1: Select a vertex
            * Step 2: press "onion" - locators will be created at each frame
        "LOCATE"
            * Step 1: Select a vertex or a group of vertices
            * Step 2: press "locate" - a locator will place in center of selection
        "ALIGN"
            * Step 1: Select a line of verts on one object and exact same number of
                verts on second object
            * Step 2: Set amount that you will want to offset. Leave at "0.0" to snap
                to.
            * Step 3: Set direction of normal to offset: X, Y, Z              
            * Step 4: press "aligne" - this will align the second selection to the first'''
        getDir=["X", "Y", "Z"]
        self.fileMenu = cmds.menu( label='Help', pmc=lambda *args:self.helpWin(stringField))         
        rowColumnLayout  (' selectArrayRow ', nr=1, w=300)
        frameLayout('LrRow', label='', lv=0, nch=1, borderStyle='out', bv=1, p='selectArrayRow')
        rowLayout  (' rMainRow ', w=300, numberOfColumns=6, p='selectArrayRow')
        columnLayout ('selectArrayColumn', parent = 'rMainRow')
        setParent ('selectArrayColumn')
        cmds.gridLayout('txvaluemeter', p='selectArrayColumn', numberOfColumns=2, cellWidthHeight=(150, 18))            
        button (label='plot', p='txvaluemeter', command = lambda *args:self._plotter())
        button (label='plot each', p='txvaluemeter', command = lambda *args:self._plot_each_vert())
        button (label='onion', p='txvaluemeter', command = lambda *args:self._onion_skin())
        button (label='locate', p='txvaluemeter', command = lambda *args:self.locator_select_verts())
        self.amount=cmds.textField( w=40, h=25, p='txvaluemeter', text="0.0")        
        self.direction=cmds.optionMenu( label='Attributes')
        for each in getDir:
            cmds.menuItem( label=each)       
        button (label='offset', p='txvaluemeter', command = lambda *args:self._offset_verts(amount=cmds.textField(self.amount, q=1, text=1), direction=cmds.optionMenu(self.direction, q=1, v=1)))        
        showWindow(window)


    def _plotter(self, arg=None):
        getBaseClass.plot_vert()


    def _offset_verts(self, amount, direction):
        getBaseClass.space_vert(amount, direction)
        
    def _plot_each_vert(self, arg=None):
        getBaseClass.plot_each_vert()

    def _onion_skin(self, arg=None):
        getBaseClass.onionSkin()


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
