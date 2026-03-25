#Magician
#Magician
import time
import math

def moveto(x, y, z):
	current_pose = dType.GetPose(api)
	dType.SetPTPCmdEx(api, 2, x,  y,  z, current_pose[3], )

def deltamove(x, y, z):
	current_pose = dType.GetPose(api)
	dType.SetPTPCmdEx(api, 7, x,  y,  z, 0, 1)

def hitMe():
	dType.SetPTPLParamsEx(api,500,1000,1)
	deltamove(0,0,-40)
	for i in range(2):
		deltamove(0,0,-20)
		deltamove(0,0,20)
	deltamove(0,0, 40)

def stand():
	dType.SetPTPLParamsEx(api,500,1000,1)
	for i in range(2):
		deltamove(20,20,0)
		deltamove(-40,-40,0)
		deltamove(20,20,0)

def lose():
	dType.SetPTPLParamsEx(api,20,50,1)
	deltamove(0,0,-50)
	time.sleep(2)
	deltamove(0,0,50)

def win():
	dType.SetPTPLParamsEx(api,500,1000,1)
	deltamove(0,0,50)
	for i in range(3):
		deltamove(20,20,20)
		deltamove(-40,-40,0)
		deltamove(20,20,-20)
	time.sleep(1)
	deltamove(0,0,-50)

moveto(0, 0, 60)

"""INSERT GAMEPLAY LOOP
