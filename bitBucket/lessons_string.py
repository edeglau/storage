        
    def apply_att(self, getFirstattr, makeAttr):
        self.att_change_callup(getFirstattr, makeAttr)
        getChangeAttr=cmds.getAttr(getFirstattr)
        self.count_attr_output(getChangeAttr)
        
     def apply_att_callup_sel(self, values, attrName):
        menuItems = cmds.optionMenu(self.objAtt, q=True, v=True)
        getAttr=menuItems.split('.')[-1]
        for each in cmds.ls(sl=1, fl=1):
            if type(values) == float:
                cmds.setAttr(each+'.'+getAttr, values)
            elif type(values)==str or type(values)==unicode:
                getNames=cmds.attributeQuery(getAttr, node = each, le=1)[0].split(":")
                for index, named_value in enumerate(getNames):
                    if named_value == values:
                        if "." in each:
                            cmds.setAttr(each, index)
                        else:
                            cmds.setAttr(each+'.'+getAttr, index)
            elif type(values)==int:
                cmds.setAttr(each+'.'+getAttr, values)

    def key_att_callup_sel(self, makeAttr, attrName):
        menuItems = cmds.optionMenu(self.objAtt, q=True, v=True)
        print menuItems
        getAttr=menuItems.split('.')[-1]
        print getAttr
        for each in cmds.ls(sl=1, fl=1):
            try:
                cmds.setKeyframe( each, at=getAttr)
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
        newSel=ls(sl=1, fl=1)
        getListAttr=listAttr (newSel[0], w=1, a=1, s=1,u=1)
        getListAttr=sorted(getListAttr)
        cmds.optionMenu(self.attributeFirstSel, e=1)
        for each in getListAttr:
            menuItem(label=each, parent=self.attributeFirstSel)   
            
            
                
    def _get_attr(self, getFirstattr):
        getSel=ls(sl=1, fl=1)        
        newAttr=getattr(getSel[0],getFirstattr)
        getChangeAttr=getattr(getSel[0],getFirstattr).get()
        select(newAttr, add=1)
        self.count_attr_output(getChangeAttr)
        print newAttr, getChangeAttr
        
    def _find_att(self, getName):       
        getSel=cmds.ls(sl=1, fl=1)
        if "," in getName:
            getName=getName.split(", ")
        else:
            getName=[getName]
        collectAttr=[]
        for each in getSel:
            print each
            Attrs=[(attrItem) for attrItem in cmds.listAttr (each, w=1, a=1, s=1,u=1) for attrName in getName if attrName in attrItem]
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
            
    def _find_value(self, getFirstattr, values):
        try:
            values=float(values)
        except:
            values=int(values)
        getSel=ls(sl=1, fl=1)        
        collectAttr=[]
        for each in getFirstattr:
            getSel=ls(getSel[0])
            find=menuItem(each, q=1, label=1)
            try:
                foundAttr=getattr(getSel[0],find).get()
            except:
                pass
            if foundAttr == values:
                print foundAttr
                collectAttr.append(find)                 
        optionMenu(self.attributeFirstSel, e=1, v=collectAttr[0])
        newAttr=getattr(getSel[0],collectAttr[0])
        select(newAttr, add=1)
        getChangeAttr=getattr(getSel[0],collectAttr[0]).get()
        menuItems = cmds.optionMenu(self.attributeFirstSel, q=True, ill=True)
        if menuItems:
            cmds.deleteUI(menuItems)        
        getListAttr=sorted(collectAttr)
        cmds.optionMenu(self.attributeFirstSel, e=1)
        for each in getListAttr:
            menuItem(label=each, parent=self.attributeFirstSel)  
        self.count_attr_output(getChangeAttr)
        print newAttr, getChangeAttr            
