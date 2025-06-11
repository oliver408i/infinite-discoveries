import random

def build_transition_table(tokens):
        transition_table = {}
        for i in range(len(tokens) - 1):
            current_char = tokens[i]
            next_char = tokens[i + 1]
            if current_char not in transition_table:
                transition_table[current_char] = []
            transition_table[current_char].append(next_char)
        return transition_table

starNameCorpus = "Sun Galaxy Nebula Constellation Supernova Comet Meteor Astronomy Celestial Stellar Twinkle Cosmic Interstellar Astronomer Black Gravity Solar Space Meteorite Nebular Satellite Planetarium Radiant Hubble Luminous"
starNameTokens = list(starNameCorpus)
starTransisionTable = build_transition_table(starNameTokens)

vacuumNameCorpus = "Earth Mercury Venus Mars Terrestrial Rocky Crust Mantle Core Atmosphere Geology Tectonics Volcanism Erosion Plateaus Mountains Canyons Valleys Deserts Plains"
vacuumNameTokens = list(vacuumNameCorpus)
vacuumTransisionTable = build_transition_table(vacuumNameTokens)

oceanicNameCorpus = "Abyssal Tidal Submersible Aquatic Hydrothermal Coral Mariner Nautical Seafloor Plankton Tsunami Neptune Voyager Liquid Maritime Seafaring Atlantis Marine Abyss Voyager"
oceanicNameTokens = list(oceanicNameCorpus)
oceanicTransisionTable = build_transition_table(oceanicNameTokens)

gaseousNameCorpus = "Cumulus Stratosphere Vapor Cirrus Nebula Condensation Haze Atmosphere Evaporation Methane Ozone Aerosol Fog Ammonia Carbon Dioxide Nitrogen Helium Vaporization Fogbank"
gaseousNameTokens = list(gaseousNameCorpus)
gaseousTransisionTable = build_transition_table(gaseousNameTokens)

lifeNameCorpus = "Organism Evolution Biology Planet Respiration Reproduction Diversity Ecosystem Genetics Metabolism Microbes Adaptation Ecology Species Sustainability Biotechnology Biodiversity Survival Physiology Genetics"
lifeNameTokens = list(lifeNameCorpus)
lifeTransisionTable = build_transition_table(lifeNameTokens)

rockyNameCorpus = "Barren Desolate Airless Vacant Lifeless Sterile Vacuum Harsh Inhospitable Rocky Surface Barren Wasteland No Atmosphere Rugged Desolation Uninhabitable"
rockyNameTokens = list(rockyNameCorpus)
rockyTransisionTable = build_transition_table(rockyNameTokens)

lavaNameCorpus = "Magma Molten Flowing Volcanic Eruption Lava Lake Pyroclastic Viscosity Hot Molten Rock Igneous Crater Obsidian Glowing Vents Geological Ejecta Eruption Incandescent Lava Tube Pahoehoe Scoria"
lavaNameTokens = list(lavaNameCorpus)
lavaTransisionTable = build_transition_table(lavaNameTokens)

icyNameCorpus = "Cryosphere Glacial Permafrost Frozen Tundra Ice Cap Frigid Glaciology Polar Icicle Frosty Snowy Frozen Wasteland Cryovolcano Hailstorm Blizzard Hibernation Subzero Crystalline Icy Surface Icebergs"
icyNameTokens = list(icyNameCorpus)
icyTransisionTable = build_transition_table(icyNameTokens)

def getTables():
    return starTransisionTable,vacuumTransisionTable,oceanicTransisionTable,gaseousTransisionTable,lifeTransisionTable,rockyTransisionTable,lavaTransisionTable,icyTransisionTable

# Step 4: Generate words
def generateName2(transition_table, word_length, seed):
    nameRNG = random.Random()
    nameRNG.seed(seed)
    current_char = ' '  # Start with a space character
    word = ""
    for _ in range(word_length):
        if current_char in transition_table:
            next_char = nameRNG.choice(transition_table[current_char])
            word += next_char
            current_char = next_char
        else:
            break
    return word

# Process a name
def processName(seed,tTable,length):
    generated_word = generateName2(tTable, length, seed)
    generatedWords = generated_word.split(" ")
    max_len = -1
    for ele in generatedWords:
        if len(ele) > max_len:
            max_len = len(ele)
            res = ele
    finalword = res
    return finalword