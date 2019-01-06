import mvg_api


def get_hauptbahnhof():
    return mvg_api.get_departures(6)
