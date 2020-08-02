import requests
from api_tutorial.keys import *

url = "https://www.livelib.ru/account/login"
payload = {
    "ab_action": "headerunreg",
    "user[login]": LIVELIB_EMAIL,
    "user[password]": LIVELIB_PASS,
    "user[redirect]": "",
    "user[onclick]": "",
    "source": "headerauth",
    "current_url": "https://www.livelib.ru/?utm_source=livelib&utm_medium=usermenu"
}

resp = requests.post(url=url, data=payload)
print(resp.text)
