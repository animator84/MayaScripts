import maya.cmds as cmds

panelnow=cmds.getPanel(wf=True)
#print panelnow
ncCheck=cmds.modelEditor(panelnow, query=True, nc=True)
#print ncCheck

if ncCheck == True :
    cmds.modelEditor(panelnow,edit=True,nc=False)
    
else :
    cmds.modelEditor(panelnow,edit=True,nc=True)
