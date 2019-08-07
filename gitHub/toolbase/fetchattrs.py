

#from pymel.core import *
import pymel.core as pm
import maya.mel
from string import *
from functools import partial
import os, subprocess, sys, platform, re
import maya.cmds as cmds

OSplatform=platform.platform()

# import tools
# toolClass=tools.ToolFunctions()

class fetchAttrs(object):
    
    def _findAttr_window(self, arg=None):
        winName = "Fetch Attributes"
        winTitle = winName
        if cmds.window(winName, exists=True):
                deleteUI(winName)
        try:
            getSel=pm.ls(sl=1, fl=1)      
            getFirst=getSel[0]
            getFirstAttr=pm.listAttr (getFirst, w=1, a=1, s=1, u=1)      
            getFirstAttr=sorted(getFirstAttr)               
        except:
            getFirst=[""]  
            getSel= [""]          
            getFirstAttr= [""]
            # return            
#        global attributeFirstSel
#        global makeAttr   
        window = cmds.window(winName, title=winTitle, tbm=1, w=550, h=600)
        cmds.menuBarLayout(h=30)
        stringField='''"Fetch Attribute" (launches window)an interface to query items attributes that
    you can hunt by name portion or values. You can also change attribute value through this
    window if number values apply. Can also query scene for all objects with a particular attribute
    or value.

        Query object for attributes:

        * Step 1: select object
        * Step 2: launch window
        * Step 3: enter a partial name in the "search" window beside the
            "Fetch Attribute Name" button
        * Step 3(alternative: enter a value in the "search" window beside the
            "Fetch Attribute Value" button            
        * Step 4: pressing the button beside either feild will repopulate the
            drop down menu with the attributes that have these names or values
        * Step 5(optional): fill in the "Change Value" field with a new value
        * Step 6: press the "Apply Value" button to change the attribute that
            is currently visible in the drop down menu
        * Step 7(optional): select a new object or keep current object selected
        * Step 8: press "Refresh Selection" will repopulate the drop down menu
            with current selection's full attributes

        Query scene for objects with attributes:

        * Step 1: launch window
        * Step 2: enter a partial name in the "search" window beside the
            "Fetch Attribute Name" button
        * Step 4(alternative: enter a value in the "search" window beside the
            "Fetch Attribute Value" button            
        * Step 5: pressing the button beside either feild will repopulate the
            drop down menu with the attributes that have these names or values
        * Step 6(optional): fill in the "Change Value" field with a new value
        * Step 7: press the "Apply Value" button to change the attribute that
            is currently visible in the drop down menu
        * Step 8(optional): press "Apply All" will change all attributes in
            dropdown to new value(EG: resetting all wind attributes to 0.0
            to reset wind in scene to none)

        "REFRESH SELECTION" - button
            Repopulates the drop down menu with attributes from new/current
                selection
        "APPLY VALUE" - button
            Will change the value on the attribute that is currently
                visible in the drop down menu
        "FETCH ATTRIBUTE NAME" - button
            Repopulates the drop down menu with all attributes on selected
                object that matches this name
        "FETCH ATTRIBUTE VALUE" - button
            Repopulates the drop down menu with all attributes on selected
                object that matches this value'''
        self.fileMenu = cmds.menu( label='Help', hm=1, pmc=lambda *args:self.helpWin(stringField))         
        cmds.rowColumnLayout  (' selectArrayRow ', nr=1, w=550)
        cmds.frameLayout('LrRow', label='', lv=0, nch=1, borderStyle='out', bv=1, p='selectArrayRow')
        cmds.rowLayout  (' rMainRow ', w=550, numberOfColumns=6, p='selectArrayRow')
        cmds.columnLayout ('selectArrayColumn', parent = 'rMainRow')
        cmds.setParent ('selectArrayColumn')
        cmds.separator(h=10, p='selectArrayColumn')
        cmds.frameLayout('title1', bgc=[0.15, 0.15, 0.15], cll=1, label='Find Attributes on Object', lv=1, nch=1, borderStyle='out', bv=1, w=550, fn="tinyBoldLabelFont", p='selectArrayColumn')
        cmds.gridLayout('valuebuttonlayout', p='title1', numberOfColumns=5, cellWidthHeight=(98, 20))
        cmds.text(label="Att Value:", p='valuebuttonlayout', align="left", w=50)
        self.attrVal=cmds.text(label="Select from drop down", p='valuebuttonlayout', w=100)
        cmds.text(label="Att Type:", p='valuebuttonlayout', align="right", w=50)
        self.attrType=cmds.text(label="", p='valuebuttonlayout', w=100)       
        cmds.button (label='Refresh Selection', p='valuebuttonlayout',  w=100, command = lambda *args:self._refresh())
        cmds.gridLayout('getattButtonLayout', p='title1', numberOfColumns=3, cellWidthHeight=(148, 20))
        cmds.button (label='Fill Find',p='getattButtonLayout', command = lambda *args:self._fill_find())
        cmds.button (label='Eyedrop Attr top', p='getattButtonLayout', command = lambda *args:self.eyedropper_single(getFirstattr=cmds.optionMenu(self.attributeFirstSel, q=1, v=1)))
        cmds.button (label='Eyedrop Attr bot', p='getattButtonLayout', command = lambda *args:self.eyedropper(getFirstattr=cmds.optionMenu(self.attributeFirstSel, q=1, v=1)))
        cmds.gridLayout('srch4attButtonLayout', p='title1', numberOfColumns=3, cellWidthHeight=(148, 20))
        cmds.text(label="Search:", align="left", w=50)
        self.findAttr=cmds.textField( text="Enter name EG:'translate'")
        cmds.button (label='Fetch Attribute Name',  bgc=[0.55, 0.6, 0.6], command = lambda *args:self._find_att(getName=cmds.textField(self.findAttr, q=1, text=1)))
        cmds.text(label="Search:", align="left", w=50)
        valueAttr=cmds.textField(text="Enter value EG:'1.0'")
        cmds.button (label='Fetch Attribute Value',  bgc=[0.55, 0.6, 0.6], command = lambda *args:self._find_value(getFirstattr=cmds.optionMenu(self.attributeFirstSel, q=1, ill=1), values=cmds.textField(valueAttr, q=1, text=1)))
        cmds.gridLayout('listBuildLayout', p='title1', numberOfColumns=1, cellWidthHeight=(445, 20))   
        self.attributeFirstSel=cmds.optionMenu( label='Find', cc=lambda *args:self.change_attr_output())
        for each in getFirstAttr:
            cmds.menuItem( label=each)
        cmds.gridLayout('listBuildButtonLayout', p='title1', numberOfColumns=3, cellWidthHeight=(148, 20))
        cmds.text(label="Change Value:", align="left", w=50)        
        makeAttr=cmds.textField(w=150, text="enter value EG:'50'")
        cmds.button (label='Apply Value', p='listBuildButtonLayout', w=150, command = lambda *args:self._apply_att(getFirstattr=cmds.optionMenu(self.attributeFirstSel, q=1, v=1), makeAttr=cmds.textField(makeAttr, q=1, text=1)))
        #search object by attribute
        cmds.frameLayout('title2', bgc=[0.15, 0.15, 0.15], cll=1, label='Find Objects by Attribute', lv=1, nch=1, borderStyle='out', bv=1, w=450, fn="tinyBoldLabelFont", p='selectArrayColumn')
        cmds.gridLayout('valuebuttonlayout2', p='title2', numberOfColumns=5, cellWidthHeight=(50, 20))          
        cmds.text(label="Att Value:", p='valuebuttonlayout2', align="left", w=50)
        self.attrValObj=cmds.text(label="Select from drop down", p='valuebuttonlayout2', w=100)
        cmds.text(label="Att Type:", p='valuebuttonlayout2', align="right", w=50)
        self.attrTypeObj=cmds.text(label="", p='valuebuttonlayout2', w=100)
        self.select=cmds.text(label="select on", p='valuebuttonlayout2', al="right", w=100)  
        cmds.popupMenu(button=1)
        self.selectOn=cmds.menuItem  (label='select on', command = self._change_to_select_on)
        self.selectOff=cmds.menuItem  (label='select off', command = self._change_to_select_off)              
        cmds.gridLayout('findbyattrButtonLayout', p='title2', numberOfColumns=2, cellWidthHeight=(148, 20))
        cmds.text(label="Att name:", align="left", w=50)
        self.findAttrObj=cmds.textField(text="Enter name EG:'translate'")
        cmds.text(label="Att value:", align="left", w=50)
        valueAttrObj=cmds.textField(text="Enter value EG:'1.0'")
        cmds.button (label='Fetch Object by Att Name',  bgc=[0.55, 0.6, 0.6], p='findbyattrButtonLayout', command = lambda *args:self._find_att_obj(getName=cmds.textField(self.findAttrObj, q=1, text=1)))
        cmds.button (label='Fetch Objects by Att Value',  bgc=[0.55, 0.6, 0.6], p='findbyattrButtonLayout', command = lambda *args:self._find_value_obj(values=cmds.textField(valueAttrObj, q=1, text=1)))
        cmds.button (label='Filter Sel by Att Name',  bgc=[0.55, 0.6, 0.6], p='findbyattrButtonLayout', command = lambda *args:self._filter_att_obj(getName=cmds.textField(self.findAttrObj, q=1, text=1)))
        cmds.button (label='Filter by Att + Value',  bgc=[0.55, 0.6, 0.6], p='findbyattrButtonLayout', command = lambda *args:self._filter_att_value(getFirstattr=cmds.textField(self.findAttrObj, q=1, text=1), values=cmds.textField(valueAttrObj, q=1, text=1)))
        cmds.gridLayout('findObjByAttrGLayout', p='title2', numberOfColumns=1, cellWidthHeight=(445, 20))
        self.objAtt=cmds.optionMenu( label='Found', cc=lambda *args:self.change_attr_output_obj())
        for each in getFirstAttr:
            cmds.menuItem( label=getSel[0]+"."+each)
        cmds.gridLayout('listBuildButtonLayout2', p='title2', numberOfColumns=2, cellWidthHeight=(115, 20))
        cmds.text(label="Change Value:", align="left", w=50)        
        makeAttrObj=cmds.textField(w=150, text="enter value EG:'50'")      
        # cmds.button (label='Apply Value', p='listBuildButtonLayout2', w=100, command = lambda *args:self.apply_att_callup(getFirstattr=cmds.optionMenu(self.objAtt, q=1, v=1), makeAttr=cmds.textField(makeAttrObj, q=1, text=1)))
        # cmds.button (label='Apply Value All', p='listBuildButtonLayout2', w=100, command = lambda *args:self.apply_att_callup_all(makeAttr=cmds.textField(makeAttrObj, q=1, text=1)))
        cmds.button (label='Apply Value Sel', p='listBuildButtonLayout2', w=100, command = lambda *args:self.apply_att_callup_sel(values=cmds.textField(makeAttrObj, q=1, text=1), attrName=cmds.textField(self.findAttrObj, q=1, text=1)))
        cmds.button (label='Key selected', p='listBuildButtonLayout2', w=100, command = lambda *args:self.key_att_callup_sel(makeAttr=cmds.textField(makeAttrObj, q=1, text=1), attrName=cmds.textField(self.findAttrObj, q=1, text=1)))
        cmds.button (label='Select all dropdown', p='listBuildButtonLayout2', w=100, command = lambda *args:self._drop_sel(getdrop=cmds.optionMenu(self.objAtt, q=1, ill=1)))
        cmds.showWindow(window)  
        
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
        selectedObject=cmds.ls(sl=1, fl=1, sn=1)
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
        selectedObject=cmds.ls(sl=1, fl=1, sn=1)
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
            
    def _apply_att(self, getFirstattr, makeAttr):
        try:
            makeAttr=float(makeAttr)
        except:
            print "Field must have number"
        try:
            cmds.setAttr(getFirstattr, makeAttr)
            pass
        except:
            print "Unable to change "+getFirstattr+" in this way"
            return
        getChangeAttr=cmds.getAttr(getFirstattr)
        self.count_attr_output(getChangeAttr)
            
    def eyedropper_single(self, getFirstattr):
        if "." in getFirstattr:
            getFirstattr = getFirstattr.split(".")[-1]
        cmds.textField(self.findAttr, e=1, text=getFirstattr)
            
    def eyedropper(self, getFirstattr):
        if "." in getFirstattr:
            getFirstattr = getFirstattr.split(".")[-1]
        cmds.textField(self.findAttrObj, e=1, text=getFirstattr)




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
        
        
    def apply_att(self, getFirstattr, makeAttr):
        self.att_change_callup(getFirstattr, makeAttr)
        getChangeAttr=cmds.getAttr(getFirstattr)
        self.count_attr_output(getChangeAttr)



    def apply_att_callup_sel(self, values, attrName):
        menuItems = cmds.optionMenu(self.objAtt, q=True, v=True)
        print menuItems
        if '.' in menuItems:
            get_attribute=menuItems.split('.')[-1]
        else:
            get_attribute = menuItems
        print get_attribute
        for each in cmds.ls(sl=1, fl=1):
            if "." in each: 
                each= each.split('.')[0]
            else:
                each = each
            if type(values) == float:
            # if values.isfloat == True:
                cmds.setAttr(each+'.'+get_attribute, values)
            elif type(values)==str:
                getNames=cmds.attributeQuery(get_attribute, node = each, le=1)[0].split(":")
                for index, named_value in enumerate(getNames):
                    if named_value == values:
                        if "." in each:
                            cmds.setAttr(each, index)
                        else:
                            cmds.setAttr(each+'.'+get_attribute, index)
            elif values.isdigit() == True:
                if "." in each:
                    cmds.setAttr(each, int(values))
                else:
                    cmds.setAttr(each+'.'+get_attribute, int(values))                            
            # elif type(values)==int:
                # cmds.setAttr(each+'.'+get_attribute, values)


    def key_att_callup_sel(self, makeAttr, attrName):
        menuItems = cmds.optionMenu(self.objAtt, q=True, v=True)
        print menuItems
        get_attribute=menuItems.split('.')[-1]
        print get_attribute
        for each in cmds.ls(sl=1, fl=1):
            try:
                cmds.setKeyframe( each, at=get_attribute)
            except:
                pass


    def _drop_sel(self, getdrop):
        menuItems = cmds.optionMenu(self.objAtt, q=True, ils=True)
        collectTheThings=[]
        for each in menuItems:
            getThing=cmds.menuItem(each, q=1, label=1)   
            collectTheThings.append(getThing)
        cmds.select(collectTheThings, r=1)


    def apply_att_callup(self, getFirstattr, makeAttr):
        getFirstattr=[getFirstattr]
        for each in getFirstattr:
            getChangeAttr=getAttr(each)
            self.att_change_callup(each, makeAttr)
            getChangeAttr=getAttr(each)
            self.count_attr_output_obj(getChangeAttr)
            
    def apply_att_change_callup_all(self, makeAttr):
        menuItems=cmds.optionMenu(self.objAtt, q=1, ill=1)
        if menuItems:
            for each in menuItems:
                getThing=menuItem(each, q=1, label=1)
                getChangeAttr=getAttr(getThing)
                self.att_change_callup(getThing, makeAttr)
            self.count_attr_output_obj(getChangeAttr)
            
    def att_change_callup(self, eachObj, makeAttr):
        # try:
        #     makeAttr=float(makeAttr)
        # except:
        #     print "Field must have number"
        # try:
        #     cmds.setAttr(eachObj, makeAttr)
        # except:
        #     print "Unable to change "+eachObj+" in this way"
        #     return
        menuItems = cmds.optionMenu(self.objAtt, q=True, v=True)
        getAttr=menuItems.split('.')[-1]
        if type(values) == float:
            cmds.setAttr(eachObj+'.'+getAttr, values)
        elif type(values)==str or type(values)==unicode:
            getNames=cmds.attributeQuery(getAttr, node = eachObj, le=1)[0].split(":")
            for index, named_value in enumerate(getNames):
                if named_value == values:
                    if "." in eachObj:
                        cmds.setAttr(eachObj, index)
                    else:
                        cmds.setAttr(eachObj+'.'+getAttr, index)
        elif type(values)==int:
            cmds.setAttr(eachObj+'.'+getAttr, values)

    def _change_to_select_on(self, arg=None):
        print "tool error: button function not built yet"

    def _change_to_select_off(self, arg=None):
        print "tool error: button function not built yet"

    def _refresh(self, arg=None):
        menuItems = cmds.optionMenu(self.attributeFirstSel, q=True, ill=True)
        if menuItems:
            cmds.deleteUI(menuItems)        
        newSel=cmds.ls(sl=1, fl=1)
        getListAttr=cmds.listAttr (newSel[0], w=1, a=1, s=1,u=1)
        getListAttr=sorted(getListAttr)
        cmds.optionMenu(self.attributeFirstSel, e=1)
        for each in getListAttr:
            cmds.menuItem(label=each, parent=self.attributeFirstSel)     
                
    def _get_attr(self, getFirstattr):
        getSel=ls(sl=1, fl=1)        
        newAttr=getattr(getSel[0],getFirstattr)
        getChangeAttr=getattr(getSel[0],getFirstattr).get()
        select(newAttr, add=1)
        self.count_attr_output(getChangeAttr)
        print newAttr, getChangeAttr

    def _fill_find(self):       
        getSel=cmds.ls(sl=1, fl=1)
        collectAttr=[]
        for each in getSel:
            print each
            Attrs=[(attrItem) for attrItem in cmds.listAttr (each, w=1, u=1)]
            if len(Attrs)>0:        
                for item in Attrs:
                    print item
                    newItem=each+"."+item
                    print newItem
                    collectAttr.append(newItem)
        menuItems = cmds.optionMenu(self.attributeFirstSel, q=True, ill=True)
        if menuItems:
            cmds.deleteUI(menuItems)       
        getListAttr=sorted(collectAttr)
        cmds.optionMenu(self.attributeFirstSel, e=1)
        for each in getListAttr:
            cmds.menuItem(label=each, parent=self.attributeFirstSel)    




    def _find_att(self, getName):       
        getSel=cmds.ls(sl=1, fl=1)
        if "," in getName:
            getName=getName.split(", ")
        else:
            getName=[getName]
        collectAttr=[]
        for each in getSel:
            print each
            Attrs=[(attrItem) for attrItem in cmds.listAttr (each, w=1, u=1) for attrName in getName if attrName in attrItem]
            if len(Attrs)>0:        
                for item in Attrs:
                    print item
                    newItem=each+"."+item
                    print newItem
                    collectAttr.append(newItem)
        getChangeAttr=cmds.getAttr(collectAttr[0])
        menuItems = cmds.optionMenu(self.attributeFirstSel, q=True, ill=True)
        if menuItems:
            cmds.deleteUI(menuItems)       
        getListAttr=sorted(collectAttr)
        cmds.optionMenu(self.attributeFirstSel, e=1)
        for each in getListAttr:
            cmds.menuItem(label=each, parent=self.attributeFirstSel)    
        self.count_attr_output(getChangeAttr)
        print getChangeAttr



    def _find_att_obj(self, getName):       
        if "," in getName:
            getName=getName.split(", ")
        else:
            getName=[getName]
        Attrs=[(attrItem) for attrName in getName for attrItem in cmds.ls ('*.'+attrName)]
        collectMoreAttrs=[(attrItem) for attrName in getName for attrItem in cmds.ls ('*:*.'+attrName)]
        Attrs=Attrs+collectMoreAttrs
        menuItems = cmds.optionMenu(self.objAtt, q=True, ill=True)
        if menuItems:
            cmds.deleteUI(menuItems)       
        getListAttr=sorted(Attrs)
        cmds.optionMenu(self.objAtt, e=1)
        for each in getListAttr:
            cmds.menuItem(label=each, parent=self.objAtt)  

    def _filter_att_obj(self, getName):       
        getAll=cmds.ls(sl=1)       
        if "," in getName:
            getName=getName.split(", ")
        else:
            getName=[getName]
        collectAttr=[]
        for each in getAll:
            Attrs=[(attrItem) for attrItem in cmds.listAttr (each, w=1, a=1, s=1,u=1) for attrName in getName if attrName in attrItem]
            if len(Attrs)>0:        
                for item in Attrs:
                    newItem=each+"."+item
                    collectAttr.append(newItem)
        menuItems = cmds.optionMenu(self.objAtt, q=True, ill=True)
        if menuItems:
            cmds.deleteUI(menuItems)       
        getListAttr=sorted(collectAttr)
        cmds.optionMenu(self.objAtt, e=1)
        for each in getListAttr:
            cmds.menuItem(label=each, parent=self.objAtt)  

    def _find_value_obj(self, values):
        if type(values) == float:
            find_attrs=[(objectItem+'.'+attrItem)  for objectItem in cmds.ls ('*:*') for attrItem in cmds.listAttr (objectItem, w=1, a=1, s=1,u=1) if cmds.getAttr(objectItem+'.'+attrItem)==float(values)]
            more_find_attrs=[(objectItem+'.'+attrItem)  for objectItem in cmds.ls ('*:*') for attrItem in cmds.listAttr (objectItem, w=1, a=1, s=1,u=1) if cmds.getAttr(objectItem+'.'+attrItem)==float(values)]
            Attrs = find_attrs+more_find_attrs
        elif type(values)==str or type(values)==unicode:
            Attrs=[]
            find_attrs = [(each+"."+item) for each in cmds.ls("*:*") for item in cmds.listAttr(each, w=1,hd=1, s=1, m=0)]
            more_find_attrs = [(each+"."+item) for each in cmds.ls("*") for item in cmds.listAttr(each, w=1,hd=1, s=1, m=0)]
            find_attrs = find_attrs+more_find_attrs
            for each_att in find_attrs:
                if cmds.objExists(each_att):
                    if cmds.getAttr(each_att, type=1) == "enum":
                        if cmds.getAttr(each_att, sl=1, asString=1) == str(values):
                            Attrs.append(each_att)
        elif type(values)==int:
            find_attrs=[(objectItem+'.'+attrItem)  for objectItem in cmds.ls ('*:*') for attrItem in cmds.listAttr (objectItem, w=1, a=1, s=1,u=1) if cmds.getAttr(objectItem+'.'+attrItem)==int(values)]
            more_find_attrs=[(objectItem+'.'+attrItem)  for objectItem in cmds.ls ('*:*') for attrItem in cmds.listAttr (objectItem, w=1, a=1, s=1,u=1) if cmds.getAttr(objectItem+'.'+attrItem)==int(values)]
            Attrs = find_attrs+more_find_attrs
        menuItems = cmds.optionMenu(self.objAtt, q=True, ill=True)
        if menuItems:
            cmds.deleteUI(menuItems)       
        getListAttr=sorted(Attrs)
        cmds.optionMenu(self.objAtt, e=1)
        for each in getListAttr:
            cmds.menuItem(label=each, parent=self.objAtt)  

    def _filter_att_value(self, getFirstattr, values):
        if "," in getFirstattr:
            getName=getName.split(", ")
        else:
            getName=[getFirstattr]
        Attrs=[(objectItem+'.'+attrItem) for objectItem in cmds.ls (sl=1) for attrItem in cmds.listAttr (objectItem, w=1, a=1, s=1,u=1) for attrName in getName if attrName in attrItem and cmds.getAttr(objectItem+'.'+attrItem)==float(values)]
        menuItems = cmds.optionMenu(self.objAtt, q=True, ill=True)
        if menuItems:
            cmds.deleteUI(menuItems)       
        getListAttr=sorted(Attrs)
        cmds.optionMenu(self.objAtt, e=1)
        for each in getListAttr:
            cmds.menuItem(label=each, parent=self.objAtt)  




    def _find_value(self, getFirstattr, values):
        # try:
        #     values=float(values)
        # except:
        #     values=int(values)
        # getSel=cmds.ls(sl=1, fl=1)        
        # collectAttr=[]
        # for each in getFirstattr:
        #     getSel=cmds.ls(getSel[0])
        #     find=cmds.menuItem(each, q=1, label=1)
        #     try:
        #         foundAttr=cmds.getattr(getSel[0],find).get()
        #     except:
        #         pass
        #     if foundAttr == values:
        #         collectAttr.append(find)         
        print values
        try: 
            float(values)
            if type(values) == float:
                print "float"
                find_attrs=[(objectItem+'.'+attrItem)  for objectItem in cmds.ls (sl=1) for attrItem in cmds.listAttr (objectItem, w=1, a=1, s=1,u=1) if cmds.getAttr(objectItem+'.'+attrItem)==float(values)]
                collectAttr = find_attrs 
        except:
            pass
        try: 
            str(values)
            if type(values)==str or type(values)==unicode:
                print "string"
                collectAttr=[]
                find_attrs = [(each+"."+item) for each in cmds.ls (sl=1) for item in cmds.listAttr(each, w=1,hd=1, s=1, m=0)]
                for each_att in find_attrs:
                    if cmds.objExists(each_att):
                        if cmds.getAttr(each_att, type=1) == "enum":
                            if cmds.getAttr(each_att, sl=1, asString=1) == str(values):
                                collectAttr.append(each_att)
        except:
            pass
        try: 
            str(values)     
            if type(values)==int:
                print "int"
                find_attrs=[(objectItem+'.'+attrItem)  for objectItem in cmds.ls (sl=1) for attrItem in cmds.listAttr (objectItem, w=1, a=1, s=1,u=1) if cmds.getAttr(objectItem+'.'+attrItem)==int(values)]
                collectAttr = find_attrs
        except:
            pass
        print collectAttr          
        cmds.optionMenu(self.attributeFirstSel, e=1, v=collectAttr[0])
        newAttr=cmds.getattr(getSel[0],collectAttr[0])
        cmds.select(newAttr, add=1)
        getChangeAttr=cmds.getattr(getSel[0],collectAttr[0]).get()
        menuItems = cmds.optionMenu(self.attributeFirstSel, q=True, ill=True)
        if menuItems:
            cmds.deleteUI(menuItems)        
        getListAttr=sorted(collectAttr)
        cmds.optionMenu(self.attributeFirstSel, e=1)
        for each in getListAttr:
            menuItem(label=each, parent=self.attributeFirstSel)  
        self.count_attr_output(getChangeAttr)
        print newAttr, getChangeAttr


        # if type(values) == float:
        #     find_attrs=[(objectItem+'.'+attrItem)  for objectItem in cmds.ls (sl=1) for attrItem in cmds.listAttr (objectItem, w=1, a=1, s=1,u=1) if cmds.getAttr(objectItem+'.'+attrItem)==float(values)]
        # elif type(values)==str or type(values)==unicode:
        #     collectAttr=[]
        #     find_attrs = [(each+"."+item) for each in cmds.ls (sl=1) for item in cmds.listAttr(each, w=1,hd=1, s=1, m=0)]
        #     for each_att in find_attrs:
        #         if cmds.objExists(each_att):
        #             if cmds.getAttr(each_att, type=1) == "enum":
        #                 if cmds.getAttr(each_att, sl=1, asString=1) == str(values):
        #                     collectAttr.append(each_att)
        # elif type(values)==int:
        #     find_attrs=[(objectItem+'.'+attrItem)  for objectItem incmds.ls (sl=1) for attrItem in cmds.listAttr (objectItem, w=1, a=1, s=1,u=1) if cmds.getAttr(objectItem+'.'+attrItem)==int(values)]
        #     collectAttr = find_attrs




    def count_attr_output(self, getChangeAttr):
        '''----------------------------------------------------------------------------------
        ----------------------------------------------------------------------------------'''
        cmds.text(self.attrVal, e=1, label=getChangeAttr )

    def change_attr_output(self):
        '''----------------------------------------------------------------------------------
        ----------------------------------------------------------------------------------'''
        getFirstattr=cmds.optionMenu(self.attributeFirstSel, q=1, v=1)  
        cmds.getAttr(getFirstattr)
        try:
            getChangeAttr=cmds.getAttr(getFirstattr)
            getTypeAttr=cmds.getAttr(getFirstattr, type=1)
            pass
        except:
            print "Can't obtain value for "+getFirstattr
            return               
        cmds.text(self.attrVal, e=1, label=getChangeAttr )
        cmds.text(self.attrType, e=1, label=getTypeAttr )

    def count_attr_output_obj(self, getChangeAttr):
        '''----------------------------------------------------------------------------------
        ----------------------------------------------------------------------------------'''
        cmds.text(self.attrValObj, e=1, label=getChangeAttr )

    def change_attr_output_obj(self):
        '''----------------------------------------------------------------------------------
        ----------------------------------------------------------------------------------'''
        getFirstattr=cmds.optionMenu(self.objAtt, q=1, v=1)
        cmds.select(str(getFirstattr.split(".")[0]), r=1)
        try:
            getAttr=cmds.getAttr(getFirstattr)
            getTypeAttr=cmds.getAttr(getFirstattr, type=1)
            pass
        except:
            print "Can't obtain value for "+getFirstattr
            return               
        cmds.text(self.attrValObj, e=1, label=getAttr )
        cmds.text(self.attrTypeObj, e=1, label=getTypeAttr )


inst=fetchAttrs()
inst._findAttr_window()






