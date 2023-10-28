import mysql.connector as sql
import mysql.connector.errors


class SQL:
    def __init__(self):
        # initial sql setup
        self.db = sql.connect(
            host="localhost",
            user="root",
            password="PhilliesRule0514!",
            database="pitchers"
        )
        self.table_name = "Pitchers"
        self.cursor = self.db.cursor()
        self.cursor.execute("SHOW TABLES")
        results = self.cursor.fetchall()
        for x in results:
            print(x)

    def get_pitchers(self):
        self.cursor.execute("SELECT * FROM Pitchers")
        results = self.cursor.fetchall()
        return results

    def get_pitcher_by_index(self, index):
        self.cursor.execute(f"SELECT {index} FROM Pitchers")
        results = self.cursor.fetchall()
        return results

    def add_pitcher(self, pitcher):
        if pitcher.jersey_num is None:
            pitcher.jersey_num = 0
        try:
            self.cursor.execute(f"INSERT INTO {self.table_name} "
                                f"(PlayerID, FirstName, LastName, Position, Team, Birthplace, Handedness, JerseyNum)\n"
                                f"VALUES ({pitcher.id}, \'{pitcher.first}\', \'{pitcher.last}\', \'{pitcher.position}\', "
                                f"\'{pitcher.team}\', \'{pitcher.birthplace}\', "
                                f"\'{pitcher.handedness}\', {pitcher.jersey_num})")
            self.db.commit()
        except mysql.connector.errors.IntegrityError as e:
            print(e)

    def update_table(self, pitcher_list):
        for pitcher in pitcher_list:
            self.cursor.execute(f"UPDATE {self.table_name} "
                                f"SET LastName = {pitcher.last}"
                                f"FirstName = {pitcher.first}"
                                f"Position = {pitcher.position}"
                                f"Team = {pitcher.team}"
                                f"Birthplace = {pitcher.birthplace}"
                                f"Handedness = {pitcher.handedness}"
                                f"JerseyNum = {pitcher.jersey_num}"
                                f"WHERE PlayerID = {pitcher.id}")
            self.db.commit()