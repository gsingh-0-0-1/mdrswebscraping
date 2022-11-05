from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from time import sleep
import re

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


#####################################################################
# http://mdrs.marssociety.org/

pattern = re.compile('.*Crew [0-9]+.*')


url = 'http://mdrs.marssociety.org/previous-field-seasons/'

driver = webdriver.Chrome()

driver.get(url)

# collects the list of elements
elements = wait4elements('div.entry-content > p [href]')

for element in elements:
    print(element.text)

N = len(elements)  # number of elements

try:
    for cnt in range(0, N):  # for each element,check if there is hyperlinks on the page where it leads
        elements = wait4elements('div.entry-content > p [href]')

        print('\nAnalysing %s' % elements[cnt].text)
        elements[cnt].click()

        hyperlink_elements = wait4elements('[href]')  # gets all elements that have a hyperlink

        print('Analysing %d hyperlinks \n' % len(hyperlink_elements))
        if not hyperlink_elements:
            driver.get(url)
            continue

        for hyperlink_element in hyperlink_elements:
            try:
                hyperlink_element.text  # verify if the element has a text
            except:
                print('Something went wrong')
                continue  # if not, just ignore

            if re.match(pattern, hyperlink_element.text):
                print(hyperlink_element.text, hyperlink_element.get_attribute('href'))
        driver.get(url)

except Exception as LoopError:
    print(hyperlink_element.get_attribute('href'))
    print(LoopError)
