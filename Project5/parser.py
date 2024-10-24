# import json
# from selenium import webdriver
# from selenium.webdriver.chrome.service import Service as ChromeService
# from bs4 import BeautifulSoup
# from bolshoi import get_users, bot
# import time

# def get_site_data():
#     cService = ChromeService(executable_path=r'chromedriver.exe')
#     driver = webdriver.Chrome(service=cService)

#     driver.get('https://ticket.bolshoi.ru/shows')
#     time.sleep(2)
#     html = driver.page_source
#     soup = BeautifulSoup(html, 'html.parser')
#     shows = soup.find_all('li', class_='scoreboard__tr')
    
#     new_data = []
#     for show in shows:
#         date = show.find('div', class_='scoreboard__td--date').p.text.strip()
#         time_and_day = show.find('div', class_='scoreboard__td--date').span.text.strip()
#         name = show.find('div', class_='scoreboard__td--name').p.text.strip()
#         type_of_show = show.find('div', class_='scoreboard__td--type').p.text.strip()
#         venue = show.find('div', class_='scoreboard__td--type').span.text.strip()

#         show_info = {
#             "date": date,
#             "time_and_day": time_and_day,
#             "name": name,
#             "type": type_of_show,
#             "venue": venue,
#         }
#         new_data.append(show_info)
    
#     return new_data 

# def parse():
#     users = get_users()
    
#     try:
#         with open('shows_data.json', 'r', encoding='utf-8') as json_file:
#             old_data = json.load(json_file)
#     except FileNotFoundError:
#         old_data = [] 

#     new_data = get_site_data()

#     if new_data != old_data:
#         added_shows = [show for show in new_data if show not in old_data]
#         removed_shows = [show for show in old_data if show not in new_data]

#         response_message = []
#         response_message.append("Есть изменения!")

#         if added_shows:
#             response_message.append("Добавлены билеты:")
#             response_message.extend([str(show) for show in added_shows])

#         if removed_shows:
#             response_message.append("Удалены билеты:")
#             response_message.extend([str(show) for show in removed_shows])

#         for user in users:
#             bot.send_message(user, "\n".join(response_message))

#     else:
#         for user in users:
#             bot.send_message(user, "Ничего не изменилось.")

#     with open('shows_data.json', 'w', encoding='utf-8') as json_file:
#         json.dump(new_data, json_file, ensure_ascii=False, indent=4)

# while True:
#     parse()
#     time.sleep(10)



import json
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from bs4 import BeautifulSoup
from bolshoi import get_users, bot
import time

def get_site_data():
    cService = ChromeService(executable_path=r'chromedriver.exe')
    driver = webdriver.Chrome(service=cService)


    driver.get('https://ticket.bolshoi.ru/shows')
    time.sleep(2)
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    shows = soup.find_all('li', class_='scoreboard__tr')
    
    new_data = []
    for show in shows:
        date = show.find('div', class_='scoreboard__td--date').p.text.strip()
        time_and_day = show.find('div', class_='scoreboard__td--date').span.text.strip()
        name = show.find('div', class_='scoreboard__td--name').p.text.strip()
        type_of_show = show.find('div', class_='scoreboard__td--type').p.text.strip()
        venue = show.find('div', class_='scoreboard__td--type').span.text.strip()

        show_info = {
            "date": date,
            "time_and_day": time_and_day,
            "name": name,
            "type": type_of_show,
            "venue": venue,
        }
        new_data.append(show_info)
    
    return new_data 

def get_current_shows():
    try:
        with open('shows_data.json', 'r', encoding='utf-8') as json_file:
            return json.load(json_file)
    except:
        return []


def save_shows(shows):
    with open('shows_data.json', 'w', encoding='utf-8') as json_file:
        json.dump(shows, json_file, ensure_ascii=False, indent=4)
    
def parse():
    users = get_users()
    
    old_data = get_current_shows()
    new_data = get_site_data()

    new_shows = [show for show in new_data if show not in old_data]
    old_shows = [show for show in new_data if show in old_data]

    print("new shows:", len(new_shows))
    print("old shows:", len(old_shows))

    save_shows(new_shows + old_shows)

    if new_shows:
        for i in range(0, len(new_shows), 20):
            text = ""
            for show in new_shows[i:i+30]:
                text += f'{show["name"]} ({show["date"]})\n'    

            for user in users:        
                bot.send_message(user, text)
        

while True:
    parse()
    time.sleep(3600)


