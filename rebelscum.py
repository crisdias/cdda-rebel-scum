import datetime
import os
import ruamel.yaml

from   utils import *
from   steps import *
from   logo  import showlogo

homedir = os.path.expanduser("~")
basefolder = os.path.join(homedir, ".rebelscum")
configfile = os.path.join(basefolder, "config.yml")

if not os.path.exists(basefolder):
    os.makedirs(basefolder)

# exit if sourcesfile does not exist
if os.path.exists(configfile):
    with open(configfile, "r") as f:
        config = ruamel.yaml.load(f, Loader=ruamel.yaml.Loader)
else:
    config = {
        "backupfolder": "G:\Meu Drive\_game_backups\cddawin-rebelscum",
        "cddafolder": "C:\games\CDDA\cddaxp\save"
    }

    # save config to configfile
    with open(configfile, "w") as f:
        ruamel.yaml.dump(config, f)
    
    print(f"No sources file found. Default values used.\nEdit {configfile} to change them.")


# find all subfolders in config["cddafolder"], store them in worlds
worlds = [f for f in os.listdir(config["cddafolder"]) if os.path.isdir(os.path.join(config["cddafolder"], f))]
worlds = sorted(worlds,
    key=lambda x: os.path.getmtime(os.path.join(config["cddafolder"], x)),
    reverse=True)


showlogo()
operation = get_operation("\nSave or restore? (S/R). Default: Save.", "S")

# zip the world folder into backuppath
if operation == "save":
    world = prompt_option(worlds, "Choose a world to backup:\n---------------\n")
    savename = input("\n(Optional) Enter a name for the save: ")
    if savename:
        savename = "-" + make_filesystem_safe(savename)
    else:
        savename = ""

    thisdate = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
    filename = f"({world}) {thisdate}{savename}.zip"
    backuppath = os.path.join(config["backupfolder"], filename)
    sourcefolder = os.path.join(config["cddafolder"], world)

    save_to_zip(sourcefolder, backuppath)
    print(f"\n\nSaved {world} to {backuppath}!\n")
else:
    worlds = find_worlds_in_folder(config["backupfolder"])
    if not worlds:
        print("No worlds found in backup folder. Exiting.")
        exit()

    world = prompt_option(
        worlds, "Choose a world to restore:\n---------------\n")
    
    backups = find_backups_for_world(config["backupfolder"], world)

    if not backups:
        print("No backups found for that world. Exiting.")
        exit()

    if len(backups) == 1:
        backup = backups[0]
    else:
        backup = prompt_option(backups, "Choose a backup to restore:\n---------------\n")

    backuppath = os.path.join(config["backupfolder"], backup)
    destfolder = os.path.join(config["cddafolder"], world)

    print(f"Restoring {backup} to {world}...")
    restore_from_zip(backuppath, destfolder)

    print("\nDone!\n")
