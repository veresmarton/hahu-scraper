import os
import sys
import requests
import argparse
import re
import pandas as pd
import numpy as np
import csv
import urllib3

from datetime import datetime
from bs4 import BeautifulSoup as bs

from preprocess import preprocess
from predicter import predict

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def create_file(filename):
    if not os.path.exists(filename):
        colnames = ['run_datetime', 'query_name', 'make', 'model', 'link', 'price', 'fuel', 'year', 'engine_size', 'engine_power', 'mileage', 'adcode']
        with open(filename, 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(colnames)

def scrape_pages(name, file, url):
    create_file(file)
    page_number = 1
    next_page = True
    while next_page:
        print(page_number, end='\r')
        page = requests.get(url + '/page'+str(page_number), verify=False)
        if page.status_code != 200:
            break
        page_number += 1
        details = scrape_page(name, file, page)

def scrape_page(name, file, page):
        soup = bs(page.content, "html.parser")
        results = soup.find_all("div", class_=re.compile("^row talalati-sor"))
        
        for r in results:
            title = r.find("h3").find('a')
            link = title.get('href')
            make, model = title.text.split()[:2]
            make = make.lower()
            model = model.lower()
            
            price = r.select("div[class^=pricefield-primary]")[0].text.strip('Ft')
            price = ''.join(price.split())
            try:
                price = int(price)
            except:
                price = np.nan
        
            details = r.find("div", class_='talalatisor-info adatok')
            fuel, year, engine_size, _, engine_power, mileage = details.text.split(',')
            year = int(year.strip().split('/')[0])
            engine_size = int(''.join(engine_size.strip(" cm³").split()))
            engine_power = int(''.join(engine_power.strip("LE").split()))
            mileage = int(''.join(mileage.strip('km').split()))
            adcode = r.find("div", class_='talalatisor-info talalatisor-hirkod').text
            adcode = re.findall('[0-9]+', adcode)[0]

            now = datetime.now()

            line = [now, name, make, model, link, price, fuel, year, engine_size, engine_power, mileage, adcode]
            with open(file, 'a', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(line)

def run_queries(queryfile, dumpfile):
    with open(queryfile, 'r', encoding='utf-8') as f:
        qs = f.readlines()
    for q in qs:
        name, url = q.split()
        print(name)
        scrape_pages(name=name, file=dumpfile, url=url)

def get_last_refresh_date(path="../data/interim/last_refresh_date.txt"):
    with open(path, "r") as f:
        ts = f.readline()
    return pd.to_datetime(ts)

def save_last_refresh_date(ts, path="../data/interim/last_refresh_date.txt"):
    with open(path, "w") as f:
        ts = datetime.strftime(ts, "%Y-%m-%d %H:%M:%S.%f")
        f.write(ts)

def check_if_exists_and_write(df, filename):
    if not os.path.isfile(filename):
        df.to_csv(filename)
    else:
        df.to_csv(filename, mode='a', header=False)

def collect_deals(source="../data/processed/predicted_price.csv"):
    df = pd.read_csv(source)
    df.drop_duplicates(keep='first', subset=['query_name', 'make', 'model', 'price', 'fuel',
       'year', 'engine_size', 'engine_power', 'mileage', 'ford', 'hyundai',
       'kia', 'skoda', 'volkswagen', 'is_diesel', 'year_old'], inplace=True)
    df['run_datetime'] = pd.to_datetime(df['run_datetime'])
    latest_date = get_last_refresh_date()
    df = df[df.run_datetime > latest_date]
    df = df.query('price < 3500000 and mileage < 200000')
    check_if_exists_and_write(df, f"../data/processed/deal_{datetime.now().strftime('%Y%m%d')}.csv")
    new_latest_date = df.run_datetime.max()
    if not pd.isna(new_latest_date):
        save_last_refresh_date(new_latest_date)

if __name__ == "__main__":
    argParser = argparse.ArgumentParser()
    argParser.add_argument("-q", "--queries", default='../data/interim/queries.txt')
    args = argParser.parse_args()
    now = datetime.now().strftime("%Y%m%d%H%M%S")
    file = f"../data/raw/cars_{now}.csv"
    run_queries(args.queries, file)

    preprocess(file)
    predict()
    collect_deals()

