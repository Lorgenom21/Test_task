import requests
from bs4 import BeautifulSoup
import fake_useragent


session = requests.Session()
link = 'https://siriust.ru/login/?return_url=index.php%3Fdispatch%3Dprofiles.update'
user = fake_useragent.UserAgent().random


header = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 YaBrowser/23.3.3.719 Yowser/2.5 Safari/537.36'
}

datas = {
    "user_login": "vanny03@mail.ru",
    "password": "Rftgyhuj21",

}



response = session.post(link,data=datas)

profile_info = "https://siriust.ru/profiles-update/"
profile_response = session.get(profile_info).text

print(profile_response)
#url = "https://siriust.ru/profiles-update/"
#res = session.get(url,headers=header).text
#print(session)


