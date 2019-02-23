from datetime import datetime
from pytz import timezone

def time_or_date_in_place(location, return_time, return_date):
    if location == "None":
        location = "Australia"
    else:
        location = location
    place = datetime.now(timezone("Australia/Melbourne"))
    time_of_day = "am"
    dic = {"france": "Europe/Paris",
           "spain": "Europe/Madrid",
           "united_states": "America/Los_Angeles",
           "china": "Asia/Shanghai",
           "italy": "Europe/Rome",
           "mexico": "America/Mexico_City",
           "uk": "Europe/London",
           "turkey": "Turkey",
           "germany": "Europe/Berlin",
           "thailand": "Asia/Bangkok",
           "australia": "Australia/Canberra",
           "japan": "Japan",
           }

    if location == "None":
        place = datetime.now(timezone("Australia/Melbourne"))

    elif location == "france" or location == "paris":
        place = datetime.now(timezone(dic["france"]))

    elif location == "spain" or location == "madrid":
        place = datetime.now(timezone(dic["spain"]))

    elif location == "united states" or location == "los angeles" or location == "la" or location == "america" or location == "us":
        place = datetime.now(timezone(dic["united_states"]))

    elif location == "china" or location == "shanghai":
        place = datetime.now(timezone(dic["china"]))

    elif location == "italy" or location == "rome":
        place = datetime.now(timezone(dic["italy"]))

    elif location == "mexico" or location == "mexico city":
        place = datetime.now(timezone(dic["mexico"]))

    elif location == "uk" or location == "london" or location == "england" or location == "britain" or location == "great britain":
        place = datetime.now(timezone(dic["uk"]))

    elif location == "turkey" or location == "istanbul" or location == "ankara" or location == "adana":
        place = datetime.now(timezone(dic["turkey"]))

    elif location == "germany" or location == "berlin":
        place = datetime.now(timezone(dic["germany"]))

    elif location == "thailand" or location == "bangkok":
        place = datetime.now(timezone(dic["thailand"]))

    elif location == "australia" or location == "canberra":
        place = datetime.now(timezone(dic["australia"]))

    elif location == "japan":
        place = datetime.now(timezone(dic["japan"]))

    if return_time is False and return_date is True:
        date_time = place.strftime('%Y-%m-%d_%H-%M-%S')

        date = date_time[:10]
        print date
        year = date[:4]
        month = date[5:7]
        day = date[8:]

        if day == "01":
            day = "first"
        elif day == "02":
            day = "second"
        elif day == "03":
            day = "third"
        elif day == "04":
            day = "4"
        elif day == "05":
            day = "5"
        elif day == "06":
            day = "6"
        elif day == "07":
            day = "7"
        elif day == "08":
            day = "8"
        elif day == "09":
            day = "9"
        elif day == "21":
            day = "twenty first"
        elif day == "22":
            day = "twenty second"
        elif day == "23":
            day = "twenty third"
        elif day == "31":
            day = "thirty first"

        if month == "01":
            month = "first"
        elif month == "02":
            month = "second"
        elif month == "03":
            month = "third"
        elif month == "04":
            month = "4"
        elif month == "05":
            month = "5"
        elif month == "06":
            month = "6"
        elif month == "07":
            month = "7"
        elif month == "08":
            month = "8"
        elif month == "09":
            month = "9"
        else:
            pass

        if (month == "first" or month == "second" or month == "third") and (day == "first" or day == "second" or day == "third" or day == "twenty first" or day == "twenty second" or day == "twenty third" or day == "thirty first"):
            date_string = "The date in " + location + " is the " + day + " of the " + month + " " + year

        elif month == "first" or month == "second" or month == "third":
            date_string = "The date in " + location + " is the " + day + "th of the " + month + " " + year

        elif day == "first" or day == "second" or day == "third" or day == "twenty first" or day == "twenty second" or day == "twenty third" or day == "thirty first":
            date_string = "The date in " + location + " is the " + day + " of the " + month + "th " + year

        else:
            date_string = "The date in " + location + " is the " + day + "th of the " + month + "th " + year

        print date_string
        return date_string

    elif return_time is True and return_date is False:
        date_time = place.strftime('%Y-%m-%d_%H-%M-%S')
        current_time = date_time[11:16]
        print current_time
        hour = int(current_time[:2])
        minute = current_time[3:]
        if hour == 12:
            twelve_hour = 12
            time_of_day = "pm"
        elif hour > 12:
            twelve_hour = hour - 12
            time_of_day = "pm"
        else:
            twelve_hour = hour

        time_string = "The time in " + location + " is " + str(twelve_hour) + " " + str(minute) + " " + str(time_of_day)
        return time_string
