from datetime import datetime
import requests

from dateutil import tz


def convert_to_local_time(time):
    to_zone = tz.gettz('Poland/Warsaw')

    utc = datetime.strptime(time, '%H:%M:%SZ')

    local = utc.astimezone(to_zone)

    # add the 2 hours to the time
    local = local.replace(hour=local.hour + 2)

    return local.strftime('%H:%M')


def get_upcoming_race():
    url = 'http://ergast.com/api/f1'

    # Get the current season info
    r = requests.get(url + '/current.json')
    data = r.json()

    # get a list of races
    races = data['MRData']['RaceTable']["Races"]

    # there is a parameter to each race named date
    # we want to print out the race that is closest to today but not in the past

    upcoming = []

    for race in races:
        date = race['date'].split('-')
        if datetime(int(date[0]), int(date[1]), int(date[2])) >= datetime.now():
            upcoming.append(race)

    return upcoming[0]


def get_schedule():
    url = 'http://ergast.com/api/f1'

    # Get the current season info
    r = requests.get(url + '/current.json')
    data = r.json()

    # get a list of races
    races = data['MRData']['RaceTable']["Races"]

    upcoming = []

    for race in races:
        date = race['date'].split('-')
        if datetime(int(date[0]), int(date[1]), int(date[2])) >= datetime.now():
            upcoming.append(race)

    upcoming_race = upcoming[0]

    practice1 = {
        'date': upcoming_race["FirstPractice"]["date"],
        'time': convert_to_local_time(upcoming_race["FirstPractice"]["time"])
    }
    practice2 = {
        'date': upcoming_race["SecondPractice"]["date"],
        'time': convert_to_local_time(upcoming_race["SecondPractice"]["time"])
    }
    practice3 = {
        'date': upcoming_race["ThirdPractice"]["date"],
        'time': convert_to_local_time(upcoming_race["ThirdPractice"]["time"]),
    }
    quali = {
        'date': upcoming_race["Qualifying"]["date"],
        'time': convert_to_local_time(upcoming_race["Qualifying"]["time"])
    }
    race = {
        'date': upcoming_race["date"],
        'time': convert_to_local_time(upcoming_race["time"]),
    }

    return {
        'practice1': practice1,
        'practice2': practice2,
        'practice3': practice3,
        'quali': quali,
        'race': race
    }


print(get_schedule())
