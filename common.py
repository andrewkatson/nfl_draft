from bs4 import BeautifulSoup

import io
import os
import pandas as pd
import pathlib
import requests
import pickle as pkl
import urllib.request

import flags


def get_all_years_in_range():

    all_years_in_range = []

    for year in range(int(flags.args.last_date) + 1):

        if year >= int(flags.args.first_date) and year <= int(flags.args.last_date):
            all_years_in_range.append(str(year))

    return all_years_in_range


def invert(some_dict):
    return {v: k for k, v in some_dict.items()}


def get_tables_from_url(url):
    mystr = None
    try: 
        fp = urllib.request.urlopen(url)
        mybytes = fp.read()

        mystr = mybytes.decode("utf8")
        fp.close()
    except Exception as e: 
        print(f"There was an issue getting the html {e}")
        
    if mystr is None: 
        return None

    table_dfs = None
    try: 
        soup = get_soup(mystr)

        tables = soup.find_all('table')
        
        table_dfs = pd.read_html(io.StringIO(str(tables)))
    except Exception as e: 
        print(f"There was an issue with finding the tables {e}")

    return table_dfs

def concat_with_identical_cols(first, second):
    if first is None: 
        return second
    
    if second is None: 
        return first 
    
    first.reset_index(inplace=True, drop=True)
    second.reset_index(inplace=True, drop=True)

    return pd.concat([first, second], axis=0, ignore_index=True)
    
def get_data(path): 
    
    data = None

    if os.path.exists(path):

        with open(path, 'rb') as f:
            data = pkl.load(f)

    return data


def store_data(data, path): 
    
    as_path = pathlib.Path(path)
    just_parent = as_path.parent.absolute()
    
    if not os.path.exists(just_parent):
        os.makedirs(just_parent)

    with open(as_path, 'wb') as f:
        pkl.dump(data, f)

def download_url(url):
    return requests.get(url).text

def get_soup(html):
    return BeautifulSoup(html, 'html.parser')
    
def get_common_columns(one, two):
    
    common_columns = []
    
    for col in one.columns.values:
        if col in two.columns.values and col not in common_columns:
            common_columns.append(col)
            
    return common_columns
