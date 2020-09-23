# -*- coding: utf-8 -*-
"""
Created on Thu Feb 27 11:01:51 2020

@author: Saraswat
"""

#The following programs crawls facebook to find user's friends and followed pages names and then store them in a csv file


from selenium import webdriver
#from selenium.webdriver.common.keys import Keys
import time
import pandas as pd


options= webdriver.ChromeOptions()
#Handling Web Push Notifications
# Pass the argument 1 to allow and 2 to block
options.add_experimental_option("prefs", { 
    "profile.default_content_setting_values.notifications": 2 
})
driver=webdriver.Chrome(chrome_options=options,executable_path='./chromedriver.exe')
driver.get('https://www.facebook.com/')

#Input Fields
username=driver.find_element_by_id('email')
username.send_keys('YOUR FACEBOOK EMAIL')

password=driver.find_element_by_id('pass')
password.send_keys('YOUR FACEBOOK PASSWORD')

#Login
loginBtn=driver.find_element_by_id('loginbutton')
loginBtn.click()

#Reach on friends page
#Replace url with url you want
url='YOUR FRIEND Friendlist URL. EXAMPLE-https://www.facebook.com/DUMMY_USER_USERNAME/friends'
driver.get(url)

#Scroll Functionality
pause_time=3
last_height=driver.execute_script("return document.body.scrollHeight")

while True:
    driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
    time.sleep(pause_time)
    new_height=driver.execute_script("return document.body.scrollHeight")
    
    if new_height==last_height:
        break
    else:
        last_height=new_height

#Getting friend names in a list
usernames=list()
usernames=driver.find_elements_by_class_name('fcb')
friend_names=list()
for name in usernames:
    friend_names.append(name.text)
#    print(name.text)

#Saving names in a csv
friend_names=[x for x in friend_names if x != '']
df=pd.DataFrame(friend_names,columns=['Names'])
df.to_csv('names.csv')

#print("Total Friends:",len(usernames))




