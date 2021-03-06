import requests
from bs4 import BeautifulSoup
import os
import csv

""" Your login information below. It's probably best to store this in environment variables."""
# EMAIL = 'email@example.com'
# PASSWORD = 'password'

""" Uncomment below and comment out above if you're using environment variables"""
EMAIL = os.environ.get('pcoemail')
PASSWORD = os.environ.get('pcopass')
FORM_ID = '9041'  # The ID of the Form
""" Internal URL """

SCRAPEURL = 'https://people.planningcenteronline.com/forms/' + FORM_ID + '/submissions/export.csv'

headers = {
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/67.0.3396.99 Safari/537.36'
}

login_data = dict(utf8=None,
                  email=EMAIL,
                  password=PASSWORD,
                  authenticity_token=None)

with requests.Session() as s:
    url = 'https://accounts.planningcenteronline.com/login'
    r = s.get(url, headers=headers)
    soup = BeautifulSoup(r.content, 'html.parser')
    login_data['authenticity_token'] = soup.find('input', attrs={'name': 'authenticity_token'})['value']
    login_data['utf8'] = soup.find('input', attrs={'name': 'utf8'})['value']
    r = s.post(url, data=login_data, headers=headers)

    page = s.get(SCRAPEURL)
    csv_file = page.content.decode('utf-8')

    csv_reader = csv.reader(csv_file.splitlines(), delimiter=',')
    line_count = 0
    for row in csv_reader:
        print(row)
        line_count += 1
