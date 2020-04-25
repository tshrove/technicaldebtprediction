from .tdevent import TDEvent
from .ieventlist import IEventList


class TDEventList(IEventList):
    ###
    # Private Variables
    ###
    _events = []

    def __init__(self, raw_jira_issues):
        self._events = []
        self.__parse_issue_list(raw_jira_issues)

    def __parse_issue_list(self, jira_issues):
        try:
            self._events = []
            for issue in jira_issues:
                if issue.fields.resolutiondate is not None:
                    # One for resolved event
                    _tdresolvedevent = TDEvent(jira_issue=issue, is_resolved=True)
                    self._events.append(_tdresolvedevent)

                # One for created event
                _tdcreatedevent = TDEvent(jira_issue=issue, is_resolved=False)
                self._events.append(_tdcreatedevent)
            return True
        except:
            print("Error occured on parsing jira issues")
            return False

    @property
    def events(self):
        return self._events
