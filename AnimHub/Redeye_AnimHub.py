#------------------------------------------------------------------#
# PR_Animhub
# author : Tan Pang Ren
#
# PR_animToolbox is a fork of TIP animTools  with the aim of providing an alternate
# UI and interaction to tools in TIP_animTools by Jit
# 
# Usage :
#      - please grab TIP_Animhub_loader.py from the server 
#      - place TIP_atb_loader.py as shelf button and load script
#
#
# Note : TIP_Animhub is undergoing heavy development and requires your feedback
#        I'm trying to keep the UI as minimal and as out of the way as possible.
#        any ideas that are going to help with development is appreciated
#        
#        Any bugs can be reported to me   
#-----------------------------------------------------------------#

import maya.cmds as cmds
import pymel.core as pm
import maya.mel as mel
import random
import os
import sys
import subprocess 


#------------- for linking Global script module folder ------------
if os.path.basename(sys.executable) == 'maya.exe':
    # call maya UI if inside maya
    paths = sys.path
    pathfound = 0
    for path in paths:
        if ('C:\Users\Administrator\Desktop\Scripts' == path):
            pathfound = 1
            import Redeye_FBXBaker

    if not pathfound:
        sys.path.insert(0, 'C:\Users\Administrator\Desktop\Scripts')
        import Redeye_FBXBaker

#------------------------------------------------------------------



