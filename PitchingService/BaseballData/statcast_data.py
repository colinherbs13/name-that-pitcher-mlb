import pybaseball as pb
from datetime import date

from django.db import transaction

import PitchingService.BaseballData.pitcher_db as db
import requests

# CONSTANTS
OPENING_DAY = '2026-03-26'
TODAY = str(date.today())

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
    'PO': '4-Seam Fastball',
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
    player_name = player_name.replace('\\xc3\\xa9', u'\u00e9')
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

    def __init__(self, raw_stats={}, db_init=False):
        """
        Constructor for Player class, sets attributes and calls some functions to set specific attributes
        :param raw_stats: When creating player objects, we first must gather baseball reference data to obtain
        player information
        """
        self.position = None
        self.last = None
        self.first = None
        self.pitches = []
        # fields set by set_personal_attributes function
        self.team = None
        self.birthplace = None
        self.handedness = None
        self.jersey_num = None
        self.age = 0
        self.awards = []

        # if we gather the player information from the DB
        if db_init:
            self.id = db_init['id']
            self.name = db_init['name']
            self.position = db_init['position']
            self.team = db_init['team']
            self.birthplace = db_init['country']
            self.handedness = db_init['handedness']
            self.jersey_num = db_init['jerseynum']
            self.age = db_init['age']
        else:
            self.raw_stats = raw_stats
            self.id = raw_stats['mlbID']
            self.age = raw_stats['Age']
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
        ret += "Name" + self.name + "\n"
        ret += "Team: " + self.team + "\n"
        ret += "Position " + self.position + "\n"
        ret += "ID: " + str(self.id) + "\n\n"
        ret += "Pitches: " + "\n"
        for i in range(len(self.pitches)):
            ret += str(self.pitches[i]) + "\n"
        return ret

    def __dict__(self):
        return {
            "id": self.id,
            "name": self.name,
            "jersey_number": self.jersey_num,
            "team": self.team,
            "age": self.age,
            "birthplace": self.birthplace,
            "position":  self.position,
            "handedness": self.handedness
        }

    def upsert_db_entry(self):
        existing_pitchers = db.Pitcher.objects.filter(id=self.id).update(comments_on=False)
        # if update fails
        if existing_pitchers == 0:
            db.Pitcher.objects.create(**self.__dict__, comments_on=False)

    def delete_db_entry(self):
        try:
            db.Pitcher.objects.delete(id=self.id)
        except Exception as e:
            print("Failed to delete Player. ID: " + self.id)

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
            try:
                index = pitches.index(pitches[j])
                pitch = Pitch(self.id, PITCH_TYPES[pitches[j]], velocities[index], spins[index], locations[index], zones[index])
                self.pitches.append(pitch)
            except KeyError:
                continue
        return self.pitches

    def set_position(self):
        """
        Determines the position of the pitcher based on MLB qualifications and sets self.position attribute
        :return: None
        """
        games = self.raw_stats['G']
        starts = self.raw_stats['GS']
        innings = self.raw_stats['IP']
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
            # Accounts for starters who made minimal starts due to injury, but go > 5 innings per appearance
            if innings / games >= 5:
                self.position = "SP"
                return
            # default to reliever role
            self.position = "RP"
            return

    def set_name(self):
        """
        Gets name from raw stats and calls _modify_utf_chars to replace special characters
        :return: None
        """
        last = " ".join(self.raw_stats['Name'].split()[1:])
        first = self.raw_stats['Name'].split()[0]
        last = _modify_utf_chars(last)
        first = _modify_utf_chars(first)
        self.name = f'{first} {last}'

    def set_personal_attributes(self):
        """
        Gets team from raw_stats.
        Since fangraphs only returns city names, determine abbreviation from presets as well as proper team name from
        league returned from fangraphs data. (EX: LAA/LAD, NYY/NYM)
        :return:
        """
        try:
            team_response = requests.get("https://statsapi.mlb.com/api/v1/people/" + self.id + "?hydrate=currentTeam")
            print(team_response)
        except requests.HTTPError as err:
            print("ERROR GETTING PLAYER INFO: " + err.errno)
            return
        team_data = team_response.json()["people"][0]
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
            awards_response = requests.get(f"https://statsapi.mlb.com/api/v1/people/{str(self.id)}?hydrate=awards")
        except requests.HTTPError as err:
            print("ERROR GETTING PLAYER AWARDS: " + err.errno)
            return
        try:
            awards_data = awards_response.json()["people"][0]["awards"]
            print(awards_data)
        except KeyError as key_err:
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

    def __init__(self, player_id, p_type, velo, spin, loc, zone):
        """
        Constructor for Pitch class, sets attributes passed in when player pitch arsenal is gathered.
        :param p_type: pitch type
        :param velo: average velocity
        :param spin: average spin rate
        """
        self.player_id = player_id
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

    def __dict__(self):
        return {
            "id": self.p_type + "_" + str(self.player_id),
            "player_id": self.player_id,
            "pitch_type": self.p_type,
            "velocity": self.velo,
            "spin": self.spin,
            "location": self.locations,
            "zone": self.zone
        }

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


def populate_pitcher_db():
    pitcher_data = pb.pitching_stats_bref(2026)
    existing_ids = set(
        db.Pitcher.objects.filter(id__in=pitcher_data['mlbID'].tolist())
        .values_list('id', flat=True)
    )
    records = pitcher_data.to_dict(orient='records')
    players = []
    with transaction.atomic():
        for row in records:
            # Check if the pitcher already exists in your database
            is_existing = row['mlbID'] in existing_ids

            # Instantiate with your required db_init parameter
            p = Player(row, db_init=is_existing)
            p.set_pitch_arsenal()
            players.append(p.__dict__())
            print(f"Provisioned {row['Name']}")
            new_pitcher, _ = db.Pitcher.objects.update_or_create(
                **players[-1]
            )
            print(p.pitches)

            for pitch in p.pitches:
                pitch_data = pitch.__dict__()

                db.PitchingStats.objects.update_or_create(
                    **pitch_data
                )