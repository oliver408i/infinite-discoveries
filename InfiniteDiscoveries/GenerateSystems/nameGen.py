SYLLABLE_SETS = {
    "star": {
        "prefixes": ["Xe", "Ka", "Ael", "Sol", "Zy", "Ast", "Or", "Alt", "Pol", "Ser"],
        "middles": ["dra", "mir", "ven", "lux", "quas", "ion", "zer", "eth", "theo", "spir"],
        "suffixes": ["os", "ar", "ion", "eus", "or", "ix", "el", "en", "arx", "orix"]
    },
    "vacuum": {
        "prefixes": ["Ter", "No", "Bas", "Vac", "Lun", "Sil", "Nul", "Um", "Erg"],
        "middles": ["ron", "crat", "form", "tect", "dran", "void", "grav", "null", "clus"],
        "suffixes": ["on", "ar", "um", "ex", "an", "or", "us", "in", "yx", "arx"]
    },
    "oceanic": {
        "prefixes": ["Aqua", "Hydr", "Mar", "Nept", "Cor", "Pel", "Del", "Sur", "Thal"],
        "middles": ["al", "ith", "una", "ser", "ae", "ora", "thal", "und", "benth"],
        "suffixes": ["on", "ia", "us", "ae", "is", "or", "isle", "in", "mar", "en"]
    },
    "gaseous": {
        "prefixes": ["Atm", "Vap", "Strat", "Cumu", "Neb", "Gas", "Aero", "Clou", "Mist"],
        "middles": ["eth", "oz", "meth", "heli", "nit", "trop", "fog", "vap", "haze"],
        "suffixes": ["os", "ion", "ar", "us", "ix", "en", "ox", "an", "or", "ume"]
    },
    "life": {
        "prefixes": ["Bio", "Eco", "Gen", "Viv", "Sym", "Phy", "Neo", "Zo", "Thri"],
        "middles": ["syn", "eth", "flora", "phy", "vita", "gene", "ess", "trop", "nour"],
        "suffixes": ["ia", "os", "on", "is", "um", "or", "ix", "ae", "ine", "el"]
    },
    "rocky": {
        "prefixes": ["Roc", "Vol", "Bas", "Strat", "Mon", "Gran", "Ter", "Pet", "Lith"],
        "middles": ["gran", "obs", "dur", "tect", "sil", "mol", "strat", "crust", "igne"],
        "suffixes": ["ar", "os", "ek", "um", "an", "or", "en", "el", "ine", "ex"]
    },
    "lava": {
        "prefixes": ["Mag", "Ig", "Lava", "Pyr", "Scor", "Ash", "Cind", "Volc", "Fum"],
        "middles": ["mol", "visc", "flow", "vent", "cald", "scor", "eject", "igne", "torr"],
        "suffixes": ["os", "ar", "um", "ix", "ae", "en", "is", "or", "ul", "oth"]
    },
    "icy": {
        "prefixes": ["Cryo", "Glac", "Fro", "Sub", "Hail", "Snow", "Gel", "Win", "Brim"],
        "middles": ["zen", "glim", "froz", "snow", "crys", "ice", "hoar", "shiv", "frim"],
        "suffixes": ["is", "ar", "um", "en", "ix", "el", "or", "an", "ice", "id"]
    }
}
import random

def getTables():
    return ["star", "vacuum", "oceanic", "gaseous", "life", "rocky", "lava", "icy"]

# Syllable-based name generator for planet types
def generate_syllable_name_for_type(planet_type, seed=None, syllables=3):
    rng = random.Random(seed)
    if planet_type not in SYLLABLE_SETS:
        planet_type = "star"  # fallback
    parts = SYLLABLE_SETS[planet_type]
    name_parts = [rng.choice(parts["prefixes"])]
    if syllables >= 3:
        name_parts.append(rng.choice(parts["middles"]))
    name_parts.append(rng.choice(parts["suffixes"]))
    return "".join(name_parts)

# Process a name (generates a name based on seed and category)
def processName(seed, category): # Length is ignored for now
    return generate_syllable_name_for_type(category) # Not using seed to encourage different names

# Use this function in place of processName() if you want syllable-based names
def generateNameByCategory(category, seed, syllables=3):
    return generate_syllable_name_for_type(category, seed, syllables)