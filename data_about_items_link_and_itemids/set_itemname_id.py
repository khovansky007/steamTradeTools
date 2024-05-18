import json
import subprocess
#from numsGoods import set_countItems
import random, time
import keyboard
import sqlite3
import random

def find_itemname_id(link):
    output = subprocess.check_output(
        ["curl", '-s', f"-d {link}", link]
        )
    time.sleep(5)
    rs = output.decode("utf-8")
    for i in range(13000, len(rs)-21):
        a = ''
        if rs[i+1] == 'M':
            for n in range(1, 21+1):
                a += rs[i+n]
            if a == 'Market_LoadOrderSprea':
                need = rs[i:]
                need = need[:40]
                break

    itemname_id = []
    for i in need:
        if i in '1234567890': itemname_id.append(i)
    itemname_id = ''.join(itemname_id)
    
    
    if len(itemname_id) > 0: return itemname_id
    else: return ''



paused = False
conn = sqlite3.connect('database\mydatabase.db')
# Открываем курсор для выполнения SQL-запросов
cursor = conn.cursor()
count_saved_item_id = 0

# Выполняем SQL-запрос на выборку данных из столбца "link" таблицы "mytable"
cursor.execute("SELECT * FROM mytable")

# Получаем результат в виде списка кортежей
rows = cursor.fetchall()

print('*')
links = [row[0] for row in rows if row[1] == 0]


for link in links:
    new_itemname_id = None
    while type(new_itemname_id) != int:
        try:
            conn = sqlite3.connect('database\mydatabase.db')
            # Открываем курсор для выполнения SQL-запросов
            cursor = conn.cursor()
            
            # Обновляем значение столбца "itemname_id" для строки, где значение столбца "link" равно
            new_itemname_id = int(find_itemname_id('https://steamcommunity.com/market/listings/730/'+link))
            cursor.execute(f"UPDATE mytable SET itemname_id = ? WHERE link = ?", (new_itemname_id, link))

            # Сохраняем изменения в базе данных
            conn.commit()
            conn.close()
            count_saved_item_id += 1
            print('---- Added a new item_id','---- Count of saved new links: ', count_saved_item_id)
            #if type(new_itemname_id) == int:
            #   time.sleep(random.randint(20,40)/10)
        except: 
            print('---- Error (mb too more requests)')
            print('---- Count of saved links (item_id): ', count_saved_item_id)
            time.sleep(random.randint(1000, 1200)/100)

print('---- end ----')
