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
	dType.SetPTPCoordinateParamsEx(api,500,1000,500,1000,1)
	deltamove(0,0,-55)
	dType.SetPTPCoordinateParamsEx(api,4000,8000,4000,8000,1)
	for i in range(2):
		deltamove(0,0,-10)
		deltamove(0,0,10)
	dType.SetPTPCoordinateParamsEx(api,500,1000,500,1000,1)
	deltamove(0,0, 55)

def stand():
	dType.SetPTPCoordinateParamsEx(api,500,1000,500,1000,1)
	deltamove(40,0,0)
	deltamove(-80,0,0)
	deltamove(80,0,0)
	deltamove(-80,0,0)
	deltamove(40,0,0)

def lose():
	dType.SetPTPCoordinateParamsEx(api,200,100,200,100,1)
	deltamove(0,0,-50)
	deltamove(20,0,0)
	deltamove(-40,0,0)
	deltamove(20,0,0)
	time.sleep(1)
	deltamove(0,0,50)

def win():
	dType.SetPTPCoordinateParamsEx(api,1000,2000,1000,2000,1)
	deltamove(0,0,50)
	for i in range(3):
		deltamove(0,20,20)
		deltamove(0,-40,0)
		deltamove(0,20,-20)
	time.sleep(1)
	deltamove(0,0,-50)

dType.SetPTPCoordinateParamsEx(api,500,2000,500,2000,1)
moveto(0, -260, -0)
hitMe()
stand()
lose()
win()
