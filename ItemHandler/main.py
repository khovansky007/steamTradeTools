import json
import re
import sqlite3
from typing import Any
import requests
from datetime import datetime, timedelta

cookies = {
    'timezoneOffset': '18000,0',
    #'_ga': 'GA1.2.1568107321.1675556007',
    #'browserid': '2867140156818504015',
    'strInventoryLastContext': '730_2',
    #'steamLoginSecure': '76561199142306040^%^7C^%^7CeyAidHlwIjogIkpXVCIsICJhbGciOiAiRWREU0EiIH0.eyAiaXNzIjogInI6MENFRl8yMjBEODJFMF9ENzAxMyIsICJzdWIiOiAiNzY1NjExOTkxNDIzMDYwNDAiLCAiYXVkIjogWyAid2ViIiBdLCAiZXhwIjogMTY4MTczMzQ5NCwgIm5iZiI6IDE2NzMwMDYyNDUsICJpYXQiOiAxNjgxNjQ2MjQ1LCAianRpIjogIjBEMjhfMjI2MUUxQkVfM0MwNzgiLCAib2F0IjogMTY3NjAyNjM5NiwgInJ0X2V4cCI6IDE2OTQyMjIyNDQsICJwZXIiOiAwLCAiaXBfc3ViamVjdCI6ICI5NC41MC4xMTIuMjE1IiwgImlwX2NvbmZpcm1lciI6ICI5NC41MC4xMTIuMjE1IiB9.TQnKBcSjmJi0zs_MQ1WO08_Z_Q1ixZrlXLCQNAJXsLSrOLx0qkx3j94mxj51_RbPUkDThXEuVM0L2BuuJTejDw',
    #'_gid': 'GA1.2.1387491289.1681646249',
    #'sessionid': 'e25ff4806fed3aa8b959db67',
    #'webTradeEligibility': '^%^7B^%^22allowed^%^22^%^3A1^%^2C^%^22allowed_at_time^%^22^%^3A0^%^2C^%^22steamguard_required_days^%^22^%^3A15^%^2C^%^22new_device_cooldown_days^%^22^%^3A0^%^2C^%^22time_checked^%^22^%^3A1681647982^%^7D',
}

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/112.0',  # mb need use fake  user agent?
    'Accept': '*/*',
    'Accept-Language': 'ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3',
    # 'Accept-Encoding': 'gzip, deflate, br',
    'X-Requested-With': 'XMLHttpRequest',
    'Connection': 'keep-alive',
    #'Referer': 'https://steamcommunity.com/market/listings/730/Revolution^%^20Case',
    # 'Cookie': 'timezoneOffset=18000,0; _ga=GA1.2.1568107321.1675556007; browserid=2867140156818504015; strInventoryLastContext=730_2; steamLoginSecure=76561199142306040^%^7C^%^7CeyAidHlwIjogIkpXVCIsICJhbGciOiAiRWREU0EiIH0.eyAiaXNzIjogInI6MENFRl8yMjBEODJFMF9ENzAxMyIsICJzdWIiOiAiNzY1NjExOTkxNDIzMDYwNDAiLCAiYXVkIjogWyAid2ViIiBdLCAiZXhwIjogMTY4MTczMzQ5NCwgIm5iZiI6IDE2NzMwMDYyNDUsICJpYXQiOiAxNjgxNjQ2MjQ1LCAianRpIjogIjBEMjhfMjI2MUUxQkVfM0MwNzgiLCAib2F0IjogMTY3NjAyNjM5NiwgInJ0X2V4cCI6IDE2OTQyMjIyNDQsICJwZXIiOiAwLCAiaXBfc3ViamVjdCI6ICI5NC41MC4xMTIuMjE1IiwgImlwX2NvbmZpcm1lciI6ICI5NC41MC4xMTIuMjE1IiB9.TQnKBcSjmJi0zs_MQ1WO08_Z_Q1ixZrlXLCQNAJXsLSrOLx0qkx3j94mxj51_RbPUkDThXEuVM0L2BuuJTejDw; _gid=GA1.2.1387491289.1681646249; sessionid=e25ff4806fed3aa8b959db67; webTradeEligibility=^%^7B^%^22allowed^%^22^%^3A1^%^2C^%^22allowed_at_time^%^22^%^3A0^%^2C^%^22steamguard_required_days^%^22^%^3A15^%^2C^%^22new_device_cooldown_days^%^22^%^3A0^%^2C^%^22time_checked^%^22^%^3A1681647982^%^7D',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    #'If-Modified-Since': 'Sun, 16 Apr 2023 12:27:00 GMT',
}

params = {
    'country': 'RU',
    'language': 'russian',
    'currency': '5',
    #'item_nameid': '176358765',
    'two_factor': '0',
}




# link = 'https://steamcommunity.com/market/listings/730/'+thing[0]
# itemname_id = str(thing[1])
# # link = 'https://steamcommunity.com/market/listings/730/MAC-10%20%7C%20Disco%20Tech%20%28Well-Worn%29'
# # itemname_id = '176118350'

# # получаем данные по продажам
# response = requests.get(link, headers=headers, cookies=cookies)
# m = re.search(r'var line1=(.+);', response.text)
# data_str = m.group(1)
# histogram = json.loads(data_str)
# #
class Db:
    def GetItemsInfo() -> list[set[str, int]]:
        '''mytable (link TEXT, itemname_id INTEGER)
            -> return [(short_link: str, item_id: int), ...]
        '''
        conn = sqlite3.connect('..\data_about_items_link_and_itemids\database\mydatabase.db')
        # Открываем курсор для выполнения SQL-запросов
        cursor = conn.cursor()
        # Получаем всю таблицу
        cursor.execute("SELECT * FROM mytable")
        data = cursor.fetchall()
        return data
    
