import pybaseball as pb
from datetime import date
import pitcher_db as db
import requests

# CONSTANTS
OPENING_DAY = '2023-03-30'
TODAY = str(date.today())
database = db.SQL()

NATIONAL_LEAGUE = {
    'Arizona Diamondbacks': 'AZ',
    'Atlanta Falcons': 'ATL',
    'Chicago Cubs': 'CHC',
    'Cincinnati Reds': 'CIN',
    'Colorado Rockies': 'COL',
    'Los Angeles Dodgers': 'LAD',
    'Miami Marlins': 'MIA',
    'Milwaukee Brewers': 'MIL',
    'New York Mets': 'NYM',
    'Philadelphia Phillies': 'PHI',
    'Pittsburgh Pirates': 'PIT',
    'San Diego Padres': 'SD',
    'San Francisco Giants': 'SF',
    'St. Louis Cardinals': 'STL',
    'Washington Nationals': 'WSH'
}
AMERICAN_LEAGUE = {
    'Baltimore Orioles': 'BAL',
    'Boston Red Sox': 'BOS',
    'Chicago White Sox': 'CWS',
    'Cleveland Guardians': 'CLE',
    'Detroit Tigers': 'DET',
    'Houston Astros': 'HOU',
    'Kansas City Royals': 'KC',
    'Los Angeles Angels': 'LAA',
    'Minnesota Twins': 'MIN',
    'New York Yankees': 'NYY',
    'Oakland Athletics': 'OAK',
    'Seattle Mariners': 'SEA',
    'Tampa Bay Rays': 'TB',
    'Texas Rangers': 'TEX',
    'Toronto Blue Jays': 'TOR'
}
PITCH_TYPES = {
    'FF': '4-Seam Fastball',
    'FA': '4-Seam Fastball',
    'SI': 'Sinker',
    'FT': 'Sinker',
    'CU': 'Curveball',
    'CS': 'Curveball',
    'KC': 'Knuckle Curve',
    'ST': 'Sweeper',
    'SL': 'Slider',
    'SV': 'Slurve',
    'CH': 'Changeup',
    'KN': 'Knuckleball',
    'FS': 'Split Finger',
    'FC': 'Cutter',
    'FO': 'Forkball',
    'EP': 'Eephus',
    'GY': 'Gyroball',
    'SC': 'Screwball'
}


def _modify_utf_chars(player_name):
    """
    Takes in a player's name and replaces each special character with utf code for printing.
    Necessary due to how BaseballReference returns player names.
    :param player_name: Name of player to edit
    :return: returns modified player name with replaced characters
    """
    player_name = player_name.replace('\\xc3\\xb1', u'\u00f1')
    player_name = player_name.replace('\\xc3\\xa1', u'\u00e1')
    player_name = player_name.replace('\\xc3\\xad', u'\u00ed')
    player_name = player_name.replace('\\xc3\\xb3', u'\u00f3')
    player_name = player_name.replace('\\xc3\\xa9', 'u\u00e9')
    return player_name


