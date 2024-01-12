# coding=utf-8
# imports libraries of python
from PIL import Image
import pytesseract
from pytesseract import image_to_string
import requests
from io import BytesIO
import sys
import re
from selenium.common.exceptions import NoSuchElementException
from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep
import time


# Defining a function to check the validity of Xpath in the browser
def hasXpath(xpath):
    try:
        if wd.find_element(By.XPATH, xpath):
            return True
    except:
        return False

def posthasXpath(xpath,post):
    try:
        if post.find_element(By.XPATH, xpath):
            return True
    except:
        return False

chrome_options = webdriver.ChromeOptions()
prefs = {"profile.default_content_setting_values.notifications": 2}
chrome_options.add_experimental_option("prefs", prefs)

wd = webdriver.Chrome(options=chrome_options)

# username and password
# Please enter valid credentials
# Do not disclose it to anyone
usr = input('Enter username:\n')  # Username
pas = input('Enter Password:\n')  # password
# Taking to the log-in page
wd.get('https://www.facebook.com')


username = wd.find_element(By.ID, 'email')
username.send_keys(usr)
sleep(0.5)

# Locate password form by ID
passw = wd.find_element(By.ID, 'pass')
passw.send_keys(pas)
sleep(0.5)

# locate submit button by_xpath
sign_in_button = wd.find_element(By.XPATH, '//*[@type="submit"]')
sign_in_button.click()
print("logged in")
sleep(10)
keyword = ["Keywords"]

