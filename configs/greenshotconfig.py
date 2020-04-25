from .iconfig import IConfig


class GreenshotConfig(IConfig):
    __priority_val_dict = {
        "Blocker": 5,
        "Critical": 4,
        "Major": 3,
        "Minor": 2,
        "Trivial": 1
    }

    __issue_tracker_type = 'jira'
    __jira_url = 'https://greenshot.atlassian.net'
    __jira_username = ''
    __jira_password = ''

    __projects = [{'key': 'BUG', 'start_date': '2007-03-28T00:00:00.000-0500', 'end_date': '2019-01-28T00:00:00.000-0500',
                 'success': 'true', 'prediction_type': 'train'}]
    #__issue_types = ['Bug']

    def __init__(self):
        super().__init__()

    def get_priority_values(self):
        return self.__priority_val_dict

    def get_jira_url(self):
        return self.__jira_url

    def get_jira_username(self):
        return self.__jira_username

    def get_jira_password(self):
        return self.__jira_password

    def get_resolved_statuses(self):
        return self.__resolved_statuses

    def get_projects(self):
        return self.__projects

    def get_issuetypes(self):
        return self.__issue_types

    def get_issuetrackertype(self):
        return self.__issue_tracker_type
