import os
import sys
import argparse
import pandas as pd
import numpy as np

def query_file(make, model, year_start, year_end, file):
    df = pd.read_csv(file)
    df = df.query('make==@make and model==@model and year<=@year_end and year>=year_start')
    return df

if __name__ == "__main__":
    argParser = argparse.ArgumentParser()
    argParser.add_argument("-M", "--make")
    argParser.add_argument("-m", "--model")
    argParser.add_argument("-ys", "--year_start", default='2010')
    argParser.add_argument("-ye", "--year_end", default='2020')
    argParser.add_argument("-f", "--file", default='../data/raw/cars.csv')
    args = argParser.parse_args()
    df = query_file(args.make, args.model, args.year_start, args.year_end, args.file)