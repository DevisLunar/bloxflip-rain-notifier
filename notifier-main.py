made_by = "kellyhated"
made_by = "coxy.57"


# modules
import http.client, requests, json, time
from colorama import Fore, Style


requests.packages.urllib3.disable_warnings()


# notifier-config.json
f = open("config.json", "r")
try:
    data = json.load(f)
except:
    print(Fore.LIGHTBLACK_EX, f"☂{time.strftime('%H:%M:%S')}│\n╰┈➤ error while reading bytes!", Style.RESET_ALL, flush=True)
    exit(0)
f.close()


# setup
webhook = data['CONFIG']['WEBHOOK']
time_sleep_every_loop = data['CONFIG']['SPEED']
ping = data['CONFIG']['PING']
ssl = data['CONFIG']['SSL']


print(Fore.LIGHTRED_EX, f"""   ______  
  (_____ \ 
 _ _____) )
(_|_____ ( 
 _ _____) )
(_|______/ 
           \n☂{time.strftime("%H:%M:%S")}│\n╰┈➤ bloxflip-rain-notifier started!""", Style.RESET_ALL, flush=True)


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
while 1:
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
        r = requests.post(webhook, json=data, verify=ssl).status_code
        is_sent_verify = True, print(Fore.LIGHTRED_EX, f"☂{time.strftime('%H:%M:%S')}│\n╰┈➤the message was sent!", Style.RESET_ALL, flush=True) if r == 200 else False
        time.sleep(time_to_sleep)
    time.sleep(time_sleep_every_loop)