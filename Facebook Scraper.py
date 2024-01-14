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
from selenium.webdriver.common.keys import Keys
from time import sleep
from getpass import getpass
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
pas = getpass('Enter Password:\n')  # password
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
keyword = ["keywords"]

# For loop for multiple keywords
for i in range(0, len(keyword)):

    print("----------------------------xxxx---------------------------")
    print(f'Searching for {keyword[i]}')

    # Open the file in write mode with the keyword provided
    f = open(keyword[i] + "_facebook.txt", "w", encoding="utf-8")

    # Entering search page for facebook with the keyword
    wd.get('https://www.facebook.com/search/posts?q=' + keyword[i])
    head = f"'post_no', 'post_type' ,'user_name', 'post_time','likes','num_coments','post_content','Cmt_content','post_url'\n"
    f.write(head)

    j = 0
    # Value of J determines how much time scrolling happens to the bottom of page
    while j < 30:
        # Scroll down to bottom so as to load more content
        wd.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        sleep(2)
        j = j + 1

    sleep(15)

    # --------------------------------xxxxxx------------------------------------------

    if hasXpath('//div[@class="x193iq5w x1xwk8fm"]'):  # expath for facebbok feed:
        print("has feed")

        posts = wd.find_elements(By.XPATH, '//div[@class="x1a2a7pz"]')  # xpath for facebbok artical: x1a2a7pz
        print(f'has {len(posts)}  post')
        for post_no, post in enumerate(posts):
            print('\n\n----------xx----------')
            print(f'\nlooking inside post no: {post_no} ')
            post_type = "Unknown"
            user_name, post_time, likes, num_coments, post_content, Cmt_content, post_url = "", "", "", "", "", "", ""
            # Taking the user name from the post with the Xpath provided
            if posthasXpath('.//span[@class="xt0psk2"]/a/strong/span', post):
                print("is general post")
                post_type = "general"
                name = post.find_element(By.XPATH, './/span[@class="xt0psk2"]/a/strong/span')
                #                 user_name = name.text
                #                 if not user_name:
                Element_HTML = name.get_attribute("outerHTML")
                user_name = Element_HTML.strip("</span>")
                print(f"user_name: {user_name}")

            if posthasXpath('.//span[@class="xt0psk2"]/a/span', post):
                print("is group post")
                post_type = "group_post"
                name = post.find_element(By.XPATH, './/span[@class="xt0psk2"]/a/span')
                #                 user_name = name.text
                #                 if not user_name:
                Element_HTML = name.get_attribute("outerHTML")
                user_name = Element_HTML.strip("</span>")
                print(f"user_name: {user_name}")

            if posthasXpath('.//div[@class="xdj266r x11i5rnm xat24cr x1mh8g0r x1vvkbs"]', post):
                print("is text")
                post_text = post.find_element(By.XPATH, './/div[@class="xdj266r x11i5rnm xat24cr x1mh8g0r x1vvkbs"]')
                post_content = post_text.text
                if not post_content:
                    post_content = post_text.get_attribute("outerHTML")
                print(content)

            if posthasXpath('.//span[@class="x65f84u"]', post):
                print("is reel")
                post_type = "reel"
                name = post.find_element(By.XPATH, './/span[@class="x65f84u"]//a')
                #                 user_name = name.text
                #                 if not user_name:
                Element_HTML = name.get_attribute("outerHTML")
                user_name = re.search(r'target="_blank">(.*?)</span>', Element_HTML)
                if user_name:
                    user_name = user_name.group(1)
                elif not user_name:
                    user_name = re.search(r'target="_blank">(.*?)</a>', Element_HTML)
                    user_name = user_name.group(1)
                print(f"Username: {user_name}")

                # post_time for reels
                reel_date = post.find_element(By.XPATH,
                                              './/span[@class="x4k7w5x x1h91t0o x1h9r5lt x1jfb8zj xv2umb2 x1beo9mf xaigb6o x12ejxvf x3igimt xarpa2k xedcshv x1lytzrv x1t2pt76 x7ja8zs x1qrby5j"]')
                Element_HTML = reel_date.get_attribute("outerHTML")
                post_time = re.search(r'x1qrby5j">(.*?)</span>', Element_HTML).group(1)

                # link for reels
                if (posthasXpath('.//div[@class="x1n2onr6"]/div[1]/div/a[@role = "link"]', post)):
                    allp = post.find_element(By.XPATH, './/div[@class="x1n2onr6"]/div[1]/div/a[@role = "link"]')
                    post_url = allp.get_attribute("href")
                    print("url: ", post_url)

                other_content = post.find_elements(By.XPATH,
                                                   './/span[@class="x1lliihq x6ikm8r x10wlt62 x1n2onr6 xlyipyv xuxw1ft x1j85h84"]')
                for content in other_content:
                    print("reel_content: ", content.get_attribute("outerHTML"))

            # No of likes for post
            if posthasXpath('.//span[@class="x1e558r4"]', post):
                No_likes = post.find_element(By.XPATH, './/span[@class="x1e558r4"]')
                #                 likes = No_likes.text
                #                 if not likes:
                Element_HTML = No_likes.get_attribute("outerHTML")
                likes = re.search(r'<span class="x1e558r4">(.*?)</span>', Element_HTML).group(1)
                print(f'{likes} likes')

            # content of no. of comments and shears
            if posthasXpath(
                    './/div[@role = "button" and @class = "x1i10hfl x1qjc9v5 xjqpnuy xa49m3k xqeqjp1 x2hbi6w x1ypdohk xdl72j9 x2lah0s xe8uvvx x2lwn1j xeuugli x1hl2dhg xggy1nq x1t137rt x1o1ewxj x3x9cwd x1e5q0jg x13rtm0m x3nfvp2 x1q0g3np x87ps6o x1a2a7pz xjyslct xjbqb8w x13fuv20 xu3j5b3 x1q0q8m5 x26u7qi x972fbf xcfux6l x1qhh985 xm0m39n x9f619 x1heor9g xdj266r x11i5rnm xat24cr x1mh8g0r xexx8yu x4uap5 x18d9i69 xkhd6sd x1n2onr6 x16tdsg8 x1ja2u2z xt0b8zv"]/span',
                    post):
                No_coments = post.find_elements(By.XPATH,
                                                './/div[@role = "button" and @class= "x1i10hfl x1qjc9v5 xjqpnuy xa49m3k xqeqjp1 x2hbi6w x1ypdohk xdl72j9 x2lah0s xe8uvvx x2lwn1j xeuugli x1hl2dhg xggy1nq x1t137rt x1o1ewxj x3x9cwd x1e5q0jg x13rtm0m x3nfvp2 x1q0g3np x87ps6o x1a2a7pz xjyslct xjbqb8w x13fuv20 xu3j5b3 x1q0q8m5 x26u7qi x972fbf xcfux6l x1qhh985 xm0m39n x9f619 x1heor9g xdj266r x11i5rnm xat24cr x1mh8g0r xexx8yu x4uap5 x18d9i69 xkhd6sd x1n2onr6 x16tdsg8 x1ja2u2z xt0b8zv"]/span')
                num_coments = ""
                for x in No_coments:
                    coments = x.text
                    if not coments:
                        coments = x.get_attribute("outerHTML")
                    num_coments = num_coments + coments + " "
                print(num_coments)

            if posthasXpath('.//div[@class="xu06os2 x1ok221b"]/span/div/div', post):
                post_texts = post.find_elements(By.XPATH, './/div[@class="xu06os2 x1ok221b"]/span/div/div')
                print("--------")
                print("post_text:")
                for post_text in post_texts:
                    content = post_text.text
                    if not content:
                        Element_HTML = post_text.get_attribute("outerHTML")
                        print(Element_HTML)
                    #                         match = re.search(r'text-align: start;">(.*?)</div>', Element_HTML)
                    #                         if match:
                    #                             content = match.group(1)
                    #                         else:
                    #                             match = re.search(r'text-align: start;">(.*?)<span', Element_HTML)
                    #                             if match:
                    #                                 content = match.group(1)
                    print(content)
                    post_content = post_content + content + " "

            # links and post_times for other post
            if posthasXpath(
                    './/a[@class = "x1i10hfl xjbqb8w x6umtig x1b1mbwd xaqea5y xav7gou x9f619 x1ypdohk xt0psk2 xe8uvvx xdj266r x11i5rnm xat24cr x1mh8g0r xexx8yu x4uap5 x18d9i69 xkhd6sd x16tdsg8 x1hl2dhg xggy1nq x1a2a7pz x1heor9g xt0b8zv xo1l8bm" and @role = "link" and @tabindex="0"]',
                    post):
                all_a_s = post.find_elements(By.TAG_NAME, 'a')  # Find all a elements
                post_url = all_a_s[-3].get_attribute("href")
                print("url: ", post_url)
                total_a = len(all_a_s)
                if total_a > 4:
                    a_s = all_a_s[4].get_attribute("outerHTML")
                    svg_id = re.search(r'<use xlink:href="#SvgT(\d)" xmlns:xlink="http://www.w3.org/1999/xlink"></use>',
                                       a_s)
                    if svg_id:
                        svg = int(svg_id.group(1))
                        date = wd.find_elements(By.ID, f"SvgT{svg + 1}")
                        Element_HTML = date[0].get_attribute("outerHTML")
                        post_time = re.search(r'visible;">(.*?)</text>', Element_HTML)
                        if post_time:
                            post_time = post_time.group(1)
                            print("Post Time : ", post_time)
                    if not svg_id:
                        a_s = all_a_s[3].get_attribute("outerHTML")
                        svg_id = re.search(
                            r'<use xlink:href="#SvgT(\d)" xmlns:xlink="http://www.w3.org/1999/xlink"></use>', a_s)
                        if svg_id:
                            svg = int(svg_id.group(1))
                            date = wd.find_elements(By.ID, f"SvgT{svg + 1}")
                            Element_HTML = date[0].get_attribute("outerHTML")
                            post_time = re.search(r'# visible;">(.*?)</text>', Element_HTML)
                            if post_time:
                                post_time = post_time.group(1)
                                print("Post Time : ", post_time)

            print('opening url')
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
                    sleep(3)
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
                    Cmt_content = ""
                    for x, y in enumerate(comments):
                        try:
                            commenter_name = y.find_element(By.XPATH, './/span[@class = "x3nfvp2"]/span')
                            cmt_user_name = commenter_name.text
                        except:
                            cmt_user_name = "is_top_fan"
                        if posthasXpath('.//div[@class= "x1lliihq xjkvuk6 x1iorvi4"]/span/div/div', y):
                            comment_lines = y.find_elements(By.XPATH,
                                                            './/div[@class= "x1lliihq xjkvuk6 x1iorvi4"]/span/div/div')
                            com_lines = ""
                            for line in comment_lines:
                                line_text = line.text
                                com_lines = com_lines + line_text
                        Cmt_content = Cmt_content + f" comment_{x + 1}, {cmt_user_name} : {com_lines} | "
                    print(Cmt_content)

                    # Close the new tab
                wd.close()
                # Switch back to the original tab
                original_tab = wd.window_handles[0]
                wd.switch_to.window(original_tab)

            to_write = f"'post_{post_no}:', '{post_type}' ,'{user_name}', '{post_time}','{likes}','{num_coments.strip()}','{post_content}','{Cmt_content}','{post_url}'\n"
            clean_text = to_write.replace("\n", "  ").replace("\t", "  ")
            f.write(f'{clean_text} \n')


