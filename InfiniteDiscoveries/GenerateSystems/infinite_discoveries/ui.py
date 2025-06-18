import importlib
from . import Settings, state
import textwrap, os, shutil, numpy as np
import customtkinter as ctk
import json
import tkinter as tk
import tkinter.messagebox as mb
from pathlib import Path

from ._version import __version__

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

WORK_DIR = Path().home() / '.infinite_discoveries'
WORK_DIR.mkdir(exist_ok=True)

ASSETS_DIR = WORK_DIR / 'assets'
ASSETS_DIR.mkdir(exist_ok=True)

state.base_dir = ASSETS_DIR

CACHE_FILE = WORK_DIR / 'cache.json'

CONFIG_PATH = WORK_DIR / "settings.json"


def load_user_settings():
    if CONFIG_PATH.exists():
        with open(CONFIG_PATH, "r") as f:
            saved = json.load(f)
    else:
        saved = {}

    for key in dir(Settings):
        if key.startswith("__"):
            continue
        if key not in saved:
            saved[key] = getattr(Settings, key)
    return saved

def save_user_settings(settings_dict):
    CONFIG_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(CONFIG_PATH, "w") as f:
        json.dump(settings_dict, f, indent=4)

def openSettings():
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("dark-blue")
    importlib.reload(Settings)

    settingsData = load_user_settings()

    usesMultithreading = settingsData.get("useMultithreading", Settings.useMultithreading)
    convertsToDDS = settingsData.get("convertTexturesToDDS", Settings.convertTexturesToDDS)
    fantasyNames = settingsData.get("fantasyNames", Settings.fantasyNames)
    minPlanets = settingsData.get("minPlanets", Settings.minPlanets)
    minMoons = settingsData.get("minMoons", Settings.minMoons)

    # New settings for binary and star overrides
    binaryOverride = settingsData.get("binaryOverride", getattr(Settings, "binaryOverride", Settings.binaryOverride))
    binaryTypeOverride = settingsData.get("binaryTypeOverride", getattr(Settings, "binaryTypeOverride", Settings.binaryTypeOverride))
    starTypeOverride = settingsData.get("starTypeOverride", getattr(Settings, "starTypeOverride", Settings.starTypeOverride))
    starTypeOverrideBinary1 = settingsData.get("starTypeOverrideBinary1", getattr(Settings, "starTypeOverrideBinary1", Settings.starTypeOverrideBinary1))
    starTypeOverrideBinary2 = settingsData.get("starTypeOverrideBinary2", getattr(Settings, "starTypeOverrideBinary2", Settings.starTypeOverrideBinary2))
    binaryBrightnessMultiplier = settingsData.get("binaryBrightnessMultiplier", getattr(Settings, "binaryBrightnessMultiplier", Settings.binaryBrightnessMultiplier))

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
            # New variables for binary/star overrides
            self.binary_override_var = ctk.StringVar(value="Default (random)" if binaryOverride is None else str(binaryOverride))
            self.binary_type_override_var = ctk.StringVar(value="Default (random)" if binaryTypeOverride is None else str(binaryTypeOverride))
            star_type_options = [
                "Default (random)",
                "Red Giant (0–18)",
                "White Dwarf (19–28)",
                "Neutron Star (29–39)",
                "Brown Dwarf (40–50)",
                "Wolf-Rayet (51–55)",
                "Main Sequence (56–175)"
            ]
            # Map numeric to label for initial value
            def get_star_type_label(val):
                mapping = {
                    None: "Default (random)",
                    "None": "Default (random)",
                    0: "Red Giant (0–18)",
                    "0": "Red Giant (0–18)",
                    19: "White Dwarf (19–28)",
                    "19": "White Dwarf (19–28)",
                    29: "Neutron Star (29–39)",
                    "29": "Neutron Star (29–39)",
                    40: "Brown Dwarf (40–50)",
                    "40": "Brown Dwarf (40–50)",
                    51: "Wolf-Rayet (51–55)",
                    "51": "Wolf-Rayet (51–55)",
                    56: "Main Sequence (56–175)",
                    "56": "Main Sequence (56–175)"
                }
                return mapping.get(val, "Default (random)")

            self.star_type_override_var = ctk.StringVar(
                value=get_star_type_label(starTypeOverride)
            )
            self.star_type_override_b1_var = ctk.StringVar(
                value=get_star_type_label(starTypeOverrideBinary1)
            )
            self.star_type_override_b2_var = ctk.StringVar(
                value=get_star_type_label(starTypeOverrideBinary2)
            )
            self.binary_brightness_multiplier_var = ctk.StringVar(
                value=binaryBrightnessMultiplier
            )

            # Main frame
            self.main_frame = ctk.CTkFrame(self)
            self.main_frame.pack(fill="both", expand=True, padx=20, pady=20)

            # Scrollable canvas frame
            self.scroll_frame = ctk.CTkFrame(self.main_frame)
            self.scroll_frame.pack(fill="both", expand=True, padx=20, pady=(10, 0))

            self.canvas = tk.Canvas(self.scroll_frame, bg="#2b2b2b", highlightthickness=0, borderwidth=0)
            self.scrollbar = ctk.CTkScrollbar(self.scroll_frame, orientation="vertical", command=self.canvas.yview)
            self.scrollable_frame = ctk.CTkFrame(self.canvas)

            self.scrollable_frame.bind(
                "<Configure>",
                lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
            )
            self.canvas_window = self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
            self.canvas.configure(yscrollcommand=self.scrollbar.set)

            self.canvas.pack(side="left", fill="both", expand=True)
            self.scrollbar.pack(side="right", fill="y")

            # Platform-aware mousewheel binding for scroll reliability (macOS/Linux/Windows)
            def _on_mousewheel(event):
                # macOS/Linux trackpad and wheel compatibility
                if hasattr(event, "num") and (event.num == 4 or event.delta > 0):
                    self.canvas.yview_scroll(-1, "units")
                elif hasattr(event, "num") and (event.num == 5 or event.delta < 0):
                    self.canvas.yview_scroll(1, "units")
                elif hasattr(event, "delta"):
                    if event.delta > 0:
                        self.canvas.yview_scroll(-1, "units")
                    elif event.delta < 0:
                        self.canvas.yview_scroll(1, "units")

            self.canvas.bind_all("<MouseWheel>", _on_mousewheel)  # Windows and macOS standard
            self.canvas.bind_all("<Button-4>", _on_mousewheel)    # Linux/mac trackpad scroll up
            self.canvas.bind_all("<Button-5>", _on_mousewheel)    # Linux/mac trackpad scroll down

            # Make scrollable frame width track canvas width
            self.canvas.bind("<Configure>", lambda e: self.canvas.itemconfig(self.canvas_window, width=e.width))

            self.gen_settings_frame = self.scrollable_frame  # Redirect UI creation to scrollable frame

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

            # --- New UI Elements for binary/star overrides ---
            self.binary_override_label = ctk.CTkLabel(master=self.gen_settings_frame, text="Binary Override", text_color="#ffffff")
            self.binary_override_label.grid(row=10, column=0, sticky="w", padx=(10, 0), pady=(10, 0))
            self.binary_override_dropdown = ctk.CTkOptionMenu(
                master=self.gen_settings_frame,
                values=["Default (random)", "True", "False"],
                variable=self.binary_override_var
            )
            self.binary_override_dropdown.grid(row=11, column=0, sticky="w", padx=(10, 0))

            self.binary_type_override_label = ctk.CTkLabel(master=self.gen_settings_frame, text="Binary Type Override", text_color="#ffffff")
            self.binary_type_override_label.grid(row=12, column=0, sticky="w", padx=(10, 0), pady=(10, 0))
            self.binary_type_override_dropdown = ctk.CTkOptionMenu(
                master=self.gen_settings_frame,
                values=["Default (random)", "True", "False"],
                variable=self.binary_type_override_var
            )
            self.binary_type_override_dropdown.grid(row=13, column=0, sticky="w", padx=(10, 0))

            self.star_type_override_label = ctk.CTkLabel(master=self.gen_settings_frame, text="Star Type Override", text_color="#ffffff")
            self.star_type_override_label.grid(row=14, column=0, sticky="w", padx=(10, 0), pady=(10, 0))
            self.star_type_override_dropdown = ctk.CTkOptionMenu(
                master=self.gen_settings_frame,
                values=star_type_options,
                variable=self.star_type_override_var
            )
            self.star_type_override_dropdown.grid(row=15, column=0, sticky="w", padx=(10, 0))

            self.star_type_override_b1_label = ctk.CTkLabel(master=self.gen_settings_frame, text="Binary Star 1 Type Override", text_color="#ffffff")
            self.star_type_override_b1_label.grid(row=16, column=0, sticky="w", padx=(10, 0), pady=(10, 0))
            self.star_type_override_b1_entry = ctk.CTkOptionMenu(
                master=self.gen_settings_frame,
                values=star_type_options,
                variable=self.star_type_override_b1_var
            )
            self.star_type_override_b1_entry.grid(row=17, column=0, sticky="w", padx=(10, 0))

            self.star_type_override_b2_label = ctk.CTkLabel(master=self.gen_settings_frame, text="Binary Star 2 Type Override", text_color="#ffffff")
            self.star_type_override_b2_label.grid(row=18, column=0, sticky="w", padx=(10, 0), pady=(10, 0))
            self.star_type_override_b2_entry = ctk.CTkOptionMenu(
                master=self.gen_settings_frame,
                values=star_type_options,
                variable=self.star_type_override_b2_var
            )
            self.star_type_override_b2_entry.grid(row=19, column=0, sticky="w", padx=(10, 0))

            self.binary_brightness_multiplier_label = ctk.CTkLabel(master=self.gen_settings_frame, text="Binary Brightness Multiplier", text_color="#ffffff")
            self.binary_brightness_multiplier_label.grid(row=20, column=0, sticky="w", padx=(10, 0), pady=(10, 0))
            self.binary_brightness_multiplier_entry = ctk.CTkEntry(master=self.gen_settings_frame, textvariable=self.binary_brightness_multiplier_var, width=120, text_color="#ffffff", fg_color="transparent")
            self.binary_brightness_multiplier_entry.grid(row=21, column=0, sticky="w", padx=(10, 0))

            # Apply Button
            self.apply_button = ctk.CTkButton(master=self, text="Apply", command=self.apply_settings, text_color="#ffffff")
            self.apply_button.pack(side="bottom", pady=(10, 10))

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
            def get_star_type_value(selection):
                mapping = {
                    "Red Giant (0–18)": 0,
                    "White Dwarf (19–28)": 19,
                    "Neutron Star (29–39)": 29,
                    "Brown Dwarf (40–50)": 40,
                    "Wolf-Rayet (51–55)": 51,
                    "Main Sequence (56–175)": 56
                }
                return mapping.get(selection, None)

            try:
                minPlanets = int(self.min_planets_var.get())
            except ValueError:
                minPlanets = Settings.minPlanets
            try:
                minMoons = int(self.min_moons_var.get())
            except ValueError:
                minMoons = Settings.minMoons

            new_settings = {
                "useMultithreading": self.use_multithread_var.get(),
                "convertTexturesToDDS": self.convert_dds_var.get(),
                "fantasyNames": self.fantasy_names_var.get(),
                "minPlanets": minPlanets,
                "minMoons": minMoons,
                "binaryOverride": None if self.binary_override_var.get() == "Default (random)" else self.binary_override_var.get(),
                "binaryTypeOverride": None if self.binary_type_override_var.get() == "Default (random)" else self.binary_type_override_var.get(),
                "starTypeOverride": None if self.star_type_override_var.get() == "Default (random)" else get_star_type_value(self.star_type_override_var.get()),
                "starTypeOverrideBinary1": None if self.star_type_override_b1_var.get() == "Default (random)" else get_star_type_value(self.star_type_override_b1_var.get()),
                "starTypeOverrideBinary2": None if self.star_type_override_b2_var.get() == "Default (random)" else get_star_type_value(self.star_type_override_b2_var.get()),
                "binaryBrightnessMultiplier": float(self.binary_brightness_multiplier_var.get()) if self.binary_brightness_multiplier_var.get() else Settings.binaryBrightnessMultiplier
            }

            save_user_settings(new_settings)
            state.settings = new_settings
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
        self.isDownloading = True

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

