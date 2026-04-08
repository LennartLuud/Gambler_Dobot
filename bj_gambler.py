fail = "C:/Users/ligi.sn7a493/Documents/Gambler_Dobot-main/detected_cards.txt"
from time import sleep
minul = 0 #summad
temal = 0
p_eel = [0]
d_eel = [0]
eel_teg = ""
otsus = ""
killswitch = 0

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
    global minul, temal, p_eel, d_eel, killswitch
    with open(fail, "r") as f:
        read = f.readlines()
    #print(read)
    try:
        ma = read[0].strip().split(); ta = read[1].strip().split(); killswitch = int(read[2].strip())
    except: ma = read[0].strip().split(); ta = read[1].strip().split(); killswitch = int(read[2].strip())
    ma.sort(), ta.sort()
    if p_eel == ma and d_eel == ta:
        sleep(1);print("ootan, sama")
    else:
        minul = sumo(ma)
        temal = sumo(ta)
        p_eel = ma; d_eel = ta
    print("minul:", minul, "dr house:", temal)

def kaik():
    global otsus, minul, temal, eel_teg
    print("aju = töötab")
    if minul < 17:
        otsus = "hit"
        eel_teg = otsus
    elif minul >= 17 and minul <= 21:
        otsus = "stand"
        eel_teg = otsus
    elif minul > 21:
        otsus = "bust"
        eel_teg = otsus

kord = "player"
while killswitch == 0:
    saa_seis(fail)
    if kord == "wait":
        if temal > 21:
            print("juhhuu")
            killswitch = 1
        elif temal < minul and temal >= 17:
            print("juhhuu")
            killswitch = 1
        elif temal > minul:
            print("BWAAAAA :(((((")
            killswitch = 1
    elif kord == "player":
        kaik()
        print(otsus)
        if otsus == "stand":
            kord = "wait"

        elif otsus == "bust":
            kord == "wait"

print("tsau")