class UIMain():
    
    
    def __init__(self, parent=None):
        
        self.winName = 'PR_Animhub'
        if pm.window(self.winName, exists=True):
            pm.deleteUI(self.winName)
        if pm.dockControl("animHubDock", label = "TIP_Animhub", exists = True) == True:
            pm.deleteUI("animHubDock")    
        pm.window(self.winName,  w=200,h=300,mnb=True,mxb=False,sizeable=True,resizeToFitChildren=True,minimizeCommand = pm.Callback(self.dockerIn), restoreCommand=pm.Callback(self.dockerOut))
        pm.showWindow(self.winName)
        
        #globals
        self.RefListt=[]
        self.DaLocator=[]
        self.ShiftList=[]
        self.CurrentSelection=''
        self.locCounter=0
        
        #main Layout start
        self.mainLay = pm.columnLayout(adjustableColumn=True)
        
        self.imageOfTheDay = cmds.paneLayout()
        #self.imageBtn = cmds.button(parent=self.imageOfTheDay,annotation='Image of the day',isObscured=True )
        self.image = cmds.symbolButton(parent=self.imageOfTheDay, image = 'G:/My Drive/goGame 3D Team (SG+MY)/Scripts/MayaTools/Redeye_Animhub/Animhub.jpg',annotation='Image of the day',preventOverride=False, command = pm.Callback(self.openImageOTD))

        #Start Scene Layout start
        self.frame4 = pm.frameLayout(parent=self.mainLay,label='Start',cll=1,cl=True,mh=5)
        self.rowcol7 = pm.rowColumnLayout(parent=self.frame4,numberOfColumns=3,height = 30,columnAttach=[1,'left',5])
        self.camBtn1 = pm.button(label='Create Camera',command = pm.Callback(self.createCamFn))
        self.audioBtn1 = pm.button(label ='Import Audio',command = pm.Callback(self.importAudioFn))
        #Start Scene Layout end
        
        #Reference Layout start
        self.frame5 = pm.frameLayout(parent=self.mainLay,label='References',cll=1,cl=True,mh=5)
        pm.text(label = 'Bulk reference',bgc=[0.8,0.8,0.8])
        self.rowcol0 = pm.rowColumnLayout(parent=self.frame5,numberOfColumns=2,height = 200,columnAttach=[1,'left',5])
        self.rowcol1 = pm.scrollLayout(parent=self.rowcol0,height = 200,width=250)
        self.rowcol2 = pm.rowColumnLayout(parent=self.rowcol0,numberOfRows=6,height = 100,columnAttach=[1,'left',5])
        
        
        self.reftextscroll = pm.textScrollList(parent=self.rowcol1,height= 200, width = 250, ams=True)
        self.prdropdown = pm.optionMenu("project",parent=self.rowcol2,width = 90)
        pm.menuItem(parent=self.prdropdown,label='One_Piece')
        pm.menuItem(parent=self.prdropdown,label='Disney')
        self.browseBtn = pm.button(parent=self.rowcol2, label = '        Browse       ',command = pm.Callback(self.browseRefFn)) 
        self.removeRefBtn = pm.button(parent=self.rowcol2, label = '       Remove       ',command = pm.Callback(self.removeFn))
        pm.separator(parent=self.rowcol2,height = 50)
        self.loadRbutton = pm.button(parent=self.rowcol2,label='Load References',annotation='Load All references in List',command = pm.Callback(self.loadAllRef))
  
        pm.text(parent=self.frame5,label = 'Misc reference Tools',bgc=[0.8,0.8,0.8])
        self.rowcol3 = pm.rowColumnLayout(parent=self.frame5,numberOfRows=1,height = 30,columnAttach=[1,'left',8])
        self.unloadRbutton = pm.button(parent=self.rowcol3,label='Unload Viewport Selection',command = pm.Callback(self.unloadSel))
        self.refPlacebutton = pm.button(parent=self.rowcol3,label='Reference Placement',command = pm.Callback(self.refPlaceFn))
        #Reference Layout end
        
        #shaking layout start----------------------------------------------------------------------------#
        #postphoned development till required
        #self.frame6 = pm.frameLayout(parent=self.mainLay,label='Shaking ( in development )',cll=1,cl=True,mh=5)
        #self.shakeText = pm.text(label = '            Lets start Shaking',parent=self.frame6, align='left')
        #self.row1 = pm.rowLayout(parent=self.frame6,numberOfColumns=3,height = 30,columnAttach=[1,'left',5])
        #self.insertButton = pm.button(parent=self.row1,label='>>',command=pm.Callback(self.inputTextfield))
        #self.deText = pm.textField('detext',parent=self.row1,width=200,height=25)
        #self.startShakeBtn = pm.button(parent=self.row1,label='Start Shake')
        #shaking layout end------------------------------------------------------------------------------#
        
        #Movekeys layout start        
        self.frame7 = pm.frameLayout(parent=self.mainLay,label='MoveKeys',cll=1,cl=True,mh=5)
        self.row2 = pm.rowLayout(parent = self.frame7,numberOfColumns=2,height=26,columnAttach=[1,'both',5])
        self.keyInt1 = pm.intField('keyInt',width=40,height = 25,enterCommand = pm.Callback(self.moveMaster))
        self.moveButton=pm.button(label='Move',width=62,height = 25,annotation='Select frame range and all keys will be moved \n [x] number of frames',command = pm.Callback(self.moveMaster))

        
        self.row3 = pm.rowLayout(parent = self.frame7,numberOfColumns=4,height=30,columnAttach=[1,'left',5])
        self.backFive = pm.button(parent = self.row3, label='|<',annotation='-5 frames',command = pm.Callback(self.moveBits,-5))
        self.backOne = pm.button(parent = self.row3, label='<    ',annotation='-1 frames',command = pm.Callback(self.moveBits,-1))
        self.forwardOne = pm.button(parent = self.row3, label='    >',annotation='+1 frames',command = pm.Callback(self.moveBits,1))
        self.forwardFive = pm.button(parent = self.row3, label='>|',annotation='+5 frames',command = pm.Callback(self.moveBits,5) )
        #Movekeys layout end
        
        #playblast layout start
        self.frame8 = pm.frameLayout(parent=self.mainLay,label='Playblast',cll=1,cl=True,mh=5) 
        self.rowcol3 = pm.rowColumnLayout(parent=self.frame8,numberOfColumns=4,height = 40,columnAttach=[1,'left',5])
        self.infoLbl = pm.text(parent=self.rowcol3,label ='Output Path :  ')
        self.outputPath = pm.textField(parent = self.rowcol3,width = 240)
        pm.separator(parent = self.rowcol3,width = 10,visible=False)
        self.browseBtn2 = pm.button(label = "...", command = pm.Callback(self.browsePbFn))
        
        self.soundChk = pm.checkBox(parent=self.rowcol3,label = 'sound', value = True)
        self.shadedChk = pm.checkBox(parent=self.rowcol3,label = 'Shaded', value = True)
        
        self.rowcol4 = pm.rowColumnLayout(parent=self.frame8,numberOfColumns=2,height = 25,columnAttach=[1,'left',10])
        self.dateLbl = pm.text(parent=self.rowcol4,label = "Updated on 13/02/2014 @ 1520hrs                                        ")
        self.playBlastBtn = pm.button(parent=self.rowcol4,label = "Playblast", command = pm.Callback(self.playBlastFn))
        #playblast layout end
        
        #snapping Functions layout start
        self.frame9 = pm.frameLayout(parent=self.mainLay,label='Snapping Functions',cll=1,cl=True,mh=5)
        snapAnnotation = 'Click on Parent first then Child / Children' 
        pm.text(parent = self.frame9,label = 'Snap to Parent',bgc=[0.8,0.8,0.8])
        self.rowcol5 = pm.rowColumnLayout(parent=self.frame9,numberOfColumns=7,height = 80,columnAttach=[1,'left',10],rowOffset=[1,'top',5])
        self.snapParentBtn = pm.button(parent = self.rowcol5,width=100,label = 'Parent',annotation=snapAnnotation,command= pm.Callback(self.snappingParent))
        pm.separator(parent=self.rowcol5,width = 10,visible=False)
        self.prx = pm.checkBox(parent=self.rowcol5,label = 'x', value = True,)
        pm.separator(parent=self.rowcol5,width = 10,visible=False)
        self.pry = pm.checkBox(parent=self.rowcol5,label = 'y', value = True)        
        pm.separator(parent=self.rowcol5,width = 10,visible=False)
        self.prz = pm.checkBox(parent=self.rowcol5,label = 'z', value = True)   
        
        self.snapPointBtn = pm.button(parent = self.rowcol5,width=100,label = 'Point',annotation=snapAnnotation,command =pm.Callback(self.snappingTrans))
        pm.separator(parent=self.rowcol5,width = 10,visible=False)
        self.px = pm.checkBox(parent=self.rowcol5,label = 'x', value = True)
        pm.separator(parent=self.rowcol5,width = 10,visible=False)
        self.py = pm.checkBox(parent=self.rowcol5,label = 'y', value = True)        
        pm.separator(parent=self.rowcol5,width = 10,visible=False)
        self.pz = pm.checkBox(parent=self.rowcol5,label = 'z', value = True)   
        
        self.snapOrientBtn = pm.button(parent = self.rowcol5,width=100,label = 'Orient',annotation=snapAnnotation,command =pm.Callback(self.snappingRot))
        pm.separator(parent=self.rowcol5,width = 10,visible=False)
        self.ox = pm.checkBox(parent=self.rowcol5,label = 'x', value = True)
        pm.separator(parent=self.rowcol5,width = 10,visible=False)
        self.oy = pm.checkBox(parent=self.rowcol5,label = 'y', value = True)        
        pm.separator(parent=self.rowcol5,width = 10,visible=False)
        self.oz = pm.checkBox(parent=self.rowcol5,label = 'z', value = True)          

        pm.text(parent = self.frame9,label = 'Sliding fixer',bgc=[0.8,0.8,0.8])
        self.rowcol6 = pm.rowColumnLayout(parent=self.frame9,numberOfColumns=4,height = 30,columnAttach=[1,'left',10],rowOffset=[1,'bottom',0])
         
        self.targetBtn = pm.button(parent = self.rowcol6, label = 'Target',command =pm.Callback(self.makingLocator)) 
        self.stickMinBtn = pm.button(parent = self.rowcol6, label = '<-- Stick',command = pm.Callback(self.stickitback))
        self.stickMaxBtn = pm.button(parent = self.rowcol6, label = 'Stick -->',command = pm.Callback(self.stickitfront))  
        self.tarCleanBtn = pm.button(parent = self.rowcol6, label = 'Clean Up Locators',command = pm.Callback(self.deleteLoc))
        #snapping functions layout end
        
        #Anim Tools Layout start
        self.frame10 = pm.frameLayout(parent=self.mainLay,label='Animation Tools',cll=1,cl=True,mh=5)
        pm.text(label = 'Animation offset Tool',width = 150,align='center',bgc=(0.7,0.7,0.7))        
        self.rowcol8 = pm.rowColumnLayout(parent=self.frame10,numberOfColumns=2,height = 200,columnAttach=[1,'left',5])
        self.rowcol9 = pm.scrollLayout(parent=self.rowcol8,height = 200,width=200)
        self.shiftytextscroll = pm.textScrollList(parent=self.rowcol9,height= 200, width = 250, ams=True)
        
        
        self.rowco20 = pm.rowColumnLayout(parent=self.rowcol8,numberOfRows=10)
        self.shiftyappend = pm.button(parent = self.rowco20,label='Append',command=pm.Callback(self.loadShifty))
        self.shiftyremove = pm.button(parent = self.rowco20,label='Remove',command=pm.Callback(self.removeShifty))
        
        pm.separator(parent=self.rowco20,height = 10,visible=False)
        pm.text(parent = self.rowco20, label = 'Translation offset',bgc = (0.3,0.3,0.3))
        self.rowco21 = pm.rowColumnLayout(parent=self.rowco20,numberOfColumns=6)
        self.shiftytx = pm.floatField(parent=self.rowco21, width=40,height = 25,pre=2)
        pm.text(label = 'X',width = 20)
        self.shiftyty = pm.floatField(parent=self.rowco21, width=40,height = 25,pre=2)
        pm.text(label = 'Y',width = 20)
        self.shiftytz = pm.floatField(parent=self.rowco21, width=40,height = 25,pre=2)
        pm.text(label = 'Z',width = 20)
        pm.separator(parent=self.rowco20,height = 10,visible=False)
                
        pm.text(parent = self.rowco20, label = 'TimeRange',bgc = (0.3,0.3,0.3))
        
        #pm.separator(parent=self.rowco20,height = 10,visible=False)
        self.rowco22 = pm.rowColumnLayout(parent=self.rowco20,numberOfColumns=4)
        self.timeSt = pm.intField(width=30,height = 25,value=1)
        pm.text(label = '   Start   ',width = 50,align='left')
        self.timeEnd = pm.intField(width=30,height = 25,value=300)
        pm.text(label = '   End   ',width = 30)
        self.shiftit = pm.button(parent = self.rowco20,label='Shift it!',bgc=(0.7,0.7,0.7), command=pm.Callback(self.runShiftySelected))

        #Anim Tools End
        
        #End layout start
        self.endframe01 = pm.frameLayout(parent=self.mainLay,label='End',cll=1,cl=False,mh=5)
        self.rowco25 = pm.rowColumnLayout(parent=self.endframe01,numberOfColumns=5,height = 100,columnAttach=[1,'left',5])
        self.copy1Chkbox = pm.checkBox(parent=self.rowco25,label = 'Server location', value = True ) 
        self.copy1Path = pm.textField(parent = self.rowco25,width = 240,text = 'G:/My Drive/goGame 3D Team (SG+MY)/Galaxy/Art/3D/Character Animation')
        pm.separator(parent=self.rowco25,width = 5,visible=False)
        self.serverBrowse = pm.button(parent=self.rowco25, label = ". . .", command=pm.Callback(self.browseServFn))
        pm.text(label='Server')
        #self.cleanupBtn = pm.button(parent = self.rowco25, label = 'AnimBake',command = pm.Callback(self.animBakeFn))
        self.copy2Chkbox = pm.checkBox(parent=self.rowco25,height = 25,label = 'FBX location', value = True)
        self.copy2Path = pm.textField(parent = self.rowco25,width = 240,text = 'G:/My Drive/goGame 3D Team (SG+MY)/Galaxy/Art/3D/Milestones/Milestone3')
        pm.separator(parent=self.rowco25,width = 5,visible=False)
        self.unityBrowse = pm.button(parent=self.rowco25, height = 20,label = ". . .", command=pm.Callback(self.browseUnityFn))
        pm.text(label='Unity')
        
        self.gmoviesChkbox = pm.checkBox(parent=self.rowco25,height = 25,label = 'Playblast loc', value = True)
        self.gmoviesPath = pm.textField(parent = self.rowco25,width = 240,text = 'G:/My Drive/goGame 3D Team (SG+MY)/Galaxy/Art/3D/Milestones/Milestone3')
        pm.separator(parent=self.rowco25,width = 5,visible=False)
        self.gmoviesBrowse = pm.button(parent=self.rowco25, height = 20,label = ". . .", command=pm.Callback(self.browseGmoviesFn))
        pm.text(label='Gdrive')
        
        self.hotreloadChkbox = pm.checkBox(parent=self.rowco25,label = 'Hot reload', value = False ) 
        
        pm.button(parent=self.rowco25, label = "Approved AnimBake", bgc =[0,1,0] , command=pm.Callback(self.animBakeFn))
        #pm.button(parent=self.rowco25, label = "copy1", command=pm.Callback(self.getcopy1field))
        #pm.button(parent=self.rowco25, label = "copy2", command=pm.Callback(self.getcopy2field))
        #pm.button(parent=self.rowco25, label = "copy3", command=pm.Callback(self.getcopy3field))

        self.rowco251 = pm.rowColumnLayout(parent=self.endframe01, numberOfColumns=2, height=30,columnAttach=[1, 'left', 5])
        pm.separator(parent=self.rowco251, width=100, visible=False)
        pm.button(parent=self.rowco251, label="Approved AnimBake New",width=240, bgc=[0, 0.8, 0.2], command =pm.Callback(self.animBakeFn2))
        self.rowco252 = pm.rowColumnLayout(parent=self.endframe01, numberOfColumns=4, height=30,
                                           columnAttach=[1, 'left', 5])
        pm.separator(parent=self.rowco252, width=100, visible=False)
        pm.button(parent=self.rowco252, label="Bake @skin", width=115, bgc=[0, 0.8, 0.2],command =pm.Callback(self.animBakeFn3))
        pm.separator(parent=self.rowco252, width=10, visible=False)
        pm.button(parent=self.rowco252, label="Bake @animation", width=115, bgc=[0, 0.8, 0.2],command =pm.Callback(self.animBakeFn4))

        self.rowco26 = pm.rowColumnLayout(parent=self.endframe01, numberOfColumns=2, height=80,columnAttach=[1, 'left', 5])
        pm.text(label='File Info :    ')
        self.filecheckBtn = pm.button (parent =self.rowco26, label = 'File Check',command=pm.Callback(self.fileCheckFn))
        pm.text (parent =self.rowco26,label='FileName : ')
        self.fileName = pm.text('<curent filename>')
        pm.text(label = "Character ID : ")
        self.charID = pm.text('<CHAxxx>')
        pm.text(label="Character Name : ")
        self.charName = pm.text('<Name>')
        pm.text(label="cycleName : ")
        self.cycleName = pm.text('<Cycle>')

        self.rowco27 = pm.rowColumnLayout(parent=self.endframe01, numberOfColumns=2, height=10,columnAttach=[1, 'left', 5])
        self.dateUpdated = pm.text(parent=self.endframe01,label = "Updated on 22/08/2019")
        #end layout end 123

        #functions to run on Start
        self.checkLocators()
        


    def dockerIn(self):
        #--- Docking of UI ---
        if pm.dockControl("animHubDock", label = "TIP_Animhub", exists = True) == True:
            pm.deleteUI("animHubDock")
        allowedAreas = ['right']
        pm.dockControl("animHubDock", label = "TIP_Animhub", area= 'right', content = self.winName, allowedArea=allowedAreas)

    def dockerOut(self):
        if pm.dockControl("animHubDock", label = "TIP_Animhub", exists = True) == True:
            pm.deleteUI("animHubDock")
        x=UIMain

    def openImageOTD(self):
        subprocess.Popen(r'explorer /select,"G:\My Drive\goGame 3D Team (SG+MY)\Scripts\MayaTools\Redeye_Animhub"')
        #subprocess.call("explorer C:\Users\pangren\Pictures\Wallpaper", shell=True)
        
