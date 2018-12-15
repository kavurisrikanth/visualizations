import pandas as pd
import pygal


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