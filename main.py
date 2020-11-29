from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time, datetime, json, os

path = r'C:\Users\Adrian\Documents\youtube\video_01\Stock_price\geckodriver.exe'

class StockPrice:
    def __init__(self, stock_code):
        self.driver = webdriver.Firefox(executable_path=path)
        self.stock_code = stock_code
        self.driver.get('http://www.aastocks.com/tc/')
        inputbox = self.driver.find_element_by_id('txtHKQuote')
        inputbox.send_keys(self.stock_code)
        inputbox.send_keys(Keys.ENTER)

    def get_price(self):
        time.sleep(3)

        timestamp = str(datetime.datetime.now())

        #搵lastbox出嚟
        layout = self.driver.find_element_by_class_name('lastBox')

        #搵有股價個div  div.abs.txt_c  => 代表<div class="abs txt_c">
        div = layout.find_element_by_css_selector('div.abs.txt_c')

        #搵個span再拎個text(股價)出嚟
        price = div.find_element_by_css_selector('span').text

        #如果升或者跌既話  要整走個箭咀
        price = price.split('\n')[1] if '\n' in price else price

        data = {
            'Stock': self.stock_code,
            'Time' : timestamp,
            'Price': price
        }
        print(data)
        self.driver.refresh()
        return data

bot = StockPrice(241)


while True:
    mydata = []
    file_name = f'{bot.stock_code}.json'
    if os.path.isfile(file_name):
        with open(file_name) as fp:
            mydata = json.load(fp)

    new_data = bot.get_price()
    mydata.append(new_data)

    with open(file_name, 'w') as fp:
        json.dump(mydata, fp)