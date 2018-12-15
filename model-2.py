import pygal as pygal
from bs4 import BeautifulSoup
from requests import get

import pandas as pd

from templates import bar, plot_pie

proxies = {
    "http": "http://20176001:!@Pass34@10.10.10.3:3128",
    "https": "http://20176001:!@Pass34@10.10.10.3:3128",
}


def q1():
    data = pd.read_csv('data/reviews.csv', index_col=0)

    # data.sort_values(by=['Label'], inplace=True)
    # print(data)
    # print(list(data))
    # print(type(data['Label']))
    # print(data.count(axis=1))

    # for x in data.iterrows():
    #     print(x)
    #     index, row = x
    #     print(index)
    #     print(type(row))
    #     print(row.index)
    #     print(row['Label'])
    #
    #     break


    bar(data.head(50))




# q1()
# plot_bar()
# plot_pie()