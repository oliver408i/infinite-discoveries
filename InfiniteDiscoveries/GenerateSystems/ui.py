import importlib
import Settings
import textwrap, os, threading, shutil, time, numpy as np
import customtkinter as ctk
import json
import tkinter.messagebox as mb
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")
CACHE_FILE = os.path.join(os.path.expanduser("~"), ".infinite_discoveries_cache.json")

def openSettings():
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("dark-blue")
    importlib.reload(Settings)

    with open("Settings.py", "r") as settingsFile:
        settingsData = settingsFile.readlines()

    usesMultithreading = Settings.useMultithreading
    convertsToDDS = Settings.convertTexturesToDDS
    fantasyNames = Settings.fantasyNames
    minPlanets = Settings.minPlanets
    minMoons = Settings.minMoons

    class SettingsWindow(ctk.CTk):
        def __init__(self):
            super().__init__()
            self.title("Settings")
            self.geometry("500x480")
            self.resizable(False, False)

            # Variables for checkboxes and entries
            self.use_multithread_var = ctk.BooleanVar(value=usesMultithreading)
            self.convert_dds_var = ctk.BooleanVar(value=convertsToDDS)
            self.fantasy_names_var = ctk.BooleanVar(value=fantasyNames)
            self.min_planets_var = ctk.StringVar(value=str(minPlanets))
            self.min_moons_var = ctk.StringVar(value=str(minMoons))

            # Main frame
            self.main_frame = ctk.CTkFrame(self)
            self.main_frame.pack(fill="both", expand=True, padx=20, pady=20)

            # Generator Settings Frame
            self.gen_settings_frame = ctk.CTkFrame(self.main_frame)
            self.gen_settings_frame.pack(fill="both", expand=True, padx=20, pady=(10, 10))

            # Multithreading
            self.use_threading_check = ctk.CTkCheckBox(
                master=self.gen_settings_frame,
                text="Use Multithreading",
                variable=self.use_multithread_var,
                onvalue=True, offvalue=False
            )
            self.use_threading_check.grid(row=0, column=0, sticky="w", padx=(10, 0), pady=(5, 2))
            self.use_threading_label = ctk.CTkLabel(
                master=self.gen_settings_frame,
                text=textwrap.fill("Multithreading drastically improves efficiency but might increase CPU usage.", 40),
                wraplength=320, justify="left", text_color="#ffffff"
            )
            self.use_threading_label.grid(row=1, column=0, sticky="w", padx=(10, 0))

            # DDS Conversion
            self.convert_dds_check = ctk.CTkCheckBox(
                master=self.gen_settings_frame,
                text="Convert Textures to DDS",
                variable=self.convert_dds_var,
                onvalue=True, offvalue=False
            )
            self.convert_dds_check.grid(row=2, column=0, sticky="w", padx=(10, 0), pady=(10, 2))
            self.convert_dds_label = ctk.CTkLabel(
                master=self.gen_settings_frame,
                text=textwrap.fill("Converting maps to DDS improves RAM usage ingame, but takes a bit longer and requires ImageMagick.", 40),
                wraplength=320, justify="left", text_color="#ffffff"
            )
            self.convert_dds_label.grid(row=3, column=0, sticky="w", padx=(10, 0))

            # Fantasy Names
            self.fantasy_names_check = ctk.CTkCheckBox(
                master=self.gen_settings_frame,
                text="Use Fantasy Names",
                variable=self.fantasy_names_var,
                onvalue=True, offvalue=False
            )
            self.fantasy_names_check.grid(row=4, column=0, sticky="w", padx=(10, 0), pady=(10, 2))
            self.fantasy_names_label = ctk.CTkLabel(
                master=self.gen_settings_frame,
                text=textwrap.fill("Fantasy names do not affect anything, but simply adds some more creative names to celestial bodies.", 40),
                wraplength=320, justify="left", text_color="#ffffff"
            )
            self.fantasy_names_label.grid(row=5, column=0, sticky="w", padx=(10, 0))

            # Min Planets/Moons
            self.min_planets_label = ctk.CTkLabel(master=self.gen_settings_frame, text="Minimum Planets", text_color="#ffffff")
            self.min_planets_label.grid(row=6, column=0, sticky="w", padx=(10, 0), pady=(10, 0))
            self.min_planets_entry = ctk.CTkEntry(master=self.gen_settings_frame, textvariable=self.min_planets_var, width=80, text_color="#ffffff", fg_color="transparent")
            self.min_planets_entry.grid(row=7, column=0, sticky="w", padx=(10, 0))

            self.min_moons_label = ctk.CTkLabel(master=self.gen_settings_frame, text="Minimum Moons", text_color="#ffffff")
            self.min_moons_label.grid(row=8, column=0, sticky="w", padx=(10, 0), pady=(10, 0))
            self.min_moons_entry = ctk.CTkEntry(master=self.gen_settings_frame, textvariable=self.min_moons_var, width=80, text_color="#ffffff", fg_color="transparent")
            self.min_moons_entry.grid(row=9, column=0, sticky="w", padx=(10, 0))

            # Removed UI Settings Frame (right column) and show console checkbox and label

            # Apply Button
            self.apply_button = ctk.CTkButton(master=self.main_frame, text="Apply", command=self.apply_settings, text_color="#ffffff")
            self.apply_button.pack(pady=(10, 10))

            # Validation: only allow integer in min_planets and min_moons
            self.min_planets_entry.bind("<KeyRelease>", self.validate_min_planets)
            self.min_moons_entry.bind("<KeyRelease>", self.validate_min_moons)

        def validate_min_planets(self, event=None):
            value = self.min_planets_var.get()
            if not value.isdigit():
                self.min_planets_var.set(value[:-1])

        def validate_min_moons(self, event=None):
            value = self.min_moons_var.get()
            if not value.isdigit():
                self.min_moons_var.set(value[:-1])

        def apply_settings(self):
            # Save settings to file
            settingsData[2] = "useMultithreading = " + str(self.use_multithread_var.get()) + " # Will use multithreading, this will drastically increase generator efficiency and thus result in faster generation, but may increase CPU usage." + "\n"
            settingsData[6] = "convertTexturesToDDS = " + str(self.convert_dds_var.get()) + " # Will remove the requirement for ImageMagick and reduce generator time if false. Will also increase KSP loading time so setting to false is not recommended." + "\n"
            settingsData[11] = "fantasyNames = " + str(self.fantasy_names_var.get()) + " # Generate a fantasy name for bodies. Will not affect internal names!" + "\n"
            try:
                minPlanets = int(self.min_planets_var.get())
            except ValueError:
                minPlanets = 0
            settingsData[8] = "minPlanets = " + str(minPlanets) + " # Minimum number of planets per star." + "\n"
            try:
                minMoons = int(self.min_moons_var.get())
            except ValueError:
                minMoons = 0
            settingsData[9] = "minMoons = " + str(minMoons) + " # Minimum number of moons per star." + "\n"
            with open("Settings.py", "w") as settingsFile:
                settingsFile.writelines(settingsData)
            print("Settings applied.")
            self.after(100, self.destroy)

    settingsWindow = SettingsWindow()
    settingsWindow.mainloop()

