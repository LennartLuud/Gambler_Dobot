#Magician
from time import sleep
import math

fail = "C:/Users/luud.lt7a493/Desktop/luud proge/python/dobonontsik/detected_cards.txt"
minul = 0 #summad
temal = 0
p_eel = [0]
d_eel = [0]
eel_teg = ""
otsus = ""
killswitch = 0
print(fail)
raha = 1000
algRaha = raha
panus = 0

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
    global minul, temal, p_eel, d_eel, killswitch, kaardidKäes
    with open(fail, "r") as f:
        read = f.readlines()
    try:
        ma = read[0].strip().split(); ta = read[1].strip().split(); killswitch = int(read[2].strip())
    except: ma = read[0].strip().split(); ta = read[1].strip().split(); killswitch = int(read[2].strip())
    ma.sort(), ta.sort()
    if p_eel == ma and d_eel == ta:
        sleep(1);print("ootan, sama")
    else:
        minul = sumo(ma)
        temal = sumo(ta)
		kaardidKäes = ma
        p_eel = ma; d_eel = ta
    print(minul, temal)

def kaik():
    global otsus, minul, temal, eel_teg
    print("aju = töötab")
    if minul < 17:
        otsus = "hit"
        eel_teg = otsus
    elif minul > 21:
        otsus = "bust"
        eel_teg = otsus
    elif (minul == 17) and (len(kaardidKäes) == 2) and ("A" in kaardidKäes):
        otsus = "doubledown"
        eel_teg = otsus
        panus = panus*2
    elif minul >= 17 and minul <= 21:
        otsus = "stand"
        eel_teg = otsus

def BetSize(raha):
    variability = random.randrange(-0.05, 0.05)
    desperationScore = 1 - (raha / algRaha)
    betConstant = min(0.1 * (raha / algRaha), 0.80)

    if raha == 0:
        betSize = 0
    if random.randrange(0, 1) > desperationScore:
        betSize = round((betConstant * raha) * (1 + variability))
    else:
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

kord = "player"
while killswitch == 0:
    saa_seis(fail)
    if kord == "wait":
        if temal > 21:
            print("juhhuu")
            win()
            killswitch = 1
        elif temal < minul and temal >= 17:
            print("juhhuu")
            win()
            killswitch = 1
        elif temal > minul:
            print("BWAAAAA :(((((")
            lose()
            killswitch = 1
    elif kord == "player":
        kaik()
        print(otsus)
        if otsus == "stand":
            kord = "wait"

        elif otsus == "bust":
            kord == "wait"

print("tsau")