#----------------------------------------------------------------------------#
#Tools from Other Scripts
    def makeDir(self, path,*args):
        """
        input a path to check if it exists, if not, it creates all the path
        :return: path string
        """
        if not os.path.exists(path):
            pm.sysFile(path, makeDir=True)
            #os.makedirs(path)

    def animBakeFn4(self, *args):
        '''
        approved with new filenaming setup
        :param args:
        :return:
        '''
        print 'bakefn2 initiated'
        try:
            reload(Redeye_FBXBaker)
        except:
            import Redeye_FBXBaker
            reload(Redeye_FBXBaker)

        charDetails2 = Redeye_FBXBaker.mainBakefunction4()

        #for char2 in charDetails2:
        #    print char2
        '''
        charDetails2 [0~5]
        [0] fbx name full path : G:/My Drive/goGame 3D Team (SG+MY)/Galaxy/Art/3D/Submission/Animation/08212019/FBX/CHA043_penguinaxe@hit.fbx
        [1] playblast local path : G:\My Drive\goGame 3D Team (SG+MY)\Galaxy\Art\3D\Character Animation\movies\CHA043_penguinaxe@hit_00.mov
        [2] character name : penguinaxe
        [3] character ID : CHA043
        [4] playblast name : CHA043_penguinaxe@hit_00.mov
        [5] maya file : G:/My Drive/goGame 3D Team (SG+MY)/Galaxy/Art/3D/Submission/Animation/08212019/CHA043_penguinaxe@hit_00.ma
        '''

        # after baking and playblasting, script will check the status of your UI , if UI specify copy location and checkbox is ticked, it will initiate copy of fbx and movie files.
        print 'FBX and Maya file copy to server :-------------------'
        if self.copy1Chkbox.getValue() == True:
            try:
                serverLoc = str(self.copy1Path.getText())
                if pm.sysFile(charDetails2[0], copy=serverLoc + '/' + charDetails2[3] + '_' + charDetails2[2] + '/' + charDetails2[3] + '/' + charDetails2[0].split("/")[-1]) == False:
                    print "FBX & Maya folder doesn't exists. Creating now.... "
                    self.makeDir(str(serverLoc + '/' + charDetails2[3] + '_' + charDetails2[2] + '/' + charDetails2[3]))
                    self.makeDir(str(serverLoc+'/'+ charDetails2[3] + '_' + charDetails2[2]+'/Raw/scenes'))
                    #copy FBX
                    pm.sysFile(charDetails2[0], copy=serverLoc + '/' + charDetails2[3] + '_' + charDetails2[2] + '/' + charDetails2[3] + '/' + charDetails2[0].split("/")[-1])
                    #copy Maya
                    pm.sysFile(charDetails2[5], copy=serverLoc + '/' + charDetails2[3] + '_' + charDetails2[2] + '/Raw/scenes/' + charDetails2[5].split("/")[-1])
                    print 'FBX and Maya file copied to %s ' % (str(serverLoc) + '/' + charDetails2[2] + '/' + charDetails2[3])
                else:
                    pm.sysFile(charDetails2[0], copy=serverLoc + '/' + charDetails2[3] + '_' + charDetails2[2] + '/' + charDetails2[3] + '/' + charDetails2[0].split("/")[-1])
                    pm.sysFile(charDetails2[5], copy=serverLoc + '/' + charDetails2[3] + '_' + charDetails2[2] + '/Raw/scenes/' + charDetails2[5].split("/")[-1])
                    print 'FBX and Maya file copied to %s ' % (str(serverLoc) + '/' + charDetails2[3] + '_' + charDetails2[2])
            except:
                print "FBX Maya loop doesn't work please contact programmer"

        else:
            print 'FBX and Maya file copy to server : no copy required'

        print 'FBX and Maya file copy to server: End'

        ######################################FBX copy to local Unity loop
        print 'FBX copy to Unity : ----------------------'
        if self.copy2Chkbox.getValue() ==True:
            try:
                unityLoc=str(self.copy2Path.getText())
                if pm.sysFile(charDetails2[0], copy=unityLoc+'/'+charDetails2[3]+'_'+ charDetails2[2]+'/'+charDetails2[0].split("/")[-1]) == False :
                    print "Unity folder doesn't exists. Creating now.... "
                    self.makeDir(str(unityLoc+'/'+charDetails2[3]+'_'+ charDetails2[2]))
                    pm.sysFile(charDetails2[0], copy=unityLoc+'/'+charDetails2[3]+'_'+ charDetails2[2]+'/'+charDetails2[0].split("/")[-1])
                    print 'FBX copy to Unity : %s' % str(unityLoc + '/'+charDetails2[3]+'_'+ charDetails2[2])
                else:
                    pm.sysFile(charDetails2[0], copy=unityLoc+'/'+charDetails2[3]+'_'+ charDetails2[2]+'/'+charDetails2[0].split("/")[-1])
                    print 'FBX copy to Unity : %s' % str(unityLoc + '/'+charDetails2[3]+'_'+ charDetails2[2])
            except:
                print "Unity loop doesn't work please contact programmer"
        else :
            print 'FBX copy to Unity : no copy required'
        print 'FBX copy to Unity : End'

        #################################### Playblast to Gmovies loop
        print 'Gmovies copy :----------------'
        if self.gmoviesChkbox.getValue() == True:
            try:
                gmoviesLoc=str(self.gmoviesPath.getText())
                if pm.sysFile(charDetails2[1], copy=gmoviesLoc+'/'+charDetails2[3]+'_'+ charDetails2[2] + '/'+charDetails2[4]) == False:
                    print "Gmovies folder doesn't exists, Creating now.... "
                    self.makeDir(str(gmoviesLoc+'/'+charDetails2[3]+'_'+ charDetails2[2]))
                    pm.sysFile(charDetails2[1], copy=gmoviesLoc+'/'+charDetails2[3]+'_'+ charDetails2[2]+ '/' + charDetails2[4])
                    print 'Gmovies copied to : %s' % str(gmoviesLoc+'/'+charDetails2[3]+'_'+ charDetails2[2]+ '/' + charDetails2[4])
                else:
                    pm.sysFile(charDetails2[1], copy=gmoviesLoc+'/'+charDetails2[3]+'_'+ charDetails2[2]+'/'+ charDetails2[4])
                    print 'Gmovies copied to : %s' % str(gmoviesLoc+'/'+charDetails2[3]+'_'+ charDetails2[2]+'/'+ charDetails2[4])
            except :
                print "copy to Gmovies loop doesn't work please contact programmer"
        else :
            print 'Gmovies copy : no copy required'
        print 'Gmovies copy : End'

        cmds.confirmDialog(title='Success', message='\n' + 'Anim Bake Finished without Errors', button='Ok',
                           messageAlign='left')

        ################check for hot reload option
        if self.hotreloadChkbox.getValue() == True:
            print
            'Hot Reload : True'
            cmds.file(newFile=True, force=True)
            cmds.file(charDetails2[5], open=True)
        else:
            print
            'Hot Reload : False'

            # print "Anim Bake Finished without Errors"

    def animBakeFn3(self, *args):
        '''
        approved with new filenaming setup
        :param args:
        :return:
        '''
        print 'bakefn2 initiated'
        try:
            reload(Redeye_FBXBaker)
        except:
            import Redeye_FBXBaker
            reload(Redeye_FBXBaker)

        charDetails2 = Redeye_FBXBaker.mainBakefunction3()

        #for char2 in charDetails2:
        #    print char2
        '''
        charDetails2 [0~5]
        [0] fbx name full path : G:/My Drive/goGame 3D Team (SG+MY)/Galaxy/Art/3D/Submission/Animation/08212019/FBX/CHA043_penguinaxe@hit.fbx
        [1] playblast local path : G:\My Drive\goGame 3D Team (SG+MY)\Galaxy\Art\3D\Character Animation\movies\CHA043_penguinaxe@hit_00.mov
        [2] character name : penguinaxe
        [3] character ID : CHA043
        [4] playblast name : CHA043_penguinaxe@hit_00.mov
        [5] maya file : G:/My Drive/goGame 3D Team (SG+MY)/Galaxy/Art/3D/Submission/Animation/08212019/CHA043_penguinaxe@hit_00.ma
        '''

        # after baking and playblasting, script will check the status of your UI , if UI specify copy location and checkbox is ticked, it will initiate copy of fbx and movie files.
        print 'FBX and Maya file copy to server :-------------------'
        if self.copy1Chkbox.getValue() == True:
            try:
                serverLoc = str(self.copy1Path.getText())
                if pm.sysFile(charDetails2[0], copy=serverLoc + '/' + charDetails2[3] + '_' + charDetails2[2] + '/' + charDetails2[3] + '/' + charDetails2[0].split("/")[-1]) == False:
                    print "FBX & Maya folder doesn't exists. Creating now.... "
                    self.makeDir(str(serverLoc + '/' + charDetails2[3] + '_' + charDetails2[2] + '/' + charDetails2[3]))
                    self.makeDir(str(serverLoc+'/'+ charDetails2[3] + '_' + charDetails2[2]+'/Raw/scenes'))
                    #copy FBX
                    pm.sysFile(charDetails2[0], copy=serverLoc + '/' + charDetails2[3] + '_' + charDetails2[2] + '/' + charDetails2[3] + '/' + charDetails2[0].split("/")[-1])
                    #copy Maya
                    pm.sysFile(charDetails2[5], copy=serverLoc + '/' + charDetails2[3] + '_' + charDetails2[2] + '/Raw/scenes/' + charDetails2[5].split("/")[-1])
                    print 'FBX and Maya file copied to %s ' % (str(serverLoc) + '/' + charDetails2[2] + '/' + charDetails2[3])
                else:
                    pm.sysFile(charDetails2[0], copy=serverLoc + '/' + charDetails2[3] + '_' + charDetails2[2] + '/' + charDetails2[3] + '/' + charDetails2[0].split("/")[-1])
                    pm.sysFile(charDetails2[5], copy=serverLoc + '/' + charDetails2[3] + '_' + charDetails2[2] + '/Raw/scenes/' + charDetails2[5].split("/")[-1])
                    print 'FBX and Maya file copied to %s ' % (str(serverLoc) + '/' + charDetails2[3] + '_' + charDetails2[2])
            except:
                print "FBX Maya loop doesn't work please contact programmer"

        else:
            print 'FBX and Maya file copy to server : no copy required'

        print 'FBX and Maya file copy to server: End'

        ######################################FBX copy to local Unity loop
        print 'FBX copy to Unity : ----------------------'
        if self.copy2Chkbox.getValue() ==True:
            try:
                unityLoc=str(self.copy2Path.getText())
                if pm.sysFile(charDetails2[0], copy=unityLoc+'/'+charDetails2[3]+'_'+ charDetails2[2]+'/'+charDetails2[0].split("/")[-1]) == False :
                    print "Unity folder doesn't exists. Creating now.... "
                    self.makeDir(str(unityLoc+'/'+charDetails2[3]+'_'+ charDetails2[2]))
                    pm.sysFile(charDetails2[0], copy=unityLoc+'/'+charDetails2[3]+'_'+ charDetails2[2]+'/'+charDetails2[0].split("/")[-1])
                    print 'FBX copy to Unity : %s' % str(unityLoc + '/'+charDetails2[3]+'_'+ charDetails2[2])
                else:
                    pm.sysFile(charDetails2[0], copy=unityLoc+'/'+charDetails2[3]+'_'+ charDetails2[2]+'/'+charDetails2[0].split("/")[-1])
                    print 'FBX copy to Unity : %s' % str(unityLoc + '/'+charDetails2[3]+'_'+ charDetails2[2])
            except:
                print "Unity loop doesn't work please contact programmer"
        else :
            print 'FBX copy to Unity : no copy required'
        print 'FBX copy to Unity : End'

        #################################### Playblast to Gmovies loop
        print 'Gmovies copy :----------------'
        if self.gmoviesChkbox.getValue() == True:
            try:
                gmoviesLoc=str(self.gmoviesPath.getText())
                if pm.sysFile(charDetails2[1], copy=gmoviesLoc+'/'+charDetails2[3]+'_'+ charDetails2[2] + '/'+charDetails2[4]) == False:
                    print "Gmovies folder doesn't exists, Creating now.... "
                    self.makeDir(str(gmoviesLoc+'/'+charDetails2[3]+'_'+ charDetails2[2]))
                    pm.sysFile(charDetails2[1], copy=gmoviesLoc+'/'+charDetails2[3]+'_'+ charDetails2[2]+ '/' + charDetails2[4])
                    print 'Gmovies copied to : %s' % str(gmoviesLoc+'/'+charDetails2[3]+'_'+ charDetails2[2]+ '/' + charDetails2[4])
                else:
                    pm.sysFile(charDetails2[1], copy=gmoviesLoc+'/'+charDetails2[3]+'_'+ charDetails2[2]+'/'+ charDetails2[4])
                    print 'Gmovies copied to : %s' % str(gmoviesLoc+'/'+charDetails2[3]+'_'+ charDetails2[2]+'/'+ charDetails2[4])
            except :
                print "copy to Gmovies loop doesn't work please contact programmer"
        else :
            print 'Gmovies copy : no copy required'
        print 'Gmovies copy : End'

        cmds.confirmDialog(title='Success', message='\n' + 'Anim Bake Finished without Errors', button='Ok',
                           messageAlign='left')

        ################check for hot reload option
        if self.hotreloadChkbox.getValue() == True:
            print
            'Hot Reload : True'
            cmds.file(newFile=True, force=True)
            cmds.file(charDetails2[5], open=True)
        else:
            print
            'Hot Reload : False'

            # print "Anim Bake Finished without Errors"

    def animBakeFn2(self, *args):
        '''
        approved with new filenaming setup
        :param args:
        :return:
        '''
        print 'bakefn2 initiated'
        try:
            reload(Redeye_FBXBaker)
        except:
            import Redeye_FBXBaker
            reload(Redeye_FBXBaker)

        charDetails2 = Redeye_FBXBaker.mainBakefunction2()

        #for char2 in charDetails2:
        #    print char2
        '''
        charDetails2 [0~5]
        [0] fbx name full path : G:/My Drive/goGame 3D Team (SG+MY)/Galaxy/Art/3D/Submission/Animation/08212019/FBX/CHA043_penguinaxe@hit.fbx
        [1] playblast local path : G:\My Drive\goGame 3D Team (SG+MY)\Galaxy\Art\3D\Character Animation\movies\CHA043_penguinaxe@hit_00.mov
        [2] character name : penguinaxe
        [3] character ID : CHA043
        [4] playblast name : CHA043_penguinaxe@hit_00.mov
        [5] maya file : G:/My Drive/goGame 3D Team (SG+MY)/Galaxy/Art/3D/Submission/Animation/08212019/CHA043_penguinaxe@hit_00.ma
        '''

        # after baking and playblasting, script will check the status of your UI , if UI specify copy location and checkbox is ticked, it will initiate copy of fbx and movie files.
        print 'FBX and Maya file copy to server :-------------------'
        if self.copy1Chkbox.getValue() == True:
            try:
                serverLoc = str(self.copy1Path.getText())
                if pm.sysFile(charDetails2[0], copy=serverLoc + '/' + charDetails2[3] + '_' + charDetails2[2] + '/' + charDetails2[3] + '/' + charDetails2[0].split("/")[-1]) == False:
                    print "FBX & Maya folder doesn't exists. Creating now.... "
                    self.makeDir(str(serverLoc + '/' + charDetails2[3] + '_' + charDetails2[2] + '/' + charDetails2[3]))
                    self.makeDir(str(serverLoc+'/'+ charDetails2[3] + '_' + charDetails2[2]+'/Raw/scenes'))
                    #copy FBX
                    pm.sysFile(charDetails2[0], copy=serverLoc + '/' + charDetails2[3] + '_' + charDetails2[2] + '/' + charDetails2[3] + '/' + charDetails2[0].split("/")[-1])
                    #copy Maya
                    pm.sysFile(charDetails2[5], copy=serverLoc + '/' + charDetails2[3] + '_' + charDetails2[2] + '/Raw/scenes/' + charDetails2[5].split("/")[-1])
                    print 'FBX and Maya file copied to %s ' % (str(serverLoc) + '/' + charDetails2[2] + '/' + charDetails2[3])
                else:
                    pm.sysFile(charDetails2[0], copy=serverLoc + '/' + charDetails2[3] + '_' + charDetails2[2] + '/' + charDetails2[3] + '/' + charDetails2[0].split("/")[-1])
                    pm.sysFile(charDetails2[5], copy=serverLoc + '/' + charDetails2[3] + '_' + charDetails2[2] + '/Raw/scenes/' + charDetails2[5].split("/")[-1])
                    print 'FBX and Maya file copied to %s ' % (str(serverLoc) + '/' + charDetails2[3] + '_' + charDetails2[2])
            except:
                print "FBX Maya loop doesn't work please contact programmer"

        else:
            print 'FBX and Maya file copy to server : no copy required'

        print 'FBX and Maya file copy to server: End'

        ######################################FBX copy to local Unity loop
        print 'FBX copy to Unity : ----------------------'
        if self.copy2Chkbox.getValue() ==True:
            try:
                unityLoc=str(self.copy2Path.getText())
                if pm.sysFile(charDetails2[0], copy=unityLoc+'/'+charDetails2[3]+'_'+ charDetails2[2]+'/'+charDetails2[0].split("/")[-1]) == False :
                    print "Unity folder doesn't exists. Creating now.... "
                    self.makeDir(str(unityLoc+'/'+charDetails2[3]+'_'+ charDetails2[2]))
                    pm.sysFile(charDetails2[0], copy=unityLoc+'/'+charDetails2[3]+'_'+ charDetails2[2]+'/'+charDetails2[0].split("/")[-1])
                    print 'FBX copy to Unity : %s' % str(unityLoc + '/'+charDetails2[3]+'_'+ charDetails2[2])
                else:
                    pm.sysFile(charDetails2[0], copy=unityLoc+'/'+charDetails2[3]+'_'+ charDetails2[2]+'/'+charDetails2[0].split("/")[-1])
                    print 'FBX copy to Unity : %s' % str(unityLoc + '/'+charDetails2[3]+'_'+ charDetails2[2])
            except:
                print "Unity loop doesn't work please contact programmer"
        else :
            print 'FBX copy to Unity : no copy required'
        print 'FBX copy to Unity : End'

        #################################### Playblast to Gmovies loop
        print 'Gmovies copy :----------------'
        if self.gmoviesChkbox.getValue() == True:
            try:
                gmoviesLoc=str(self.gmoviesPath.getText())
                if pm.sysFile(charDetails2[1], copy=gmoviesLoc+'/'+charDetails2[3]+'_'+ charDetails2[2] + '/'+charDetails2[4]) == False:
                    print "Gmovies folder doesn't exists, Creating now.... "
                    self.makeDir(str(gmoviesLoc+'/'+charDetails2[3]+'_'+ charDetails2[2]))
                    pm.sysFile(charDetails2[1], copy=gmoviesLoc+'/'+charDetails2[3]+'_'+ charDetails2[2]+ '/' + charDetails2[4])
                    print 'Gmovies copied to : %s' % str(gmoviesLoc+'/'+charDetails2[3]+'_'+ charDetails2[2]+ '/' + charDetails2[4])
                else:
                    pm.sysFile(charDetails2[1], copy=gmoviesLoc+'/'+charDetails2[3]+'_'+ charDetails2[2]+'/'+ charDetails2[4])
                    print 'Gmovies copied to : %s' % str(gmoviesLoc+'/'+charDetails2[3]+'_'+ charDetails2[2]+'/'+ charDetails2[4])
            except :
                print "copy to Gmovies loop doesn't work please contact programmer"
        else :
            print 'Gmovies copy : no copy required'
        print 'Gmovies copy : End'

        cmds.confirmDialog(title='Success', message='\n' + 'Anim Bake Finished without Errors', button='Ok',
                           messageAlign='left')

        ################check for hot reload option
        if self.hotreloadChkbox.getValue() == True:
            print
            'Hot Reload : True'
            cmds.file(newFile=True, force=True)
            cmds.file(charDetails2[5], open=True)
        else:
            print
            'Hot Reload : False'

            # print "Anim Bake Finished without Errors"


    def animBakeFn(self, *args):
        '''
            Grabbing Animbake Function from maya path 
        '''
        try:
            reload(Redeye_FBXBaker)
        except:
            import Redeye_FBXBaker
            reload(Redeye_FBXBaker)
        
        charDetails = Redeye_FBXBaker.mainBakefunction()

        #DEBUG HERE IF YOU WANT TO KNOW WHAT VARIABLES ARE EXPOSED IN CHARDETAILS
        for char in charDetails:
            print char
        '''charDetails[0~5]
        [0] fbx name full path
        [1] playblast local path
        [2] character name
        [3] character version
        [4] playblast name 
        [5] maya local path
        '''
        #after baking and playblasting, script will check the status of your UI , if UI specify copy location and checkbox is ticked, it will initiate copy of fbx and movie files. 
        #print self.copy1Path.getText() 
        #print self.copy2Path.getText()
        #print self.gmoviesPath.getText()

        #######################################FBX copy to server loop 
        print 'FBX and Maya file copy to server :-------------------'
        if self.copy1Chkbox.getValue() ==True:
            try:
                serverLoc=str(self.copy1Path.getText())
                if pm.sysFile(charDetails[0], copy=serverLoc+'/'+charDetails[2]+'/'+ charDetails[3]+'/FBX/'+charDetails[0].split("/")[-1]) == False :
                    print "FBX folder doesn't exists. Creating now.... "
                    self.makeDir(str(serverLoc+'/'+charDetails[2]+'/'+ charDetails[3]+'/FBX'))
                    pm.sysFile(charDetails[0], copy=serverLoc+'/'+charDetails[2]+'/'+ charDetails[3]+'/FBX/'+charDetails[0].split("/")[-1])
                    pm.sysFile(charDetails[5], copy=serverLoc+'/'+charDetails[2]+'/'+ charDetails[3]+"/"+charDetails[5].split("/")[-1])
                    print 'FBX and Maya file copied to %s ' % (str(serverLoc)+'/'+charDetails[2]+'/'+ charDetails[3])
                else :
                    pm.sysFile(charDetails[0], copy=serverLoc+'/'+charDetails[2]+'/'+ charDetails[3]+'/FBX/'+charDetails[0].split("/")[-1])
                    pm.sysFile(charDetails[5], copy=serverLoc+'/'+charDetails[2]+'/'+ charDetails[3]+"/"+charDetails[5].split("/")[-1])
                    print 'FBX and Maya file copied to %s ' % (str(serverLoc)+'/'+charDetails[2]+'/'+ charDetails[3])
            except :
                print "FBX Maya loop doesn't work please contact programmer"

        else : 
            print 'FBX and Maya file copy to server : no copy required'
        
        print 'FBX and Maya file copy to server: End'
        
        ######################################FBX copy to local Unity loop
        print 'FBX copy to Unity : ----------------------'
        if self.copy2Chkbox.getValue() ==True:
            try:
                unityLoc=str(self.copy2Path.getText())
                if pm.sysFile(charDetails[0], copy=unityLoc+'/'+charDetails[2]+'/'+ charDetails[3]+'/'+charDetails[0].split("/")[-1]) == False : 
                    print "Unity folder doesn't exists. Creating now.... "
                    self.makeDir(str(unityLoc+'/'+charDetails[2]+'/'+ charDetails[3]))
                    pm.sysFile(charDetails[0], copy=unityLoc+'/'+charDetails[2]+'/'+ charDetails[3]+'/'+charDetails[0].split("/")[-1])
                    print 'FBX copy to Unity : %s' % str(unityLoc + '/'+charDetails[2]+'/'+ charDetails[3])
                else:
                    pm.sysFile(charDetails[0], copy=unityLoc+'/'+charDetails[2]+'/'+ charDetails[3]+'/'+charDetails[0].split("/")[-1])
                    print 'FBX copy to Unity : %s' % str(unityLoc + '/'+charDetails[2]+'/'+ charDetails[3])
            except:
                print "Unity loop doesn't work please contact programmer"
        else :
            print 'FBX copy to Unity : no copy required'
        print 'FBX copy to Unity : End'           
        #################################### Playblast to Gmovies loop
        print 'Gmovies copy :----------------'        
        if self.gmoviesChkbox.getValue() == True:
            try:
                gmoviesLoc=str(self.gmoviesPath.getText())
                if pm.sysFile(charDetails[1], copy=gmoviesLoc+'/'+charDetails[2]+'/'+ charDetails[3] + '/'+charDetails[4]) == False:
                    print "Gmovies folder doesn't exists, Creating now.... "
                    self.makeDir(str(gmoviesLoc+'/'+charDetails[2]+'/'+ charDetails[3]))
                    pm.sysFile(charDetails[1], copy=gmoviesLoc+'/'+charDetails[2]+'/'+ charDetails[3]+ '/' + charDetails[4])
                    print 'Gmovies copied to : %s' % str(gmoviesLoc+'/'+charDetails[2]+'/'+ charDetails[3]+ '/' +charDetails[4])
                else:
                    pm.sysFile(charDetails[1], copy=gmoviesLoc+'/'+charDetails[2]+'/'+ charDetails[3]+'/'+ charDetails[4])
                    print 'Gmovies copied to : %s' % str(gmoviesLoc+'/'+charDetails[2]+'/'+ charDetails[3]+'/'+ charDetails[4])
            except :
                print "copy to Gmovies loop doesn't work please contact programmer"
        else :
            print 'Gmovies copy : no copy required'
        print 'Gmovies copy : End'

        #print "Anim Bake Finished without Errors"
        cmds.confirmDialog(title='Success', message='\n' + 'Anim Bake Finished without Errors', button='Ok',
                           messageAlign='left')
        
        ################check for hot reload option
        if self.hotreloadChkbox.getValue()==True:
            print 'Hot Reload : True'
            cmds.file(newFile=True,force=True)
            cmds.file(charDetails[5], open=True)
        else :
            print 'Hot Reload : False'        
        


    def getcopy1field(self, *args):
        '''
        getting copy1 field
        '''
        loc = self.copy1Path.getText() 
        print loc 

    def getcopy2field(self, *args):
        '''
        getting copy2 field
        '''
        loc = self.copy2Path.getText() 
        print loc 
    
    def getcopy3field(self, *args):
        '''
        getting copy2 field
        '''
        loc = self.gmoviesPath.getText() 
        print loc
            
    def animConstFn(self, *args):
        """
            Purpose: Run the animConstraint tool
        """
        try:
            reload(TIP_animConstraint)
        except:
            import TIP_animConstraint
            
        TIP_animConstraint.animConstrainDialog()
            
    
    def camShakeFn(self, *args):
        """
            Purpose: Run the camera shake tool
        """
        try:
            reload(TIP_cameraShake)
        except:
            import TIP_cameraShake
            
        TIP_cameraShake.camShakeDialog()
    
    def createCamFn(self, *args):
        """
            Purpose: Run the create camera tool
        """
        try:
            reload(TIP_createCam)
        except:
            import TIP_createCam
            
        TIP_createCam.UIMainDialog()
        
    def importAudioFn(self, *args):
        """
            Purpose: Run the import Audio tool
        """
        try:
            reload(TIP_refSound)
        except:
            import TIP_refSound
            
        TIP_refSound.UIMainDialog()
        
    def animCleanUpFn(self, *args):
        """
            Purpose: Run the Anim Clean up Tool by Pang Ren
        """
        try:
            reload(TIP_AnimCleanup)
        except:
            import TIP_AnimCleanup
            
        TIP_AnimCleanup.UIMain()        
        
    def refPlaceFn(self, *args):
        """
            Purpose: Run the Reference Placement Tool
        """
        try:
            reload(TIP_placeRef)
        except:
            import TIP_placeRef
        
        TIP_placeRef.UIMainDialog()  
        
    def libModFn (self, *args):
        """
            Purpose: Run the library Module Tool
        """
        import TIP_libraryModule
        reload(TIP_libraryModule)        
