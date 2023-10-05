from bs4 import BeautifulSoup

import matplotlib as mpl
import os
import pandas as pd
import pickle as pkl
import urllib.request

import constants
import flags


def create_urls_for_all_teams():
    urls = {}

    for abbreviation in constants.TEAMS_ABBREVIATIONS.keys():

        if flags.args.included_teams == 'all' or abbreviation in flags.args.included_teams:
            urls[abbreviation] = f"{constants.NFL_DRAFT_BASE_URL}/{abbreviation}/draft.htm"

    return urls


def get_old_draft_data():

    old_draft_data = None 

    if os.path.exists(constants.OLD_DRAFT_DATA_PATH):

        with open(constants.OLD_DRAFT_DATA_PATH, 'rb') as f: 
            old_draft_data = pkl.load(f)

    return old_draft_data

def store_old_draft_data(draft_data):

    with open(constants.OLD_DRAFT_DATA_PATH, 'wb') as f: 
        pkl.dump(old_draft_data, f)


def get_all_team_draft_data():

    urls = create_urls_for_all_teams()

    old_draft_data = None
    if flags.args.fresh_data == 'no':
        old_draft_data = get_old_draft_data()

    draft_data = pd.DataFrame(columns=[
                              "team_name", "abbreviation", "year", "player", "round", "games_played"], dtype=str)

    for abbreviation, url in urls.items():

        # If there is old data and the current team's abbreviation exists in it and we don't want fresh data pull it.
        if old_draft_data is not None and old_draft_data['abbreviation'].str.contains().any() and flags.args.fresh_data == 'no':
            continue


        fp = urllib.request.urlopen(url)
        mybytes = fp.read()

        mystr = mybytes.decode("utf8")
        fp.close()

        soup = BeautifulSoup(mystr, 'html.parser')

        tables = soup.findAll('table')
        links = table.findAll('a')

        drafts_per_year_for_team = extracted_drafts_by_year(tables)

        player_history = get_all_player_history_data(links)

        join_player_history_to_team(
            draft_data, player_history, drafts_per_year_for_team)


    join_old_and_new_data(draft_data, old_draft_data)
    return draft_data


def extracted_drafts_by_year(html_tables):
    pass


def get_all_player_history_data(links):
    pass


def join_player_history_to_team(draft_data, player_history, drafts_per_year_for_team):
    pass

def join_old_and_new_data(new, old):
    pass

def visualize(all_team_and_player_draft_data):
    pass


def main():

    all_team_and_player_draft_data = get_all_team_draft_data()

    visualize(all_team_and_player_draft_data)

    store_old_draft_data(all_team_and_player_draft_data)


if __name__ == "__main__":
    main()
