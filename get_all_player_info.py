import io
import os
import pandas as pd
import string
import time


import common
import constants
import crawler
import flags


def get_player_urls():
    
    if os.path.exists(constants.PLAYER_URL_DF) and flags.args.fresh_data == "False":
        player_url_df = common.get_data(constants.PLAYER_MASTER_DF)
        
        return player_url_df["URL"]
    
    player_alphabet_urls = []
    for letter in string.ascii_uppercase:
        player_alphabet_urls.append(
            f"{constants.PFR_PLAYER_SCRAPING_BASE_URL}/{letter}/")
    player_url_crawler = crawler.Crawler(
        player_alphabet_urls, limit, "players", r".*/players/[a-zA-Z]/[a-zA-Z]+/*", depth)

    player_url_crawler.run()

    player_urls = player_url_crawler.final_urls
    
    player_url_df = pd.DataFrame(columns = ["Suffix", "URL"], dtype=str)
    
    for url in player_urls:
        suffix = url.rsplit('/', 1)[-1]
        
        player_url_df.loc[len(player_url_df.index)] = [suffix, url] 
        
    common.store_data(player_url_df, constants.PLAYER_URL_DF)
    return player_url_df["URL"]
        

def get_every_player_info(limit=None, depth=None, players_to_get=1):
    
    player_urls = get_player_urls()

    player_df = None
    if os.path.exists(constants.PLAYER_MASTER_DF):
        player_df = common.get_data(constants.PLAYER_MASTER_DF)

    count = 0
    for url in player_urls:
        print(f"Starting player import {url}")
        if count < players_to_get:
            player_info = None
            # If the player exists in the master data frame and we dont want fresh data
            if player_df is not None and url in player_df["URL"] and flags.args.fresh_data == "False":
                continue
            else:
                player_info = get_player_info_from_url(url)

            player_info["URL"] = url

            if player_df is None:
                player_df = player_info
            else:
                common_columns = common.get_common_columns(player_df, player_info)
                player_df = pd.merge(player_df, player_info, on=common_columns)
        else:
            break
        count += 1
        print(f"Finished player {url} import sleeping")
        time.sleep(60)

    common.store_data(player_df, constants.PLAYER_MASTER_DF)
    return player_df


def get_player_info_from_url(player_url):

    html = common.download_url(player_url)

    return get_player_info_from_raw_info(html)


def get_player_info_from_raw_info(raw_player_info):

    soup = common.get_soup(raw_player_info)

    tables = soup.find_all('table')

    h1s = soup.find_all('h1')
    
    name = ""
    for h1 in h1s:
        span = h1.find('span')
        
        if span is None: 
            continue
        else:
            name = span.text
            break

    table_dfs = pd.read_html(io.StringIO(str(tables)))

    complete_table_df = None

    for table_df in table_dfs:
        
        # Turn any multiindex cols into single index 
        table_df = combine_columns(table_df)
        table_df["Player"] = name

        if complete_table_df is None:
            complete_table_df = table_df
        else:
            common_columns = common.get_common_columns(complete_table_df, table_df)
            complete_table_df = pd.merge(complete_table_df, table_df, on=common_columns)

    complete_table_df.reset_index(inplace=True, drop=True)

    return complete_table_df


def combine_columns(df):
    df.columns = combine_columns_of_df(df.columns.values)
    return df

def combine_columns_of_df(column_values):
    new_cols = []
    for col in column_values:
        if "Unnamed" in col[0]:
            new_cols.append(col[1].strip())
        else: 
            new_cols.append(' '.join(col).strip())
    return new_cols

print(get_every_player_info(limit=30, depth=1, players_to_get=100).head())
