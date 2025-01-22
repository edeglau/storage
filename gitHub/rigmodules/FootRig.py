import sys, os
filepath= os.getcwd()
sys.path.append(str(filepath))
import baseFunctions_maya
reload (baseFunctions_maya)
getClass=baseFunctions_maya.BaseClass()

'''MG rigging modules'''
__author__ = "Elise Deglau"
__version__ = 1.00
'This work is licensed under a Creative Commons License'
'http://creativecommons.org/licenses/by-sa/3.0/au/'

import maya.cmds as cmds
import maya.mel

#JOINTS
class FootRig(object):
    def __init__(self):
        cmds.select(cl=1) 
        getGuide=cmds.ls("*_guide")    
        getGuide.remove("footheelLeft_guide")  
        legRightFull=(             
                  "legkneeRight_guide", 
                  "footankleRight_guide", 
                  "footballRight_guide", 
                  "foottoeRight_guide")
        legRight=(
                  "footankleRight_guide", 
                  "footballRight_guide", 
                  "foottoeRight_guide")
                          
        legRightRFL=( "footankleRight_guide",
                  "footballRight_guide", 
                  "foottoeRight_guide",
                  "footheelRight_guide",
                  #"footheelLeft_guide"
                  )    
                  
        getLimbs=(legRightFull)         
        for each in getGuide:
            if "heel" in each:
                jointSuffix='_jnt'
                getClass.rigJoints(each, jointSuffix)
                cmds.select(cl=1)       
                jointSuffix='IK_jnt'
                getClass.rigJoints(each, jointSuffix)
                cmds.select(cl=1)
                jointSuffix='FK_jnt'
                getClass.rigJoints(each, jointSuffix)
                cmds.select(cl=1)        
        for each in legRight:
            jointSuffix='FK_jnt'
            getClass.rigJoints(each, jointSuffix)
        cmds.select(cl=1)  
        for each in legRight:
            jointSuffix='IK_jnt'
            getClass.rigJoints(each, jointSuffix)
        cmds.select(cl=1)    
        for each in legRight:
            jointSuffix='_jnt'
            getClass.rigJoints(each, jointSuffix)    
        cmds.select(cl=1)  
                
        for each in reversed(legRightRFL):
            getName=each.split("_")
            jointnames=str(getName[0]+'RFL_jnt')
            if "ankle" in each:
                getTranslation=cmds.xform(each, q=1, t=1)
                RFLitem=cmds.joint(n="footRightRFL_jnt", p=(getTranslation[0], 0, getTranslation[2]))
                #cmds.setAttr(RFLitem+".visibility", 0)
            cmds.select(cl=1)  
            if "foot" in each:
                getTranslation=cmds.xform(each, q=1, t=1)
                cmds.joint(n=jointnames, p=getTranslation) 
            cmds.select(cl=1)
        cmds.parent( "foottoeRightRFL_jnt","footRightRFL_jnt") 
        cmds.parent("footballRightRFL_jnt","foottoeRightRFL_jnt" )
        cmds.parent("footankleRightRFL_jnt","footballRightRFL_jnt" )
        cmds.parent("footheelRightRFL_jnt","footankleRightRFL_jnt" )
        cmds.parent("footheelRight_jnt","footankleRight_jnt" )
        cmds.parent("footheelRightFK_jnt","footankleRightFK_jnt" )
        cmds.parent("footheelRightIK_jnt","footankleRightIK_jnt" )
        
        cmds.mirrorJoint("footRightRFL_jnt", myz=1, sr=("Right", "Left"))
        cmds.mirrorJoint("footankleRightIK_jnt", myz=1, sr=("Right", "Left"))
        cmds.mirrorJoint("footankleRightFK_jnt", myz=1, sr=("Right", "Left"))
        cmds.mirrorJoint("footankleRight_jnt", myz=1, sr=("Right", "Left"))

        
        #########################################################################
        #########################################################################
        #########################################################################
        #########################################################################
        
        Side=["Right", "Left"]
        
        for eachSide in Side:
        
            resetOrient=[
                         "foot"+eachSide+"RFL_jnt",
                         "footankle"+eachSide+"IK_jnt",
                         "footankle"+eachSide+"FK_jnt",
                         "footankle"+eachSide+"_jnt",           
                        ]
                        
            for each in resetOrient:
                    cmds.joint( each, e=1, children=1, zso=1, oj='xyz', sao='yup', spa=1)     
            locsForCleanup=[]
            #locators
            legRFL=( 
                      "footballRight_guide", 
                      "foottoeRight_guide",
                      "footheelRight_guide",
                      "footankle"+eachSide+"RFL_jnt",
                      )        
            for each in reversed(legRFL):
                getName=each.split("_")
                jointnames=str(getName[0]+'_lctr')
                getTranslation=cmds.xform(each, q=1, t=1, ws=1)
                RFLitem=cmds.spaceLocator(n=jointnames, p=(getTranslation[0],0, getTranslation[2]))
                locsForCleanup.append(RFLitem)
                cmds.CenterPivot()
                #cmds.setAttr(RFLitem+".visibility", 0)

                
            #ik hookup
            startLegJoint=[
                        "footankle"+eachSide+"IK_jnt",
                        "football"+eachSide+"IK_jnt",
                        "footankle"+eachSide+"IK_jnt"]
            
            IKleglist=[
                    "football"+eachSide,
                    "foottoe"+eachSide,
                    "footheel"+eachSide]
            for each, item in map(None, IKleglist, startLegJoint):
                cmds.ikHandle(n=each+"_ik", sj=item, ee=each+"IK_jnt", sol="ikRPsolver")
                #cmds.setAttr(each+"_ik.visibility", 0)
                cmds.parent(each+"_ik", each+"RFL_jnt")
                
                
                
            jointGroup=[
                        "football"+eachSide, 
                        "footankle"+eachSide,
                        ]
            for eachjoint in jointGroup:
                if "leg" in eachjoint:
                    eachName=eachjoint+"IK_jnt"
                    getTranslation=cmds.xform(eachName, q=1, t=1, ws=1)
                else:
                    eachName=eachjoint+"RFL_jnt"
                    getTranslation=cmds.xform(eachName, q=1, t=1, ws=1)
                cmds.spaceLocator(n=str(eachName)+"Pole_lctr", p=(getTranslation))
                cmds.CenterPivot()
                cmds.setAttr(str(eachName)+"Pole_lctr.visibility", 0)
            
            cmds.poleVectorConstraint("footankle"+eachSide+"RFL_jntPole_lctr", "football"+eachSide+"_ik")   
            cmds.poleVectorConstraint("football"+eachSide+"RFL_jntPole_lctr ", "foottoe"+eachSide+"_ik") 

            cmds.parent("foottoe"+eachSide+"_ik", "footheel"+eachSide+"RFL_jnt")
            
            
            #CONTROLLER
            scaleWorldMatrix = cmds.xform("footheelRight_guide", q=True, r=1, s=True)
            scaleWorldMatrix=int(scaleWorldMatrix[0])              
            name="footheel"+eachSide+"IK_ctrl"
            grpname="footheel"+eachSide+"IK_grp"
            numlen=5*scaleWorldMatrix
            numwid=12*scaleWorldMatrix
            colour=13
            transformWorldMatrix=cmds.xform("footheel"+eachSide+"_guide", q=1, t=1, ws=1)
            rotateWorldMatrix=[0,0,0]
            getClass.rectI(name, grpname, numlen, numwid, transformWorldMatrix, rotateWorldMatrix, colour)  
            cmds.move(0, 0, 12, name ,r=1, rpr=1, )
            cmds.move(0, 0, -12, name+".rotatePivot" ,r=1, rpr=1 )                 
            cmds.makeIdentity(name, a=True, t=1, s=1, r=1, n=0)
            
            cmds.parentConstraint("footheel"+eachSide+"IK_ctrl", "foot"+eachSide+"RFL_jnt", mo=1, w=1)
            
            scaleWorldMatrix = cmds.xform("footballRight_guide", q=True, r=1, s=True)
            scaleWorldMatrix=int(scaleWorldMatrix[0])     
            eachPiece="football"+eachSide+"_jnt"
            name="football"+eachSide+"_ctrl"
            grpname="football"+eachSide+"_grp"    
            size=7*scaleWorldMatrix
            colour=6     
            nrx=1
            nry=0
            nrz=0
            cmds.select(cl=1) 
            getTranslation, getRotation=getClass.locationXForm(eachPiece)
            getClass.buildCtrl(eachjoint, name, grpname, getTranslation, getRotation, size, colour, nrx, nry, nrz)
            colour1=18
            colour2=colour1
            colour3=colour1
            
            
            ##CONNECT
            
            cmds.connectAttr ("football"+eachSide+"_ctrl.rotate", "football"+eachSide+"FK_jnt.rotate", f=1)

            #use only if controller is lacking these attributes
            cmds.addAttr("footheel"+eachSide+"IK_ctrl", ln="RaiseHeel", at="long", min=-10, max=90, dv=0, k=1, nn="RaiseHeel")
            cmds.addAttr("footheel"+eachSide+"IK_ctrl", ln="TipToe", at="long", min=-10, max=90, dv=0, k=1, nn="TipToe")            
            footAttributes=["SwivelFoot", 
                            "PivotToe", 
                            "SwivelHeel",
                            "RaiseToe"]
            for each in footAttributes:
                cmds.addAttr("footheel"+eachSide+"IK_ctrl", ln=each, at="long", min=-90, max=90, dv=0, k=1, nn=each)
            
            
            cmds.connectAttr ("footheel"+eachSide+"IK_ctrl.RaiseHeel", "foottoe"+eachSide+"RFL_jnt.rotateZ", f=1)

            cmds.connectAttr ("footheel"+eachSide+"IK_ctrl.PivotToe", "foottoe"+eachSide+"RFL_jnt.rotateY", f=1)
            cmds.connectAttr ("footheel"+eachSide+"IK_ctrl.SwivelHeel", "foot"+eachSide+"RFL_jnt.rotateY", f=1)
            cmds.connectAttr ("footheel"+eachSide+"IK_ctrl.SwivelFoot", " football"+eachSide+"RFL_jnt.rotateX", f=1)
            
            cmds.connectAttr ("footheel"+eachSide+"IK_ctrl.RaiseToe", " football"+eachSide+"_jnt.rotateZ", f=1)
            
            cmds.orientConstraint("footankle"+eachSide+"IK_jnt", "footankle"+eachSide+"_jnt", mo=1, w=1)
            cmds.orientConstraint("footankle"+eachSide+"FK_jnt", "footankle"+eachSide+"_jnt", mo=1, w=1)
            for each in locsForCleanup:
                cmds.delete(each)
                
                
            getClass.buildGrp("football"+eachSide+"_jnt")
            getTranslation, getRotation=getClass.locationXForm("football"+eachSide+"_jnt")
            cmds.move(getTranslation[0], getTranslation[1], getTranslation[2], "football"+eachSide+"_jnt_grp.rotatePivot" ,r=1, rpr=1 )
            cmds.orientConstraint("football"+eachSide+"RFL_jnt", "football"+eachSide+"_jnt_grp", mo=1)
            cmds.pointConstraint("foottoe"+eachSide+"RFL_jnt", "foottoe"+eachSide+"_ik", mo=1)
            cmds.connectAttr ("footheel"+eachSide+"IK_ctrl.TipToe", "football"+eachSide+"RFL_jnt.rotateZ", f=1)
            
       