import os
import sys
import argparse
import pandas as pd
import numpy as np

def query_file(make, model, year, file):
    df = pd.read_csv(file)
    df = df.query('make==@make and model==@model and year<=@year+2 and year>=@year-2')
    return df

if __name__ == "__main__":
    argParser = argparse.ArgumentParser()
    argParser.add_argument("-f", "--file", default='../data/raw/cars.csv')
    args = argParser.parse_args()
    make = input('Make of car: ')
    model = input('Model of car: ')
    year = input('Year: ')
    mileage = input('Mileage: ')
    print(make, model, year, args.file)
    df = query_file(make.lower(), model.lower(), int(year), args.file)