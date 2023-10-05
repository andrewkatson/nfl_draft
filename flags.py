import argparse
import datetime

today = datetime.date.today()
today_formatted = today.strftime('%Y-%m-%d')


parser = argparse.ArgumentParser(
    prog='NflDraftAnalyzer',
    description='It validates the draft history of teams in the NFL',
    epilog='Please take this with a grain of salt')

parser.add_argument('--first_date', default="2000-01-01",
                    help='The date in YYYY-MM-DD format that you want the data to start at. Exclusive. 2000-01-01 is default.')

parser.add_argument('--last_date', default=today_formatted,
                   help='The end date in YYYY-MM-DD format that you want the data to end at. Exclusive. Today is default.')

parser.add_argument('--included_teams', default='all',
                    help='The list of abbreviated included teams you want. This goes by Pro Football Reference abbreviations. All is the default')

parser.add_argument('--rounds_to_consider', default='all',
                   help='What rounds you want to consider for the analysis. All is the default.')

parser.add_argument('--fresh_data', default='no', help='Whether you want fresh data or we can read from our db. Default is no')

args = parser.parse_args()
