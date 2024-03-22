# coding=utf-8

# imports libraries of python
import re
from getpass import getpass
from time import sleep
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By

# configuration
NUM_SCROLLS = 10  # increase to load more data on search page
keywords = ["stock market Equity", "stock market Broker", "stock market Arbitrage", "stock market Trading",
            "Prediction", "Dividends", "stockmarket", "shear-market", "nifty", "banknifty", "investment", "intraday",
            "options trading"]
location = "Mumbai"


# setup browser
def setup_browser():
    global wd
    chrome_options = webdriver.ChromeOptions()
    prefs = {"profile.default_content_setting_values.notifications": 2}
    chrome_options.add_experimental_option("prefs", prefs)
    wd = webdriver.Chrome(options=chrome_options)


# Defining a function to check the validity of Xpath in the browser
def hasXpath(xpath):
    try:
        if wd.find_element(By.XPATH, xpath):
            return True
    except:
        return False


# Defining a function to check the validity of Xpath in the Post
def posthasXpath(xpath, post):
    try:
        if post.find_element(By.XPATH, xpath):
            return True
    except:
        return False


# Defining a function to check if facebook is logged in
def is_logged_in(driver):
    try:
        profile_svg_element = driver.find_element(By.XPATH, './/div[@aria-label="Account Controls and Settings"]')
        if profile_svg_element:
            return True
        else:
            return False
    except NoSuchElementException:
        return False


# Defining a function to extract text from html element
def get_text(element):
    pattern = re.compile('<.*?>')
    element_html = element.get_attribute("outerHTML")
    return pattern.sub(r'', element_html)


# Defining a function to login
def login():
    # Taking to the log-in page
    wd.get('https://www.facebook.com')

    # username and password
    usr = input('Enter username:\n')  # Username
    pas = getpass('Enter Password:\n')  # password

    # Locate username and password form by ID
    username = wd.find_element(By.ID, 'email')
    username.send_keys(usr)
    sleep(0.5)

    passw = wd.find_element(By.ID, 'pass')
    passw.send_keys(pas)
    sleep(0.5)

    # locate submit button by_xpath
    sign_in_button = wd.find_element(By.XPATH, '//*[@type="submit"]')
    sign_in_button.click()
    sleep(3)

    if is_logged_in(wd):
        print("logged in")
    else:
        print('log_in Error!!\nPlease login again.')
        login()


# Defining a function for initializing the search for a given keyword
def initialize_search(keyword, location):
    print("----------------------------xxxx----------------------------")
    print(f'Searching for {keyword}')
    # Open the file in write mode with the keyword provided
    global f
    f = open(location + "_" + keyword + "_facebook.txt", "a", encoding="utf-8")

    head = f"'post_no', 'post_type', 'is_text_only' ,'user_name', 'post_time','likes','num_coments','num_shares','post_content','Cmt_content','post_url'\n"
    f.write(head)

    # Entering search page for facebook with the keyword
    wd.get('https://www.facebook.com/search/posts?q=' + keyword)
    sleep(1)
    if hasXpath('.//input[@aria-label = "Tagged Location"]'):
        Location = wd.find_element(By.XPATH, './/input[@aria-label = "Tagged Location"]')
        Location.send_keys(location)
        sleep(1)
        if hasXpath('.//ul[@role = "listbox"]/li[@role="option"]'):
            first_option = wd.find_element(By.XPATH, './/ul[@role = "listbox"]/li[@role="option"]')
            first_option.click()

        else:
            print("opps")


def scroll_to_bottom(wd, num_scrolls=3):
    j = 0
    while j < num_scrolls:
        # Scroll down to bottom so as to load more content
        wd.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        sleep(2)
        j = j + 1
    sleep(2)


def scroll_into_view(element):
    wd.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)


def click_see_more(element):
    while hasXpath("//*[contains(text(), 'See more')]"):
        seemore_buttons = element.find_elements(By.XPATH, "//*[contains(text(), 'See more')]")
        print(len(seemore_buttons))
        for seemore_button in reversed(seemore_buttons):
            scroll_into_view(seemore_button)
            sleep(0.5)
            seemore_button.click()


