made_by = "kellyhated"
made_by = "coxy.57"


# modules
import http.client, requests, json, time
from colorama import Fore, Style


print(Fore.LIGHTRED_EX, """   ______  
  (_____ \ 
 _ _____) )
(_|_____ ( 
 _ _____) )
(_|______/ 
           \n╰┈➤bloxflip-rain-notifier notifier!""", Style.RESET_ALL, flush=True)


# notifier-config.json
f = open("notifier-config.json", "r")
try:
    config = json.load(f)
except:
    print(Fore.LIGHTRED_EX, "╰┈➤Error while reading bytes!", Style.RESET_ALL, flush=True)
    exit(0)
f.close()


# setup
webhook = config['CONFIG']['WEBHOOK']
time_sleep_every_loop = config['CONFIG']['SPEED']
ping = config['CONFIG']['PING']
ssl = config['CONFIG']['SSL']


def active():
    # headers & api.bloxflip.com conn
    headers = {
        "Referer": "https://bloxflip.com/",
        "Content-Type": "application/x-www-form-urlencoded",
        "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/117.0.5938.108 Mobile/15E148 Safari/604.1"
    }
    conn = http.client.HTTPSConnection("api.bloxflip.com")
    conn.request("GET", "/chat/history", headers=headers)
    return json.loads(conn.getresponse().read().decode())['rain']


# loop
while True:
    rain = active()
    if rain['active']:
        add = rain['duration'] + rain['created']
        dur = add/1000
        duration = round(dur)
        conv = (duration/(1000*60))%60
        time_to_sleep = (conv*60+10)
        rblxid = requests.post(f"https://users.roblox.com/v1/usernames/users", json={"usernames": [rain['host']]}, verify=ssl).json()['data'][0]['id'] 
        data = {
            "content": ping,
            "username": "Rain Notifier"
        }
        data["embeds"] = [
        {
            "description" : f"A rain has been started!\n**Host**: {rain['host']}\n**Rain Amount**: {rain['prize']}\n**Expiration**: <t:{duration}:R>\n**Hop on [BloxFlip](https://bloxflip.com) to participate in this chat rain!**",
            "title" : "Rain Notifier",
            "thumbnail": {
                "url": requests.get(f"https://thumbnails.roblox.com/v1/users/avatar-headshot?userIds={rblxid}&size=50x50&format=Png&isCircular=false", verify=ssl).json()['data'][0]['imageUrl']
                }
            }
        ]
        # webhook send
        r = requests.post(webhook, json=data, verify=ssl)
        time.sleep(time_to_sleep)
    time.sleep(time_sleep_every_loop)