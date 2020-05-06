import maya.cmds as cmds
import pymel.core as pm
import maya.mel as mel
import random
import os
import sys
import subprocess 

PLAYER = 'pl_'
MOB = 'mob_'
BOSS = 'bs_'
fbxFolder='FBX'
fbxExt='.fbx'



def listCtrls():
    '''
    the usual list selection
    '''
    if len(cmds.ls(selection=True)) == 0  :
        cmds.confirmDialog(title='Selection Error',message='\n'+'You should select something',button = 'Ok',messageAlign='left',icon = 'warning')
    if len(cmds.ls(selection=True)) > 1  :
        cmds.confirmDialog(title='Selection Error',message='\n'+'You should select one thing',button = 'Ok',messageAlign='left',icon = 'warning')
    elif len(cmds.ls(selection=True)) == 1:
        return cmds.ls(selection=True)

def filenameManager():
    '''
    eg for character file D:/[Project]/14_Disney/DisneyProject/scenes/pl_donald/01_original/pl_donald01_original_flinch_02.ma
    output 
    [0] filepath : D:/[Project]/14_Disney/DisneyProject/scenes/pl_donald/01_original
    [1] fbx export filename  : pl_donald01_original@flinch
    [2] file extension : ma
    [3] iteration : 02
    [4] characterName : pl_donald
    [5] characterVersion : 01_original
    [6] playblast filename : pl_donald01_original_flinch_02
    '''
    
    filename=os.path.basename(pm.system.sceneName())
    fileExt=os.path.splitext(pm.system.sceneName())[1]
    fileloc=os.path.dirname(pm.system.sceneName())
        
    #For character Name [4]
    characterName=filename.split(fileExt)[0].split("_")[0]+'_'+filename.split(fileExt)[0].split("_")[1]
    characterVersion = characterName[-2:]
    characterName=characterName[:-2]
    characterVersion = characterVersion + '_'+ filename.split("_")[2]
 
    print 'Character is : %s' % characterName
    
    #if "pl_" or "mob_" or "bs_" in characterVersion:
    #    characterVersion = "01_original"
    #    print 'Charcter Version : %s' % characterVersion
    print 'Charcter Version : %s' % characterVersion
    
    fileIteration = filename.split(fileExt)[0].split("_")[-1]
    #knockout the iteration from filename.
    filenameList = filename.split(fileExt)[0].split("_")
    playblastName = '_'.join(filenameList)   
    del filenameList[-1]
    
    filenameList[2] = filenameList[2]+'@'+filenameList[3]
    del filenameList[-1]
    
    ExportFilename='_'.join(filenameList)

    return fileloc, ExportFilename, fileExt, fileIteration, characterName, characterVersion , playblastName


def filenameManager2():
    '''
    eg for character file G:/My Drive/goGame 3D Team (SG+MY)/Galaxy/Art/3D/Character Animation/CHA007_skeletonspear/Raw/scenes/CHA007_skeletonspear@idlefreeze_01.ma
    output
    [0] filepath : G:/My Drive/goGame 3D Team (SG+MY)/Galaxy/Art/3D/Character Animation/CHA007_skeletonspear/Raw/scenes'
    [1] fbx export filename  : CHA007_skeletonspear@idlefreeze
    [3] iteration : 02
    [4] characterName : skeletonspear
    [5] characterID : CHA007
    [6] playblast filename : CHA007_skeletonspear@idlefreeze_01
    [7] fbx location is here : G:/My Drive/goGame 3D Team (SG+MY)/Galaxy/Art/3D/Character Animation/CHA007_skeletonspear/CHA007
    '''

    filename = os.path.basename(pm.system.sceneName())
    fileExt = os.path.splitext(pm.system.sceneName())[1]
    fileloc = os.path.dirname(pm.system.sceneName())
    fileSplit = filename.split(fileExt)[0].split("_")
    fileIteration = fileSplit[-1]
    characterID = fileSplit[0]
    characterName, cycleName = fileSplit[1].split("@")[0], fileSplit[1].split("@")[1]

    print
    'Character ID : %s \nCharacter Name : %s' % (characterID, characterName)

    playblastName = '_'.join(fileSplit)
    ExportFilename = '_'.join(fileSplit[0:2])
    fileloclist = fileloc.split("/")
    fbxLocation = '/'.join(fileloclist[:8]) + '/' + characterID

    return fileloc, ExportFilename, fileExt, fileIteration, characterName, characterID, playblastName, fbxLocation


