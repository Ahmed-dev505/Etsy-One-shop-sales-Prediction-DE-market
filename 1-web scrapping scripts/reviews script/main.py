import re
import time
import warnings
import pandas as pd
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
    driver = driver_conn()
    driver.minimize_window()
    print('==================== Start scraping & getting links ====================')
    df = pd.read_csv("link.csv")
    store = df['url'].values
    print('Total Links in CSV: ' + str(len(store)))
    ll = 0
    for link in store:
        ll += 1
        print('Getting link from CSV ' + str(ll) + ' out of ' + str(len(store)))
        driver.close()
        driver = driver_conn()
        driver.minimize_window()
        driver.get(link)
        time.sleep(2)
        try:
            driver.find_element_by_xpath('''/html/body/div[8]/div[2]/div/div[2]/div[2]/button''').click()
        except:
            pass
        while True:
            time.sleep(2)
            new = driver.current_url
            soup = BeautifulSoup(driver.page_source, 'html.parser')
            lis = soup.find_all('div', {'class': 'review-item'})
            if len(lis) <= 0:
                driver.close()
                driver = driver_conn()
                driver.minimize_window()
                driver.get(new)
                time.sleep(2)
                try:
                    driver.find_element_by_xpath('''/html/body/div[8]/div[2]/div/div[2]/div[2]/button''').click()
                except:
                    pass
                soup = BeautifulSoup(driver.page_source, 'html.parser')
                lis = soup.find_all('div', {'class': 'review-item'})
                pass
            for tr in lis:
                item_link = ''
                item_title = ''
                customer_name = ''
                temp_1 = ''
                item_rating = ''
                review_text = ''
                try:
                    item_link = 'https://www.etsy.com' + tr.find('div', {'class': 'listing-group'}).find('a', {'class': 'text-link-secondary'})['href']
                except:
                    pass
                try:
                    item_title = tr.find('a', {'class': 'text-link-secondary'}).find('p').text
                except:
                    pass
                try:
                    customer_name = tr.find('p', {'class': 'shop2-review-attribution'}).find('a').text
                except:
                    pass
                try:
                    review_date = tr.find('p', {'class': 'shop2-review-attribution'}).text.replace('''
''', '').replace('''
                    ''', '')
                    temp_1 = review_date.split('on')[-1]
                except:
                    pass
                try:
                    item_rating = tr.find('span', {'class': 'stars-svg'}).find('span', {'class': 'screen-reader-only'}).text
                except:
                    pass
                try:
                    review_text = tr.find('div', {'class': 'text-gray-lighter'}).find('p', {'class': 'prose'}).text
                except:
                    pass
                data = {
                    'links': item_link,
                    'item_title': item_title,
                    'Customer Name': customer_name,
                    'Review Date': temp_1,
                    'Item rating': item_rating,
                    'Review text': review_text,
                }
                # print(data)
                all_links.append(data)
                df = pd.DataFrame(all_links)
                df = df.rename_axis("Index")
                df.to_csv('data.csv')

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
