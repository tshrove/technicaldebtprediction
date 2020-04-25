from dateutil.parser import parse
from configs import ConfigFactory

config = ConfigFactory.factory()


class TDEvent:

    ###
    # Private Variables
    ###
    __raw_issue = None
    __is_resolved = None

    ###
    # Public Methods
    ###
    def __init__(self, jira_issue, is_resolved):
        self.__raw_issue = jira_issue
        self.__is_resolved = is_resolved

    @property
    def event_value(self):
        if self.__raw_issue.fields.priority is not None:
            _event_val = TDEvent.get_debt_value(self.__raw_issue.fields.priority.name)
        else:
            _event_val = 3

        if self.__is_resolved:
            return _event_val * -1
        else:
            return _event_val


    @property
    def event_date(self):
        if self.__is_resolved is True:
            return self.__getresolveddate()
        else:
            return self.__getcreateddate()

    ###
    # Private Methods
    ###
    def __getresolveddate(self):
        if self.__raw_issue.fields.resolutiondate is not None:
            return parse(self.__raw_issue.fields.resolutiondate)
        else:
            return None

    def __getcreateddate(self):
        return parse(self.__raw_issue.fields.created)

    ###
    # Static Methods
    ###
    @staticmethod
    def get_debt_value(priority_val_str):
        """ Gets the amount of technical debt related to the issue. """
        _val = config.get_priority_values()[priority_val_str]
        return _val