def makeDir(path):
    """
    input a path to check if it exists, if not, it creates all the path
    :return: path string
    """
    if not os.path.exists(path):
        os.makedirs(path)

def exportFBX(file1):
    try :
        return pm.system.exportSelected(file1[0]+'/'+fbxFolder+"/"+file1[1]+fbxExt, force = 1)
    except :
        print "fbx folder doesn't exist, creating now... "
        makeDir(file1[0]+'/'+fbxFolder)
        try :
            return pm.system.exportSelected(file1[0]+'/'+fbxFolder+"/"+file1[1]+fbxExt,force = 1)
        except :
            cmds.confirmDialog(title='Error dialog', message='Something is amiss FBX Export failed', messageAlign='left',button='Ok', defaultButton='Ok', dismissString='Ok', icon='warning')
            print "FBX Export failed" 

def _getPlaybackTimeRange():
    '''
    get playback time range
    '''
    AnimSt=cmds.playbackOptions( animationStartTime=True,query=True )
    AnimEnd= cmds.playbackOptions(animationEndTime=True,query=True )
    return AnimSt, AnimEnd


def _cleanupNamespace():
    '''
    find the reference, import it,
    finds the prefix of the reference and cleans up the namespace 
    '''
    for item in listCtrls():
        pre=str(listCtrls()[0])
        prefix = pre.rsplit(":")[0]
        
        print 'Cleaning up file : RIG is %s' % prefix
        ref=cmds.referenceQuery( item, filename=True )
        cmds.file(ref,importReference=True)
        cmds.namespace(mv=(prefix,":"),force=True)
        cmds.namespace(rm = prefix)
        print "Cleaning up file : namespace deleted and cleaned up"

def bakeJntMesh():
    #rest of bake fn
    allObjects = cmds.ls(l=True)
    jointsOnly=[]
    meshy=[]
    cmds.select(clear = True)
    
    for obj in allObjects:
       if cmds.nodeType(obj) == 'joint':
           jointsOnly.append(obj)
           #cmds.setAttr((str(obj)+".segmentScaleCompensate"), 0)
    
    #cmds.bakeSimulation(jointsOnly, t=(AnimSt,AnimEnd),at=["rx","ry","rz","tx","ty","tz","sx","sy","sz"])
    cmds.bakeResults(jointsOnly,simulation=True, t=(_getPlaybackTimeRange()[0],_getPlaybackTimeRange()[1]),at=["rx","ry","rz","tx","ty","tz","sx","sy","sz"])
   
    cmds.select(clear = True)
    cmds.select(cmds.listRelatives(cmds.ls(type='mesh'),type='transform',p=True))
    cmds.bakeResults(t=(_getPlaybackTimeRange()[0],_getPlaybackTimeRange()[1]),at=["visibility"])
    
    #finish baking
    #now search for correct items and add it to your selction.
    cmds.select(clear = True)
    #check for model_root
    if cmds.objExists('model_root') == True :
        cmds.select('model_root')
        cmds.select(hi=True)
        cmds.select('model_root',d=True)
        #enable line below for 2019 characters
        cmds.select('world_jnt', hi=True,tgl=True)
        
        #enable line below for old characters.
        #cmds.select(jointsOnly,add=True)
        #cmds.confirmDialog(title='Success',message='\n'+'Bake Successful! Yay!',button = 'Ok',messageAlign='left',icon = 'information')
    
   
    else:
        cmds.confirmDialog(title='Selection Error',message='\n'+'model_root / model_root_fix doesnt exists',button = 'Ok',messageAlign='left',icon = 'warning')


