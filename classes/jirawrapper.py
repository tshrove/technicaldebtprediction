from jira import JIRA
from dateutil.parser import parse
from .iwrapper import IWrapper


class JIRAWrapper (IWrapper):

    ###
    # Private Variable
    ###
    __issue_types = ""


    ###
    # Public Methods
    ###
    def __init__(self, jira_url, jira_username, jira_password):
        """ Default Constructor """
        self.__issue_types = ""
        options = {'server': jira_url, 'verify': False}
        if jira_username is not '' and jira_password is not '':
            self.jira = JIRA(options=options, basic_auth=(jira_username, jira_password))
        if jira_username is '' and jira_password is '':
            self.jira = JIRA(options=options)

    def get_data(self, project_key, issues_type_str=None, from_date_str=None, to_date_str=None):
        """ Function used to set the data in the class by the parameters """
        self.issue_types = issues_type_str

        """ Start building the query string """
        query_str = 'project = ' + project_key

        """ Check to see if the issue type exist and not empty before adding it to the query. """
        if bool(issues_type_str and issues_type_str.strip()):
            issues_type_list = issues_type_str.split(",")
            query_str += ' AND issuetype in ('
            issues_type_list = ['"' + issue.strip() + '"' for issue in issues_type_list]
            for issue_type in issues_type_list:
                query_str += issue_type + ", "
            query_str = query_str[:-2]
            query_str += ')'

        """ Check to see if the from date exist and not empty before adding it to the query. """
        if bool(from_date_str and from_date_str.strip()):
            if type(from_date_str) is str:
                _fd = parse(from_date_str).strftime('%Y-%m-%d %H:%M')
                query_str += ' AND created >= "' + _fd + '"'

        """ Check to see if the to date exist and not empty before adding it to the query. """
        if bool(to_date_str and to_date_str.strip()):
            if type(to_date_str) is str:
                _td = parse(to_date_str).strftime('%Y-%m-%d %H:%M')
                query_str += ' AND created < "' + _td + '"'

        """ Add the ordering by clause """
        query_str += ' ORDER BY created ASC'

        """ Sets the issues from jira """
        return self.get_data_by_query(query_str)

    def get_data_by_query(self, query_str):
        """ Get the issues from jira by query string"""
        proj_issues = self.jira.search_issues(query_str, 0, -1, True,
                                              'key, summary, "issuetype", status, priority, created, resolutiondate',
                                              True, False)
        # added this in order to account for jira's limitation on max results for api calls.
        total = proj_issues.total
        length = len(proj_issues)
        while len(proj_issues) < total:
            """ Get the issues from jira by query string"""
            _issues = self.jira.search_issues(query_str, len(proj_issues), -1, True,
                                                  'key, summary, "issuetype", status, priority, created, resolutiondate',
                                                  True, False)
            proj_issues += _issues
        return proj_issues
