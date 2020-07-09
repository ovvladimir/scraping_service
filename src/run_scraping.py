import asyncio
import os
import sys
import datetime as dt

from django.contrib.auth import get_user_model
from django.db import DatabaseError

proj = os.path.dirname(os.path.abspath('manage.py'))
sys.path.append(proj)
os.environ["DJANGO_SETTINGS_MODULE"] = "scraping_service.settings"

try:
    import django
    django.setup()

    from scraping.parsers import *
    from scraping.models import Vacancy, Error, Url
except (BaseException, ImportError):
    pass

User = get_user_model()

parsers = (
    (work, 'work'),
    (dou, 'dou'),
    (djinni, 'djinni'),
    (rabota, 'rabota')
)
jobs, errors = [], []


def get_settings():
    qs1 = User.objects.filter(send_email=True).values()
    settings_lst = set((q['city_id'], q['language_id']) for q in qs1)
    return settings_lst


def get_urls(_settings):
    qs2 = Url.objects.all().values()
    url_dct = {(q['city_id'], q['language_id']): q['url_data'] for q in qs2}
    urls = []
    for pair in _settings:
        if pair in url_dct:
            tmp = {'city': pair[0], 'language': pair[1], 'url_data': url_dct[pair]}
            urls.append(tmp)
    return urls


async def main(value):
    func, url, city, language = value
    job, err = await loop.run_in_executor(None, func, url, city, language)
    errors.extend(err)
    jobs.extend(job)

settings = get_settings()
url_list = get_urls(settings)

loop = asyncio.get_event_loop()
tmp_tasks = [(func, data['url_data'][key], data['city'], data['language'])
             for data in url_list
             for func, key in parsers]
tasks = asyncio.wait([loop.create_task(main(f)) for f in tmp_tasks])

# for data in url_list:
#     for func, key in parsers:
#         url = data['url_data'][key]
#         j, e = func(url, city=data['city'], language=data['language'])
#         jobs += j
#         errors += e

loop.run_until_complete(tasks)
loop.close()

for jb in jobs:
    v = Vacancy(**jb)
    try:
        v.save()
        print(v)
    except DatabaseError:
        print('ERROR')
if errors:
    qs3 = Error.objects.filter(timestamp=dt.date.today())
    if qs3.exists():
        ers = qs3.first()
        ers.data.update({'errors': errors})
        ers.save()
    else:
        er = Error(data=f'errors:{errors}').save()

"""
from scraping.models import City, Language
import codecs

parsers = (
    (work, 'https://www.work.ua/ru/jobs-kyiv-python/'),
    (dou, 'https://jobs.dou.ua/vacancies/?category=Python'),
    (djinni, 'https://djinni.co/jobs/?location=%D0%9A%D0%B8%D0%B5%D0%B2&primary_keyword=Python'),
    (rabota, 'https://rabota.ua/zapros/python')
)
# city = City.objects.filter(slug='kiev').first()
# language = Language.objects.filter(slug='python').first()
city = City.objects.get(slug='kiev')
language = Language.objects.get(slug='python')
jobs, errors = [], []

for func, url in parsers:
    j, e = func(url, city=city.id, language=language.id)
    jobs += j
    errors += e
print(len(jobs))

for job in jobs:
    v = Vacancy(**job)
    try:
        v.save()
        print(v)
    except DatabaseError:
        print('[ERROR]')

if errors:
    er = Error(data=errors).save()

with codecs.open('work.txt', 'w', 'utf-8') as h:
    h.write(str(jobs))
"""
