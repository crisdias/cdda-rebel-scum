import re
import os
from   tqdm import tqdm
import zipfile
from   utils import *




def prompt_option(worlds, msg="Enter the number of the desired world: "):
    print(msg)
    while True:
        for i, world in enumerate(worlds):
            print(f"{i+1}: {world}")

        user_input = input("> ") or "1"

        if user_input.isdigit():
            user_input = int(user_input)
            if user_input > 0 and user_input <= len(worlds):
                chosen_world = worlds[user_input - 1]
                return chosen_world
            else:
                print(
                    f"Invalid number. Please enter a number between 1 and {len(worlds)}.")
        else:
            print("Invalid input. Please enter a number.")


def get_operation(msg, default="S"):
    while True:
        user_input = input(
            msg) or default
        if user_input.upper() in ["S", "R"]:
            return "save" if user_input.upper() == "S" else "restore"
        else:
            print("Invalid input. Please enter S or R.")


def save_to_zip(source_folder, backup_path):
    # count how many files is source_folder
    total_files = 0
    for root, dirs, files in os.walk(source_folder):
        print(".", end="")
        total_files += len(files)

    print(f"\nBacking up {total_files} files to {backup_path}...\n")

    with zipfile.ZipFile(backup_path, 'w', zipfile.ZIP_DEFLATED) as backup:
        for root, dirs, files in os.walk(source_folder):
            progressname = root.split(os.sep)[-1]
            for file in tqdm(files, desc=f"Adding {progressname}", leave=False):
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, source_folder)
                backup.write(file_path, arcname)


def restore_from_zip(backup_path, source_folder):
    # delete all files, folders and subfolde
    for root, dirs, files in os.walk(source_folder, topdown=False):
        for name in files:
            os.remove(os.path.join(root, name))
        for name in dirs:
            os.rmdir(os.path.join(root, name))

    # unzip backup to source_folder
    with zipfile.ZipFile(backup_path, 'r') as backup:
        for file in tqdm(backup.namelist(), leave=False):
            backup.extract(file, source_folder)


def find_worlds_in_folder(folder):
    zips = [f for f in os.listdir(folder)
              if os.path.isfile(os.path.join(folder, f)) and f.endswith(".zip")]
    
    zips = sorted(zips,
                    key=lambda x: os.path.getmtime(os.path.join(folder, x)),
                    reverse=True)

    worlds = []
    for z in zips:
        w = extract_world_name(z)
        if w and w not in worlds:
            worlds.append(w)

    return worlds




def find_backups_for_world(folder, world):
    zips = [f for f in os.listdir(folder)
              if os.path.isfile(os.path.join(folder, f)) and f.endswith(".zip")]
    
    zips = sorted(zips,
                    key=lambda x: os.path.getmtime(os.path.join(folder, x)),
                    reverse=True)

    backups = []
    for z in zips:
        w = extract_world_name(z)
        if w and w == world:
            backups.append(z)

    return backups