def bakeJntMesh2():
    # rest of bake fn
    allObjects = cmds.ls(l=True)
    jointsOnly = []
    meshy = []
    cmds.select(clear=True)

    for obj in allObjects:
        if cmds.nodeType(obj) == 'joint':
            jointsOnly.append(obj)
            # cmds.setAttr((str(obj)+".segmentScaleCompensate"), 0)

    # cmds.bakeSimulation(jointsOnly, t=(AnimSt,AnimEnd),at=["rx","ry","rz","tx","ty","tz","sx","sy","sz"])
    cmds.bakeResults(jointsOnly, simulation=True, t=(_getPlaybackTimeRange()[0], _getPlaybackTimeRange()[1]),
                     at=["rx", "ry", "rz", "tx", "ty", "tz", "sx", "sy", "sz"])

    #cmds.select(clear=True)
    #cmds.select(cmds.listRelatives(cmds.ls(type='mesh'), type='transform', p=True))
    #cmds.bakeResults(t=(_getPlaybackTimeRange()[0], _getPlaybackTimeRange()[1]), at=["visibility"])

    # finish baking
    # now search for correct items and add it to your selction.
    cmds.select(clear=True)
    # check for model_root
    for obj in allObjects:
        if 'model_root_old' in obj:
            try:
                cmds.delete(obj)
            except:
                pass
        if 'world_jnt_old' in obj:
            try:
                cmds.delete(obj)
            except:
                pass

    pm.mel.source('cleanUpScene')
    pm.mel.scOpt_performOneCleanup({
        'setsOption',
        'transformOption',
        'displayLayerOption',
        'renderLayerOption',
        'animationCurveOption',
        'nurbsSrfOption',
        'partitionOption',
        'animationCurveOption',
        'deformerOption',
        'unusedSkinInfsOption',
        'brushOption',
        'shaderOption',
        'pbOption',
        'ptConOption',
        'groupIDnOption',
        'snapshotOption',
        'unitConversionOption',
        'referencedOption',
        'brushOption',
        'shadingNetworksOption'
    }
    )



    if cmds.objExists('model_root') == True:
        cmds.select('model_root')
        cmds.select(hi=True)
        cmds.select('model_root', d=True)
        # enable line below for 2019 characters
        cmds.select('world_jnt', hi=True, tgl=True)

        # enable line below for old characters.
        # cmds.select(jointsOnly,add=True)
        # cmds.confirmDialog(title='Success',message='\n'+'Bake Successful! Yay!',button = 'Ok',messageAlign='left',icon = 'information')


    else:
        cmds.confirmDialog(title='Selection Error', message='\n' + 'model_root / model_root_fix doesnt exists',
                           button='Ok', messageAlign='left', icon='warning')

def bakeJntsOnly():
    # rest of bake fn
    allObjects = cmds.ls(l=True)
    jointsOnly = []
    meshy = []
    cmds.select(clear=True)

    for obj in allObjects:
        if cmds.nodeType(obj) == 'joint':
            jointsOnly.append(obj)
            # cmds.setAttr((str(obj)+".segmentScaleCompensate"), 0)

    # cmds.bakeSimulation(jointsOnly, t=(AnimSt,AnimEnd),at=["rx","ry","rz","tx","ty","tz","sx","sy","sz"])
    cmds.bakeResults(jointsOnly, simulation=True, t=(_getPlaybackTimeRange()[0], _getPlaybackTimeRange()[1]),
                     at=["rx", "ry", "rz", "tx", "ty", "tz", "sx", "sy", "sz"])

    cmds.select(clear=True)
    for obj in allObjects:
        if 'model_root' in obj:
            try:
                cmds.delete(obj)
            except:
                pass
        if 'world_jnt_old' in obj:
            try:
                cmds.delete(obj)
            except:
                pass
        if 'world_ctrl_grp' in obj:
            try:
                cmds.delete(obj)
            except:
                pass

    pm.mel.source('cleanUpScene')

    pm.mel.scOpt_performOneCleanup({
        'setsOption',
        'transformOption',
        'displayLayerOption',
        'renderLayerOption',
        'animationCurveOption',
        'nurbsSrfOption',
        'partitionOption',
        'animationCurveOption',
        'deformerOption',
        'unusedSkinInfsOption',
        'brushOption',
        'shaderOption',
        'pbOption',
        'ptConOption',
        'groupIDnOption',
        'snapshotOption',
        'unitConversionOption',
        'referencedOption',
        'brushOption',
        'shadingNetworksOption'
    }
    )

    # finish baking
    # now search for correct items and add it to your selction.
    cmds.select(clear=True)
    # check for model_root
    if cmds.objExists('world_jnt') == True:
        cmds.select('world_jnt', d=True)
        # enable line below for 2019 characters
        cmds.select('world_jnt', hi=True, tgl=True)

        # enable line below for old characters.
        # cmds.select(jointsOnly,add=True)
        # cmds.confirmDialog(title='Success',message='\n'+'Bake Successful! Yay!',button = 'Ok',messageAlign='left',icon = 'information')


    else:
        cmds.confirmDialog(title='Selection Error', message='\n' + 'model_root / model_root_fix doesnt exists',
                           button='Ok', messageAlign='left', icon='warning')

