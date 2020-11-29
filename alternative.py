import requests
from bs4 import BeautifulSoup

stock = 2
url = f'http://www.aastocks.com/tc/stocks/quote/quick-quote.aspx?symbol={stock}'
res = requests.get(url, headers={'referer': url})
soup = BeautifulSoup(res.content, 'html.parser')

text = soup.select_one("div.abs.txt_c span").text

letter = [num for num in text if num.isdigit() or num == "."]

price = "".join(letter)

print(price)