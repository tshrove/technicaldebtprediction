from .iconfig import IConfig


class MongoDBConfig(IConfig):
    __priority_val_dict = {
        "Blocker - P1": 5,
        "Critical - P2": 4,
        "Major - P3": 3,
        "Minor - P4": 2,
        "Trivial - P5": 1
    }

    __issue_tracker_type = 'jira'
    __jira_url = 'https://jira.mongodb.org'
    __jira_username = ''
    __jira_password = ''

    __projects = [
        {'key': 'NODE', 'start_date': '2010-01-07T00:00:00.000-0500', 'end_date': '2019-02-11T00:00:00.000-0500',
         'success': '-1', 'prediction_type': 'train', 'github': 'mongodb/node-mongodb-native'},
        {'key': 'CSHARP', 'start_date': '2010-02-12T00:00:00.000-0500', 'end_date': '2019-02-11T00:00:00.000-0500',
         'success': '-1', 'prediction_type': 'train', 'github': 'mongodb/mongo-csharp-driver'},
        {'key': 'JAVA', 'start_date': '2009-01-15T00:00:00.000-0500', 'end_date': '2019-02-11T00:00:00.000-0500',
         'success': '-1', 'prediction_type': 'train', 'github': 'mongodb/mongo-java-driver'},
        {'key': 'PYTHON', 'start_date': '2009-01-15T00:00:00.000-0500', 'end_date': '2019-02-11T00:00:00.000-0500',
         'success': '-1', 'prediction_type': 'train', 'github': 'mongodb/mongo-python-driver'},
        {'key': 'RUBY', 'start_date': '2009-01-15T00:00:00.000-0500', 'end_date': '2019-02-11T00:00:00.000-0500',
         'success': '-1', 'prediction_type': 'train', 'github': 'mongodb/mongo-ruby-driver'},
        {'key': 'CDRIVER', 'start_date': '2009-12-03T00:00:00.000-0500', 'end_date': '2019-02-11T00:00:00.000-0500',
         'success': '-1', 'prediction_type': 'train', 'github': 'mongodb/mongo-c-driver'},
        {'key': 'PERL', 'start_date': '2009-03-05T00:00:00.000-0500', 'end_date': '2019-02-11T00:00:00.000-0500',
         'success': '-1', 'prediction_type': 'train', 'github': 'mongodb/mongo-perl-driver'}
    ]

    # __issue_types = ['Bug']

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
