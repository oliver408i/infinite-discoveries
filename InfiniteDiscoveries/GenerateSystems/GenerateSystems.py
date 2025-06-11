import os
import shutil, state, textwrap

import Settings
from pathlib import Path
base_dir = Path(__file__).resolve().parent.parent

import PySimpleGUI as sg


import multiprocessing
import threading
currentProcess = threading.current_thread()
allThreads = []
allActions = []
mainThreadFinished = False
everythingEnded = False
print(currentProcess.name)

amountOfThingsToDo = 0
amountOfThingsDone = 0

if currentProcess.name == "MainThread":
    print(
        "■■■■■■■■■■■■■  ■■        ■■  ■■■■■■■■  ■■■■■■■■■■■■■  ■■        ■■  ■■■■■■■■■■■■■  ■■■■■■■■■■■■■  ■■■■■■■■■\n"
        "     ■■        ■■■■      ■■  ■■             ■■        ■■■■      ■■       ■■             ■■        ■      \n"
        "     ■■        ■■  ■■    ■■  ■■■■■■         ■■        ■■  ■■    ■■       ■■             ■■        ■■■■■  \n"
        "     ■■        ■■    ■■  ■■  ■■             ■■        ■■    ■■  ■■       ■■             ■■        ■      \n"
        "     ■■        ■■      ■■■■  ■■             ■■        ■■      ■■■■       ■■             ■■        ■      \n"
        "■■■■■■■■■■■■■  ■■        ■■  ■■        ■■■■■■■■■■■■■  ■■        ■■  ■■■■■■■■■■■■■       ■■        ■■■■■■■■■\n"
    )
    
    print(
        "■■■     ■■■■■     ■■■■       ■■■■       ■■       ■     ■      ■■■■■     ■■■■■    ■■■■■    ■■■■■     ■■■■\n"
        "■  ■      ■      ■          ■          ■  ■       ■   ■       ■         ■   ■      ■      ■        ■\n"
        "■  ■      ■       ■■■       ■          ■  ■       ■   ■       ■■■       ■■■        ■      ■■■       ■■■■\n"
        "■  ■      ■          ■      ■          ■  ■        ■ ■        ■         ■ ■        ■      ■             ■\n"
        "■■■     ■■■■■    ■■■■        ■■■■       ■■          ■         ■■■■■     ■  ■■    ■■■■■    ■■■■■     ■■■■\n"
    )
    
    print("---------------------------------------------------------------------------------------------------------")
    queue = []
import random
import string
from colour import Color
import sys
import time
import math
import numpy as np
import importlib
import colorsys
import matplotlib.pyplot as plt
from matplotlib.colors import to_hex

targetPath = ""

if Settings.convertTexturesToDDS == True:
    try:
        from wand import image as wImage
        canConvertToDDS = True
    except:
        print("ImageMagick is not installed, install it from: https://docs.wand-py.org/en/latest/guide/install.html#install-imagemagick-on-windows")
        canConvertToDDS = False
else:
    canConvertToDDS = False

from nameGen import processName, getTables
starTransisionTable,vacuumTransisionTable,oceanicTransisionTable,gaseousTransisionTable,lifeTransisionTable,rockyTransisionTable,lavaTransisionTable,icyTransisionTable = getTables()
from templateGens import generateNebula, generateSuperheatedClouds, generateWRBinarySpiral

# Variables lamo
templates = ["Dres", "Duna", "Laythe", "Mun", "Jool"] # Laythe and Mun are unused lmao lol oops.
planetsGenerated = 0
alphabet = list(string.ascii_uppercase)

# Star Colors
cmap = plt.get_cmap('coolwarm')  # 'coolwarm' is a colormap that goes from red to blue
gradient = np.linspace(0, 1, 100)
colors = [to_hex(cmap(x)) for x in gradient]
colorsReversed = list(reversed(colors))

black = Color("#000000")
lavaRed = Color("#eb2700")
lavaColors1 = list(black.range_to(Color("#eb2700"),7))
lavaColors2 = list(lavaRed.range_to(Color("#ebac00"),10))
lavaSpectrum = lavaColors1 + lavaColors2


# Set all values to zero to prevent weird shenanigans from happening.
totalSystemsGenerated = 0
totalStarsGenerated = 0
totalPlanetsGenerated = 0
totalMoonsGenerated = 0

availableGalaxies = ["Sun","Sun","Sun","Sun","LKC_CtrlB","LKC_CtrlB","SKC_CtrlB"] # "Sun" is the milky way.

print("Starting generator...")
allPlanets = []
wormholeList = []

# !!!!! THE GLOBAL SEED!!! THIS IS VERY IMPORTANT !!!!!!
gloablSeed = 42

# Gets star color multiplier I guess
def getStarColorMult(radi):
    starRadiusMult = radi/261600000
    if starRadiusMult < 1:
        colorMult = np.interp(starRadiusMult, [0, 1], [0, 45])
    elif starRadiusMult > 1:
        colorMult = np.interp(starRadiusMult, [1, 7], [45, 99])
    else:
        colorMult = 45
    return colorMult

from resConfig import createResourceConfig


from wormholeGen import generateWormhole # Unused?

from parallax import addParallaxScatter, addToParallaxScatterFixCfg, addToParallaxCfg, addSubdividerFix
from generateDisk import generateDisks

from eveAscatterer import addToVolumetricEveCfg, addPQSFix, addSunflareCfg, addToAtmoCfg, addToEVEAurora, addToEVECfg, addToOceanCfg, addToScattererList

from starConfig import writeBarycenterCfg, writeStarCfg
from bodyConfig import writeBodyCfg, genRing

from generateMaps import generateGasGiantMaps, generatePlanetMaps

# Picks parameters for a moon.
def generateMoon(planetSeed, moonNum, parentPlanet, moonsGenerated, parentRadius, gasGiantP, atmoCfg, starN, starColor, listCfg, colorsRound, oceanCfg, eveCfg, VolumetricEveCfg, Lum, parentSMA, starRadius, parallaxCfg, subdfixCfg, parallax_scatterfix_Cfg, parallax_scatter_Cfg, rationalResources_Cfg, moonDistMult, isAsteroid, binaryParents=None, distBinaryParents=None,distBinaryStarNum=None):
    global gloablSeed
    
    #global amountOfThingsToDo
    #global amountOfThingsDone

    #amountOfThingsToDo += 1

    moonRNG = random.Random()

    if not distBinaryParents == None:
        moonSeed = planetSeed+moonNum+(int(distBinaryStarNum)*-1)
    else:
        moonSeed = planetSeed+moonNum

    moonRNG.seed(moonSeed)

    if isAsteroid == True:
        print(str(moonsGenerated) + "<---------------------------------------------------------------------------------------------------------------------------------- asterodfs ")
    print(moonsGenerated)
    if isAsteroid == True:
        planetName = parentPlanet + "-SUB-" + str(moonsGenerated)
    else:
        planetName = parentPlanet + "-" + str(moonsGenerated)
    global totalMoonsGenerated
    totalMoonsGenerated = totalMoonsGenerated + 1
    print(planetName)

    if isAsteroid == True:
        inclinationLimits = [-20,20]
        if gasGiantP == True:
            planetRadius = moonRNG.randint(5,29)*1000
            planetSMA = (moonRNG.randint(1000000,10000000)*moonsGenerated)*(parentRadius/600000)
        else:
            planetRadius = moonRNG.randint(5,29)*1000
            planetSMA = (moonRNG.randint(1000000,10000000)*moonsGenerated)*(parentRadius/600000)
    else:
        if gasGiantP == True:
            planetRadius = moonRNG.randint(50,700)*1000
            planetSMA = (moonRNG.randint(3300000,5000000)*moonsGenerated)*(parentRadius/600000)
        else:
            planetRadius = (parentRadius*moonRNG.randint(40,80)/100)/2
            planetSMA = ((moonRNG.randint(3300000,5000000)*moonsGenerated)*moonDistMult)*(parentRadius/600000)

    gasGiant = False
    planetMass = (5.29151583439215E+22 / (600000/planetRadius)**3.7)
    
    allActions.append([time.localtime(),"Picking parameters for moon: " + planetName])
    state.allActionArrayUpdated = True

    try:
        inclinationLimits
    except:
        inclinationLimits = [0,10]

    atmoPress = 0
    atmClrR = 0
    atmClrG = 0
    atmClrB = 0
    sctrClrR = 0
    sctrClrG = 0
    sctrClrB = 0
    if planetRadius > 300000:
        atmo = "Atmospheric"
        vacuum = False
        lessOrMore = moonRNG.choice([0,1,2])
        if lessOrMore == 1:
            numberguy = moonRNG.randint(100,1000)
        else:
            numberguy = moonRNG.randint(1,100)
        atmoPress = numberguy*((planetRadius/600000)*0.5)
    else:
        atmo = "Vacuum"
        vacuum = True
    
    if atmo == "Atmospheric":
        templ = 1
    elif atmo == "Vacuum":
        templ = 0
    
    starLum = Lum
    starLumMult = starLum/1360
    smaMult = 13599840256/parentSMA
    
    pressureMultiplier = atmoPress/100

    randomGreenhouse = moonRNG.randint(5,20)/10

    vacuumTemp = 233*starLumMult*smaMult # Base temperature without any greenhouse.

    greenhouse = 80*(pressureMultiplier*randomGreenhouse) # Additional temperature to add above the base temperature, assuming there's an atmosphere.

    finalTemp = round(vacuumTemp + greenhouse)
    if atmo == "Atmospheric":
        if gasGiant == False:
            if moonRNG.randint(1,3) == 1:
                if finalTemp > 200 and finalTemp < 600:
                    ocean = True
                else:
                    ocean = False
            else:
                ocean = False
        else:
            ocean = False
    else:
        ocean = False

    if finalTemp < 200 and moonRNG.randint(1,2) == 1 and isAsteroid == False:
        icy = True
    else:
        icy = False

    possibleLife = []

    if finalTemp > 223 and finalTemp < 373:
        if gasGiant == False and ocean == True and atmo == "Atmospheric" and atmoPress > 10:
            if moonRNG.randint(0,0) == 0:
                possibleLife.append("organic")
    if finalTemp < 223 or finalTemp > 373:
        if gasGiant == False and atmo == "Atmospheric":
            if moonRNG.randint(0,3) == 0:
                possibleLife.append("exotic")
    if finalTemp < 223 and gasGiant == False and ocean == False and atmo == "Vacuum" and icy == True:
        if moonRNG.randint(0,3) == 0:
            possibleLife.append("subglacial")
    if gasGiant == True or atmoPress > 700:
        if moonRNG.randint(0,3) == 0:
            possibleLife.append("aerial")

    if len(possibleLife) > 0:
        life = random.choice(possibleLife)
        if life == "organic":
            oxygen = True
            atmClrR = moonRNG.randint(100,200)
            atmClrG = moonRNG.randint(75,150)
            atmClrB = moonRNG.randint(0,50)
        else:
            oxygen = False
            atmClrR = moonRNG.randint(0,200)
            atmClrG = moonRNG.randint(0,200)
            atmClrB = moonRNG.randint(0,200)
    else:
        oxygen = False
        life = None
        atmClrR = moonRNG.randint(0,200)
        atmClrG = moonRNG.randint(0,200)
        atmClrB = moonRNG.randint(0,200)

    sctrClrR = (atmClrR*-1)+255
    sctrClrG = (atmClrG*-1)+255
    sctrClrB = (atmClrB*-1)+255

    if Settings.fantasyNames == True:
        if atmo == "Atmospheric":
            if finalTemp > 600:
                dispName = processName(moonSeed,lavaTransisionTable,10)
            elif finalTemp < 100:
                dispName = processName(moonSeed,icyTransisionTable,10)
            elif ocean == True:
                if not life == None:
                    dispName = processName(moonSeed,lifeTransisionTable,10)
                else:
                    dispName = processName(moonSeed,oceanicTransisionTable,10)
            else:
                dispName = processName(moonSeed,rockyTransisionTable,10)
        else:
            dispName = processName(moonSeed,vacuumTransisionTable,10)
    else:
        dispName = planetName

    print("Display name for " + planetName + " is " + dispName)

    black = Color("#000000")
    Pcolors1 = list(black.range_to(Color("#700000"),5))
    red = Color("#700000")
    Pcolors2 = list(red.range_to(Color("#9e008c"),90))
    pink = Color("#9e008c")
    Pcolors3 = list(pink.range_to(Color("#fcf2fa"),5))
    PfinalColors = Pcolors1 + Pcolors2 + Pcolors3

    PMult = starRadius*30 / 261600000
    if PMult > len(PfinalColors):
        PMult = len(PfinalColors)
    PmultRound = round(PMult)
    plantColor = Color.get_rgb(PfinalColors[PmultRound-1])

    if atmo == "Atmospheric" and finalTemp >= 50 and finalTemp <= 300:
        icecaps = True
    else:
        icecaps = False

    if finalTemp > 700:
        lava = True
        if round(finalTemp/100) < 17:
            lavaClr = (lavaSpectrum[round(finalTemp/100)])
        else:
            lavaClr = lavaSpectrum[16]
    else:
        lava = False
        lavaClr = Color("#000000")

    lavaClrRGB = Color.get_rgb(lavaClr)

    oceanR = moonRNG.randint(5,20)
    oceanG = moonRNG.randint(5,35)
    oceanB = moonRNG.randint(10,75)

    moon = True

    terrainR = moonRNG.randint(50,175)
    terrainG = moonRNG.randint(50,175)
    terrainB = moonRNG.randint(50,175)

    #if gasGiant == False:
    #    if random.randint(1,1) == 1:
    #        if random.randint(0,1) == 1:
    #            print("??????????!!!?!??")
    #            anomaly = "crshShp"
    #            anLat = random.randint(-45,45)
    #            anLon = random.randint(-180,180)
    #        else:
    #            print("?????????")
    #            anomaly = "fltStrc"
    #            anLat = random.randint(-45,45)
    #            anLon = random.randint(-180,180)
    #        anLatLon = [anLat,anLon]
    #    else:
    #        anomaly = "None"
    #        anLatLon = []
    #else:
    #    anomaly = "None"
    #    anLatLon = []
    anLatLon = []
    anomaly = "None"

    if atmo == "Atmospheric":
        if ocean == True:
            if icy == True:
                groundType = 3
            else:
                groundType = moonRNG.choice([0,1,2])
        else:
            if icy == True:
                groundType = 3
            else:
                groundType = moonRNG.choice([0,1,2])
    else:
        if icy == True:
            groundType = 3
        else:
            groundType = moonRNG.choice([0,1,2])

    if gasGiant == False:
        addSubdividerFix(subdfixCfg, planetName)
        addToParallaxCfg(moonSeed, parallaxCfg, planetName, lava, lavaClrRGB, groundType, icy, allActions)
        addToParallaxScatterFixCfg(parallax_scatterfix_Cfg, planetName)
        addParallaxScatter(moonSeed, parallax_scatter_Cfg, planetName, life, plantColor, planetRadius)

    terrainClr = "RGBA(" + str(terrainR) + ", " + str(terrainG) + ", " + str(terrainB) + ", 100)"

    print("-------Physical Values-------")
    print("Radius: " + str(planetRadius))
    print("Mass: " + str(planetMass))
    print("Semimajor Axis: " + str(planetSMA))
    print("Terrain tint: " + str(terrainClr))
    if not life == None:
        print("Has life!")

    print("-------Atmosphere Values-------")
    if atmo == "Atmospheric":
        print("Atmosphere scattering color: " + str(atmClrR) + " " + str(atmClrG) + " " + str(atmClrB))
        print("Atmosphere main color: " + str(sctrClrR) + " " + str(sctrClrG) + " " + str(sctrClrB))
        print("kPa at sea level: " + str(atmoPress))
        print("Temperature at sea level: " + str(finalTemp) + " kelvin.")
        if oxygen == True:
            print("Oxygenated!")
    else:
        print("No atmosphere!")

    print("-------------------------------")
    planetCfg = open(targetPath + "/Configs/" + planetName + "-" + str(moonsGenerated) + ".cfg","x")
    if moonRNG.randint(1,2) == 1:
        geoActive = True
        if moonRNG.randint(1,2) == 1:
            activeVolcano = True
        else:
            activeVolcano = False
    else:
        geoActive = False
        activeVolcano = False

    if moonRNG.randint(0,3) == 0:
        oceanFactor = moonRNG.randint(16,255)
    else:
        oceanFactor = moonRNG.randint(16,128)

    generatePlanetMaps(vacuum, terrainR, terrainG, terrainB, planetName, ocean, oceanR, oceanG, oceanB, atmoPress, geoActive, icecaps, finalTemp, life, plantColor, planetRadius, anomaly, anLatLon, activeVolcano, lava, False, oceanFactor, isAsteroid, moonSeed, icy, allActions, base_dir, lavaSpectrum, everythingEnded, targetPath, canConvertToDDS)

    ringInn = 2000
    ringOut = 2001
    rings = False

    atmoHeight = moonRNG.randint(50,90)*1000

    if ocean == True:
        addToOceanCfg(moonSeed, oceanCfg, oceanR, oceanG, oceanB, planetName, allActions)

    Tag = "InfD_Moon"

    if atmo == "Atmospheric":
        addToAtmoCfg(atmoCfg, starN, planetName, starColor, sctrClrR, sctrClrG, sctrClrB, ocean, gasGiant, atmoHeight, atmoPress, allActions)
        if binaryParents == None:
            if distBinaryParents == None:
                addToScattererList(listCfg, starN, planetName, starColor, ocean, colorsRound)
            else:
                addToScattererList(listCfg, starN, planetName, starColor, ocean, colorsRound, None, distBinaryParents)
        else:
            addToScattererList(listCfg, starN, planetName, starColor, ocean, colorsRound, binaryParents)
        if gasGiant == False:
            if ocean == True or moonRNG.randint(1,2) == 1:
                cloudTexNum = moonRNG.randint(1,5)
                addToEVECfg(eveCfg, cloudTexNum, planetName, False, allActions)
                addToVolumetricEveCfg(moonSeed, VolumetricEveCfg, cloudTexNum, planetName, False, ocean, allActions)

    createResourceConfig(moonSeed,rationalResources_Cfg,planetName,lava,icy,finalTemp,atmoPress,ocean,gasGiant,life,None)

    sciValue = 3

    if atmo == "Atmospheric":
        sciValue += 5

    if ocean == True:
        sciValue += 10

    if life == "Organic":
        sciValue += 15
    elif life == "Exotic":
        sciValue += 25
    elif life == "Aerial":
        sciValue += 20
    elif life == "Subglacial":
        sciValue += 10

    if lava == True:
        sciValue += 10

    if icy == True:
        sciValue += 5

    tidallyLocked = True
    writeBodyCfg(moonSeed, planetCfg, planetName, planetRadius, planetMass, planetSMA, parentPlanet, atmo, atmoPress, templ, atmClrR, atmClrG, atmClrB, sctrClrR, sctrClrG, sctrClrB, terrainClr, moon, gasGiant, rings, ringInn, ringOut, ocean, oceanR, oceanG, oceanB, atmoHeight, finalTemp, oxygen, life, dispName, anomaly, anLatLon, Tag, lava, tidallyLocked, oceanFactor, isAsteroid, icy, inclinationLimits, sciValue, allActions, templates, canConvertToDDS)
    #amountOfThingsDone += 1