#----------------------------------------------------------------------------#
#TSM Functions

    def TSMmirror(self):
        TSMm = mel.eval('source  "Q://TD Dept//Released//MelScript//TSM//TSM2_mirrorPose.mel"')

    def TSMfkik(self):
        TSMfi = mel.eval('source  "Q://TD Dept//Released//MelScript//TSM//TSM_FKIK.mel"')

        
#----------------------------------------------------------------------------#           
    def inputTextfield(self):
        '''
        Function for shaker portion
        '''
        sel=cmds.ls(selection=True)[0]
        add=cmds.textField(self.deText, edit=True,text=str(sel))
        attr = self.populateAttr(sel)
       
    def _listCtrls(self):
        '''
        the usual list selection
        '''
        if len(cmds.ls(selection=True)) == 0:
            cmds.confirmDialog(title='Selection Error',message='\n'+'You should select something',button = 'Ok',messageAlign='left',icon = 'warning')
        elif len(cmds.ls(selection=True)) >= 1:
            return cmds.ls(selection=True)
            
    def _refreshViewport(self):
        '''
        refreshes viewport by going 1 frame forward and back
        '''
        currentFrame=cmds.currentTime(query=True)
        cmds.currentTime(currentFrame+1, edit=True)
        cmds.currentTime(currentFrame,edit=True)
        
    def timeRanger(self):
        '''
        getting the range of your selection , currently doesn't work for range that reaches the end. 
        '''
        aPlayBackSliderPython = mel.eval('$tmpVar=$gPlayBackSlider')
        Ranger=((cmds.timeControl(aPlayBackSliderPython,query=True, range=True)).replace('"',"")).split(':')
        selstRange = Ranger[0]
        selendRange = Ranger[1]
        return selstRange, selendRange
       
    def moveKeys(self,objects,selstRange,selendRange,frameChange):
        '''
        Move keys MAIN module
        '''
        for object in objects:
            cmds.keyframe(object,edit=True,relative=True,timeChange=frameChange,time=(selstRange,selendRange))
        
    def moveMaster(self):
        '''
        Move keys SUB module for integer input
        '''
        int1 = pm.intField(self.keyInt1, query = True,value=True)
        self.moveKeys(self._listCtrls(),self.timeRanger()[0],self.timeRanger()[1],int1)
    
    def moveBits(self, int):
        '''
        Move keys SUB module for shortcut buttons 
        '''
        self.moveKeys(self._listCtrls(),self.timeRanger()[0],self.timeRanger()[1],int)

