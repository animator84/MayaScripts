import maya.cmds as cmds

if cmds.play(query=True, state=True) == True:
    cmds.play(state=False)

elif cmds.play(query=True, state=True) == False:
    cmds.play(state=True)
