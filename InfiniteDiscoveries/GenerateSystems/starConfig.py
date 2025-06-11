import random, time, state

# Writes star configs.
def writeStarCfg(cfgSeed, starCfg, starName, starRadius, starMass, starDist, RGBfinal, starDistG, dispName, Tag, typeOfStar, Lum, coronaColor, parentBarycenter=None, period=None, maaoD=None, parentGalaxy=None, binaryEccentricity=None, binaryType=None, allActions=[], AmountOfMoonsToGenerate=0, AmountOfAsteroidsToGenerate=0, AmountOfPlanetsToGenerate=0, minPlanets=0, minMoons=0):
    starCfgRNG = random.Random()
    starCfgRNG.seed(cfgSeed)
    allActions.append([time.localtime(),"Writing config for star: " + starName])
    state.allActionArrayUpdated = True
    print(starRadius)
    defaultSOIforNonBinaryStars = 350000000000
    #print(starMass)
    if typeOfStar == "RedGiant":
        brightnessThing = (starRadius/30)*5 # I honestly do not know what to call these variables anymore.
    elif typeOfStar == "BrownDwarf":
        brightnessThing = starRadius*4
        randomThingamabob = starCfgRNG.randint(1,3) # ????????????????????????
        if randomThingamabob == 1: # Redder brown dwarfs
            mainR = 0 #random.randint(0,100)/100
            mainG = 0 #mainR/2
            secR = starCfgRNG.randint(60,100)/100
            secG = starCfgRNG.randint(0,int((secR*100)/2))/100
        elif randomThingamabob == 2: # Same as 1 but inverted and a bit yellower
            mainR = starCfgRNG.randint(75,100)/100
            mainG = starCfgRNG.randint(0,int((mainR*100)*0.3))/100
            secR = 0
            secG = 0
        elif randomThingamabob == 3: # Random bullshit
            mainR = starCfgRNG.randint(50,100)/100
            mainG = mainR/1.5
            secR = starCfgRNG.randint(25,75)/100
            secG = 0
        
    elif typeOfStar == "Neutron":
        brightnessThing = starRadius*5450
    elif typeOfStar == "WhiteDwf":
        brightnessThing = starRadius*50
    elif typeOfStar == "WolfRayet":
        brightnessThing = 1048800000
        defaultSOIforNonBinaryStars = 2000000000000
    else:
        if starRadius > 523200000:
            brightnessThing = 523200000
        elif starRadius < 348800000:
            brightnessThing = 348800000
        else:
            brightnessThing = starRadius

    print(starName + " brightness: " + str(brightnessThing))
    starCfg.write(
        "@Kopernicus:AFTER[Kopernicus]\n"
        "{\n"
        "    Body\n"
        "    {\n"
        "        name = " + starName + "\n"
    )
    if typeOfStar == "RedGiant":
        starCfg.write(
            "        cacheFile = InfiniteDiscoveries/Misc/RedGiantBump.bin\n"
        )
    else:
        starCfg.write(
            "        cacheFile = InfiniteDiscoveries/Cache/" + starName + ".bin" + "\n"
        )
    starCfg.write(
        "        Tag = " + Tag + "\n"
        "        Template\n"
        "        {\n"
        "            name = Sun\n"
        "        }\n"
    )
    if not parentBarycenter == None:
        starCfg.write(
            "        Properties\n"
            "        {\n"
            "            displayName = " + dispName + "^N" + "\n"
        )
        starCfg.write(
            "            radius = " + str(starRadius) + "\n"
            "            mass = " + str(starMass) + "\n"
            "            rotationPeriod = 1063000.6069891\n"
            "            tidallyLocked = true\n"
            "            description = " + str(starName) + " is a randomly generated star roughly " + str(round(starRadius / 261600000, 2)) + " times the size of Kerbol! \\n<color=#faff9e>This star was generated using seed " + str(cfgSeed) + "." + str(AmountOfPlanetsToGenerate) + ":" + str(AmountOfMoonsToGenerate) + ":" + str(AmountOfAsteroidsToGenerate) + ":" + str(minPlanets) + ":" + str(minMoons) +  " (CHECK BARYCENTER FOR SYSTEM SEED)\n"
        )
        if binaryType == "Distant":
            starCfg.write(
                "            sphereOfInfluence = 100000000000\n"
            )
        starCfg.write(
            "            ScienceValues\n"
            "            {\n"
            "                landedDataValue = 10000\n"
            "                flyingLowDataValue = 20\n"
            "                flyingHighDataValue = 20\n"
            "                inSpaceLowDataValue = 20\n"
            "                inSpaceHighDataValue = 5\n"
            "                recoveryValue = 10\n"
            "                flyingAltitudeThreshold = 18000\n"
            "                spaceAltitudeThreshold = 1E+09\n"
            "            }\n"	
            "        }\n"
        )
        if binaryType == "Near":
            starCfg.write(
                "        Orbit\n"
                "        {\n"
                "            referenceBody = " + parentBarycenter + "\n"
                "            color = " + RGBfinal + ", 1\n"
                "            semiMajorAxis = " + str(starDist*4.2) + "\n"
                "            inclination = " + str(0) + "\n"
                "            eccentricity = " + str(0) + "\n"
                "            longitudeOfAscendingNode = " + str(0) + "\n"
                "            argumentOfPeriapsis = " + str(0) + "\n"
                "            meanAnomalyAtEpochD = " + str(maaoD) + "\n"
                "            period = " + str(period) + "\n"
                "            epoch = 0\n"
                "            iconTexture = InfiniteDiscoveries/Textures/Misc/starIcon.png\n"
                "        }\n"
            )
        else:
            starCfg.write(
                "        Orbit\n"
                "        {\n"
                "            referenceBody = " + parentBarycenter + "\n"
                "            color = " + RGBfinal + ", 1\n"
                "            semiMajorAxis = " + str(starDist*4.2) + "\n"
                "            inclination = " + str(0) + "\n"
                "            eccentricity = " + str(binaryEccentricity) + "\n"
                "            longitudeOfAscendingNode = " + str(maaoD) + "\n"
                "            argumentOfPeriapsis = " + str(0) + "\n"
                "            meanAnomalyAtEpochD = " + str(0) + "\n"
                "            period = " + str(period) + "\n"
                "            epoch = 0\n"
                "            iconTexture = InfiniteDiscoveries/Textures/Misc/starIcon.png\n"
                "        }\n"
            )
    else:
        starCfg.write(
            "        Properties\n"
            "        {\n"
            "            displayName = " + dispName + "^N" + "\n"
        )
        if not typeOfStar == "neutron":
            starCfg.write(
                "            radius = " + str(starRadius) + "\n"
            )
        else:
            starCfg.write(
                "            radius = " + str(10000) + "\n"
            )
        print(str(starMass) + " <------------ WHY")
        print(parentGalaxy)
        starCfg.write(
            "            mass = " + str(starMass) + "\n"
            "            rotationPeriod = 5000.6069891\n"
            "            tidallyLocked = false\n"
            "            description = " + str(starName) + " is a randomly generated star roughly " + str(round(starRadius / 261600000, 2)) + " times the size of Kerbol! \\n<color=#faff9e>This system was generated using seed " + str(cfgSeed) + "." + str(AmountOfPlanetsToGenerate) + ":" + str(AmountOfMoonsToGenerate) + ":" + str(AmountOfAsteroidsToGenerate) + ":" + str(minPlanets) + ":" + str(minMoons) + "\n"
            "            sphereOfInfluence = " + str(defaultSOIforNonBinaryStars) + "\n"
            "            ScienceValues\n"
            "            {\n"
            "                landedDataValue = 10000\n"
            "                flyingLowDataValue = 20\n"
            "                flyingHighDataValue = 20\n"
            "                inSpaceLowDataValue = 20\n"
            "                inSpaceHighDataValue = 5\n"
            "                recoveryValue = 10\n"
            "                flyingAltitudeThreshold = 18000\n"
            "                spaceAltitudeThreshold = 1E+09\n"
            "            }\n"	
            "        }\n"
            "        Orbit\n"
            "        {\n"
            "            referenceBody = Sun\n"
            "            color = " + RGBfinal + ", 1\n"
            "            semiMajorAxis = " + str(starDist) + "\n"
            "            inclination = " + str(starCfgRNG.randint(0,360)) + "\n"
            "            eccentricity = " + str(starCfgRNG.randint(0,500)/1000) + "\n"
            "            longitudeOfAscendingNode = 0\n"
            "            argumentOfPeriapsis = 0\n"
            "            meanAnomalyAtEpochD = " + str(starCfgRNG.randint(0,360)) + "\n"
            "            epoch = 0\n"
            "            mode = OFF\n"
            "            iconTexture = InfiniteDiscoveries/Textures/Misc/starIcon.png\n"
            "        }\n"
        )
    
    starCfg.write(
        "        ScaledVersion\n"
        "        {\n"
        "            type = Star\n"
    ) 
    if parentBarycenter == None or binaryType == "Distant":
        starCfg.write(
            "            Light\n"
            "            {\n"
            "                sunlightColor = " + RGBfinal + ", 1\n"
            "                sunlightShadowStrength = 0.75\n"
            "                scaledSunlightColor = " + RGBfinal + ", 1\n"
            "                IVASunColor = " + RGBfinal + ", 1\n"
            "                sunLensFlareColor = " + RGBfinal + ", 1\n"
            "                givesOffLight = true\n"
        )
        if typeOfStar == "neutron":
            starCfg.write(
                "                sunAU = 18000000\n"
            )
        else:
            starCfg.write(
                "                sunAU = " + str(16000000000 * (starRadius/261600000)) + "\n"
            )
        starCfg.write(
            "                luminosity = " + str(Lum) + "\n"
            "                insolation = 0.15\n"
            "                brightnessCurve\n"
            "                {\n"
            "                   key = -0.01573471 0 1.706627 1.706627\n"
            "                   key = 5.084181 5.997075 -0.001802375\n"
            "                   key = 38.56295 10.82142 0.0001713 0.0001713\n"
            "                }\n"
            "                IntensityCurve\n"
            "                {\n"
            "                    key = 0 " + str((brightnessThing / 261600000)/1.1) + " 0 0\n"
            "   			     key = " + str((760320000000*(brightnessThing / 261600000))) + " 0 0 0\n"
            "                }\n"
            "                ScaledIntensityCurve\n"
            "                {\n"
            "                   key = 0 " + str((brightnessThing / 261600000)/1.1) + " 0 0\n"
            "                   key = " + str((126720000*(brightnessThing / 261600000))) + " 0 0 0\n"
            "                }\n"
            "                IVAIntensityCurve\n"
            "                {\n"
            "                   key = 0 " + str((brightnessThing / 261600000)/1.1) + " 0 0\n"
            "          			key = " + str((760320000000*(brightnessThing / 261600000))) + " 0 0 0\n"
            "                }\n"
            "            }\n"
        )
    else:
        #starCfg.write(
        #    "            Light:NEEDS[Parallax]\n"
        #    "            {\n"
        #    "                sunlightColor = " + RGBfinal + ", 1\n"
        #    "                sunlightShadowStrength = 0.75\n"
        #    "                scaledSunlightColor = " + RGBfinal + ", 1\n"
        #    "                IVASunColor = " + RGBfinal + ", 1\n"
        #    "                sunLensFlareColor = " + RGBfinal + ", 1\n"
        #    "                givesOffLight = false\n"
        #)
        #if typeOfStar == "neutron":
        #    starCfg.write(
        #        "                sunAU = 18000000\n"
        #    )
        #else:
        #    starCfg.write(
        #        "                sunAU = " + str(16000000000 * (starRadius/261600000)) + "\n"
        #    )
        #starCfg.write(
        #    "                luminosity = " + str(Lum) + "\n"
        #    "                insolation = 0.15\n"
        #    "                brightnessCurve\n"
        #    "                {\n"
        #    "                   key = -0.01573471 0 1.706627 1.706627\n"
        #    "                   key = 5.084181 5.997075 -0.001802375\n"
        #    "                   key = 38.56295 10.82142 0.0001713 0.0001713\n"
        #    "                }\n"
        #    "                IntensityCurve\n"
        #    "                {\n"
        #    "                    key = 0 " + str((brightnessThing / 261600000)/1.1) + " 0 0\n"
        #    "   			     key = " + str((760320000000*(brightnessThing / 261600000))) + " 0 0 0\n"
        #    "                }\n"
        #    "                ScaledIntensityCurve\n"
        #    "                {\n"
        #    "                   key = 0 " + str((brightnessThing / 261600000)/1.1) + " 0 0\n"
        #    "                   key = " + str((126720000*(brightnessThing / 261600000))) + " 0 0 0\n"
        #    "                }\n"
        #    "                IVAIntensityCurve\n"
        #    "                {\n"
        #    "                   key = 0 " + str((brightnessThing / 261600000)/1.1) + " 0 0\n"
        #    "          			key = " + str((760320000000*(brightnessThing / 261600000))) + " 0 0 0\n"
        #    "                }\n"
        #    "            }\n"
        #)
        starCfg.write(
            "            Light\n"
            "            {\n"
            "                sunlightColor = " + RGBfinal + ", 1\n"
            "                sunlightShadowStrength = 0.75\n"
            "                scaledSunlightColor = " + RGBfinal + ", 1\n"
            "                IVASunColor = " + RGBfinal + ", 1\n"
            "                sunLensFlareColor = " + RGBfinal + ", 1\n"
            "                givesOffLight = true\n"
        )
        if typeOfStar == "neutron":
            starCfg.write(
                "                sunAU = 18000000\n"
            )
        else:
            starCfg.write(
                "                sunAU = " + str(13599840256 * (starRadius/261600000)) + "\n"
            )
        starCfg.write(
            "                luminosity = " + str(Lum) + "\n"
            "                insolation = 0.15\n"
            "                brightnessCurve\n"
            "                {\n"
            "                   key = -0.01573471 0 1.706627 1.706627\n"
            "                   key = 5.084181 5.997075 -0.001802375\n"
            "                   key = 38.56295 10.82142 0.0001713 0.0001713\n"
            "                }\n"
            "                IntensityCurve\n"
            "                {\n"
            "                    key = 0 " + str((brightnessThing / 261600000)/1.1) + " 0 0\n"
            "   			     key = " + str((760320000000*(brightnessThing / 261600000))) + " 0 0 0\n"
            "                }\n"
            "                ScaledIntensityCurve\n"
            "                {\n"
            "                   key = 0 " + str((brightnessThing / 261600000)/1.1) + " 0 0\n"
            "                   key = " + str((126720000*(brightnessThing / 261600000))) + " 0 0 0\n"
            "                }\n"
            "                IVAIntensityCurve\n"
            "                {\n"
            "                   key = 0 " + str((brightnessThing / 261600000)/1.1) + " 0 0\n"
            "          			key = " + str((760320000000*(brightnessThing / 261600000))) + " 0 0 0\n"
            "                }\n"
            "            }\n"

        )
    if typeOfStar == "RedGiant":
        starCfg.write(
            "            Material\n"
            "            {\n"
            "               emitColor0 = " + RGBfinal + ", 1\n"
            "               emitColor1 = " + RGBfinal + ", 1\n"
            "               sunspotTex = InfiniteDiscoveries/Textures/Misc/redGiantMap.dds\n"
            "               sunspotPower = 2\n"
            "               sunspotColor = 0,0,0,1\n"
            "               rimColor = 0,0,0,1\n"
            "               rimPower = 1\n"
            "               rimBlend = -0.3\n"
            "            }\n"
        )
    elif typeOfStar == "BrownDwarf":
        starCfg.write(
            "            Material\n"
            "            {\n"
            "               emitColor0 = " + str(mainR) + ", " + str(mainG) + ", 0, 1\n"
            "               emitColor1 = " + str(mainR) + ", " + str(mainG) + ", 0, 1\n"
            "               sunspotTex = InfiniteDiscoveries/Textures/Misc/brownDwarfMap.dds\n"
            "               sunspotPower = 1\n"
            "               sunspotColor = " + str(secR) + ", " + str(secG) + ", 0, 1\n"
            "               rimColor = 0,0,0,1\n"
            "               rimPower = 1\n"
            "               rimBlend = -0.3\n"
            "            }\n"
        )
    else:
        starCfg.write(
            "            Material\n"
            "            {\n"
            "               emitColor0 = " + RGBfinal + ", 1\n"
            "               emitColor1 = " + RGBfinal + ", 1\n"
            "               sunspotTex = BUILTIN/sunsurfacenew\n"
            "               sunspotPower = 1\n"
            "               sunspotColor = 0.283582091,0.126710668,0.0208224356,1\n"
            "               rimColor = 0,0,0,1\n"
            "               rimPower = 1\n"
            "               rimBlend = -0.3\n"
            "            }\n"
        )
    starCfg.write(
        "            Coronas\n"
        "            {\n"
        "                Value\n"
        "                {\n"
        "                    scaleSpeed = 0.007\n"
        "                    scaleLimitY = 3\n"
        "                    scaleLimitX = 5\n"
        "                    updateInterval = 5\n"
        "                    speed = -1\n"
        "                    rotation = 0\n"
        "                    Material\n"
        "                    {\n"
        "                        texture = InfiniteDiscoveries/Textures/Misc/" + coronaColor + ".dds\n"
        "                        mainTexScale = 1,1\n"
        "                        mainTexOffset = 0,0\n"
        "                        invFade = 2.553731\n"
        "                    }\n"
        "                }\n"
        "            }\n"
        "        }\n"
        "    }\n"
        "}\n"
    )
    if parentBarycenter == None:
        starCfg.write(
            "@Kopernicus:LAST[InfiniteDiscoveries]:HAS[@InfiniteDiscoveriesSettings:HAS[#GalaxyMode[?rue]]]\n"
            "{\n"
            "    @Body:HAS[#name[" + starName + "]]\n"
            "    {\n"
            "        !Orbit{}\n"
            "        Orbit\n"
            "        {\n"
            "            referenceBody = " + parentGalaxy + "\n"
            "            color = " + RGBfinal + ", 1\n"
            "            semiMajorAxis = " + str(starDistG) + "\n"
        )
        if parentGalaxy == "LKC_CtrlB":
            starCfg.write(
                "            inclination = " + str(starCfgRNG.randint(80,100)) + "\n"
            )
        elif parentGalaxy == "SKC_CtrlB":
            starCfg.write(
                "            inclination = " + str(starCfgRNG.randint(80,100)) + "\n"
            )
        else:
            starCfg.write(
                "            inclination = " + str(starCfgRNG.randint(0,10)) + "\n"
            )
        starCfg.write(
            "            eccentricity = " + str(starCfgRNG.randint(0,200)/1000) + "\n"
            "            longitudeOfAscendingNode = 0\n"
            "            argumentOfPeriapsis = 0\n"
            "            meanAnomalyAtEpochD = " + str(starCfgRNG.randint(0,360)) + "\n"
            "            epoch = 0\n"
            "            mode = OFF\n"
            "            iconTexture = InfiniteDiscoveries/Textures/Misc/starIcon.png\n"
            "        }\n"
            "    }\n"
            "}\n"
        )
    allActions.append([time.localtime(),"Wrote config for star: " + starName])
    state.allActionArrayUpdated = True