class Player:
    """
    Player class references a selected pitcher
    Attributes - position(str): SP, RP, SP/RP (the pitcher's position based on MLB qualifications
    first, last(str): first and last name of player
    raw_stats(obj): Base stats gathered from BaseballReference (G, GS, Team, W/L, K's, etc)
    pitches(list): List of Pitch objects based on pitch arsenal. Empty until set_pitch_arsenal is called
    id(int): Statcast ID for player
    team(str): Player's current team abbreviation
    """

    def __init__(self, raw_stats):
        """
        Constructor for Player class, sets attributes and calls some functions to set specific attributes
        :param raw_stats: When creating player objects, we first must gather baseball reference data to obtain
        player information
        """
        self.position = None
        self.last = None
        self.first = None
        self.raw_stats = raw_stats
        print(self.raw_stats.keys())
        self.pitches = []
        self.id = raw_stats['mlbID']

        # fields set by set_personal_attributes function
        self.team = None
        self.birthplace = None
        self.handedness = None
        self.jersey_num = None
        self.awards = []

        # These functions set the strings for player name, player position, and player team
        self.set_name()
        self.set_position()
        self.set_personal_attributes()

    def __str__(self):
        """
        String representation of Player. Lists
        :return: returns string representation of player
        """
        ret = "PLAYER INFO: \n"
        ret += "First Name: " + self.first + "\n"
        ret += "Last Name: " + self.last + "\n"
        ret += "Team: " + self.team + "\n"
        ret += "Position " + self.position + "\n"
        ret += "ID: " + str(self.id) + "\n\n"
        ret += "Pitches: " + "\n"
        for i in range(len(self.pitches)):
            ret += str(self.pitches[i]) + "\n"
        return ret

    def set_pitch_arsenal(self):
        """
        Returns the pitch arsenal list for a specific player
        :param self: player object
        :return: List of Pitch objects containing pitch info
        """
        last = self.last
        first = self.first
        # if no ID found, we cannot search for pitch arsenal, so we return
        if self.id == 0:
            print("No valid ID for player: " + last + " " + first + ". Returning.")
            return

        # data contains data for every pitch thrown by player in current season
        data = pb.statcast_pitcher(str(OPENING_DAY), str(TODAY), player_id=self.id)
        pitches = []
        velocities = []
        spins = []
        locations = []
        zones = []
        print(data.keys())
        # iterate through each pitch and separate by type, velocity and spin rate
        for i in range(len(data)):
            pitch_data = data.iloc[i]
            pitch_type = pitch_data['pitch_type']
            pitch_velo = pitch_data['release_speed']
            pitch_spin = pitch_data['release_spin_rate']
            pitch_loc = (pitch_data['plate_x'], pitch_data['plate_z'])
            zone = (pitch_data['sz_top'], pitch_data['sz_bot'])

            # we need to check if we have already recorded pitch types, to calculate averages
            if pitch_type not in pitches:
                pitches.append(pitch_type)
                velocities.append([pitch_velo])
                spins.append([pitch_spin])
                locations.append([pitch_loc])
                zones.append([zone])
            else:
                index = pitches.index(pitch_type)
                velocities[index].append(pitch_velo)
                spins[index].append(pitch_spin)
                locations[index].append(pitch_loc)
                zones[index].append(zone)

        # calculate the averages into Pitch object and place it in player arsenal
        for j in range(len(pitches)):
            index = pitches.index(pitches[j])
            pitch = Pitch(PITCH_TYPES[pitches[j]], velocities[index], spins[index], locations[index], zones[index])
            self.pitches.append(pitch)
        return self.pitches

    def set_position(self):
        """
        Determines the position of the pitcher based on MLB qualifications and sets self.position attribute
        :return: None
        """
        games = self.raw_stats['G']
        starts = self.raw_stats['GS']
        # A pitcher is a qualified starter if they make 3 starts
        if starts >= 3:
            # some pitchers can be openers - check if they meet both starter and reliever requirements
            # relief eligibility is 5 appearances
            if games >= starts + 5:
                self.position = "SP/RP"
                return
            self.position = "SP"
            return
        else:
            # default to reliever role
            self.position = "RP"
            return

    def set_name(self):
        """
        Gets name from raw stats and calls _modify_utf_chars to replace special characters
        :return: None
        """
        self.last = " ".join(self.raw_stats['Name'].split()[1:])
        self.first = self.raw_stats['Name'].split()[0]
        self.last = _modify_utf_chars(self.last)
        self.first = _modify_utf_chars(self.first)

    def get_name(self):
        return self.first + " " + self.last

    def set_personal_attributes(self):
        """
        Gets team from raw_stats.
        Since fangraphs only returns city names, determine abbreviation from presets as well as proper team name from
        league returned from fangraphs data. (EX: LAA/LAD, NYY/NYM)
        :return:
        """
        try:
            team_response = requests.get("https://statsapi.mlb.com/api/v1/people/" + self.id + "?hydrate=currentTeam")
        except requests.HTTPError as err:
            print("ERROR GETTING PLAYER INFO: " + err.errno)
            return
        print(self.last + " " + self.first)
        team_data = team_response.json()["people"][0]
        print(team_data.keys())
        if "currentTeam" in team_data.keys():
            self.team = team_data["currentTeam"]["name"]
        if "birthCountry" in team_data.keys():
            self.birthplace = team_data["birthCountry"]
        if "pitchHand" in team_data.keys():
            self.handedness = team_data["pitchHand"]["code"]
        if "primaryNumber" in team_data.keys():
            self.jersey_num = team_data["primaryNumber"]

    def get_awards(self):
        try:
            awards_response = requests.get("https://statsapi.mlb.com/api/v1/people/" + self.id + "?hydrate=awards")
        except requests.HTTPError as err:
            print("ERROR GETTING PLAYER AWARDS: " + err.errno)
            return
        try:
            awards_data = awards_response.json()["people"][0]["awards"]
        except KeyError as key_err:
            print("Player " + self.id + " has no awards")
            self.awards = []
            return

        matches = ["WSCHAMP", "ALSS", "NLSS", "ALCY", "NLCY", "MLBAFIRST", "MLBASECOND", "ALAS", "NLAS", "NLGG", "ALGG",
                   "ALMVP", "NLMVP", "ASMVP", "ALROY", "NLROY", "WSMVP", "ALCSMVP", "NLCSMVP"]
        for award in awards_data:
            if any([x in award["id"] for x in matches]):
                self.awards.append(award["season"] + " " + award["name"])

        print(self.awards)


