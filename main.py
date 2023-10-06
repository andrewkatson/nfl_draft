from bs4 import BeautifulSoup

import io
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
        pkl.dump(draft_data, f)


def get_all_team_draft_data():

    urls = create_urls_for_all_teams()

    old_draft_data = None
    if flags.args.fresh_data == 'no':
        old_draft_data = get_old_draft_data()

    draft_data = pd.DataFrame(columns=[
                              "Team", "Abbreviation", "Year", "Player", "Rnd", "AP1", "PB", "St", "G"], dtype=str)

    for abbreviation, url in urls.items():

        # If there is old data and the current team's abbreviation exists in it and we don't want fresh data don't pull it.
        if old_draft_data is not None and old_draft_data['Abbreviation'].str.contains(abbreviation).any() and flags.args.fresh_data == 'no':
            continue

        fp = urllib.request.urlopen(url)
        mybytes = fp.read()

        mystr = mybytes.decode("utf8")
        fp.close()

        soup = BeautifulSoup(mystr, 'html.parser')

        tables = soup.find_all('table')
        tables_dfs = pd.read_html(io.StringIO(str(tables)))

        for index, table in enumerate(tables):
            table_df = tables_dfs[index]

            # Remove the top level index with "unnamed_0_level_0" and such
            table_df.columns = table_df.columns.droplevel()

            # Add the team and abbreviation
            table_df = table_df.assign(
                Team=constants.TEAMS_ABBREVIATIONS[abbreviation])
            table_df = table_df.assign(Abbreviation=abbreviation)

            drafts_per_year_for_team = pair_down_data(table_df)

            draft_data = join_player_history_to_team(
                draft_data, drafts_per_year_for_team)

    draft_data = join_old_and_new_data(draft_data, old_draft_data)

    print(draft_data.head())
    return draft_data


def pair_down_data(dataframe):
    return dataframe[constants.COLS_TO_SELECT]


def join_player_history_to_team(draft_data, drafts_per_year_for_team):
    return pd.concat([draft_data, drafts_per_year_for_team], axis=0, ignore_index=True)


def join_old_and_new_data(new, old):
    return pd.concat([new, old], axis=0, ignore_index=True)


def visualize(all_team_and_player_draft_data):
    pass


def main():

    all_team_and_player_draft_data = get_all_team_draft_data()

    visualize(all_team_and_player_draft_data)

    store_old_draft_data(all_team_and_player_draft_data)


if __name__ == "__main__":
    main()
