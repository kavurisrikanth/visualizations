import pygal as pygal
from bs4 import BeautifulSoup
from requests import get

import pandas as pd

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


def plot_bar():
    data = pd.read_csv('data/amazon_alexa.tsv', sep='\t')
    print(data.columns)
    bar(data.head(50))


def plot_pie():
    data = pd.read_csv('data/amazon_alexa.tsv', sep='\t')
    data = data.drop(['date', 'variation', 'verified_reviews', 'feedback'], axis=1)
    pie(data)


def bar(data):

    # Start up a chart object.
    chart = pygal.Bar()

    # Setup x and y data.
    # y_data = list(data['Label'])
    y_data = list(data['rating'])
    x_data = list(data.index)

    # Plot
    chart.add('Rating', y_data)
    chart.x_labels = x_data

    # Aaaaand save!
    chart.render_to_file('images/bar_chart.svg')


def pie(data):
    # Start up chart object.
    chart = pygal.Pie()

    chart.title = 'Ratings for Alexa.'

    # Setup required data. In this case, we're counting the number of each rating received (number of 1, number of 2, etc.)
    counts = data['rating'].value_counts()
    counts.sort_index(inplace=True)

    # Add to chart (hehe...)
    for x, y in counts.items():
        chart.add(str(x), y)

    # And go!
    chart.render_to_file('images/pie_chart.svg')

# q1()
# plot_bar()
plot_pie()