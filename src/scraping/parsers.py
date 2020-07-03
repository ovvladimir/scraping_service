import requests
import codecs
from bs4 import BeautifulSoup as BSp
from random import randint

__all__ = ('work', "rabota", 'dou', 'djinni')
jobs, errors = [], []

headers = [
    {'User-Agent': 'Mozilla/5.0 (Windows NT 5.1; rv:47.0) Gecko/20100101 Firefox/47.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'},
    {'User-Agent': 'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 '
                   '(KHTML, like Gecko) Chrome/49.0.2623.112 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'},
    {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; rv:53.0) Gecko/20100101 Firefox/53.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'},
    {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                   '(KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36'}
]


def work(url, city=None, language=None):
    jobs.clear()
    errors.clear()
    domain = 'https://www.work.ua'
    if url:
        resp = requests.get(url, headers=headers[randint(0, 2)])
        if resp.status_code == 200:
            soup = BSp(resp.content, 'html.parser')
            main_div = soup.find('div', id='pjax-job-list')
            if main_div:
                div_lst = main_div.find_all('div', attrs={'class': 'job-link'})
                for div in div_lst:
                    title = div.find('h2')
                    href = title.a['href']
                    content = div.p.text
                    company = 'No name'
                    logo = div.find('img')
                    if logo:
                        company = logo['alt']
                    jobs.append({'title': title.text, 'url': domain + href,
                                 'description': content, 'company': company,
                                 'city_id': city, 'language_id': language})
            else:
                errors.append({'url': url, 'title': "Div does not exists"})
        else:
            errors.append({'url': url, 'title': "Page do not response"})

    return jobs, errors


def rabota(url, city=None, language=None):
    jobs.clear()
    errors.clear()
    domain = 'https://rabota.ua'
    if url:
        resp = requests.get(url, headers=headers[randint(0, 2)])
        if resp.status_code == 200:
            soup = BSp(resp.content, 'html.parser')
            new_jobs = soup.find('div',
                                 attrs={'class': 'f-vacancylist-newnotfound'})
            if not new_jobs:
                table = soup.find('table',
                                  id='ctl00_content_vacancyList_gridList')
                if table:
                    tr_lst = table.find_all('tr', attrs={'id': True})
                    for tr in tr_lst:
                        div = tr.find('div', attrs={'class': 'card-body'})
                        if div:
                            title = div.find('p',
                                             attrs={'class': 'card-title'})
                            href = title.a['href']
                            content = div.p.text
                            company = 'No name'
                            p = div.find('p', attrs={'class': 'company-name'})
                            if p:
                                company = p.a.text
                            jobs.append({
                                'title': title.text,
                                'url': domain + href,
                                'description': content,
                                'company': company,
                                'city_id': city, 'language_id': language})
                else:
                    errors.append({'url': url, 'title': "Table does not exists"})
            else:
                errors.append({'url': url, 'title': "Page is empty"})
        else:
            errors.append({'url': url, 'title': "Page do not response"})

    return jobs, errors


def dou(url, city=None, language=None):
    jobs.clear()
    errors.clear()
    # domain = 'https://www.work.ua'
    if url:
        resp = requests.get(url, headers=headers[randint(0, 2)])
        if resp.status_code == 200:
            soup = BSp(resp.content, 'html.parser')
            main_div = soup.find('div', id='vacancyListId')
            if main_div:
                li_lst = main_div.find_all('li', attrs={'class': 'l-vacancy'})
                for li in li_lst:
                    # if '__hot' not in li['class']:
                    title = li.find('div', attrs={'class': 'title'})
                    href = title.a['href']
                    cont = li.find('div', attrs={'class': 'sh-info'})
                    content = cont.text
                    company = 'No name'
                    a = title.find('a', attrs={'class': 'company'})
                    if a:
                        company = a.text
                    jobs.append({'title': title.text, 'url': href,
                                 'description': content, 'company': company,
                                 'city_id': city, 'language_id': language})
            else:
                errors.append({'url': url, 'title': "Div does not exists"})
        else:
            errors.append({'url': url, 'title': "Page do not response"})

    return jobs, errors


def djinni(url, city=None, language=None):
    jobs.clear()
    errors.clear()
    domain = 'https://djinni.co'
    if url:
        resp = requests.get(url, headers=headers[randint(0, 2)])
        if resp.status_code == 200:
            soup = BSp(resp.content, 'html.parser')
            main_ul = soup.find('ul', attrs={'class': 'list-jobs'})
            if main_ul:
                li_lst = main_ul.find_all('li',
                                          attrs={'class': 'list-jobs__item'})
                for li in li_lst:
                    title = li.find('div',
                                    attrs={'class': 'list-jobs__title'})
                    href = title.a['href']
                    cont = li.find('div',
                                   attrs={'class': 'list-jobs__description'})
                    content = cont.text
                    company = 'No name'
                    comp = li.find('div',
                                   attrs={'class': 'list-jobs__details__info'})
                    if comp:
                        company = comp.text
                    jobs.append({'title': title.text, 'url': domain + href,
                                 'description': content, 'company': company,
                                 'city_id': city, 'language_id': language})
            else:
                errors.append({'url': url, 'title': "Div does not exists"})
        else:
            errors.append({'url': url, 'title': "Page do not response"})

    return jobs, errors


if __name__ == '__main__':
    url_list = [
        'https://www.work.ua/ru/jobs-kyiv-python/',
        'https://rabota.ua/zapros/python',
        'https://jobs.dou.ua/vacancies/?category=Python',
        'https://djinni.co/jobs/?location=%D0%9A%D0%B8%D0%B5%D0%B2&primary_keyword=Python'
    ]
    jobs, errors = work(url_list[0])

    with codecs.open('work.txt', 'w', 'utf-8') as h:
        h.write(str(jobs))

"""
resp = requests.get(
    'https://www.work.ua/ru/jobs-kyiv-python/',
    headers={
        'User-Agent': 'Mozilla/5.0 (Windows NT 5.1; rv:47.0) Gecko/20100101 Firefox/47.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
    }
)
if resp.status_code == 200:
    with codecs.open('work.html', 'w', 'utf-8') as h:
        h.write(str(resp.text))
"""
