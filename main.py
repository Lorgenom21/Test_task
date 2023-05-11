import requests
from bs4 import BeautifulSoup



session = requests.Session()
link = 'https://siriust.ru/'
f = open('result.txt', "w", encoding="utf-8")

login = input('Введите email: ')
pasword = input('Введите пароль: ')
header = {
    'user-agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 YaBrowser/23.3.3.719 Yowser/2.5 Safari/537.36"
}

datas = {
    "return_url": "index.php?dispatch=profiles.update",
    "redirect_url":	"index.php?return_url=index.php%3Fdispatch%3Dprofiles.update&dispatch=auth.login_form",
    "user_login": login,
    "password": pasword,
    "dispatch[auth.login]":	""


}

comments_dict= {}
shops = {}
count_sites = 0
arr_page = list()
arr_favourite_name = list()
arr_fav = list()
arr_favourite_price = list()
arr_fav_price = list()
arr_number_comment = list()
count_check_presence = 0

page = 0

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

for name in favourite_items_name:
    arr_favourite_name.append(name.text)
print(arr_favourite_name)

#Поиск цена товаров
favourite_items_price = soup.find_all('span', class_="ty-price-num")

for price in favourite_items_price[::2]:
    arr_fav.append(price.text)
for price in arr_fav[::2]:
    arr_favourite_price.append(price)
print(arr_favourite_price)

# Сортировка по розничной цене

for i in arr_favourite_price[::2]:
    arr_fav_price.append(i)

#Поиск иформации на каждой странице товара
find_comments = soup.find_all('a', class_='abt-single-image')


for i in find_comments:
    arr_page.append(i.get("href"))
print(arr_page)



# Функция для сбора комментов со страниц

for href in arr_page:
    comments = str()
    arr_check_shop = list()
    pars_page = session.get(href, headers=header).text
    soup = BeautifulSoup(pars_page,'lxml')
    visit_page = soup.find_all('div',class_ = "ty-discussion-post__message")
    number_comment = soup.find('a', class_='ty-discussion__review-a cm-external-click')
    check_product = soup.find_all('div', class_='ty-product-feature__value')
    #Провер на наличие отзвов
    if number_comment != None:
        arr_number_comment.append(number_comment.text.strip())
    else:
        arr_number_comment.append('0 Отзывов')
    #Перебор комментов
    for i in visit_page:

        comments += (i.text)
        comments += '\n'
    for i in check_product:
        i = i.text
        if i in ['  —  мало','  —  много','  —  достаточно']:
            count_check_presence += 1
    shops.setdefault(count_sites, str(count_check_presence))
    comments_dict.setdefault(count_sites,comments)
    count_sites +=1
    count_check_presence = 0


# Вывод всей информации в текстоовый документ
for i in range(len(arr_favourite_name)):
    f.write('Товар: ' + arr_favourite_name[i] + '\n' + 'Цена: ' + arr_favourite_price[i]+'\n' + 'Всего: '  + arr_number_comment[i] + '\n')
    f.write('Количество магазинов, в которых есть товар: ' + shops[i] + '\n\n')
    f.write('Отзывы: '+ comments_dict[i] +'\n')
    f.write('--------------------------------------------------------------------------'+'\n')
f.close()


