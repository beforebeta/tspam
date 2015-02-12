# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import requests
import time

     # 'user_email': 'lraleigh@taunton.com',
     # 'user_pass': 'joshua19'}

import sys
import traceback
def print_stack_trace():
    print '-'*60
    traceback.print_exc(file=sys.stdout)
    print '-'*60


from bs4 import BeautifulSoup

def del_requests():
    url = 'https://www.finehomebuilding.com/user/login'
    payload = {'return_url': 'https://www.finehomebuilding.com/admin/content/content_list',
     'user_email': 'amrish.singh@gmail.com',
     'user_pass': 'Wookie01Linker'}
    s = requests.Session()
    #login in requests
    s.post(url, data=payload)
    should_continue = True
    print "Logged in"
    page = 1
    spam_words = """appetite suppressant
weight watchers
serotonin
metabolism
leptin
bmi
garcinia
fat loss
weight loss
fat
diet
lose weight
weight reduction
vitamin supplements
Basketball
soccer
football
PLAYOFF
Streaming
NFL
supplement
Natural Formula
LIVE STREAM
Basketall
full Movie
divx
xvid
onlinewatch
watchonline
college_football_logos
Full Online Free Movie
(2014) Online Movie
WATCH FREE FULL EPISODE
espn
thinfit""".lower().split("\n")
    tries = 0
    while should_continue:
        to_delete = 0
        response = s.get("https://www.finehomebuilding.com/admin/content/content_list/sort/post_modified/page/%s?sort_field=post_modified&sort_order=DESC" % page)
        soup = BeautifulSoup(response.content)
        try:
            posts = soup.find_all("tr", class_="bg-grey")
            posts.extend(soup.find_all("tr", class_="bg-white"))
            to_delete = len(posts)
            for post in posts:
                tds = post.find_all("td")
                delete_url = tds[-1].find_all("a")[0]["href"]
                if any(x in tds[4].text.lower() for x in spam_words):
                    payload={"delete":1}
                    print delete_url, s.post(delete_url, data=payload).status_code
                    to_delete -= 1
                else:
                    full_url = "https://www.finehomebuilding.com/item/%s" % tds[1].text.lower().strip()
                    response = s.get(full_url)
                    soup = BeautifulSoup(response.content)
                    body = soup.find("div", {"id": "left"})
                    try:
                        if any(x in body.text.lower() for x in ["watch-full-movie-online", "livesportspctv", "NCAA_on-line_lg.jpg".lower(), "Megashare".lower(), "Putlocker".lower(), "dailymotion", "Online Full Movie".lower(), "garcinia", "download full movie", "weight loss", "(2014) Online Movie".lower(), "college_football_logos", "WATCH FREE FULL EPISODE".lower()]):
                            payload={"delete":1}
                            print delete_url, s.post(delete_url, data=payload).status_code
                            to_delete -= 1
                    except:
                        pass
                        # print_stack_trace()
        except:
            print_stack_trace()
        print "Page",page,"To delete:",to_delete
        if to_delete > 0:
            tries += 1
            if tries > 4 or to_delete == 20:
                page += 1
                tries = 0
        else:
            tries = 0
        # if to_delete > 0:
        #     page += 1
        # if page > 100:
        #     should_continue = False


def del_chrome_driver():
    #Login Screen
    driver = webdriver.Chrome()
    driver.get("https://www.vegetablegardener.com/user/login")
    driver.find_element_by_name("user_email").send_keys("ssmith@taunton.com")
    driver.find_element_by_name("user_pass").send_keys("Taunton63")
    driver.find_element_by_name("user_pass").send_keys(Keys.RETURN)
    time.sleep(2)


    url = 'https://www.vegetablegardener.com/user/login'
    payload = {'return_url': 'https://www.vegetablegardener.com/admin/content/content_list',
     'user_email': 'ssmith@taunton.com',
     'user_pass': 'Taunton63'}
    s = requests.Session()
    #login in requests
    s.post(url, data=payload)



    should_continue = True
    page = 1
    while should_continue:
        driver.get("https://www.vegetablegardener.com/admin/content/content_list/sort/post_modified?sort_field=post_modified&sort_order=ASC&page=%s&search=&editor=0&author=&level=any&status=any&date=any&category=any&type=any&featured=any&comments=any&pool_ID=0" % page)
        try:
            posts = driver.find_elements_by_css_selector("tr.bg-grey")
            for post in posts:
                tds = post.find_elements_by_tag_name("td")
                if tds[3].text in ["12/18/2014", "12/17/2014", "12/19/2014"]:
                    should_continue = True
                    a = tds[-1].find_element_by_tag_name("a")
                    url = a.get_attribute("href")
                    payload={"delete":1}
                    #delete it
                    print url, s.post(url, data=payload).status_code
                # else:
                #     should_continue = False
            # driver.get("https://www.vegetablegardener.com/admin/content/content_list/page/%s" % page)
        except:
            pass
        # page +=1
        # try:
        #     while True:
        #         post = driver.find_elements_by_css_selector("tr.bg-grey")[0]
        #         tds = post.find_elements_by_tag_name("td")
        #         if tds[2].text == "12/18/2014" or tds[2].text == "12/17/2014" or tds[2].text == "12/19/2014"  :
        #             should_continue = True
        #             a = tds[-1].find_element_by_tag_name("a")
        #             url = a.get_attribute("href")
        #             payload={"delete":1}
        #             #delete it
        #             s.post(url, data=payload)
        #         #     a.click()
        #         #     input_button = driver.find_elements_by_css_selector("input.button-basic")[0]
        #         #     input_button.click()
        #         #     div = driver.find_elements_by_css_selector("div.preview-confirmation")[0]
        #         #     div.find_elements_by_tag_name('a')[0].click()
        #         # else:
        #             should_continue = False
        # except:
        #     pass
        # page +=1

    driver.close()

del_requests()