from .iprojectevent import IProjectEvent
from .tdevent import TDEvent
from dateutil.parser import parse


class ProjectTDEvent(IProjectEvent, TDEvent):

    ###
    # Private Variables
    ###
    __project_start_date = None
    __project_end_date = None
    __cumlative_event_value = None

    ###
    # Public Methods
    ###
    def __init__(self, jira_issue, is_resolved):
        TDEvent.__init__(self, jira_issue=jira_issue, is_resolved=is_resolved)

    @property
    def project_percentage(self):
        _project_date_diff = self.__days_between(self.__project_start_date, self.__project_end_date)
        _event_date = self.event_date
        _project_event_diff = self.__days_between(_event_date, self.__project_start_date)
        return _project_event_diff / _project_date_diff

    @property
    def cumlative_value(self):
        return self.__cumlative_event_value

    @cumlative_value.setter
    def cumlative_value(self, value):
        self.__cumlative_event_value = value

    def set_project_dates(self, startdate, enddate):
        self.__project_start_date = startdate
        self.__project_end_date = enddate

    def to_dict(self):
        return {
            'value': self.event_value,
            'date': self.event_date,
            'project_percentage': self.project_percentage
        }

    ###
    # Private Methods
    ###
    def __days_between(self, d1, d2):
        if type(d1) is str:
            d1 = parse(d1)
        if type(d2) is str:
            d2 = parse(d2)
        return abs((d2 - d1).days)