# Picks parameters for a planet.
def generate(seedThing,starN,starRadius,starMass,starColor,atmoCfg,listCfg,colorsRound,oceanCfg,eveCfg,VolumetricEveCfg,Lum,parallaxCfg,subdfixCfg,parallax_scatterfix_Cfg,parallax_scatter_Cfg,evePQSCfg,rationalResources_Cfg,typeOfStar,currentPlanetNum,binaryParents=None,binaryTypes=None,gSMA=None,distanceThingamabob=None,distBinaryParents=None,distBinaryStarNum=None):
    planetRNG = random.Random()

    global amountOfThingsToDo
    global amountOfThingsDone

    amountOfThingsToDo += 1

    if not distBinaryParents == None:
        planetSeed = seedThing+currentPlanetNum+(int(distBinaryStarNum)*-1)
    else:
        planetSeed = seedThing+currentPlanetNum

    planetRNG.seed(planetSeed) # I'm throwing stuff at the wall to see what sticks. This one has tape on it, one-sided tape.

    # Set them to 0 because python is like that smh
    moonsGenerated = 0
    asteroidsGenerated = 0
    global totalPlanetsGenerated
    totalPlanetsGenerated = totalPlanetsGenerated + 1

    if typeOfStar == "MainSeq":
        starSizeToSun = starRadius/261600000
        if starSizeToSun >= 1:
            starSizeToSun = 1
    else:
        starSizeToSun = 1

    planetName = starN + "-" + alphabet[currentPlanetNum]

    allActions.append([time.localtime(),"Picking parameters for planet: " + planetName])
    state.allActionArrayUpdated = True

    print(planetName)
    allPlanets.append(planetName)
    gasGiant = False
    if planetRNG.randint(1,3) == 1:
        planetRadius = planetRNG.randint(100,800)*10000
        gasGiant = True
    else:
        planetRadius = planetRNG.randint(50,800)*1000
        gasGiant = False
    #planetRadius = random.randint(50,800)*1000
    #gasGiant = False
    if gasGiant == False:
        planetMass = (5.29151583439215E+22 / (600000/planetRadius)**3.7)
    else:
        planetMass = (4.23321273059351E+24 / (6000000/planetRadius)**3.7)

    print(typeOfStar + "AAYGAUYGYUFEYHUEYUHEGAHYAEUYHFUIAEFUIHASUIFASUFHUIASHFIUASHFASHFASASFASF")

    if typeOfStar == "MainSeq":
        if not gSMA == None:
            planetSMA = int(((planetRNG.randint(4500000000,5500000000)*currentPlanetNum)*(distanceThingamabob/261600000))+gSMA)
        else:
            planetSMA = int(((planetRNG.randint(4500000000,5500000000)*currentPlanetNum)*(starRadius/261600000)))
    elif typeOfStar == "Neutron":
        if not gSMA == None:
            planetSMA = int(((planetRNG.randint(4500000000,5500000000)*currentPlanetNum)*(distanceThingamabob/261600000))+gSMA)
        else:
            planetSMA = int(((planetRNG.randint(4500000000,5500000000)*currentPlanetNum)*(starRadius*2378/261600000)))*5
    elif typeOfStar == "RedGiant":
        if binaryParents == None:
            planetSMA = int(((planetRNG.randint(4500000000,5500000000)*currentPlanetNum)*(starRadius/261600000)))/8
        else:
            planetSMA = int(((planetRNG.randint(4500000000,5500000000)*currentPlanetNum)*(distanceThingamabob/261600000))+gSMA)/6
    elif typeOfStar == "BrownDwarf":
        if not gSMA == None:
            planetSMA = int(((planetRNG.randint(4500000000,5500000000)*currentPlanetNum)*(distanceThingamabob/261600000))+gSMA)
        else:
            planetSMA = int(((planetRNG.randint(4500000000,5500000000)*currentPlanetNum)*(starRadius/261600000)))/4
        planetRadius = int(planetRadius / 1.5)
    elif typeOfStar == "WhiteDwf":
        if not gSMA == None:
            planetSMA = int(((planetRNG.randint(4500000000,5500000000)*currentPlanetNum)*((distanceThingamabob)/261600000))+gSMA)
        else:
            planetSMA = int(((planetRNG.randint(4500000000,5500000000)*currentPlanetNum)*(starRadius*43.6/261600000)))*5
    elif typeOfStar == "WolfRayet":
        if not gSMA == None:
            planetSMA = int(((planetRNG.randint(4500000000,5500000000)*currentPlanetNum)*((distanceThingamabob)/261600000))+gSMA)
        else:
            planetSMA = int(((planetRNG.randint(4500000000,5500000000)*currentPlanetNum)*(starRadius/261600000)))*7
        inclinationLimits = [-25,25]
    else:
        if not gSMA == None:
            planetSMA = int(((planetRNG.randint(4500000000,5500000000)*currentPlanetNum)*(distanceThingamabob/261600000))+gSMA)
            print("AYUAGYUGHYURHYGURSYUGHSREHUYSRGHYUIRSHYUGHYUSRGHUYRGSUHYGRSUYRHSGUYHGYU*IRSHYURGHYURGHYUR BALLS BVALLB BALLS BALLS BALL WR WR WR WR AHHHH")
        else:
            planetSMA = int(((planetRNG.randint(4500000000,5500000000)*currentPlanetNum)*(starRadius/261600000)))

    if currentPlanetNum > 1:
        maxMoonsPossible = round(np.interp(planetSMA, [0,68773560320*(starMass/1.75654591319326E+28)*(5.29151583439215E+22/planetMass)], [0,AmountOfMoonsToGenerate]))
        moonAmount = int(planetRNG.randint(0,maxMoonsPossible))
    else:
        moonAmount = 0

    if gasGiant == True:
        maxAsteroidsPossible = round(np.interp(planetSMA, [0,68773560320*(starMass/1.75654591319326E+28)*(5.29151583439215E+22/planetMass)], [0,AmountOfAsteroidsToGenerate]))
        asteroidAmount = int(planetRNG.randint(0,maxAsteroidsPossible))
    else:
        if planetRNG.randint(1,2) == True:
            maxAsteroidsPossible = round(np.interp(planetSMA, [0,68773560320*(starMass/1.75654591319326E+28)*(5.29151583439215E+22/planetMass)], [0,AmountOfAsteroidsToGenerate]))
            asteroidAmount = int(planetRNG.randint(0,maxAsteroidsPossible)/2)
        else:
            asteroidAmount = 0

    if typeOfStar == "BrownDwarf":
        moonAmount = 0
        asteroidAmount = 0

    print("Number Of Moons For " + planetName + ": " + str(moonAmount))

    #if binaryTypes[0] == "WolfRayet" or binaryTypes[0] == "WolfRayet":
    #    inclinationLimits = [-25,25]

    try:
        inclinationLimits
    except:
        inclinationLimits = [0,10]

    atmoPress = 0
    atmClrR = 0
    atmClrG = 0
    atmClrB = 0
    sctrClrR = 0
    sctrClrG = 0
    sctrClrB = 0

    if planetRadius > 300000:
        atmo = "Atmospheric"
        vacuum = False
        if gasGiant == True:
            atmoPress = planetRNG.randint(200,1600)
        else:
            lessOrMore = planetRNG.choice([0,1,2])
            if lessOrMore == 1:
                numberguy = planetRNG.randint(100,1000)
            else:
                numberguy = planetRNG.randint(1,100)
            atmoPress = numberguy*((planetRadius/600000)*0.5)
    else:
        atmo = "Vacuum"
        vacuum = True
            
    # Tidally locked or not? This is where we find that out!
    tdSMAmult = starRadius/261600000
    requiredTidalLockingSMA = int(5263138304/0.5) # Moho's SMA divided by a number. 13526298302
    finalTidalLockingSMA = requiredTidalLockingSMA/tdSMAmult

    #if binaryParents == None:
    if not typeOfStar == "Neutron" and not typeOfStar == "WhiteDwf" and not typeOfStar == "RedGiant":
        if atmoPress < 400:
            if moonAmount > 0:
                randomshit = planetRNG.randint(0,2)
                if randomshit == 0:
                    if planetSMA < finalTidalLockingSMA:
                        print("At an SMA of " + str(planetSMA) + ", the planet " + planetName + " is tidally locked.")
                        tidallyLocked = True
                    else:
                        tidallyLocked = False
                else:
                    tidallyLocked = False
            else:
                if planetSMA < finalTidalLockingSMA:
                    print("At an SMA of " + str(planetSMA) + ", the planet " + planetName + " is tidally locked.")
                    tidallyLocked = True
                else:
                    tidallyLocked = False
        else:
            tidallyLocked = False
    else:
        tidallyLocked = False
    #else:
    #    tidallyLocked = False

    starLum = Lum
    starLumMult = starLum/1360
    smaMult = 13599840256/planetSMA

    pressureMultiplier = atmoPress/100

    randomGreenhouse = planetRNG.randint(5,20)/10

    vacuumTemp = 233*starLumMult*smaMult # Base temperature without any greenhouse.

    if gasGiant == False:
        greenhouse = 80*(pressureMultiplier*randomGreenhouse) # Additional temperature to add above the base temperature, assuming there's an atmosphere.
    else:
        greenhouse = 1

    finalTemp = round(vacuumTemp + greenhouse)
    if atmo == "Atmospheric":
        if gasGiant == False:
            if finalTemp > 100 and finalTemp < 500:
                if planetRNG.randint(1,2) == 1:
                    ocean = True
                else:
                    ocean = False
            else:
                ocean = False
        else:
            ocean = False
    else:
        ocean = False

    if finalTemp < 200 and planetRNG.randint(1,2) == 1:
        icy = True
    else:
        icy = False

    possibleLife = []

    if finalTemp > 223 and finalTemp < 373:
        if gasGiant == False and ocean == True and atmo == "Atmospheric" and atmoPress > 10:
            if planetRNG.randint(0,0) == 0: # Juuuuuuust in case I want it to be rarer.
                possibleLife.append("organic")
    if finalTemp < 223 or finalTemp > 373:
        if gasGiant == False and atmo == "Atmospheric":
            if planetRNG.randint(0,5) == 0:
                possibleLife.append("exotic")
    if finalTemp < 223 and gasGiant == False and ocean == False and atmo == "Vacuum" and icy == True:
        if planetRNG.randint(0,3) == 0:
            possibleLife.append("subglacial")
    if gasGiant == True or atmoPress > 700:
        if planetRNG.randint(0,3) == 0:
            possibleLife.append("aerial")

    if len(possibleLife) > 0:
        life = random.choice(possibleLife)
        if life == "organic":
            oxygen = True
            atmClrR = planetRNG.randint(100,200)
            atmClrG = planetRNG.randint(75,150)
            atmClrB = planetRNG.randint(0,50)
        else:
            oxygen = False
            atmClrR = planetRNG.randint(0,200)
            atmClrG = planetRNG.randint(0,200)
            atmClrB = planetRNG.randint(0,200)
    else:
        oxygen = False
        life = None
        atmClrR = planetRNG.randint(0,200)
        atmClrG = planetRNG.randint(0,200)
        atmClrB = planetRNG.randint(0,200)

    sctrClrR = (atmClrR*-1)+255
    sctrClrG = (atmClrG*-1)+255
    sctrClrB = (atmClrB*-1)+255

    if Settings.fantasyNames == True:
        if atmo == "Atmospheric":
            if finalTemp > 600:
                dispName = processName(planetSeed,lavaTransisionTable,10)
            elif finalTemp < 100:
                dispName = processName(planetSeed,icyTransisionTable,10)
            elif ocean == True:
                if not life == None:
                    dispName = processName(planetSeed,lifeTransisionTable,10)
                else:
                    dispName = processName(planetSeed,oceanicTransisionTable,10)
            elif gasGiant == True:
                dispName = processName(planetSeed,gaseousTransisionTable,10)
            else:
                dispName = processName(planetSeed,rockyTransisionTable,10)
        else:
            dispName = processName(planetSeed,vacuumTransisionTable,10)
    else:
        dispName = planetName

    print("Display name for " + planetName + " is " + dispName)

    black = Color("#000000")
    Pcolors1 = list(black.range_to(Color("#700000"),5))
    red = Color("#700000")
    Pcolors2 = list(red.range_to(Color("#9e008c"),90))
    pink = Color("#9e008c")
    Pcolors3 = list(pink.range_to(Color("#fcf2fa"),5))
    PfinalColors = Pcolors1 + Pcolors2 + Pcolors3

    PMult = starRadius*30 / 261600000
    if PMult > len(PfinalColors):
        PMult = len(PfinalColors)
    PmultRound = round(PMult)
    plantColor = Color.get_rgb(PfinalColors[PmultRound-1])

    if atmo == "Atmospheric" and finalTemp >= 50 and finalTemp <= 300:
        icecaps = True
    else:
        icecaps = False

    oceanR = planetRNG.randint(5,20)
    oceanG = planetRNG.randint(5,35)
    oceanB = planetRNG.randint(10,75)

    moon = False
    
    if gasGiant == True:
        terrainR = planetRNG.randint(50,255)
        terrainG = planetRNG.randint(50,255)
        terrainB = planetRNG.randint(50,255)

        terrainClr = "RGBA(" + str(terrainR) + ", " + str(terrainG) + ", " + str(terrainB) + ", 100)"
    else:
        terrainR = planetRNG.randint(50,175)
        terrainG = planetRNG.randint(50,175)
        terrainB = planetRNG.randint(50,175)

        terrainClr = "RGBA(" + str(terrainR) + ", " + str(terrainG) + ", " + str(terrainB) + ", 100)"

    if atmo == "Atmospheric" and gasGiant == False:
        templ = 1
    elif atmo == "Atmospheric" and gasGiant == True:
        templ = 4
    elif atmo == "Vacuum":
        templ = 0

    #if gasGiant == False:
    #    if random.randint(1,1) == 1:
    #        if random.randint(0,1) == 1:
    #            print("??????????!!!?!??")
    #            anomaly = "crshShp"
    #            anLat = random.randint(-45,45)
    #            anLon = random.randint(-180,180)
    #        else:
    #            print("?????????")
    #            anomaly = "fltStrc"
    #            anLat = random.randint(-45,45)
    #            anLon = random.randint(-180,180)
    #        anLatLon = [anLat,anLon]
    #    else:
    #        anomaly = "None"
    #        anLatLon = []
    #else:
    #    anomaly = "None"
    #    anLatLon = []
    anLatLon = []
    anomaly = "None"
    #print(anLatLon)

    #print("-------Physical Values-------")
    #print("Radius: " + str(planetRadius))
    #print("Mass: " + str(planetMass))
    #print("Semimajor Axis: " + str(planetSMA))
    #print("Terrain tint: " + str(terrainClr))
    #if life == True:
    #    print("Has life!")

    #print("-------Atmosphere Values-------")
    #if atmo == "Atmospheric":
    #    print("Atmosphere scattering color: " + str(atmClrR) + " " + str(atmClrG) + " " + str(atmClrB))
    #    print("Atmosphere main color: " + str(sctrClrR) + " " + str(sctrClrG) + " " + str(sctrClrB))
    #    print("kPa at sea level: " + str(atmoPress))
    #    print("Temperature at sea level: " + str(finalTemp) + " kelvin.")
    #    if oxygen == True:
    #        print("Oxygenated!")
    #else:
    #    print("No atmosphere!")

    #print("-------------------------------")

    if planetRNG.randint(1,2) == 1:
        geoActive = True
        if planetRNG.randint(1,2) == 1:
            activeVolcano = True
        else:
            activeVolcano = False
    else:
        geoActive = False
        activeVolcano = False

    if finalTemp > 700:
        lava = True
        if round(finalTemp/100) < 17:
            lavaClr = (lavaSpectrum[round(finalTemp/100)])
        else:
            lavaClr = lavaSpectrum[16]
    else:
        lava = False
        lavaClr = Color("#000000")

    lavaClrRGB = Color.get_rgb(lavaClr)

    if planetRNG.randint(0,3) == 0:
        oceanFactor = planetRNG.randint(16,255)
    else:
        oceanFactor = planetRNG.randint(16,128)

    planetCfg = open(targetPath + "/Configs/" + planetName + ".cfg","x")
    if gasGiant == True:
        generateGasGiantMaps(planetSeed, terrainR, terrainG, terrainB, planetName, allActions, targetPath, base_dir, canConvertToDDS)
    else:
        #rockyPlanetMapThread = threading.Thread(target=GeneratePlanetMaps, args=(vacuum, terrainR, terrainG, terrainB, planetName, ocean, oceanR, oceanG, oceanB, atmoPress, geoActive, icecaps, finalTemp, life, plantColor, planetRadius, anomaly, anLatLon, activeVolcano, lava))
        #rockyPlanetMapThread.run()
        generatePlanetMaps(vacuum, terrainR, terrainG, terrainB, planetName, ocean, oceanR, oceanG, oceanB, atmoPress, geoActive, icecaps, finalTemp, life, plantColor, planetRadius, anomaly, anLatLon, activeVolcano, lava, tidallyLocked, oceanFactor, False, planetSeed, icy, allActions, base_dir, lavaSpectrum, everythingEnded, targetPath, canConvertToDDS)
    
    ringChance = int((AmountOfPlanetsToGenerate - currentPlanetNum)+1)

    #print("Ring chance: 1 in " + str(ringChance))
    if ringChance < 1:
        print("I'm not sure what kind of black magic was performed to cause this stupid thing to happen, but the ring change is 1 in 0. Don't worry, the program will continue as usual.")
        print("No rings were generated.")
        rings = False
        ringInn = 2000
        ringOut = 2001
    else:
        if planetRNG.randint(1,ringChance) == 1:
            print("RINGS!")
            print("-------------------------------")
            rings = True
            genRing(planetSeed, planetName, targetPath)
            ringInn = planetRNG.randint(1000,4000)
            ringOut = ringInn + planetRNG.randint(100,3000)
        else:
            rings = False
            ringInn = 2000
            ringOut = 2001

    atmoHeight = planetRNG.randint(50,90)*1000

    if ocean == True:
        addToOceanCfg(planetSeed, oceanCfg, oceanR, oceanG, oceanB, planetName, allActions)

    if atmo == "Atmospheric":
        addToAtmoCfg(atmoCfg, starN, planetName, starColor, sctrClrR, sctrClrG, sctrClrB, ocean, gasGiant, atmoHeight, atmoPress, allActions)
        if binaryParents == None:
            if distBinaryParents == None:
                addToScattererList(listCfg, starN, planetName, starColor, ocean, colorsRound)
            else:
                addToScattererList(listCfg, starN, planetName, starColor, ocean, colorsRound, None, distBinaryParents)
        else:
            addToScattererList(listCfg, starN, planetName, starColor, ocean, colorsRound, binaryParents)
        if gasGiant == False:
            if ocean == True or planetRNG.randint(1,2) == 1:
                if tidallyLocked == True:
                    cloudTexNum = planetRNG.randint(1,3)
                else:
                    cloudTexNum = planetRNG.randint(1,5)
                addToEVECfg(eveCfg, cloudTexNum, planetName, tidallyLocked, allActions)
                addToVolumetricEveCfg(planetSeed, VolumetricEveCfg, cloudTexNum, planetName, tidallyLocked, ocean)
            if atmoPress > 10:
                auroraBright = planetRNG.randint(128,255)
                aurR = planetRNG.randint(0,255)
                aurG = planetRNG.randint(100,255)
                aurB = planetRNG.randint(0,255)
                auroraClr = (aurR,aurG,aurB)
                addToEVEAurora(VolumetricEveCfg, planetName, auroraBright, auroraClr)
        else:
            auroraBright = planetRNG.randint(200,512)
            aurR = planetRNG.randint(0,255)
            aurG = planetRNG.randint(0,255)
            aurB = 255
            auroraClr = (aurR,aurG,aurB)
            addPQSFix(evePQSCfg, planetName)
            addToEVECfg(eveCfg, 1, planetName, tidallyLocked, planetName, allActions)
            addToVolumetricEveCfg(planetSeed, VolumetricEveCfg, 1, planetName, tidallyLocked, ocean, planetName)
            addToEVEAurora(eveCfg, planetName, auroraBright, auroraClr)
            if finalTemp > 700:
                generateSuperheatedClouds(eveCfg,planetName,finalTemp, colorsReversed, colorsys)
                generateSuperheatedClouds(VolumetricEveCfg,planetName,finalTemp, colorsReversed, colorsys)

    if atmo == "Atmospheric":
        if ocean == True:
            if icy == True:
                groundType = 3
            else:
                groundType = planetRNG.choice([0,1,2])
        else:
            if icy == True:
                groundType = 3
            else:
                groundType = planetRNG.choice([0,1,2])
    else:
        if icy == True:
            groundType = 3
        else:
            groundType = planetRNG.choice([0,1,2])

    if gasGiant == False:
        addSubdividerFix(subdfixCfg, planetName)
        addToParallaxCfg(planetSeed, parallaxCfg, planetName, lava, lavaClrRGB, groundType, icy, allActions)
        addToParallaxScatterFixCfg(parallax_scatterfix_Cfg, planetName)
        addParallaxScatter(planetSeed, parallax_scatter_Cfg, planetName, life, plantColor, planetRadius)

    Tag = "InfD_Planet"

    sciValue = 3

    if atmo == "Atmospheric":
        sciValue += 5

    if ocean == True:
        sciValue += 10

    if life == "Organic":
        sciValue += 15
    elif life == "Exotic":
        sciValue += 25
    elif life == "Aerial":
        sciValue += 20
    elif life == "Subglacial":
        sciValue += 10

    if lava == True:
        sciValue += 10

    if icy == True:
        sciValue += 5

    createResourceConfig(planetSeed,rationalResources_Cfg,planetName,lava,icy,finalTemp,atmoPress,ocean,gasGiant,life,None)
    writeBodyCfg(planetSeed, planetCfg, planetName, planetRadius, planetMass, planetSMA, starN, atmo, atmoPress, templ, atmClrR, atmClrG, atmClrB, sctrClrR, sctrClrG, sctrClrB, terrainClr, moon, gasGiant, rings, ringInn, ringOut, ocean, oceanR, oceanG, oceanB, atmoHeight, finalTemp, oxygen, life, dispName, anomaly, anLatLon, Tag, lava, tidallyLocked, oceanFactor, False, icy, inclinationLimits, sciValue, allActions, templates, canConvertToDDS)
    
    moonDistMult = planetRNG.randint(10,50)/10
    for a in range(moonAmount):
        moonsGenerated = moonsGenerated + 1
        moonNum = a
        if binaryParents == None:
            #generateMoonThread = threading.Thread(target=generateMoon, args=(planetName, moonsGenerated, planetRadius, gasGiant, atmoCfg, starN, starColor, listCfg, colorsRound, oceanCfg, eveCfg, Lum, planetSMA, starRadius, parallaxCfg, subdfixCfg))
            #generateMoonThread.start()
            if distBinaryParents == None:
                generateMoon(planetSeed, a, planetName, moonsGenerated, planetRadius, gasGiant, atmoCfg, starN, starColor, listCfg, colorsRound, oceanCfg, eveCfg, VolumetricEveCfg, Lum, planetSMA, starRadius, parallaxCfg, subdfixCfg, parallax_scatterfix_Cfg, parallax_scatter_Cfg, rationalResources_Cfg, moonDistMult, False)
            else:
                generateMoon(planetSeed, a, planetName, moonsGenerated, planetRadius, gasGiant, atmoCfg, starN, starColor, listCfg, colorsRound, oceanCfg, eveCfg, VolumetricEveCfg, Lum, planetSMA, starRadius, parallaxCfg, subdfixCfg, parallax_scatterfix_Cfg, parallax_scatter_Cfg, rationalResources_Cfg, moonDistMult, False, None, distBinaryParents, distBinaryStarNum)
        else:
            #generateMoonThread = threading.Thread(target=generateMoon, args=(planetName, moonsGenerated, planetRadius, gasGiant, atmoCfg, starN, starColor, listCfg, colorsRound, oceanCfg, eveCfg, Lum, planetSMA, starRadius, parallaxCfg, subdfixCfg, binaryParents))
            #generateMoonThread.start()
            generateMoon(planetSeed, a, planetName, moonsGenerated, planetRadius, gasGiant, atmoCfg, starN, starColor, listCfg, colorsRound, oceanCfg, eveCfg, VolumetricEveCfg, Lum, planetSMA, starRadius, parallaxCfg, subdfixCfg, parallax_scatterfix_Cfg, parallax_scatter_Cfg, rationalResources_Cfg, moonDistMult, False, binaryParents)

    for b in range(asteroidAmount):
        asteroidsGenerated = asteroidsGenerated + 1
        if binaryParents == None:
            #generateMoonThread = threading.Thread(target=generateMoon, args=(planetName, moonsGenerated, planetRadius, gasGiant, atmoCfg, starN, starColor, listCfg, colorsRound, oceanCfg, eveCfg, Lum, planetSMA, starRadius, parallaxCfg, subdfixCfg))
            #generateMoonThread.start()
            if distBinaryParents == None:
                generateMoon(planetSeed, b, planetName, asteroidsGenerated, planetRadius, gasGiant, atmoCfg, starN, starColor, listCfg, colorsRound, oceanCfg, eveCfg, VolumetricEveCfg, Lum, planetSMA, starRadius, parallaxCfg, subdfixCfg, parallax_scatterfix_Cfg, parallax_scatter_Cfg, rationalResources_Cfg, moonDistMult, True)
            else:
                generateMoon(planetSeed, b, planetName, asteroidsGenerated, planetRadius, gasGiant, atmoCfg, starN, starColor, listCfg, colorsRound, oceanCfg, eveCfg, VolumetricEveCfg, Lum, planetSMA, starRadius, parallaxCfg, subdfixCfg, parallax_scatterfix_Cfg, parallax_scatter_Cfg, rationalResources_Cfg, moonDistMult, True, None, distBinaryParents, distBinaryStarNum)
        else:
            #generateMoonThread = threading.Thread(target=generateMoon, args=(planetName, moonsGenerated, planetRadius, gasGiant, atmoCfg, starN, starColor, listCfg, colorsRound, oceanCfg, eveCfg, Lum, planetSMA, starRadius, parallaxCfg, subdfixCfg, binaryParents))
            #generateMoonThread.start()
            generateMoon(planetSeed, b, planetName, asteroidsGenerated, planetRadius, gasGiant, atmoCfg, starN, starColor, listCfg, colorsRound, oceanCfg, eveCfg, VolumetricEveCfg, Lum, planetSMA, starRadius, parallaxCfg, subdfixCfg, parallax_scatterfix_Cfg, parallax_scatter_Cfg, rationalResources_Cfg, moonDistMult, True, binaryParents)

    amountOfThingsDone += 1

