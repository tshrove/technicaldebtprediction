import time
from dateutil.parser import parse

class StarGazer:
    ###
    # Public Methods
    ###
    def __init__(self):
        """ Default Constructor """
        ## Nothing to do.

    @staticmethod
    def normalize(star_list, start_date, end_date):
        if type(start_date) is str:
            start_date = parse(start_date)

        if type(end_date) is str:
            end_date = parse(end_date)

        total_time = StarGazer.__differenceofdates(end_date, start_date)
        for star in star_list:
            norm_star = StarGazer.__differenceofdates(star.event_date, start_date)
            percentage = norm_star / total_time
            star.normalized_percentage_temp = percentage
        return star_list

    @staticmethod
    def __datetotimestamp(date):
        timestamp = int(time.mktime(date.timetuple()))
        return timestamp

    @staticmethod
    def __differenceofdates(date1, date2):
        date1_ts = StarGazer.__datetotimestamp(date1)
        date2_ts = StarGazer.__datetotimestamp(date2)
        return date1_ts - date2_ts
