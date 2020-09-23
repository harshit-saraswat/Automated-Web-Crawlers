# -*- coding: utf-8 -*-
"""
Created on Fri Feb 28 19:06:47 2020

@author: acer
"""
from selenium import webdriver
import time
from bs4 import BeautifulSoup as bs
import re
import pandas as pd


options= webdriver.ChromeOptions()
#Handling Web Push Notifications
# Pass the argument 1 to allow and 2 to block
options.add_experimental_option("prefs", { 
    "profile.default_content_setting_values.notifications": 2 
})
driver=webdriver.Chrome(chrome_options=options,executable_path='./chromedriver.exe')
driver.get('https://www.linkedin.com/')

#Click Sign In button
signIn=driver.find_element_by_xpath('/html/body/nav/a[3]')
signIn.click()
time.sleep(1)

#Input Fields
username=driver.find_element_by_id('username')
username.send_keys('YOUR_EMAIL')

password=driver.find_element_by_id('password')
password.send_keys('YOUR_PASSWORD')

#Login
loginBtn=driver.find_element_by_xpath('//*[@id="app__container"]/main/div/form/div[3]/button')
loginBtn.click()
time.sleep(3)

#Go to connections
driver.get('https://www.linkedin.com/mynetwork/invite-connect/connections/')

#Scroll functionality
last_height = driver.execute_script("return document.body.scrollHeight")
while True:
    driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
    time.sleep(4)
    new_height=driver.execute_script("return document.body.scrollHeight")
    if new_height==last_height:
        break
    else:
        last_height=new_height
    print("New:",new_height)
    print("Last:",last_height)


#Setting up my network
page = bs(driver.page_source, features="html.parser")
content = page.find_all('a', {'class':"mn-connection-card__link ember-view"})

mynetwork = []
for contact in content:
    mynetwork.append(contact.get('href'))
print(len(mynetwork), " connections")

my_network_emails = []
contact_names=[]
contact_titles=[]
contact_locations=[]
# Connect to the profile of all contacts and save the email within a list
for contact in mynetwork:
    driver.get("https://www.linkedin.com" + contact)
    driver.implicitly_wait(3)
    
    name=driver.find_element_by_xpath('/html/body/div[5]/div[4]/div[3]/div/div/div/div/div[2]/main/div[1]/section/div[2]/div[2]/div[1]/ul[1]/li[1]')
    contact_names.append(name.text)
    
    title=driver.find_element_by_xpath('/html/body/div[5]/div[4]/div[3]/div/div/div/div/div[2]/main/div[1]/section/div[2]/div[2]/div[1]/h2')
    contact_titles.append(title.text)
    
    loc=driver.find_element_by_xpath('/html/body/div[5]/div[4]/div[3]/div/div/div/div/div[2]/main/div[1]/section/div[2]/div[2]/div[1]/ul[2]/li[1]')
    contact_locations.append(loc.text)
    
    driver.get("https://www.linkedin.com" + contact + "detail/contact-info/")
    driver.implicitly_wait(3)
#    name=driver.find_element_by_id('pv-contact-info')
    contact_page = bs(driver.page_source, features="html.parser")
    content_contact_page = contact_page.find_all('a',href=re.compile("mailto"))
    
    #If email desn't exist then add a NULL entry
    if len(content_contact_page)==0:
        my_network_emails.append('NULL')
    
    for contact in content_contact_page:
        print("[+]", contact.get('href')[7:])
        my_network_emails.append(contact.get('href')[7:])
    # wait few seconds before to connect to the next profile
    time.sleep(2)
    
#Saving details in a csv
df = pd.DataFrame(list(zip(contact_names, contact_titles,contact_locations,my_network_emails)), columns =['Name', 'Title', 'Location', 'Email'])
df.to_csv('data.csv',index=False) 
