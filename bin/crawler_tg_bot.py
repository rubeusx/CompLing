import sqlite3
from selenium.webdriver.support import expected_conditions as EC
from urllib.parse import urljoin
import requests
from bs4 import BeautifulSoup as BS
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
import asyncio

async def crawler():
    url = "https://www.volgograd.kp.ru/online/"
    driver = webdriver.Chrome()
    driver.get(url)
    count = 0
    flag = 1
    checked_urls = set()

    while flag!=0:
        time.sleep(0.5)
        LoadMoreButton = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, '.cdgmSL'))
        )
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, '.cdgmSL'))
        )
        LoadMoreButton.click()

        soup = BS(driver.page_source, 'html.parser')
        NewsItems = soup.find_all('div', class_='ixDVFm')

        for item in NewsItems:
            title = item.find('a', class_='drlShK').text

            # блок даты
            date_element = item.find('span', class_='sc-1tputnk-9 gpa-DyG')
            date = []
            _ = []
            import datetime
            if date_element:
                if "вчера" in date_element.text:
                    _ = datetime.date.today() - datetime.timedelta(days=1)
                    date = _.strftime("%Y-%m-%d")
                elif "2 дня назад" in date_element.text:
                    _ = datetime.date.today() - datetime.timedelta(days=2)
                    date = _.strftime("%Y-%m-%d")
                elif "3 дня назад" in date_element.text:
                    _ = datetime.date.today() - datetime.timedelta(days=3)
                    date = _.strftime("%Y-%m-%d")
                elif "января" in date_element.text:
                    _ = date_element.text.split()
                    _[1] = '1'
                    if len(_) == 2:
                        _.append('2024')
                    _ = list(map(int, _))
                    newFormat = datetime.date(_[2], _[1], _[0])
                    date = newFormat.strftime("%Y-%m-%d")
                elif "февраля" in date_element.text:
                    _ = date_element.text.split()
                    _[1] = '2'
                    if len(_) == 2:
                        _.append('2024')
                    _ = list(map(int, _))
                    newFormat = datetime.date(_[2], _[1], _[0])
                    date = newFormat.strftime("%Y-%m-%d")
                elif "марта" in date_element.text:
                    _ = date_element.text.split()
                    _[1] = '3'
                    if len(_) == 2:
                        _.append('2024')
                    _ = list(map(int, _))
                    newFormat = datetime.date(_[2], _[1], _[0])
                    date = newFormat.strftime("%Y-%m-%d")
                elif "апреля" in date_element.text:
                    _ = date_element.text.split()
                    _[1] = '4'
                    if len(_) == 2:
                        _.append('2024')
                    _ = list(map(int, _))
                    newFormat = datetime.date(_[2], _[1], _[0])
                    date = newFormat.strftime("%Y-%m-%d")
                elif "мая" in date_element.text:
                    _ = date_element.text.split()
                    _[1] = '5'
                    if len(_) == 2:
                        _.append('2024')
                    _ = list(map(int, _))
                    newFormat = datetime.date(_[2], _[1], _[0])
                    date = newFormat.strftime("%Y-%m-%d")
                elif "июня" in date_element.text:
                    _ = date_element.text.split()
                    _[1] = '6'
                    if len(_) == 2:
                        _.append('2024')
                    _ = list(map(int, _))
                    newFormat = datetime.date(_[2], _[1], _[0])
                    date = newFormat.strftime("%Y-%m-%d")
                elif "июля" in date_element.text:
                    _ = date_element.text.split()
                    _[1] = '7'
                    if len(_) == 2:
                        _.append('2024')
                    _ = list(map(int, _))
                    newFormat = datetime.date(_[2], _[1], _[0])
                    date = newFormat.strftime("%Y-%m-%d")
                elif "августа" in date_element.text:
                    _ = date_element.text.split()
                    _[1] = '8'
                    if len(_) == 2:
                        _.append('2024')
                    _ = list(map(int, _))
                    newFormat = datetime.date(_[2], _[1], _[0])
                    date = newFormat.strftime("%Y-%m-%d")
                elif "сентября" in date_element.text:
                    _ = date_element.text.split()
                    _[1] = '9'
                    if len(_) == 2:
                        _.append('2024')
                    _ = list(map(int, _))
                    newFormat = datetime.date(_[2], _[1], _[0])
                    date = newFormat.strftime("%Y-%m-%d")
                elif "октября" in date_element.text:
                    _ = date_element.text.split()
                    _[1] = '10'
                    if len(_) == 2:
                        _.append('2024')
                    _ = list(map(int, _))
                    newFormat = datetime.date(_[2], _[1], _[0])
                    date = newFormat.strftime("%Y-%m-%d")
                elif "ноября" in date_element.text:
                    _ = date_element.text.split()
                    _[1] = '11'
                    if len(_) == 2:
                        _.append('2024')
                    _ = list(map(int, _))
                    newFormat = datetime.date(_[2], _[1], _[0])
                    date = newFormat.strftime("%Y-%m-%d")
                elif "декабря" in date_element.text:
                    _ = date_element.text.split()
                    _[1] = '12'
                    if len(_) == 2:
                        _.append('2024')
                    _ = list(map(int, _))
                    newFormat = datetime.date(_[2], _[1], _[0])
                    date = newFormat.strftime("%Y-%m-%d")
                elif "минуту назад" or "минуты назад" or "минут назад" or "час назад" or "часа назад" or "часов назад" in date_element.text:
                    date = datetime.date.today().strftime("%Y-%m-%d")
            else:
                date = "Нет даты"

            LinkElement = item.find('a', class_='drlShK').get('href')
            if LinkElement in checked_urls:
                continue
            FullLink = urljoin(url,LinkElement)

            answer = requests.get(FullLink)
            soup = BS(answer.content, "html.parser")
            texts = soup.find('p', class_='sc-1wayp1z-16 dqbiXu')

            # Блок ошибок
            try:
                answer = requests.get(FullLink)
                answer.raise_for_status()  # Проверка наличия ошибок при запросе
            except requests.exceptions.HTTPError as errh:
                print("HTTP Error:", errh)
                continue
            except requests.exceptions.ConnectionError as errc:
                print("Error Connecting:", errc)
                continue
            except requests.exceptions.Timeout as errt:
                print("Timeout Error:", errt)
                continue
            except requests.exceptions.RequestException as err:
                print("Other Error:", err)
                continue

            FullText = []
            for paragraph in texts:
                FullText.append(paragraph.text)
            text = ' '.join([str(i) for i in FullText])

            conn = sqlite3.connect("db_news_main2.db")
            cursor = conn.cursor()

            cursor.execute('''
                    CREATE TABLE IF NOT EXISTS db_news_main2 (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        title TEXT,
                        date_news TEXT,
                        url TEXT,
                        content TEXT
                    )
                ''')
            conn.commit()

            if FullLink not in checked_urls:
                cursor.execute('SELECT COUNT(*) FROM db_news_main2 WHERE url = ?', (FullLink,))

                ExistingRecordCount = cursor.fetchone()[0]

                if ExistingRecordCount == 0:

                    cursor.execute('''
                                INSERT INTO db_news_main2 (title, date_news, url, content) VALUES (?, ?, ?, ?)
                            ''', (str(title), str(date) ,str(FullLink), str(text)))

                    conn.commit()
                    #print(f"добавил {FullLink}")
                else:
                    flag=0
                    count+=1
                    #print(f"Уже есть {FullLink}")
                checked_urls.add(FullLink)

            cursor.execute('SELECT COUNT(*) FROM db_news_main2')
            if flag==0:
                break
            time.sleep(0.2)

    driver.quit()
    conn.close()