def selectMainRef():
    cmds.select( clear=True )
    correctNode=[]
    allnurbs=cmds.listRelatives(cmds.ls(type='nurbsCurve'),p=True)
    for nurb in allnurbs:
        if str.lower(str(nurb.split(":")[-1])) == 'world_ctrl':
            cmds.select(nurb)      
    correctNode=cmds.ls(selection=True)
    return correctNode[0]
    

def muteWorld(world):
    cmds.currentTime(1)
    cmds.mute(str(world)+'.translateZ')
    cmds.mute(str(world)+'.translateX')
    cmds.mute(str(world)+'.translateY')        
    cmds.mute(str(world)+'.rotateZ')   
    cmds.mute(str(world)+'.rotateX')
    cmds.mute(str(world)+'.rotateY')  
        
def createPlayblast(filename1):
    
    #search for local movies folder
    #moviesFolder=pm.workspace(query=True, active=True)+'/movies/'+filename1[4]+'/'+filename1[5]+'/'
    moviesFolder=pm.workspace(query=True, active=True)+'/movies/'
    print 'Playblast location is : ' + moviesFolder
    panelnow=cmds.getPanel(wf=True)
    cmds.modelEditor(panelnow, e=1, displayLights='default',cme=False)
    thingstoHide = ['nurbsCurves', 'joints','motionTrails','locators','ikHandles']
    # for loop to check through all 4 items on top. 
    for thing in thingstoHide:
        kwargs = {'query': True, thing: True}
        thingCheck = cmds.modelEditor(panelnow, **kwargs)
        if thingCheck == True :
            kwargs = {'edit': True, thing: False}
            cmds.modelEditor(panelnow, **kwargs)
        else :
            print "Playblast : %s is already hidden " % thing    
    
    return pm.playblast(format='qt',cc=True,filename=moviesFolder+filename1[6],fo=True,percent=100,compression='H.264',quality=100,width=960,height=540)
    #except :
        #cmds.confirmDialog(title='Error',message='\n'+'Playblast creation error+'\n, button = 'Ok',messageAlign='left',icon = 'information')

def mainBakefunction():
    '''
    compile all scripts bake all meshes and joints of related reference.
    clean up namespace

    '''
    file2=filenameManager()
    pbloc=createPlayblast(file2)
    muteWorld(selectMainRef())
    cmds.select( clear=True )
    selectMainRef()
    _cleanupNamespace()
    bakeJntMesh()
    fbxName = exportFBX(file2)
    #cmds.confirmDialog(title='Success',message='\n'+'FBX Export Successful! Yay!'+'\n'+fbxName+'\n'+'Playblast Successful'+'\n'+ pbloc , button = 'Ok',messageAlign='left',icon = 'information')
    #tentatively integrated like crap here
    #cmds.file(newFile=True,force=True)
    #fileReopen = cmds.file(str(file2[0]+'/'+file2[6]+file2[2]), open=True)
    #cmds.file(newFile=True,force=True)
    mayaFileReopen = str(file2[0]+'/'+file2[6]+file2[2])

    print '###########################'
    #print fbxName, pbloc, file2[4], file2[5], file2[6]+'.mov' , mayaFileReopen
    return fbxName, pbloc, file2[4], file2[5], file2[6]+'.mov', mayaFileReopen