def extract_post_content(post):
    post_content = ""
    post_texts = post.find_elements(By.XPATH, post_content_xpath)
    for post_text in post_texts:
        content = None
        content = get_text(post_text)
        post_content = post_content + content + " "
    return post_content


def extract_reels_info(post):
    # post_time for reels
    reel_date = post.find_element(By.XPATH, reel_date_xpath)
    post_time = get_text(reel_date)

    # link for reels
    if (posthasXpath(reels_link_xpath, post)):
        allp = post.find_element(By.XPATH, reels_link_xpath)
        post_url = allp.get_attribute("href")

    other_content = post.find_elements(By.XPATH,
                                       './/span[@class="x1lliihq x6ikm8r x10wlt62 x1n2onr6 xlyipyv xuxw1ft x1j85h84"]')
    content_text = ""
    for content in other_content:
        content_line = get_text(content)
        content_text = content_text + content_line + "\n"
    return post_time, post_url, content_text


def extract_interaction_data(post):
    likes, num_comments, num_shares = "", "", ""
    # No of likes for post
    if posthasXpath(likes_num_xpath, post):
        num_likes = post.find_element(By.XPATH, likes_num_xpath)
        likes = get_text(num_likes)

    # no. of comments and shares
    if posthasXpath(comment_num_xpath, post) and post_type != "reel":
        num_comments_element = post.find_elements(By.XPATH, comment_num_xpath)
        if len(num_comments_element) > 1:
            num_comments = get_text(num_comments_element[1])
        if len(num_comments_element) > 2:
            num_shares = get_text(num_comments_element[2])
    return likes, num_comments, num_shares


def open_comments_popup(post, post_type):
    try:
        if post_type != "reel":
            num_comments_elements = post.find_elements(By.XPATH, comment_num_xpath)
            if len(num_comments_elements) > 1 and posthasXpath('.//div[@role = "button"]', num_comments_elements[1]):
                button_element = num_comments_elements[1].find_element(By.XPATH, './/div[@role = "button"]')
                scroll_into_view(button_element)
                sleep(0.5)
                button_element.click()
                sleep(5)
                return True
        else:
            if posthasXpath('.//div[ @role="button" and @aria-label="Comment"]', post):
                button_element = post.find_element(By.XPATH, './/div[ @role="button" and @aria-label="Comment"]')
                scroll_into_view(button_element)
                sleep(0.5)
                button_element.click()
                sleep(5)
                return True

    except:
        print("Error clicking comments button")
    return False


def select_display_all_comments(wd):
    try:
        dropdown_button = wd.find_element(By.XPATH,
                                          './/div[@class = "x6s0dn4 x78zum5 xdj266r x11i5rnm xat24cr x1mh8g0r xe0p6wg"]/div[@role= "button"]')
        dropdown_button.click()
        sleep(0.5)
        all_comments_option = wd.find_element(By.XPATH,
                                              './/div[@role = "menu" and @class = "x1n2onr6 xcxhlts x1fayt1i"]//div[@class = "x78zum5 xdt5ytf x1iyjqo2 x1n2onr6"]/div/div[3]')
        all_comments_option.click()
        print("Successfully selected all comments")
        sleep(3)
        return True
    except:
        print("Error selecting all comments")
    return False


def view_all_replies(wd):
    try:
        while posthasXpath('.//div[@class="x78zum5 x1iyjqo2 x21xpn4 x1n2onr6"]/div[@role= "button"]', wd):
            view_reply_buttons = wd.find_elements(By.XPATH,
                                                  './/div[@class="x78zum5 x1iyjqo2 x21xpn4 x1n2onr6"]/div[@role= "button"]')
            print("Number of buttons detected:", len(view_reply_buttons))
            for view_reply_button in view_reply_buttons:
                scroll_into_view(view_reply_button)
                view_reply_button.click()
                sleep(0.5)
    except:
        print("Error finding view reply buttons")


