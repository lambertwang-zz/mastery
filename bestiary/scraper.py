# import time
from bs4 import BeautifulSoup
import bs4
import sys
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

from fractions import Fraction
import re
import json

baseUrl = 'http://paizo.com/pathfinderRPG/prd/bestiary/'

def init_driver():
    driver = webdriver.Firefox()
    driver.wait = WebDriverWait(driver, 5)
    return driver

def lookup(driver, query):
    driver.get(baseUrl + 'monsterIndex.html')

    try:
        table = driver.wait.until(EC.presence_of_element_located((By.ID, 'monster-index-wrapper'))).get_attribute('innerHTML')

        soup = BeautifulSoup(table, 'html.parser')

        return soup
    except TimeoutException:
        print("Table not found")
        return None

def get_monster(index, all_stats, flavor = None):
    monster = {}

    if not flavor:
        print('No flavor passed')
        while True:
            if index >= len(all_stats):
                break
            try:
                if all_stats[index]['class'][0] == 'flavor-text':
                    print('Found flavor')
                    print(all_stats[index])
                    break
            except:
                pass
            index += 1

        monster['flavor'] = all_stats[index].text
        index += 1
        print(monster['flavor'])
        while True:
            if all_stats[index].name != 'p':
                index += 1
            else:
                break
    else:
        print('Is sub-monster')
        monster['flavor'] = flavor

    # print(all_stats[index])
    monster['name'] = all_stats[index].b.contents[0].lower()
    try:
        monster['challenge'] = float(Fraction(all_stats[index].b.contents[1].string.split()[1].lower()))
    except:
        monster['challenge'] = None
        return (monster, index)

    index += 2

    alignment = ''
    while True:
        if index >= len(all_stats):
            break
        try:
            alignment = re.search('([LNC][GNE])|([N])', all_stats[index].contents[0]).group(0)
            # print(all_stats[index].contents[0])
            # print(alignment)
            if alignment:
                break
        except:
            pass
        try:
            if all_stats[index]['class'][0] == 'stat-block-breaker':
                alignment = None
                break
        except:
            pass
        index += 1

    if alignment:
        monster['alignment'] = alignment
        monster['size'] = all_stats[index].contents[0].split()[1]

    while True:
        if index >= len(all_stats):
            break
        try:
            if all_stats[index]['class'][0] == 'stat-block-breaker':
                break
        except:
            pass
        index += 1
    index += 1
    while True:
        if all_stats[index].name != 'p':
            index += 1
        else:
            break
    # monster['ac'] = int(all_stats[index].contents[1].split()[0][:-1])
    monster['ac'] = int(all_stats[index].text.split()[1].replace(',', ' '))
    index += 1
    while True:
        if all_stats[index].name != 'p':
            index += 1
        else:
            break
    monster['hitpoints'] = int(all_stats[index].contents[1].split()[0])
    
    index += 1
    while True:
        if index >= len(all_stats):
            break
        try:
            if all_stats[index]['class'][0] == 'stat-block-breaker':
                break
        except:
            pass
        index += 1
    index += 1
    while True:
        try:
            if all_stats[index]['class'][0] == 'stat-block-breaker':
                break
        except:
            pass
        trait = ''
        try:
            trait = all_stats[index].b.string.lower()
        except:
            index += 1
            continue
        if trait == 'melee' or trait == 'ranged':
            string = list(map(lambda s: s.string if type(s) == bs4.element.NavigableString else s.text, all_stats[index].contents[1:]))
            string = ' '.join(string).replace(u'\u2013', '-')

            try:

                weapon = {}
                weapon['name'] = re.search('([a-zA-Z]+[a-zA-Z ]*)', string).group(0)
                damage = re.search('(\(.+\))', string).group(0)
                dice = re.search('(\dd\d+)', string)
                flat = re.search('(?:[\+-])(\d+)', string)
                weapon['flat_damage'] = 0 if flat == None else int(flat.group(0))
                weapon['dice'] = int(dice.group(0).split('d')[1])
                weapon['dice_count'] = int(dice.group(0).split('d')[0])

                monster[trait] = weapon
            except:
                pass
        index += 1

    while True:
        if index >= len(all_stats):
            print('End of page')
            break
        # print(all_stats[index])
        try:
            all_stats[index]['class']
            try:
                all_stats[index]['id']
                break
            except:
                pass
        except:
            if all_stats[index].name == 'p':
                break
        index += 1
    monster['description'] = []

    while True:
        if index >= len(all_stats):
            print('End of page')
            break
        if all_stats[index] == None:
            print('Empty element')
            break
        # if all_stats[index].name != 'p':
        #     print('Non-paragraph element')
        #     print(all_stats[index])
        #     break
        if all_stats[index].name == 'h1' or all_stats[index].name == 'h2':
            print('Found Header')
            break
        try:
            if all_stats[index]['class']:
                print('Element with class')
                break
        except:
            pass
        if all_stats[index].name == 'p':
            monster['description'].append(str(all_stats[index].text))
        # print(all_stats[index])
        # print(all_stats[index].string)
        index += 1

    return (monster, index)