# For loop for multiple keywords
for i in range(0, len(keyword)):

    print("----------------------------xxxx---------------------------")
    print(f'Searching for {keyword[i]}')

    # Open the file in write mode with the keyword provided
    f = open(keyword[i] + "_facebook.txt", "wb")

    # Entering search page for facebook with the keyword
    wd.get('https://www.facebook.com/search/posts?q=' + keyword[i])

    j = 0
    # Value of J determines how much time scrolling happens to the bottom of page
    while j < 5:
        # Scroll down to bottom so as to load more content
        wd.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        sleep(1)
        j = j + 1

    sleep(5)

    if hasXpath('//div[@class="x193iq5w x1xwk8fm"]'):  # expath for facebbok feed:
        print("has feed")
        posts = wd.find_elements(By.XPATH, '//div[@class="x1a2a7pz"]')  # xpath for facebbok artical: x1a2a7pz
        print(f'has {len(posts)}  post')
        for post_no, post in enumerate(posts):
            print('\n\n----------xx----------')
            print(f'\nlooking inside post no: {post_no} ')

            # Taking the user name from the post with the Xpath provided
            if posthasXpath('.//span[@class="xt0psk2"]/a/strong/span', post):
                print("is general post")
                name = post.find_element(By.XPATH, './/span[@class="xt0psk2"]/a/strong/span')
                user_name = name.text
                if not user_name:
                    Element_HTML = name.get_attribute("outerHTML")
                    user_name = Element_HTML.strip("</span>")
                    print("html post")
                print(f"user_name: {user_name}")

            if posthasXpath('.//span[@class="xt0psk2"]/a/span', post):
                print("is group post")
                name = post.find_element(By.XPATH, './/span[@class="xt0psk2"]/a/span')
                user_name = name.text
                if not user_name:
                    Element_HTML = name.get_attribute("outerHTML")
                    user_name = Element_HTML.strip("</span>")
                print(f"user_name: {user_name}")

            if posthasXpath('.//span[@class="x65f84u"]', post):
                print("is reel")
                username_element = post.find_element(By.XPATH, './/span[@class="x65f84u"]//a')
                username = username_element.text
                if not user_name:
                    Element_HTML = name.get_attribute("outerHTML")
                    user_name = Element_HTML.strip("</span>")
                print(f"Username: {username}")

            # No of likes for post
            if posthasXpath('.//span[@class="x1e558r4"]', post):
                No_likes = post.find_element(By.XPATH, './/span[@class="x1e558r4"]')
                likes = No_likes.text
                if not likes:
                    Element_HTML = No_likes.get_attribute("outerHTML")
                    likes = re.search(r'<span class="x1e558r4">(.*?)</span>', Element_HTML).group(1)
                print(f'{likes} likes')

            # content of no. of comments and shears
            if posthasXpath(
                    './/div[@role = "button" and @class = "x1i10hfl x1qjc9v5 xjqpnuy xa49m3k xqeqjp1 x2hbi6w x1ypdohk xdl72j9 x2lah0s xe8uvvx x2lwn1j xeuugli x1hl2dhg xggy1nq x1t137rt x1o1ewxj x3x9cwd x1e5q0jg x13rtm0m x3nfvp2 x1q0g3np x87ps6o x1a2a7pz xjyslct xjbqb8w x13fuv20 xu3j5b3 x1q0q8m5 x26u7qi x972fbf xcfux6l x1qhh985 xm0m39n x9f619 x1heor9g xdj266r x11i5rnm xat24cr x1mh8g0r xexx8yu x4uap5 x18d9i69 xkhd6sd x1n2onr6 x16tdsg8 x1ja2u2z xt0b8zv"]/span',
                    post):
                No_coments = post.find_elements(By.XPATH,
                                                './/div[@role = "button" and @class= "x1i10hfl x1qjc9v5 xjqpnuy xa49m3k xqeqjp1 x2hbi6w x1ypdohk xdl72j9 x2lah0s xe8uvvx x2lwn1j xeuugli x1hl2dhg xggy1nq x1t137rt x1o1ewxj x3x9cwd x1e5q0jg x13rtm0m x3nfvp2 x1q0g3np x87ps6o x1a2a7pz xjyslct xjbqb8w x13fuv20 xu3j5b3 x1q0q8m5 x26u7qi x972fbf xcfux6l x1qhh985 xm0m39n x9f619 x1heor9g xdj266r x11i5rnm xat24cr x1mh8g0r xexx8yu x4uap5 x18d9i69 xkhd6sd x1n2onr6 x16tdsg8 x1ja2u2z xt0b8zv"]/span')
                #                 print("No Comment and shares")
                for x in No_coments:
                    coments = x.text
                    print(coments)
                    if not coments:
                        print(x.get_attribute("outerHTML"))

            # link for reels
            if (posthasXpath('.//div[@class="x1n2onr6"]/div[1]/div/a[@role = "link"]', post)):
                allp = post.find_element(By.XPATH, './/div[@class="x1n2onr6"]/div[1]/div/a[@role = "link"]')
                post_url = allp.get_attribute("href")
                print("url: ", post_url)

            # links for other post
            if posthasXpath(
                    './/a[@class = "x1i10hfl xjbqb8w x6umtig x1b1mbwd xaqea5y xav7gou x9f619 x1ypdohk xt0psk2 xe8uvvx xdj266r x11i5rnm xat24cr x1mh8g0r xexx8yu x4uap5 x18d9i69 xkhd6sd x16tdsg8 x1hl2dhg xggy1nq x1a2a7pz x1heor9g xt0b8zv xo1l8bm" and @role = "link" and @tabindex="0"]',
                    post):
                allps = post.find_elements(By.TAG_NAME, 'a')
                #                 for allp in allps:
                post_url = allps[-3].get_attribute("href")
                print("url: ", post_url)

            print('opening url')
            sleep(5)
            if post_url:
                # Open a new tab
                wd.execute_script("window.open();")
                # Switch to the newly opened tab
                new_tab = wd.window_handles[-1]
                wd.switch_to.window(new_tab)
                wd.get(post_url)
                print("new link loaded")
                sleep(5)
                try:
                    button_element = wd.find_element(By.XPATH,
                                                     './/div[@class = "x6s0dn4 x78zum5 xdj266r x11i5rnm xat24cr x1mh8g0r xe0p6wg"]/div[@role= "button"]')
                    button_element.click()
                    sleep(0.5)
                except:
                    print("it had error 1")
                try:
                    button_element = wd.find_element(By.XPATH,
                                                     './/div[@role = "menu" and @class = "x1n2onr6 xcxhlts x1fayt1i"]//div[@class = "x78zum5 xdt5ytf x1iyjqo2 x1n2onr6"]/div/div[3]')
                    button_element.click()
                    print("sucses")
                    sleep(2)
                except:
                    print("it had error 2")
                try:
                    button_element = wd.find_element(By.XPATH,
                                                     './/span[@class = "x78zum5 x1iyjqo2 x21xpn4 x1n2onr6"]/div[@role ="button"]')
                    button_element.click()
                    print("sucses")
                    sleep(5)
                except:
                    print("it had error 3")

                if hasXpath('//div[@class="x1n2onr6 x1swvt13 x1iorvi4 x78zum5 x1q0g3np x1a2a7pz" and @role="article"]'):
                    comments = wd.find_elements(By.XPATH,
                                                '//div[@class="x1n2onr6 x1swvt13 x1iorvi4 x78zum5 x1q0g3np x1a2a7pz" and @role="article"]')
                    print(f"has {len(comments)} comments")
                    for x, y in enumerate(comments):
                        print(f"\ncomment {x}")
                        commenter_name = y.find_element(By.XPATH, './/span[@class = "x3nfvp2"]/span')
                        print(f"{commenter_name.text} :")
                        if posthasXpath('.//div[@class= "x1lliihq xjkvuk6 x1iorvi4"]/span/div/div', y):
                            comment_lines = y.find_elements(By.XPATH,
                                                            './/div[@class= "x1lliihq xjkvuk6 x1iorvi4"]/span/div/div')
                            for line in comment_lines:
                                line_text = line.text
                                print(f"{line_text}")

                sleep(5)
                # Close the new tab
                wd.close()
                # Switch back to the original tab
                original_tab = wd.window_handles[0]
                wd.switch_to.window(original_tab)

            # post text content
            if posthasXpath('.//div[@class="xu06os2 x1ok221b"]/span/div/div', post):
                post_texts = post.find_elements(By.XPATH, './/div[@class="xu06os2 x1ok221b"]/span/div/div')
                print("--------")
                print("post_text:")
                for post_text in post_texts:
                    content = post_text.text
                    print(content)