# -----------------------------------------------------------------------------------------#
    def populatePr(self):
        '''
        callback the reference settings for various projects.
        '''
        'G-fighters'
        'Ladybug'
        if x.prdropdown.getValue() == 'One_Piece':
            return ("displayLayers" , "renderLayersByName")
        if x.prdropdown.getValue() == 'Disney':
            return ("displayLayers" , "renderLayersByName")

    def browseRefFn(self):
        """
            Just Browsing
        """
        try:
            outputPath = (pm.fileDialog2(caption = "Reference file" , dialogStyle=2, fileMode = 1, okCaption = "select"))[0]
            #ref = outputPath.split("/")[-1]
            self.RefListt.append(outputPath)
            self.reftextscroll.removeAll()
            for item in self.RefListt:
                short = item.split("/")[-1]
                self.reftextscroll.append(short)
            print pm.textScrollList(self.reftextscroll,query=True,allItems=True)
        except:
            pass

    def removeFn(self):
        '''
            Check reftextscroll selection, remove it from textscroll and RefListt , refresh text scroll
        '''
        toRm = pm.textScrollList(self.reftextscroll,query=True,si=True)[0]
        pm.textScrollList(self.reftextscroll,edit=True,removeItem = str(toRm))
        for item in self.RefListt:            
            if str(toRm) in item:
                self.RefListt.remove(item)
 
            
    def unloadSel(self):
        '''
        Reference TAB unload selected references
        '''
        for item in self._listCtrls():
            ref=pm.referenceQuery( item, filename=True )
            cmds.file(ref,unloadReference=True)
        #ref=pm.referenceQuery( self._listCtrls(), filename=True )
        #cmds.file(ref,unloadReference=True)
        
    def appendtoReflist(self,fileloc):
        '''
        browse file and add selected into the self.reftextscroll
        '''        
        
        multipleFilters = "Maya Files (*.ma *.mb);;Maya ASCII (*.ma);;Maya Binary (*.mb)"
        #self.RefListt.append(fileloc)
        cmds.textScrollList(self.reftextscroll,e=1,append=fileloc)
        #RefListt.append(cmds.fileDialog2(caption='Select Reference',dialogStyle=2,okc='Select',fileFilter=multipleFilters))

    def loadAllRef(self):
        '''
        for item in self.reftextscroll , load ref
        '''
        sharedNodeArray = self.populatePr()
        for ref in self.RefListt:
            fileName= os.path.basename(ref).split('.')[0] 
            cmds.file(ref, groupLocator = True , reference = True, returnNewNodes = True, loadReferenceDepth = "all",  sharedNodes = sharedNodeArray, mergeNamespacesOnClash = False, namespace = fileName, options = "v=0")
        self.RefListt = []
        self.reftextscroll.removeAll()
        