# Picks parameters for stars
def generateStar(starSeed, AmountOfPlanetsToGenerate, systemName, targetFilepath, parentBarycenter=None, binarySMA=None, binaryP=None, binaryRad=None, maaoD=None, baryOrder=None, starType=None, binaryType=None, binaryEccentricity=None):
    print(str(starType) + " sooooooooooooo like it's right and all but????")
    #print(str(starType) + " BRUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUH")
    
    global targetPath
    targetPath = targetFilepath
    global planetsGenerated
    planetsGenerated = 0
    global totalSystemsGenerated
    global totalStarsGenerated

    starGenRNG = random.Random()
    starGenRNG.seed(starSeed)

    if parentBarycenter == None:
        totalSystemsGenerated = totalSystemsGenerated + 1
        parentGalaxy = availableGalaxies[starGenRNG.randint(0,len(availableGalaxies)-1)]
        if Settings.starTypeOverride == None:
            typeOfStar = starGenRNG.randint(0,175)
        else:
            try:
                typeOfStar = Settings.starTypeOverride
            except:
                print('Incredible star type override failue, check if it is "None" or a number.')
                typeOfStar = starGenRNG.randint(0,175)
    else:
        allActions.append([time.localtime(),"Generating star: " + systemName + str(baryOrder)])
        state.allActionArrayUpdated = True
        typeOfStar = starType

    totalStarsGenerated = totalStarsGenerated + 1
    
    print(typeOfStar)
    if 0 <= typeOfStar <= 18:
        redGiant = True
    elif 19 <= typeOfStar <= 28:
        whiteDwarf = True
    elif 29 <= typeOfStar <= 39:
        neutron = True
    elif 40 <= typeOfStar <= 50:
        brownDwarf = True
    elif 51 <= typeOfStar <= 55:
        wolfRayet = True
    else:
        mainSeq = True
        
    if parentBarycenter == None:
        starName = str(alphabet[starGenRNG.randint(0,len(alphabet)-1)]) + str(alphabet[starGenRNG.randint(0,len(alphabet)-1)]) + "-" + str(starGenRNG.randint(0,99999))
        allActions.append([time.localtime(),"Generating system: " + starName])
    else:
        starName = systemName + str(baryOrder)

    try:
        if mainSeq:
            print("Main sequence")
            starTypeStr = "MainSeq"
            if parentBarycenter == None:
                Tag = "InfD_Star"
            else:
                if binaryType == "Distant":
                    Tag = "InfD_DistantBinaryStar"
                else:
                    Tag = "InfD_BinaryStar"
            minStarSize = Settings.minStarSize
            maxStarSize = Settings.maxStarSize

            if binaryRad == None:
                randomSizeType = starGenRNG.randint(1,3)
                if randomSizeType == 1:
                    starRadius = starGenRNG.randint(minStarSize,maxStarSize)
                else:
                    starRadius = starGenRNG.randint(minStarSize,maxStarSize/6)
                #starRadius =  math.floor(abs(random.random() - random.random()) * (10 + maxStarSize - minStarSize) + minStarSize)
                starMass = starRadius * 6.7146251e+19
            else:
                starRadius =  binaryRad
                starMass = starRadius * 6.7146251e+19

            coronaMult = (starRadius*10 / 261600000)/200
            coronaMultRound = round(coronaMult)

            mult = int(getStarColorMult(starRadius))

            print(mult)

            if mult < 100 and mult > 0:
                starColorHex = colorsReversed[mult]
                starColor = Color.get_rgb(Color(starColorHex))
                RGBfinal = str(starColor)[1:][:-1]
                print(starColorHex)
                print(RGBfinal)
            elif mult >= 100:
                starColorHex = colorsReversed[99]
                starColor = Color.get_rgb(Color(starColorHex))
                RGBfinal = str(starColor)[1:][:-1]
                print(starColorHex)
                print(RGBfinal)
            elif mult < 0:
                starColorHex = colorsReversed[0]
                starColor = Color.get_rgb(Color(starColorHex))
                RGBfinal = str(starColor)[1:][:-1]
                print(starColorHex)
                print(RGBfinal)
            
            Lum = 1360 * starRadius / 261600000
            
            planetsNum = starGenRNG.randint(minPlanets,AmountOfPlanetsToGenerate)

            if mult > 0 and mult <= 20:
                coronaColor = "coronaRed"
            elif mult > 20 and mult <= 40:
                coronaColor = "coronaOrange"
            elif mult > 40 and mult <= 50:
                coronaColor = "coronaYellow"
            elif mult > 50 and mult <= 70:
                coronaColor = "coronaWhite"
            else:
                coronaColor = "coronaBlue"
    except UnboundLocalError:
        #print("God why")
        #logging.error(traceback.format_exc())
        #print(traceback.format_exc())
        #input("Type anything or press enter to close: ")
        pass
    try:
        if wolfRayet:
            print("Wolf Rayet")
            starTypeStr = "WolfRayet"
            if parentBarycenter == None:
                Tag = "InfD_WolfRayet"
            else:
                if binaryType == "Distant":
                    Tag = "InfD_DistantBinaryWolfRayet"
                else:
                    Tag = "InfD_BinaryWolfRayet"
            minStarSize = 130800000 #Settings.minStarSize
            maxStarSize = 6016800000 #Settings.maxStarSize

            if binaryRad == None:
                starRadius =  int(math.floor(abs(starGenRNG.random() - starGenRNG.random()) * (10 + maxStarSize - minStarSize) + minStarSize))
                starMass = (((starRadius/10)/261600000) * 1.75654591319326E+28)*15
            else:
                starRadius =  binaryRad
                starMass = (((starRadius)/261600000) * 1.75654591319326E+28)*15

            #Mult = (starRadius*10 / 261600000)/200
            #multRound = round(Mult)
            starColor = Color.get_rgb(Color("#568bff"))
            RGBfinal = str(starColor)[1:][:-1]
            Lum = (((starRadius)/261600000)*15) * 1200
            
            planetsNum = starGenRNG.randint(minPlanets,AmountOfPlanetsToGenerate)/2

            coronaColor = "None"
    except UnboundLocalError:
        pass
    try:
        if redGiant:
            print("Red Giant")
            starTypeStr = "RedGiant"
            if parentBarycenter == None:
                Tag = "InfD_RedGiant"
            else:
                if binaryType == "Distant":
                    Tag = "InfD_DistantBinaryRedGiant"
                else:
                    Tag = "InfD_BinaryRedGiant"
            minStarSize = 66160000 #Settings.minStarSize
            maxStarSize = 784800000 #Settings.maxStarSize

            if binaryRad == None:
                starRadius =  int(math.floor(abs(starGenRNG.random() - starGenRNG.random()) * (10 + maxStarSize - minStarSize) + minStarSize)*10)
                starMass = (starRadius/10) * 6.7146251e+19
            else:
                starRadius =  binaryRad
                starMass = starRadius * 6.7146251e+19

            #Mult = (starRadius*10 / 261600000)/200
            #multRound = round(Mult)
            starColor = Color.get_rgb(Color("#fa4b28"))
            RGBfinal = str(starColor)[1:][:-1]
            Lum = (1360 * (starRadius/4) / 261600000)
            
            planetsNum = starGenRNG.randint(minPlanets,AmountOfPlanetsToGenerate)/1.5

            coronaColor = "None"
    except UnboundLocalError:
        pass
    try:
        if whiteDwarf:
            print("White Dwarf")
            starTypeStr = "WhiteDwf"
            if parentBarycenter == None:
                Tag = "InfD_WhiteDwarfStar"
            else:
                if binaryType == "Distant":
                    Tag = "InfD_DistantBinaryWhiteDwarfStar"
                else:
                    Tag = "InfD_BinaryWhiteDwarfStar"
            minStarSize = 500000
            maxStarSize = 700000

            if binaryRad == None:
                starRadius =  (math.floor(abs(starGenRNG.random() - starGenRNG.random()) * (10 + maxStarSize - minStarSize) + minStarSize))*4.24
                starMass = (((starRadius/4.42) * 6.7146251e+19)*436)/2
            else:
                starRadius =  binaryRad
                starMass = (((starRadius/4.42) * 6.7146251e+19)*436)/2

            #Mult = 33
            #multRound = round(Mult)
            starColor = Color.get_rgb(Color(colorsReversed[50]))
            RGBfinal = str(starColor)[1:][:-1]
            Lum = 150
            
            planetsNum = starGenRNG.randint(minPlanets,AmountOfPlanetsToGenerate)/2

            coronaColor = "None"
    except UnboundLocalError:
        pass
    try:
        if neutron:
            print("Neutron Star")
            starTypeStr = "Neutron"
            if parentBarycenter == None:
                Tag = "InfD_NeutronStar"
            else:
                if binaryType == "Distant":
                    Tag = "InfD_DistantBinaryNeutronStar"
                else:
                    Tag = "InfD_BinaryNeutronStar"
            minStarSize = Settings.minStarSize
            maxStarSize = Settings.maxStarSize

            if binaryRad == None:
                starRadius =  48000
                starMass = 3.5130918e+28
            else:
                starRadius =  binaryRad
                starMass = 3.5130918e+28

            #Mult = 80
            #multRound = round(Mult)
            starColor = Color.get_rgb(Color(colorsReversed[75]))
            RGBfinal = str(starColor)[1:][:-1]
            Lum = 1260
            
            diskRadius = starGenRNG.randint(3000000000,6000000000)
            generateDisks(starName, diskRadius, targetPath)

            planetsNum = starGenRNG.randint(minPlanets,AmountOfPlanetsToGenerate)/1.5

            coronaColor = "None"
    except UnboundLocalError:
        pass
    try:
        if brownDwarf:
            print("Brown Dwarf")
            starTypeStr = "BrownDwarf"
            if parentBarycenter == None:
                Tag = "InfD_BrownDwfStar"
            else:
                if binaryType == "Distant":
                    Tag = "InfD_DistantBinaryBrownDwfStar"
                else:
                    Tag = "InfD_BinaryBrownDwfStar"
            minStarSize = 5592000
            maxStarSize = 10487000

            if binaryRad == None:
                starRadius =  (math.floor(abs(starGenRNG.random() - starGenRNG.random()) * (10 + maxStarSize - minStarSize) + minStarSize))*4.24
                starMass = (((starRadius/4.42) * 6.7146251e+19))*10
            else:
                starRadius =  binaryRad
                starMass = (starRadius * 6.7146251e+19)*3

            #Mult = 1
            #multRound = round(Mult)
            starColor = Color.get_rgb(Color(colorsReversed[5]))
            RGBfinal = str(starColor)[1:][:-1]
            Lum = 1360 * (starRadius / 261600000)/8
            
            planetsNum = starGenRNG.randint(minPlanets,AmountOfPlanetsToGenerate)/1.5

            coronaColor = "None"
    except UnboundLocalError:
        pass

    # Wolf Rayet Thingamajigs
    if binaryType == "Distant" or parentBarycenter == None:
        if starTypeStr == "WolfRayet":
            generateNebula(starName, base_dir)

    # Not type-specific settings.
    if parentBarycenter == None:
        starDist = starGenRNG.randint(Settings.minStarDistance,Settings.maxStarDistance)
        if parentGalaxy == "LKC_CtrlB":
            starDistG = starGenRNG.randint(Settings.minStarDistance/5,Settings.maxStarDistance*10)/3.5
        elif parentGalaxy == "SKC_CtrlB":
            starDistG = starGenRNG.randint(Settings.minStarDistance/5,Settings.maxStarDistance*10)/11
        else:
            starDistG = starGenRNG.randint(Settings.minStarDistance/5,Settings.maxStarDistance*10)
    else:
        starDist = binarySMA
        starDistG = binarySMA

    dispName = processName(starSeed, starTransisionTable, 10)

    #if parentBarycenter == None:
    print("Number of planets for " + dispName + "(" + starName + "): " + str(int(planetsNum)))

    colorsRound = (starColor[0] + starColor[1] + starColor[2])/3

    starCfg = open(targetPath + "/Configs/" + starName + ".cfg","x")

    print("-------------------------------------------------------")
    print(starName + " is a " + starTypeStr)
    print(" ")
    print("Star radius: " + str(starRadius) + " meters.")
    print("Star mass: " + str(starMass) + " kilograms.")
    print("Star luminosity: " + str(Lum) + " (" + str(Lum/1360) + " times Kerbol's luminosity!)")
    print("-------------------------------------------------------")

    if parentBarycenter == None:
        writeStarCfg(starSeed, starCfg, starName, starRadius, starMass, starDist, RGBfinal, starDistG, dispName, Tag, starTypeStr, Lum, coronaColor, None, None, None, parentGalaxy, allActions=allActions, AmountOfAsteroidsToGenerate=AmountOfAsteroidsToGenerate, AmountOfMoonsToGenerate=AmountOfMoonsToGenerate, AmountOfPlanetsToGenerate=AmountOfPlanetsToGenerate, minPlanets=minPlanets, minMoons=minMoons)
    else:
        writeStarCfg(starSeed, starCfg, starName, starRadius, starMass, starDist, RGBfinal, starDistG, dispName, Tag, starTypeStr, Lum, coronaColor, parentBarycenter, binaryP, maaoD, None, binaryEccentricity, binaryType, allActions, AmountOfMoonsToGenerate, AmountOfAsteroidsToGenerate, AmountOfPlanetsToGenerate, minPlanets, minMoons)

    if parentBarycenter == None or binaryType == "Distant":
        #if binaryType == "Distant":
        #    if planetsNum > 9:
        #        planetsNum == 9
        #    planetsNum = planetsNum/1.5
        listCfg = open(targetPath + "/Visuals/Scatterer/" + starName + "_ScattererList" + ".cfg","x")
        listCfg.write(
            "@Scatterer_planetsList:FINAL\n"
            "{\n"
            "    @scattererCelestialBodies\n"
            "    {\n"
        )
        atmoCfg = open(targetPath + "/Visuals/Scatterer/" + starName + "_ScattererAtmo" + ".cfg","x")
        atmoCfg.write(
            "Scatterer_atmosphere\n"
            "{\n"
        )
        oceanCfg = open(targetPath + "/Visuals/Scatterer/" + starName + "_ScattererOcean" + ".cfg","x")
        oceanCfg.write(
            "Scatterer_ocean\n"
            "{\n"
        )
        eveCfg = open(targetPath + "/Visuals/EVE/Configs/" + starName + "_EVE" + ".cfg","x")
        eveCfg.write(
            "EVE_CLOUDS:NEEDS[!Infinite_VolumetricClouds]\n"
            "{\n"
        )
        VolumetricEveCfg = open(targetPath + "/Visuals/EVE/Configs/" + starName + "_VOLUMEEVE" + ".cfg","x")
        VolumetricEveCfg.write(
            "EVE_CLOUDS:NEEDS[Infinite_VolumetricClouds]\n"
            "{\n"
        )
        evePQSCfg = open(targetPath + "/Visuals/EVE/Configs/" + starName + "_PQSFIX" + ".cfg","x")
        evePQSCfg.write(
            "PQS_MANAGER\n"
            "{\n"
        )
        parallaxCfg = open(targetPath + "/Visuals/Parallax/Configs/" + starName + "_PARALLAX" + ".cfg","x")
        parallaxCfg.write(
            "Parallax\n"
            "{\n"
        )
        parallax_subd_Cfg = open(targetPath + "/Visuals/Parallax/Configs/" + starName + "_PARALLAX_SUBDFIX" + ".cfg","x")
        parallax_subd_Cfg.write(
            "@Kopernicus:LAST[InfiniteDiscoveries]:NEEDS[Parallax]\n"
            "{\n"
        )
        parallax_scatterfix_Cfg = open(targetPath + "/Visuals/Parallax/Configs/" + starName + "_PARALLAX_SCATTERFIX" + ".cfg","x")
        parallax_scatterfix_Cfg.write(
            "@Kopernicus:LAST[InfiniteDiscoveries]:NEEDS[Parallax]\n"
            "{\n"
        )
        # Empty for now.
        parallax_scatter_Cfg = open(targetPath + "/Visuals/Parallax/Configs/" + starName + "_PARALLAX_SCATTERS" + ".cfg","x")

        rationalResources_Cfg = open(targetPath + "/Misc/RR/" + starName + "_RationalResources" + ".cfg","x")
        createResourceConfig(starSeed,rationalResources_Cfg,starName,False,False,0,0,False,False,None,starTypeStr)

        sunfCfg = open(targetPath + "/Visuals/Scatterer/" + starName + "_ScattererSunflare" + ".cfg","x")
        addSunflareCfg(sunfCfg, starColor, starName, starTypeStr, colorsys)

        allPlanetThreads = []

        if binaryType == "Distant":
            distBinaryParents = [systemName + "-1", systemName + "-2"]

        if binaryType == "Distant":
            for x in range(int(planetsNum)):
                if everythingEnded == True:
                    raise Exception("UI thread isn't running.")
                print("wowowowowowowowoooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooohohohohohohohohololololooleeeeheeeeee")
                planetsGenerated = planetsGenerated + 1
                if Settings.useMultithreading == True:
                    generatePlanetProcess = threading.Thread(target=generate, args=(starSeed,starName,starRadius,starMass,starColor,atmoCfg,listCfg,colorsRound,oceanCfg,eveCfg,VolumetricEveCfg,Lum,parallaxCfg,parallax_subd_Cfg,parallax_scatterfix_Cfg,parallax_scatter_Cfg,evePQSCfg,rationalResources_Cfg,starTypeStr,x+1,None,None,None,None,distBinaryParents,baryOrder))
                    allThreads.append(generatePlanetProcess)
                    allActions.append([time.localtime(),"Starting thread: " + str(generatePlanetProcess)])
                    allActions.append([time.localtime(),"Thread for planet: " + str(x)])
                    allActions.append([time.localtime(),"Total threads:" + str(threading.active_count())])
                    state.allActionArrayUpdated = True
                    allPlanetThreads.append(generatePlanetProcess)
                    generatePlanetProcess.start()
                else:
                    generate(starSeed,starName,starRadius,starMass,starColor,atmoCfg,listCfg,colorsRound,oceanCfg,eveCfg,VolumetricEveCfg,Lum,parallaxCfg,parallax_subd_Cfg,parallax_scatterfix_Cfg,parallax_scatter_Cfg,evePQSCfg,rationalResources_Cfg,starTypeStr,x+1,None,None,None,None,distBinaryParents,baryOrder)
        else:
            for x in range(int(planetsNum)):
                if everythingEnded == True:
                    raise Exception("UI thread isn't running.")
                print("wowowowowowowowoooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooohohohohohohohohololololooleeeeheeeeee")
                planetsGenerated = planetsGenerated + 1
                if Settings.useMultithreading == True:
                    generatePlanetProcess = threading.Thread(target=generate, args=(starSeed,starName,starRadius,starMass,starColor,atmoCfg,listCfg,colorsRound,oceanCfg,eveCfg,VolumetricEveCfg,Lum,parallaxCfg,parallax_subd_Cfg,parallax_scatterfix_Cfg,parallax_scatter_Cfg,evePQSCfg,rationalResources_Cfg,starTypeStr,x+1))
                    allThreads.append(generatePlanetProcess)
                    allActions.append([time.localtime(),"Starting thread: " + str(generatePlanetProcess)])
                    allActions.append([time.localtime(),"Thread for planet: " + str(x)])
                    allActions.append([time.localtime(),"Total threads:" + str(threading.active_count())])
                    state.allActionArrayUpdated = True
                    allPlanetThreads.append(generatePlanetProcess)
                    generatePlanetProcess.start()
                else:
                    generate(starSeed,starName,starRadius,starMass,starColor,atmoCfg,listCfg,colorsRound,oceanCfg,eveCfg,VolumetricEveCfg,Lum,parallaxCfg,parallax_subd_Cfg,parallax_scatterfix_Cfg,parallax_scatter_Cfg,evePQSCfg,rationalResources_Cfg,starTypeStr,x+1,parentBarycenter)

        for thread in allPlanetThreads:
            thread.join()

        listCfg.write(
            "   }\n"
            "}\n"
        )
        atmoCfg.write(
            "}\n"
        )
        oceanCfg.write(
            "}\n"
        )
        eveCfg.write(
            "}\n"
        )
        VolumetricEveCfg.write(
            "}\n"
        )
        evePQSCfg.write(
            "}\n"
        )
        parallaxCfg.write(
            "}\n"
        )
        parallax_subd_Cfg.write(
            "}\n"
        )
        parallax_scatterfix_Cfg.write(
            "}\n"
        )
    return starColor, starName, dispName, Lum, starTypeStr