class DeleteWindow(ctk.CTk):
    def __init__(self, targetPath):
        super().__init__()
        self.title("Delete Systems")
        self.geometry("350x320")
        self.resizable(False, False)
        self.configure(bg="#1f2836")
        self.deleteStarAreYouSure = False
        self.deleteDirAreYouSure = False
        self.targetPath = targetPath

        explText = textwrap.fill(
            "The below input requires the star's internal name. You can find it by going ingame and looking at the description, where the name is formatted as 'AA-11111' WARNING: will delete EVERY config/texture containing what you inputted! Leave blank to delete everything.",
            width=40)

        # Layout
        self.main_frame = ctk.CTkFrame(self)
        self.main_frame.pack(fill="both", expand=True, padx=10, pady=10)

        self.explanation = ctk.CTkLabel(self.main_frame, text=explText, wraplength=320, justify="left", text_color="#ffffff")
        self.explanation.pack(pady=(0, 10))

        self.starDelInput = ctk.CTkEntry(self.main_frame, width=220, text_color="#ffffff", fg_color="transparent")
        self.starDelInput.pack(pady=(0, 5))

        self.starDelButton = ctk.CTkButton(self.main_frame, text="Delete", fg_color="#e65045", command=self.delete_star, text_color="#ffffff")
        self.starDelButton.pack(pady=(0, 10))

        self.deleteAllButton = ctk.CTkButton(self.main_frame, text="Remove Directory", fg_color="#e65045", command=self.delete_all, text_color="#ffffff")
        self.deleteAllButton.pack(pady=(10, 0))

        self.protocol("WM_DELETE_WINDOW", self.destroy)

        # Directories
        self.textureDir = os.path.join(targetPath, "InfiniteDiscoveries", "Textures", "PluginData")
        self.configDir = os.path.join(targetPath, "InfiniteDiscoveries", "Configs")
        self.cacheDir = os.path.join(targetPath, "InfiniteDiscoveries", "Cache")
        self.visual_ScattererDir = os.path.join(targetPath, "InfiniteDiscoveries", "Visuals", "Scatterer")
        self.visual_EveConfigDir = os.path.join(targetPath, "InfiniteDiscoveries", "Visuals", "Eve", "Configs")
        self.visual_ParallaxDir = os.path.join(targetPath, "InfiniteDiscoveries", "Visuals", "Parallax", "Configs")
        self.visual_CloudMapDir = os.path.join(targetPath, "InfiniteDiscoveries", "Textures", "Clouds")
        self.visual_NiftyNebulaeDir = os.path.join(targetPath, "InfiniteDiscoveries", "Visuals", "NiftyNebulae")
        self.misc_RRDir = os.path.join(targetPath, "InfiniteDiscoveries", "Misc", "RR")
        self.allDirs = [
            self.textureDir, self.configDir, self.cacheDir, self.visual_ScattererDir, self.visual_EveConfigDir,
            self.visual_ParallaxDir, self.visual_CloudMapDir, self.visual_NiftyNebulaeDir, self.misc_RRDir
        ]

    def reset_star_button(self):
        self.deleteStarAreYouSure = False
        self.starDelButton.configure(text="Delete")

    def reset_all_button(self):
        self.deleteDirAreYouSure = False
        self.deleteAllButton.configure(text="Remove Directory")

    def delete_star(self):
        if not self.deleteStarAreYouSure:
            self.deleteStarAreYouSure = True
            self.starDelButton.configure(text="Are You Sure? This CANNOT be undone!")
            self.after(2000, self.reset_star_button)
        else:
            targetStar = self.starDelInput.get()
            try:
                for currentDir in self.allDirs:
                    if not os.path.isdir(currentDir):
                        continue
                    for f in os.listdir(currentDir):
                        if targetStar in f:
                            os.remove(os.path.join(currentDir, f))
            except FileNotFoundError:
                self.starDelButton.configure(text="Directory doesn't exist!")
                self.after(2000, self.reset_star_button)

    def delete_all(self):
        if not self.deleteDirAreYouSure:
            self.deleteDirAreYouSure = True
            self.deleteAllButton.configure(text="Are You Sure? This CANNOT be undone!")
            self.after(2000, self.reset_all_button)
        else:
            try:
                shutil.rmtree(os.path.join(self.targetPath, "InfiniteDiscoveries"))
            except FileNotFoundError:
                self.deleteAllButton.configure(text="Directory doesn't exist!")
                self.after(2000, self.reset_all_button)

