
import re
import pprint
import os


def pp(var, name=None):
    if name:
        print(f"{{ {name} }}:")
    pprint.pprint(var)


def showlogo():
    with open("logo.txt", "r", encoding="utf-8") as f:
        logo = f.read()

    print(logo)


def make_filesystem_safe(savename):
    return re.sub(r'[^\w.-]+', '-', savename)


def extract_world_name(filename):
    pattern = r"^\((.*)\) \d{4}-\d{2}-\d{2}-\d{2}-\d{2}-\d{2}"
    match = re.match(pattern, filename)
    if match:
        return match.group(1)
    return None
