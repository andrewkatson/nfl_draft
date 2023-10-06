from bs4 import BeautifulSoup

import io
import matplotlib.pyplot as plt 
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

    if old_draft_data is not None:
        draft_data = join_old_and_new_data(draft_data, old_draft_data)
    
    return draft_data


def pair_down_data(dataframe):
    return dataframe[constants.COLS_TO_SELECT]


def join_player_history_to_team(draft_data, drafts_per_year_for_team):
    return pd.concat([draft_data, drafts_per_year_for_team], axis=0, ignore_index=True)


def join_old_and_new_data(new, old):
    return pd.concat([new, old], axis=0, ignore_index=True)


def visualize(all_team_and_player_draft_data):
    
    all_years_in_range = get_all_years_in_range()
    
    # For visualization we drop the years that arent in the range we care about. 
    pared_down_by_year = all_team_and_player_draft_data[all_team_and_player_draft_data["Year"].isin(all_years_in_range)]
    
    for abbreviation in constants.TEAMS_ABBREVIATIONS.keys():
        
        pared_down_by_team = pared_down_by_year[pared_down_by_year["Abbreviation"] == abbreviation]
        
        if pared_down_by_team.empty:
            continue
            
        visualize_per_round_games_played(pared_down_by_team, constants.TEAMS_ABBREVIATIONS[abbreviation])
        
        visualize_per_year_games_played(pared_down_by_team, constants.TEAMS_ABBREVIATIONS[abbreviation])

def get_all_years_in_range(): 
    
    all_years_in_range = []
    
    for year in range(int(flags.args.last_date) + 1): 
        
        if year >= int(flags.args.first_date) and year <= int(flags.args.last_date):
            all_years_in_range.append(str(year)) 
            
    return all_years_in_range

def visualize_per_round_games_played(df, team):
    
    df = df[["Rnd", "G"]]
    
    df = df.dropna()
    
    df = df.astype({"G": int})

    df = df.groupby("Rnd").sum()
    
    fig = plt.figure(figsize = (10, 5))
    
    rounds = df.index
    games = df["G"].astype(int)
 
    # creating the bar plot
    plt.bar(rounds.values, games.values, color ='maroon', 
            width = 0.4)
    
    plt.xlabel("Round drafted")
    plt.ylabel("No. of games played")
    plt.title(f"{team} games played per round drafted")
    plt.savefig(f"images/{team}_games_played_per_round_drafted.png")


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

def main():

    all_team_and_player_draft_data = get_all_team_draft_data()

    visualize(all_team_and_player_draft_data)

    store_old_draft_data(all_team_and_player_draft_data)


if __name__ == "__main__":
    main()
