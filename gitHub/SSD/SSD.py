'''
Created on Jul 7, 2011
Swim Stream

@author: elise.deglau

'''

'''Swim stream'''
__author__ = "Elise Deglau"
__version__ = 1.00
'This work is licensed under a Creative Commons License'
'http://creativecommons.org/licenses/by-sa/3.0/au/'

import maya.cmds as cmds
from functools import partial
from string import *
import re
import maya.mel
##the following library outmeshs/inmeshs is determining the connections of the network per input>>node>>output. Currently set to accommodate rig edits. Edit to suit need.
outmeshs=["outputGeometry", "outputGeometry[0]", "outMesh", "outputMesh", "worldMesh", "worldMesh[0]", "_outMesh", "output" ]
inmeshs=["input[0].inputGeometry", "inputGeometry", "inMesh", "inputMesh", "basePoints", "input"]

class ui(object):
    def __init__(self, winName="swimtWindow"):
        self.winTitle = "Stream swimming - Developer mode"
        self.winName = winName

    def create(self):
        global drown
        global urp
        global ctAt_name
        global nd_name
        global add_in
        global ndeLst
        global joe
        global jotl
        global sel_ON
        global sel_PN

        if cmds.window(self.winName, exists=True):
                cmds.deleteUI(self.winName)

        self.window = cmds.window(self.winName, title=self.winTitle, tbm=1, w=800, h=480 )

        cmds.menuBarLayout(h=30)
        fileMenu = cmds.menu( label='clean interface', pmc=self.clnint )
        cmds.rowColumnLayout  (' JrRow ', nr=3, nch=3, rat=[(1, 'top', 0),(2, 'bottom', 0)], rh=[(1, 50),(2, 450)], w=680)

        cmds.frameLayout('LrRow', label='', lv=0, nch=2, borderStyle='out', bv=1, p='JrRow')
        cmds.rowLayout  (' KrRow ', p='LrRow', numberOfColumns=50, w=680, h=50)
        cmds.gridLayout('KR_sh', p='KrRow', numberOfColumns=6, cellWidthHeight=(90, 20))
        cmds.button( label='outliner', c=self.olw , w=90, p='KR_sh')
        cmds.button( label='hypergraph', c=self.hg , w=90, p='KR_sh')
        cmds.button( label='update graph', c=self.hgu , w=90, p='KR_sh')
        cmds.button( label='connnect edit', c=self.cw , w=90, p='KR_sh')
        cmds.button( label='hypershade', c=self.hsw , w=90, p='KR_sh')
        cmds.button( label='add attribute', c=self.ada , w=90, p='KR_sh')
        cmds.button( label='edit attribute', c=self.ea , w=90, p='KR_sh')
        cmds.button( label='channel control', c=self.chan , w=90, p='KR_sh')
        cmds.button( label='set driven key', c=self.sdk , w=90, p='KR_sh')
        cmds.button( label='script editor', c=self.scrpted , w=90, p='KR_sh')
        #cmds.button( label='float Att', c=self.fltAtt , w=90, p='KR_sh')

        cmds.rowLayout  (' rMainRow ', w=150, numberOfColumns=6, cw6=[160, 500, 1, 1, 1, 1], ct6=[ 'both', 'right', 'right',  'right', 'both', 'both'], p='JrRow')
        cmds.columnLayout ('KLrColumn1', parent = 'rMainRow')
        cmds.setParent ('KLrColumn1')##################find node
        cmds.text (label='Selection arrays', p='KLrColumn1')
        cmds.separator(h=10, p='KLrColumn1')
        cmds.gridLayout('IO_sh', p='KLrColumn1', numberOfColumns=2, cellWidthHeight=(80, 20))
        cmds.button (label='grab node', p='IO_sh', command = self.fndNd )
        cmds.button (label='grab name', p='IO_sh', command = self.findName )
        cmds.button (label='filter node', p='IO_sh', command = self.selNd )
        cmds.popupMenu(button=1)
        cmds.menuItem  (label='filter selected by type and make list', command = self.selNd )
        cmds.menuItem  (label='filter selected by type and add to list', command = self.adfltnd )
        cmds.button (label='filter name', p='IO_sh', command = self.selname )
        cmds.popupMenu(button=1)
        cmds.menuItem  (label='filter selected by name and make list', command = self.selname )
        cmds.menuItem  (label='filter selected by name and add to list', command = self.adfltnm )
        #cmds.button (label='sel all node', p='IO_sh', command = self.selAl )
        cmds.popupMenu(button=1)
        #cmds.menuItem  (label='select all scene by type and make list', command = self.selAl )
        cmds.menuItem  (label='select all scene by type and add to list', command = self.adaltnd )
        cmds.button (label='sel all name', p='IO_sh', command = self.selAlname )
        cmds.popupMenu(button=1)
        cmds.menuItem  (label='select all scene by name and make list', command = self.selAlname )
        cmds.menuItem  (label='select all scene by name and add to list', command = self.adaltnm )
        cmds.text (label='name or node type',  p='KLrColumn1')
        cmds.gridLayout('PO_sm', p='KLrColumn1', numberOfColumns=2, cellWidthHeight=(120, 25))
        nd_name=cmds.textField(w=120, h=25, p='PO_sm')
        cmds.button (label='find', command = self.fnd , p='PO_sm', w=40, ann='find this name in list below')
        cmds.text (label='selection list', p='KLrColumn1')
        cmds.textField(nd_name, edit=True, enterCommand=('cmds.setFocus(\"' + nd_name + '\")'))
        ndeLst=cmds.textScrollList( numberOfRows=8, ra=1, allowMultiSelection=True, sc=self.selNod , dcc=self.nodesel2 , dkc=self.nodesel2 , io=True, w=150, h=220, p='KLrColumn1')
        cmds.gridLayout('IO_sm', p='KLrColumn1', numberOfColumns=4, cellWidthHeight=(40, 20))
        cmds.button (label='clr', command = self.clr , p='IO_sm')
        cmds.button (label='+', command = self.pls , p='IO_sm')
        cmds.button (label='-', command = self.mns , p='IO_sm')
        cmds.button (label='><', command = self.swp , p='IO_sm', ann='swap out selected in list with selected in scene')
        cmds.button (label='selal', command = self.sall , p='IO_sm', w=40, ann='select all')
        cmds.button (label='sel- ', command = self.snon , p='IO_sm', w=40, ann='select none')
        cmds.button (label='sort', command = self.srt , p='IO_sm', w=40, ann='sort alphabetically-numerally')
        cmds.button (label='set', command = self.mkset , p='IO_sm', w=40, ann='create set from selected in list')

        cmds.frameLayout('SB', label='StreamSwim', li=180, la="center", borderStyle='etchedIn', bv=1, p='rMainRow', w=480, h=400, mw=10)
        cmds.rowLayout  (' SS_window_row ', w=150, numberOfColumns=6, cw6=[150, 150, 150, 1, 1, 1], ct6=[ 'both', 'both', 'both',  'both', 'both', 'both'], p='SB')
        cmds.columnLayout ('rColumn1', parent = 'SS_window_row')
        cmds.columnLayout ('rColumn2', parent = 'SS_window_row')
        cmds.columnLayout ('rColumn3', parent = 'SS_window_row')

        cmds.setParent ('rColumn1')##################upstream window
        cmds.gridLayout('uplst_st', p='rColumn1', numberOfColumns=2, cellWidthHeight=(75, 20))
        cmds.text("up stream", p='uplst_st', al='left')
        cmds.popupMenu(button=1)
        cmds.menuItem  (label='CW Left', command = self.upL )
        cmds.menuItem  (label='CW Right', command = self.upR )
        sel_PN=cmds.text("seloff", p='uplst_st', al='right', w=75)
        cmds.popupMenu(button=1)
        cmds.menuItem  (label='seloff', command = self.suoff )
        cmds.menuItem  (label='selon', command = self.suon )
        urp=cmds.textScrollList( numberOfRows=8,ra=1, allowMultiSelection=False, sc=self.strnupOFF , dcc=self.strselup , dkc=self.strselup , p= 'rColumn1', w=150, h=330)
        cmds.gridLayout('IO_sL', p='rColumn1', numberOfColumns=4, cellWidthHeight=(35, 20))
        cmds.button (label='clr', command = self.clrup , p='IO_sL')
        cmds.button (label='-', command = self.mnsup , p='IO_sL')

        cmds.setParent ('rColumn2')##################link buttons
        cmds.gridLayout('uplst_st', p='rColumn2', numberOfColumns=2, cellWidthHeight=(75, 20))
        joe=cmds.text(label='no focus', p='rColumn2', rs=0, w=150, fn="boldLabelFont", h=50)
        cmds.popupMenu(button=1)
        cmds.menuItem  (label='CW Left', command = self.cwlL )
        cmds.menuItem  (label='CW Right', command = self.cwlR )
        cmds.menuItem  (label='Refocus', command = self.re_foc )
        
        
        ##################buttons
        cmds.gridLayout('sl_Grd', p='rColumn2', numberOfColumns=1, cellWidthHeight=(150, 20))
        cmds.button (label='Focus', command = self.focsSel , p='sl_Grd', w=150, h=20)
        cmds.button (label='Append connections', command = self.appcon , p='sl_Grd', w=150, h=20)
        cmds.gridLayout('gash', p='rColumn2', numberOfColumns=2, cellWidthHeight=(75, 20))
        cmds.separator (h=20, p='rColumn2', vis=1, w=150)
        cmds.text("surf", al='center', p='rColumn2', rs=0, w=150)
        cmds.gridLayout('awf', p='rColumn2', numberOfColumns=2, cellWidthHeight=(75, 20))
        cmds.button (label='<<up', al='left', command = self.upstr , p='awf')
        cmds.button (label='down>>', al='right', command = self.dnstr , p='awf')
        cmds.separator (h=30, p='rColumn2', vis=1, w=150)
        add_in=cmds.text("Connect", al='center', p='rColumn2', rs=0, w=150)
        cmds.gridLayout('a_f', p='rColumn2', numberOfColumns=2, cellWidthHeight=(75, 20))
        cmds.button (label='bypass', command = self.bypss , p='a_f')
        cmds.button ('sn', label='AttLockin')
        cmds.popupMenu(button=1)
        cmds.menuItem  (label='unlock', command = self.unlckin )
        cmds.menuItem  (label='lock', command = self.lckin )
        cmds.button (label='<<Insert', command = self.upstreamInsert  , p='a_f')
        cmds.button (label='Insert>>', command = self.downstreamInsert  , p='a_f')
        cmds.button (label='<<Connect', command = self.upstrcon  , p='a_f')
        cmds.button (label='Connect>>', command = self.dnstrcon   , p='a_f')
        cmds.button (label='<<Choice', command = self.chN_in , p='a_f')
        cmds.button (label='Choice>>', command = self.chN_ot , p='a_f')


        cmds.setParent ('rColumn3')##################downstream window
        cmds.gridLayout('dnlst_st', p='rColumn3', numberOfColumns=2, cellWidthHeight=(75, 20))
        cmds.text("down stream", al='left', w=100, p='dnlst_st')
        cmds.popupMenu(button=1)
        cmds.menuItem  (label='CW Left', command = self.dnL )
        cmds.menuItem  (label='CW Right', command = self.dnR )
        sel_ON=cmds.text("seloff", p='dnlst_st', al='right', w=75)
        cmds.popupMenu(button=1)
        cmds.menuItem  (label='seloff', command = self.sdoff )
        cmds.menuItem  (label='selon', command = self.sdon )
        drown=cmds.textScrollList( numberOfRows=8, ra=1, allowMultiSelection=False, sc=self.strngOFF , dcc=self.strseldn , dkc=self.strseldn , p= 'rColumn3', io=True, w=150, h=330)
        cmds.gridLayout('IO_sR', p='rColumn3', numberOfColumns=4, cellWidthHeight=(35, 20))
        cmds.button (label='clr', command = self.clrdn , p='IO_sR')
        cmds.button (label='-', command = self.mnsdn , p='IO_sR')

        cmds.showWindow(self.window)




