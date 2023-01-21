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

def scrape(name, url):
    pass

if __name__ == "__main__":
    argParser = argparse.ArgumentParser()
    args = argParser.parse_args()
    scrape(*args)

