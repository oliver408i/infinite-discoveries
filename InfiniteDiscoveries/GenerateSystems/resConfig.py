import random

# Make resourced for Rational Resourced because yummy
def createResourceConfig(seed,config,bodyName,lava,icy,temp,pressure,ocean,gasGiant,life,starType):
    resourceRNG = random.Random()
    resourceRNG.seed(seed)
    resources = []

    if not starType == None:
        if starType == "RedGiant": 
            resources.append("StarDyingRedGiant")
        elif starType == "Neutron":
            resources.append("StarNeutron")
        else:
            if resourceRNG.randint(0,100) > 10:
                resources.append("StarPop1")
            else:
                resources.append("StarPop2")

    if starType == None:
        if gasGiant == False:
            #resources.append("SrfRock")
            #resources.append("SrfSilica")
            #resources.append("SrfRockMetal")
            #resources.append("SrfRockMineral")

            #if resourceRNG.randint(0,10) == 0:
            #    resources.append("ExoRock")
            #
            #if resourceRNG.randint(0,1) == 0:
            #    resources.append("SrfAlumina")
            #if resourceRNG.randint(0,1) == 0:
            #    resources.append("SrfMetalCarbon")
            #if resourceRNG.randint(0,1) == 0:
            #    resources.append("SrfMetalSulfur")
            if lava == True:
                resources.append("SrfVulcan")
                resources.append("OcnLava")
            elif icy == True:    
                if ocean == False:            
                    if temp < 273:
                        resources.append("SrfIceWater")
                    if temp < 91:
                        resources.append("SrfIceMethane")
                    if temp < 63:
                        resources.append("SrfIceNitrogen")
                else:
                    resources.append("SrfRockIce")
            else:
                randomGroundResource = resourceRNG.randint(0,100)
                if randomGroundResource > 0 and randomGroundResource < 10:
                    resources.append("ExoRock")
                elif randomGroundResource >= 10 and randomGroundResource < 20:
                    resources.append("SrfAlumina")
                elif randomGroundResource >= 20 and randomGroundResource < 30:
                    resources.append("SrfMetalCarbon")
                elif randomGroundResource >= 30 and randomGroundResource < 40:
                    resources.append("SrfMetalSulfur")
                elif randomGroundResource >= 40 and randomGroundResource < 50:
                    resources.append("SrfRockMineral")
                elif randomGroundResource >= 50 and randomGroundResource < 60:
                    resources.append("SrfSilica")
                elif randomGroundResource >= 60 and randomGroundResource < 70:
                    resources.append("SrfRockMetal")
                else:
                    resources.append("SrfRock")
            
            if ocean == True:
                if life == "exotic":
                    if resourceRNG.randint(0,2) == 0:
                        resources.append("OcnAcid")
                    else:
                        resources.append("OcnKerosene")
                else:
                    if temp < 240:
                        resources.append("OcnAmmonia")
                    elif temp < 195:
                        resources.append("OcnOxygenC")
                    elif temp < 121:
                        resources.append("OcnOxygenN")
                    elif temp < 111:
                        resources.append("OcnMethane")
                    elif temp < 90:
                        resources.append("OcnOxygen")
                    elif temp < 77:
                        resources.append("OcnNitrogen")
                    else:
                        resources.append("OcnTerra")

            if pressure > 0:
                #if life == "organic":
                #    resources.append("AtmOxygen")
                #else:
                #    resources.append("AtmDefault")
                #if lava == True:
                #    resources.append("AtmVulcan")
                if life == "organic":
                    resources.append("AtmOxygen")
                else:
                    if ocean == True:
                        if temp < 273:
                            resources.append(resourceRNG.choice(["AtmIceWaterThick","AtmIceWaterThin"]))
                        elif temp < 194:
                            resources.append("AtmIceAmmonia")
                        elif temp < 91:
                            resources.append("AtmIceMethane")
                        elif temp < 63:
                            resources.append("AtmIceNitrogen")
                        else:
                            resources.append("AtmDefault")
                    elif lava == True:
                        resources.append("AtmVulcan")
                    else:
                        if temp < 373:
                            resources.append("AtmDefault")
                        elif temp < 273:
                            resources.append(resourceRNG.choice(["AtmIceWaterThick","AtmIceWaterThin"]))
                        elif temp < 194:
                            resources.append("AtmIceAmmonia")
                        elif temp < 91:
                            resources.append("AtmIceMethane")
                        elif temp < 63:
                            resources.append("AtmIceNitrogen")
                        else:
                            resources.append(resourceRNG.choice(["AtmSteam","AtmSteamC","AtmSteamN"]))
        else: # "AtmGasI","AtmGasII","AtmGasIII","AtmGasIV","AtmGasIV"
            if temp < 150:
                resources.append("AtmGasI")
            elif temp < 250:
                resources.append("AtmGasII")
            elif temp < 800:
                resources.append("AtmGasIII")
            elif temp < 1400:
                resources.append("AtmGasIV")
            else:
                resources.append("AtmGasV")

    print(resources)
    for resource in resources:
        config.write(
            "+PLANETARY_RESOURCE:HAS[#Tag[" + resource + "]]\n"
            "{\n"
            "    @PlanetName = "+ bodyName +"\n"
            "    @Tag = Applied\n"
            "}\n"
        )