# Picks parameters for a barycenter. Influences star generation.
def generateBarycenter(starSeed, AmountOfPlanetsToGenerate, targetFilepath):
    global gloablSeed
    global targetPath
    targetPath = targetFilepath
    global totalSystemsGenerated
    totalSystemsGenerated = totalSystemsGenerated + 1
    global planetsGenerated
    planetsGenerated = 0

    baryGenRNG = random.Random()
    baryGenRNG.seed(starSeed)
    print(str(starSeed) + " <-------------- barycenter seed thing")
    randomfucker = baryGenRNG.randint(1,2)
    print(randomfucker)
    if Settings.binaryTypeOverride == None:
        binaryType = baryGenRNG.choice(["Near","Distant"])
    elif Settings.binaryTypeOverride == True:
        binaryType = "Distant"
    elif Settings.binaryTypeOverride == False:
        binaryType = "Near"
    else:
        binaryType = baryGenRNG.choice(["Near","Distant"])

    print(binaryType)

    systemName = str(alphabet[baryGenRNG.randint(0,len(alphabet)-1)]) + str(alphabet[baryGenRNG.randint(0,len(alphabet)-1)]) + "-" + str(baryGenRNG.randint(0,99999))

    allActions.append([time.localtime(),"Generating binary system: " + systemName])
    state.allActionArrayUpdated = True

    parentGalaxy = availableGalaxies[baryGenRNG.randint(0,len(availableGalaxies)-1)]

    minStarSize = Settings.minStarSize
    maxStarSize = Settings.maxStarSize

    star1Radius = baryGenRNG.randint(392400000,784800000)
    star1Mass = star1Radius * 6.7146251e+19

    star2Radius = math.floor(abs(baryGenRNG.random() - baryGenRNG.random()) * (10 + maxStarSize - minStarSize) + maxStarSize)
    star2Mass = star2Radius * 6.7146251e+19

    totalSystemsGenerated = totalSystemsGenerated + 1

    if Settings.starTypeOverrideBinary1 == None:
        if binaryType == "Near":
            typeOfStar1 = baryGenRNG.randint(19,175)
        elif binaryType == "Distant":
            typeOfStar1 = baryGenRNG.randint(0,175)
    else:
        typeOfStar1 = Settings.starTypeOverrideBinary1
    print(typeOfStar1)
    if 0 <= typeOfStar1 <= 18:
        redGiant1 = True
    elif 19 <= typeOfStar1 <= 28:
        whiteDwarf1 = True
    elif 29 <= typeOfStar1 <= 39:
        neutron1 = True
    elif 40 <= typeOfStar1 <= 50:
        brownDwarf1 = True
    elif 51 <= typeOfStar1 <= 55:
        wolfRayet1 = True
    else:
        mainSeq1 = True

    if Settings.starTypeOverrideBinary2 == None:
        if binaryType == "Near":
            typeOfStar2 = baryGenRNG.randint(19,175)
        elif binaryType == "Distant":
            typeOfStar2 = baryGenRNG.randint(0,175)
    else:
        typeOfStar2 = Settings.starTypeOverrideBinary2
    if 0 <= typeOfStar2 <= 18:
        redGiant2 = True
    elif 19 <= typeOfStar2 <= 28:
        whiteDwarf2 = True
    elif 29 <= typeOfStar2 <= 39:
        neutron2 = True
    elif 40 <= typeOfStar2 <= 50:
        brownDwarf2 = True
    elif 51 <= typeOfStar2 <= 55:
        wolfRayet2 = True
    else:
        mainSeq2 = True

    #print(str(typeOfStar2) + " GGGGGGGGGGAHHHHHHHHHHHHHHHHH TTYOE IF STAR @")

    try:
        if mainSeq1:
            print("Main sequence")
            randomSizeType = baryGenRNG.randint(1,3)
            if randomSizeType == 1:
                if binaryType == "Distant":
                    star1Radius = baryGenRNG.randint(minStarSize,maxStarSize/3)
                else:
                    star1Radius = baryGenRNG.randint(minStarSize,maxStarSize)
            else:
                star1Radius = baryGenRNG.randint(minStarSize,maxStarSize/6)
            #star1Radius =  math.floor(abs(random.random() - random.random()) * (10 + maxStarSize - minStarSize) + minStarSize)
            distanceRadiusThing1 = star1Radius
            star1Mass = star1Radius * 6.7146251e+19
    except UnboundLocalError:
        pass
    try:
        if wolfRayet1:
            print("Wolf Rayet")
            minWRStarSize = 130800000 #Settings.minStarSize
            maxWRStarSize = 6016800000 #Settings.maxStarSize
            star1Radius =  int(math.floor(abs(baryGenRNG.random() - baryGenRNG.random()) * (10 + maxWRStarSize - minWRStarSize) + minWRStarSize))
            distanceRadiusThing1 = star1Radius*2
            star1Mass = (((star1Radius/10)/261600000) * 1.75654591319326E+28)*15
    except UnboundLocalError:
        pass
    try:
        if redGiant1:
            print("Red Giant")
            minRGSize = 66160000 #Settings.minStarSize
            maxRGSize = 784800000 #Settings.maxStarSize
            star1Radius =  int(math.floor(abs(baryGenRNG.random() - baryGenRNG.random()) * (10 + maxRGSize - minRGSize) + minRGSize)*10)
            distanceRadiusThing1 = star1Radius
            star1Mass = (star1Radius/10) * 6.7146251e+19
    except UnboundLocalError:
        pass
    try:
        if whiteDwarf1:
            print("White Dwarf")
            WDmin = 500000
            WDmax = 700000

            star1Radius =  (math.floor(abs(baryGenRNG.random() - baryGenRNG.random()) * (10 + WDmax - WDmin) + WDmin))*4.24
            distanceRadiusThing1 = 261600000
            star1Mass = (((star1Radius/4.42) * 6.7146251e+19)*436)/2
    except UnboundLocalError:
        pass
    try:
        if neutron1:
            print("Neutron Star")
            star1Radius = 48000
            distanceRadiusThing1 = 261600000
            star1Mass = 3.5130918e+28
    except UnboundLocalError:
        pass
    try:
        if brownDwarf1:
            print("Brown Dwarf")
            BDmax = 5592000
            BDmin = 10487000
            star1Radius =  (math.floor(abs(baryGenRNG.random() - baryGenRNG.random()) * (10 + BDmax - BDmin) + BDmin))*4.24
            distanceRadiusThing1 = 161600000
            star1Mass = (((star1Radius/4.42) * 6.7146251e+19))*3
    except UnboundLocalError:
        pass

        # AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA

    try:
        if mainSeq2:
            randomSizeType = baryGenRNG.randint(1,3)
            if randomSizeType == 1:
                if binaryType == "Distant":
                    star2Radius = baryGenRNG.randint(minStarSize,maxStarSize/3)
                else:
                    star2Radius = baryGenRNG.randint(minStarSize,maxStarSize)
            else:
                star2Radius = baryGenRNG.randint(minStarSize,maxStarSize/6)
            #star2Radius =  math.floor(abs(random.random() - random.random()) * (10 + maxStarSize - minStarSize) + minStarSize)
            distanceRadiusThing2 = star2Radius
            star2Mass = star2Radius * 6.7146251e+19
    except UnboundLocalError:
        pass
    try:
        if wolfRayet2:
            print("Wolf Rayet")
            minWRStarSize = 130800000 #Settings.minStarSize
            maxWRStarSize = 6016800000 #Settings.maxStarSize
            star2Radius =  int(math.floor(abs(baryGenRNG.random() - baryGenRNG.random()) * (10 + maxWRStarSize - minWRStarSize) + minWRStarSize))
            distanceRadiusThing2 = star2Radius*2
            star2Mass = (((star2Radius/10)/261600000) * 1.75654591319326E+28)*15
    except UnboundLocalError:
        pass
    try:
        if redGiant2:
            print("Red Giant")
            minRGSize = 66160000 #Settings.minStarSize
            maxRGSize = 784800000 #Settings.maxStarSize
            star2Radius =  int(math.floor(abs(baryGenRNG.random() - baryGenRNG.random()) * (10 + maxRGSize - minRGSize) + minRGSize)*10)
            distanceRadiusThing2 = star2Radius
            star2Mass = (star2Radius/10) * 6.7146251e+19
    except UnboundLocalError:
        pass
    try:
        if whiteDwarf2:
            print("White Dwarf")
            WDmin = 500000
            WDmax = 700000

            star2Radius =  (math.floor(abs(baryGenRNG.random() - baryGenRNG.random()) * (10 + WDmax - WDmin) + WDmin))*4.24
            distanceRadiusThing2 = 261600000
            star2Mass = (((star2Radius/4.42) * 6.7146251e+19)*436)/2
    except UnboundLocalError:
        pass
    try:
        if neutron2:
            print("Neutron Star")
            star2Radius = 48000
            distanceRadiusThing2 = 261600000
            star2Mass = 3.5130918e+28
    except UnboundLocalError:
        pass
    try:
        if brownDwarf2:
            print("Brown Dwarf")
            BDmax = 5592000
            BDmin = 10487000
            star2Radius =  (math.floor(abs(baryGenRNG.random() - baryGenRNG.random()) * (10 + BDmax - BDmin) + BDmin))*4.24
            distanceRadiusThing2 = 261600000
            star2Mass = (((star2Radius/4.42) * 6.7146251e+19))*3
    except UnboundLocalError:
        pass

    print(systemName)

    largerStarRadius = max([star1Radius,star2Radius])
    largerDistance = max([distanceRadiusThing1,distanceRadiusThing2])

    barycenterMass = star1Mass + star2Mass
    barycenterRadius = largerStarRadius
    distanceThingamabob = largerDistance
    barycenterDist = baryGenRNG.randint(Settings.minStarDistance,Settings.maxStarDistance)
    if parentGalaxy == "LKC_CtrlB":
        barycenterDistG = baryGenRNG.randint(Settings.minStarDistance/5,Settings.maxStarDistance*10)/3.5
    elif parentGalaxy == "SKC_CtrlB":
        barycenterDistG = baryGenRNG.randint(Settings.minStarDistance/5,Settings.maxStarDistance*10)/11
    else:
        barycenterDistG = baryGenRNG.randint(Settings.minStarDistance/5,Settings.maxStarDistance*10)
    if star1Mass > star2Mass:
        ML = star1Mass # Larger object mass.
        MS = star2Mass # Smaller object mass.
    else:
        ML = star2Mass # Larger object mass.
        MS = star1Mass # Smaller object mass.

    neutronInSystem = False
    try:
        if neutron1 == True:
            neutronInSystem = True
    except:
        pass
    try:
        if neutron2 == True:
            neutronInSystem = True
    except:
        pass

    if neutronInSystem == True:
        if binaryType == "Near":
            gSMA = int(baryGenRNG.randint(Settings.binaryMinSMA + 50000000, Settings.binaryMaxSMA) + ((star1Radius + star2Radius)/2)) # Distance between both bodies in meters.
        else:
            gSMA = int(baryGenRNG.randint(Settings.distantBinaryMinSMA,Settings.distantBinaryMaxSMA))
    else:
        if binaryType == "Near":
            gSMA = int(baryGenRNG.randint(Settings.binaryMinSMA,Settings.binaryMaxSMA) + ((star1Radius + star2Radius)/2)) # Distance between both bodies in meters.
        else:
            gSMA = int(baryGenRNG.randint(Settings.distantBinaryMinSMA,Settings.distantBinaryMaxSMA))

    print(gSMA)
    diff = ML/MS
    # math lol
    gSMA_km = gSMA/1000
    distL = gSMA_km * 1/(1+diff)
    distS = gSMA_km * diff/(1+diff)
    pi = math.pi
    Period = 2 * pi * math.sqrt(gSMA**3 / (6.67408E-11*(ML + MS)))

    binarySMA1 = distL * 1000
    binarySMA2 = distS * 1000

    listCfg = open(targetPath + "/Visuals/Scatterer/" + systemName + "_ScattererList" + ".cfg","x")
    listCfg.write(
        "@Scatterer_planetsList:FINAL\n"
        "{\n"
        "    @scattererCelestialBodies\n"
        "    {\n"
    )
    atmoCfg = open(targetPath + "/Visuals/Scatterer/" + systemName + "_ScattererAtmo" + ".cfg","x")
    atmoCfg.write(
        "Scatterer_atmosphere\n"
        "{\n"
    )
    oceanCfg = open(targetPath + "/Visuals/Scatterer/" + systemName + "_ScattererOcean" + ".cfg","x")
    oceanCfg.write(
        "Scatterer_ocean\n"
        "{\n"
    )
    eveCfg = open(targetPath + "/Visuals/EVE/Configs/" + systemName + "_EVE" + ".cfg","x")
    eveCfg.write(
        "EVE_CLOUDS:NEEDS[!Infinite_VolumetricClouds]\n"
        "{\n"
    )
    VolumetricEveCfg = open(targetPath + "/Visuals/EVE/Configs/" + systemName + "_VOLUMEEVE" + ".cfg","x")
    VolumetricEveCfg.write(
        "EVE_CLOUDS:NEEDS[Infinite_VolumetricClouds]\n"
        "{\n"
    )
    evePQSCfg = open(targetPath + "/Visuals/EVE/Configs/" + systemName + "_PQSFIX" + ".cfg","x")
    evePQSCfg.write(
        "PQS_MANAGER\n"
        "{\n"
    )
    if binaryType == "Near":
        parallaxCfg = open(targetPath + "/Visuals/Parallax/Configs/" + systemName + "_PARALLAX" + ".cfg","x")
        parallaxCfg.write(
            "Parallax\n"
            "{\n"
        )
        parallax_subd_Cfg = open(targetPath + "/Visuals/Parallax/Configs/" + systemName + "_PARALLAX_SUBDFIX" + ".cfg","x")
        parallax_subd_Cfg.write(
            "@Kopernicus:LAST[InfiniteDiscoveries]:NEEDS[Parallax]\n"
            "{\n"
        )
        parallax_scatterfix_Cfg = open(targetPath + "/Visuals/Parallax/Configs/" + systemName + "_PARALLAX_SCATTERFIX" + ".cfg","x")
        parallax_scatterfix_Cfg.write(
            "@Kopernicus:LAST[InfiniteDiscoveries]:NEEDS[Parallax]\n"
            "{\n"
        )
        # Empty
        parallax_scatter_Cfg = open(targetPath + "/Visuals/Parallax/Configs/" + systemName + "_PARALLAX_SCATTERS" + ".cfg","x")
        rationalResources_Cfg = open(targetPath + "/Misc/RR/" + systemName + "_RationalResources" + ".cfg","x")
    if binaryType == "Distant":
        binaryEccentricity = baryGenRNG.randint(0,60)/100
    else:
        binaryEccentricity = 0

    # Turns out I don't need it.

    #star1_IsBarycenter = False
    #star2_IsBarycenter = False

    #if star1Mass > star2Mass:
    #    massDiff = star1Mass/star2Mass
    #    if massDiff > 4:
    #        star1_IsBarycenter = True
    #    else:
    #        star1_IsBarycenter = False
    #else:
    #    massDiff = star2Mass/star1Mass
    #    if massDiff > 4:
    #        star2_IsBarycenter = True
    #    else:
    #        star2_IsBarycenter = False

    print("-------------------------- STAR THINGS")
    print(star1Radius)
    print(star2Radius)
    print(typeOfStar1)
    print(typeOfStar2)
    print("-------------------------- STAR THINGS")

    if star1Mass > star2Mass:
        star1Color, star1Name, dispName1, Lum1, starTypeStr1 = generateStar(starSeed+1, AmountOfPlanetsToGenerate, systemName, targetPath, systemName, binarySMA1, Period, star1Radius, 0, "-1", typeOfStar1, binaryType, binaryEccentricity)
        star2Color, star2Name, dispName2, Lum2, starTypeStr2 = generateStar(starSeed+2, AmountOfPlanetsToGenerate, systemName, targetPath, systemName, binarySMA2, Period, star2Radius, 180, "-2", typeOfStar2, binaryType, binaryEccentricity)
    else:
        star1Color, star1Name, dispName1, Lum1, starTypeStr1 = generateStar(starSeed+1, AmountOfPlanetsToGenerate, systemName, targetPath, systemName, binarySMA2, Period, star1Radius, 0, "-1", typeOfStar1, binaryType, binaryEccentricity)
        star2Color, star2Name, dispName2, Lum2, starTypeStr2 = generateStar(starSeed+2, AmountOfPlanetsToGenerate, systemName, targetPath, systemName, binarySMA1, Period, star2Radius, 180, "-2", typeOfStar2, binaryType, binaryEccentricity)

    if binaryType == "Near":
        if starTypeStr1 == "WolfRayet" or starTypeStr2 == "WolfRayet":
            generateWRBinarySpiral(systemName, base_dir)
            generateNebula(systemName, base_dir)

    if starTypeStr1 == "WolfRayet" or starTypeStr2 == "WolfRayet":
        planetsNum = baryGenRNG.randint(minPlanets,AmountOfPlanetsToGenerate)/2
    elif starTypeStr1 == "RedGiant" or starTypeStr2 == "RedGiant":
        planetsNum = baryGenRNG.randint(minPlanets,AmountOfPlanetsToGenerate)/1.5
    elif starTypeStr1 == "Neutron" or starTypeStr2 == "Neutron":
        planetsNum = baryGenRNG.randint(minPlanets,AmountOfPlanetsToGenerate)/1.5
    elif starTypeStr1 == "WhiteDwf" or starTypeStr2 == "WhiteDwf":
        planetsNum = baryGenRNG.randint(minPlanets,AmountOfPlanetsToGenerate)/1.5
    else:
        planetsNum = baryGenRNG.randint(minPlanets,AmountOfPlanetsToGenerate)
    baryCfg = open(targetPath + "/Configs/" + systemName + ".cfg","x")
    if star1Mass > star2Mass:
        starColors = star1Color
    else:
        starColors = star2Color

    print("Number Of Planets For " + systemName + ": " + str(int(planetsNum)))

    RGBfinal = str(starColors)[1:][:-1]
    baryDispName = dispName1 + "-" + dispName2 + " Barycenter"
    averageClrR = (star1Color[0] + star2Color[0])/2
    averageClrG = (star1Color[1] + star2Color[1])/2
    averageClrB = (star1Color[2] + star2Color[2])/2
    averageClr = [averageClrR, averageClrG, averageClrB]

    if starTypeStr1 == "RedGiant":
        brightnessThing1 = (star1Radius/30)*2 # I honestly do not know what to call these variables anymore.
    elif starTypeStr1 == "BrownDwarf":
        brightnessThing1 = star1Radius*10
    elif starTypeStr1 == "Neutron":
        brightnessThing1 = star1Radius*5450
    elif starTypeStr1 == "WhiteDwf":
        brightnessThing1 = star1Radius*50
    elif starTypeStr1 == "WolfRayet":
        brightnessThing1 = star1Radius*30
    else:
        brightnessThing1 = star1Radius

    if starTypeStr2 == "RedGiant":
        brightnessThing2 = (star2Radius/30)*2 # I honestly do not know what to call these variables anymore.
    elif starTypeStr2 == "BrownDwarf":
        brightnessThing2 = star2Radius*10
    elif starTypeStr2 == "Neutron":
        brightnessThing2 = star2Radius*5450
    elif starTypeStr2 == "WhiteDwf":
        brightnessThing2 = star2Radius*50
    elif starTypeStr2 == "WolfRayet":
        brightnessThing2 = star2Radius*30
    else:
        brightnessThing2 = star2Radius

    baryBrightness = (brightnessThing1 + brightnessThing2)
    print("Barycenter brightness info:")
    print("Total brightness: " + str(baryBrightness))
    print("Star 1 brightness : " + str(brightnessThing1) + " (" + starTypeStr1 + ")")
    print("Star 2 brightness: " + str(brightnessThing2) + " (" + starTypeStr2 + ")")

    if star1Mass > star2Mass:
        binaryParents = [star1Name,star2Name]
    else:
        binaryParents = [star2Name,star1Name]
    binaryTypes = [starTypeStr1,starTypeStr2]

    #if star1_IsBarycenter == False and star2_IsBarycenter == False:
    writeBarycenterCfg(starSeed, baryCfg, systemName, barycenterRadius, barycenterMass, barycenterDist, systemName, RGBfinal, barycenterDistG, baryDispName, averageClr, baryBrightness, parentGalaxy, binaryType, binaryTypes, AmountOfPlanetsToGenerate, AmountOfMoonsToGenerate, AmountOfAsteroidsToGenerate, minPlanets, minMoons)

    print(star1Color)
    colorsRound1 = (star1Color[0] + star1Color[1] + star1Color[2])/3
    colorsRound2 = (star2Color[0] + star2Color[1] + star2Color[2])/3
    colorsRound = colorsRound1 + colorsRound2

    Lum = (Lum1 + Lum2)/2

    sunfCfg = open(targetPath + "/Visuals/Scatterer/" + systemName + "_ScattererSunflare" + ".cfg","x")
    addSunflareCfg(sunfCfg, star1Color, star1Name, starTypeStr1)
    addSunflareCfg(sunfCfg, star2Color, star2Name, starTypeStr2)

    if binaryType == "Near":
        allPlanetThreads = []
        for x in range(int(planetsNum)):
            if everythingEnded == True:
                raise Exception("UI thread isn't running.")
            #print("wowowowowowowowoooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooohohohohohohohohololololooleeeeheeeeee")
            planetsGenerated = planetsGenerated + 1
            if Settings.useMultithreading == True:
                generatePlanetProcess = threading.Thread(target=generate, args=(starSeed,systemName,barycenterRadius,barycenterMass,star1Color,atmoCfg,listCfg,colorsRound,oceanCfg,eveCfg,VolumetricEveCfg,Lum,parallaxCfg,parallax_subd_Cfg,parallax_scatterfix_Cfg,parallax_scatter_Cfg,evePQSCfg,rationalResources_Cfg,starTypeStr1,x+1,binaryParents,binaryTypes,gSMA,distanceThingamabob))
                allThreads.append(generatePlanetProcess)
                allActions.append([time.localtime(),"Starting thread: " + str(generatePlanetProcess)])
                allActions.append([time.localtime(),"Total threads:" + str(threading.active_count())])
                state.allActionArrayUpdated = True
                allPlanetThreads.append(generatePlanetProcess)
                generatePlanetProcess.start()
            else:
                generate(starSeed,systemName,barycenterRadius,barycenterMass,star1Color,atmoCfg,listCfg,colorsRound,oceanCfg,eveCfg,VolumetricEveCfg,Lum,parallaxCfg,parallax_subd_Cfg,parallax_scatterfix_Cfg,parallax_scatter_Cfg,evePQSCfg,rationalResources_Cfg,starTypeStr1,x+1,binaryParents,binaryTypes,gSMA,distanceThingamabob)

        for thread in allPlanetThreads:
            thread.join()

    listCfg.write(
        "   }\n"
        "}\n"
    )
    atmoCfg.write(
        "}\n"
    )
    oceanCfg.write(
        "}\n"
    )
    eveCfg.write(
        "}\n"
    )
    VolumetricEveCfg.write(
        "}\n"
    )
    evePQSCfg.write(
        "}\n"
    )
    if binaryType == "Near":
        parallaxCfg.write(
            "}\n"
        )
        parallax_subd_Cfg.write(
            "}\n"
        )
        parallax_scatterfix_Cfg.write(
            "}\n"
        )
