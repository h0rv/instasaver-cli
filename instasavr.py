#!/usr/bin/python
import click
import os
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import urllib.request


@click.command()
@click.option('--username', prompt='Username', help='User with saved collection.')
@click.option('--password', prompt='Password', help="User\'s password.")
@click.option('--browser', prompt='Firefox or Chrome', default='Firefox', help="Browser for selenium.")
@click.option('--collection', prompt='Saved Collection Name', default='All Posts', help="User's saved collection name. Default is 'All Posts' collection.")
@click.option('--number', default=-1, help="Number of posts to save, starting from most recent. Default is all.")
def login(username, password, browser, collection, number):
    browser = browser.lower()
    if browser == 'firefox':
        driver = webdriver.Firefox()
    elif browser == 'chrome':
        driver = webdriver.Chrome()
    else:
        print('Invalid browser.')
        quit()

    driver.get("https://www.instagram.com/accounts/login/")
    time.sleep(5)

    username_input = driver.find_element_by_xpath('//*[@name="username"]')
    password_input = driver.find_element_by_xpath('//*[@name="password"]')

    username_input.send_keys(username)
    password_input.send_keys(password)

    # login
    password_input.send_keys(Keys.RETURN)
    time.sleep(3)
    logged_in_class = driver.find_elements_by_class_name("logged-in")

    # to check if logged-in
    print(len(logged_in_class))

    # if not logged in, exit
    if len(logged_in_class) == '0':
        driver.quit()

    driver.get("https://www.instagram.com/"+username+"/saved/")
    time.sleep(3)
    try:
        driver.find_element_by_xpath(
            "//*[text() = '" + collection + "']").click()
    except:
        print('Collection does not exist.')
        driver.quit()
        quit()
    time.sleep(3)

    # Get scroll height
    last_height = driver.execute_script("return document.body.scrollHeight")

    while True:
        # Scroll down to bottom
        driver.execute_script(
            "window.scrollTo(0, document.body.scrollHeight);")

        # Wait to load page
        time.sleep(3)

        # Calculate new scroll height and compare with last scroll height
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

    photos = driver.find_elements_by_class_name('FFVAD')
    # photos = driver.find_elements_by_xpath('//*[@class="FFVAD"]')
    time.sleep(3)
    x = 1
    try:
        os.mkdir('./images')
    except:
        print('./images directory already exists')
    for photo in photos:
        file_name = str(x) + '.jpg'
        urllib.request.urlretrieve(photo.get_attribute(
            'src'), './images/'+file_name)
        x = x + 1

    print('Download Successful.')
    driver.quit()
    quit()


if __name__ == '__main__':
    login()