# Writes barycenter configs.
def writeBarycenterCfg(barySeed, baryCfg, baryName, baryRadius, baryMass, baryDist, systemName, starColors, baryDistG, baryDispName, averageClr, baryBrightness, parentGalaxy, binaryType, starTypes, AmountOfPlanetsToGenerate, AmountOfMoonsToGenerate, AmountOfAsteroidsToGenerate, minPlanets, minMoons):
    baryRNG = random.Random()
    baryRNG.seed(barySeed)
    baryCfg.write(
        "@Kopernicus:AFTER[Kopernicus]\n"
        "{\n"
        "    Body\n"
        "    {\n"
        "        name = " + baryName + "\n"
        "        cacheFile = InfiniteDiscoveries/Cache/" + baryName + ".bin" + "\n"
        "        Tag = InfD_Barycenter\n"
        "        Template\n"
        "        {\n"
        "            name = Sun\n"
        "        }\n"
        "        Properties\n"
        "        {\n"
        "            displayName = " + baryDispName + "^N" + "\n"
        "            radius = " + str(baryRadius/4.2) + "\n"
        "            mass = " + str(baryMass) + "\n"
        "            rotationPeriod = 1063000.6069891\n"
        "            tidallyLocked = false\n"
        "            description = The barycenter of the " + str(systemName) + " system. \\n<color=#faff9e>This system was generated using seed " + str(barySeed) + "." + str(AmountOfPlanetsToGenerate) + ":" + str(AmountOfMoonsToGenerate) + ":" + str(AmountOfAsteroidsToGenerate) + ":" + str(minPlanets) + ":" + str(minMoons) + "\n"
    )
    if binaryType == "Distant":
        baryCfg.write(
            "            sphereOfInfluence = 3000000000000\n"
        )
    else:
        if starTypes[0] == "WolfRayet" or starTypes[1] == "WolfRayet":
            baryCfg.write(
                "            sphereOfInfluence = 2000000000000\n"
            )
        else:
            baryCfg.write(
                "            sphereOfInfluence = 350000000000\n"
            )
    baryCfg.write(
        "            ScienceValues\n"
        "            {\n"
        "                landedDataValue = 100000000000000\n"
        "                flyingLowDataValue = 2000000000\n"
        "                flyingHighDataValue = 20000000\n"
        "                inSpaceLowDataValue = 200000\n"
        "                inSpaceHighDataValue = 5\n"
        "                recoveryValue = 10\n"
        "                flyingAltitudeThreshold = 18000\n"
        "                spaceAltitudeThreshold = 1E+09\n"
        "            }\n"	
        "        }\n"
        "        Orbit\n"
        "        {\n"
        "            referenceBody = Sun\n"
        "            color = " + starColors + ", 1\n"
        "            semiMajorAxis = " + str(baryDist) + "\n"
        "            inclination = " + str(baryRNG.randint(0,360)) + "\n"
        "            eccentricity = " + str(baryRNG.randint(0,500)/1000) + "\n"
        "            longitudeOfAscendingNode = 0\n"
        "            argumentOfPeriapsis = 0\n"
        "            meanAnomalyAtEpochD = " + str(baryRNG.randint(0,360)) + "\n"
        "            epoch = 0\n"
        "            mode = OFF\n"
        "            iconTexture = InfiniteDiscoveries/Textures/Misc/binaryStarIco.png\n"
        "        }\n"
        "        ScaledVersion\n"
        "        {\n"
        "            type = Star\n"
        "            invisible = True\n"
    )
    if binaryType == "Near":
        baryCfg.write(
            "            Light\n"
            "            {\n"
            "                givesOffLight = false\n"
            "            }\n"
            "            //Light:NEEDS[Parallax]\n"
            "            //{\n"
            "            //    sunlightColor = " + str(averageClr[0]) + ", " + str(averageClr[1]) + ", " + str(averageClr[2]) + "\n"
            "            //    sunlightShadowStrength = 0.75\n"
            "            //    scaledSunlightColor = " + str(averageClr[0]) + ", " + str(averageClr[1]) + ", " + str(averageClr[2]) + "\n"
            "            //    IVASunColor = " + str(averageClr[0]) + ", " + str(averageClr[1]) + ", " + str(averageClr[2]) + "\n"
            "            //    sunLensFlareColor = 0, 0, 0, 0\n"
            "            //    givesOffLight = true\n"
            "            //    sunAU = 1\n"
            "            //    luminosity = 1\n"
            "            //    insolation = 0.15\n"
            "            //    brightnessCurve\n"
            "            //    {\n"
            "            //       key = -0.01573471 0 1.706627 1.706627\n"
            "            //       key = 5.084181 5.997075 -0.001802375\n"
            "            //       key = 38.56295 10.82142 0.0001713 0.0001713\n"
            "            //    }\n"
            "            //    IntensityCurve\n"
            "            //    {\n"
            "            //        key = 0 " + str((baryBrightness / 261600000)/1.1) + " 0 0\n"
            "   		 //	     key = " + str((90000000000*(baryBrightness / 261600000))) + " " + str((baryBrightness / 261600000)/1.5) + " -2E-12 -2E-12\n"
            "   		 //	     key = " + str((150000000000*(baryBrightness / 261600000))) + " 0 0 0\n"
            "            //    }\n"
            "            //    ScaledIntensityCurve\n"
            "            //    {\n"
            "            //       key = 0 " + str((baryBrightness / 261600000)/1.1) + " 0 0\n"
            "         	 //		key = " + str((15000000*(baryBrightness / 261600000))) + " " + str((baryBrightness / 261600000)/1.5) + " -1.2E-08 -1.2E-08\n"
            "            //       key = " + str((30000000*(baryBrightness / 261600000))) + " 0 0 0\n"
            "            //    }\n"
            "            //    IVAIntensityCurve\n"
            "            //    {\n"
            "            //       key = 0 " + str((baryBrightness / 261600000)/1.1) + " 0 0\n"
            "          	 //		key = " + str((90000000000*(baryBrightness / 261600000))) + " " + str((baryBrightness / 261600000)/1.5) + " -1.8E-12 -1.8E-12\n"
            "          	 //		key = " + str((150000000000*(baryBrightness / 261600000))) + " 0 0 0\n"
            "            //    }\n"
            "            //}\n"
            "        }\n"
            "    }\n"
            "}\n"
        )
    else:
        baryCfg.write(
            "            Light\n"
            "            {\n"
            "                givesOffLight = false\n"
            "            }\n"
            "        }\n"
            "    }\n"
            "}\n"
        )
    baryCfg.write(
        "@Kopernicus:LAST[InfiniteDiscoveries]:HAS[@InfiniteDiscoveriesSettings:HAS[#GalaxyMode[?rue]]]\n"
        "{\n"
        "    @Body:HAS[#name[" + baryName + "]]\n"
        "    {\n"
        "        !Orbit{}"
        "        Orbit\n"
        "        {\n"
        "            referenceBody = " + parentGalaxy + "\n"
        "            color = " + starColors + ", 1\n"
        "            semiMajorAxis = " + str(baryDistG) + "\n"
    )
    if parentGalaxy == "LKC_CtrlB":
        baryCfg.write(
            "            inclination = " + str(baryRNG.randint(80,100)) + "\n"
        )
    elif parentGalaxy == "SKC_CtrlB":
        baryCfg.write(
            "            inclination = " + str(baryRNG.randint(80,100)) + "\n"
        )
    else:
        baryCfg.write(
            "            inclination = " + str(baryRNG.randint(0,10)) + "\n"
        )
    baryCfg.write(
        "            eccentricity = " + str(baryRNG.randint(0,200)/1000) + "\n"
        "            longitudeOfAscendingNode = 0\n"
        "            argumentOfPeriapsis = 0\n"
        "            meanAnomalyAtEpochD = " + str(baryRNG.randint(0,360)) + "\n"
        "            epoch = 0\n"
        "            mode = OFF\n"
        "            iconTexture = InfiniteDiscoveries/Textures/Misc/binaryStarIco.png\n"
        "        }\n"
        "    }\n"
        "}\n"
    )