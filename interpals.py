#!/usr/bin/env python
import tkinter as tk
import time
import sys
import os
import requests
import re
import random
import getpass
import lxml.html
from tkinter import ttk
from tkinter import *
from lxml.html import fromstring
from selenium.webdriver import Firefox
from selenium import webdriver
from selenium.webdriver.firefox.options import Options

##
## CONFIG VARIABLES : YOU CAN EDIT THESE VARIABLES TO CHANGE TIMER VALUES ##
##
MIN_DELAY_BETWEEN_PROFILE_VIEWS = 1
MAX_DELAY_BETWEEN_PROFILE_VIEWS = 5
DELAY_BETWEEN_RUNS = 10

login = 'login' # EDIT
password = 'password' # EDIT
sex = 'female' # Possible values: 'male', 'female', or empty '' for both
cont = 'EU' # Possible values: 'AF' (Africa) 'AS' (Asia), 'EU' (Europe)
            #'NA' (North America), 'OC' (Oceania), 'SA' (South America)
age1 = '15' # minimum age
age2 = '22' # maximum age
message = 'message' # message to send
sending = 0 # send mesaage for all found users
sending2 = 0 # send mesaage only for users from needful_city
needful_city = 'Krasnodar'

visitedUsersFilename = "users_visited.txt"
DEBUG = True

###############################################################################

opts = Options()
opts.set_headless()
assert opts.headless
browser = webdriver.Firefox(executable_path='geckodriver', options=opts)
sessioncount = 0
run_number = 1
f = open(visitedUsersFilename, 'a+')
processedUsers = [line.strip() for line in f]
print ("Logging in...")
browser.get("https://www.interpals.net/")
time.sleep(10)
LogInp = browser.find_element_by_id("topLoginEmail")
PasInp = browser.find_element_by_id("topLoginPassword")
Button = browser.find_element_by_xpath('//td/input[@type="submit"]')
LogInp.send_keys(login)
PasInp.send_keys(password)
Button.click()
time.sleep(5)
if not browser.find_elements_by_class_name("msg_error"):
    print ("Logged in: Starting the dance \o/")
    time.sleep(2)
    while True:
        runcount = 0
        if DEBUG:
            print ("Fetching online users page...")
        link = str('https://www.interpals.net/app/online?sex='+sex+'&continents%5B%5D='+cont+'&age1='+age1+'&age2='+age2+'&csrf_token=NGE1Y2I3YjA%3D')
        browser.get(link)
        data = browser.page_source
        tree = lxml.html.fromstring(data)
        usernames = tree.xpath('.//div[@class="online_prof"]//div[@class="olUserDetails"]//span[1]/a/@href')
        print(usernames)
        f = open(visitedUsersFilename,'w')
        for username in usernames:
            if username not in processedUsers:
                if DEBUG:
                    print ("Visiting profile of " + username + " (" + str(sessioncount) + ")")
                runcount += 1
                sessioncount += 1
                browser.get("https://www.interpals.net" + username)
                waitTime = random.randrange(MIN_DELAY_BETWEEN_PROFILE_VIEWS*10, MAX_DELAY_BETWEEN_PROFILE_VIEWS*10) / float(10)
                if (sending == 1)&(not browser.find_elements_by_class_name("msg_error")):
                    data = browser.page_source
                    tree = lxml.html.fromstring(data)
                    MesLink = tree.xpath('//div[@id="prof-action-links"]//a[1]/@href')
                    browser.get('https://www.interpals.net'+str(MesLink)[2:len(MesLink)-3])
                    time.sleep(2)
                    MesInp = browser.find_element_by_id("message")
                    MesBut = browser.find_element_by_id("msg_submit")
                    MesInp.send_keys(message)
                    MesBut.click()
                    time.sleep(1)
                elif (sending2 == 1)&(not browser.find_elements_by_class_name("msg_error")):
                    data = browser.page_source
                    tree = lxml.html.fromstring(data)
                    city = tree.xpath('//div[@class="profDataTopData"]//div//a[1]/text()')
                    print(str(city))
                    if needful_city in str(city):
                        MesLink = tree.xpath('//div[@id="prof-action-links"]//a[1]/@href')
                        browser.get('https://www.interpals.net'+str(MesLink)[2:len(MesLink)-3])
                        time.sleep(2)
                        MesInp = browser.find_element_by_id("message")
                        MesBut = browser.find_element_by_id("msg_submit")
                        MesInp.send_keys(message)
                        MesBut.click()
                        print('Отправлено сообщение.')
                        time.sleep(1)
                if DEBUG:
                    print ("Waiting " + str(waitTime) + "s")
                else:
                    os.system('cls' if os.name=='nt' else 'clear')
                    print ('\rRun %d - Fetched %d users (%d total)' % (run_number, runcount, sessioncount))
                time.sleep(waitTime)
                processedUsers.append(username)
                f.write(username + "\n")
            elif DEBUG:
                print ("Already visited " + username)
        run_number += 1
        if (runcount < 20):
            print ('[-] Waiting (%d)s before next run (fetched %d users this run, %d total)\n' % (DELAY_BETWEEN_RUNS * 4, runcount, sessioncount))
            time.sleep(DELAY_BETWEEN_RUNS * 4)
        else:
            print ('[+] Waiting (%d)s before next run (fetched %d users this run, %d total)\n' % (DELAY_BETWEEN_RUNS, runcount, sessioncount))
            time.sleep(DELAY_BETWEEN_RUNS)
else:
    print('Invalid login or password!')
    browser.quit()
    sys.exit()