# -----------------------------------------------------------------------------------------#
    
    def browsePbFn(self, *args):
        """
            Just Browsing pb
        """
        '''try:
            reload(TIP_playblast_noUI)
            from TIP_playblast_noUI import browseRefFn

        except:
            import TIP_playblast_noUI
            
        x=TIP_playblast_noUI()
        x.browseRefFn'''
        outputPath = pm.fileDialog2(caption = "Directory to store Playblast" , dialogStyle=2, fileMode = 0, okCaption = "Select")
        outputPathStr = str(outputPath[0]).split('.')[0]
        pm.textField(self.outputPath,edit = True, text = outputPathStr)
        
        
        
    def playBlastFn(self, *args):
        """
            Purpose: create playblast with additional frame at the back
        """
        #--- frame range ---
        minTime = pm.playbackOptions(query=True, minTime=True)
        maxTime = pm.playbackOptions(query=True, maxTime=True)
        
        #--- output file path ---
        selPath = pm.textField(self.outputPath, query = True, text = True)
        fileNamePath = str(selPath.split('.')[0])
        
        #--- sound in PlayBlast ---
        soundNode = None
        soundFile = None
        soundArray = pm.ls(type="audio")
        if soundArray != []:
            soundFile = soundArray[-1]
        if soundFile != None:
            soundNode = pm.PyNode(soundFile)
                
        #--- grab current resolution ---
        currentRen = pm.Attribute('defaultRenderGlobals.ren').get()
        renWidth = 1280 # default values just in case
        renHeight = 720 # default values just in case
        
        if currentRen == 'mayaSoftware':
            renWidth = pm.PyNode('defaultResolution').width.get()
            renHeight = pm.PyNode('defaultResolution').height.get()
        elif currentRen == 'vray':
            renWidth = pm.PyNode('vraySettings').width.get()
            renHeight = pm.PyNode('vraySettings').height.get()
        
        #--- Tear Off Current Panel ---
        currPanel = pm.getPanel(withFocus = True)
        playBlastEditor = pm.modelPanel(tearOffCopy = currPanel, modelEditor = True)
        
        #--- window should be shaded mode ---
        if (self.shadedChk.getValue() == True):
            pm.modelEditor(playBlastEditor.getModelEditor(), edit = True, displayAppearance = "smoothShaded", displayTextures = True, wireframeOnShaded = False)
                
        #--- set the window's display settings ---
        pm.modelEditor(playBlastEditor.getModelEditor(), edit = True, allObjects = 0) # off everything first
        
        pm.modelEditor(playBlastEditor.getModelEditor(), edit = True, nurbsSurfaces = 1) # nurbs surfaces
        pm.modelEditor(playBlastEditor.getModelEditor(), edit = True, polymeshes = 1) # polygons
        pm.modelEditor(playBlastEditor.getModelEditor(), edit = True, subdivSurfaces = 1) # subdiv surfaces
        pm.modelEditor(playBlastEditor.getModelEditor(), edit = True, clipGhosts = 1) # clip ghosts
        pm.modelEditor(playBlastEditor.getModelEditor(), edit = True, hud = 1) # HUD
        
        #--- set new model editor as focus ---
        pm.setFocus(playBlastEditor.getModelEditor())
        pm.modelEditor(playBlastEditor.getModelEditor(),  edit = True, activeView = 1)
        
        #**********************************************
        #--- close quicktime file if it is open ---
        #--- Currently don't know how to do ---
        #**********************************************
        
        #--- Clear selection ---
        pm.select(clear = True) # So got no selection highlights in playblast
        
        #--- compile command string ---
        try: # have to use try catch because sound node maybe available but not at the specified timings. This will make the script throw an error
            if (self.soundChk.getValue() == True) and (soundNode != None) : # might not want sound even though there is sound
                cmdStr = 'pm.playblast(offScreen = 1, forceOverwrite = 1, sequenceTime = 0, widthHeight = (' + str(renWidth) + ', ' + str(renHeight) + ') ,fp = 4, startTime = ' + str(minTime) + ', endTime = (' + str(maxTime) + ' + 1), filename = "' + str(fileNamePath) + '", format = "qt", percent = 50 , compression = "Sorenson Video 3", quality = 70, clearCache = 0, viewer = 1, showOrnaments = 1, sound = "' + str(soundNode) + '")'
            else:
                cmdStr = 'pm.playblast(offScreen = 1, forceOverwrite = 1, sequenceTime = 0, widthHeight = (' + str(renWidth) + ', ' + str(renHeight) + ') ,fp = 4, startTime = ' + str(minTime) + ', endTime = (' + str(maxTime) + ' + 1), filename = "' + str(fileNamePath) + '", format = "qt", percent = 50 , compression = "Sorenson Video 3", quality = 70, clearCache = 0, viewer = 1, showOrnaments = 1)'
                
            pm.evalDeferred(cmdStr)

        except:
            cmdStr = 'pm.playblast(offScreen = 1, forceOverwrite = 1, sequenceTime = 0, widthHeight = (' + str(renWidth) + ', ' + str(renHeight) + ') ,fp = 4, startTime = ' + str(minTime) + ', endTime = (' + str(maxTime) + ' + 1), filename = "' + str(fileNamePath) + '", format = "qt", percent = 50 , compression = "Sorenson Video 3", quality = 70, clearCache = 0, viewer = 1, showOrnaments = 1)'
            pm.evalDeferred(cmdStr)
        
        #--- close playblast window ---
        playBlastWindow = playBlastEditor.window()
        closeCmdStr = 'pm.deleteUI("' + str(playBlastWindow) + 'Window' + '")' # deletes the actual window
        pm.evalDeferred(closeCmdStr, lowestPriority = True)

