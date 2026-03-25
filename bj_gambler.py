from time import sleep
f = open("C:/Users/luud.lt7a493/Desktop/kaardid.txt")
minul = 0 #summad
temal = 0
kord = "" #str: player, wait
p_eel = [0]
d_eel = [0]
eel_teg = ""
otsus = ""

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
                ajut +=1
    if assad == 1:
        if (ajut + 10 ) > 21:
            ajut += 1
        else:
            ajut += 10
    elif assad ==2:
        if (ajut + 1) > 21:
            ajut += 2
        else:
            ajut += 12
    elif assad >= 3:
        ajut += assad
    return ajut

def saa_seis(fail):
    global minul, temal, kord
    read = fail.readlines()
    ma = read[0].strip().split(); ta = read[1].strip().split(); kord = read[2].strip()
    ma.sort(), ta.sort()
    if p_eel == ma and d_eel == ta:
        sleep(1000)
    else:
        minul = sumo(ma)
        temal = sumo(ta)
        p_eel = ma; d_eel = ta
    print(minul, temal)

def kaik():
    global otsus, minul, temal, eel_teg
    print("aju = töötab")
    if minul < 17:
        otsus = "hit"
        eel_teg = otsus
    elif minul > 17 and minul <= 21:
        otsus = "stand"
        eel_teg = otsus
    elif minul > 21:
        otsus = "bust"
        eel_teg = otsus

saa_seis(f)
if kord == "player":
    kaik()