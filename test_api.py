import os
import django
import sys
import json

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Chronical.settings')
django.setup()

from django.test import Client
c = Client()
r = c.get('/api/chart-data/number-of-livestock/?district=Ahilyanagar', HTTP_HOST='localhost')
print("Status code:", r.status_code)
if r.status_code == 200:
    print(json.dumps(r.json(), indent=2)[:500])
else:
    print(r.content)