# -----------------------------------------------------------------------------------------#

    def parCheckboxCkr(self):
        '''
        check self.prx pry prz checkboxes 
        '''
        holdingList = []
        if self.prx.getValue() == False :
            holdingList.append(self.prx.getLabel())
            
        if self.pry.getValue() == False :
            holdlingList.append(self.pry.getLabel())
        
        if self.prz.getValue() == False :
            holdingList.append(self.prz.getLabel())    
        return holdingList
        
    def snappingParent(self):
        '''
        snaps to parent on command
        '''
        skipped = self.parCheckboxCkr()
        parentObj = self._listCtrls()[0]
        
        if len(cmds.ls(selection=True))>=2:
            for i in range(1,len(cmds.ls(selection=True))):
                childObj = self._listCtrls()[i]
                const=cmds.parentConstraint(parentObj,childObj,maintainOffset=False,skipRotate=skipped,skipTranslate=skipped)
                cmds.select(childObj)
                cmds.setKeyframe()
                cmds.delete(const)
                cmds.deleteAttr(childObj, at='blendOrient1') # need to make this dynamic    

    def transCheckboxCkr(self):
        '''
        transSnap button checks the below values and executes function
        '''
        holdingList =[]
        if self.px.getValue() == False :
            holdingList.append(self.prx.getLabel())
            
        if self.py.getValue() == False :
            holdingList.append(self.pry.getLabel())
        
        if self.pz.getValue() == False :
            holdingList.append(self.prz.getLabel())    
        return holdingList

    def snappingTrans(self):
        '''
        translate Snapping On Command
        '''
        skipped=self.transCheckboxCkr()
        parentObj = self._listCtrls()[0]
        
        if len(cmds.ls(selection=True))>=2:
            for i in range(1,len(cmds.ls(selection=True))):
                childObj = self._listCtrls()[i]
                const=cmds.parentConstraint(parentObj,childObj,maintainOffset=False,skipRotate=['x','y','z'],skipTranslate=skipped)
                cmds.select(childObj)
                cmds.setKeyframe()
                cmds.delete(const)
                cmds.deleteAttr(childObj, at='blendOrient1') # need to make this dynamic

    def rotCheckboxCkr(self):
        '''
        rotateSnap button checks the below values and executes function
        '''
        holdingList =[]
        if self.ox.getValue() == False :
            holdingList.append(self.px.getLabel())
            
        if self.oy.getValue() == False :
            holdlingList.append(self.py.getLabel())
        
        if self.oz.getValue() == False :
            holdingList.append(self.pz.getLabel())    
        return holdingList

    def snappingRot(self):
        '''
        rotate Snapping On Command
        '''
        skipped=self.rotCheckboxCkr()
        parentObj = self._listCtrls()[0]
        
        if len(cmds.ls(selection=True))>=2:
            for i in range(1,len(cmds.ls(selection=True))):
                childObj = self._listCtrls()[i]
                const=cmds.parentConstraint(parentObj,childObj,maintainOffset=False,skipRotate=skipped,skipTranslate=['x','y','z'])
                cmds.select(childObj)
                cmds.setKeyframe()
                cmds.delete(const)
                cmds.deleteAttr(childObj, at='blendOrient1') # need to make this dynamic 
