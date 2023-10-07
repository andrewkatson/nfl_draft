
import pandas as pd
import re

import common
import constants
import flags


def get_sportrac_data_for_team(name):

    years_in_range = common.get_all_years_in_range()

    all_players_all_years = pd.DataFrame(columns=[
        "Team", "Abbreviation", "Year", "Player", "Rnd", "AP1", "PB", "St", "G"], dtype=str)

    for year in years_in_range:
        hypenated_name = common.invert(
            constants.SPORTRAC_TEAM_ABBREVIATIONS)[name]

        url = f"{constants.UNDRAFTED_FREE_AGENT_BASE_URL}/{year}/{hypenated_name}/"

        table_dfs = common.get_tables_from_url(url)

        if table_dfs is None:
            print(f"{url} did not exist or had some error")
            continue

        for table_df in table_dfs:

            table_df = table_df.filter(regex=("Player*"))
                        
            table_df.columns.values[0] = "Player"
            
            table_df = table_df.assign(Year=year)
            
            table_df = table_df.assign(Team=name)
            
            table_df = table_df.assing(Rnd="UDFA")

            all_players_all_years = common.concat_with_identical_cols(
                all_players_all_years, table_df)

    print(all_players_all_years.head())


get_sportrac_data_for_team("New England Patriots")