monster_data = []

def extract_monster_data(driver, link):
    id = None
    if len(link.split('#')) > 1:
        id = link.split('#')[1]

    driver.get(baseUrl + link)
    
    monster_html = driver.wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'body'))).get_attribute('innerHTML')
    soup = BeautifulSoup(monster_html, 'html.parser')
    # all_stats = soup.VypfindAll('p')
    all_stats = soup.findChildren()

    index = 0
    while True:
        if index >= len(all_stats):
            print('Reached end of page ' + link)
            return
        try:
            if all_stats[index].name == 'h1':
                # print('Checking id')
                # print(id)
                # print(all_stats[index])
                try:
                    # print(all_stats[index]['id'])
                    if all_stats[index]['id'] == id:
                        break
                except:
                    # Has id but the link has no id
                    if id == None:
                        break
                    else:
                        # print('Cannot find ' + link)
                        # return
                        pass
        except:
            pass
        index += 1
    
    try:
        if all_stats[index + 1]['class'] == 'flavor-text':
            pass
    except:
        print('No flavor for ' + link)
        return

    monster = get_monster(index, all_stats)
    index = monster[1]

    if monster[0]['challenge']:
        monster_data.append(monster[0])
    print(monster[0])

    while True:
        if index >= len(all_stats):
            return
        try:
            if all_stats[index].name == 'h1' or all_stats[index].name == 'h2':
                print('Found Header')
                sys.stdout.flush()
                return
            # print(all_stats[index]['class'])
            if all_stats[index]['class'][0] == 'stat-block-title' and all_stats[index].b:
                print('Got sub monster')
                print(all_stats[index])
                sys.stdout.flush()
                pass
            else:
                index += 1
                continue
        except:
            index += 1
            continue
        sub_monster = get_monster(index, all_stats, monster[0]['flavor'])
        index = sub_monster[1]
        print(sub_monster)
        if sub_monster[0]['challenge']:
            monster_data.append(sub_monster[0])
        else:
            # pass
            index += 1


monster_urls = []

if __name__ == "__main__":
    driver = init_driver()
    soup = lookup(driver, "Selenium")

    if soup == None:
        exit()

    # table = driver.find_element(By.ID, 'monster-index-wrapper')
    # data_table = soup.body.find('table', { 'id': 'DataTables_Table_0'} )

    monster_links = soup.findAll('a')

    for a in monster_links:
        monster_urls.append(a['href'])

    url_index = 0
    # for link in monster_urls[:10]:
    for link in monster_urls:
        print('Url Index: ' + str(url_index))
        extract_monster_data(driver, link)
        url_index += 1
        # columns = row.findAll('td')
        # print(columns)
        # data = {}
        # data["rank"] =     columns[0].getText()
        # data["name"] =     columns[1].getText()
        # data["guild"] =    columns[2].getText()
        # data["realm"] =    columns[3].getText()
        # data["item_lvl"] = columns[4].getText()
        # data["dps"] =      columns[5].getText()
        # data["size"] =     columns[6].getText()
        # data["date"] =     columns[7].getText()
        # data["duration"] = columns[8].getText()
        # death_knights.append(data)
    # print(monster_data)
    print('Got ' + str(len(monster_urls)) + ' urls')
    print('Got ' + str(len(monster_data)) + ' monsters')
    with open('monsters.json', 'w') as outfile:
        json.dump(monster_data, outfile, indent=4, )

    driver.quit()