# Tests if inputted numbers are actual numbers, currently broken. Also useless.
def testNum(Numer):
    try:
        val = int(Numer)
    except ValueError:
        print("That's not an number!")
        exit()

#print("---------------------------------------------------------------")
#print("Infinite-Discoveries Version 0.9.8 (public beta!)")
#print("---------------------------------------------------------------")
#print("WARNING: Generating a large amount of stars will take longer to... generate! The more stars you generate, the more it has to generate. You can find a settings file in the mod directory if you want to adjust some parameters.")
#print("---------------------------------------------------------------")
#
#StarAmount = int(input("Amount of stars to generate: "))
#testNum(StarAmount)
#
#print("---------------------------------------------------------------")
#print("If you happened to input a very high number just now, it's recommended to lower the amount of planets per star to reduce KSP loading times.")
#print("---------------------------------------------------------------")
#AmountOfPlanetsToGenerate = int(input("Maximum number of planets to add around stars: "))
#testNum(AmountOfPlanetsToGenerate)
#print("---------------------------------------------------------------")
#print("Last thing to input before you can generate! Please input the maximum number of moons to add around a planet.")
#print("---------------------------------------------------------------")
#AmountOfMoonsToGenerate = int(input("Maximum number of moons per planet: "))
#testNum(AmountOfMoonsToGenerate)
#print("---------------------------------------------------------------")
#estTime = ((AmountOfPlanetsToGenerate * AmountOfMoonsToGenerate) * StarAmount)*15
#print("The generator should take AT MOST " + str(round((estTime/60),2)) + " minutes.")
#if Settings.deleteUnnecessarFolders == True:
#    print("The program WILL delete itself once it's done!")
#print("---------------------------------------------------------------")
#input("Type anything or press enter to continue: ")
#planetsGenerated = 0
#startTime = time.time()

