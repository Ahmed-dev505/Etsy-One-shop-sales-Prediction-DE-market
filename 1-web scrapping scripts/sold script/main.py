import os
import time
import warnings
import pandas as pd
import requests
from bs4 import BeautifulSoup
from selenium import webdriver

warnings.filterwarnings("ignore")

def driver_conn():
    try:
        options = webdriver.FirefoxOptions()
        options.add_argument("no-sandbox")
        options.add_argument("--disable-extensions")
        return webdriver.Firefox(executable_path="lib/geckodriver.exe", options=options)

    except:
        options = webdriver.ChromeOptions()
        options.add_argument("no-sandbox")
        options.add_argument("--incognito")
        options.add_argument('--disable-gpu')
        options.add_argument("--disable-extensions")
        return webdriver.Chrome(executable_path="lib/chromedriver.exe", options=options)


def get_data():
    all_links = []
    all_data = []
    driver = driver_conn()
    driver.minimize_window()
    print('==================== Getting links ====================')
    df = pd.read_csv("shopes_link.csv")
    store = df['url'].values
    print('Total Links: ' + str(len(store)))
    ll = 0
    for link in store:
        ll += 1
        print('Getting link ' + str(ll) + ' out of ' + str(len(store)))
        driver.close()
        driver = driver_conn()
        driver.minimize_window()
        driver.get(link)
        time.sleep(2)
        driver.find_element_by_xpath('''/html/body/div[8]/div[2]/div/div[2]/div[2]/button''').click()
        while True:
            time.sleep(2)
            new = driver.current_url
            soup = BeautifulSoup(driver.page_source, 'html.parser')
            lis = soup.find_all('div', {'class': 'v2-listing-card'})
            if len(lis) <= 0:
                driver.close()
                driver = driver_conn()
                driver.minimize_window()
                driver.get(new)
                time.sleep(2)
                driver.find_element_by_xpath('''/html/body/div[8]/div[2]/div/div[2]/div[2]/button''').click()
                time.sleep(2)
                soup = BeautifulSoup(driver.page_source, 'html.parser')
                lis = soup.find_all('div', {'class': 'v2-listing-card'})
                pass
                # break

            for tr in lis:
                lin = tr.find('a')['href']
                data = {
                    'links': lin,
                }
                # print(data)
                all_links.append(data)
                df = pd.DataFrame(all_links)
                df = df.rename_axis("Index")
                df.to_csv('links.csv')

            try:
                print('Total Link: ' + str(len(all_links)))
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(2)
                driver.execute_script("window.scrollTo(0, window.scrollY -150);")
                time.sleep(2)
                aa = driver.find_element_by_class_name('ss-navigateright').click()
            except:
                break
                # driver.close()
    return


if __name__ == '__main__':
    get_data()

