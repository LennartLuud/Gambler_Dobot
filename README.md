double down: 
def doubledown():
	dType.SetPTPCoordinateParamsEx(api,500,1000,500,1000,1)
	deltamove(40,0,0)
	deltamove(-80,0,0)
	sleep(0.1)
	deltamove(80,0,0)
	deltamove(40,0,0)