StarAmount = 0
AmountOfPlanetsToGenerate = 0
AmountOfMoonsToGenerate = 0
AmountOfAsteroidsToGenerate = 0
minPlanets = 0
minMoons = 0
minAsteroids = 0

startTime = time.time()

loopProcess = None

def systemLoop(queue, starAmnt, planetAmnt, moonAmnt, asteroidAmnt, targetFilepath, customSeed=None, overrideValues=None):
    print(str(customSeed) + " <------------------------------------------ THE FUCKING SEED BITCH")
    print(multiprocessing.current_process())
    importlib.reload(Settings)
    os.makedirs(targetFilepath + "/InfiniteDiscoveries", exist_ok=True)
    allActions.append([time.localtime(),"Creating Directory"])
    os.makedirs(targetFilepath + "/InfiniteDiscoveries/Configs", exist_ok=True)
    allActions.append([time.localtime(),targetFilepath + "/InfiniteDiscoveries/Configs"])
    os.makedirs(targetFilepath + "/InfiniteDiscoveries/Cache", exist_ok=True)
    allActions.append([time.localtime(),targetFilepath + "/InfiniteDiscoveries/Cache"])
    try:
        shutil.copytree(base_dir / "Misc", Path(targetFilepath) / "InfiniteDiscoveries" / "Misc")
        allActions.append([time.localtime(),"Cloning: " + "filepath" + "/Misc"])
    except FileExistsError:
        allActions.append([time.localtime(),str(Path(targetFilepath) / "InfiniteDiscoveries" / "Misc") + " Already exists."])

    try:
        shutil.copytree(base_dir / "Visuals", targetFilepath + "/InfiniteDiscoveries/Visuals")
        allActions.append([time.localtime(),"Cloning: " + str(base_dir / "Visuals")])
    except FileExistsError:
        allActions.append([time.localtime(),str(Path(targetFilepath) / "InfiniteDiscoveries" / "Visuals") + " Already exists."])
        pass
    try:
        shutil.copytree(base_dir / "Textures", targetFilepath + "/InfiniteDiscoveries/Textures")
        allActions.append([time.localtime(),"Cloning: " + str(base_dir / "Textures")])
    except FileExistsError:
        allActions.append([time.localtime(),str(Path(targetFilepath) / "InfiniteDiscoveries" / "Textures") + " Already exists."])
        pass
    try:
        shutil.copytree(base_dir / "Presets", targetFilepath + "/InfiniteDiscoveries/Presets")
        allActions.append([time.localtime(),"Cloning: " + str(base_dir / "Presets")])
    except FileExistsError:
        allActions.append([time.localtime(),str(Path(targetFilepath) / "InfiniteDiscoveries" / "Presets") + " Already exists."])
        pass
    try:
        shutil.copy(base_dir / "_Gameplay Settings.cfg", targetFilepath + "/InfiniteDiscoveries/")
        allActions.append([time.localtime(),"Cloning: " + str(base_dir / "_Gameplay Settings.cfg")])
    except FileExistsError:
        allActions.append([time.localtime(),str(Path(targetFilepath) / "InfiniteDiscoveries" / "_Gameplay Settings.cfg") + " Already exists."])
        pass

    state.allActionArrayUpdated = True

    queue.append("heeeeeheeeeeeeeee")

    global StarAmount
    global AmountOfPlanetsToGenerate
    global AmountOfMoonsToGenerate
    global AmountOfAsteroidsToGenerate
    global minPlanets
    global minMoons
    global minAsteroids

    if customSeed == None:
        StarAmount = starAmnt
    else:
        StarAmount = 1
    
    if overrideValues == None:
        AmountOfPlanetsToGenerate = planetAmnt
        AmountOfMoonsToGenerate = moonAmnt
        AmountOfAsteroidsToGenerate = asteroidAmnt
        minPlanets = Settings.minPlanets
        minMoons = Settings.minMoons
    else:
        #AmountOfPlanetsToGenerate = overrideValues[0]
        #AmountOfMoonsToGenerate = overrideValues[1]
        #AmountOfAsteroidsToGenerate = overrideValues[2]
        #minPlanets = overrideValues[3]
        #minMoons = overrideValues[4]
        AmountOfPlanetsToGenerate, AmountOfMoonsToGenerate, AmountOfAsteroidsToGenerate, minPlanets, minMoons = overrideValues

    global targetPath
    targetPath = targetFilepath + "/InfiniteDiscoveries/"

    for i in range(0,StarAmount):
        randomSeedRNG = random.Random()
        starChoiceRNG = random.Random()
        if customSeed == None:
            generatorSeed = randomSeedRNG.randint(0,(2**32)-1)
            global gloablSeed
            gloablSeed = generatorSeed
        else:
            if int(customSeed) >= 0:
                generatorSeed = int(customSeed)
                print("AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA" + str(generatorSeed))
                gloablSeed = generatorSeed
            else:
                generatorSeed = int(0)
                gloablSeed = generatorSeed
        starChoiceRNG.seed(generatorSeed)
        starSeed = generatorSeed
        if Settings.binaryOverride == None:
            binaryChoice = starChoiceRNG.randint(0,1)
        elif Settings.binaryOverride == True:
            binaryChoice = 0
        elif Settings.binaryOverride == False:
            binaryChoice = 1
        else:
            print("epic binary override fail")
            binaryChoice = starChoiceRNG.randint(0,1)
        if binaryChoice == 0:
            barycenter = True
            if Settings.useMultithreading == True:
                generateBarycenterProcess = threading.Thread(target=generateBarycenter, args=(starSeed, AmountOfPlanetsToGenerate, targetPath))
                allThreads.append(generateBarycenterProcess)
                generateBarycenterProcess.start()
            else:
                generateBarycenter(starSeed, AmountOfPlanetsToGenerate, targetPath)
        else:
            barycenter = False
            if Settings.useMultithreading == True:
                generateStarProcess = threading.Thread(target=generateStar, args=(starSeed, AmountOfPlanetsToGenerate, barycenter, targetPath))
                allThreads.append(generateStarProcess)
                generateStarProcess.start()
            else:
                generateStar(starSeed, AmountOfPlanetsToGenerate, barycenter, targetPath)

    if everythingEnded == True:
        raise Exception("UI thread isn't running.")

def waitForThreadsToFinish(mainThread, idk):
    mainThread.join()
    for thread in allThreads:
        thread.join()
    global mainThreadFinished
    mainThreadFinished = True
    allActions.append([time.localtime(),"Generating wormholes..."])
    state.allActionArrayUpdated = True

    #generateWormholes()

    allActions.append([time.localtime(),"Finished generation."])
    state.allActionArrayUpdated = True

def startLoop(starAm,planetAm,moonAM,asteroidAM,targetPath,customSeed=None,overrides=None):
    global loopProcess
    loopProcess = threading.Thread(target=systemLoop, args=(queue,starAm,planetAm,moonAM,asteroidAM,targetPath,customSeed,overrides))
    allThreads.append(loopProcess)
    allActions.append([time.localtime(),"Starting thread: " + str(loopProcess)])
    allActions.append([time.localtime(),"Total threads:" + str(threading.active_count())])
    state.allActionArrayUpdated = True
    loopProcess.start()
    waitForThreadsToFinishThread = threading.Thread(target=waitForThreadsToFinish, args=(loopProcess,None))
    waitForThreadsToFinishThread.start()

