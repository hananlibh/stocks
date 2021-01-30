import requests
import pandas as pd
from bs4 import BeautifulSoup
import string
import nltk
from nltk.corpus import stopwords

# Create a function to scrape the data
def _scrape_stock_symbols(letter=None):
    company_name = []
    company_ticker = []
    if not letter:
        url = 'https://www.advfn.com/nyse/newyorkstockexchange.asp'
    else:
        letter = letter.upper()
        url = 'https://www.advfn.com/nyse/newyorkstockexchange.asp?companies=' + letter
    page = requests.get(url)
    soup = BeautifulSoup(page.text, "html.parser")
    odd_rows = soup.find_all('tr', attrs={'class': 'ts0'})
    even_rows = soup.find_all('tr', attrs={'class': 'ts1'})
    for i in odd_rows:
        row = i.find_all('td')
        company_name.append(row[0].text.strip())
        company_ticker.append(row[1].text.strip())
    for i in even_rows:
        row = i.find_all('td')
        company_name.append(row[0].text.strip())
        company_ticker.append(row[1].text.strip())
    return company_name, company_ticker


def get_companies_df():
    companies_df = pd.DataFrame(columns=['company_name', 'company_ticker'])
    (temp_name, temp_ticker) = _scrape_stock_symbols()
    companies_df['company_name'] = temp_name
    companies_df['company_ticker'] = temp_ticker
    for char in string.ascii_uppercase:
        (temp_name, temp_ticker) = _scrape_stock_symbols(char)
        letter_companies = pd.DataFrame(columns=['company_name', 'company_ticker'])
        letter_companies['company_name'] = temp_name
        letter_companies['company_ticker'] = temp_ticker
        letter_companies = letter_companies[letter_companies['company_name'] != '']
        companies_df = companies_df.append(letter_companies)
    companies_df.drop_duplicates(subset=['company_ticker'], inplace=True)
    return companies_df