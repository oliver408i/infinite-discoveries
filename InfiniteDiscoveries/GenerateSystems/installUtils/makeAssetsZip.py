import os
import zipfile

if os.path.exists('assets.zip'):
    os.remove('assets.zip')

with zipfile.ZipFile('assets.zip', 'w', compression=zipfile.ZIP_DEFLATED) as zipf:
    cwd = os.getcwd()
    while not os.path.basename(cwd) == 'InfiniteDiscoveries':
        print("Trying: " + cwd)
        cwd = os.path.dirname(cwd)
        if cwd == "/":
            raise Exception("Could not find InfiniteDiscoveries directory")
    for root, dirs, files in os.walk(cwd):
        for file in files:
            if 'GenerateSystems' in os.path.relpath(root, cwd).split(os.sep):
                continue
            if file.startswith('.'):
                continue
            print("Adding: " + os.path.relpath(os.path.join(root, file), cwd))
            zipf.write(os.path.join(root, file), os.path.relpath(os.path.join(root, file), cwd))