class Pitch:
    """
    Pitch class references a player's pitch
    Attributes - p_type(str): Pitch type
    velo(float): Average pitch velocity (MPH)
    spin(int): Average spin rate of pitch (RPM)
    """

    def __init__(self, p_type, velo, spin, loc, zone):
        """
        Constructor for Pitch class, sets attributes passed in when player pitch arsenal is gathered.
        :param p_type: pitch type
        :param velo: average velocity
        :param spin: average spin rate
        """
        self.p_type = p_type
        self.velo = self._set_average_of(velo)
        self.spin = self._set_average_of(spin)
        self.locations = loc
        self.zone = self._set_average_of(zone)

    def __str__(self):
        """
        String representation of Pitch object. Prints type, velocity, and spin rate.
        :return: ret: string representation of Pitch
        """
        ret = "Pitch Type: " + self.p_type + "\n"
        ret += "Pitch Velo: " + str(self.velo) + "\n"
        ret += "Pitch Spin Rate: " + str(self.spin) + "\n"
        ret += "Average Pitch Location: " + str(self._set_average_of(self.locations)) + "\n"
        ret += "Average Strike Zone: " + str(self.zone) + "\n"
        return ret

    def _set_average_of(self, ls):
        """
        sets the average of the given list ls
        :param ls: list of datapoints
        :return: returns average (either float or tuple depending on list)
        """
        ls = [x for x in ls if str(x) != 'nan']
        length = len(ls)
        if type(ls[0]) is tuple:
            sum_x = 0
            sum_y = 0
            for point in ls:
                sum_x += point[0]
                sum_y += point[1]
            return (sum_x / length, sum_y / length)
        else:
            return sum(ls) / len(ls)


class Statcast:
    """
    Statcast class is a container for players and their statistics
    Attributes - pitchers: list of active pitchers
    Public Methods - gather_pitchers(): used to gather active pitchers from bbref data
    """

    def __init__(self):
        self.pitchers = []
        self.gather_pitchers()

    def gather_pitchers(self):
        """
        Accesses baseball reference stats for pitchers this year and gathers data into pitchers list.
        Creates player objects for each pitcher as well.
        :return:
        """
        pitchers = pb.pitching_stats_bref(2023)
        players = []
        for i in range(len(pitchers)):
            pitcher = pitchers.iloc[i]
            p = Player(pitcher)
            database.add_pitcher(p)
            players.append(p)
        self.pitchers = players
