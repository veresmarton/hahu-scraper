import os
import sys
import requests
import argparse
import re
import pandas as pd
import numpy as np
import csv

from datetime import datetime
from bs4 import BeautifulSoup as bs

from preprocess import preprocess

def create_file(filename):
    if not os.path.exists(filename):
        colnames = ['run_datetime', 'query_name', 'make', 'model', 'link', 'price', 'fuel', 'year', 'engine_size', 'engine_power', 'mileage']
        with open(filename, 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(colnames)

def scrape_pages(name, file, url):
    create_file(file)
    page_number = 1
    next_page = True
    while next_page:
        print(page_number)
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

            now = datetime.now()

            line = [now, name, make, model, link, price, fuel, year, engine_size, engine_power, mileage]
            with open(file, 'a', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(line)

def run_queries(queryfile, dumpfile):
    with open(queryfile, 'r', encoding='utf-8') as f:
        qs = f.readlines()
    for q in qs:
        print(q)
        name, url = q.split()
        scrape_pages(name=name, file=dumpfile, url=url)

if __name__ == "__main__":
    argParser = argparse.ArgumentParser()
    argParser.add_argument("-q", "--queries", default=False)
    argParser.add_argument("-n", "--name")
    argParser.add_argument("-u", "--url")
    argParser.add_argument("-f", "--file", default='../data/raw/cars.csv')
    args = argParser.parse_args()
    if args.queries:
        run_queries(args.queries, args.file)
    else:
        scrape_pages(name=args.name, file=args.file, url=args.url)

    preprocess(args.file)
    #TODO predict

