# Quickly runs the program for development, to avoid having to package and install it
import os
if os.getenv('debug') is None:
    print("This file is for development only and should not be used in a production environment! Run it using python3 -m or the cli command!")
    exit()
import infinite_discoveries.__main__
infinite_discoveries.__main__.main()