#---------------------------------------------------------#
    def _getPosition(self,obj):
        ''' return 2 arrays worldspace position and rotation'''
        return [cmds.xform(obj, query=True, rotatePivot = True, ws = True), cmds.xform(obj,query=True, rotation = True, ws=True)]
    
    def makingLocator(self): 

        #Step 1 make a locator that is in the exact location as the Target.
        if len(self._listCtrls()) == 1:
            selection = self._listCtrls()
            worldTrans = self._getPosition(selection)[0]
            worldRot = self._getPosition(selection)[1]
            
            #create locator in some position
            theLocator = cmds.spaceLocator(n='prAwesomeLocator'+str(self.locCounter))[0]
            #print theLocator
            cmds.setAttr(theLocator+'.translate',worldTrans[0],worldTrans[1],worldTrans[2],type = 'double3')
            cmds.setAttr(theLocator+'.rotate',worldRot[0],worldRot[1],worldRot[2],type = 'double3')
            #DaLocator.append(selection)
            self.locCounter +=1
            self.DaLocator.append(theLocator) 
            self.CurrentSelection = selection
                    
        else:
            cmds.confirmDialog(title='Error dialog', message='Please Select 1 Target to Stick', messageAlign='left',button='Ok', defaultButton='Ok', dismissString='Ok', icon='warning')
    
    def stickitfront(self):
        #Step 2 parent constraint and remove , the parent constraint then move one frame forward.
        #So the idea is click this as many times as you need to stick the foot
        
        theConstraint = cmds.parentConstraint ( self.DaLocator[-1], self.CurrentSelection , n ='myConstraint_parent',mo=False )[0]
        currentFrame = cmds.currentTime(query=True)
        cmds.setKeyframe (self.CurrentSelection)
        cmds.currentTime( currentFrame+1 , edit = True)#switched the order, so it keys first before moving on to next frame
        cmds.delete(theConstraint)
    
    def stickitback(self):
    
        theConstraint = cmds.parentConstraint ( self.DaLocator[-1], self.CurrentSelection , n ='myConstraint_parent',mo=False )[0]
        currentFrame = cmds.currentTime(query=True)
        cmds.setKeyframe (self.CurrentSelection)
        cmds.currentTime( currentFrame-1 , edit = True)#switched the order, so it keys first before moving on to next frame
        cmds.delete(theConstraint)
    
    def deleteLoc(self):
        '''the unfortunate consequence of creating a locator is the need to delete it. '''
                
        if len(self.DaLocator) == 0:
            cmds.confirmDialog(title='No Snap Locators', message="There are no Snap locators to delete", messageAlign='left',
                    button='Ok', defaultButton='Ok', dismissString='Ok', icon='warning')
        else :
            for items in self.DaLocator :
                cmds.delete(items)
        self.DaLocator=[]
        self.locCounter=0
    
    def checkLocators(self):
        '''checking for any locators with the name 'prAwesomeLocatorXX'. ''' 
            
        locX = cmds.ls('prAwesomeLocator*',type='locator')##works
        for items in locX :
            self.DaLocator.append(cmds.listRelatives(items, parent = True)[0])

    
# -----------------------------------------------------------------------------------------#
    def _getOffset(self):
        transOffset = (self.shiftytx.getValue(),self.shiftyty.getValue(),self.shiftytz.getValue())
        return transOffset        

    def _getTimeRange(self):
        timerange =  (self.timeSt.getValue(),self.timeEnd.getValue())
        return timerange

    def _checkindexLen(self,object,translate):
        '''
        just checking if the selected object's 
        '''
        

    def loadShifty(self):
        '''
        selected items get loaded into shiftytextscroll
        '''
        listlen = self.shiftytextscroll.getNumberOfItems()
        sel = self._listCtrls()
        #self.shiftytextscroll.removeAll()
        if listlen == 0:
            for s in sel:
                #self.ShiftList.append(s)
                pm.textScrollList(self.shiftytextscroll,e=1,append=s)
                #self.shiftytextscroll.append(s)
        if listlen >= 1:
            currentList = self.shiftytextscroll.getAllItems()
            #check for repeated items and skip if item selected is repeated.
            for s in sel:
                if s in currentList:
                    print s , 'is in shift list --- Skipped Append'
                else :
                    pm.textScrollList(self.shiftytextscroll,e=1,append=s)
                    
        print self.shiftytextscroll.getNumberOfItems()

    def removeShifty(self):
        '''
        removing items from clear shiftytextscroll
        '''
        self.shiftytextscroll.removeItem(self.shiftytextscroll.getSelectItem())

    def shiftynew(self,object,transOffset,timeRange):
        '''
        running proceedure #x.shiftynew('pCube1',x._getOffset(),x._getTimeRange())
        '''
        #print transOffset , timeRange
        
        
    
    def shifty(self,object,v1,v2,v3,range1,range2): 
        if v1 !=0:
            objTrans = cmds.keyframe( object+'.translateX', time=(range1,range2),relative=True, query=True, valueChange=True)
            objTime = cmds.keyframe( object,at='tx', q=True,time=(range1,range2), tc=True )
            print objTrans , objTime
            print len(objTrans), len(objTime)
            #check number of items in objTime and objTrans
            if len(objTrans) == len(objTime):
                for i in range(0,len(objTrans)):
                    cmds.setKeyframe(object, attribute='translateX', t=objTime[i],value=objTrans[i]+v1)
            else : 
                print 'TranslateX index break'
        else :
            print 'TranslateX skipped'
                    
        if v2 !=0:
            objTrans = cmds.keyframe( object+'.translateY', time=(range1,range2),relative=True, query=True, valueChange=True)
            objTime = cmds.keyframe( object,at='ty', q=True, time=(range1,range2),tc=True )
            print objTrans , objTime
            print len(objTrans), len(objTime)
            #check number of items in objTime and objTrans
            if len(objTrans) == len(objTime):
                for i in range(0,len(objTrans)):
                    cmds.setKeyframe(object, attribute='translateY', t=objTime[i],value=objTrans[i]+v2)
            else : 
                print 'TranslateY index break'
        else :
            print 'translateY skipped'
        
        if v3 !=0:
            objTrans = cmds.keyframe( object+'.translateZ', time=(range1,range2),relative=True, query=True, valueChange=True)
            objTime = cmds.keyframe( object,at='tz', q=True,time=(range1,range2), tc=True )
            print objTrans , objTime
            print len(objTrans), len(objTime)
            #check number of items in objTime and objTrans
            if len(objTrans) == len(objTime):
                for i in range(0,len(objTrans)):
                    cmds.setKeyframe(object, attribute='translateZ', t=objTime[i],value=objTrans[i]+v3)
            else : 
                print 'TranslateZ index break'
          
        else :
            print 'translateZ skipped'

        
    def runShiftySelected(self):
        v1 = pm.floatField(self.shiftytx, query = True,value=True)
        v2 = pm.floatField(self.shiftyty, query = True,value=True)
        v3 = pm.floatField(self.shiftytz, query = True,value=True)
        range1 = pm.intField(self.timeSt, query = True,value=True)
        range2 = pm.intField(self.timeEnd, query=True, value=True)
        for item in self.shiftytextscroll.getAllItems():            
            self.shifty(item,v1,v2,v3,range1,range2)
        self._refreshViewport()
# -----------------------------------------------------------------------------------------#

    def browseServFn(self, *args):
        pathholder = pm.fileDialog2(caption = "Character Directory" , dialogStyle=2, fileMode = 2, okCaption = "Select")
        
        pm.textField(self.copy1Path,edit = True, text = str(pathholder[0]))
        
    def browseUnityFn(self,*args):
        pathholder = pm.fileDialog2(caption = "Unity Character Directory" , dialogStyle=2, fileMode = 2, okCaption = "Select")
        pm.textField(self.copy2Path,edit = True, text = str(pathholder[0]))
        
    def browseGmoviesFn(self,*args):
        pathholder = pm.fileDialog2(caption = "Gmovies Character Directory" , dialogStyle=2, fileMode = 2, okCaption = "Select")
        pm.textField(self.gmoviesPath,edit = True, text = str(pathholder[0]))        

    def fileCheckFn(self,*args):
        """So we're going to use filecheck to catch the next Animbake function. If CHA in character ID then we execute A animbake
         if not exceute B animbake."""

        filename = os.path.basename(pm.system.sceneName())
        if 'CHA' in filename.split("_")[0]:
            self.charID.setLabel(filename.split("_")[0])
            self.fileName.setLabel(filename)
            self.cycleName.setLabel(filename.split("_")[1].split("@")[1])
            self.charName.setLabel(filename.split("_")[1].split("@")[0])
        else :
            char = Redeye_FBXBaker.filenameManager()
            self.charID.setLabel('NO ID')
            self.fileName.setLabel(char[6])
            self.charName.setLabel(char[4])
            self.cycleName.setLabel(char[6].split("_")[-2])

        #print filename
        #self.fileName = pm.text('<curent filename>')
        #self.charID = pm.text('<CHAxxx>')
        #self.charName = pm.text('<Name>')
        #self.cycleName = pm.text('<Cycle>')
        #self.verName = pm.text('<00>')
        #self.fileType = pm.text('NEW/OLD')


x=UIMain()
#print x.unityPath.getText()
#x.shiftynew('pCube1',x._getOffset(),x._getTimeRange())

 
