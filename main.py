#from pyfiglet import figlet_format
#import pyfiglet.fonts
import argparse
import json
import os
import subprocess

# FIGLET IS DISABLED DUE TO NOT COMPILING CORRECTLY WITH NUITKA

VERSION = "1.0"

#print(figlet_format(f"DebAssistant {VERSION}"))
print(f"DebAssistant {VERSION}")

parser = argparse.ArgumentParser()
parser.add_argument("--setup", action="store_true")
parser.add_argument("--make", action="store_true")
parser.add_argument("--build", action="store_true")
args = parser.parse_args()

print("Parsing args")
print("\n")

if args.setup:
    print("Creating a config")
    name = input("Name > ")
    version = input("Version > ")
    architecture = input("Architecture > ")
    maintainer = input("Maintainer > ")
    with open("debassistant.json", "w") as f:
        f.write(json.dumps({"name": name, "version": version, "architecture": architecture, "maintainer": maintainer, "debassistant": {"version": VERSION}}))
        f.close()
    #print(figlet_format("Done!"))
    print("Done!")
    print("Run --make to expand config!")
elif args.make:
    #print(figlet_format("Making!"))
    print("Making!")
    with open("debassistant.json", "r") as f:
        data = json.loads(f.read())
    os.mkdir(data['name'])
    print(f"Created {data['name']}")
    os.mkdir(f"{data['name']}/DEBIAN")
    print(f"Created {data['name']}/DEBIAN")

    with open(f"{data['name']}/DEBIAN/control", "w") as f:
        f.write(f"""Package: {data["name"]}
        Version: {data["version"]}
        Maintainer: {data["maintainer"]}
        Architecture: {data["architecture"]}
        Description: {data["name"]} created by DebAssistant
        """)
        f.close()
    
    with open(f"{data['name']}/DEBIAN/postinst", "w") as f:
        f.write("echo Installation complete - DebAssistant")
        f.close()

    #print(figlet_format("Done!"))
    print("Done!")
    print("Edit DEBIAN/postinst to edit commands ran after the install of the files.")
    print("Create files in the root where files would be saved. e.g. i would create usr/bin and put an executable inside.")
    print("Run --build to build to a .deb")
elif args.build:
    with open("debassistant.json", "r") as f:
        data = json.loads(f.read())
        f.close()
    #print(figlet_format("Building"))
    print("Building")
    res = subprocess.run(f"dpkg -b {data['name']}", shell=True, stdout=subprocess.PIPE)
    print(res.stdout.decode("utf-8"))
    #print(figlet_format("Built!"))
    print("Built!")