class SteamItem:
    def __init__(self, gameCode: int, currency: int, short_link: str, itemname_id: int):
        '''
        gameCOde:
            Стим код игры https://steamcommunity.com/market/listings/{код_игры}/...
            Для ксго = 730
        currency:
            1 - в долларах
            5 - в рублях    
        '''
        self.gameCode = gameCode
        self.currency = currency
        self.short_link = short_link
        self.itemname_id = itemname_id


class SteamItemTools(SteamItem):
    '''Получение данных о предмете'''

    def __init__(self, gameCode: int, currency: int, short_link: str, itemname_id: int):
        #inherit
        self.gameCode = gameCode
        self.currency = currency
        self.short_link = short_link
        self.itemname_id = itemname_id

        #extends
        self.soldData: list[list[str, float, int]] | None = None
        self.soldDataExpires: datetime | None = None

    def GetSoldData(self):
        '''Гистограмма: сколько раз продали за какой период и по какой цене
            return [['Mar 19 2024 19: +0', 0.414, '3294'], ['Mar 19 2024 20: +0', 0.414, '3443']]
            -> [[date, price, count]]
        Нагрузка (выполняется) раз в liveTimeMinunes минут, по дефолту 50 минут
        '''
        def _getData(self):
            '''Метод получения данных гистограммы'''
            full_item_link = f'https://steamcommunity.com/market/listings/{self.gameCode}/{self.short_link}'

            response = requests.get(url=full_item_link, headers=headers, cookies=cookies)
            print(response.status_code)
            def _getSellData(response) -> str:
                m = re.search(r'var line1=(.+);', response.text)
                data_str = m.group(1)
                return data_str
            data_str = _getSellData(response)     
            data = [list(x) for x in json.loads(data_str)] # конвертирует строку в словарь
            return data

        def _OptimazeWithExpire(self, liveTimeMinunes: int = 50):
            '''Оптимизация: устанавливает время жизни данных, и если он еще нормальные, но ничего не делаем.'''
            if (self.soldDataExpires == None) or (self.soldDataExpires < datetime.now()):
                
                self.soldData = _getData(self)
                self.soldDataExpires = datetime.now() + timedelta(minutes=liveTimeMinunes)
            return self.soldData
        
        return _OptimazeWithExpire(self)

    def GetOrdersData(self) -> set[    list[list[float, int, str]],   list[list[float, int, str]]    ]:
        '''Возвращает два списка: buy order, sell order
        buy order: [39.62, 773, 'Предложений по цене 39,62 pуб. и ниже: 773']
        sell order: [31.63, 313264, 'Заказов по цене 31,63 pуб. и выше: 313,264']
        types: [float, int, str]
        '''
        cookies = {
            # 'sessionid': '3c756f98329f1bfe8f193654',
            'steamCountry': 'RU%7C73f3574ae74bf64524b56db52d370d47',
            'timezoneOffset': '18000,0',
        }

        headers = {
            'Accept': '*/*',
            'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
            'Connection': 'keep-alive',
            # 'Cookie': 'sessionid=3c756f98329f1bfe8f193654; steamCountry=RU%7C73f3574ae74bf64524b56db52d370d47; timezoneOffset=18000,0',
            'If-Modified-Since': 'Wed, 20 Mar 2024 16:03:20 GMT',
            # 'Referer': 'https://steamcommunity.com/market/listings/730/AWP%20%7C%20POP%20AWP%20%28Well-Worn%29',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
            'X-Requested-With': 'XMLHttpRequest',
            'sec-ch-ua': '"Chromium";v="122", "Not(A:Brand";v="24", "Google Chrome";v="122"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
        }

        params = {
            'country': 'RU',
            'language': 'russian',
            'currency': 5,
            'item_nameid': {self.itemname_id},
            'two_factor': '0',
        }
        link = f'https://steamcommunity.com/market/itemordershistogram'
        response = requests.get(url=link, params=params, cookies=cookies, headers=headers)
        print(response.status_code)
        # graf_data = json.loads(response.text)
        buy_order_graph = [list(x) for x in json.loads(response.text)['buy_order_graph']]
        sell_order_graph = [list(x) for x in json.loads(response.text)['sell_order_graph']]
        
        return (buy_order_graph, sell_order_graph)
       
    def GetCountSold(self, period_days: int) -> int:
        '''Количество продаж этой вещи за period_days дней
            Нагрузка (выполняется GetSoldData) раз в liveTimeMinunes минут, по дефолту 50 минут'''
        return sum(int(frame_per_hour[2]) for frame_per_hour in self.GetSoldData()[-24*period_days:])

    def GetMenianPrice(self, period_days: int) -> float:
        '''Медианная цена
            Нагрузка (выполняется GetSoldData) раз в liveTimeMinunes минут, по дефолту 50 минут'''
        prices = sorted([float(frame_per_hour[1]) for frame_per_hour in self.GetSoldData()[-24*period_days:]])
        if len(prices)%2 !=0:
            return prices[len(prices)//2 + 1]
        return (prices[len(prices)//2] + prices[len(prices)//2 + 1]) / 2



def Main(*args, **kwargs):
    for itemData in Db.GetItemsInfo():
        csgo = SteamItemTools(gameCode=730, currency=5, short_link=itemData[0], itemname_id=itemData[1])
        while True:
            print(csgo.GetSoldData(), csgo.GetCountSold(period_days=1), csgo.GetMenianPrice(period_days=1))
            input()
            
            # print(csgo.GetMenianPrice(period_days=1))
            # print(csgo.GetItemSoldData(itemData)[0][0])




if __name__ == '__main__':
    Main()