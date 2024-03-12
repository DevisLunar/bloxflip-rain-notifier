# RESTARTER BY Revive#8798
# WEBHOOK AND JSON SUPPORT BY Moonly#7996

try:
  import requests
  import subprocess
  import json
except ModuleNotFoundError:
  __import__("os").system("pip install requests")

with open('restarter-config.json', 'r') as f:
  data = json.load(f)

minutes_per_restart = data["minutes"]

while True:
    process = subprocess.Popen(['python', 'notifier-main.py'])
    try:
        process.wait(minutes_per_restart * 60)
    except KeyboardInterrupt:
        print("Exiting")
        break
    except Exception:
        pass
    process.kill()
    print("Restarting")
    continue