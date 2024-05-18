import xml
import json
import re
import fake_useragent
import requests
import time
from bs4 import BeautifulSoup
import random
import sqlite3
import random


while True:
    try:
        ua = fake_useragent.UserAgent()
        headers1 = {'User-Agent': ua.random}

        cookies = {
            'ActListPageSize': '10',
            'enableSIH': 'true',
            'browserid': '2716269035775147421',
            'timezoneOffset': '18000,0',
            '_ga': 'GA1.2.1729894480.1675531847',
            'steamCurrencyId': '1',
            'strInventoryLastContext': '440_2',
            '_gid': 'GA1.2.90428206.1680871404',
            'sessionid': '58503e3caef48051f205bb6d',
            'steamCountry': 'IE%7C3fd0a85da73a39238aaa57e81b715d47',
            'cookieSettings': '%7B%22version%22%3A1%2C%22preference_state%22%3A1%2C%22content_customization%22%3Anull%2C%22valve_analytics%22%3Anull%2C%22third_party_analytics%22%3Anull%2C%22third_party_content%22%3Anull%2C%22utm_enabled%22%3Atrue%7D',
            'strResponsiveViewPrefs': 'touch',
        }

        headers = {
            'Accept': 'text/javascript, text/html, application/xml, text/xml, */*',
            'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
            'Connection': 'keep-alive',
            # 'Cookie': 'ActListPageSize=10; enableSIH=true; browserid=2716269035775147421; timezoneOffset=18000,0; _ga=GA1.2.1729894480.1675531847; steamCurrencyId=1; strInventoryLastContext=440_2; _gid=GA1.2.90428206.1680871404; sessionid=58503e3caef48051f205bb6d; steamCountry=IE%7C3fd0a85da73a39238aaa57e81b715d47; cookieSettings=%7B%22version%22%3A1%2C%22preference_state%22%3A1%2C%22content_customization%22%3Anull%2C%22valve_analytics%22%3Anull%2C%22third_party_analytics%22%3Anull%2C%22third_party_content%22%3Anull%2C%22utm_enabled%22%3Atrue%7D; strResponsiveViewPrefs=touch',
            'Referer': 'https://steamcommunity.com/market/search?q=&category_730_ItemSet%5B%5D=any&category_730_ProPlayer%5B%5D=any&category_730_StickerCapsule%5B%5D=any&category_730_TournamentTeam%5B%5D=any&category_730_Weapon%5B%5D=any&appid=730',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Mobile Safari/537.36',
            'X-Prototype-Version': '1.7',
            'X-Requested-With': 'XMLHttpRequest',
            'sec-ch-ua': '"Chromium";v="112", "Google Chrome";v="112", "Not:A-Brand";v="99"',
            'sec-ch-ua-mobile': '?1',
            'sec-ch-ua-platform': '"Android"',
        }

        params = {
            'start': '1400', #страницы перелистываются не в строке, а в этом параметре
            'count': '10'  
        }

        links = []

        # empty_url = input('Enter url: ')
        # for i in range(len(empty_url)-2):
        #     if empty_url[i] == 'p' and empty_url[i+2] == '_':
        #             empty_url = [empty_url[:i+1], empty_url[i+2:]]           #ссылкой станет: url = empty_url[0] + page + empty_url[1]
        #             break




        # Создаем соединение с базой данных
        conn = sqlite3.connect('database\mydatabase.db')
        # Открываем курсор для выполнения SQL-запросов
        cursor = conn.cursor()


        def set_countLinks(cursor):
            # Выполняем SQL-запрос на выборку количества записей из таблицы
            cursor.execute("SELECT COUNT(*) FROM mytable")

            # Получаем результат в виде числа
            count = cursor.fetchone()[0]

            # Выводим количество записей на экран
            return count
        countLinks = set_countLinks(cursor)
        countLinks = max(countLinks, 1)


        for page in range(countLinks//10, (2037//2)+1):  # хз, как это работает, но лучше сюда парсить кол-во страниц, а не писать на рандом второй аргумент ренжа
            successResponse = False
            while successResponse == False:
                url = f'https://steamcommunity.com/market/search?q=&category_730_ItemSet%5B%5D=any&category_730_ProPlayer%5B%5D=any&category_730_StickerCapsule%5B%5D=any&category_730_TournamentTeam%5B%5D=any&category_730_Weapon%5B%5D=any&appid=730#p{page}_popular_desc'
                response = requests.get(url, headers=headers, params={'start': page*10,'count': '10'}, cookies=cookies)

                if response.status_code == 200:
                    successResponse = True
                else:
                    print('---- Response error')
                    time.sleep(random.randint(320, 350)/10)
                    continue

                soup = BeautifulSoup(response.text, 'lxml')
                for link in soup.find_all(class_ = 'market_listing_row_link'):
                    conn = sqlite3.connect('database\mydatabase.db')
                    cursor = conn.cursor()
                    
                    if link.get('href') != '':
                        print(link.get('href'))
                        # Выполняем запрос INSERT для добавления новой строки в таблицу
                        cursor.execute("INSERT INTO mytable (link, itemname_id) VALUES (?, ?)", (link.get('href')[47:], 0))

                        # Сохраняем изменения
                        conn.commit()

                        # Закрываем соединение
                        conn.close()

                time.sleep(random.randint(30, 40)/10)
                del response
                del soup
    except:
        print('---- Error')
        time.sleep(10)


   

    



# jsom add itemname_id |
#                      v
# import subprocess

# output = subprocess.check_output(["curl", "-v", "https://steamcommunity.com/market/listings/730/Dreams%20%26%20Nightmares%20Case"])
# rs = output.decode("utf-8")

# for i in range(len(rs)-21):
#     a = ''
#     for n in range(1, 21+1):
#         a += rs[i+n]
#     if a == 'Market_LoadOrderSprea':
#         need = rs[i:]
#         need = need[:40]
#         break

# itemname_id = []
# for i in need:
#     if i in '1234567890': itemname_id.append(i)
# itemname_id = ''.join(itemname_id)

# itemname_id