def openSettings():

    importlib.reload(Settings)


    with open("Settings.py", "r") as settingsFile:
        settingsData = settingsFile.readlines()

    usesMultithreading = Settings.useMultithreading

    convertsToDDS = Settings.convertTexturesToDDS

    fantasyNames = Settings.fantasyNames

    minPlanets = Settings.minPlanets
    minMoons = Settings.minMoons

    showConsole = Settings.showConsole

    useThreadingText = sg.Text(textwrap.fill("Multithreading drastically improves efficiency but might increase CPU usage.", 40), background_color="#1f2836")
    useThreadingCheck = sg.Checkbox("Use Multithreading", default=usesMultithreading, key="useMultithreading")
    useThreadingLayout = [[useThreadingCheck],[useThreadingText]]
    useThreadingFrame = sg.Frame("Multithreading",layout=useThreadingLayout)

    convertToDDSText = sg.Text(textwrap.fill("Converting maps to DDS improves RAM usage ingame, but takes a bit longer and requires ImageMagick.", 40), background_color="#1f2836")
    convertToDDSCheck = sg.Checkbox("Convert Textures to DDS", default=convertsToDDS, key="convertsToDDS")
    convertToDDSLayout = [[convertToDDSCheck],[convertToDDSText]]
    convertToDDSrame = sg.Frame("DDS Conversion",layout=convertToDDSLayout)

    fantasyNamesText = sg.Text(textwrap.fill("Fantasy names do not affect anything, but simply adds some more creative names to celestial bodies.", 40), background_color="#1f2836")
    fantasyNamesCheck = sg.Checkbox("Use Fantasy Names", default=fantasyNames, key="fantasyNames")
    fantasyNamesLayout = [[fantasyNamesCheck],[fantasyNamesText]]
    fantasyNamesrame = sg.Frame("Fancy Names",layout=fantasyNamesLayout)

    minPlanetsBox = sg.Input(str(minPlanets), key="minPlanetsInp", enable_events=True, size=(12,10), expand_y=False, expand_x=False)
    minPlanetsLayout = [[minPlanetsBox]]
    minPlanetsFrame = sg.Frame("Minimum Planets", layout=minPlanetsLayout)

    minMoonsBox = sg.Input(str(minMoons), key="minMoonsInp", enable_events=True, size=(12,10), expand_y=False, expand_x=False)
    minMoonsLayout = [[minMoonsBox]]
    minMoonsFrame = sg.Frame("Minimum Moons", layout=minMoonsLayout)

    variablesLayout = [[useThreadingFrame],[convertToDDSrame],[fantasyNamesrame],[minPlanetsFrame,minMoonsFrame]]

    variablesFrame = sg.Frame("Generator Settings", layout=variablesLayout, expand_x=True, expand_y=True)

    showConsoleText = sg.Text(textwrap.fill("Shows the console in the background. Requires a restart to apply.", 40), background_color="#1f2836")
    showConsoleCheck = sg.Checkbox("Show Console", default=showConsole, key="showConsole")
    showConsoleLayout = [[showConsoleCheck],[showConsoleText]]
    showConsoleFrame = sg.Frame("Console",layout=showConsoleLayout)

    UIvariablesLayout = [[showConsoleFrame]]

    UIvariablesFrame = sg.Frame("UI Settings", layout=UIvariablesLayout, expand_x=True, expand_y=True)

    applyButton = sg.Button("Apply", key="Apply")

    applyLayout = [[applyButton]]

    applyFrame = sg.Frame("", layout=applyLayout)

    settingsLayout = [[variablesFrame,UIvariablesFrame],[applyFrame]]


    settingsWindow = sg.Window(title="Settings", layout=settingsLayout, size=(300,450), resizable=False, finalize=True, background_color="#1f2836")

    settingsWindow.TKroot.minsize(600,450)


    while True:
        event, values = settingsWindow.read()

        if event == "minPlanetsInp":
            try: 
                int(values["minPlanetsInp"])
            except:
                print("Not a number!")
                settingsWindow["minPlanetsInp"].update(values["minPlanetsInp"][:-1])

        if event == "minMoonsInp":
            try: 
                int(values["minMoonsInp"])
            except:
                print("Not a number!")
                settingsWindow["minMoonsInp"].update(values["minMoonsInp"][:-1])

        if event == "Apply":
            usesMultithreading = values["useMultithreading"]
            print(usesMultithreading)
            settingsData[2] = "useMultithreading = " + str(usesMultithreading) + " # Will use multithreading, this will drastically increase generator efficiency and thus result in faster generation, but may increase CPU usage." + "\n"

            convertsToDDS = values["convertsToDDS"]
            print(convertsToDDS)
            settingsData[6] = "convertTexturesToDDS = " + str(convertsToDDS) + " # Will remove the requirement for ImageMagick and reduce generator time if false. Will also increase KSP loading time so setting to false is not recommended." + "\n"

            fantasyNames = values["fantasyNames"]
            print(fantasyNames)
            settingsData[11] = "fantasyNames = " + str(fantasyNames) + " # Generate a fantasy name for bodies. Will not affect internal names!" + "\n"

            minPlanets = int(values["minPlanetsInp"])
            print(minPlanets)
            settingsData[8] = "minPlanets = " + str(minPlanets) + " # Minimum number of planets per star." + "\n"

            minMoons = int(values["minMoonsInp"])
            print(minMoons)
            settingsData[9] = "minMoons = " + str(minMoons) + " # Minimum number of moons per star." + "\n"

            showConsole = values["showConsole"]
            print(showConsole)
            settingsData[13] = "showConsole = " + str(showConsole) + " # Whether or not to show the console." + "\n"

            with open("Settings.py", "w") as settingsFile:
                settingsFile.writelines( settingsData )

            print(threading.current_thread())

        if event == sg.WIN_CLOSED:
            break

def openDelete(targetPath):

    explText = textwrap.fill("The below input requires the star's internal name. You can find it by going ingame and looking at the description, where the name is formatted as 'AA-11111' WARNING: will delete EVERY config/texture containing what you inputted! Leave blank to delete everything.", width=40)

    explanation = sg.Text(explText)

    starDelInput = sg.Input(key="deleteStarValue")

    starDelButton = sg.Button("Delete", button_color="#e65045", key="deleteStar")

    deleteSystemsLayout = [[explanation],[starDelInput],[starDelButton]]

    deleteSystemsFrame = sg.Frame("Delete star", layout=deleteSystemsLayout, expand_x=True, expand_y=False)

    deleteAllButton = sg.Button("Remove Directory", button_color="#e65045", key="deleteALL")

    deleteAllLayout = [[deleteAllButton]]

    deleteAllFrame = sg.Frame("Warning: this will delete the mod from KSP!", layout=deleteAllLayout, expand_x=True, expand_y=False)

    deleteLayout = [[deleteSystemsFrame],[deleteAllFrame]]

    deleteWindow = sg.Window(title="Delete Systems", layout=deleteLayout, size=(300,300), resizable=False, finalize=True, background_color="#1f2836")

    deleteStarAreYouSure = False

    deleteDirAreYouSure = False

    targetPath

    print(targetPath)

    textureDir = targetPath + "/InfiniteDiscoveries" + "/Textures/PluginData"
    configDir = targetPath + "/InfiniteDiscoveries" + "/Configs"
    cacheDir = targetPath + "/InfiniteDiscoveries" + "/Cache"
    visual_ScattererDir = targetPath + "/InfiniteDiscoveries" + "/Visuals/Scatterer"
    visual_EveConfigDir = targetPath + "/InfiniteDiscoveries" + "/Visuals/Eve/Configs"
    visual_ParallaxDir = targetPath + "/InfiniteDiscoveries" + "/Visuals/Parallax/Configs"
    visual_CloudMapDir = targetPath + "/InfiniteDiscoveries" + "/Textures/Clouds"
    visual_NiftyNebulaeDir = targetPath + "/InfiniteDiscoveries" + "/Visuals/NiftyNebulae"
    misc_RRDir = targetPath + "/InfiniteDiscoveries" + "/Misc/RR"

    allDirs = [textureDir, configDir, cacheDir, visual_ScattererDir, visual_EveConfigDir, visual_ParallaxDir, visual_CloudMapDir, visual_NiftyNebulaeDir, misc_RRDir]

    def areYouSureWait(thing, text):
        time.sleep(2)
        global deleteStarAreYouSure
        deleteStarAreYouSure = False
        thing.update(text)

    def areYouSureAllWait(thing, text):
        time.sleep(2)
        global deleteDirAreYouSure
        deleteDirAreYouSure = False
        thing.update(text)

    while True:
        event, values = deleteWindow.read()

        if event == "deleteStar":
            if deleteStarAreYouSure == False:
                deleteStarAreYouSure = True
                deleteWindow["deleteStar"].update("Are You Sure? This CANNOT be undone!")
                areYouSureThread = threading.Thread(target=areYouSureWait, args=(deleteWindow["deleteStar"], "Delete"))
                areYouSureThread.start()
            else:
                targetStar = values["deleteStarValue"]
                print(targetStar)
                try:
                    for e in range(0,len(allDirs)):
                        currentDir = allDirs[e]
                        for f in os.listdir(currentDir):
                            if targetStar in f:
                                os.remove(os.path.join(currentDir, f))
                except FileNotFoundError:
                    deleteWindow["deleteStar"].update("Directory doesn't exist!")
                    areYouSureThread = threading.Thread(target=areYouSureWait, args=(deleteWindow["deleteStar"], "Delete"))
                    areYouSureThread.start()

        if event == "deleteALL":
            if deleteDirAreYouSure == False:
                deleteDirAreYouSure = True
                deleteWindow["deleteALL"].update("Are You Sure? This CANNOT be undone!")
                areYouSureThread = threading.Thread(target=areYouSureAllWait, args=(deleteWindow["deleteALL"], "Remove Directory"))
                areYouSureThread.start()
            else:
                try:
                    shutil.rmtree(targetPath + "/InfiniteDiscoveries")
                except FileNotFoundError:
                    deleteWindow["deleteALL"].update("Directory doesn't exist!")
                    areYouSureThread = threading.Thread(target=areYouSureAllWait, args=(deleteWindow["deleteALL"], "Remove Directory"))
                    areYouSureThread.start()

        if event == sg.WIN_CLOSED:
            break

def openHelp():
    noticeWindow = sg.Window(title="Infinite Discoveries Help", layout=[[]])
    noticeWindow.read()

