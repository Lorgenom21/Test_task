import requests
from bs4 import BeautifulSoup
import fake_useragent


session = requests.Session()
link = 'https://siriust.ru/'
user = fake_useragent.UserAgent().random
f = open('result.txt', "w", encoding="utf-8")

#login = input('Введите логин: ')
#pasword = input('Введите пароль: ')
header = {
    'user-agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 YaBrowser/23.3.3.719 Yowser/2.5 Safari/537.36"
}

datas = {
    "return_url": "index.php?dispatch=profiles.update",
    "redirect_url":	"index.php?return_url=index.php%3Fdispatch%3Dprofiles.update&dispatch=auth.login_form",
    "user_login": 'vanny03@mail.ru',
    "password": 'Rftgyhuj21',
    "dispatch[auth.login]":	""


}



response = session.post(link,headers=header,data=datas).text

# Получаю данные с учетной записью
profile= 'https://siriust.ru/profiles-update/'
pars_profile = session.get(profile, headers=header).text
soup = BeautifulSoup(pars_profile, 'lxml')

# Записываю email
email = soup.find('input', id = 'email')
f.write("email: "+ email.get('value')+"\n")

#Записываю Имя, Фамилия и город
Name = soup.find('input', id = 'elm_15')
Surname = soup.find('input', id = 'elm_17')
City = soup.find('input', id ='elm_23')
f.write('Name: '+ Name.get('value')+ '\n')
f.write('Surname: '+ Surname.get('value')+ '\n')
f.write('City: ' + City.get('value')+ '\n')
f.write('-----------Избранные товары-----------'+'\n\n')

#Открываю страницу избранного
Favourite = 'https://siriust.ru/wishlist/'
pars_favourite = session.get(Favourite,headers=header).text
soup = BeautifulSoup(pars_favourite,'lxml')

#Поиск имен товаров
favourite_items_name = soup.find_all('a',class_='product-title')
arr_favourite_name = list()
for name in favourite_items_name:
    arr_favourite_name.append(name.text)
print(arr_favourite_name)
#Поиск цена товаров
favourite_items_price = soup.find_all('span', class_="ty-price-num")
arr_favourite_price = list()
for price in favourite_items_price[::2]:
    arr_favourite_price.append(price.text)
print(arr_favourite_price)
# Сортировка по розничной цене
arr_fav_price = list()
for i in arr_favourite_price[::2]:
    arr_fav_price.append(i)


count_comments = soup.find_all('span', class_='cn-comments')
arr_count = list()

for i in count_comments:
    arr_count.append(i.text)
print(count_comments)

# Вывод всей информации в текстоовый документ
for i in range(len(arr_favourite_name)):
    f.write('Товары: '+ arr_favourite_name[i] +'\n'+ 'Цена: '+ arr_favourite_price[i]+'\n'+
            'Кол-во отзывов: '+'\n')


f.close()



