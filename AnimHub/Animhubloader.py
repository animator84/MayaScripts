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
    if not pathfound:
        sys.path.insert(0, 'C:\Users\Administrator\Desktop\Scripts')
#------------------------------------------------------------------

import Redeye_AnimHub
reload(Redeye_AnimHub)
