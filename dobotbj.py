from time import sleep
import math
import random

fail = "C:/Users/luud.lt7a493/Desktop/luud proge/python/dobonontsik/detected_cards.txt"
rahafail = open("C:/Users/luud.lt7a493/Desktop/luud proge/python/dobonontsik/raha.txt", "w+")
minul = 0 #summad
temal = 0
kord = "player" #str: player, wait
p_eel = [0]
d_eel = [0]
eel_teg = ""
otsus = ""
killswitch = 0
# VAADATA RAHA KIRJUTAMINE ÜLE
raha = int(rahafail.read())
algRaha = raha
panus = 0
toomas_sularaha = ""
kaija = True
ma = []
looping = True

def sumo(nimekiri):
    ajut = 0
    assad = 0
    for i in range(len(nimekiri)):
        try:
            ajut += int(nimekiri[i])
        except:
            if nimekiri[i]== "J" or nimekiri[i] == "Q" or nimekiri[i] =="K":
                ajut += 10
            elif nimekiri[i] == "A":
                assad +=1
    if assad == 1:
        if (ajut + 11 ) > 21:
            ajut += 1
        else:
            ajut += 11
    elif assad ==2:
        if (ajut + 1) > 21:
            ajut += 2
        else:
            ajut += 12
    elif assad >= 3:
        if (ajut + 11 + (assad-1)) <= 21:
            ajut += (11+ (assad-1))
        else:
            ajut += assad
    return ajut

def saa_seis(fail):
    global minul, temal, kord, p_eel, d_eel, killswitch, toomas_sularaha, kaija, ma
    with open(fail, "r") as f:
        read = f.readlines()
    if read != toomas_sularaha:
	    toomas_sularaha = read
	    ma = read[0].strip().split(); ta = read[1].strip().split(); killswitch = int(read[2].strip())
	    if p_eel == ma and d_eel == ta:
		    sleep(1);print("ootan, sama")
	    else:
		    minul = sumo(ma)
		    temal = sumo(ta)
		    p_eel = ma; d_eel = ta
	    print("mul", minul, "tal", temal)
	    kaija = True
    else:
	    kaija = False

def kaik():
    global otsus, minul, temal, eel_teg, kaija, panus, raha
    if kaija == False:
        #print("a ple minu asi lowk")
        otsus = "ei"
        sleep(1)
    elif kaija == True:
    		#print("aju = töötab")
    		if minul < 17:
        		otsus = "hit"
        		eel_teg = otsus
    		elif minul > 21:
        		otsus = "bust"
        		raha -= panus
        		eel_teg = otsus
    		elif (minul == 17) and (len(ma) == 2) and ("A" in ma):
        		otsus = "doubledown"
        		eel_teg = otsus
        		panus = min(panus*2, raha)
    		elif minul >= 17 and minul <= 21:
        		otsus = "stand"
        		eel_teg = otsus

def BetSize():
    global raha, algRaha
    variability = random.uniform(-0.05, 0.05)
    desperationScore = 1 - (raha / algRaha)
    betConstant = min(0.1 * (raha / algRaha), 0.80)

    if raha == 0:
        betSize = 0
    if random.uniform(0, 1) > desperationScore:
        betSize = round((betConstant * raha) * (1 + variability))
    else:
	    print("ALL IN!")
	    betSize = raha
		
    return betSize

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

def doubleDown():
	global panus
	dType.SetPTPCoordinateParamsEx(api,500,1000,500,1000,1)
	deltamove(0,0,-55)
	sleep(1)
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
	sleep(1)
	deltamove(0,0,50)

def win():
	dType.SetPTPCoordinateParamsEx(api,1000,2000,1000,2000,1)
	deltamove(0,0,50)
	for i in range(3):
		deltamove(0,20,20)
		deltamove(0,-40,0)
		deltamove(0,20,-20)
	sleep(1)
	deltamove(0,0,-50)

dType.SetPTPCoordinateParamsEx(api,500,2000,500,2000,1)
moveto(240, -14, -4)
#hitMe()
#stand()
#lose()
#win()
while looping == True:
    panus = BetSize()
    print("Alles " + str(raha) + " euri")
    print("Panustan " + str(panus) + " euri")
    while killswitch == 0:
        saa_seis(fail)
        if kord == "wait":
            sleep(3)
            killswitch = 1
        elif kord == "player":
            kaik()
            print(otsus)
            if otsus == "hit":
                hitMe()
            elif otsus == "doubledown":
                #print("DOUBLE OR NOTHING BABY")
                doubleDown()
                killswitch = 1
            elif otsus == "stand":
                stand()
                kord = "wait"
                killswitch = 1
            elif otsus == "bust":
                lose()
                kord = "wait"
                killswitch = 1
                sleep(3)

            elif kord == "wait":
                sleep(3)
                killswitch = 1

            elif kord == "ei":
                sleep(1)

    while temal < 17:
        saa_seis(fail)
        #print("honk mimimi")
        sleep(1)
        
    killswitch = 1

    if killswitch == 1:
        if minul < 22:
            if minul >= temal:
                raha += panus
                win()
            else:
                raha -= panus
                lose()
    print("Raha on nüüd " + str(raha))
    rahafail.write(str(raha))
    if int(raha) <= 0:
        looping = False
    while looping == True:
        print("jarvis, check my loop", minul, temal)
        if minul == temal == 0:
            looping = False
        else:
            sleep(1)
print("tsau")