class HelpWindow(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Infinite Discoveries Help")
        self.geometry("400x200")
        self.resizable(False, False)
        self.label = ctk.CTkLabel(self, text="Help content goes here.", wraplength=380, justify="left", text_color="#ffffff")
        self.label.pack(expand=True, padx=20, pady=20)
        self.protocol("WM_DELETE_WINDOW", self.destroy)


class MainUI(ctk.CTk):
    def __init__(self, targetPath, base_dir, Settings, state, startLoop, allActions, allThreads, mainThreadFinished, amountOfThingsDone, amountOfThingsToDo):
        super().__init__()
        self.title("Infinite Discoveries 0.9.9")
        self.geometry("800x500")
        self.minsize(700, 500)
        self.configure(bg="#1f1f1f")
        self.amountValues = [1, 5, 4, 2]
        self.targetPath = targetPath
        self.base_dir = base_dir
        self.Settings = Settings
        self.app_state = state
        self.startLoop = startLoop
        self.allActions = allActions
        self.allThreads = allThreads
        self.mainThreadFinished = mainThreadFinished
        self.amountOfThingsDone = amountOfThingsDone
        self.amountOfThingsToDo = amountOfThingsToDo
        self.running = False
        self.overrideSeed = False
        self.overrideValues = False
        self.customSeed = None
        self.maxPlanetOvrd = None
        self.maxMoonOvrd = None
        self.maxAsteroidOvrd = None
        self.minPlanetOvrd = None
        self.minMoonOvrd = None
        self.lastMoment = 0
        self.actionText = ""

        def load_cache():
            if os.path.isfile(CACHE_FILE):
                try:
                    with open(CACHE_FILE, "r") as f:
                        return json.load(f)
                except:
                    return {}
            return {}

        cache = load_cache()

        # File log
        self.ActionLog = open(base_dir / "ActionLog.txt", "a")

        # Main frames
        self.input_frame = ctk.CTkFrame(self)
        self.input_frame.pack(side="left", fill="both", expand=True, padx=5, pady=5)
        self.output_frame = ctk.CTkFrame(self)
        self.output_frame.pack(side="right", fill="both", expand=True, padx=5, pady=5)

        # Title
        self.title_label = ctk.CTkLabel(self.input_frame, text="Infinite Discoveries", font=ctk.CTkFont(size=18, weight="bold"), text_color="#ffffff")
        self.title_label.pack(pady=(10, 5))

        # Amounts input
        self.star_var = ctk.StringVar(value=cache.get("stars", str(self.amountValues[0])))
        self.planet_var = ctk.StringVar(value=cache.get("planets", str(self.amountValues[1])))
        self.moon_var = ctk.StringVar(value=cache.get("moons", str(self.amountValues[2])))
        self.asteroid_var = ctk.StringVar(value=cache.get("asteroids", str(self.amountValues[3])))

        self.amounts_frame = ctk.CTkFrame(self.input_frame)
        self.amounts_frame.pack(fill="x", padx=10, pady=(0, 5))

        self.amount_star = ctk.CTkFrame(self.amounts_frame, fg_color="transparent")
        self.amount_star.pack(side="left", expand=True, padx=5)
        ctk.CTkLabel(self.amount_star, text="Star amount", text_color="#ffffff").pack()
        self.star_entry = ctk.CTkEntry(self.amount_star, textvariable=self.star_var, width=60, text_color="#ffffff", fg_color="transparent")
        self.star_entry.pack()

        self.amount_planet = ctk.CTkFrame(self.amounts_frame, fg_color="transparent")
        self.amount_planet.pack(side="left", expand=True, padx=5)
        ctk.CTkLabel(self.amount_planet, text="Max planets", text_color="#ffffff").pack()
        self.planet_entry = ctk.CTkEntry(self.amount_planet, textvariable=self.planet_var, width=60, text_color="#ffffff", fg_color="transparent")
        self.planet_entry.pack()

        self.amount_moon = ctk.CTkFrame(self.amounts_frame, fg_color="transparent")
        self.amount_moon.pack(side="left", expand=True, padx=5)
        ctk.CTkLabel(self.amount_moon, text="Max moons", text_color="#ffffff").pack()
        self.moon_entry = ctk.CTkEntry(self.amount_moon, textvariable=self.moon_var, width=60, text_color="#ffffff", fg_color="transparent")
        self.moon_entry.pack()

        self.amount_asteroid = ctk.CTkFrame(self.amounts_frame, fg_color="transparent")
        self.amount_asteroid.pack(side="left", expand=True, padx=5)
        ctk.CTkLabel(self.amount_asteroid, text="Max asteroids", text_color="#ffffff").pack()
        self.asteroid_entry = ctk.CTkEntry(self.amount_asteroid, textvariable=self.asteroid_var, width=60, text_color="#ffffff", fg_color="transparent")
        self.asteroid_entry.pack()

        startAmountDescText = "Recommended values are however many stars, 7 planets and 3 moons. Higher amounts will generate planets/moons further out and might start causing issues. Make sure to select the KSP GameData folder as the directory."
        self.amount_desc = ctk.CTkLabel(self.input_frame, text=textwrap.fill(startAmountDescText, 49), wraplength=350, justify="left", text_color="#ffffff")
        self.amount_desc.pack(fill="x", padx=10, pady=(20, 10))

        # Directory selection
        self.directory_var = ctk.StringVar(value=cache.get("path", targetPath))
        # Simulate user selection of cached directory
        self.targetPath = self.directory_var.get()
        self.directory_entry = ctk.CTkEntry(self.input_frame, textvariable=self.directory_var, width=250, text_color="#ffffff", fg_color="transparent")
        self.directory_entry.pack(padx=10, pady=(0, 5), side="left")
        # No direct folder browse in CTk, so use filedialog
        self.dir_button = ctk.CTkButton(self.input_frame, text="Set GameData folder...", command=self.browse_directory, text_color="#ffffff")
        self.dir_button.pack(padx=10, pady=(0, 5), side="left")

        # Access info
        self.okToAccess = ctk.CTkLabel(self.input_frame, text="To write or not to write? That is the question.", text_color="#ffffff")
        self.okToAccess.pack(fill="x", padx=10, pady=(0, 5))

        # Estimated time
        self.est_time_text = ctk.CTkLabel(self.input_frame, text="Estimated Generator Time: 26.25 minutes.", text_color="#ffffff")
        self.est_time_text.pack(fill="x", padx=10, pady=(0, 5))

        # Start button
        self.start_button = ctk.CTkButton(self.input_frame, text="Start Generator", command=self.start_generator, text_color="#ffffff")
        self.start_button.pack(fill="x", padx=10, pady=(0, 5))

        # Stats frame
        self.stats_frame = ctk.CTkFrame(self.input_frame)
        self.stats_frame.pack(fill="x", padx=10, pady=(0, 5))
        self.stats_system_amount = ctk.CTkLabel(self.stats_frame, text="Amount of systems: ????", text_color="#ffffff")
        self.stats_system_amount.pack(fill="x")
        self.stats_config_amount = ctk.CTkLabel(self.stats_frame, text="Amount of configs: ????", text_color="#ffffff")
        self.stats_config_amount.pack(fill="x")
        self.stats_texture_amount = ctk.CTkLabel(self.stats_frame, text="Amount of textures: ????", text_color="#ffffff")
        self.stats_texture_amount.pack(fill="x")

        # Seed input
        self.seed_var = ctk.StringVar(value=cache.get("seed", ""))
        self.seed_frame = ctk.CTkFrame(self.input_frame)
        self.seed_frame.pack(fill="x", padx=10, pady=(0, 5))
        self.seed_entry = ctk.CTkEntry(self.seed_frame, textvariable=self.seed_var, width=120, text_color="#ffffff", fg_color="transparent")
        self.seed_entry.pack(side="left", padx=5)
        self.seed_label = ctk.CTkLabel(self.seed_frame, text="Custom Seed", text_color="#ffffff")
        self.seed_label.pack(side="left", padx=5)
        self.seed_entry.bind("<KeyRelease>", self.handle_seed_input)

        # Settings, Delete, Help buttons
        self.buttons_frame = ctk.CTkFrame(self.input_frame)
        self.buttons_frame.pack(fill="x", padx=10, pady=(0, 20))
        self.settings_button = ctk.CTkButton(self.buttons_frame, text="Settings", command=openSettings, text_color="#ffffff")
        self.settings_button.pack(side="left", padx=10)
        self.delete_button = ctk.CTkButton(self.buttons_frame, text="Delete", command=lambda: DeleteWindow(self.targetPath).mainloop(), text_color="#ffffff")
        self.delete_button.pack(side="left", padx=10)
        self.help_button = ctk.CTkButton(self.buttons_frame, text="Help", command=lambda: HelpWindow().mainloop(), text_color="#ffffff")
        self.help_button.pack(side="left", padx=10)

        # Output frame
        self.currentFocusText = ctk.CTkLabel(self.output_frame, text="Generator is not currently running.", text_color="#ffffff")
        self.currentFocusText.pack(fill="x", pady=(10, 2))
        self.currentActionText = ctk.CTkTextbox(self.output_frame, fg_color="#2a2a2a", text_color="#ffffff", height=320)
        self.currentActionText.pack(fill="both", expand=True, padx=10, pady=5)

        # Bindings for input validation
        self.star_entry.bind("<KeyRelease>", self.validate_star)
        self.planet_entry.bind("<KeyRelease>", self.validate_planet)
        self.moon_entry.bind("<KeyRelease>", self.validate_moon)
        self.asteroid_entry.bind("<KeyRelease>", self.validate_asteroid)

        self.protocol("WM_DELETE_WINDOW", self.on_close)

        # Start update loop
        self.after(100, self.update_stats_loop)

    def browse_directory(self):
        import tkinter.filedialog as fd
        folder = fd.askdirectory(initialdir=self.targetPath)
        if folder:
            self.directory_var.set(folder)
            self.targetPath = folder

    def validate_star(self, event=None):
        val = self.star_var.get()
        if not val.isdigit():
            self.star_var.set(val[:-1])

    def validate_planet(self, event=None):
        val = self.planet_var.get()
        if not val.isdigit():
            self.planet_var.set(val[:-1])
        elif int(val) > 25:
            self.planet_var.set("25")

    def validate_moon(self, event=None):
        val = self.moon_var.get()
        if not val.isdigit():
            self.moon_var.set(val[:-1])

    def validate_asteroid(self, event=None):
        val = self.asteroid_var.get()
        if not val.isdigit():
            self.asteroid_var.set(val[:-1])

    def handle_seed_input(self, event=None):
        customSeedInput = self.seed_var.get()
        seperatedValues = customSeedInput.split(".")
        self.overrideSeed = False
        self.overrideValues = False
        if customSeedInput != "":
            if len(seperatedValues) > 1:
                if len(seperatedValues[1]) >= 9 and len(seperatedValues[1]) <= 14:
                    try:
                        self.customSeed = int(seperatedValues[0])
                        fullySeperatedValues = seperatedValues[1].split(":")
                        self.maxPlanetOvrd = int(fullySeperatedValues[0])
                        self.maxMoonOvrd = int(fullySeperatedValues[1])
                        self.maxAsteroidOvrd = int(fullySeperatedValues[2])
                        self.minPlanetOvrd = int(fullySeperatedValues[3])
                        self.minMoonOvrd = int(fullySeperatedValues[4])
                        if 0 <= self.customSeed < (2**32):
                            self.setStarAmntToOverriden()
                            self.setOtherAmntToOverriden()
                            self.overrideSeed = True
                            self.overrideValues = True
                        else:
                            self.setStarAmntToDefault()
                            self.setOtherAmntToDefault()
                    except:
                        self.setStarAmntToDefault()
                        self.setOtherAmntToDefault()
                else:
                    try:
                        self.customSeed = int(seperatedValues[0])
                        if 0 <= self.customSeed < (2**32):
                            self.setStarAmntToOverriden()
                            self.setOtherAmntToDefault()
                            self.overrideSeed = True
                            self.overrideValues = False
                        else:
                            self.setStarAmntToDefault()
                            self.setOtherAmntToDefault()
                    except:
                        self.setStarAmntToDefault()
                        self.setOtherAmntToDefault()
            else:
                try:
                    self.customSeed = int(seperatedValues[0])
                    if 0 <= self.customSeed < (2**32):
                        self.setStarAmntToOverriden()
                        self.setOtherAmntToDefault()
                        self.overrideSeed = True
                        self.overrideValues = False
                    else:
                        self.setStarAmntToDefault()
                        self.setOtherAmntToDefault()
                except:
                    self.setStarAmntToDefault()
                    self.setOtherAmntToDefault()
        else:
            self.setStarAmntToDefault()
            self.setOtherAmntToDefault()

    def setStarAmntToOverriden(self):
        self.star_entry.configure(state="disabled")
        self.star_var.set("SEED SET")

    def setStarAmntToDefault(self):
        self.star_entry.configure(state="normal")
        self.star_var.set(str(self.amountValues[0]))

    def setOtherAmntToOverriden(self):
        self.planet_entry.configure(state="disabled")
        self.planet_var.set("SEED SET")
        self.moon_entry.configure(state="disabled")
        self.moon_var.set("SEED SET")
        self.asteroid_entry.configure(state="disabled")
        self.asteroid_var.set("SEED SET")

    def setOtherAmntToDefault(self):
        self.planet_entry.configure(state="normal")
        self.planet_var.set(str(self.amountValues[1]))
        self.moon_entry.configure(state="normal")
        self.moon_var.set(str(self.amountValues[2]))
        self.asteroid_entry.configure(state="normal")
        self.asteroid_var.set(str(self.amountValues[3]))

    def start_generator(self):
        try:
            starAmount = int(self.star_var.get())
            planetAmount = int(self.planet_var.get())
            moonAmount = int(self.moon_var.get())
            asteroidAmount = int(self.asteroid_var.get())
        except:
            return
        self.currentFocusText.configure(text="Generator is active.")
        # Only disable button, do not set text here (let update_stats_loop manage text)
        self.start_button.configure(state="disabled")
        self.start_button.update()
        self.running = True
        # Set latest action text before starting
        if self.allActions:
            latest = self.allActions[-1]
            self.actionText = f"{latest[0].tm_hour:02}:{latest[0].tm_min:02}:{latest[0].tm_sec:02} - {latest[1]}"
        if self.seed_var.get() != "":
            if self.overrideSeed and not self.overrideValues:
                self.startLoop(starAmount, planetAmount, moonAmount, asteroidAmount, self.targetPath, self.customSeed)
            elif self.overrideSeed and self.overrideValues:
                self.startLoop(starAmount, planetAmount, moonAmount, asteroidAmount, self.targetPath, self.customSeed,
                    [self.maxPlanetOvrd, self.maxMoonOvrd, self.maxAsteroidOvrd, self.minPlanetOvrd, self.minMoonOvrd])
            else:
                self.startLoop(starAmount, planetAmount, moonAmount, asteroidAmount, self.targetPath)
            self.mainThreadFinished = False
        else:
            self.startLoop(starAmount, planetAmount, moonAmount, asteroidAmount, self.targetPath)
            self.mainThreadFinished = False

    def update_stats_loop(self):
        # Update stats, estimated time, etc.
        try:
            starAmount = int(self.star_var.get())
        except:
            starAmount = 0
        try:
            planetAmount = int(self.planet_var.get())
        except:
            planetAmount = 0
        try:
            moonAmount = int(self.moon_var.get())
        except:
            moonAmount = 0
        try:
            asteroidAmount = int(self.asteroid_var.get())
        except:
            asteroidAmount = 0

        # Estimated time
        if self.Settings.useMultithreading:
            estTime = (((planetAmount * moonAmount * asteroidAmount) * starAmount) * 15) / 6.17
        else:
            estTime = ((planetAmount * moonAmount * asteroidAmount) * starAmount) * 15
        if estTime >= 60:
            if estTime >= 3600:
                if estTime >= 86400:
                    if estTime >= 604800:
                        if estTime >= 2.628e+6:
                            if estTime >= 3.154e+7:
                                self.est_time_text.configure(text=f"Estimated Generator Time: {round((estTime/3.154e+7),2)} years.")
                            else:
                                self.est_time_text.configure(text=f"Estimated Generator Time: {round((estTime/2.628e+6),2)} months.")
                        else:
                            self.est_time_text.configure(text=f"Estimated Generator Time: {round((estTime/604800),2)} weeks.")
                    else:
                        self.est_time_text.configure(text=f"Estimated Generator Time: {round((estTime/86400),2)} days.")
                else:
                    self.est_time_text.configure(text=f"Estimated Generator Time: {round((estTime/3600),2)} hours.")
            else:
                self.est_time_text.configure(text=f"Estimated Generator Time: {round((estTime/60),2)} minutes.")
        else:
            self.est_time_text.configure(text=f"Estimated Generator Time: {round(estTime,2)} seconds.")

        # Stats
        try:
            allKopConfigs = os.listdir(os.path.join(self.targetPath, "InfiniteDiscoveries", "Configs"))
            allEVEConfigs = os.listdir(os.path.join(self.targetPath, "InfiniteDiscoveries", "Visuals", "EVE", "Configs"))
            allParallaxConfigs = os.listdir(os.path.join(self.targetPath, "InfiniteDiscoveries", "Visuals", "Parallax", "Configs"))
            allTextures = os.listdir(os.path.join(self.targetPath, "InfiniteDiscoveries", "Textures", "PluginData"))
            allCloudTextures = os.listdir(os.path.join(self.targetPath, "InfiniteDiscoveries", "Textures", "Clouds"))
            allALLTextures = allTextures + allCloudTextures
            allScattererConfigs = os.listdir(os.path.join(self.targetPath, "InfiniteDiscoveries", "Visuals", "Scatterer"))
            allRRConfigs = os.listdir(os.path.join(self.targetPath, "InfiniteDiscoveries", "Misc", "RR"))
            allSystems = []
            for scattererCfg in allScattererConfigs:
                if "ScattererSunflare" in scattererCfg:
                    systemName = scattererCfg.replace("ScattererSunflare", "").replace("_", "").replace(".cfg", "").replace("1", "").replace("2", "").replace("-", "")
                    allSystems.append(systemName)
            allSystemsREAL = np.unique(allSystems)
            allConfigs = allKopConfigs + allEVEConfigs + allParallaxConfigs + allScattererConfigs + allRRConfigs
            self.stats_system_amount.configure(text=f"Amount of systems: {len(allSystemsREAL)}")
            self.stats_config_amount.configure(text=f"Amount of configs: {len(allConfigs)}")
            self.stats_texture_amount.configure(text=f"Amount of textures: {len(allALLTextures)}")
        except Exception as e:
            #print("Error while getting settings for directory",e,"\nPaths:",self.targetPath)
            self.stats_system_amount.configure(text="Amount of systems: No directory!")
            self.stats_config_amount.configure(text="Amount of configs: No directory!")
            self.stats_texture_amount.configure(text="Amount of textures: No directory!")

        # Directory access
        if os.access(self.targetPath, os.W_OK):
            self.okToAccess.configure(text="Selected directory can be written to.", text_color="#8fff8f")
        else:
            self.okToAccess.configure(text="Cannot write to selected directory!", text_color="#ff8f8f")

        
        # Update start button text to latest action if changed
        if self.allActions:
            latest_action = self.allActions[-1]
            formatted_action = latest_action[1]
            if self.actionText != formatted_action:
                self.actionText = formatted_action
                self.start_button.configure(text=self.actionText)

        if self.allActions and 'Finished generation' in formatted_action:
            self.start_button.configure(text="Start Generator", state="normal")
            self.running = False
            mb.showinfo("Generation Complete", "The generator has finished running.")
            self.allActions.clear()
        
        
        # Re-schedule
        self.after(100, self.update_stats_loop)

    def on_close(self):
        # Save cache on close
        cache_data = {
            "stars": self.star_var.get(),
            "planets": self.planet_var.get(),
            "moons": self.moon_var.get(),
            "asteroids": self.asteroid_var.get(),
            "seed": self.seed_var.get(),
            "path": self.directory_var.get()
        }
        try:
            with open(CACHE_FILE, "w") as f:
                json.dump(cache_data, f)
        except Exception as e:
            print("Failed to write cache:", e)
        # Properly close log file and exit
        self.ActionLog.close()
        self.destroy()