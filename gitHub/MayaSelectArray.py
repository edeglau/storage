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

    def create_select_array_window(self):
        
        if cmds.window(self.winName, exists=True):
                cmds.deleteUI(self.winName)

        self.window = cmds.window(self.winName, title=self.winTitle, tbm=1, w=270, h=550 )

        cmds.menuBarLayout(h=30)
        self.fileMenu = cmds.menu( label='Clean Interface', pmc=self.clear_superflous_windows)
        cmds.rowColumnLayout  (' selectArrayRow ', nr=1, w=200)

        cmds.frameLayout('LrRow', label='', lv=0, nch=1, borderStyle='out', bv=1, p='selectArrayRow')

        cmds.rowLayout  (' rMainRow ', w=350, numberOfColumns=6, p='selectArrayRow')
        cmds.columnLayout ('selectArrayColumn', parent = 'rMainRow')
        cmds.setParent ('selectArrayColumn')
        cmds.separator(h=10, p='selectArrayColumn')
        cmds.gridLayout('listBuildButtonLayout', p='selectArrayColumn', numberOfColumns=2, cellWidthHeight=(80, 20))
        cmds.button (label='Grab Node', p='listBuildButtonLayout', command = self._get_node_property)
        cmds.button (label='Grab Name', p='listBuildButtonLayout', command = self._get_name_property)
        cmds.button (label='Filter Node', p='listBuildButtonLayout', command = self._create_list_by_node_filter)
        cmds.popupMenu(button=1)
        cmds.menuItem  (label='filter selected by type and make list', command = self._create_list_by_node_filter)
        cmds.menuItem  (label='filter selected by type and add to list', command = self._add_list_by_node_filter)
        cmds.button (label='Filter Name', p='listBuildButtonLayout', command = self._create_list_by_name_filter)
        cmds.popupMenu(button=1)
        cmds.menuItem  (label='filter selected by name and make list', command = self._create_list_by_name_filter)
        cmds.menuItem  (label='filter selected by name and add to list', command = self._add_list_by_name_filter)
        cmds.button (label='All Node', p='listBuildButtonLayout', command = self._create_list_by_all_node)
        cmds.popupMenu(button=1)
        cmds.menuItem  (label='select all scene by type and make list', command = self._create_list_by_all_node)
        cmds.menuItem  (label='select all scene by type and add to list', command = self._add_list_by_all_node)
        cmds.button (label='All Name', p='listBuildButtonLayout', command = self._create_list_by_all_name)
        cmds.popupMenu(button=1)
        cmds.menuItem  (label='select all scene by name and make list', command = self._create_list_by_all_name)
        cmds.menuItem  (label='select all scene by name and add to list', command = self._add_list_by_all_name)
        cmds.text (label='Name or node type field',  p='selectArrayColumn')
        cmds.gridLayout('searchLayout', p='selectArrayColumn', numberOfColumns=2, cellWidthHeight=(80, 25))
        self.nodeName=cmds.textField(w=120, h=25, p='searchLayout')
        cmds.button (label='Find', command = self._find_in_list, p='searchLayout', w=20, ann='find this name in list below')
        cmds.popupMenu(button=1)
        cmds.menuItem  (label='Select in list only', command = self._find_in_list)
        cmds.menuItem  (label='Select in list and scene', command = self._find_in_listAndSelect)
        self.listCountLabel=cmds.text (label='Selection list', p='selectArrayColumn')
        self.nodeList=cmds.textScrollList( numberOfRows=8, ra=1, allowMultiSelection=True, sc=self.list_item_selectability, io=True, w=220, h=300, p='selectArrayColumn')
        cmds.gridLayout('listArrangmentButtonLayout', p='selectArrayColumn', numberOfColumns=4, cellWidthHeight=(40, 20))
        cmds.button (label='clr', command = self._clear_list, p='listArrangmentButtonLayout')
        cmds.button (label='+', command = self._add_selected_to_list, p='listArrangmentButtonLayout')
        cmds.button (label='-', command = self._remove_from_list, p='listArrangmentButtonLayout')
        cmds.button (label='><', command = self._swap_with_selected, p='listArrangmentButtonLayout', ann='swap out selected in list with selected in scene')
        cmds.button (label='sel all', command = self._select_all_in_list, p='listArrangmentButtonLayout', w=50, ann='select all')
        cmds.button (label='sel- ', command = self._clear_selection, p='listArrangmentButtonLayout', w=40, ann='select none')
        cmds.button (label='sort', command = self._sort_list, p='listArrangmentButtonLayout', w=40, ann='sort alphabetically-numerally')
        cmds.button (label='set', command = self._make_set_from_selection_list, p='listArrangmentButtonLayout', w=40, ann='create set from selected in list')
        cmds.text (label='Author: Elise Deglau',w=120, al='left', p='selectArrayColumn')
        cmds.text (label="elisedeglau.wordpress.com/2014/03/25/select-palette/", hl=1, w=300, al='left', p='selectArrayColumn')
        cmds.text (label='This work is licensed under a Creative Commons License', hl=1, w=300, al='left', p='selectArrayColumn')
        cmds.text (label='http://creativecommons.org/licenses/by/4.0/', hl=1, w=350, al='left', p='selectArrayColumn')        
        cmds.showWindow(self.window)

    '''==========================================================================================================================================
    COMMON ERRORS
    =========================================================================================================================================='''          
     

    def already_in_list_error(self, eachSortedObject):
        print '%s'%eachSortedObject+' already in list' 
    
    def selection_field_error(self):
        print "Check that there is a name in the field, spelling and/or if the list has anything in it"
    
    def nothing_selected_error(self):
        print "Nothing Selected"    
        
    '''==========================================================================================================================================
    COMMON LIST FUNCTIONS
    =========================================================================================================================================='''          
     
    def count_objects_in_list(self, arg=None):
        '''----------------------------------------------------------------------------------
        Gets the length of list items and any selected items function
        ----------------------------------------------------------------------------------'''          
        countObj=cmds.textScrollList(self.nodeList, q=1, ni=1)
        countSelObj=cmds.textScrollList(self.nodeList, q=1, nsi=1)
        cmds.text (self.listCountLabel, e=1, label='Selection list    '+ str(countObj)+' Items    '+str(countSelObj)+' Selected list items' )                               
    
    def add_to_list_function(self, eachSortedObj):
        '''----------------------------------------------------------------------------------
        Common add to list function
        ----------------------------------------------------------------------------------'''          
        cmds.textScrollList(self.nodeList, e=1, a=eachSortedObj)
        self.count_objects_in_list()              
    
    def deselect_in_list_function(self, arg=None):
        '''----------------------------------------------------------------------------------
        Common deselect in list function
        ----------------------------------------------------------------------------------'''              
        cmds.textScrollList(self.nodeList, e=1, da=1)
        self.count_objects_in_list()
        
    def select_list_item_function(self, eachSortedObj):
        '''----------------------------------------------------------------------------------
        Common select in list function
        ----------------------------------------------------------------------------------'''          
        cmds.textScrollList(self.nodeList, e=1, si=eachSortedObj) 
        self.count_objects_in_list()
        
    def repopulate_list(self, eachSortedObj):
        '''----------------------------------------------------------------------------------
        Common refill the list function
        ----------------------------------------------------------------------------------'''          
        cmds.textScrollList(self.nodeList, e=1, ra=1)
        cmds.textScrollList(self.nodeList, e=1, append=eachSortedObj[0::1])
        self.count_objects_in_list()     
        
    
    def adding_to_list_function_main(self, selectedObject, foundExistantListObj):
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
                    self.deselect_in_list_function()
                    self.already_in_list_error(eachObject)
                    self.select_list_item_function(eachObject)                                           
                else:
                    self.add_to_list_function(eachObject) 
        else:
            for eachObject in sortObjects:
                self.add_to_list_function(eachObject)
                
    '''======================================================================================================================================
    TOP BUTTON FUNCTIONS
    ======================================================================================================================================'''  
    
    def list_item_selectability(self, arg=None):
        '''----------------------------------------------------------------------------------
        This selects items in scene from list
        ----------------------------------------------------------------------------------'''          
        selectedListItems=cmds.textScrollList(self.nodeList, q=1, selectItem=1)
        cmds.select(selectedListItems, r=1)
        self.count_objects_in_list()
        print selectedListItems
        
        

    def clear_superflous_windows(self, arg=None):
        '''----------------------------------------------------------------------------------
        This clears the interface of window clutter and puts display in wire to lower file load time
        ----------------------------------------------------------------------------------'''          
        windows = cmds.lsUI(wnd=1)
        for eachWindow in closeWindow:
            if eachWindow in windows:
                windows.remove(eachWindow)
        cmds.deleteUI(windows, window=1)
        
    
    def _get_node_property(self, arg=None):
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
            self.nothing_selected_error()
    
    
    def _get_name_property(self, arg=None):
        '''----------------------------------------------------------------------------------
        This grabs the named property of selected object
        ----------------------------------------------------------------------------------'''          
        selectedObject=cmds.ls(sl=1)
        objListLength=len(selectedObject)
        if objListLength:
            if objListLength >= 1:
                cmds.textField(self.nodeName,e=1, text=selectedObject[0])  
        else:
            self.nothing_selected_error()
            
    def _create_list_by_all_node(self, arg=None):
        '''----------------------------------------------------------------------------------
        This selects everything in scene by the matched node type in field and create list
        ----------------------------------------------------------------------------------'''          
        nameFieldText=cmds.textField(self.nodeName,q=True, text=True)
        if nameFieldText: 
            try:
                selectedObject=cmds.ls(type=nameFieldText)
                pass
            except:
                self.selection_field_error()
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
            self._clear_list()
            for each in selectedObject:
                cmds.select(each, r=1)
                self.repopulate_list(selectedObject)                      
        else:
            self.selection_field_error()
            return       
    
    
    def _add_list_by_all_node(self, arg=None):
        '''----------------------------------------------------------------------------------
        This adds all items of the same type
        ----------------------------------------------------------------------------------'''          
        nameFieldText=cmds.textField(self.nodeName,q=True, text=True)
        if nameFieldText:
            try:
                selectedObject=cmds.ls(type=nameFieldText)
                pass
            except:
                self.selection_field_error()    
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
                self.adding_to_list_function_main(selectedObject, foundExistantListObj)                                          
        else:
            self.selection_field_error()                       
    
    def _create_list_by_all_name(self, arg=None):
        '''----------------------------------------------------------------------------------
        This selects everything in scene by the matched name in field
        ----------------------------------------------------------------------------------'''          
        nameFieldText=cmds.textField(self.nodeName,q=True, text=True)
        if nameFieldText:
            allObject=cmds.ls(sn=1)
            selectedObject=[(each)for each in allObject if nameFieldText in each]
            if selectedObject:
                self.repopulate_list(selectedObject)
            else:
                self.selection_field_error()             
        else:
            self.selection_field_error()
            
    
    def _add_list_by_all_name(self, arg=None):
        '''----------------------------------------------------------------------------------
        This adds all items in scene that share the same name shown in field
        ----------------------------------------------------------------------------------'''          
        nameFieldText=cmds.textField(self.nodeName,q=True, text=True)
        listArray=cmds.textScrollList(self.nodeList, q=1, ai=1)
        if nameFieldText:
            allObject=cmds.ls(sn=1)
            selectedObject=[(each)for each in allObject if nameFieldText in each]
            if selectedObject:
                self.adding_to_list_function_main(selectedObject, listArray)
            else:
                self.selection_field_error()                                              
        else:
            self.selection_field_error()
    
    def _create_list_by_node_filter(self, arg=None):
        '''----------------------------------------------------------------------------------
        This filters all selected objects by name in field and create a list from it
        ----------------------------------------------------------------------------------'''
        nameFieldText=cmds.textField(self.nodeName,q=True, text=True)
        selectedObject=cmds.ls(sl=1, fl=1)
        objFiltered=[(eachObj) for eachObj in selectedObject if nameFieldText in cmds.nodeType(eachObj)]
        if nameFieldText and selectedObject and objFiltered:
            self.repopulate_list(objFiltered)
        else:
            self.selection_field_error()
    
    def _add_list_by_node_filter(self, arg=None):
        '''----------------------------------------------------------------------------------
        Adds selected objects with filtered name to the list
        ----------------------------------------------------------------------------------'''          
        nameFieldText=cmds.textField(self.nodeName,q=True, text=True)
        listArray=cmds.textScrollList(self.nodeList, q=1, ai=1)
        selectedObject=cmds.ls(sl=1, fl=1)
        objFiltered=[(eachObj) for eachObj in selectedObject if nameFieldText in cmds.nodeType(eachObj)]
        if nameFieldText and selectedObject and objFiltered:
            self.adding_to_list_function_main(objFiltered, listArray)
        else:
            self.selection_field_error()
    
    
    
    def _create_list_by_name_filter(self, arg=None):
        '''----------------------------------------------------------------------------------
        This filters all selected objects by name in field and create a list from it
        ----------------------------------------------------------------------------------'''
        nameFieldText=cmds.textField(self.nodeName,q=True, text=True)
        selectedObject=cmds.ls(sl=1, fl=1)
        objFiltered=[(eachSelObj)for eachSelObj in selectedObject if nameFieldText in eachSelObj]
        if nameFieldText and selectedObject and objFiltered:
            self.repopulate_list(objFiltered)
        else:
            self.selection_field_error()
            
                 
    def _add_list_by_name_filter(self, arg=None):
        '''----------------------------------------------------------------------------------
        Adds selected objects with filtered name to the list
        ----------------------------------------------------------------------------------'''          
        listArray=cmds.textScrollList(self.nodeList, q=1, ai=1)
        nameFieldText=cmds.textField(self.nodeName,q=True, text=True)
        selectedObject=cmds.ls(sl=1, fl=1)
        objFiltered=[(eachSelObj)for eachSelObj in selectedObject if nameFieldText in eachSelObj]
        if nameFieldText and selectedObject and objFiltered:
            self.adding_to_list_function_main(objFiltered, listArray)
        else:
            self.selection_field_error()
            
    def _find_in_list(self, arg=None):
        '''----------------------------------------------------------------------------------
        This locates the object by name in list
        ----------------------------------------------------------------------------------'''          
        nameFieldText=cmds.textField(self.nodeName,q=True, text=True)
        listArray=cmds.textScrollList(self.nodeList, q=1, ai=1)
        if nameFieldText and listArray:
            foundExistantListObj=[(eachObj) for eachObj in listArray if nameFieldText in str(eachObj)]
            if foundExistantListObj:
                self.deselect_in_list_function()
                print '%s'%foundExistantListObj+' already in list'   
                self.select_list_item_function(foundExistantListObj)                            
                print 'Objects containing "'+nameFieldText+'" found in: '+str(foundExistantListObj)
            else:
                cmds.textScrollList(self.nodeList, e=1, da=1)
                self.count_objects_in_list()                         
                print 'Objects containing "' +nameFieldText+'" not found in this list.'
        else:
            self.selection_field_error()  
    
    def _find_in_listAndSelect(self, arg=None):
        '''----------------------------------------------------------------------------------
        This locates the object by name in list
        ----------------------------------------------------------------------------------'''          
        nameFieldText=cmds.textField(self.nodeName,q=True, text=True)
        listArray=cmds.textScrollList(self.nodeList, q=1, ai=1)
        if nameFieldText and listArray:
            foundExistantListObj=[(eachObj) for eachObj in listArray if nameFieldText in str(eachObj)]
            if foundExistantListObj:
                self.deselect_in_list_function()
                print '%s'%foundExistantListObj+' already in list'   
                self.select_list_item_function(foundExistantListObj)
                cmds.select(foundExistantListObj, r=1)                      
                print 'Objects containing "'+nameFieldText+'" found in: '+str(foundExistantListObj)
            else:
                cmds.textScrollList(self.nodeList, e=1, da=1)
                self.count_objects_in_list()                         
                print 'Objects containing "' +nameFieldText+'" not found in this list.'
        else:
            self.selection_field_error()       
    
    '''==========================================================================================================================================
    BOTTOM BUTTON FUNCTIONS
    =========================================================================================================================================='''          
    
    def _clear_list(self, arg=None):
        '''----------------------------------------------------------------------------------
        this clears the list
        ----------------------------------------------------------------------------------'''          
        cmds.textScrollList(self.nodeList, e=1, ra=1)
        self.count_objects_in_list() 
        
    def _add_selected_to_list(self, arg=None):
        '''----------------------------------------------------------------------------------
        Adds selected objects to the list
        ----------------------------------------------------------------------------------'''          
        listArray=cmds.textScrollList(self.nodeList, q=1, ai=1)
        selectedObject=cmds.ls(sl=1, fl=1)
        if selectedObject:
            self.adding_to_list_function_main(selectedObject, listArray)  
            
    def _remove_from_list(self, arg=None):
        '''----------------------------------------------------------------------------------
        This removes the selected item in the list from the list
        ----------------------------------------------------------------------------------'''          
        selectedListItems=cmds.textScrollList(self.nodeList, q=1, selectItem=1)
        if selectedListItems<1:
            print 'Select item to subtract from list.'
        else:
            cmds.textScrollList(self.nodeList, e=1, ri=selectedListItems)
            self.count_objects_in_list() 
    
    def _swap_with_selected(self, arg=None):
        '''----------------------------------------------------------------------------------
        This swaps the selected list item with the selected object
        ----------------------------------------------------------------------------------'''          
        selectedListItems=cmds.textScrollList(self.nodeList, q=1, selectItem=1)
        listArray=cmds.textScrollList(self.nodeList, q=1, ai=1)
        selectedObject=cmds.ls(sl=1, fl=1)
        if selectedObject:
            if selectedObject[0] in listArray:
                cmds.textScrollList(self.nodeList, e=1, si=selectedObject)
                self.already_in_list_error(selectedObject)
            else:
                cmds.textScrollList(self.nodeList, e=1, ri=selectedListItems)
                cmds.textScrollList(self.nodeList, e=1, a=selectedObject[0::1])
                self.count_objects_in_list()         
        else:
            print 'Select list item first and then object to swap with.'
    
    def _select_all_in_list(self, arg=None):
        '''----------------------------------------------------------------------------------
        This selects all items in list
        ----------------------------------------------------------------------------------'''          
        listArray=cmds.textScrollList(self.nodeList, q=1, ai=1)
        if listArray:
            self.select_list_item_function(listArray)
            cmds.select(listArray)           
        else:
            print "List is empty."
            
    def _clear_selection(self, arg=None):
        '''----------------------------------------------------------------------------------
        This clears the selection of the items in the list
        ----------------------------------------------------------------------------------'''          
        self.deselect_in_list_function()
    
    def _sort_list(self, arg=None):
        '''----------------------------------------------------------------------------------
        This sorts the list by alphabetical and numerical
        ----------------------------------------------------------------------------------'''          
        listArray=cmds.textScrollList(self.nodeList, q=1, ai=1)
        if listArray:
            sortedObjList=sorted(listArray, key=lower)
            self.repopulate_list(sortedObjList)                              
        else:
            print "Check that list is present."
            
    def _make_set_from_selection_list(self, arg=None):
        '''----------------------------------------------------------------------------------
        This create a set from selected items in list
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
                print "create set cancelled"
                return
        else:
            print "Select something from selection list."

inst = SelectionPalettUI()
inst.create_select_array_window()
      
