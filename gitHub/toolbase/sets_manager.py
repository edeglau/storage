import maya.cmds as cmds
import maya.mel
class setMemUI(object):




    def __init__(self, winName="Membership Sets"):
        self.winTitle = "Membership Sets"
        self.winName = winName



    # def _sets_win(self):
        if cmds.window(self.winName, exists=True):
                cmds.deleteUI(self.winName)
        self.window = cmds.window(self.winName, title=self.winTitle, tbm=1, w=270, h=550 )

        Name="Sets"
        annot="Select vertices and then select set from drop down. Select add to or remove from set"
        '''--------------------------------------------------------------------------------------------------------------------------------------
        This is the sets window interface
        --------------------------------------------------------------------------------------------------------------------------------------'''   
        
        listLayout='setslistLayout'
        rowColumnLayout='windowMenuRow'
        windowColumnLayout='windowMenuColumn'
        listBuildLayout='listBuildLayout'
        listName='mySets'        
        cmds.menuBarLayout(h=30)
        stringField='''"Membership Sets" - (launches window)this tool allows for adding and subtracting of verts to a
    blenshape or a dynamic constraint set or a regular objectSet
        * Step 1: Set the type of set from the drop down menu
        * Step 2: Select a name from the second drop down
        * Step 3: Select objects/verts
        * Step 4: add or remove  '''        self.fileMenu = cmds.menu( label='Help', hm=1, pmc=lambda *args:self.helpWin(stringField))            
        cmds.rowColumnLayout  (rowColumnLayout, nr=1, w=530)
        cmds.frameLayout('frameLayout', label='', lv=0, nch=1, borderStyle='out', bv=1, p=rowColumnLayout)
        cmds.rowLayout  ('rowLayout', w=600, numberOfColumns=6, p=rowColumnLayout)
        cmds.columnLayout (windowColumnLayout, p= 'rowLayout')
