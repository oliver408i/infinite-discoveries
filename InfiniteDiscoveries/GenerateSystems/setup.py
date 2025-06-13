from setuptools import setup, find_packages

setup(
    name="infinite-discoveries",
    version=__import__("infinite_discoveries").__version__,
    author="nitrogendioxide",
    description="Procedurally generates star systems for KSP",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "numpy",
        "customtkinter",
        "matplotlib",
        "Wand",
        "scipy",
        "colour",
        "noise",
        "pillow",
        "tk"
    ],
    entry_points={
        "gui_scripts": [
            "infinite-discoveries = infinite_discoveries.__main__:main"
        ]
    },
    python_requires=">=3.8",
)