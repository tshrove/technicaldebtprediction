from .projecttdevent import ProjectTDEvent
from .tdeventlist import TDEventList
from .ieventlist import IEventList
import pandas as pd
import numpy as np


class ProjectEventList(TDEventList, IEventList):

    ###
    # Private Variables
    ###
    __start_date = None
    __end_date = None

    ###
    # Public Methods
    ###

    def __init__(self, raw_jira_issues, start_date, end_date):
        self.__start_date = start_date
        self.__end_date = end_date
        self.__parse_issue_list(raw_jira_issues)

    def set_project_dates(self, start_date, end_date):
        self.__start_date = start_date
        self.__end_date = end_date
        for event in self._events:
            event.set_project_dates(startdate=self.__start_date, enddate=self.__end_date)

    def sort(self):
        self._events = sorted(self._events, key=lambda event: event.project_percentage)

    @property
    def cumlative_events(self):
        _sorted_events = sorted(self._events, key=lambda event: event.project_percentage)
        _cumlative_sorted_events = []
        total = 0
        for e in _sorted_events:
            total += e.get_event_value
            e.cumlative_value = total
            _cumlative_sorted_events.append(e)

        return _cumlative_sorted_events

    def cumlative_event_totals(self, by='project_percentage'):
        _agg = self.__get_aggregated_dataframe_by(by=by)
        _value_dict = _agg.to_dict()
        # remove the first dictionary
        _value_dict = _value_dict['value']
        # value used to hold the total value
        _total = 0
        for key, value in _value_dict.items():
            _total += value
            _value_dict[key] = _total

        return _value_dict

    def get_cumlative_totals_by_bins(self, number_of_bins):
        _df = self.__get_dataframe_with_sorted_events()
        """ Check for the parameter being an int value """
        if type(number_of_bins) is str:
            number_of_bins = int(number_of_bins)
        _bin_list = np.linspace(start=0.0, stop=1.0, num=(number_of_bins + 1))
        _bins = pd.cut(_df['project_percentage'], _bin_list)
        _df = _df.groupby(_bins)['value'].agg(['sum'])
        _values = _df.to_dict()['sum']
        _values = list(list(np.cumsum(_values))[0].values())
        _values = list(np.cumsum(_values))
        _value_dict = dict(zip(_bin_list[1:], _values))
        return _value_dict

    ###
    # Private Methods
    ###
    def __parse_issue_list(self, jira_issues):
        if self.__start_date is not None or self.__end_date is not None:
            self._events = []
            for issue in jira_issues:
                if issue.fields.resolutiondate is not None:
                    # One for resolved event
                    _tdresolvedevent = ProjectTDEvent(jira_issue=issue, is_resolved=True)
                    _tdresolvedevent.set_project_dates(startdate=self.__start_date, enddate=self.__end_date)
                    self._events.append(_tdresolvedevent)

                # One for created event
                _tdcreatedevent = ProjectTDEvent(jira_issue=issue, is_resolved=False)
                _tdcreatedevent.set_project_dates(startdate=self.__start_date, enddate=self.__end_date)
                self._events.append(_tdcreatedevent)
            return True
        else:
            print('No start or end date values')
            return False

    def __get_dataframe_with_sorted_events(self):
        _sorted_events = sorted(self._events, key=lambda event: event.project_percentage)
        _df = pd.DataFrame.from_records([e.to_dict() for e in _sorted_events])
        return _df

    def __get_aggregated_dataframe_by(self, by='project_percentage'):
        _df = self.__get_dataframe_with_sorted_events()
        _group = _df.groupby(by)
        _agg = _group.aggregate({'value': np.sum})
        return _agg
