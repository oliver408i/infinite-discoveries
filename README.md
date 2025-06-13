# Infinite-Discoveries
Infinite Discoveries is a randomized star system generator for KSP, so you never run of stars and planets to explore.  
This is a fork of the [original script](https://github.com/Sushutt/Infinite-Discoveries) that improves on a number of things (see below).

**Sample Planets**  
<img src="https://github.com/user-attachments/assets/e36f1e61-c25a-461a-adfb-31f2aa451931" width="400"/>
<img src="https://github.com/user-attachments/assets/d8fe08a3-3cb1-4600-a1b9-eff52378356d" width="300"/>
<img src="https://github.com/user-attachments/assets/f56d6b42-bf0e-4afc-8781-46870b1cdf46" width="250"/>


## Features
- **Procedural Star System Generation**  
  Automatically generates unique star systems with stars, planets, and moons for Kerbal Space Program.

- **Realistic Planetary Bodies**  
  Each body features diverse terrain such as mountains, oceans, canyons, and ice caps.

- **Multiple Star Types**  
  Supports various stellar classes:  
  Main Sequence, Red Giant, White Dwarf, Neutron Star, Brown Dwarf, and Wolf-Rayet.

- **Planetary Rings**  
  Some planets are adorned with procedurally generated ring systems.

- **Life Possibilities**  
  Worlds may support organic, exotic, aerial, or subglacial life, depending on atmospheric and surface conditions.

- **Atmospheric & Visual Effects**  
  Includes support for atmospheric scattering, volumetric clouds, auroras, and more—automatically configured per body.

- **Scientific Value System**  
  Bodies are assigned science values based on their physical and environmental attributes.

- **Color-Coded Diversity**  
  Stars and planets use a temperature-based color spectrum for realistic and aesthetic visuals.

- **Infinite Replayability**  
  Procedural generation ensures no two playthroughs are ever the same.

## HOW TO USE
### Requirements (install first)
- Python 3 (Tested on python3.13)
- MagickWand (follow [this](https://docs.wand-py.org/en/0.6.7/guide/install.html). Ignore the `pip install` command here)
- Kopernicus (and deps)
- EVE & Scatterer (optional visuals)
- Parallax (optional ground scatters)
- SigmaLoadingScreens (optional visuals)
### Running
- Download the latest `.whl` file from the releases page (right sidebar)
- Set up a venv if you need to (for install pip packages); activate it
- Run `pip install path/to/theFileYouJustDownloaded.whl` (you can drag the whl file into your terminal. You might use `pip3` or `py -m pip`)
- Run the command `infinite-discoveries` or `python -m infinite_discoveries`
- Wait a bit for the GUI to open
### After generation
- Check the `Configs` folder for any bad planet files (usually those with zero bytes or empty)
- If you find any, you can either delete them, or delete the whole `InfiniteDiscoveries` folder and regenerate
- (Optional) If you don't use Parallax or the other visual mods, you can remove their settings and assets from the `Visuals` folder to save space.
- Now you can boot up KSP and play

## Improvements over the original
- Code up the damn code (it's a big mess, I'm still working on it)
- Full support for Mac and Linux (and Windows, of course)
- Custom tkinter instead of the now paid pysimplegui (complete UI rewrite)
- Fix several bugs in the original scripts (including solar panels not working)
- Removed random unused assets (like a video of a thumbs up emoji, for whatever reason)
- Better name generation (to prevent duplicate names)

## Issues/problems to be worked on
- Duplicate names (not enought names, need better name gen)
- Continue to clean up the super dirty code

## Web-based star system viewer
See the `InfiniteViewer` directory. I will continue to work on this and fix this.  
A separate program that allows you to preview star systems and planets, without booting up KSP or installing anything extra.
Use it to preview your star systems. Just zip up the generated folder and upload it to https://nitrogendioxide.dev/infiniteviewer/  
You can ignore the planet called RedGiantThing, it won't show up in game