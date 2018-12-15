from bs4 import BeautifulSoup
from requests import get

base_url = 'https://www.imdb.com/search/title?'
type_url_feature = 'title_type=feature'
rating_gt_8_url = 'user_rating=8.0,'
num_votes_gt_url = 'num_votes=40000,'
year_gt_url = 'release_date=2000-01-01,'


def q1():
    url = base_url + type_url_feature + '&' + rating_gt_8_url

    response = get(url)

    html_soup = BeautifulSoup(response.text, 'html.parser')
    movie_containers = html_soup.find_all('div', class_='lister-item mode-advanced')

    top_20 = []

    # Get the top 20.
    for x in range(20):
        m = movie_containers[x]

        title = m.h3.a.text
        rating = float(m.strong.text)

        top_20.append((title, rating))

    return top_20


def q2():
    url = base_url + num_votes_gt_url + '&' + year_gt_url + '&sort=num_votes,desc'

    response = get(url)

    html_soup = BeautifulSoup(response.text, 'html.parser')
    movie_containers = html_soup.find_all('div', class_='lister-item mode-advanced')

    top_20 = []

    # Get the top 20.
    for x in range(20):
        m = movie_containers[x]

        title = m.h3.a.text
        rating = float(m.strong.text)

        votes_str = m.find('span', attrs = {'name':'nv'}).text
        num_votes = int(votes_str.replace(',', ''))
        y_str = m.h3.find('span', class_='lister-item-year text-muted unbold').text[1:5]
        year = int(y_str.replace(',', ''))

        top_20.append((title, rating, num_votes, year))

    return top_20


def test_q1(l):
    for n, r in l:
        if r < 8.0:
            return False

    return True


def test_q2(l):
    try:
        for n, r, v, y in l:
            if v < 40000 or y < 2000:
                return False
        return True
    except:
        return False


def main():
    if not test_q1(q1()):
        print('Q1 Failed!')
    else:
        print('Q1 Passed')

    if not test_q2(q2()):
        print('Q2 Failed!')
    else:
        print('Q2 Passed')


if __name__ == '__main__':
    main()
