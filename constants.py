NFL_DRAFT_BASE_URL = "https://www.pro-football-reference.com/teams"

UNDRAFTED_FREE_AGENT_BASE_URL = "https://www.spotrac.com/nfl/undrafted-free-agents"

PFR_PLAYER_SCRAPING_BASE_URL = "https://www.pro-football-reference.com/players"

TEAMS_ABBREVIATIONS = {"nwe": "New England Patriots", "buf": "Buffalo Bills",
                       "mia": "Miami Dolphins", "nyj": "New York Jets", "clt": "Indianapolis Colts",
                       "htx": "Houston Texans", "jax": "Jacksonville Jaguars", "oti": "Tennessee Titans", "rav": "Baltimore Ravens",
                       "cle": "Cleveland Browns", "pit": "Pittsburgh Steelers", "cin": "Cincinnati Bengals",
                       "kan": "Kansas City Chiefs", "sdg": "Los Angeles Chargers", "den": "Denver Broncos",
                       "rai": "Las Vegas Raiders", "phi": "Philadelphia Eagles", "dal": "Dallas Cowboys",
                       "was": "Washington Commanders", "nyg": "New York Giants", "tam": "Tampa Bay Buccaneers",
                       "atl": "Atlanta Falcons", "nor": "New Orleans Saints", "car": "Carolina Panthers",
                       "det": "Detroit Lions", "gnb": "Green Bay Packers", "min": "Minnesota Vikings",
                       "chi": "Chicago Bears", "sfo": "San Francisco 49ers", "sea": "Seattle Seahawks",
                       "ram": "Los Angeles Rams", "crd": "Arizone Cardinals"}

SPORTRAC_TEAM_ABBREVIATIONS = {"arizona-cardinals": "Arizona Cardinals", "atlanta-falcons": "Atlanta Falcons", "baltimore-ravens": "Baltimore Ravens",
                               "buffalo-bills": "Buffalo Bills", "carolina-pathers": "Carolina Panthers", "chicago-bears": "Chicago Bears",
                               "cincinnati-bengals": "Cincinnati Bengals", "cleveland-browns": "Cleveland Browns", "dallas-cowboys": "Dallas Cowboys",
                               "denver-broncos": "Denver Broncos", "detroit-lions": "Detroit Lions", "green-bay-packers": "Green Bay Packers",
                               "houston-texans": "Houston Texans", "indianapolis-colts": "Indianapolis Colts", "jacksonville-jaguars": "Jacksonville Jaguars",
                               "kansas-city-chiefs": "Kansas City Chiefs", "las-vegas-raiders": "Las Vegas Raiders", "los-angeles-chargers": "Los Angeles Chargers",
                               "los-angeles-rams": "Los Angeles Rams", "miami-dolphins": "Miami Dolphins", "minnesota-vikings": "Minnesota Vikings",
                               "new-england-patriots": "New England Patriots", "new-orleans-saints": "New Orleans Saints", "new-york-giants": "New York Giants",
                               "new-york-jets": "New York Jets", "philadelphia-eagles": "Philadelphia Eagles", "pittsburgh-steelers": "Pittsburgh Steelers",
                               "san-francisco-49ers": "San Francisco 49ers", "seattle-seahawks": "Seattle Seahawks", "tampa-bay-buccaneers": "Tampa Bay Buccaneers",
                               "tennessee-titans": "Tennessee Titans", "washington-commanders": "Washington Commanders"}

OLD_DRAFT_DATA_PATH = "old_draft_data.pkl"

PLAYER_MASTER_DF = "players/players.pkl"

PLAYER_URL_DF = "players/player_urls.pkl"

COLS_TO_SELECT = ["Team", "Abbreviation", "Year",
                  "Rnd", "Player", "AP1", "PB", "St", "G"]

GENERAL_COLS = ["Year", "Age", "Tm", "Pos", "No."]