#         cmds.setParent (windowColumnLayout)
        cmds.separator(h=10, p=windowColumnLayout)
        cmds.gridLayout(listBuildLayout, p=windowColumnLayout, numberOfColumns=1, cellWidthHeight=(530, 20))
        self.getSetTyp=cmds.optionMenu( label='Set Type', cc=lambda *args:self.change_set(), w=120, ann="Select set type to edit(Dynamic ncloth constraints or Blenshape memberships)")
        cmds.menuItem( label="Deformer sets")       
        cmds.menuItem( label="Dynamic sets")
        cmds.menuItem( label="Set memberships")
        self.setNames=cmds.optionMenu(label='Set Name') 
        cmds.gridLayout('setBuildButtonLayout', p='windowMenuColumn', numberOfColumns=3, cellWidthHeight=(150, 20))
        cmds.button (label='Add to set', p='setBuildButtonLayout', command = lambda *args:self._add_to_set(querySet=cmds.optionMenu(self.setNames, q=1, v=1)))
        cmds.button (label='remove from set', p='setBuildButtonLayout', command = lambda *args:self._remove_from_set(querySet=cmds.optionMenu(self.setNames, q=1, v=1)))
        # cmds.button (label='refresh', p='setBuildButtonLayout', command = lambda *args:self._refresh())
        cmds.showWindow(self.window)


    def _refresh(self):
        titleName="Membership Sets"        
        winName = titleName
        winTitle = winName
        if cmds.window(winName, exists=True):
                cmds.deleteUI(winName)        
        self._sets_win()

    def change_set(self):
        '''----------------------------------------------------------------------------------
        -----------------------------------------------------------------------        deformSets=["blendShape", "cluster"]
        memberSets=["transform"]
        getSetType=cmds.optionMenu(self.getSetTyp, q=1, v=1)  
        if getSetType=="Dynamic sets":
            menuItems = cmds.optionMenu(self.setNames, q=True, ill=True)
            if menuItems:
                cmds.deleteUI(menuItems)             
            getAllSets=[(each) for each in cmds.ls(typ="dynamicConstraint")]
            cmds.optionMenu(self.setNames, e=1)
            for each in getAllSets:
                cmds.menuItem( label=each)   
        elif getSetType=="Deformer sets":
            menuItems = cmds.optionMenu(self.setNames, q=True, ill=True)
            if menuItems:
                cmds.deleteUI(menuItems)             
            getAllSets=[(each) for each in cmds.ls(typ="objectSet")]
            collectBlendSets=[]
            for each in getAllSets:
                try:
                    keepEach=[(connectedObj) for connectedObj in cmds.listConnections(each, s=1) for eachDeform in deformSets if cmds.nodeType(connectedObj) ==eachDeform]
                    if keepEach:
                        collectBlendSets.append(each)
                except:
                    pass
            cmds.optionMenu(self.setNames, e=1)
            for each in collectBlendSets:
                cmds.menuItem( label=each)
        elif getSetType=="Set memberships":                
            menuItems = cmds.optionMenu(self.setNames, q=True, ill=True)
            if menuItems:
                cmds.deleteUI(menuItems)             
            getAllSets=[(each) for each in cmds.ls(typ="objectSet")]
            collectBlendSets=[]
            for each in getAllSets:
                try:
                    keepEach=[(connectedObj) for connectedObj in cmds.listConnections(each, s=1) for eachMember in memberSets if cmds.nodeType(connectedObj) ==eachMember]
                    if keepEach:
                        collectBlendSets.append(each)
                except:
                    pass            
            cmds.optionMenu(self.setNames, e=1)
            for each in getAllSets:
                cmds.menuItem( label=each)    def _add_to_set(self, querySet):
        '''--------------------------------------------------------------------------------------------------------------------------------------
        This adds the current selection to the current set membership in the drop down menu
        --------------------------------------------------------------------------------------------------------------------------------------'''
        setMembers=["Deformer sets", "Set memberships"]
        getSetType=cmds.optionMenu(self.getSetTyp, q=1, v=1)  
        getSel=self.selection_grab()
        if getSetType=="Dynamic sets":
            if querySet !=None and getSel:
                for each in getSel:
                    cmds.select(querySet, add=1)
                    maya.mel.eval( 'dynamicConstraintMembership "add";' )
        else:
            if querySet !=None and getSel:
                for each in getSel:
                    cmds.sets(each, add=querySet)

    def _remove_from_set(self, querySet):
        '''--------------------------------------------------------------------------------------------------------------------------------------
        This removes the current selection from the current set membership in the drop down menu
        --------------------------------------------------------------------------------------------------------------------------------------'''
        setMembers=["Deformer sets", "Set memberships"]
        getSetType=cmds.optionMenu(self.getSetTyp, q=1, v=1)  
        getSel=self.selection_grab()
        if getSetType=="Dynamic sets":
            if querySet !=None and getSel:
                for each in getSel:
                    cmds.select(querySet, add=1)
                    maya.mel.eval( 'dynamicConstraintMembership "remove";' )    

        else:
            if querySet !=None and getSel:
                for each in getSel:
                    cmds.sets(each, rm=querySet)


    def selection_grab(self):
        '''--------------------------------------------------------------------------------------------------------------------------------------
        Common selection query
        --------------------------------------------------------------------------------------------------------------------------------------'''        
        getSel=cmds.ls(sl=1, fl=1)
        if getSel:
            pass
        else:
            print ("You need to make a selection for this tool to operate on.")
            return
        return getSel


    def default_error(self):
        '''--------------------------------------------------------------------------------------------------------------------------------------
        Common default error prompting user to check script editor for details
        --------------------------------------------------------------------------------------------------------------------------------------'''        
        my_message="Something went wrong. See script editor for error messages"
        return my_message


    def helpWin(self, stringField):
        '''--------------------------------------------------------------------------------------------------------------------------------------
        Interface Layout
        --------------------------------------------------------------------------------------------------------------------------------------'''
        # def helpPage(self, arg=None):
        winName = "Description"
        winTitle = winName
        if cmds.window(winName, exists=True):
                cmds.deleteUI(winName)
        window = cmds.window(winName, title=winTitle, tbm=1, w=700, h=400 )
        cmds.menuBarLayout(h=30)
        cmds.rowColumnLayout  (' selectArrayRow ', nr=1, w=700)
        cmds.frameLayout('LrRow', label='', lv=0, nch=1, borderStyle='out', bv=1, p='selectArrayRow')
        cmds.rowLayout  (' rMainRow ', w=700, numberOfColumns=6, p='selectArrayRow')
        cmds.columnLayout ('selectArrayColumn', parent = 'rMainRow')
        cmds.setParent ('selectArrayColumn')
        cmds.gridLayout('txvaluemeter', p='selectArrayColumn', numberOfColumns=2, cellWidthHeight=(700, 400))
        self.list=cmds.scrollField( editable=False, wordWrap=True, ebg=1,bgc=[0.11, 0.15, 0.15], w=700, text=str(stringField))
        cmds.showWindow(window)

inst=setMemUI()