def close_comments_popup():
    try:
        close_button_element = wd.find_element(By.XPATH, './/div[@role="button" and @aria-label="Close"]')
        close_button_element.click()
        print("Successfully closed comments popup")
        sleep(3)
        return True
    except:
        print("Error closing comments popup")
    return False


def get_comments(element):
    comments = element.find_elements(By.XPATH,
                                     './/div[@class="x1n2onr6 x1swvt13 x1iorvi4 x78zum5 x1q0g3np x1a2a7pz"] | .//div[@class="x1n2onr6 xurb0ha x1iorvi4 x78zum5 x1q0g3np x1a2a7pz"]')
    print(f"Found {len(comments)} comments")
    cmt_content = ""
    for x, comment_element in enumerate(comments):
        com_lines = ""

        cmt_details = comment_element.get_attribute("aria-label")
        if posthasXpath('.//div[@class="x1lliihq xjkvuk6 x1iorvi4"]/span/div/div', comment_element):
            comment_lines = comment_element.find_element(By.XPATH, './/div[@class="x1lliihq xjkvuk6 x1iorvi4"]')
            com_lines = get_text(comment_lines)

        #         cmt_content += f"comment_{x+1}:- {cmt_details}:- {cmt_user_name} : {com_lines} | \n "
        cmt_content += f"{x + 1}:- {cmt_details}:- {com_lines} | \n "

    return cmt_content


try:
    if is_logged_in(wd):
        print("Already logged in")
    else:
        login()

except:
    setup_browser()
    login()

fb_feed_xpath = '//div[@class="x193iq5w x1xwk8fm"]'
fb_artical_xpath = '//div[@class="x1a2a7pz"]'
general_u_name_xpath = './/span[@class="xt0psk2"]/a/strong/span'
group_post_u_name_xpath = './/span[@class="xt0psk2"]/a/span'
text_post_xpath = './/div[@class="xdj266r x11i5rnm xat24cr x1mh8g0r x1vvkbs"]'
reels_u_name_xpath = './/span[@class="x65f84u"]//a'
reels_link_xpath = './/div[@class="x1n2onr6"]/div[1]/div/a[@role = "link"]'
reel_date_xpath = './/span[@class="x4k7w5x x1h91t0o x1h9r5lt x1jfb8zj xv2umb2 x1beo9mf xaigb6o x12ejxvf x3igimt xarpa2k xedcshv x1lytzrv x1t2pt76 x7ja8zs x1qrby5j"]'
post_content_xpath = './/div[@class="xu06os2 x1ok221b"]/span/div/div'
likes_num_xpath = './/span[@class="x1e558r4"]'
comment_num_xpath = './/div[@class="x1n2onr6"]/div/div[2]/div'
comment_button_xpath = './/div[@class="x1n2onr6"]/div/div[2]/div/span/div[@role=button]'
link_url_xpath = './/a[@class = "x1i10hfl xjbqb8w x6umtig x1b1mbwd xaqea5y xav7gou x9f619 x1ypdohk xt0psk2 xe8uvvx xdj266r x11i5rnm xat24cr x1mh8g0r xexx8yu x4uap5 x18d9i69 xkhd6sd x16tdsg8 x1hl2dhg xggy1nq x1a2a7pz x1heor9g xt0b8zv xo1l8bm" and @role = "link" and @tabindex="0"]'

