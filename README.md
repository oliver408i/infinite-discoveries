# Infinite-Discoveries
Infinite Discoveries is a randomized star system generator for KSP, so you never run of stars and planets to explore.  
This is a fork of the [original script](https://github.com/Sushutt/Infinite-Discoveries) that improves on a number of things (see below).

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
- MagickWand (see below)
- Kopernicus (and deps)
- EVE & Scatterer (optional visuals)
- Parallax (optional ground scatters)
### Running
- Navigate to the `GenerateSystems` directory
- Do `pip install -r requirements.txt`. Use a venv if needed, and make sure you use the right pip
- Do `python GenerateSystems.py`
- Use the UI to set your settings and select your `GameData` directory
- Hit generate and wait for it to finish  
*Im working on packaging it so it's easier to run*
### After generation
- Check the `Configs` folder for any bad planet files (usually those with zero bytes or empty)
- If you find any, you can either delete them, or delete the whole `InfiniteDiscoveries` folder and regenerate
- Now you can boot up KSP and play

<details><summary>MagickWand Install</summary>
`libmagickwand-dev` for APT on Debian/Ubuntu,
`imagemagick` for MacPorts/Homebrew on Mac,
`ImageMagick-devel` for Yum on CentOS
</details>

## Improvements over the original
- Code up the damn code (it's a big mess, I'm still working on it)
- Full support for Mac and Linux (and Windows, of course)
- Custom tkinter instead of the now paid pysimplegui
- Fix several bugs in the original scripts (including solar panels not working)
- Removed random unused assets (like a video of a thumbs up emoji, for whatever reason)