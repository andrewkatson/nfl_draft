from bs4 import BeautifulSoup

import io
import matplotlib.pyplot as plt 
import os
import pandas as pd
import pickle as pkl
import urllib.request

import common
import constants
import flags


def create_urls_for_all_teams():
    urls = {}

    for abbreviation in constants.TEAMS_ABBREVIATIONS.keys():

        if flags.args.included_teams == 'all' or abbreviation in flags.args.included_teams:
            urls[abbreviation] = f"{constants.NFL_DRAFT_BASE_URL}/{abbreviation}/draft.htm"

    return urls


def get_old_draft_data():
    return common.get_data(constants.OLD_DRAFT_DATA_PATH)


def store_old_draft_data(draft_data):
    common.store_data(draft_data, constants.OLD_DRAFT_DATA_PATH)


def get_all_team_draft_data():

    urls = create_urls_for_all_teams()

    old_draft_data = None
    if flags.args.fresh_data == "False":
        old_draft_data = get_old_draft_data()

    draft_data = pd.DataFrame(columns=[
                              "Team", "Abbreviation", "Year", "Player", "Rnd", "AP1", "PB", "St", "G"], dtype=str)

    for abbreviation, url in urls.items():

        # If there is old data and the current team's abbreviation exists in it and we don't want fresh data don't pull it.
        if old_draft_data is not None and old_draft_data['Abbreviation'].str.contains(abbreviation).any() and flags.args.fresh_data == "False":
            continue

        table_dfs = common.get_tables_from_url(url)
        
        if table_dfs is None: 
            print(f"{url} did not exist or had some error")
            continue

        for index, table in enumerate(tables):
            table_df = tables_dfs[index]

            # Remove the top level index with "unnamed_0_level_0" and such
            table_df.columns = table_df.columns.droplevel()

            # Add the team and abbreviation
            table_df = table_df.assign(
                Team=constants.TEAMS_ABBREVIATIONS[abbreviation])
            table_df = table_df.assign(Abbreviation=abbreviation)

            drafts_per_year_for_team = pair_down_data(table_df)

            draft_data = common.concat_with_identical_cols(
                draft_data, drafts_per_year_for_team)

    if old_draft_data is not None:
        draft_data = common.concat_with_identical_cols(draft_data, old_draft_data)
    
    return draft_data


def pair_down_data(dataframe):
    return dataframe[constants.COLS_TO_SELECT]


def visualize(all_team_and_player_draft_data):
    
    all_years_in_range = common.get_all_years_in_range()
    
    # For visualization we drop the years that arent in the range we care about. 
    pared_down_by_year = all_team_and_player_draft_data[all_team_and_player_draft_data["Year"].isin(all_years_in_range)]
    
    for abbreviation in constants.TEAMS_ABBREVIATIONS.keys():
        
        pared_down_by_team = pared_down_by_year[pared_down_by_year["Abbreviation"] == abbreviation]
        
        if pared_down_by_team.empty:
            continue
            
        visualize_per_round_games_played(pared_down_by_team, constants.TEAMS_ABBREVIATIONS[abbreviation])
        
        visualize_per_year_games_played(pared_down_by_team, constants.TEAMS_ABBREVIATIONS[abbreviation])

def visualize_per_round_games_played(df, team):
    
    df = df[["Rnd", "G"]]
    
    df = df.dropna()
    
    df = df.astype({"G": int})

    df = df.groupby("Rnd").sum()
    
    fig = plt.figure()
    fig.canvas.manager.full_screen_toggle()
    
    rounds = df.index
    games = df["G"].astype(int)
 
    # creating the bar plot
    plt.bar(rounds.values, games.values, color ='maroon', 
            width = 0.4)
    
    plt.xlabel("Round drafted")
    plt.ylabel("No. of games played")
    plt.title(f"{team} games played per round drafted")
    plt.savefig(f"images/{team}_games_played_per_round_drafted.png")
    
    plt.close()


def visualize_per_year_games_played(df, team):
    df = df[["Year", "G"]]
    
    df = df.dropna()
    
    df = df.astype({"G": int})

    df = df.groupby("Year").sum()
    
    fig = plt.figure()
    fig.canvas.manager.full_screen_toggle()
    
    years = df.index
    games = df["G"].astype(int)
 
    # creating the bar plot
    plt.bar(years.values, games.values, color ='maroon', 
            width = 0.4)
    
    plt.xlabel("Year drafted")
    plt.ylabel("No. of games played")
    plt.title(f"{team} games played per year drafted")
    plt.savefig(f"images/{team}_games_played_per_year_drafted.png")
    
    plt.close()

def main():

    all_team_and_player_draft_data = get_all_team_draft_data()

    visualize(all_team_and_player_draft_data)

    store_old_draft_data(all_team_and_player_draft_data)


if __name__ == "__main__":
    main()