#     def fltAtt(self, arg=None):
#         import controllerUI
#         reload(controllerUI)
#         from controllerUI import *
    
    def fnd(self, arg=None):###################select all node type in scene
        who=cmds.textField(nd_name, q=True, text=True)
        bH_i=cmds.textScrollList(ndeLst, q=1, ai=1)
        for r in range (len(bH_i)):
            if who in bH_i[r]:
                cmds.textScrollList(ndeLst, e=1, da=1, w=150, h=220)
                cmds.textScrollList(ndeLst, e=1, si=who, w=150, h=220)
                print who+' found'
        else:
            cmds.textScrollList(ndeLst, e=1, da=1, w=150, h=220)
            print who+' not found in this list'
    
    def adaltnm(self, arg=None):###################select all node type in scene
        who=cmds.textField(nd_name, q=True, text=True)
        if who<1:
            print 'nothing selected'
        else:
            cmds.select(who, r=1)
            jack=cmds.ls(sl=1)
            bH_i=cmds.textScrollList(ndeLst, q=1, ai=1)
            if len(jack)>0:
                if jack>1:
                    rg=sorted(jack, key=lower)
                if len(jack)==1:
                    rg=jack
                if bH_i<0:
                    for u in range (len(rg)):
                        cmds.textScrollList(ndeLst, e=1, a=rg[u], w=150, h=220)
                if bH_i>0:
                    for u in range (len(rg)):
                        if rg[u] in bH_i:
                            cmds.textScrollList(ndeLst, e=1, da=1, w=150, h=220)
                            print '%s'%rg[u]+' already in list'
                            cmds.textScrollList(ndeLst, e=1, si=rg[u], w=150, h=220)
                        else:
                            cmds.textScrollList(ndeLst, e=1, a=rg[u], w=150, h=220)
    
    
    def adaltnd(self, arg=None):###################select all node type in scene
        who=cmds.textField(nd_name, q=True, text=True)
        if who<1:
            print 'nothing selected'
        jack=cmds.ls(type=who)
        hgt=[]
        dng=['transform', 'mesh', 'joint', 'shape', 'nurbsCurve', 'shape']
        for r in range(len(jack)):
            for i in range (len(dng)):
                if dng[i] in jack[r]:
                    hgt.append(jack[r])
        if (len(hgt))>0:
            print "This is too common and will likely lock up your scene! Try filtering from a selection"
        else:
            bH_i=cmds.textScrollList(ndeLst, q=1, ai=1)
            if len(jack)>0:
                if jack>1:
                    rg=sorted(jack, key=lower)
                if len(jack)==1:
                    rg=jack
                if bH_i<0:
                    for u in range (len(rg)):
                        cmds.textScrollList(ndeLst, e=1, a=rg[u], w=150, h=220)
                if bH_i>0:
                    for u in range (len(rg)):
                        if rg[u] in bH_i:
                            cmds.textScrollList(ndeLst, e=1, da=1, w=150, h=220)
                            print '%s'%rg[u]+' already in list'
                            cmds.textScrollList(ndeLst, e=1, si=rg[u], w=150, h=220)
                        else:
                            cmds.textScrollList(ndeLst, e=1, a=rg[u], w=150, h=220)
    
    def adfltnm(self, arg=None):###################Select nodetype in selection array
        klo=cmds.ls(sl=1)
        ft_List=[]
        who=cmds.textField(nd_name, q=True, text=True)
        for i in range (len(klo)):
            if who in klo[i]:
                ft_List.append(klo[i])
                cmds.select(ft_List, r=1)
        bH_i=cmds.textScrollList(ndeLst, q=1, ai=1)
        if len(ft_List)>0:
            if ft_List>1:
                rg=sorted(ft_List, key=lower)
            if len(ft_List)==1:
                rg=ft_List
            if bH_i<0:
                for u in range (len(rg)):
                    cmds.textScrollList(ndeLst, e=1, a=rg[u], w=150, h=220)
            if bH_i>0:
                for u in range (len(rg)):
                    if rg[u] in bH_i:
                        cmds.textScrollList(ndeLst, e=1, da=1, w=150, h=220)
                        print '%s'%rg[u]+' already in list'
                        cmds.textScrollList(ndeLst, e=1, si=rg[u], w=150, h=220)
                    else:
                        cmds.textScrollList(ndeLst, e=1, a=rg[u], w=150, h=220)
    
    def adfltnd(self, arg=None):
        klo=cmds.ls(sl=1)
        ft_List=[]
        who=cmds.textField(nd_name, q=True, text=True)
        for i in range (len(klo)):
            filter= cmds.nodeType(klo[i])
            if who in filter:
                ft_List.append(klo[i])
                cmds.select(ft_List, r=1)
        bH_i=cmds.textScrollList(ndeLst, q=1, ai=1)
        if len(ft_List)>0:
            if ft_List>1:
                rg=sorted(ft_List, key=lower)
            if len(ft_List)==1:
                rg=ft_List
            if bH_i<0:
                for u in range (len(rg)):
                    cmds.textScrollList(ndeLst, e=1, a=rg[u], w=150, h=220)
            if bH_i>0:
                for u in range (len(rg)):
                    if rg[u] in bH_i:
                        cmds.textScrollList(ndeLst, e=1, da=1, w=150, h=220)
                        print '%s'%rg[u]+' already in list'
                        cmds.textScrollList(ndeLst, e=1, si=rg[u], w=150, h=220)
                    else:
                        cmds.textScrollList(ndeLst, e=1, a=rg[u], w=150, h=220)
    
    def mkset(self, arg=None):
        nd_set=cmds.textScrollList(ndeLst, q=1, selectItem=1)
        if nd_set<1:
            print "select something from selection list"
        else:
            cmds.sets()
    
    def clrdn(self, arg=None):
        cmds.textScrollList(drown, e=1, ra=1, w=150, h=330)
    
    def mnsdn(self, arg=None):
        shrt=cmds.textScrollList(drown, q=1, selectItem=1)
        if shrt<1:
            print 'select item to subtract from list'
        cmds.textScrollList(drown, e=1, ri=shrt, w=150, h=330)
    
    def clrup(self, arg=None):
        cmds.textScrollList(urp, e=1, ra=1, w=150, h=330)
    
    def mnsup(self, arg=None):
        shrt=cmds.textScrollList(urp, q=1, selectItem=1)
        if shrt<1:
            print 'select item to subtract from list'
        cmds.textScrollList(urp, e=1, ri=shrt, w=150, h=330)
    
    def suoff(self, arg=None):
        cmds.textScrollList(urp, e=1, sc="strnupOFF()", w=150, h=330)
        cmds.text(sel_PN, e=1, label='seloff', w=75)
    
    def suon(self, arg=None):
        cmds.textScrollList(urp, e=1, sc="strnup()", w=150, h=330)
        cmds.text(sel_PN, e=1, label='selon', w=75)
    
    def sdoff(self, arg=None):
        cmds.textScrollList(drown, e=1, sc="strngOFF()", w=150, h=330)
        cmds.text(sel_ON, e=1, label='seloff', w=75)
    
    def sdon(self, arg=None):
        cmds.textScrollList(drown, e=1, sc="strng()", w=150, h=330)
        cmds.text(sel_ON, e=1, label='selon',  w=75)
    
    def appcon(self, arg=None):
        bH_i=cmds.textScrollList(urp, q=1, ai=1)
        bH_d=cmds.textScrollList(drown, q=1, ai=1)
        n_str=cmds.ls(sl=1)
        if n_str<1:
            print 'select item to add to list'
        else:
            ls_str=cmds.listConnections( n_str[0], d=0, s=1, p=1, sh=1)
            if ls_str<1:
                print 'item has no input'
            dn_str=cmds.listConnections( n_str[0], s=0, d=1, p=1, sh=1)
            if dn_str<1:
                print 'item has no output'
            if bH_i<0:
                for u in range (len(ls_str)):
                    cmds.textScrollList(urp, e=1, a=ls_str[u], w=150, h=330)
            if bH_i>0:
                for u in range (len(ls_str)):
                    if ls_str[u] in bH_i:
                        cmds.textScrollList(urp, e=1, da=1, w=150, h=330)
                        print '%s'%ls_str[u]+' already in list'
                        cmds.textScrollList(urp, e=1, si=ls_str[u], w=150, h=330)
                    else:
                        cmds.textScrollList(urp, e=1, a=ls_str[u], w=150, h=330)
            if bH_d<0:
                for u in range (len(dn_str)):
                    cmds.textScrollList(drown, e=1, a=dn_str[u], w=150, h=330)
            if bH_d>0:
                for u in range (len(dn_str)):
                    if dn_str[u] in bH_d:
                        cmds.textScrollList(drown, e=1, da=1, w=150, h=330)
                        print '%s'%dn_str[u]+' already in list'
                        cmds.textScrollList(drown, e=1, si=dn_str[u], w=150, h=330)
                    else:
                        cmds.textScrollList(drown, e=1, a=dn_str[u], w=150, h=330)
    
    def srt(self, arg=None):
        bH_i=cmds.textScrollList(ndeLst, q=1, ai=1)
        hg=sorted(bH_i, key=lower)
        cmds.textScrollList(ndeLst, e=1, ra=1, w=150, h=220)
        cmds.textScrollList(ndeLst, e=1, append=hg[0::1], w=150, h=220)
    
    def pls(self, arg=None):
        bH_i=cmds.textScrollList(ndeLst, q=1, ai=1)
        poBL = cmds.ls (sl=1)
        pObj=[]
        crap=[]
        pObjd=[]
        Cln=poBL
        dets=['.e[', '.f[', '.vtx[', '.map[', '.vtxFace[']
        for r in range (len(dets)):
            for j in range(len(poBL)):
                for h in range(len(Cln)):
                    if dets[r] in poBL[j]:
                        pObjd.append(poBL[j])
                        Cln.remove(poBL[j])
        if len(Cln)>0:
            if Cln>1:
                rg=sorted(Cln, key=lower)
            if len(Cln) ==1:
                rg=Cln
            if bH_i<0:
                for u in range (len(rg)):
                    cmds.textScrollList(ndeLst, e=1, a=rg[u], w=150, h=220)
            if bH_i>0:
                for u in range (len(rg)):
                    if rg[u] in bH_i:
                        cmds.textScrollList(ndeLst, e=1, da=1, w=150, h=220)
                        print '%s'%rg[u]+' already in list'
                        cmds.textScrollList(ndeLst, e=1, si=rg[u], w=150, h=220)
                    else:
                        cmds.textScrollList(ndeLst, e=1, a=rg[u], w=150, h=220)
        if pObjd>0:
            for h in range (len(pObjd)):
                f=pObjd[h].split('.')
                j=f[1].split('[')
                str= j[1][:-1]
                if ':' not in (str):
                    pObj.append(pObjd[h])
                else:
                    crap.append(str)
                for p in range (len(crap)):
                    g=crap[p].split(':')
                    t=int(g[0])
                    v=int(g[1])
                    nmbr=range (t, v)
                    nmbr.append(v)
                    for k in range(len(nmbr)):
                        kol=f[0]+'.%s'%j[0]+'[%d' %nmbr[k]+']'
                        pObj.append(kol)
                        d = {}
                    for x in pObj:
                        d[x] = 1
                    pObj = list(d.keys())
            if len(pObj)>0:
                if pObjd>1:
                    hg=sorted(pObj, key=lower)
                if len(pObj) ==1:
                    hg=pObj
                if bH_i<0:
                    for u in range (len(hg)):
                        cmds.textScrollList(ndeLst, e=1, a=hg[u], w=150, h=220)
                if bH_i>0:
                    for u in range (len(hg)):
                        if hg[u] in bH_i:
                            cmds.textScrollList(ndeLst, e=1, da=1, w=150, h=220)
                            print '%s'%hg[u]+' already in list'
                            cmds.textScrollList(ndeLst, e=1, si=hg[u], w=150, h=220)
                        else:
                            cmds.textScrollList(ndeLst, e=1, a=hg[u], w=150, h=220)
    
    def focsSel(self, arg=None):##################focus on selected in scene
        n_str=cmds.ls(sl=1)
        undg=len(n_str)
        if undg<1:
            print 'select something'
        else:
            ls_str=cmds.listConnections( n_str[0], d=0, s=1, p=1, sh=1)
            if ls_str<1:
                cmds.textScrollList(urp, e=1, ra=1, w=150, h=330)
            else:
                cmds.textScrollList(urp, e=1, ra=1, w=150, h=330)
                cmds.textScrollList(urp, e=1, append=ls_str[0::1], w=150, h=330)
            dn_str=cmds.listConnections( n_str[0], s=0, d=1, p=1, sh=1)
            if dn_str<1:
                cmds.textScrollList(drown, e=1, ra=1, w=150, h=330)
            else:
                cmds.textScrollList(drown, e=1, ra=1, w=150, h=330)
                cmds.textScrollList(drown, e=1, append=dn_str[0::1], w=150, h=330)
            print n_str[0]
            cmds.text(joe, e=1, label='%s'%n_str[0], rs=0)
    
    def sall(self, arg=None):
        bH_i=cmds.textScrollList(ndeLst, q=1, ai=1)
        cmds.textScrollList(ndeLst, e=1, si=bH_i, w=150, h=220)
    
    def snon(self, arg=None):
        cmds.textScrollList(ndeLst, e=1, da=1, w=150, h=220)
    
    def mns(self, arg=None):
        shrt=cmds.textScrollList(ndeLst, q=1, selectItem=1)
        if shrt<1:
            print 'select item to subtract from list'
        else:
            cmds.textScrollList(ndeLst, e=1, ri=shrt, w=150, h=220)
    
    def swp(self, arg=None):
        shrt=cmds.textScrollList(ndeLst, q=1, selectItem=1)
        bH_i=cmds.textScrollList(ndeLst, q=1, ai=1)
        n_str=cmds.ls(sl=1)
        if n_str<1:
            print 'select list item first and then object to swap with'
        else:
            if n_str[0] in bH_i:
                cmds.textScrollList(ndeLst, e=1, si=n_str, w=150, h=220)
                print '%s'%n_str+' already in list'
            else:
                cmds.textScrollList(ndeLst, e=1, ri=shrt,  w=150, h=220)
                cmds.textScrollList(ndeLst, e=1, a=n_str[0::1],  w=150, h=220)
    
    def inL(self, arg=None):    #################
        o_str=cmds.text(add_in, q=1, label=1)
        if o_str<1:
            print 'no insert has been identified'
        else:
            cmds.select(o_str, r=1)
            maya.mel.eval( "connectWindowFillFromActiveList 0;" )
    
    def otR(self, arg=None):    #################
        o_str=cmds.text(add_in, q=1, label=1)
        if o_str<1:
            print 'no insert has been identified'
        else:
            cmds.select(o_str, r=1)
            maya.mel.eval( "connectWindowFillFromActiveList 1;" )
    
    
    def insertsel(self, arg=None):
        n_str=cmds.ls(sl=1)
        job=len(n_str)
        if job==1:
            cmds.text(add_in, e=1, label='%s'%n_str[0])
            print 'you have selected:'+'%s'%n_str[0]+' to insert. Check that it has input/output attributes.'
    
    def Issel(self, arg=None):
        n_str=cmds.ls(sl=1)
        job=len(n_str)
        if job==1:
            cmds.text(joe, e=1, label='%s'%n_str[0], rs=0)
        else:
            cmds.text(joe, e=1, label='nothing selected', rs=0)
    
    def cw(self, arg=None):#################
        maya.mel.eval( "connectWindow;" )
    
    
    def cwlL(self, arg=None):    #################
        klo=cmds.text(joe, q=1, label=1)
        cmds.select(klo, r=1)
        maya.mel.eval( "connectWindowFillFromActiveList 0;" )
    
    
    def cwlR(self, arg=None):
        klo=cmds.text(joe, q=1, label=1)
        cmds.select(klo, r=1)
        maya.mel.eval( "connectWindowFillFromActiveList 1;" )
    
    def upL(self, arg=None):    #################
        o_str=cmds.textScrollList(urp, q=1, selectItem=1)
        if o_str<1:
            print 'select from the upstream scroll-list to assign in the left connection editor window'
        else:
            p_str=o_str[0].split('.')
            cmds.select(p_str[0], r=1)
            maya.mel.eval( "connectWindowFillFromActiveList 0;" )
    
    def upR(self, arg=None):    #################
        o_str=cmds.textScrollList(urp, q=1, selectItem=1)
        if o_str<1:
            print 'select from the upstream scroll-list to assign in the right connection editor window'
        else:
            p_str=o_str[0].split('.')
            cmds.select(p_str[0], r=1)
            maya.mel.eval( "connectWindowFillFromActiveList 1;" )
    
    def dnL(self, arg=None):    #################
        o_str=cmds.textScrollList(drown, q=1, selectItem=1)
        if o_str<1:
            print 'select from the downstream scroll-list to assign in the left connection editor window'
        else:
            p_str=o_str[0].split('.')
            cmds.select(p_str[0], r=1)
            maya.mel.eval( "connectWindowFillFromActiveList 0;" )
    
    def dnR(self, arg=None):    #################
        o_str=cmds.textScrollList(drown, q=1, selectItem=1)
        if o_str<1:
            print 'select from the downstream scroll-list to assign in the right connection editor window'
        else:
            p_str=o_str[0].split('.')
            cmds.select(p_str[0], r=1)
            maya.mel.eval( "connectWindowFillFromActiveList 1;" )
    
    def chan(self, arg=None):    #################
        maya.mel.eval( "ChannelControlEditor;;" )
    
    def ea(self, arg=None):    #################
        maya.mel.eval( "RenameAttribute;" )
    
    def ada(self, arg=None):    #################
        maya.mel.eval( "AddAttribute;" )
    
    def hsw(self, arg=None):    #################
        maya.mel.eval( "HypershadeWindow;" )
    
    def scrpted(self, arg=None):    #################
        maya.mel.eval( "ScriptEditor;" )
    
    def sdk(self, arg=None):    #################
        maya.mel.eval( "SetDrivenKeyOptions;" )
    
    def olw(self, arg=None):    #################
        maya.mel.eval( "OutlinerWindow;" )
    
    def clr(self, arg=None):##################
        cmds.textScrollList(ndeLst, e=1, ra=1, w=150, h=220)
    
    
    def upstr(self, arg=None):##################<<upstream select
        n_str=cmds.ls(sl=1)[0]
        en_str=[]
        ls_str=cmds.listConnections( n_str, s=1, d=1, p=1, sh=1, scn=1)
        for r in range(len(ls_str)):
            for i in range(len(outmeshs)):
                if outmeshs[i] in ls_str[r]:
                    en_str.append(ls_str[r])
        fs_nm=en_str[0].split('.')
        cmds.select(fs_nm[0], r=1)
        cmds.text(joe, e=1, label='%s'%fs_nm[0], rs=0)
        shrt=cmds.ls(sl=1)
        if shrt > 0:
            cmds.select(shrt, r=1)
            cmds.text(joe, e=1, label='%s'%shrt[0], rs=0)
            ls_str=cmds.listConnections( shrt[0], s=1, d=0, p=1, sh=1)
            if ls_str<1:
                cmds.textScrollList(urp, e=1, ra=1, w=150, h=330)
            else:
                cmds.textScrollList(urp, e=1, ra=1, w=150, h=330)
                cmds.textScrollList(urp, e=1, append=ls_str[0::1], w=150, h=330)
            ds_str=cmds.listConnections( shrt[0], s=0, d=1, p=1, sh=1)
            if ds_str<1:
                cmds.textScrollList(drown, e=1, ra=1, w=150, h=330)
            else:
                cmds.textScrollList(drown, e=1, ra=1, w=150, h=330)
                cmds.textScrollList(drown, e=1, append=ds_str[0::1], w=150, h=330)
    
    def dnstr(self, arg=None):##################>>downstream select
        n_str=cmds.ls(sl=1)[0]
        en_str=[]
        ls_str=cmds.listConnections( n_str, d=1, s=0, p=1, sh=1, scn=1)
        for r in range(len(ls_str)):
            for i in range(len(inmeshs)):
                if inmeshs[i] in ls_str[r]:
                    en_str.append(ls_str[r])
        fs_nm=en_str[0].split('.')
        cmds.select(fs_nm[0], r=1)
        cmds.text(joe, e=1, label='%s'%fs_nm[0], rs=0)
        shrt=cmds.ls(sl=1)
        if shrt > 0:
            cmds.select(shrt, r=1)
            cmds.text(joe, e=1, label='%s'%shrt[0], rs=0)
            ls_str=cmds.listConnections( shrt[0], s=1, d=0, p=1, sh=1)
            if ls_str<1:
                cmds.textScrollList(urp, e=1, ra=1, w=150, h=330)
            else:
                cmds.textScrollList(urp, e=1, ra=1, w=150, h=330)
                cmds.textScrollList(urp, e=1, append=ls_str[0::1], w=150, h=330)
            ds_str=cmds.listConnections( shrt[0], s=0, d=1, p=1, sh=1)
            if ds_str<1:
                cmds.textScrollList(drown, e=1, ra=1, w=150, h=330)
            else:
                cmds.textScrollList(drown, e=1, ra=1, w=150, h=330)
                cmds.textScrollList(drown, e=1, append=ds_str[0::1], w=150, h=330)
    
    def fndNd(self, arg=None):###################find node type
        klo=cmds.ls(sl=1)
        huy=len(klo)
        if huy < 1:
            print "nothing selected"
        else:
            if huy > 1:
                filter= cmds.nodeType(klo[0])
                cmds.textField(nd_name, e=1, text=filter)
            if huy == 1:
                filter= cmds.nodeType(klo)
                cmds.textField(nd_name, e=1, text=filter)
    
    
    def findName(self, arg=None):###################find name
        klo=cmds.ls(sl=1)
        huy=len(klo)
        if huy < 1:
            print "nothing selected"
        else:
            if huy >= 1:
                cmds.textField(nd_name, e=1, text=klo[0])
    
    def selNd(self, arg=None):###################Select nodetype in selection array
        klo=cmds.ls(sl=1)
        ft_List=[]
        who=cmds.textField(nd_name, q=True, text=True)
        for i in range (len(klo)):
            filter= cmds.nodeType(klo[i])
            if who in filter:
                ft_List.append(klo[i])
                cmds.select(ft_List, r=1)
                cmds.textScrollList(ndeLst, e=1, ra=1, w=150, h=220 )
                cmds.textScrollList(ndeLst, e=1, append=ft_List[0::1], w=150, h=220 )
    
    def selname(self, arg=None):###################Select nodetype in selection array
        klo=cmds.ls(sl=1)
        ft_List=[]
        who=cmds.textField(nd_name, q=True, text=True)
        for i in range (len(klo)):
            if who in klo[i]:
                ft_List.append(klo[i])
                cmds.select(ft_List, r=1)
                cmds.textScrollList(ndeLst, e=1, ra=1, w=150, h=220)
                cmds.textScrollList(ndeLst, e=1, append=ft_List[0::1], w=150, h=220)
    
    