for i in range(0, len(keywords)):
    initialize_search(keywords[i], location)

    scroll_to_bottom(wd, NUM_SCROLLS)
    sleep(2)
    try:
        click_see_more(wd)
    except Exception as e:
        print(f"An error occurred: {e}")

    # --------------------------------xxxxxx----------------------------------------

    if hasXpath(fb_feed_xpath):  # xpath for facebbok feed:

        posts = wd.find_elements(By.XPATH, fb_artical_xpath)  # xpath for facebbok artical:
        print(f'has {len(posts)}  post')
        sleep(5)
        for post_no, post in enumerate(posts):
            print('\n\n----------xx----------')
            print(f'\nlooking inside post no: {post_no} ')

            post_type, is_text_only = "Unknown", 0
            user_name, post_time, likes, num_comments, num_shares, post_content, Cmt_content, post_url = "", "", "", "", "", "", "", ""

            # Taking the user name from the post with the Xpath provided
            if posthasXpath(general_u_name_xpath, post):
                post_type = "general"
                name = post.find_element(By.XPATH, general_u_name_xpath)
                user_name = get_text(name)
                likes, num_comments, num_shares = extract_interaction_data(post)

            if posthasXpath(group_post_u_name_xpath, post):
                post_type = "group_post"
                name = post.find_element(By.XPATH, group_post_u_name_xpath)
                user_name = get_text(name)
                likes, num_comments, num_shares = extract_interaction_data(post)

            if posthasXpath(reels_u_name_xpath, post):
                post_type = "reel"
                name = post.find_element(By.XPATH, reels_u_name_xpath)
                user_name = get_text(name)
                post_time, post_url, post_content = extract_reels_info(post)
                if open_comments_popup(post, post_type):
                    if select_display_all_comments(wd):
                        view_all_replies(wd)
                    if hasXpath(
                            './/div[@class="x1n2onr6 x1swvt13 x1iorvi4 x78zum5 x1q0g3np x1a2a7pz" and @role="article"]'):
                        Cmt_content = get_comments(wd)

                    close_comments_popup()

            # post_content
            if posthasXpath(post_content_xpath, post):
                post_texts = post.find_elements(By.XPATH, post_content_xpath)
                for post_text in post_texts:
                    content = get_text(post_text)
                    post_content = post_content + content + " "

            if posthasXpath(text_post_xpath, post):
                is_text_only = 1
                post_text = post.find_element(By.XPATH, text_post_xpath)
                post_content = get_text(post_text)

                # links and post_times for other post
            if posthasXpath('.//a[@role = "link" and @tabindex="0"]', post) and post_type != 'reel':
                all_a_s = post.find_elements(By.XPATH, './/a[@role = "link" and @tabindex="0"]')  # Find all a elements
                post_url = all_a_s[-3].get_attribute("href")
                for a_no, a_s in enumerate(all_a_s):
                    a_s_html = a_s.get_attribute("outerHTML")
                    svg_id = re.search(r'href="#SvgT(\d)" ', a_s_html)
                    if svg_id:
                        svg = int(svg_id.group(1))
                        date = wd.find_elements(By.ID, f"SvgT{svg}")
                        post_time = get_text(date[0])
                        print(f'time in svg {a_no}: {post_time}')

            if posthasXpath(comment_num_xpath, post) and post_type != "reel":
                if open_comments_popup(post, post_type):
                    if select_display_all_comments(wd):
                        view_all_replies(wd)

                    if hasXpath(
                            './/div[@class="x1n2onr6 x1swvt13 x1iorvi4 x78zum5 x1q0g3np x1a2a7pz" and @role="article"]'):
                        Cmt_content = get_comments(wd)

                    close_comments_popup()

            to_write = f"'post_{post_no}:', '{post_type}','{is_text_only}' ,'{user_name}', '{post_time}','{likes}','{num_comments}','{num_shares}' ,'{post_content}','{Cmt_content}','{post_url}'\n"
            print(
                f"'post_{post_no}:',\nPost_type:\t\t'{post_type}',\nis_text_only:\t\t{is_text_only},\nUserName:\t\t'{user_name}',\nPost_time:\t\t'{post_time}',\nnum_likes:\t\t'{likes}',\nnumber_comments:\t'{num_comments}',\nnum_shares:\t\t'{num_shares}'  ,\nPost_content:\t'{post_content}',\nComments:\t'{Cmt_content}'\n\n")
            cleaned_text = to_write.replace("\n", "  ").replace("\t", "  ").replace("\\", "  ")
            f.write(f'{cleaned_text} \n')



