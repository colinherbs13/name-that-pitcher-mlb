import math

import pybaseball as pb
from datetime import date

OPENING_DAY = '2023-03-30'
TODAY = date.today()
PITCH_TYPES = {
    'FF': '4-Seam Fastball',
    'CU': 'Curveball',
    'ST': 'Sweeper',
    'SL': 'Slider',
    'SV': 'Slurve',
    'SI': 'Sinker',
    'CH': 'Changeup',
    'KN': 'Knuckleball',
    'FS': 'Split Finger',
    'FC': 'Cutter',
    'FO': 'Forkball',
    'KC': 'Knuckle Curve'
}
PROBLEMATIC_IDS = {
    "J.P. France": 641585,
    "Michael King": 650633,
    "Luis L. Ortiz": 682847,
    "Matthew Boyd": 571510,
    "Mark Leiter Jr.": 643410,
    "A.J. Minter": 621345,
    "A.J. Puk": 640462,
    "Daniel Lynch IV": 663738,
    "Adrián Martínez": 661309,
    "JT Chargois": 608638,
    "Carl Edwards Jr.": 605218,
    "Jose A. Ferrer": 678606,
    "Duane Underwood Jr.": 621249,
    "Luis F. Ortiz": 656814
}


class Player:
    def __init__(self, last, first, id=0):
        self.last = last
        self.first = first
        self.pitches = []
        self.id = id

    def __str__(self):
        ret = "PLAYER INFO: \n"
        ret += "First Name: " + self.first + "\n"
        ret += "Last Name: " + self.last + "\n"
        ret += "ID: " + str(self.id) + "\n"
        ret += "Pitches: " + "\n"
        for i in range(len(self.pitches)):
            ret += str(self.pitches[i])
        return ret

    def get_pitch_arsenal(self):
        """
        Returns the pitch arsenal DataFrame for a specific player
        :param self: player object
        :return: Dataframe of pitch types
        """
        last = self.last.strip()
        first = self.first.strip()
        id = self.id
        if id == 0:
            print("No valid ID for player: " + last + " " + first + ". Returning.")
            return

        data = pb.statcast_pitcher(OPENING_DAY, TODAY, player_id=id)
        print(data.keys())
        pitches = []
        velocities = []
        spins = []
        for i in range(len(data)):
            pitch_data = data.iloc[i]
            pitch_type = pitch_data['pitch_type']
            pitch_velo = pitch_data['release_speed']
            pitch_spin = pitch_data['release_spin_rate']
            if pitch_type not in pitches:
                pitches.append(pitch_type)
                velocities.append((pitch_velo, 1))
                spins.append((pitch_spin, 1))
            else:
                velo_avg = velocities[pitches.index(pitch_type)][0]
                spin_avg = spins[pitches.index(pitch_type)][0]
                count = velocities[pitches.index(pitch_type)][1]
                count2 = spins[pitches.index(pitch_type)][1]

                # Some pitches may return nan for some data points, make sure we track only the pitches that have data
                if not math.isnan(pitch_spin):
                    spins[pitches.index(pitch_type)] = (
                        spin_avg + pitch_spin, count2 + 1)
                if not math.isnan(pitch_velo):
                    velocities[pitches.index(pitch_type)] = (velo_avg + pitch_velo, count + 1)

        # gather the averages into Pitch object and place it in player arsenal
        for j in range(len(pitches)):
            pitch = Pitch(PITCH_TYPES[pitches[j]], round((velocities[j][0] / velocities[j][1]), 1),
                          round((spins[j][0] / spins[j][1]), 1))
            self.pitches.append(pitch)
        self.id = id
        return pitches


class Pitch:
    def __init__(self, type, velo, spin):
        self.type = type
        self.velo = velo
        self.spin = spin

    def __str__(self):
        ret = "Pitch Type: " + self.type + "\n"
        ret += "Pitch Velo: " + str(self.velo) + "\n"
        ret += "Pitch Spin Rate: " + str(self.spin)
        return ret


if __name__ == '__main__':
    pitchers = pb.statcast_pitcher_pitch_arsenal(2023)
    players = []
    last = ""
    first = ""
    id = 0
    for i in range(len(pitchers)):
        last = pitchers['last_name'][i].strip()
        first = pitchers['first_name'][i].strip()
        try:
            id = pb.playerid_lookup(last, first)['key_mlbam'][0]
        except:
            print("Could not automatically get ID for player: " + first + " " + last)
            id = PROBLEMATIC_IDS[first + " " + last]
        p = Player(last, first, id)
        players.append(p)

