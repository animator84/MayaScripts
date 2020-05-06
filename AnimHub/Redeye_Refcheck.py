import maya.cmds as cmds
import pymel.core as pm
import maya.mel as mel
import random
import os
import sys
import subprocess

#links to these drives are hard coded. Not fantastic, but because our workflow is already standardized
#with G and Z drive. this works for us with minimal effort.
GDrivePath = 'G:/My Drive/goGame 3D Team (SG+MY)/Galaxy/Art/3D/Character Animation'
ZDrivePath = 'Z:/006_Art/002_3DArtist/GALAXY/Character Animation'
RawScenes = '/Raw/scenes'
LatestRigFullPath = ''
ChosenPath = ''


def choose():
    #lets user choose where they are working on. Z or G drive
    global ChosenPath
    global GDrivePath
    global ZDrivePath
    result = cmds.confirmDialog(title='Where do you work', message='Are you working Locally or Googley?',
                                button=['Local Z', 'Google G'])

    if result == 'Local Z':
        ChosenPath = ZDrivePath

    elif result == 'Google G':
        ChosenPath = GDrivePath

    print ChosenPath
    return result, ChosenPath


def filenameManager2():
    '''
    This is an old Filemanager function i use with many other scripts. I break down the current scene's filename into parts to decipher its
    Charactername, Character ID and etc. I didn't clean up this portion because I'm lazy.

    FilenameManager2 should only run AFTER choose() function because ChosenPath is null on execution
    Currently filenameManger2 only outputs The CHOSEN FOLDER PATH
    '''

    global ChosenPath

    filename = os.path.basename(pm.system.sceneName())
    fileExt = os.path.splitext(pm.system.sceneName())[1]
    fileloc = os.path.dirname(pm.system.sceneName())
    fileSplit = filename.split(fileExt)[0].split("_")
    fileIteration = fileSplit[-1]
    characterID = fileSplit[0]
    characterName, cycleName = fileSplit[1].split("@")[0], fileSplit[1].split("@")[1]

    print 'Character ID : %s \nCharacter Name : %s' % (characterID, characterName)

    playblastName = '_'.join(fileSplit)
    ExportFilename = '_'.join(fileSplit[0:2])
    fileloclist = fileloc.split("/")
    fbxLocation = '/'.join(fileloclist[:8]) + '/' + characterID

    print ChosenPath + '/' + characterID + '_' + characterName + RawScenes
    return ChosenPath + '/' + characterID + '_' + characterName + RawScenes
    # return fileloc, ExportFilename, fileExt, fileIteration, characterName, characterID, playblastName, fbxLocation


def searchFolder(folder, Tag=None):
    '''takes in a folder path and a string as a Tag
    seach through the folder for filenames with the selected tag and
    return the filenames with the tag

    return : all the rigs present[0] + the latest rig's full path[1]
    '''
    global LatestRigFullPath

    rigsPresent = []
    sortedFiles = []
    for file in os.listdir(folder):
        sortedFiles.append(file)

    #put the files in a list first then sort so tt RIG latest will always be the last index
    sortedFiles.sort()

    for file in sortedFiles:
        if os.path.isfile(os.path.join(folder, file)):
            if Tag in file:
                rigsPresent.append(file)

    LatestRigFullPath = folder + '/' + rigsPresent[-1]
    return rigsPresent, LatestRigFullPath


def findLatest(files):
    '''
    for the files, if there's just 1 file, pass and return
    '''
    if len(files) == 1:
        return files
        print "There's only 1 RIG you're good"
    elif len(files) != 1:
        print 'there are %s RIGs and you need to use %s' % (len(files), files[-1])
    return files[-1]


def checkCurrentRef(latest):
    '''
    Function must only run after LatestRigFullPath has been defined.
    :param latest:
    :return:
    '''
    global LatestRigFullPath
    refObjects = cmds.ls(l=True, type='reference')
    if len(refObjects) <= 2:
        curRef = cmds.referenceQuery(refObjects[0], filename=True).split("/")[-1]
        print 'current Reference is : ' + curRef
        if curRef == latest:
            print 'current Reference is Latest'
            cmds.confirmDialog(title='Success', message='\n' + 'Your Rig is the latest liao~~ dont worry', button='Ok',
                               messageAlign='left')

        else:
            cmds.file(LatestRigFullPath, loadReference=refObjects[0])
            cmds.confirmDialog(title='Success', message='\n' + 'you did it! you changed the reference to \n %s' %
                                                        LatestRigFullPath.split("/")[-1], button='Ok',
                               messageAlign='left')
    elif len(refObjects) > 2:
        print "there's more than 1 reference Object in this scene \n this script is not catered for that"

def isRef():
    '''
    is there any reference? If there's no references, then return False
    :return: True/ False
    '''
    refObjects = cmds.ls(l=True, type='reference')
    if len(refObjects) == 0:
        cmds.confirmDialog(title='Umm...', message="There's no Reference in this scene. \nReference in a RIG file. \nThis script checks for the latest RIG \nfrom your scene name \n e.g.: CHA111_character@idle_00.ma ", button='Ok', messageAlign= 'center')
        return False
    else:
        return True

def main():
    refHere = isRef()
    if refHere == True:
        choose()
        a = findLatest(searchFolder(filenameManager2(), 'RIG')[0])
        checkCurrentRef(a)

#main()