class MainUI(ctk.CTk):
    def __init__(self, targetPath, startLoop, allActions, allThreads, mainThreadFinished, amountOfThingsDone, amountOfThingsToDo):
        super().__init__()
        self.wm_attributes("-type", "splash") if os.name != 'nt' else self.overrideredirect(True)
        self.option_add('*tearOff', False)
        self.config(menu=tk.Menu(self))  # Empty menu
        self.title("Infinite Discoveries " + __version__)
        self.geometry("800x500")
        self.minsize(900, 600)
        self.configure(bg="#1f1f1f")
        self.amountValues = [1, 5, 4, 2]
        self.targetPath = targetPath
        state.settings = load_user_settings()
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
        self.ActionLog = open(state.base_dir / "ActionLog.txt", "a")

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

        # System type dropdown
        self.system_type_var = ctk.StringVar(value=state.settings.get("systemType", "Interstellar"))
        self.system_type_label = ctk.CTkLabel(self.input_frame, text="System Type", text_color="#ffffff")
        self.system_type_label.pack(padx=10, pady=(5, 0), anchor="w")
        self.system_type_dropdown = ctk.CTkOptionMenu(
            self.input_frame,
            values=["Interstellar", "Interstellar + Wormholes"],
            variable=self.system_type_var
        )
        self.system_type_dropdown.pack(padx=10, pady=(0, 5), anchor="w")
        # Description with styled font
        regular_font = ctk.CTkFont(size=11)
        bold_font = ctk.CTkFont(size=11, weight="bold")

        self.system_type_desc_frame = ctk.CTkFrame(self.input_frame, fg_color="transparent")
        self.system_type_desc_frame.pack(padx=10, pady=(0, 1), anchor="w")

        ctk.CTkLabel(
            self.system_type_desc_frame,
            text="Interstellar: The classic planet pack system with planets around new stars",
            font=regular_font,
            text_color="#ffffff"
        ).pack(anchor="w", pady=0)

        ctk.CTkLabel(
            self.system_type_desc_frame,
            text="Interstellar + Wormholes: Makes wormholes between the stock planets and generated planets",
            font=regular_font,
            text_color="#ffffff"
        ).pack(anchor="w", pady=0)

        ctk.CTkLabel(
            self.system_type_desc_frame,
            text="[Coming soon] Kerbol System: Adds new planets and moons to the stock system, like OPM. No stars",
            font=regular_font,
            text_color="#888888"
        ).pack(anchor="w", pady=0)
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
        self.okToAccess = ctk.CTkLabel(self.output_frame, text="To write or not to write? That is the question.", text_color="#ffffff")
        # Estimated time
        self.est_time_text = ctk.CTkLabel(self.output_frame, text="Estimated Generator Time: 26.25 minutes.", text_color="#ffffff")
        # Start button
        self.start_button = ctk.CTkButton(self.output_frame, text="Start Generator", command=self.start_generator, text_color="#ffffff")
        self.check_and_download_assets()
        # Stats frame
        self.stats_frame = ctk.CTkFrame(self.output_frame)
        self.stats_system_amount = ctk.CTkLabel(self.stats_frame, text="Amount of systems: ????", text_color="#ffffff")
        self.stats_system_amount.pack(fill="x")
        self.stats_config_amount = ctk.CTkLabel(self.stats_frame, text="Amount of configs: ????", text_color="#ffffff")
        self.stats_config_amount.pack(fill="x")
        self.stats_texture_amount = ctk.CTkLabel(self.stats_frame, text="Amount of textures: ????", text_color="#ffffff")
        self.stats_texture_amount.pack(fill="x")
        # Seed input
        self.seed_var = ctk.StringVar(value=cache.get("seed", ""))
        self.seed_frame = ctk.CTkFrame(self.output_frame)
        self.seed_entry = ctk.CTkEntry(self.seed_frame, textvariable=self.seed_var, width=120, text_color="#ffffff", fg_color="transparent")
        self.seed_entry.pack(side="left", padx=5)
        self.seed_label = ctk.CTkLabel(self.seed_frame, text="Custom Seed", text_color="#ffffff")
        self.seed_label.pack(side="left", padx=5)
        self.seed_entry.bind("<KeyRelease>", self.handle_seed_input)
        # Settings, Delete buttons
        self.buttons_frame = ctk.CTkFrame(self.output_frame)
        self.settings_button = ctk.CTkButton(self.buttons_frame, text="Settings", command=openSettings, text_color="#ffffff")
        self.settings_button.pack(side="left", padx=10)
        self.delete_button = ctk.CTkButton(self.buttons_frame, text="Delete", command=lambda: DeleteWindow(self.targetPath).mainloop(), text_color="#ffffff")
        self.delete_button.pack(side="left", padx=10)
        # Output frame
        # Place moved widgets under output_frame, after currentActionText
        self.okToAccess.pack(fill="x", padx=10, pady=(0, 5))
        self.est_time_text.pack(fill="x", padx=10, pady=(0, 5))
        self.start_button.pack(fill="x", padx=10, pady=(0, 5))
        self.stats_frame.pack(fill="x", padx=10, pady=(0, 5))
        self.seed_frame.pack(fill="x", padx=10, pady=(0, 5))
        self.buttons_frame.pack(fill="x", padx=10, pady=(0, 20))

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
        # Prompt if InfiniteDiscoveries directory exists
        existing_dir = os.path.join(self.targetPath, "InfiniteDiscoveries")
        if os.path.exists(existing_dir):
            proceed = mb.askyesno("Directory Exists", f"The folder '{existing_dir}' already exists.\nContinuing may have unexpected results and/or cause errors with the generator. Proceed?")
            if not proceed:
                return
        try:
            starAmount = int(self.star_var.get())
            planetAmount = int(self.planet_var.get())
            moonAmount = int(self.moon_var.get())
            asteroidAmount = int(self.asteroid_var.get())
        except:
            return
        
        state.settings = load_user_settings()

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
        if state.settings["useMultithreading"]:
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
        if os.access(self.targetPath, os.W_OK) and not self.isDownloading:
            self.okToAccess.configure(text="Selected directory can be written to.", text_color="#8fff8f")
            if not self.running:
                self.start_button.configure(state="normal")
        elif self.isDownloading:
            self.okToAccess.configure(text="Asset download in progress!", text_color="#ff8f8f")
            self.start_button.configure(state="disabled")
        else:
            self.okToAccess.configure(text="Cannot write to selected directory!", text_color="#ff8f8f")
            self.start_button.configure(state="disabled")
        

        
        # Update start button text to latest action if changed
        if self.allActions:
            latest_action = self.allActions[-1]
            formatted_action = latest_action[1]
            if self.actionText != formatted_action:
                self.actionText = formatted_action
                self.start_button.configure(text=self.actionText, state="disabled")

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
            "path": self.directory_var.get(),
            "systemType": self.system_type_var.get()
        }
        try:
            with open(CACHE_FILE, "w") as f:
                json.dump(cache_data, f)
        except Exception as e:
            print("Failed to write cache:", e)
        # Save systemType to user settings before closing log file
        state.settings["systemType"] = self.system_type_var.get()
        save_user_settings(state.settings)
        # Properly close log file and exit
        self.ActionLog.close()
        self.destroy()
    def check_and_download_assets(self):
        import threading
        import urllib.request
        import zipfile

        def download():
            self.isDownloading = True
            try:
                url = "http://nitrogendioxide.dev/files/id-assets.zip"
                local_zip = WORK_DIR / "id-assets.zip"

                if local_zip.exists():
                    local_zip.unlink()

                self.show_download_popup()
                urllib.request.urlretrieve(url, local_zip, self.report_hook)

                with zipfile.ZipFile(local_zip, 'r') as zip_ref:
                    zip_ref.extractall(ASSETS_DIR)
                local_zip.unlink()

                self.close_download_popup()
                self.isDownloading = False
                mb.showinfo("Download Complete", f"Assets downloaded and extracted successfully.")
            except Exception as e:
                print("Asset download failed (or cancelled):", e)
                self.download_popup_label.configure(text=f"Download failed:\n{e}")

        # Only trigger download if directory is empty
        if not any(p.is_dir() for p in ASSETS_DIR.iterdir()):
            if hasattr(self, "start_button"):
                self.start_button.configure(state="disabled")
            threading.Thread(target=download, daemon=True).start()
        else:
            self.isDownloading = False

    def show_download_popup(self):
        self.download_popup = ctk.CTkToplevel(self)
        self.download_popup.geometry("400x150")
        self.download_popup.title("Downloading Assets")
        self.download_popup_label = ctk.CTkLabel(self.download_popup, text="Downloading asset pack...", wraplength=350, justify="center", text_color="#ffffff")
        self.download_popup_label.pack(pady=20, padx=20)
        self.download_progress = ctk.CTkProgressBar(self.download_popup)
        self.download_progress.set(0)
        self.download_progress.pack(pady=10, padx=20)
        self.download_popup.protocol("WM_DELETE_WINDOW", self.on_close)

    def close_download_popup(self):
        if hasattr(self, "download_popup"):
            self.download_popup.destroy()

    def report_hook(self, block_num, block_size, total_size):
        import time
        if total_size > 0:
            downloaded = block_num * block_size
            progress = min(downloaded / total_size, 1.0)
            self.download_progress.set(progress)

            now = time.time()
            if not hasattr(self, "_last_report_time"):
                self._last_report_time = now
                self._start_time = now
                self._last_downloaded = 0

            elapsed = now - self._last_report_time
            if elapsed >= 0.5:
                speed = (downloaded - self._last_downloaded) / elapsed / (1024 * 1024)  # MB/s
                self._last_report_time = now
                self._last_downloaded = downloaded
                self.download_popup_label.configure(
                    text=f"Downloading asset pack... {int(progress * 100)}% ({speed:.2f} MB/s)"
                )