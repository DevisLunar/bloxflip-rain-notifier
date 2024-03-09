# RESTARTER BY Revive#8798
# WEBHOOK AND JSON SUPPORT BY Moonly#7996


# modules
import requests, subprocess, json
from colorama import Fore, Style


# open file
f = open("restarter-config.json", "r")
data = json.load(f)
f.close()


# setup
minutes_per_restart = data['minutes']


# loop
while 1:
    process = subprocess.Popen(['python', 'notifier-main.py'])
    try:
        process.wait(minutes_per_restart * 60)
    except Exception:
        pass
    process.kill()
    print(Fore.LIGHTBLACK_EX, "restarting...", Style.RESET_ALL, flush=True)
    continue
