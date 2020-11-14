from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import os
import time
import datetime
import json

path = os.path.abspath(
    r'C:\Users\Adrian\Documents\youtube\video_01\stock_price(prep)\geckodriver.exe')


class StockPrice:
    def __init__(self, url, stock_code):
        self.driver = webdriver.Firefox(executable_path=path)
        self.driver.get(url)
        self.stock_code = stock_code
        inputbox = self.driver.find_element_by_id('txtHKQuote')
        inputbox.send_keys(stock_code)
        inputbox.send_keys(Keys.ENTER)

    def get_price(self):
        time.sleep(3)
        timestamp = str(datetime.datetime.now())
        layout = self.driver.find_element_by_class_name('lastBox')
        text = layout.find_element_by_class_name(
            'pos').get_attribute('innerHTML')
        price = text.split('</span>')[1]

        data = {
            'Stock': self.stock_code,
            'Time': timestamp,
            'Price': price
        }
        print(data)
        self.driver.refresh()
        return data


bot = StockPrice('http://www.aastocks.com/tc/default.aspx', 700)


while True:
    mydata = []
    fn = f'{bot.stock_code}.json'

    if os.path.isfile(fn):
        with open(fn) as fp:
            mydata = json.load(fp)

    new_data = bot.get_price()
    mydata.append(new_data)

    with open(fn, 'w') as fp:
        json.dump(mydata, fp)