#     def selAl(self, arg=None):###################select all node type in scene
#         who=cmds.textField(nd_name, q=True, text=True)
#         if who<1:
#             print 'nothing selected'
#             cmds.frameLayout(IL_0p, e=1, label="nothing selected" )
#             cmds.textScrollList(ndeLst, e=1, ra=1, w=150, h=220)
#         jack=cmds.ls(type=who)
#         hgt=[]
#         dng=['transform', 'mesh', 'joint', 'shape', 'nurbsCurve', 'shape']
#         for r in range(len(jack)):
#             for i in range (len(dng)):
#                 if dng[i] in jack[r]:
#                     hgt.append(jack[r])
#         if (len(hgt))>0:
#             print "This is too common and will likely lock up your scene! Try filtering from a selection"
#             cmds.frameLayout(IL_0p, e=1, label="This is too common and will likely lock up your scene! Try filtering from a selection" )
#             cmds.textScrollList(ndeLst, e=1, ra=1, w=150, h=220)
#         else:
#             cmds.select(jack[r], r=1)
#             cmds.textScrollList(ndeLst, e=1, ra=1, w=150, h=220)
#             cmds.textScrollList(ndeLst, e=1, append=jack[0::1], w=150, h=220)
    
    def selAlname(self, arg=None):###################select all node type in scene
        who=cmds.textField(nd_name, q=True, text=True)
        if who<1:
            print 'nothing selected'
            cmds.textScrollList(ndeLst, e=1, ra=1, w=150, h=220)
        else:
            cmds.select(who, r=1)
            jack=cmds.ls(sl=1)
            cmds.textScrollList(ndeLst, e=1, ra=1, w=150, h=220)
            cmds.textScrollList(ndeLst, e=1, append=jack[0::1], w=150, h=220)
    
    def hg(self, arg=None):##################open hypergraph
        maya.mel.eval( "HypergraphHierarchyWindow;" )
    
    def hgu(self, arg=None):##################update hypergraph to selected
        maya.mel.eval(' showDGLevel hyperGraphPanel2HyperGraphEd; ')
        maya.mel.eval(' FrameSelected; ')
    #    maya.mel.eval(' fitPanel -selected;')
    
    def link (self, arg=None):#################relinker
        o_str=cmds.textScrollList(urp, q=1, selectItem=1)
        d_str=cmds.textScrollList(drown, q=1, selectItem=1)
        cmds.connectAttr(o_str[0], d_str[0], f=1)
    
    def nodesel (self, arg=None):###################list node type scene selection
        n_wgh=cmds.ls(sl=1)
        if n_wgh<1:
            print 'nothing selected'
            cmds.textScrollList(ndeLst, e=1, ra=1, w=150, h=220)
        else:
            cmds.textScrollList(ndeLst, e=1, ra=1, w=150, h=220)
            cmds.textScrollList(ndeLst, e=1, append=n_wgh[0::1], w=150, h=220)
    
    def selNod(self, arg=None):#################list node type scene selection
        shrt=cmds.textScrollList(ndeLst, q=1, selectItem=1)
        cmds.select(shrt, r=1)
        print shrt[0]
    
    def ctlct(self, arg=None):###################create locator
        batman = cmds.ls(sl=True)
        for i in range (len(batman)):
            jack=cmds.spaceLocator()
            scalefrog=cmds.xform(batman[i], q=True, s=True, r=True)
            cmds.scale(scalefrog[0], scalefrog[1], scalefrog[2], jack, r=True)
            movefrog=cmds.xform(batman[i], q=True, t=True, ws=True)
            cmds.move(movefrog[0], movefrog[1], movefrog[2], jack, ws=True)
            rotatefrog=cmds.xform(batman[i], q=True, ro=True, ws=True)
            cmds.rotate(rotatefrog[0], rotatefrog[1], rotatefrog[2], jack, ws=True)
            if ':' in batman[i]:
                hg=batman[i].split(':')
                jk=hg[2:]
                helga=hg[:1]
                hr=helga[0]+'_'+jk[0]
                cmds.rename(jack, '%s' %hr + '_ploc')
            else:
                cmds.rename(jack, batman[i]+'_ploc')
    
    def adatt(self, arg=None):#################Quick add float
        who=cmds.textField(ctAt_name, q=True, text=True)
        npl=cmds.ls(sl=1)
        cmds.addAttr(npl, ln=who, at="double", min=0, max=1, dv=0)
        cmds.setAttr(npl[0]+"."+who, k=1)
    
    
    def hdtrn(self, arg=None):#################lock and hide toggle on transform attribute
        ijop=[".rx", ".ry", ".rz", ".sx", ".sy", ".sz", ".tx", ".ty", ".tz"]
        npl=cmds.ls(sl=1)[0]
        for i in range (len(ijop)):
            getTatt=cmds.getAttr(npl+ijop[i], k=1)
            if getTatt==1:
                cmds.setAttr(npl+ijop[i], k=0)
            else:
                cmds.setAttr(npl+ijop[i], k=1)
            getLatt=cmds.getAttr(npl+ijop[i], l=1)
            if getLatt==0:
                cmds.setAttr(npl+ijop[i], l=1)
            else:
                cmds.setAttr(npl+ijop[i], l=0)
    
    
    def clnint(self, arg=None):
        cmds.DisplayWireframe()
        windows = cmds.lsUI(wnd=1)
        nt_win=['CommandWindow', 'MayaWindow', 'scriptEditorPanel1Window', 'swimtWindow', 'shelfEditorWin', 'ColorEditor' ]
        for i in range(len(nt_win)):
            if nt_win[i] in windows:
                windows.remove(nt_win[i])
        cmds.deleteUI(windows, window=1)
    
    
    def foc_in(self, arg=None):
        shep=cmds.text(add_in, q=1, label=1)
        cmds.select('%s'%shep, r=1)
        n_str=cmds.ls(sl=1)
        ls_str=cmds.listConnections( n_str, d=0, s=1, p=1, sh=1)
        if ls_str<1:
            cmds.textScrollList(urp, e=1, ra=1, w=150, h=330)
        else:
            cmds.textScrollList(urp, e=1, ra=1, w=150, h=330)
            cmds.textScrollList(urp, e=1, append=ls_str[0::1], w=150, h=330)
        dn_str=cmds.listConnections( n_str[0], s=0, d=1, p=1, sh=1)
        if dn_str<1:
            cmds.textScrollList(drown, e=1, ra=1, w=150, h=330)
        else:
            cmds.textScrollList(drown, e=1, ra=1, w=150, h=330)
            cmds.textScrollList(drown, e=1, append=dn_str[0::1], w=150, h=330)
        print n_str[0]
        cmds.text(joe, e=1, label='%s'%n_str[0], rs=0)
    
    def re_foc(self, arg=None):
        rf=cmds.text(joe, q=1, label=1)
        cmds.select('%s'%rf, r=1)
        n_str=cmds.ls(sl=1)
        ls_str=cmds.listConnections( n_str, d=0, s=1, p=1, sh=1)
        if ls_str<1:
            cmds.textScrollList(urp, e=1, ra=1, w=150, h=330)
        else:
            cmds.textScrollList(urp, e=1, ra=1, w=150, h=330)
            cmds.textScrollList(urp, e=1, append=ls_str[0::1], w=150, h=330)
        dn_str=cmds.listConnections( n_str[0], s=0, d=1, p=1, sh=1)
        if dn_str<1:
            cmds.textScrollList(drown, e=1, ra=1, w=150, h=330)
        else:
            cmds.textScrollList(drown, e=1, ra=1, w=150, h=330)
            cmds.textScrollList(drown, e=1, append=dn_str[0::1], w=150, h=330)
        print n_str[0]
        cmds.text(joe, e=1, label='%s'%n_str[0], rs=0)
    
    
    
    def strselup(self, arg=None):###################text scroll list upstream functions
        o_str=cmds.textScrollList(urp, q=1, selectItem=1)
        p_str=o_str[0].split('.')
        cmds.select(p_str[0], r=1)
        ls_str=cmds.listConnections( p_str[0], s=1, d=0, p=1, sh=1)
        if ls_str<1:
            cmds.textScrollList(urp, e=1, ra=1, w=150, h=330)
        else:
            cmds.textScrollList(urp, e=1, ra=1, w=150, h=330)
            cmds.textScrollList(urp, e=1, append=ls_str[0::1], w=150, h=330)
        dn_str=cmds.listConnections( p_str[0], s=0, d=1, p=1, sh=1)
        if dn_str<1:
            cmds.textScrollList(drown, e=1, ra=1, w=150, h=330)
        else:
            cmds.textScrollList(drown, e=1, ra=1, w=150, h=330)
            cmds.textScrollList(drown, e=1, append=dn_str[0::1], w=150, h=330)
        cmds.text(joe, e=1, label='%s'%p_str[0], rs=0)
    
    def strseldn(self, arg=None):###################text scroll list downstream functions
        sm_str=cmds.textScrollList(drown, q=1, selectItem=1)
        sp_str=sm_str[0].split('.')
        cmds.select(sp_str[0], r=1)
        ls_str=cmds.listConnections( sp_str[0], s=1, d=0, p=1, sh=1)
        if ls_str<1:
            cmds.textScrollList(urp, e=1, ra=1, w=150, h=330)
        else:
            cmds.textScrollList(urp, e=1, ra=1, w=150, h=330)
            cmds.textScrollList(urp, e=1, append=ls_str[0::1], w=150, h=330)
        dn_str=cmds.listConnections( sp_str[0], d=1, s=0, sh=1, p=1)
        if dn_str<1:
            cmds.textScrollList(drown, e=1, ra=1, w=150, h=330)
        else:
            cmds.textScrollList(drown, e=1, ra=1, w=150, h=330)
            cmds.textScrollList(drown, e=1, append=dn_str[0::1], w=150, h=330)
        print sp_str[0]
        cmds.text(joe, e=1, label='%s'%sp_str[0], rs=0)
    
    def nodesel2(self, arg=None):
        shrt=cmds.textScrollList(ndeLst, q=1, selectItem=1)
        if shrt > 0:
            cmds.select(shrt, r=1)
            cmds.text(joe, e=1, label='%s'%shrt[0], rs=0)
            ls_str=cmds.listConnections( shrt[0], s=1, d=0, p=1, sh=1)
            if ls_str<1:
                cmds.textScrollList(urp, e=1, ra=1, w=150, h=330)
            else:
                cmds.textScrollList(urp, e=1, ra=1, w=150, h=330)
                cmds.textScrollList(urp, e=1, append=ls_str[0::1], w=150, h=330)
            ds_str=cmds.listConnections( shrt[0], s=0, d=1, p=1, sh=1)
            if ds_str<1:
                cmds.textScrollList(drown, e=1, ra=1, w=150, h=330)
            else:
                cmds.textScrollList(drown, e=1, ra=1, w=150, h=330)
                cmds.textScrollList(drown, e=1, append=ds_str[0::1], w=150, h=330)
    def bypss (self, arg=None):
        n_str=cmds.text(joe, q=1)
        b_str=cmds.ls(sl=1)
        o_str=cmds.textScrollList(urp, q=1, selectItem=1)
        if o_str>1:
            up_des=cmds.connectionInfo(o_str, dfs=1)
        d_str=cmds.textScrollList(drown, q=1, selectItem=1)
        if d_str>1:
            drn_src=cmds.connectionInfo(d_str, sfd=1)
            drn_des=cmds.connectionInfo(drn_src, dfs=1)
        cmds.connectAttr(o_str[0], d_str[0], f=1)
        cmds.disconnectAttr(o_str[0], up_des[0])
        print o_str[0]+', '+ d_str[0]+' has been connected'
        print o_str[0]+', '+ up_des[0]+' has been disconnected'
    
    def chN_in (self, arg=None):#### build a choice node going in
        n_str=cmds.text(joe, q=1, label=1)
        o_str=cmds.textScrollList(urp, q=1, selectItem=1)
        if o_str<1:
            print 'you need to select from the up stream scroll list for insert choice'
        else:
            up_des=cmds.connectionInfo(o_str, dfs=1)
            str_updes=up_des[0]
            gh_o=str_updes.split('.')
            IP_g=gh_o[1:]
            Ct_g=[]
            for i in range(len(IP_g)):
                gr_u='.'+IP_g[i]
                Ct_g.append(gr_u)
                Al_Lst=Ct_g[1:]
                Al_Lnk=gh_o[1:2]+Al_Lst
                myString="".join(Al_Lnk)
            upchoice=cmds.choice(n_str, at='%s'%myString)
            print 'you have inserted a choice node at: '+ '%s'%o_str[0]+', %s'%n_str[0]+'.'+'%s'%myString
    
    def chN_ot (self, arg=None):##build a choice node going out
        n_str=cmds.text(joe, q=1, label=1)
        o_str=cmds.textScrollList(urp, q=1, selectItem=1)
        if o_str>1:
            up_des=cmds.connectionInfo(o_str, dfs=1)
        d_str=cmds.textScrollList(drown, q=1, selectItem=1)
        drn_src=cmds.connectionInfo(d_str, sfd=1)
        drn_des=cmds.connectionInfo(drn_src, dfs=1)
        str_dndes=drn_des[0]
        gh_lo=str_dndes.split('.')
        IP_g=gh_lo[1:]
        Ct_g=[]
        for i in range(len(IP_g)):
            gr_u='.'+IP_g[i]
            Ct_g.append(gr_u)
            Al_Lst=Ct_g[1:]
            Al_Lnk=gh_lo[1:2]+Al_Lst
            myString="".join(Al_Lnk)
        downchoice=cmds.choice(d_str, at='%s'%myString)
        print 'you have inserted a choice node at: '+ '%s'%drn_src+', %s'%d_str
    
    def upstreamInsert (self, arg=None):
        win=cmds.text(add_in, q=1, label=1)##insert
        glogged=cmds.attributeInfo(win, all=1)##insert info
        o_str=cmds.textScrollList(urp, q=1, selectItem=1)##source
        stich=[]
        sew=[]
        if o_str>0:
            up_des=cmds.connectionInfo(o_str, dfs=1)##destination info
        else:
            print "select source from upstream scroll-list"
        for i in range(len(outmeshs)):
            for r in range(len(glogged)):
                if outmeshs[i] in glogged[r]:
                    stich.append(outmeshs[i])
        for i in range(len(inmeshs)):
            for r in range(len(glogged)):
                if inmeshs[i] in glogged[r]:
                    sew.append(inmeshs[i])
        dn_str=cmds.listConnections( win, s=1, d=0, p=1, sh=1)
        cmds.connectAttr( '%s'%win+'.%s'%stich[0], '%s'%up_des[0], f=1)
        print '%s'%win+'.%s'%stich[0]+', '+'%s'%up_des[0] + ' has been connected'
        cmds.connectAttr( '%s'%o_str[0], '%s'%win+'.%s'%sew[0], f=1)
        print '%s'%o_str[0]+', '+'%s'%win+'.%s'%sew[0] + ' has been connected'
    
    def downstreamInsert (self, arg=None):
        win=cmds.text(add_in, q=1, label=1)##insert
        glogged=cmds.attributeInfo(win, all=1)##insert info
        o_str=cmds.textScrollList(drown, q=1, selectItem=1)##source
        stich=[]
        sew=[]
        if o_str<0:
            print "select source from upstream scroll-list"
        else:
            dn_des=cmds.connectionInfo(o_str, sfd=1)##destination info
            for i in range(len(inmeshs)):
                for r in range(len(glogged)):
                    if inmeshs[i] in glogged[r]:
                        sew.append(inmeshs[i])
            for i in range(len(outmeshs)):
                for r in range(len(glogged)):
                    if outmeshs[i] in glogged[r]:
                        stich.append(outmeshs[i])
            dn_str=cmds.listConnections( win, s=0, d=1, p=1, sh=1)
            oit= '%s'%win+'.'+'%s'%stich[0]
            iit='%s'%win+'.'+'%s'%sew[0]
            spaz=cmds.text(joe, q=1, label=1)#focus
            dop_str=cmds.listConnections( spaz, s=1, d=0, p=1, sh=1)
            dip_str=cmds.listConnections( win, s=0, d=1, p=1, sh=1)
            if dop_str>0:
                if oit==dop_str[0]:
                    cmds.disconnectAttr(dop_str[0], dip_str[0])
            frip_str=cmds.listConnections( win, s=1, d=0, p=1, sh=1)
            if frip_str>0:
                fip_str=frip_str[0].split('.')
                fop_str=cmds.listConnections( fip_str[0], s=0, d=1, p=1, sh=1)
                if iit==fop_str[0]:
                    cmds.disconnectAttr(frip_str[0], fop_str[0])
                    cmds.connectAttr(frip_str[0], dip_str[0], f=1)
                    print '%s'%frip_str[0]+', %s'%dip_str[0]+' has been connected'
            cmds.connectAttr( '%s'%dn_des, '%s'%win+'.%s'%sew[0], f=1)
            print'%s'%dn_des+', '+'%s'%win+'.%s'%sew[0] + ' has been connected'
            cmds.connectAttr( '%s'%win+'.%s'%stich[0], '%s'%o_str[0], f=1)
            print '%s'%win+'.%s'%stich[0]+', '+'%s'%o_str[0] + ' has been connected'
    
    def upstrcon (self, arg=None):
        win=cmds.ls(sl=1)[0]##insert
        if win==0:
            print 'select something to connect'
        glogged=cmds.attributeInfo(win, all=1)##insert info
        o_str=cmds.text(joe, q=1, label=1)#focus
        dn_str=cmds.listConnections( win, s=1, d=0, p=1, sh=1)
        plogged=cmds.attributeInfo(o_str, all=1)##insert info
        stich=[]
        sew=[]
        for g in range(len(inmeshs)):
            if inmeshs[g] in plogged:
                sew.append(inmeshs[g])
        for i in range(len(outmeshs)):
            if outmeshs[i] in glogged:
                stich.append(outmeshs[i])
        if dn_str>0:
            joined='%s'%o_str+'.'+'%s'%stich[0]
            joiner='%s'%win+'.'+'%s'%sew[0]
            if joined==dn_str[0]:
                print '%s'%joined +' is already connected to %s'%joiner+ '. Cannot make cycle in this fashion.'
        else:
            cmds.connectAttr( '%s'%win+'.%s'%stich[0], '%s'%o_str+'.%s'%sew[0], f=1)
            print '%s'%win+'.%s'%stich[0]+', %s'%o_str+ '.%s' %sew[0] + ' has been connected'
    
    def dnstrcon (self, arg=None):
        o_str=cmds.ls(sl=1)##insert
        if o_str==0:
            print 'select something to connect'
        win=cmds.text(joe, q=1, label=1)#focus
        glogged=cmds.attributeInfo(win, all=1)##insert info
        plogged=cmds.attributeInfo(o_str, all=1)##insert info
        dn_str=cmds.listConnections( o_str, s=0, d=1, p=1, sh=1)
        stich=[]
        sew=[]
        for g in range(len(inmeshs)):
            if inmeshs[g] in plogged:
                sew.append(inmeshs[g])
        for i in range(len(outmeshs)):
            if outmeshs[i] in glogged:
                stich.append(outmeshs[i])
        if dn_str>0:
            joined='%s'%win+'.'+'%s'%sew[0]
            joiner='%s'%o_str[0]+'.'+'%s'%stich[0]
            if joined==dn_str[0]:
                print '%s'%joined +' is already connected to %s'%joiner+ '. Cannot make cycle in this fashion.'
            else:
                for h in range(len(o_str)):
                    cmds.connectAttr( '%s'%win+'.%s'%stich[0], '%s'%o_str[h]+'.%s'%sew[0], f=1)
                    print '%s'%win+'.%s'%stich[0]+', %s'%o_str+ '.%s' %sew[0] + ' has been connected'
    
    def unlckin (self, arg=None):
        klo=cmds.text(joe, q=1, label=1)
        dw=cmds.textScrollList(urp, q=1, selectItem=1)
        if dw<1:
            print "you must make a selection in the 'up-stream' scroll-list to unlock from"
        else:
            dn_des=cmds.connectionInfo(dw, dfs=1)
            hint=[]
            for o in range(len(klo)):
                for i in range(len(dn_des)):
                    if klo[o] in dn_des[i]:
                        hint.append(dn_des[i])
                        for p in range(len(hint)):
                            cmds.setAttr(hint[p], l=0)##this is necessary to only unlock the focus input instead of all connected
            print '%s'%hint[0]+"attribute has been unlocked"
    
    def lckin (self, arg=None):
        klo=cmds.text(joe, q=1, label=1)
        dw=cmds.textScrollList(urp, q=1, selectItem=1)
        if dw<1:
            print "you must make a selection in the 'up-stream' scroll-list to lock from"
        else:
            dn_des=cmds.connectionInfo(dw, dfs=1)
            hint=[]
            for o in range(len(klo)):
                for i in range(len(dn_des)):
                    if klo[o] in dn_des[i]:
                        hint.append(dn_des[i])
                        for p in range(len(hint)):
                            cmds.setAttr(hint[p], l=1)
            print '%s'%hint[0]+ " has been locked"
    
    def strnup(self, arg=None):###################select upstream function
        jri=cmds.textScrollList(urp, q=1, selectItem=1)
        yru=cmds.connectionInfo(jri[0], dfs=1)
        klo=cmds.text(joe, q=1, label=1)
        dw=cmds.textScrollList(urp, q=1, selectItem=1)
        hint=[]
        dn_des=cmds.connectionInfo(dw, dfs=1)
        ilo=cmds.connectionInfo( dn_des[0], gla=1)
        if len(ilo)>0:
            print 'CONNECTION:: %s'%jri[0]+', '+'%s'%yru[0]+'    ||     '+ ilo +' is a locked attribute'
        else:
            print 'CONNECTION:: %s'%jri[0]+', '+'%s'%yru[0]+'    ||     '+'%s'%yru[0] + ' attribute is open'
        eff=jri[0].split('.')
        cmds.select(eff[0], r=1)
    
    def strnupOFF(self, arg=None):###################select upstream function
        jri=cmds.textScrollList(urp, q=1, selectItem=1)
        yru=cmds.connectionInfo(jri[0], dfs=1)
        klo=cmds.text(joe, q=1, label=1)
        dw=cmds.textScrollList(urp, q=1, selectItem=1)
        hint=[]
        dn_des=cmds.connectionInfo(dw, dfs=1)
        ilo=cmds.connectionInfo( dn_des[0], gla=1)
        if len(ilo)>0:
            print 'CONNECTION:: %s'%jri[0]+', '+'%s'%yru[0]+'    ||     '+ ilo +' is a locked attribute'
        else:
            print 'CONNECTION:: %s'%jri[0]+', '+'%s'%yru[0]+'    ||     '+'%s'%yru[0] + ' attribute is open'
    
    
    
    def strng(self, arg=None):##################select downstream function
        jri=cmds.textScrollList(drown, q=1, selectItem=1)
        yru=cmds.connectionInfo(jri[0], sfd=1)
        if jri > 0:
                if yru > 0:
                    print 'CONNECTION:: %s'%yru + ', '+'%s'%jri[0]
        eff=jri[0].split('.')
        cmds.select(eff[0], r=1)
    
    def strngOFF(self, arg=None):##################select downstream function
        jri=cmds.textScrollList(drown, q=1, selectItem=1)
        yru=cmds.connectionInfo(jri[0], sfd=1)
        if jri > 0:
                if yru > 0:
                    print 'CONNECTION:: %s'%yru + ', '+'%s'%jri[0]
                    
                    

inst = ui()
inst.create()
                    