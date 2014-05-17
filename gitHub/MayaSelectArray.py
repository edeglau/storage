'''----------------------------------------------------------
Selection Palette offers a work area where the artist
can create a temporary selection group from commonly selected
objects in scene.
-----------------------------------------------------------'''         


import maya.cmds as cmds
from functools import partial
from string import *
import re
import maya.mel
__author__ = "Elise Deglau"
__version__ = 1.00



'''====================================================================================================================================
The following lists are set to polygons and rigging needs but 
can be modified to add object components and node types:
====================================================================================================================================''' 
         

objectCommonalityWarning=[
                          'transform',
                          'mesh',
                          'joint',
                          'shape',
                          'nurbsCurve'
                          ]

closeWindow=[
            'CommandWindow', 
            'MayaWindow', 
            'scriptEditorPanel1Window', 
            'selectArrayWindow', 
            'shelfEditorWin', 
            'ColorEditor' ]


class SelectionPalettUI(object):
    '''--------------------------------------------------------------------------------------------------------------------------------------
    Interface Layout
    --------------------------------------------------------------------------------------------------------------------------------------'''          
    def __init__(self, winName="selectArrayWindow"):
        self.winTitle = "Selection Palette"
        self.winName = winName

    def create(self):
        
        if cmds.window(self.winName, exists=True):
                cmds.deleteUI(self.winName)

        self.window = cmds.window(self.winName, title=self.winTitle, tbm=1, w=270, h=550 )

        cmds.menuBarLayout(h=30)
        self.fileMenu = cmds.menu( label='Clean Interface', pmc=self.clearSuperflousWindows)
        cmds.rowColumnLayout  (' selectArrayRow ', nr=1, w=200)

        cmds.frameLayout('LrRow', label='', lv=0, nch=1, borderStyle='out', bv=1, p='selectArrayRow')

        cmds.rowLayout  (' rMainRow ', w=350, numberOfColumns=6, p='selectArrayRow')
        cmds.columnLayout ('selectArrayColumn', parent = 'rMainRow')
        cmds.setParent ('selectArrayColumn')
        cmds.separator(h=10, p='selectArrayColumn')
        cmds.gridLayout('listBuildButtonLayout', p='selectArrayColumn', numberOfColumns=2, cellWidthHeight=(80, 20))
        cmds.button (label='Grab Node', p='listBuildButtonLayout', command = self.getNodeProperty)
        cmds.button (label='Grab Name', p='listBuildButtonLayout', command = self.getNameProperty)
        cmds.button (label='Filter Node', p='listBuildButtonLayout', command = self.createListByNodeFilter)
        cmds.popupMenu(button=1)
        cmds.menuItem  (label='filter selected by type and make list', command = self.createListByNodeFilter)
        cmds.menuItem  (label='filter selected by type and add to list', command = self.addListByNodeFilter)
        cmds.button (label='Filter Name', p='listBuildButtonLayout', command = self.createListByNameFilter)
        cmds.popupMenu(button=1)
        cmds.menuItem  (label='filter selected by name and make list', command = self.createListByNameFilter)
        cmds.menuItem  (label='filter selected by name and add to list', command = self.addListByNameFilter)
        cmds.button (label='All Node', p='listBuildButtonLayout', command = self.createListByAllNode)
        cmds.popupMenu(button=1)
        cmds.menuItem  (label='select all scene by type and make list', command = self.createListByAllNode)
        cmds.menuItem  (label='select all scene by type and add to list', command = self.addListByAllNode)
        cmds.button (label='All Name', p='listBuildButtonLayout', command = self.createListByAllName)
        cmds.popupMenu(button=1)
        cmds.menuItem  (label='select all scene by name and make list', command = self.createListByAllName)
        cmds.menuItem  (label='select all scene by name and add to list', command = self.addListByAllName)
        cmds.text (label='Name or node type field',  p='selectArrayColumn')
        cmds.gridLayout('searchLayout', p='selectArrayColumn', numberOfColumns=2, cellWidthHeight=(80, 25))
        self.nodeName=cmds.textField(w=120, h=25, p='searchLayout')
        cmds.button (label='Find', command = self.findInList, p='searchLayout', w=20, ann='find this name in list below')
        cmds.popupMenu(button=1)
        cmds.menuItem  (label='Select in list only', command = self.findInList)
        cmds.menuItem  (label='Select in list and scene', command = self.findInListAndSelect)
        self.listCountLabel=cmds.text (label='Selection list', p='selectArrayColumn')
        self.nodeList=cmds.textScrollList( numberOfRows=8, ra=1, allowMultiSelection=True, sc=self.listItemSelectability, io=True, w=220, h=300, p='selectArrayColumn')
        cmds.gridLayout('listArrangmentButtonLayout', p='selectArrayColumn', numberOfColumns=4, cellWidthHeight=(40, 20))
        cmds.button (label='clr', command = self.clearList, p='listArrangmentButtonLayout')
        cmds.button (label='+', command = self.addSelectedToList, p='listArrangmentButtonLayout')
        cmds.button (label='-', command = self.removeFromList, p='listArrangmentButtonLayout')
        cmds.button (label='><', command = self.swapWithSelected, p='listArrangmentButtonLayout', ann='swap out selected in list with selected in scene')
        cmds.button (label='sel all', command = self.selectAllInList, p='listArrangmentButtonLayout', w=50, ann='select all')
        cmds.button (label='sel- ', command = self.clearSelection, p='listArrangmentButtonLayout', w=40, ann='select none')
        cmds.button (label='sort', command = self.sortList, p='listArrangmentButtonLayout', w=40, ann='sort alphabetically-numerally')
        cmds.button (label='set', command = self.makeSetFromSelectionList, p='listArrangmentButtonLayout', w=40, ann='create set from selected in list')
        cmds.text (label='Author: Elise Deglau',w=120, al='left', p='selectArrayColumn')
        cmds.text (label="elisedeglau.wordpress.com/2014/03/25/select-palette/", hl=1, w=300, al='left', p='selectArrayColumn')
        cmds.text (label='This work is licensed under a Creative Commons License', hl=1, w=300, al='left', p='selectArrayColumn')
        cmds.text (label='http://creativecommons.org/licenses/by/4.0/', hl=1, w=350, al='left', p='selectArrayColumn')        
        cmds.showWindow(self.window)

    '''==========================================================================================================================================
    COMMON ERRORS
    =========================================================================================================================================='''          
     

    def alreadyInListError(self, eachSortedObject):
        print '%s'%eachSortedObject+' already in list' 
    
    def selectionFieldError(self):
        print "Check that there is a name in the field, spelling and/or if the list has anything in it"
    
    def nothingSelectedError(self):
        print "Nothing Selected"    
        
    '''==========================================================================================================================================
    COMMON LIST FUNCTIONS
    =========================================================================================================================================='''          
     
    def countObjectsInList(self, arg=None):
        '''----------------------------------------------------------------------------------
        Gets the length of list items and any selected items function
        ----------------------------------------------------------------------------------'''          
        countObj=cmds.textScrollList(self.nodeList, q=1, ni=1)
        countSelObj=cmds.textScrollList(self.nodeList, q=1, nsi=1)
        cmds.text (self.listCountLabel, e=1, label='Selection list    '+ str(countObj)+' Items    '+str(countSelObj)+' Selected list items' )                               
    
    def addToListFunction(self, eachSortedObj):
        '''----------------------------------------------------------------------------------
        Common add to list function
        ----------------------------------------------------------------------------------'''          
        cmds.textScrollList(self.nodeList, e=1, a=eachSortedObj)
        self.countObjectsInList()              
    
    def deselectInListFunction(self, arg=None):
        '''----------------------------------------------------------------------------------
        Common deselect in list function
        ----------------------------------------------------------------------------------'''              
        cmds.textScrollList(self.nodeList, e=1, da=1)
        self.countObjectsInList()
        
    def selectListItemFunction(self, eachSortedObj):
        '''----------------------------------------------------------------------------------
        Common select in list function
        ----------------------------------------------------------------------------------'''          
        cmds.textScrollList(self.nodeList, e=1, si=eachSortedObj) 
        self.countObjectsInList()
        
    def repopulateList(self, eachSortedObj):
        '''----------------------------------------------------------------------------------
        Common refill the list function
        ----------------------------------------------------------------------------------'''          
        cmds.textScrollList(self.nodeList, e=1, ra=1)
        cmds.textScrollList(self.nodeList, e=1, append=eachSortedObj[0::1])
        self.countObjectsInList()     
        
    
    def addingTolistFunctionMAIN(self, selectedObject, foundExistantListObj):
        '''----------------------------------------------------------------------------------
        Main populate list function
        ----------------------------------------------------------------------------------'''              
        if selectedObject>1:
            sortObjects=sorted(selectedObject, key=lower)
        if len(selectedObject)==1:
            sortObjects=selectedObject                                       
        if foundExistantListObj:
            for eachObject in sortObjects:
                if eachObject in foundExistantListObj:
                    self.deselectInListFunction()
                    self.alreadyInListError(eachObject)
                    self.selectListItemFunction(eachObject)                                           
                else:
                    self.addToListFunction(eachObject) 
        else:
            for eachObject in sortObjects:
                self.addToListFunction(eachObject)
                
    '''======================================================================================================================================
    TOP BUTTON FUNCTIONS
    ======================================================================================================================================'''  
    
    def listItemSelectability(self, arg=None):
        '''----------------------------------------------------------------------------------
        This selects items in scene from list
        ----------------------------------------------------------------------------------'''          
        selectedListItems=cmds.textScrollList(self.nodeList, q=1, selectItem=1)
        cmds.select(selectedListItems, r=1)
        self.countObjectsInList()
        print selectedListItems
        
        

    def clearSuperflousWindows(self, arg=None):
        '''----------------------------------------------------------------------------------
        This clears the interface of window clutter and puts display in wire to lower file load time
        ----------------------------------------------------------------------------------'''          
        windows = cmds.lsUI(wnd=1)
        for eachWindow in closeWindow:
            if eachWindow in windows:
                windows.remove(eachWindow)
        cmds.deleteUI(windows, window=1)
        
    
    def getNodeProperty(self, arg=None):
        '''----------------------------------------------------------------------------------
        This grabs the node property of selected object
        ----------------------------------------------------------------------------------'''          
        selectedObject=cmds.ls(sl=1)
        objListLength=len(selectedObject)
        if objListLength:
            if objListLength > 1:
                filternode= cmds.nodeType(selectedObject[0])
                cmds.textField(self.nodeName,e=1, text=filternode)
            if objListLength == 1:
                filternode= cmds.nodeType(selectedObject)
                cmds.textField(self.nodeName,e=1, text=filternode)        
        else:
            self.nothingSelectedError()
    
    
    def getNameProperty(self, arg=None):
        '''----------------------------------------------------------------------------------
        This grabs the named property of selected object
        ----------------------------------------------------------------------------------'''          
        selectedObject=cmds.ls(sl=1)
        objListLength=len(selectedObject)
        if objListLength:
            if objListLength >= 1:
                cmds.textField(self.nodeName,e=1, text=selectedObject[0])  
        else:
            self.nothingSelectedError()
            
    def createListByAllNode(self, arg=None):
        '''----------------------------------------------------------------------------------
        This selects everything in scene by the matched node type in field and creates list
        ----------------------------------------------------------------------------------'''          
        nameFieldText=cmds.textField(self.nodeName,q=True, text=True)
        if nameFieldText: 
            try:
                selectedObject=cmds.ls(type=nameFieldText)
                pass
            except:
                self.selectionFieldError()
                return  
            selfObjList=[(eachtype) for eachtype in selectedObject for item in objectCommonalityWarning if item in str(cmds.objectType(eachtype))]
            if selfObjList:
                result = cmds.confirmDialog( 
                            title='Confirm', 
                            message='Caution! This node type is very common and could potentially lock up your scene.', 
                            button=['Continue','Cancel'],
                            defaultButton='Continue', 
                            cancelButton='Cancel', 
                            dismissString='Cancel' )
                if result == 'Continue':
                    pass
                else:
                    return
            self.clearList()
            for each in selectedObject:
                cmds.select(each, r=1)
                self.repopulateList(selectedObject)                      
        else:
            self.selectionFieldError()
            return       
    
    
    def addListByAllNode(self, arg=None):
        '''----------------------------------------------------------------------------------
        This adds all items of the same type
        ----------------------------------------------------------------------------------'''          
        nameFieldText=cmds.textField(self.nodeName,q=True, text=True)
        if nameFieldText:
            try:
                selectedObject=cmds.ls(type=nameFieldText)
                pass
            except:
                self.selectionFieldError()    
            selfObjList=[(eachtype) for eachtype in selectedObject for item in objectCommonalityWarning if item in str(cmds.objectType(eachtype))]
            if selfObjList:
                result = cmds.confirmDialog( 
                            title='Confirm', 
                            message='Caution! This node type is very common and could potentially lock up your scene.', 
                            button=['Continue','Cancel'],
                            defaultButton='Continue', 
                            cancelButton='Cancel', 
                            dismissString='Cancel' )
                if result == 'Continue':
                    pass
                else:
                    return                
            foundExistantListObj=cmds.textScrollList(self.nodeList, q=1, ai=1)
            if selectedObject:
                self.addingTolistFunctionMAIN(selectedObject, foundExistantListObj)                                          
        else:
            self.selectionFieldError()                       
    
    def createListByAllName(self, arg=None):
        '''----------------------------------------------------------------------------------
        This selects everything in scene by the matched name in field
        ----------------------------------------------------------------------------------'''          
        nameFieldText=cmds.textField(self.nodeName,q=True, text=True)
        if nameFieldText:
            allObject=cmds.ls(sn=1)
            selectedObject=[(each)for each in allObject if nameFieldText in each]
            if selectedObject:
                self.repopulateList(selectedObject)
            else:
                self.selectionFieldError()             
        else:
            self.selectionFieldError()
            
    
    def addListByAllName(self, arg=None):
        '''----------------------------------------------------------------------------------
        This adds all items in scene that share the same name shown in field
        ----------------------------------------------------------------------------------'''          
        nameFieldText=cmds.textField(self.nodeName,q=True, text=True)
        listArray=cmds.textScrollList(self.nodeList, q=1, ai=1)
        if nameFieldText:
            allObject=cmds.ls(sn=1)
            selectedObject=[(each)for each in allObject if nameFieldText in each]
            if selectedObject:
                self.addingTolistFunctionMAIN(selectedObject, listArray)
            else:
                self.selectionFieldError()                                              
        else:
            self.selectionFieldError()
    
    def createListByNodeFilter(self, arg=None):
        '''----------------------------------------------------------------------------------
        This filters all selected objects by name in field and creates a list from it
        ----------------------------------------------------------------------------------'''
        nameFieldText=cmds.textField(self.nodeName,q=True, text=True)
        selectedObject=cmds.ls(sl=1, fl=1)
        objFiltered=[(eachObj) for eachObj in selectedObject if nameFieldText in cmds.nodeType(eachObj)]
        if nameFieldText and selectedObject and objFiltered:
            self.repopulateList(objFiltered)
        else:
            self.selectionFieldError()
    
    def addListByNodeFilter(self, arg=None):
        '''----------------------------------------------------------------------------------
        Adds selected objects with filtered name to the list
        ----------------------------------------------------------------------------------'''          
        nameFieldText=cmds.textField(self.nodeName,q=True, text=True)
        listArray=cmds.textScrollList(self.nodeList, q=1, ai=1)
        selectedObject=cmds.ls(sl=1, fl=1)
        objFiltered=[(eachObj) for eachObj in selectedObject if nameFieldText in cmds.nodeType(eachObj)]
        if nameFieldText and selectedObject and objFiltered:
            self.addingTolistFunctionMAIN(objFiltered, listArray)
        else:
            self.selectionFieldError()
    
    
    
    def createListByNameFilter(self, arg=None):
        '''----------------------------------------------------------------------------------
        This filters all selected objects by name in field and creates a list from it
        ----------------------------------------------------------------------------------'''
        nameFieldText=cmds.textField(self.nodeName,q=True, text=True)
        selectedObject=cmds.ls(sl=1, fl=1)
        objFiltered=[(eachSelObj)for eachSelObj in selectedObject if nameFieldText in eachSelObj]
        if nameFieldText and selectedObject and objFiltered:
            self.repopulateList(objFiltered)
        else:
            self.selectionFieldError()
            
                 
    def addListByNameFilter(self, arg=None):
        '''----------------------------------------------------------------------------------
        Adds selected objects with filtered name to the list
        ----------------------------------------------------------------------------------'''          
        listArray=cmds.textScrollList(self.nodeList, q=1, ai=1)
        nameFieldText=cmds.textField(self.nodeName,q=True, text=True)
        selectedObject=cmds.ls(sl=1, fl=1)
        objFiltered=[(eachSelObj)for eachSelObj in selectedObject if nameFieldText in eachSelObj]
        if nameFieldText and selectedObject and objFiltered:
            self.addingTolistFunctionMAIN(objFiltered, listArray)
        else:
            self.selectionFieldError()
            
    def findInList(self, arg=None):
        '''----------------------------------------------------------------------------------
        This locates the object by name in list
        ----------------------------------------------------------------------------------'''          
        nameFieldText=cmds.textField(self.nodeName,q=True, text=True)
        listArray=cmds.textScrollList(self.nodeList, q=1, ai=1)
        if nameFieldText and listArray:
            foundExistantListObj=[(eachObj) for eachObj in listArray if nameFieldText in str(eachObj)]
            if foundExistantListObj:
                self.deselectInListFunction()
                print '%s'%foundExistantListObj+' already in list'   
                self.selectListItemFunction(foundExistantListObj)                            
                print 'Objects containing "'+nameFieldText+'" found in: '+str(foundExistantListObj)
            else:
                cmds.textScrollList(self.nodeList, e=1, da=1)
                self.countObjectsInList()                         
                print 'Objects containing "' +nameFieldText+'" not found in this list.'
        else:
            self.selectionFieldError()  
    
    def findInListAndSelect(self, arg=None):
        '''----------------------------------------------------------------------------------
        This locates the object by name in list
        ----------------------------------------------------------------------------------'''          
        nameFieldText=cmds.textField(self.nodeName,q=True, text=True)
        listArray=cmds.textScrollList(self.nodeList, q=1, ai=1)
        if nameFieldText and listArray:
            foundExistantListObj=[(eachObj) for eachObj in listArray if nameFieldText in str(eachObj)]
            if foundExistantListObj:
                self.deselectInListFunction()
                print '%s'%foundExistantListObj+' already in list'   
                self.selectListItemFunction(foundExistantListObj)
                cmds.select(foundExistantListObj, r=1)                      
                print 'Objects containing "'+nameFieldText+'" found in: '+str(foundExistantListObj)
            else:
                cmds.textScrollList(self.nodeList, e=1, da=1)
                self.countObjectsInList()                         
                print 'Objects containing "' +nameFieldText+'" not found in this list.'
        else:
            self.selectionFieldError()       
    
    '''==========================================================================================================================================
    BOTTOM BUTTON FUNCTIONS
    =========================================================================================================================================='''          
    
    def clearList(self, arg=None):
        '''----------------------------------------------------------------------------------
        this clears the list
        ----------------------------------------------------------------------------------'''          
        cmds.textScrollList(self.nodeList, e=1, ra=1)
        self.countObjectsInList() 
        
    def addSelectedToList(self, arg=None):
        '''----------------------------------------------------------------------------------
        Adds selected objects to the list
        ----------------------------------------------------------------------------------'''          
        listArray=cmds.textScrollList(self.nodeList, q=1, ai=1)
        selectedObject=cmds.ls(sl=1, fl=1)
        if selectedObject:
            self.addingTolistFunctionMAIN(selectedObject, listArray)  
            
    def removeFromList(self, arg=None):
        '''----------------------------------------------------------------------------------
        This removes the selected item in the list from the list
        ----------------------------------------------------------------------------------'''          
        selectedListItems=cmds.textScrollList(self.nodeList, q=1, selectItem=1)
        if selectedListItems<1:
            print 'Select item to subtract from list.'
        else:
            cmds.textScrollList(self.nodeList, e=1, ri=selectedListItems)
            self.countObjectsInList() 
    
    def swapWithSelected(self, arg=None):
        '''----------------------------------------------------------------------------------
        This swaps the selected list item with the selected object
        ----------------------------------------------------------------------------------'''          
        selectedListItems=cmds.textScrollList(self.nodeList, q=1, selectItem=1)
        listArray=cmds.textScrollList(self.nodeList, q=1, ai=1)
        selectedObject=cmds.ls(sl=1, fl=1)
        if selectedObject:
            if selectedObject[0] in listArray:
                cmds.textScrollList(self.nodeList, e=1, si=selectedObject)
                self.alreadyInListError(selectedObject)
            else:
                cmds.textScrollList(self.nodeList, e=1, ri=selectedListItems)
                cmds.textScrollList(self.nodeList, e=1, a=selectedObject[0::1])
                self.countObjectsInList()         
        else:
            print 'Select list item first and then object to swap with.'
    
    def selectAllInList(self, arg=None):
        '''----------------------------------------------------------------------------------
        This selects all items in list
        ----------------------------------------------------------------------------------'''          
        listArray=cmds.textScrollList(self.nodeList, q=1, ai=1)
        if listArray:
            self.selectListItemFunction(listArray)
            cmds.select(listArray)           
        else:
            print "List is empty."
            
    def clearSelection(self, arg=None):
        '''----------------------------------------------------------------------------------
        This clears the selection of the items in the list
        ----------------------------------------------------------------------------------'''          
        self.deselectInListFunction()
    
    def sortList(self, arg=None):
        '''----------------------------------------------------------------------------------
        This sorts the list by alphabetical and numerical
        ----------------------------------------------------------------------------------'''          
        listArray=cmds.textScrollList(self.nodeList, q=1, ai=1)
        if listArray:
            sortedObjList=sorted(listArray, key=lower)
            self.repopulateList(sortedObjList)                              
        else:
            print "Check that list is present."
            
    def makeSetFromSelectionList(self, arg=None):
        '''----------------------------------------------------------------------------------
        This creates a set from selected items in list
        ----------------------------------------------------------------------------------'''          
        selectedListItems=cmds.textScrollList(self.nodeList, q=1, selectItem=1)
        if selectedListItems:
            result = cmds.promptDialog( 
                title='Confirm', 
                message='Name of set:', 
                button=['Continue','Cancel'],
                defaultButton='Continue', 
                cancelButton='Cancel', 
                dismissString='Cancel' )
            if result == 'Continue':
                text = cmds.promptDialog(query=True, text=True)
                cmds.sets(n=text)
            else:
                print "Create set cancelled"
                return
        else:
            print "Select something from selection list."

inst = SelectionPalettUI()
inst.create()
      
