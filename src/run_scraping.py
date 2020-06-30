import codecs
import os
import sys
from django.db import DatabaseError

proj = os.path.dirname(os.path.abspath('manage.py'))
sys.path.append(proj)
os.environ["DJANGO_SETTINGS_MODULE"] = "scraping_service.settings"

import django
django.setup()

from scraping.parsers import *
from scraping.models import Vacancy, City, Language

parsers = (
    (work, 'https://www.work.ua/ru/jobs-python/'),
    (dou, 'https://jobs.dou.ua/vacancies/?category=Python'),
    (djinni, 'https://djinni.co/jobs/?location=%D0%9A%D0%B8%D0%B5%D0%B2&primary_keyword=Python'),
    (rabota, 'https://rabota.ua/zapros/python')
)
city = City.objects.filter(slug='kiev').first()
language = Language.objects.filter(slug='python').first()

jobs, errors = [], []

for func, url in parsers:
    j, e = func(url)
    jobs += j
    errors += e

print(len(jobs), len(errors), city, language)

for job in jobs:
    v = Vacancy(**job, city=city, language=language)
    v.save()
    try:
        v.save()
        print(v)
    except DatabaseError:
        print('[ERROR]')

# with codecs.open('work.txt', 'w', 'utf-8') as h:
#    h.write(str(jobs))
