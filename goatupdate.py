#!/usr/bin/python3
import json
import argparse
import os
import sys
import datetime
import subprocess

parser = None
FILE_NAME = "goatupdate_data.json"

BANNER = r"""
 _______________
<   GoatUpdate  >
 ---------------
        \   ^__^
         \  (oo)\_______
            (__)\       )\/\
                ||----w |
                ||     ||
"""


GOAT_BANNER = r"""
    _))
   > *\     _~
   `;'\\__-' \_
      | )  _ \ \
    / /  ``   w w
   w w
"""



COLOR = {
    "WHITE": "\033[0;37m",
    "RED": "\033[0;31m",
    "BLUE": "\033[0;34m",
    "CYAN": "\033[0;36m",
    "GREEN": "\033[0;32m",
    "RESET": '\033[0m',
    "BOLD": "\033[;1m",
    "YELLOW": "\033[0;33m",
    "BBLACK": "\033[1;30m",
    "BRED": "\033[1;31m",
    "BGREEN": "\033[1;32m",
    "BYELLOW": "\033[1;33m",
    "BBLUE": "\033[1;34m",
    "BPURPLE": "\033[1;35m",
    "BCYAN": "\033[1;36m",
    "BWHITE": "\033[1;37m",
    "REVERSE": "\033[;7m"
}


def console_print(txt: str, signe="+", color="yellow", line: bool=False) -> None:
    """print output console message with color

    Args:
        txt (str): text to print
        signe (str, optional): signe after text. Defaults to "!".
        color (str, optional): color of message. Defaults to "byellow".
    """
    line_return = ""
    if line:
        line_return = "\n"
    if color != None and type(color) == str:
        sys.stdout.write(COLOR[color.upper()])
    if signe is None:
        print(f"{line_return} {txt}{COLOR['RESET']}")
    else:
        print(f"{line_return}[{signe}] {txt}{COLOR['RESET']}")


def update_command(path: str, json_data: dict):
    console_print("update run")
    try:
        subprocess.run(["apt", "update"], check=True)
        subprocess.run(["apt", "upgrade"], check=True)
    except (subprocess.CalledProcessError, OSError) as e:
        console_print("An error has occurred during the apt command", color="red")
        console_print(e, "!",color="red")
        sys.exit(1)
    except (Exception) as e:
        console_print('An error has occurred : ', color="red")
        console_print(e, color="red", signe=None)
        sys.exit(1)
    os.remove(path + FILE_NAME)
    with open(path + FILE_NAME, "w", encoding="utf-8") as f:
        json.dump(json_data, f)



def check_up_to_date(path: str):
    if(path[-1] != "/"):
        path = path + "/"

    console_print("path verification")
    if(not os.access(path, os.F_OK)):
        msg = "Error the path specified in command cannot be accessed."
        console_print(msg, "!", "red", True)
        raise OSError("Error with path validation")
    elif(not os.access(path, os.R_OK)):
        msg = "Error the path specified in command cannot be accessed. You have not right for read"
        console_print(msg, "!", "red", True)
        raise OSError("Error with path validation")
    elif(not os.access(path, os.W_OK)):
        msg = "Error the path specified in command cannot be accessed. You have not right for write"
        console_print(msg, "!", "red", True)
        raise OSError("Error with path validation")

    if(os.path.exists(path + FILE_NAME)):
        # file exist read this
        console_print("data file exist, checking validity")
        json_data = None
        with open(path + FILE_NAME, "r", encoding="utf-8") as f:
            json_data = json.load(f)
        date = datetime.datetime.now().strftime("%Y-%m-%d")

        if(date == json_data["date"] and json_data["update"]):
            console_print("already up to date", color="green")
            return
        else:
            json_data["date"] = date
            update_command(path, json_data)
    else:
        # file not exist make this and run command
        console_print("data file not exist, start update and creation of file")
        console_print("run update")
        try:
            json_data = {}
            with open(path + FILE_NAME, "w", encoding="utf-8") as f: 
                json_data["date"] = datetime.datetime.now().strftime("%Y-%m-%d")
                json_data["update"] = True
                json.dump(json_data, f)
                
            console_print("file created", color="green")
            update_command(path, json_data)
        except Exception as e:
            console_print("An error has occurred for create file", "!", "red", True)
            console_print(e, "!",color="red")
            raise

def main():
    args = parser.parse_args()
    print(BANNER)
    if(os.getuid() != 0):
        console_print("Error please run goatupdate with root right", "!", "red")
        sys.exit(1)
    console_print("Welcome, uploadgoat check if you are up to date")
    try:
        check_up_to_date(args.path)
    except Exception as e:
        console_print(f"An error has occurred during the command :")
        console_print(e, "!",color="red")
        sys.exit(1)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="autoupdate linux with apt, use -h or --help for usage help")
    parser.add_argument("path", metavar="path", type=str, help="path to store file with data of last update. Do not specify the file")
    main()