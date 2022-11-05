from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from time import sleep


def sendkeys(keys, css_selector, wait_time=10):
    cnt = 1
    while True:
        try:
            element = WebDriverWait(driver, wait_time).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, css_selector)))
            element.send_keys(keys)
            break
        except:
            if cnt > 3:
                print('\nNão foi possível interagir com o elemento %s' % css_selector)
                raise Exception('sendkeys fail.')

            else:
                print('\nNão foi possível enviar comandos (%d) para o elemento \n'
                      '%s. \nTentando novamente...' % (cnt, css_selector))
                cnt += 1
                continue


def click(css_selector, wait_time=10):
    cnt = 1
    while True:
        try:
            element = WebDriverWait(driver, wait_time).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, css_selector)))
            element.click()
            break
        except:
            if cnt > 3:
                print('\nNão foi possível interagir com o elemento %s' % css_selector)
                raise Exception('click fail.')
            else:
                print('\nNão foi possível enviar comandos (%d) para o elemento \n'
                      '%s. \nTentando novamente...' % (cnt, css_selector))
                cnt += 1
                continue


def clicktext(text_selector, wait_time=10):
    cnt = 1
    while True:
        try:
            element = WebDriverWait(driver, wait_time).until(
                EC.element_to_be_clickable((By.LINK_TEXT, text_selector)))
            element.click()
            break
        except:
            if cnt > 3:
                print('\nNão foi possível interagir com o elemento %s' % text_selector)
                raise Exception('click_text fail.')
            else:
                print('\nNão foi possível enviar comandos (%d) para o elemento \n'
                      '%s. \nTentando novamente...' % (cnt, text_selector))
                cnt += 1
                continue


def wait4element(css_selector, wait_time=10):
    try:
        element = WebDriverWait(driver, wait_time).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, css_selector)))
        sleep(0.25)
        return element

    except:
        return 0


def wait4text(text_selector, wait_time=10):
    try:
        element = WebDriverWait(driver, wait_time).until(
            EC.presence_of_element_located((By.LINK_TEXT, text_selector)))
        sleep(0.25)
        return element
    except:
        return 0


def wait4elements(css_selector, wait_time=10):
    if wait_time == 0:
        element = driver.find_elements(By.CSS_SELECTOR, css_selector)
        return element
    try:
        element = WebDriverWait(driver, wait_time).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, css_selector)))
        sleep(0.25)
        return element

    except:
        return []


def wait4click(css_selector, wait_time=10):
    try:
        element = WebDriverWait(driver, wait_time).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, css_selector)))
        sleep(0.25)
        return element

    except:
        return []


def wait4element2disappear(css_selector: str, wait_time=3):
    while wait4element(css_selector, wait_time):
        pass



#################################

url = 'https://docs.google.com/forms/u/0/'

user = 'lucas.rezende.malta@gmail.com'
pw = 'i73!w?MN'

driver = webdriver.Chrome()
driver.get(url)

sendkeys(user, '#identifierId')
click('#identifierNext > div > button')