def mainBakefunction2():
    '''
    compile all scripts bake all meshes and joints of related reference.
    clean up namespace

    '''
    file3 = filenameManager2()
    pbloc = createPlayblast(file3)
    muteWorld(selectMainRef())
    cmds.select(clear=True)
    selectMainRef()
    _cleanupNamespace()
    bakeJntMesh()
    fbxName = exportFBX(file3)
    # cmds.confirmDialog(title='Success',message='\n'+'FBX Export Successful! Yay!'+'\n'+fbxName+'\n'+'Playblast Successful'+'\n'+ pbloc , button = 'Ok',messageAlign='left',icon = 'information')
    # tentatively integrated like crap here
    # cmds.file(newFile=True,force=True)
    # fileReopen = cmds.file(str(file2[0]+'/'+file2[6]+file2[2]), open=True)
    # cmds.file(newFile=True,force=True)
    mayaFileReopen = str(file3[0] + '/' + file3[6] + file3[2])


    print '###########################'
    # print fbxName, pbloc, file2[4], file2[5], file2[6]+'.mov' , mayaFileReopen
    return fbxName, pbloc, file3[4], file3[5], file3[6] + '.mov', mayaFileReopen

def mainBakefunction3():
    '''
    compile all scripts bake all meshes and joints of related reference.
    clean up namespace

    '''
    file3 = filenameManager2()
    pbloc = createPlayblast(file3)
    muteWorld(selectMainRef())
    cmds.select(clear=True)
    selectMainRef()
    _cleanupNamespace()
    bakeJntMesh2()
    fbxName = exportFBX(file3)
    # cmds.confirmDialog(title='Success',message='\n'+'FBX Export Successful! Yay!'+'\n'+fbxName+'\n'+'Playblast Successful'+'\n'+ pbloc , button = 'Ok',messageAlign='left',icon = 'information')
    # tentatively integrated like crap here
    # cmds.file(newFile=True,force=True)
    # fileReopen = cmds.file(str(file2[0]+'/'+file2[6]+file2[2]), open=True)
    # cmds.file(newFile=True,force=True)
    mayaFileReopen = str(file3[0] + '/' + file3[6] + file3[2])


    print '###########################'
    # print fbxName, pbloc, file2[4], file2[5], file2[6]+'.mov' , mayaFileReopen
    return fbxName, pbloc, file3[4], file3[5], file3[6] + '.mov', mayaFileReopen
def mainBakefunction4():
    '''
    compile all scripts bake ONLY joints of related reference.
    clean up namespace

    '''
    file3 = filenameManager2()
    pbloc = createPlayblast(file3)
    muteWorld(selectMainRef())
    cmds.select(clear=True)
    selectMainRef()
    _cleanupNamespace()
    bakeJntsOnly()
    fbxName = exportFBX(file3)
    # cmds.confirmDialog(title='Success',message='\n'+'FBX Export Successful! Yay!'+'\n'+fbxName+'\n'+'Playblast Successful'+'\n'+ pbloc , button = 'Ok',messageAlign='left',icon = 'information')
    # tentatively integrated like crap here
    # cmds.file(newFile=True,force=True)
    # fileReopen = cmds.file(str(file2[0]+'/'+file2[6]+file2[2]), open=True)
    # cmds.file(newFile=True,force=True)
    mayaFileReopen = str(file3[0] + '/' + file3[6] + file3[2])


    print '###########################'
    # print fbxName, pbloc, file2[4], file2[5], file2[6]+'.mov' , mayaFileReopen
    return fbxName, pbloc, file3[4], file3[5], file3[6] + '.mov', mayaFileReopen
