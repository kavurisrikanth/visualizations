def is_dividend(line):
    pieces = line.split(' ')
    return True if len(pieces) < 7 else False


def process_stock_line(line, sym):
    date = line[:12]
    line = line[13:]

    return [sym, date, line.split(' ')[3]]


def get_1000_days(browser, symbol, freq='d'):
    browser.get("https://finance.yahoo.com/quote/" + symbol + "/history?period1=" + str(fya_ms) + '&period2=' + str(
        today_ms) + '&interval=1' + freq + '&filter=history&frequency=1' + freq)

    j = 0
    while j < 20:
        browser.execute_script("window.scrollTo(0, 108000);")
        time.sleep(0.25)
        j = j + 1

    titles_element = browser.find_elements_by_xpath(".//tbody[@data-reactid='50']")
    # print(titles_element[0].text)
    # print(type(titles_element[0]))
    # print(titles_element[0].size)
    # print(type(titles_element[0].text))

    one_big_text = titles_element[0].text
    lines = one_big_text.split('\n')
    # print(len(lines))

    formatted_data = []
    for x in lines:
        if not is_dividend(x):
            formatted_data.append(process_stock_line(x, symbol))

    print(len(formatted_data))
    days_1000 = formatted_data[:1000]
    print(len(days_1000))
    print(days_1000[0])
    print(days_1000[1])
    print(days_1000[2])

    return days_1000


def q1():
    '''
    Fetch 1000 trading days' worth of data from the Yahoo! Finance website.
    Awfully conveniently, the site itself doesn't list any data for holidays.
    So, just pull 5 years' worth of data, assuming it's around 250 days per year.
    And then we run through the days counting to 1000.
    We just discard the extras.
    :return:
    '''

    option = webdriver.ChromeOptions()
    option.add_argument("--incognito")
    driver_path = "F:\\msit\\specialization\\topics\\visualization\\chromedriver.exe"
    
    data = pd.read_html('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')
    table = data[0]

    sliced_table = table[1:]
    header = table.iloc[0]

    corrected_table = sliced_table.rename(columns=header)

    tickers = corrected_table['Symbol'].tolist()

    days_df = pd.DataFrame()
    weeks_df = pd.DataFrame()
    months_df = pd.DataFrame()

    overall_delta = {}

    for ele in tickers:
        print(ele)

        browser = webdriver.Chrome(driver_path)

        days_1000 = get_1000_days(browser, ele, 'd')
        old_price = float(days_1000[-1][2])
        new_price = float(days_1000[0][2])
        overall_delta[ele] = (old_price - new_price)/old_price * 100
        days_df = days_df.append(pd.DataFrame(days_1000, columns=['Symbol', 'Date', 'Closing price']))


        time.sleep(1)
        weeks_1000 = get_1000_days(browser, ele, 'wk')
        weeks_df = weeks_df.append(pd.DataFrame(weeks_1000, columns=['Symbol', 'Date', 'Closing price']))

        time.sleep(1)
        months_1000 = get_1000_days(browser, ele, 'mo')
        months_df = months_df.append(pd.DataFrame(months_1000, columns=['Symbol', 'Date', 'Closing price']))

        # print_list(days_1000[0].split(' '))

        browser.quit()
        break

    print(days_df.head())
    print(weeks_df.head())
    print(months_df.head())

    if False:
        days_df.to_csv('data/exam_days.csv')
        weeks_df.to_csv('data/exam_weeks.csv')
        months_df.to_csv('data/exam_months.csv')

    return (days_df, weeks_df, months_df, overall_delta)
	
	
# Calculate times in micro-seconds
today_ms = math.floor(time.time())
four_years_ago = datetime.date.today() - datetime.timedelta(days=365 * 4)
fya_ms = int(time.mktime(four_years_ago.timetuple()))

days_df, weeks_df, months_df, overall_change = q1()