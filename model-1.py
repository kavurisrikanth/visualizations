import datetime
import math
import time
import pandas as pd
from random import randint

from bs4 import BeautifulSoup
from requests import get

proxies = {
    "http": "http://20176001:!@Pass34@10.10.10.3:3128",
    "https": "http://20176001:!@Pass34@10.10.10.3:3128",
}


def q1():
    # Wikipedia URL for Fortune 500 list.
    snp_wiki_url = 'https://en.wikipedia.org/wiki/List_of_S%26P_500_companies'

    # Open URL and get list of companies.
    # response = get(snp_wiki_url, proxies=proxies)
    response = get(snp_wiki_url)
    print(response.status_code)

    # Response code validation.
    if response.status_code != 200:
        print('ERROR: Accessing URL "' + snp_wiki_url + '" returned status code ' + str(response.status_code))
        return

    print('Success!')

    # URL for Yahoo finance. We formulate this URL for every company.
    base_url = 'https://finance.yahoo.com/quote/'
    history_url = '/history?'
    period_1_arg = 'period1='
    period_2_arg = 'period2='
    tail_args = 'interval=1d&filter=history&frequency=1d'

    # One month. Times in milliseconds, as required by Yahoo.
    today_ms = math.floor(time.time())
    one_month_ago = datetime.date.today() - datetime.timedelta(days=30)
    oma_ms = int(time.mktime(one_month_ago.timetuple()))

    period_1_arg += str(oma_ms)
    period_2_arg += str(today_ms)

    # Fetching the table of companies.
    wiki_soup = BeautifulSoup(response.text, 'html.parser')
    first_table = wiki_soup.table
    body = first_table.tbody

    closing_prices = {}
    price_rows = {}
    codes = []

    # Get all rows.
    rows_list = body.find_all('tr')

    for r in rows_list[1:]:
        # Get the first "slot". This contains the symbol with which we search.
        slots = r.find_all('td')

        data = slots[0]

        if len(slots) >= 4:
            gics = slots[3].text
        else:
            gics = 'NA'

        # Again, validation
        if data:
            # Get the symbol
            name = data.a.text

            if name and len(name) > 0:
                print(name + ', ' + gics)
                codes.append((name, gics))

    print('Loop 1 done.')

    for c in codes:
        name = c[0]

        # Construct the URL for this company.
        yahoo_stocks_url = base_url + name + history_url + period_1_arg + '&' + period_2_arg + '&' + tail_args
        # print(yahoo_stocks_url)

        # Send a GET request.
        # stocks_response = get(yahoo_stocks_url, proxies=proxies)
        stocks_response = get(yahoo_stocks_url)

        # Validate.
        if stocks_response.status_code != 200:
            print('ERROR: Accessing URL "' + yahoo_stocks_url + '" returned status code ' + str(
                response.status_code))
            return

        # Soupify
        stocks_soup = BeautifulSoup(stocks_response.text, 'html.parser')

        # Extract the first table.
        stocks_table = stocks_soup.table.tbody
        # print(stocks_table)

        # Get all rows.
        rows_list = stocks_table.find_all('tr')
        print(rows_list)

        price_rows[name] = rows_list

    print('Loop 2 done.')

    for name in price_rows:
        # List to hold all the prices for the last month.
        prices = []

        rows_list = price_rows[name]

        for r in rows_list:
            # If the row contains the closing price, extract it.
            if len(r) >= 5:
                span = r.find_all('td')[4].span

                if span:
                    p = span.text
                    p = p.replace(',', '')
                    prices.append(float(p))
                else:
                    prices.append(float('NaN'))

        # Add it into the dictionary.
        closing_prices[name] = prices

        # Sleep a bit to avoid pummelling the server.
        # time.sleep(0.8)

    print('Loop 3 done.')

    print(closing_prices)

    stocks_df = pd.DataFrame(closing_prices, columns=['Symbol', 'Closing Price'])

    print(stocks_df)


def main():

    q1()


if __name__ == '__main__':
    main()
