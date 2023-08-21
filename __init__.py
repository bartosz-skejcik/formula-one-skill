from adapt.intent import IntentBuilder

from mycroft import MycroftSkill, intent_handler
from datetime import datetime
from dateutil import tz
import requests


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


def get_weekday(date):
    date = date.split('-')
    return datetime(int(date[0]), int(date[1]), int(date[2])).strftime('%A')


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
        'weekday': get_weekday(upcoming_race["FirstPractice"]["date"]),
        'date': upcoming_race["FirstPractice"]["date"],
        'time': convert_to_local_time(upcoming_race["FirstPractice"]["time"])
    }
    practice2 = {
        'weekday': get_weekday(upcoming_race["SecondPractice"]["date"]),
        'date': upcoming_race["SecondPractice"]["date"],
        'time': convert_to_local_time(upcoming_race["SecondPractice"]["time"])
    }
    practice3 = {
        'weekday': get_weekday(upcoming_race["ThirdPractice"]["date"]),
        'date': upcoming_race["ThirdPractice"]["date"],
        'time': convert_to_local_time(upcoming_race["ThirdPractice"]["time"]),
    }
    quali = {
        'weekday': get_weekday(upcoming_race["Qualifying"]["date"]),
        'date': upcoming_race["Qualifying"]["date"],
        'time': convert_to_local_time(upcoming_race["Qualifying"]["time"])
    }
    race = {
        'weekday': get_weekday(upcoming_race["date"]),
        'date': upcoming_race["date"],
        'time': convert_to_local_time(upcoming_race["time"]),
    }

    return {
        'practice1date': practice1['date'],
        'practice1time': practice1['time'],
        'practice2date': practice2['date'],
        'practice2time': practice2['time'],
        'practice3date': practice3['date'],
        'practice3time': practice3['time'],
        'qualidate': quali['date'],
        'qualitime': quali['time'],
        'racedate': race['date'],
        'racetime': race['time']
    }


class FormulaOne(MycroftSkill):
    def __init__(self):
        MycroftSkill.__init__(self)

    @intent_handler(IntentBuilder('RaceInformation').one_of("F1").require("Race").one_of("TimeSpecification").one_of("Time"))
    def handle_race_information(self, message):
        weekday = get_weekday(get_upcoming_race()['date'])
        date = get_upcoming_race()['date']
        location = get_upcoming_race()['Circuit']['Location']['locality']
        raceTime = convert_to_local_time(get_upcoming_race()['time'])
        self.speak_dialog(
            'one.formula', {'date': date, 'location': location, 'raceTime': raceTime, 'raceweekday': weekday})

    @intent_handler(IntentBuilder("ScheduleInfo").optionally("F1").one_of("Schedule").one_of("Race").one_of("TimeSpecification"))
    def handle_schedule_info(self, message):
        schedule = get_schedule()
        print(schedule)
        self.speak_dialog('one.schedule', schedule)


def create_skill():
    return FormulaOne()