def startUI():

    amountValues = [1,5,4,2] # Default

    #sg.Window(title="Hello World", layout=[[]], margins=(100, 50)).read()

    actionText = ""

    inputButtonSize = (12,10)

    currentObjectText = sg.Text("Generator is not currently running.", background_color=("#0c0f1a"), key="currentFocusText")

    currentActionText = sg.Multiline(background_color=("#0c0f1a"), key="currentActionText", expand_y=True, expand_x=True, text_color=("#ffffff"), autoscroll=True, enable_events=True, do_not_clear=True)

    currentActionLayout = [[currentObjectText],[currentActionText]]

    currentActionFrame = sg.Column(layout=currentActionLayout, background_color=("#0c0f1a"), key="currentActionFrame", expand_y=True, expand_x=True)

    startAmountDescText = "Recommended values are however many stars, 7 planets and 3 moons. Higher amounts will generate planets/moons further out and might start causing issues. Make sure to select the KSP GameData folder as the directory."

    starAmountDescription = sg.Text(textwrap.fill(startAmountDescText, 49), expand_y=False, expand_x=True, pad=(5,5), key="starAmountDesc")

    starAmountInp = sg.Input(default_text=amountValues[0], key="starAmountInput", enable_events=True, size=inputButtonSize, expand_y=False, expand_x=True)
    starAmountLayout = [[starAmountInp]]
    starAmountFrame = sg.Frame("Star amount", layout=starAmountLayout, expand_y=True, expand_x=True, pad=(5,5))
    planetAmountInp = sg.Input(default_text=amountValues[1], key="planetAmountInput", enable_events=True, size=inputButtonSize, expand_y=False, expand_x=True)
    planetAmountLayout = [[planetAmountInp]]
    planetAmountFrame = sg.Frame("Max planets", layout=planetAmountLayout, expand_y=True, expand_x=True, pad=(5,5))
    moonAmountInp = sg.Input(default_text=amountValues[2], key="moonAmountInput", enable_events=True, size=inputButtonSize, expand_y=False, expand_x=True)
    moonAmountLayout = [[moonAmountInp]]
    moonAmountFrame = sg.Frame("Max moons", layout=moonAmountLayout, expand_y=True, expand_x=True, pad=(5,5))
    asteroidAmountInp = sg.Input(default_text=amountValues[3], key="asteroidAmountInput", enable_events=True, size=inputButtonSize, expand_y=False, expand_x=True)
    asteroidAmountLayout = [[asteroidAmountInp]]
    asteroidAmountFrame = sg.Frame("Max asteroids", layout=asteroidAmountLayout, expand_y=True, expand_x=True, pad=(5,5))

    numInpLayout = [[starAmountFrame, planetAmountFrame, moonAmountFrame, asteroidAmountFrame],[starAmountDescription]]

    amountInpFrame = sg.Frame("", layout=numInpLayout, background_color=("#43474d"), expand_y=False, expand_x=True, pad=(10,0))

    startButton = sg.pin(sg.Button(button_text="Start Generator", size=(25,5), key="startGenerator", visible=True, expand_y=False, expand_x=True, pad=(10,0)), expand_x=True)

    estTimeText = sg.Text("Estimated Generator Time: 26.25 minutes.", key="timeRemainingText", background_color=("#43474d"), expand_y=False, expand_x=True)

    directoryText = sg.Input(targetPath, size=(30,10), key="directoryText", enable_events=True, expand_y=False, expand_x=True)

    directoryBrowser = sg.FolderBrowse("Set GameData folder...", key="directoryButton", enable_events=True, initial_folder=targetPath)

    #statsDesc = sg.Text("Current Statistics:", key="stats_Desc", background_color=("#43474d"), expand_y=False, expand_x=True)
    
    statsSystemAmount = sg.Text("Amount of systems: ????", key="stats_SystemAmount", background_color=("#43474d"), expand_y=False, expand_x=True)
    statsConfigAmount = sg.Text("Amount of configs: ????", key="stats_ConfigAmount", background_color=("#43474d"), expand_y=False, expand_x=True)
    statsTextureAmount = sg.Text("Amount of textures: ????", key="stats_TextureAmount", background_color=("#43474d"), expand_y=False, expand_x=True)

    statsLayout = [[statsSystemAmount],[statsConfigAmount],[statsTextureAmount]]

    statsFrame = sg.Frame("Current statistics", layout=statsLayout, expand_y=False, expand_x=True, background_color="#43474d")

    okToAccess = sg.Text("To write or not to write? That is the question.", background_color=("#43474d"), expand_x=True, key="okToAccess")

    InfDLayout = [[sg.Text("Infinite Discoveries", background_color=("#43474d"))], [amountInpFrame], [directoryText,directoryBrowser], [okToAccess], [estTimeText], [startButton], [statsFrame]]

    InfDOutputLayout = [[currentActionFrame]]

    settingsButton = sg.Button("Settings", image_size=(50,50), key="openSettings")

    settingsLayout = [[settingsButton]]

    settingsFrame = sg.Frame("", layout=settingsLayout)

    deleteButton = sg.Button("Delete", image_size=(50,50), key="openDelete")

    deleteLayout = [[deleteButton]]

    deleteFrame = sg.Frame("", layout=deleteLayout)

    infoButton = sg.Button("Help", image_size=(50,50), key="openHelp")

    infoLayout = [[infoButton]]

    infoFrame = sg.Frame("", layout=infoLayout)

    seedText = sg.Text("Custom Seed")
    seedInput = sg.Input("", key="setSeed", enable_events=True, size=(20,0))

    seedLayout = [[seedInput,seedText]]

    seedFrame = sg.Frame("", layout=seedLayout, element_justification="c",tooltip="Setting a custom seed will limit the star amount to 1. Seeds must be integers between 0 and 2^32 - 1")

    InputFrame = sg.Frame("", layout=InfDLayout, expand_y=True, expand_x=True, element_justification="c", background_color="#50535c")

    OutputFrame = sg.Frame("", layout=InfDOutputLayout, expand_y=True, expand_x=True, element_justification="c", background_color="#50535c")

    fullLayout = [[InputFrame,OutputFrame],[settingsFrame,deleteFrame,infoFrame,seedFrame]]

    InfDWindow = sg.Window(title="Infinite Discoveries 0.9.9", layout=fullLayout, size=(800,500), margins=(5,0), resizable=True, finalize=True background_color="#1f2836")

    InfDWindow.TKroot.minsize(700,500)

    # Things??

    lastMoment = 0

    ActionLog = open(base_dir / "ActionLog.txt", "w")
    ActionLog = open(base_dir / "ActionLog.txt", "a")

    if Settings.convertTexturesToDDS == True:
        try:
            from wand import image as wImage
        except:
            #print("ImageMagick is not installed, install it from: https://docs.wand-py.org/en/latest/guide/install.html#install-imagemagick-on-windows")
            noticeText = textwrap.fill("ImageMagick is not installed! You can continue to run the program as intended, but it will not convert textures to DDS.", 40)
            noticeLayour = [[sg.Text(noticeText)]]
            noticeWindow = sg.Window(title="Notice", layout=noticeLayour)
            noticeWindow.read()     

        def setStarAmntToOverriden():
            InfDWindow["starAmountInput"].update(disabled=True)
            InfDWindow["starAmountInput"].update("SEED SET")
            InfDWindow["starAmountInput"].update(text_color="#6e6e6e")
            InfDWindow["starAmountInput"].set_tooltip("Overriden due to setting a custom seed.")

        def setStarAmntToDefault():
            InfDWindow["starAmountInput"].update(disabled=False)
            InfDWindow["starAmountInput"].update(amountValues[0])
            InfDWindow["starAmountInput"].update(text_color="#000000")
            InfDWindow["starAmountInput"].set_tooltip(None)

        def setOtherAmntToOverriden():
            InfDWindow["planetAmountInput"].update(disabled=True)
            InfDWindow["planetAmountInput"].update("SEED SET")
            InfDWindow["planetAmountInput"].update(text_color="#6e6e6e")
            InfDWindow["planetAmountInput"].set_tooltip("Overriden due to setting a custom seed.")

            InfDWindow["moonAmountInput"].update(disabled=True)
            InfDWindow["moonAmountInput"].update("SEED SET")
            InfDWindow["moonAmountInput"].update(text_color="#6e6e6e")
            InfDWindow["moonAmountInput"].set_tooltip("Overriden due to setting a custom seed.")

            InfDWindow["asteroidAmountInput"].update(disabled=True)
            InfDWindow["asteroidAmountInput"].update("SEED SET")
            InfDWindow["asteroidAmountInput"].update(text_color="#6e6e6e")
            InfDWindow["asteroidAmountInput"].set_tooltip("Overriden due to setting a custom seed.")

        def setOtherAmntToDefault():
            InfDWindow["planetAmountInput"].update(disabled=False)
            InfDWindow["planetAmountInput"].update(amountValues[1])
            InfDWindow["planetAmountInput"].update(text_color="#000000")
            InfDWindow["planetAmountInput"].set_tooltip(None)

            InfDWindow["moonAmountInput"].update(disabled=False)
            InfDWindow["moonAmountInput"].update(amountValues[2])
            InfDWindow["moonAmountInput"].update(text_color="#000000")
            InfDWindow["moonAmountInput"].set_tooltip(None)

            InfDWindow["asteroidAmountInput"].update(disabled=False)
            InfDWindow["asteroidAmountInput"].update(amountValues[3])
            InfDWindow["asteroidAmountInput"].update(text_color="#000000")
            InfDWindow["asteroidAmountInput"].set_tooltip(None)

    running = False
    import os
    while True:
        event, values = InfDWindow.read(timeout=100)

        if event == "starAmountInput":
            try: 
                int(values["starAmountInput"])
            except:
                print("Not a number!")
                InfDWindow["starAmountInput"].update(values["starAmountInput"][:-1])

        if event == "planetAmountInput":
            try: 
                int(values["planetAmountInput"])
                if int(values["planetAmountInput"]) > 25:
                    InfDWindow["planetAmountInput"].update(25)
            except:
                print("Not a number!")
                InfDWindow["planetAmountInput"].update(values["planetAmountInput"][:-1])

        if event == "moonAmountInput":
            try: 
                int(values["moonAmountInput"])
            except:
                print("Not a number!")
                InfDWindow["moonAmountInput"].update(values["moonAmountInput"][:-1])
        
        if event == "asteroidAmountInput":
            try: 
                int(values["asteroidAmountInput"])
            except:
                print("Not a number!")
                InfDWindow["asteroidAmountInput"].update(values["asteroidAmountInput"][:-1])
        try:
            starAmount = int(values["starAmountInput"])
        except:
            starAmount = 0
        try:
            planetAmount = int(values["planetAmountInput"])
        except:
            planetAmount = 0
        try:
            moonAmount = int(values["moonAmountInput"])
        except:
            moonAmount = 0
        try:
            asteroidAmount = int(values["asteroidAmountInput"])
        except:
            asteroidAmount = 0

        #overrideSeed = False
        #overrideValues = False

        if event == "setSeed":
            customSeedInput = values["setSeed"]
            seperatedValues = customSeedInput.split(".")
            if not customSeedInput == "":
                if len(seperatedValues) > 1:
                    if len(seperatedValues[1]) >= 9 and len(seperatedValues[1]) <= 14:
                        try:
                            customSeed = int(seperatedValues[0])
                            fullySeperatedValues = seperatedValues[1].split(":")
                            maxPlanetOvrd = int(fullySeperatedValues[0])
                            maxMoonOvrd = int(fullySeperatedValues[1])
                            maxAsteroidOvrd = int(fullySeperatedValues[2])
                            minPlanetOvrd = int(fullySeperatedValues[3])
                            minMoonOvrd = int(fullySeperatedValues[4])
                            #maxPlanetOvrd, maxMoonOvrd, maxAsteroidOvrd, minPlanetOvrd, minMoonOvrd = seperatedValues[1].split(":")
                            if customSeed >= 0 and customSeed < (2**32):
                                print("Seed and overrides set.") # This is the part where there is both valid seed and overrides!
                                setStarAmntToOverriden()
                                setOtherAmntToOverriden()
                                overrideSeed = True # True
                                overrideValues = True # True
                            else:
                                print("ERROR: Seed out of bounds!")
                                setStarAmntToDefault()
                                setOtherAmntToDefault()
                                overrideSeed = False
                                overrideValues = False
                        except:
                            print("ERROR: Seed or overrides not integers!")
                            setStarAmntToDefault()
                            setOtherAmntToDefault()
                            overrideSeed = False
                            overrideValues = False
                    else:
                        try:
                            customSeed = int(seperatedValues[0])
                            if customSeed >= 0 and customSeed < (2**32):
                                print("Only seed applied. Invalid overrides.") # This is the part where a valid seed is set despite invalid overrides!
                                setStarAmntToOverriden()
                                setOtherAmntToDefault()
                                overrideSeed = True # True
                                overrideValues = False
                            else:
                                print("ERROR: Seed out of bounds! (Also invalid overrides.)")
                                setStarAmntToDefault()
                                setOtherAmntToDefault()
                                overrideSeed = False
                                overrideValues = False
                        except:
                            print("ERROR: Seed not integer! (Also invalid overrides.)")
                            setStarAmntToDefault()
                            setOtherAmntToDefault()
                            overrideSeed = False
                            overrideValues = False
                else:
                    try:
                        customSeed = int(seperatedValues[0])
                        if customSeed >= 0 and customSeed < (2**32):
                            print("Only seed applied.") # This is the part where a valid seed is set! (ONLY SEED, NO OVERRIDES.)
                            setStarAmntToOverriden()
                            setOtherAmntToDefault()
                            overrideSeed = True # True
                            overrideValues = False
                        else:
                            setStarAmntToDefault()
                            setOtherAmntToDefault()
                            print("ERROR: Seed out of bounds!")
                            overrideSeed = False
                            overrideValues = False
                    except:
                        print("ERROR: Seed not integer!")
                        setStarAmntToDefault()
                        setOtherAmntToDefault()
                        overrideSeed = False
                        overrideValues = False
            else:
                print("No seed set.")
                setStarAmntToDefault()
                setOtherAmntToDefault()
                overrideSeed = False
                overrideValues = False


        if event == "directoryText" or event == "starAmountInput" or event == "planetAmountInput" or event == "moonAmountInput" or event == "asteroidAmountInput":
            targetPath = values["directoryText"]
            print("Setting directory to: " + targetPath)
            print("Values are: " + "[" + str(starAmount) + "," + str(planetAmount) + "," + str(moonAmount) + "," + str(asteroidAmount) + "]")
            # cacheFile = open(cachePath, "w")
            # cacheFile.write(
            #     'filepath = "' + targetPath + '"' + "\n"
            #     "numbers = " + "[" + str(starAmount) + "," + str(planetAmount) + "," + str(moonAmount) + "," + str(asteroidAmount) + "]" + "\n"
            # )
            # cacheFile.close()

        if event == "openSettings":
            openSettings()

        if event == "openDelete":
            openDelete(targetPath)

        if event == "openHelp":
            openHelp()

        if Settings.useMultithreading == True:
            estTime = (((planetAmount * moonAmount * asteroidAmount) * starAmount)*15)/6.17
        else:
            estTime = ((planetAmount * moonAmount * asteroidAmount) * starAmount)*15

        if estTime >= 60:
            if estTime >= 3600:
                if estTime >= 86400:
                    if estTime >= 604800:
                        if estTime >= 2.628e+6:
                            if estTime >= 3.154e+7:
                                InfDWindow["timeRemainingText"].update("Estimated Generator Time: " + str(round((estTime/3.154e+7),2)) + " years.")
                            else:
                                InfDWindow["timeRemainingText"].update("Estimated Generator Time: " + str(round((estTime/2.628e+6),2)) + " months.")
                        else:
                            InfDWindow["timeRemainingText"].update("Estimated Generator Time: " + str(round((estTime/604800),2)) + " weeks.")
                    else:
                        InfDWindow["timeRemainingText"].update("Estimated Generator Time: " + str(round((estTime/86400),2)) + " days.")
                else:
                    InfDWindow["timeRemainingText"].update("Estimated Generator Time: " + str(round((estTime/3600),2)) + " hours.")
            else:
                InfDWindow["timeRemainingText"].update("Estimated Generator Time: " + str(round((estTime/60),2)) + " minutes.")
        else:
            InfDWindow["timeRemainingText"].update("Estimated Generator Time: " + str(round((estTime),2)) + " seconds.")

        #print("fine")

        #if not len(queue) < 1:
        #    for i in len(queue):
        #        allActions.append(queue[i])

        actionText = ""

        if state.allActionArrayUpdated == True:
            for a in range(lastMoment,len(allActions)):
                lastMoment = lastMoment + 1
                currentAction = allActions[a]
                actionText = str(currentAction[0].tm_hour) + ":" + str(currentAction[0].tm_min) + ":" + str(currentAction[0].tm_sec) + " - " + currentAction[1] + "\n"
                InfDWindow["currentActionText"].update(actionText,append=True)
                ActionLog.write(actionText)
                ActionLog.flush()
            state.allActionArrayUpdated = False

        if running == True:
            #print(amountOfThingsDone/amountOfThingsToDo)
            try:
                InfDWindow["startGenerator"].update(str((amountOfThingsDone/amountOfThingsToDo)*100) + "%")
            except ZeroDivisionError:
                print("Division by zero (ignore this)")

        if event == "startGenerator":
            #InfDWindow.set_icon(filepath + "/UIdata/StatusIcons/Icon_Working.ico")
            try: 
                int(values["starAmountInput"])
                try: 
                    int(values["planetAmountInput"])
                    try: 
                        int(values["moonAmountInput"])
                        try:
                            int(values["asteroidAmountInput"])
                        except:
                            print("Not a number!")
                    except:
                        print("Not a number!")
                except:
                    print("Not a number!")
            except:
                print("Not a number!")

            print("The generator should take AT MOST " + str(round((estTime/60),2)) + " minutes.")

            InfDWindow["currentFocusText"].update("Generator is active.")
            InfDWindow["startGenerator"].update("0%")
            InfDWindow["startGenerator"].update(disabled=True)

            running = True

            #InfDWindow["startGenerator"].hide_row()

            #allActions.append("Making directory at: " + targetPath)

            #os.makedirs(targetPath + "/InfiniteDiscoveries_Systems", exist_ok=True)

            #print(currentActionLayout)

            #time.sleep(1)

            #systemThread = threading.Thread(target=systemLoop, args=(queue,starAmount,planetAmount,moonAmount,targetPath))
            #systemThread.run()

            if not values["setSeed"] == "":
                if overrideSeed == True and overrideValues == False:
                    startLoop(starAmount,planetAmount,moonAmount,asteroidAmount,targetPath,customSeed)
                elif overrideSeed == True and overrideValues == True:
                    startLoop(starAmount,planetAmount,moonAmount,asteroidAmount,targetPath,customSeed,[maxPlanetOvrd,maxMoonOvrd,maxAsteroidOvrd,minPlanetOvrd,minMoonOvrd])
                else:
                    startLoop(starAmount,planetAmount,moonAmount,asteroidAmount,targetPath)
                global mainThreadFinished
                mainThreadFinished = False
            else:
                startLoop(starAmount,planetAmount,moonAmount,asteroidAmount,targetPath)
                mainThreadFinished = False

            #for a in allThreads:
            #    a.join()
        if mainThreadFinished == True:
            #InfDWindow.set_icon(filepath + "/UIdata/StatusIcons/Icon_Idle.ico")
            #InfDWindow["startGenerator"].unhide_row()
            InfDWindow["currentFocusText"].update("Generator is finished!")
            InfDWindow["startGenerator"].update("Generate")
            InfDWindow["startGenerator"].update(disabled=False)

            running = False

            InfDWindow.refresh()

        try:
            allKopConfigs = os.listdir(targetPath + "/InfiniteDiscoveries/Configs/")
            allEVEConfigs = os.listdir(targetPath + "/InfiniteDiscoveries/Visuals/EVE/Configs/")
            allParallaxConfigs = os.listdir(targetPath + "/InfiniteDiscoveries/Visuals/Parallax/Configs/")
            #allKopConfigs = os.listdir(targetPath + "/InfiniteDiscoveries/Visuals/Parallax/Configs/")
            allTextures = os.listdir(targetPath + "/InfiniteDiscoveries/Textures/PluginData/")
            allCloudTextures = os.listdir(targetPath + "/InfiniteDiscoveries/Textures/Clouds/")
            allALLTextures = allTextures + allCloudTextures
            #print(len(allKopConfigs))
            allScattererConfigs = os.listdir(targetPath + "/InfiniteDiscoveries/Visuals/Scatterer/")
            allRRConfigs = os.listdir(targetPath + "/InfiniteDiscoveries/Misc/RR/")
            #print(len(allScattererConfigs))
            allSystems = []
            for scattererCfg in allScattererConfigs:
                if "ScattererSunflare" in scattererCfg:
                    systemName = scattererCfg.replace("ScattererSunflare", "").replace("_", "").replace(".cfg", "").replace("1","").replace("2","").replace("-","")
                    allSystems.append(systemName)
                    #print(systemName)
            #print(len(allSystems))
            allSystemsREAL = np.unique(allSystems)

            allConfigs = allKopConfigs + allEVEConfigs + allParallaxConfigs + allScattererConfigs + allRRConfigs
            #print(allConfigs)
            InfDWindow["stats_SystemAmount"].update("Amount of systems: " + str(len(allSystemsREAL)))
            InfDWindow["stats_ConfigAmount"].update("Amount of configs: " + str(len(allConfigs)))
            InfDWindow["stats_TextureAmount"].update("Amount of textures: " + str(len(allALLTextures)))
        except:
            InfDWindow["stats_SystemAmount"].update("Amount of systems: No directory!")
            InfDWindow["stats_ConfigAmount"].update("Amount of configs: No directory!")
            InfDWindow["stats_TextureAmount"].update("Amount of textures: No directory!")

        if os.access(targetPath, os.W_OK):
            InfDWindow["okToAccess"].update("Selected directory can be written to.")
            InfDWindow["okToAccess"].update(text_color=("#8fff8f"))
        else:
            InfDWindow["okToAccess"].update("Cannot write to selected directory!")
            InfDWindow["okToAccess"].update(text_color=("#ff8f8f"))

        if event == sg.WINDOW_CLOSED:
            global everythingEnded
            everythingEnded = True
            import os
            import signal

            # Get the process ID (PID) of the current Python process
            current_pid = os.getpid()

            print(current_pid)

            # Terminate the current process using its PID
            os.kill(current_pid, signal.SIGTERM)

            break

if currentProcess.name == "MainThread":
    startUI()

#print("gagagaga")

#systemLoop(StarAmount, AmountOfPlanetsToGenerate, AmountOfMoonsToGenerate)

print("All done!")
print("---------------------------------------------------------------")
print("Total number of stars generated: " + str(totalStarsGenerated))
print("Total number of planets generated: " + str(totalPlanetsGenerated))
print("Total number of moons generated: " + str(totalMoonsGenerated))
print("---------------------------------------------------------------")
print("Total objects generated: " + str(totalStarsGenerated + totalPlanetsGenerated + totalMoonsGenerated))
print("---------------------------------------------------------------")
#print("Now it's REALLY all done!")
#print("---------------------------------------------------------------")
endTime = time.time()
elapsedTime = endTime - startTime
if elapsedTime > 60:
    print("Time elapsed: " + str(round(elapsedTime/60,2)) + " minutes.")
elif elapsedTime < 60:
    print("Time elapsed: " + str(round(elapsedTime,2)) + " seconds.")